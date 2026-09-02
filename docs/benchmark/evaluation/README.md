# The frozen evaluation layer

**Status: protocol version 4, frozen 2026-09-03.** `uv run allo evaluate verify --detect`
re-derives every pinned value and exits 0 only if nothing moved. **The bare form skips the
decoy half**, because pocket detection needs the structures, and it says so in its own output.
Corrected 2026-09-03: this line promised the whole re-derivation for the offline command. Version 1 was frozen and reopened on
2026-08-25 by an audit; version 2 was frozen the same day; version 3 opened on 2026-09-02, and
version 4 on 2026-09-03. **Section 0a below is what version 4 changes.** Every version number
in the body of this page below section 0a describes version 3 and is left as written.
**No method had been scored under version 2 for a reported result**, which is the only
condition under which this layer may move at all. Methods were run under version 2 — the
2026-08-26 sweep, the five gate controls — but every one of those is a development-tier
measurement or a control, and none is a claim this submission makes. Version 3 re-measures
the controls; §8 carries the new numbers.

> **Read [`../review/README.md`](../review/README.md) before quoting a number from this page.**
> An audit closed on 2026-09-02, after the organisers answered four questions about the
> benchmark. It ratifies most of this document, corrects four stated facts in it, and lists the
> decisions it forces. Corrections are recorded there rather than edited in here, so that this
> freeze stays a freeze.

The input layer answers **what** is scored: which structures, which residues, which labels,
which candidate set. It is frozen separately, in [`../README.md`](../primary/README.md). This layer
answers **how** a score is computed: which endpoint, which null, which decoys, which
decision rule. The two were one file until 2026-08-24. The coupling meant an unfinished
null model blocked a finished input layer, so they were split. Do not merge them back.

| File                                                                     | What it holds                                           |
| ------------------------------------------------------------------------ | ------------------------------------------------------- |
| [`manifest.yaml`](manifest.yaml)                                         | every pinned choice, with the reason beside it          |
| `frozen.json`                                                            | the consequences — chance lines, patch geometry, decoys |
| [`../evidence/evaluation-metrics.md`](../evidence/evaluation-metrics.md) | the literature basis for every choice                   |
| `experiments/2026-08-25-null-calibration/`                               | the v2 run that fixed the one free parameter            |
| `experiments/2026-09-02-null-recalibration/`                             | the v3 re-run, over six primary arms and fifteen in all |

**What this layer is for.** It makes methods comparable. Classical, quantum, AI and hybrid
methods all pass through one function, `allo.scoring.score_arm`, and none of them chooses
its own estimator, tie rule, null or replicate count. A quantum number that beats a
classical number computed differently is not evidence.

**Nothing here may change once a method is scored.** A threshold picked with results
in hand is a hyperparameter, not a protocol.

---

## 0a. What version 4 changes

Two changes, from the 2026-09-03 fourth pass
([`../review/27-fourth-pass-synthesis.md`](../review/27-fourth-pass-synthesis.md)). Neither
moves a pinned value: `frozen.json` changed only its version number and its date.

| #   | Change | Why it is not tuning |
| --- | --- | --- |
| 1   | **A family is cleared when Holm rejects at least one arm** (ADR 0038), and `confirmatory_verdict` returns `cleared` | The protocol declared two families, corrected each by Holm, and never said what clearing one is. This page held both readings: §8 and ADR 0030 read the combination test disjunctively, §13 printed one-of-three as a failure. Measured global-null familywise error of the disjunction is 0.0416 to 0.0457 against a nominal 0.05, which is what Holm controls. A conjunction is an intersection-union test and needs no multiplicity step at all, so freezing Holm implies the disjunction. **§13's "the positive control rejects on one of three" is a clearance, not a failure** |
| 2   | **Negative class (b) also scores the label set** (ADR 0039), reported as `label_p` beside `p` | `p` ranks the detector's site-pocket lining, and measured on the real linings a shift of four standard deviations on every label residue gives power 0 on KRAS and on cardiac myosin. Twelve myosin labels sit inside a 295-residue lining. `label_p` reaches 0.875 and 1.000 on the same fields. It is a **descriptive percentile and not a p-value**: over four null generators its size reaches 0.0548, with a 95 % interval above alpha, so it carries no rejection. `p` holds on all four. Both stay descriptive and neither enters a confirmatory family, so no bar moves |

**What did not change at version 4.** Every pinned value in `frozen.json`. The confirmatory
endpoint, the confirmatory family, the matched-patch tolerance, the detector and its settings,
alpha, and the decoy linings are all exactly as version 3 froze them.

---

## 0. What version 3 changes, and why it was allowed to change

Four questions went to the organisers and were answered on 2026-09-02
([`../review/00-official-reply.md`](../review/00-official-reply.md)). Their answers outrank
`CHALLENGE.md`. An audit of all three frozen layers followed
([`../review/README.md`](../review/README.md)). Six changes came out of it. Each names the ADR
that decided it, and the reason it is not a hyperparameter.

| #   | Change                                                                                                                                                                                                                                                                   | Why it is not tuning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **The input layer moved, so the calibration had to move with it.** `bcr_abl1_mandated` is now `1OPL` chain B (365 nodes, not 451) and `cardiac_myosin_mandated` is frozen for the first time. Both arms are recalibrated in `experiments/2026-09-02-null-recalibration/` | A threshold measured _after_ a method is scored is a hyperparameter. Nothing has been scored. Every unchanged arm must reproduce its 2026-08-25 value exactly, and any that does not is a finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 2   | **The decoy detector is re-frozen at `probe_out 8.0, removal_distance 1.2, volume_cutoff 1.0`**, selecting on `n_decoys` alone (ADR 0030)                                                                                                                                | The organisers answered that no detector is prescribed and each team defines its own decoy set, which removed the reason to hold the v2 defaults fixed. **CORRECTED 2026-09-02: this cell said `n_decoys` is label-free and that is false.** `decoys.classify` picks the site pocket by maximum label coverage and admits a decoy only when its lining holds no label, so the count is a function of the answer key. The label-free criterion is `n_detected`, the pocket count before any label is consulted, and it selects the identical setting on all five arms with no tie — so the freeze does not move, only the justification. Site coverage improved as a consequence and was never the selection target |
| 3   | **The pocket-rank test stays descriptive, and a Fisher combination across the three confirmatory arms is added as `decoy_pockets_combined`** (ADR 0030)                                                                                                                  | Per arm the p-value floor is `1/(1 + n_decoys)`, so `kras_g12c_mandated` at 13 decoys cannot reject at any effect size. A combination escapes the floor. It tests the **intersection null**, so a rejection licenses "at least one arm separates the site from non-functional pockets" and **not** a generalisation claim                                                                                                                                                                                                                                                                                                                                                                                          |
| 4   | **The claim threshold becomes its own confirmatory family**: a paired `compare_methods` against `cavity_volume` on the same three arms, Holm over three, two-sided (ADR 0032)                                                                                            | ADR 0025 already made "beat `cavity_volume`" the claim threshold, and §8 then declared everything except the matched-patch family descriptive. The load-bearing comparison sat in an unprotected family. This closes the contradiction rather than lowering a bar                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 5   | **`top_5_components` is added as a reported endpoint** — how many connected components the top-5 list lands in                                                                                                                                                           | Reported, never tested. `CHALLENGE.md` §4.2 asks for actionable output and nothing else here measured it                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 6   | **Four omission rationales in §3.3 are corrected**, and one (RBO) was wrong about its reason                                                                                                                                                                             | A stated reason that is false is worse than no reason                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

**What did not change.** The confirmatory endpoint is still the mean midrank. The confirmatory
family is still the three `corrected` arms. The matched-patch tolerance is still 0.10 and the
size-ratio rescale is still calibrated at every Holm level. Alpha is still 0.05.

### 0.1 What the recalibration measured

`experiments/2026-09-02-null-recalibration/`, fifteen gate arms at 9999 replicates.

**The pre-registered check passed.** Thirteen of the fifteen arms reproduce their 2026-08-25
`size_ratio` and `alpha_star` **to six decimal places**. The two that moved are the two the
input re-freeze changed. Nothing else drifted.

| Arm                       | `size_ratio` | `alpha_star` | Against version 2              |
| ------------------------- | -----------: | -----------: | ------------------------------ |
| `bcr_abl1_mandated`       |   **1.2073** |   **0.0277** | was 1.0960 / 0.0357 on chain A |
| `cardiac_myosin_mandated` |   **1.0509** |   **0.0485** | new arm, no prior value        |
| the other thirteen        |    unchanged |    unchanged | bit-for-bit                    |

**The organisers' chain B needs more tightening than chain A did.** Its matched-patch type-I
rate is 0.054 / 0.071 / 0.069 / 0.079 across λ = 4–20 Å, so three of four correlation lengths
sit above the binomial band [0.0370, 0.0640]. That is what a `size_ratio` of 1.2073 is for.
Calibration may tighten and may never loosen, so the arm is tested at a stricter threshold
rather than at a wrong one.

**The homology-model arm is the best-calibrated arm in the set, and the reason matters.**
`cardiac_myosin_mandated` sits inside the band at every λ (0.051 / 0.048 / 0.046 / 0.054),
while the _measured_ `cardiac_myosin_corrected` sits **below** it at two. A calibrated null
says the matched-patch construction works on that arm. It says nothing about whether the arm's
contact graph is right — and that graph agrees with the measured structure at long-range
Jaccard 0.471. No null calibration can see that, which is exactly why the arm is
non-confirmatory and prints the Jaccard beside every number.

**The positive control is 0.0001 on all fifteen arms**, the smallest value 9999 replicates can
produce. The type-I band is not being passed by a test that rejects nothing.

**One measurement to record about the matched-patch pool.** On the 0.05 rung of the tolerance
sweep, `cardiac_myosin_mandated` cannot supply a pool: 822 of 999 patches in 3 996 000
attempts, acceptance 0.000206. At the frozen 0.10 it draws all 9999 gate patches in 11 390 541
attempts at acceptance **0.000878** — within 1 % of the 0.000884 a standalone probe measured,
which is the determinism check on the sampler. The sweep records the rung as undrawable and
continues; the scored arm keeps its null. **No arm's tolerance is widened because that arm
failed** — a per-arm tolerance chosen after the fact is the hyperparameter this protocol exists
to prevent, and `allo.scoring.nulls.MatchedPoolUnavailable` says so at the raise site.

---

## 1. What the challenge asks for

`CHALLENGE.md` §4.1 states the success criterion:

> Success is defined by the algorithm's ability to assign **statistically significantly
> higher scores to known distal regulatory residues** compared to: **random background
> residues**, and **non-functional surface pockets**.

Two negative classes, both required. §5 names the scored artifact: a **top-5 ranked residue
list per target**. The N × N connectivity matrix is a required deliverable, but accuracy is
not measured on it.

Everything below is built on those two sentences, or on the allosteric-site prediction
literature. Nothing is built on our preference.

---

## 2. The contract

A method returns one score per candidate residue, higher meaning more allosteric. That is
the whole interface:

```python
from allo.inputs import apo_input  # prediction side: what the method receives
from allo.scoring import score_arm  # evaluation side: what scores it

apo = apo_input("kras_g12c_corrected")
scores = my_method(apo)  # {author residue number: float}
record = score_arm("kras_g12c_corrected", scores, method="ctqw_transfer")
```

Three properties of that contract matter.

- **A method must score every candidate.** A missing residue raises. Filling a gap with a
  constant would tie those residues and quietly move the AUC.
- **Scores are converted to midranks before any test.** Two methods on different scales
  therefore get the same test.
- **The record never contains the label set.** `tests/test_no_leakage.py` checks this.

**The evaluation graph is not the method's graph.** This layer builds one contact graph per
arm, heavy-atom minimum distance at the input layer's frozen cutoff, and it never moves. A
method is free to choose its own cutoff, weighting and node representation. That choice is
a hyperparameter, and it is made on the secondary set's `development` tier.

---

## 3. Endpoints

### 3.1 The confirmatory statistic

**The mean midrank of the scoreable label set.** Every null below holds the positive-class
size fixed, so this statistic is a strictly increasing function of AUC-ROC. The permutation
p-value is therefore identical to one computed on AUC-ROC, and the effect size reported
beside it is the metric this field actually uses.

AUC-ROC is the residue-level convention in this literature. At least eight independent
groups report it, including CryptoSite (doi:10.1016/j.jmb.2016.01.029), PocketMiner
(doi:10.1038/s41467-023-36699-3) and CryptoBench (doi:10.1093/bioinformatics/btae745).

### 3.2 What is reported beside it

| Metric                        | Estimator                                                    | Tie rule                     |
| ----------------------------- | ------------------------------------------------------------ | ---------------------------- |
| AUC-ROC                       | rank-based Mann-Whitney                                      | midrank                      |
| AUC-PR                        | `allo.scoring.metrics.auc_pr`, step: AP = Σ (Rᵢ − Rᵢ₋₁) · Pᵢ | one point per distinct score |
| precision@5, hits@5, recall@5 | top 5 of the ranking                                         | pessimistic                  |
| DCC, angstrom                 | centre of the top 5 to centre of the site                    | pessimistic                  |
| AUC-ROC against decoy linings | rank-based Mann-Whitney                                      | midrank                      |
| site pocket rank              | pockets ordered by lining mean midrank                       | pessimistic                  |

**recall@5 is printed, because a reader will otherwise derive it and derive it wrongly.** It
is one division from hits@5, hits divided by the label-set size, and its chance line is
`k / n_candidates`, which does not depend on the label-set size.

**It is not the field's top-N number, and this page used to say that it was.** Corrected
2026-09-03 by [`../review/07-metrics-audit.md`](../review/07-metrics-audit.md), weakness 1.
The earlier wording cited 17 of 22 surveyed tools reporting a recall-style top-N success rate.
The count is right and the inference is a category error. The field's top-N is a **per-protein
binary**: did the true pocket land in the top three of the pockets a detector returned. This
recall@5 is the **fraction of a multi-residue label set** recovered in five picks. The two have
different units and different chance lines, so one cannot be read as evidence for the other.
Printing it still costs nothing. The reason is convenience, not convention.

**The site pocket's rank is printed, because that is the field's own convention.** Every
detected pocket is ordered by the mean midrank of its lining, and the record carries where the
site pocket lands out of how many. APOP words the convention as "If this pocket is among the
top-ranked three predicted pockets, we count it as a success"
(doi:10.1093/bioinformatics/btad275). It is reported and never tested: the detector, not the
method, fixes how many pockets exist, and on three of five primary arms there are too few to
reject at all (§5).

**DCC is reported, because it is the one published criterion built for a residue list rather
than a pocket** (STINGAllo, doi:10.1093/bib/bbaf424). It is the distance from the centre of
the predicted top 5 to the centre of the site, printed against the median distance a uniformly
random 5-residue list achieves on that arm.

**It is a distance here, never a success rate.** The usual threshold is 4 Å
(doi:10.1023/A:1008124202956), and LIGYSIS-bench measured that threshold and rejected it for
centre-to-centre use: 4 Å "is too conservative, and a more flexible DCC threshold of 10–12 Å
should be used for comparable performance with DCA = 4 Å". Freezing either number takes a side
in a live disagreement, so the continuous distance is frozen and both conventions print beside
it.

**DCC is not redundant with the p-value, and one measurement settles that.** On
`cardiac_myosin_corrected` the cavity-volume baseline rejects the confirmatory null at
`p_calibrated` **0.0046** — while its top five hold **no** label at all and its predicted
centre sits no closer to the true site than chance: DCC **26.14 Å** against a chance line of
**28.73 Å**. A confirmatory rejection and a useful hit list are different claims, and without
this column the report would print only the first.

**CORRECTED 2026-09-03.** This argument used to run on `bcr_abl1_corrected` at
`p_calibrated` 0.0003 and DCC 26.5 Å against 17.7 Å. Those are version-2 numbers; §13 of this
page withdrew them and that arm now reads 0.3236, which is no rejection at all. The point
survives, on the arm that still makes it under version 3. The other published residue-list criterion, Jaccard on residue sets
(AlloBench, doi:10.1021/acsomega.5c01263), is declined in §3.3 on its own merits.

**Every top-5 number is printed against its exact hypergeometric chance line**, computed from
the freeze and never quoted from prose: E[precision@5] and P(at least one hit in the top 5) on
that arm's candidate set. Those lines run from 0.078 to 0.445 across the five primary arms, and
that is the bar a top-5 list must clear before it means anything. `score_arm` returns them in
`chance` beside the endpoints, so the two cannot drift apart.

**AUC-PR is reported, not tested, and that corrects the earlier draft.** The draft made
AUC-PR the tested endpoint. Two measurements say it cannot carry a confirmatory decision.
It is about three times noisier than AUC-ROC in the one paper that reports both with
dispersion: 0.44 ± 0.12 against 0.83 ± 0.04 (doi:10.1038/s41467-023-36699-3). And §7 below
shows this benchmark barely detects a strong effect at all. A noisier statistic detects
less.

**AUC-PR is still reported, because AUC-ROC hides the hard arms.** Prevalence spans 6.79×
across the five primary arms. On one dataset with one split, AllositePro reads AUROC 0.68
with AUPRC 0.07 while PASSerRank reads 0.82 and 0.46 (Allo-Allo,
doi:10.1101/2024.09.28.615583). The two columns reorder the methods. Always print AUC-PR
against its chance line, which is the prevalence: AUC-PR is not comparable across arms of
different prevalence, and it favours the higher-prevalence ones (McDermott et al.,
arXiv:2401.06091).

**Both AUC-PR estimators are biased upward at this prevalence.** The step estimator is the
more biased of the two. It is kept because it is the scikit-learn convention and because it
never interpolates between thresholds a method did not produce. The argument for it is a
**common** estimator across methods, not an unbiased one. Report the bias rather than
claiming the estimator removes it.

### 3.3 What is not reported, and why

Recorded so the omissions read as decisions rather than gaps.

- **Accuracy.** At 1.6–11 % prevalence, predicting "not a label" for every residue scores
  0.89–0.98, so accuracy measures the negative class and nothing else. That is arithmetic and
  needs no citation. The illustration usually given here — Allo-Allo Table 1 reading 0.91–0.98
  for every method including the one at AUPRC 0.07 — is **read from a bitmap table and not
  independently verified**, so it is flagged rather than relied on.
- **MCC and F1.** Both are field conventions — CAPASP 2026 names them among its five
  evaluation dimensions — and both are omitted here because **k = 5 is too small**. At a
  fixed 5-residue prediction against 11–20 labels, recall cannot exceed 0.25–0.45, so F1 and
  MCC measure the label-set size more than the method. Utgés & Barton 2024 say the
  usefulness of residue-level F1 and MCC "is limited" (doi:10.1186/s13321-024-00923-z), but
  their objection is about the size of the predicted set, not about thresholds, so it is
  quoted here for agreement in direction and not as the argument. Threshold-free AUROC and
  AUPRC are unaffected either way, which is why those stay.
- **Jaccard.** Determined by the label set rather than by the method. Five predicted
  residues against an 11–19 residue label set cap at **0.2632 to 0.4545** across the 15 frozen
  arms (0.2778 to 0.4167 on the six primary ones), and a perfect method hits that ceiling. So
  Jaccard@5 ranks arms by how few labels they carry. AlloBench tabulates values of 0.1–0.4,
  which these ceilings reach, so "below the reporting threshold" is not the reason — the
  reason is that the statistic is not about the method.
- **DVO.** No volume is predicted, which settles it alone. (An earlier draft added "and no
  standard threshold for it exists". That is false — `DVO > 0.2` is stated verbatim in
  doi:10.1021/acs.jcim.5c00336 — so the clause is withdrawn.)
- **A bootstrap confidence interval on the effect size.** A reviewer will ask, and it is
  declined on the same argument that withdrew the closed-form power columns in §7. A
  nonparametric bootstrap over residues assumes the resampled units are exchangeable and
  independent. The label set is a contiguous, spatially autocorrelated patch of 11–20
  residues, so they are neither, and resampling them also moves the prevalence the null is
  conditioned on. An interval built that way would be too narrow and would look authoritative
  while being wrong. What answers the same question honestly is already reported: the exact
  permutation p, and the minimum detectable effect in §7, which states what this benchmark
  can and cannot resolve.
- **A sequence-identity redundancy threshold.** Handled at the input layer instead, and more
  strictly: clause (xii) of the secondary freeze requires that no two targets share a Pfam
  family, and the secondary set is disjoint from every primary target on accession, family and
  homologous site (`../secondary/README.md`). Family-level disjointness is stronger than any
  percent-identity cut.
- **Enrichment factor, BEDROC, RIE.** Two independent literature sweeps found no use of
  them in site prediction. BEDROC's conventional α = 20 encodes "the top 8 % matters",
  which is meaningless at k = 5.

---

## 4. The nulls, and why there are four

`CHALLENGE.md` §4.1 names two negative classes. The first is split three ways: the form the
challenge words, the form that holds its size, and that form with the distance confound added.
Reporting the whole ladder is what shows which rung a result stands on.

| Null                     | Answers                              | Status                          |
| ------------------------ | ------------------------------------ | ------------------------------- |
| background residues      | the challenge's negative class (a)   | reported, never a decision      |
| **matched patch**        | (a), in the form that holds its size | **confirmatory**                |
| matched patch + distance | (a), plus the distance confound      | pre-registered secondary        |
| decoy pockets            | the challenge's negative class (b)   | reported, power floor disclosed |

### 4.1 Why the unmatched null is not usable

An allosteric label set is a spatially contiguous, partly buried patch. Any connectivity
score favours contiguous buried residues. Drawing residues uniformly asks whether these
m residues beat m random ones, and a method answers that correctly by finding any buried
blob.

This is measured, not asserted. Under a site-uninformative spatially autocorrelated score,
the unmatched null's rejection rate across all 15 frozen arms is **0.096 to 0.323** against a
nominal 0.05, and it rises monotonically with the correlation length on every arm. A test
with a type-I rate of 0.30 is not a test.

Two published sources support the same conclusion from outside this field. On residue
contact graphs, nulls that ignore spatial embedding "tend to identify as significantly
(under-) over-represented almost all analyzed subgraphs" (Milenković, Filippis, Lappe &
Pržulj, doi:10.1371/journal.pone.0005967). Their own prescription is a geometric null on the
graph, GEO-3D, which we do not adopt: it randomises the graph, and we need to randomise the
**patch** while holding the graph fixed, because the graph is what every method shares.

And the confound is measured inside this method's own family. Elastic-network
perturbation-response residues cluster at **3.56–3.69× random** over 502 structure pairs
(Zheng & Tekpinar, doi:10.1186/1472-6807-9-45). A null that does not hold clustering fixed
is therefore testing clustering.

### 4.2 What the matched patch matches

| Property    | Rule                                                      |
| ----------- | --------------------------------------------------------- |
| graph       | heavy atom, the input layer's frozen cutoff               |
| size        | the same number of residues                               |
| components  | the same component-size multiset, components non-adjacent |
| burial      | patch mean contact degree, within 10 %                    |
| compactness | patch radius of gyration, within 10 %                     |
| growth      | uniform contact frontier, inside the candidate set        |
| p-value     | upper tail, plus-one correction, 9999 replicates          |

**Components, not connectivity.** Two of the five primary label sets are disconnected:
`bcr_abl1_corrected` is [17, 1] and `cardiac_myosin_corrected` is [8, 4]. Sampling connected
blobs against a two-lobed observation imposes a property the observation lacks, which is
anti-conservative.

**Compactness, and it is the property that decides whether the test works.** Matching size,
components and burial alone left the rejection rate at 0.07–0.12. The cause was measurable:
matched patches were far more spread out than the observations. The myosin label set has a
radius of gyration of 8.9 Å against 21.1 ± 6.7 Å for size-and-component-matched patches,
because its two lobes are adjacent while two freely grown lobes land anywhere in a
764-residue chain. Radius of gyration is the closest single property to what sets the variance of a
patch mean under a spatially autocorrelated score. Adding it moved every arm most of the
way, and §6 reports the residual it does not close and what is done about that.

**One tolerance, not two.** The same relative bound applies to burial and to compactness. It
is fixed by the calibration gate in §6 and by nothing else.

**The decision threshold is calibrated per arm, because the matching is not sufficient.**
§6 measures the residual and freezes a `size_ratio` for every arm. Read §6 before quoting a
p-value from this null.

**Precedent, and one improvement on it.** The closest published construction is Amor et
al.'s surrogate sites: 1000 per protein, matched on residue count and diameter
(doi:10.1038/ncomms12477). Their diameter rule is one-sided — a surrogate must be smaller —
which biases the surrogates toward compactness. The bound here is two-sided.

**Known limitation, disclosed rather than hidden.** Drawing a fresh patch pool per replicate
is prohibitive, so the pool is drawn once per arm, cached, and shared. The replicates are
conditionally independent given the pool, not independent, and the binomial band in §6 is a
screen rather than a proof (ADR 0018). Sharing the pool has one benefit worth stating: every
method is tested against the identical null sample, so a difference between two methods
cannot be sampler noise.

### 4.3 The distance-matched null

This sub-field has a published name for the confound: **distance bias**. ProteinLens states
it directly — "The distribution of bond-to-bond propensities declines with distance from the
chosen source… To account for this distance bias, we use quantile regression"
(doi:10.1093/nar/gkab350). A propagation score from an active site has this problem by
construction.

The distance-matched null adds median Cα distance to the source to the matched properties.
It is **reported always and confirmatory never**. The reason is that it answers a different
question. The challenge asks for enrichment against background. This one asks whether
propagation adds anything beyond geometry. Both belong in the report, and only one can be
the declared decision.

It runs at 1999 replicates rather than 9999. Five simultaneous matched properties drop the
acceptance rate to 0.0018 on the myosin arm, and a secondary endpoint does not need a
p-value floor below 5 × 10⁻⁴.

**A distance-only baseline is not a substitute for this null, and it is weaker than it
looks.** Scoring each candidate by minus its distance to the source gives AUC-ROC, over the
six primary arms: **0.589 / 0.588 / 0.385 / 0.215 / 0.442 / 0.335** for
`kras_g12c_mandated`, `kras_g12c_corrected`, `bcr_abl1_mandated`, `bcr_abl1_corrected`,
`cardiac_myosin_mandated`, `cardiac_myosin_corrected`. **It is below chance on four of the
six**, re-measured at version 3; the two arms added on 2026-09-02 are both below chance too.
Those arms are distal, so the _inverted_ baseline is the strong one there. Both directions are
required baselines (`manifest.yaml`, `secondary_objectives.classical_comparison`).

---

## 5. Non-functional surface pockets

### 5.1 The detector

**pyKVFinder 0.9.3** (doi:10.1186/s12859-021-04519-4), run on the apo input alone. The frozen
settings are **step 0.6 Å, probe_in 1.4 Å, probe_out 8.0 Å, removal_distance 1.2 Å,
volume_cutoff 1.0 Å³**, and `manifest.yaml` is the authority for them.

**CORRECTED 2026-09-03.** This section gave the package's version-0.9.3 defaults — probe_out
4.0, removal_distance 2.4, volume_cutoff 5.0 — as though they were current. ADR 0030 re-froze
the detector on 2026-09-02 and §0 and §5.3 of this same page have carried the new triple
since. §5.1 is the section a reader opens to answer "what is the detector", so it was the one
place the withdrawn values could do damage. The package defaults are now history and are
quoted as such in §5.3.

The deciding argument is that it is purely geometric, so it raises no C2 question, and that
it is versioned and installable, so this configuration is reproducible. Choosing the
defaults is the choice not to tune a detector on the benchmark it will score. Version
discipline in this literature is close to absent — of the allosteric papers surveyed,
exactly one states a detector version — so stating ours in full is a low bar that is
nonetheless above the field's.

It is an optional `eval` extra, not a runtime dependency. The decoy sets are derived once
and committed, so `make check` verifies them offline. Only re-deriving needs the detector.

### 5.2 What makes a pocket a decoy

Every lining is first restricted to the candidate set: a residue that scores by construction
leaves both classes, and a pocket lining is no exception (ADR 0011). A pocket is then a
**decoy** only if its lining shares no residue with the label set.

**The halo is 0 Å, and that is forced.** Excluding pockets near the site is the right idea —
without it a method is penalised for being nearly right — but at 5 Å `kras_g12c_mandated`
keeps zero decoys, and at 8 Å both KRAS arms do. A 169-residue protein has five detectable
pockets. An earlier draft named a 5 Å sensitivity analysis in the manifest and no code ran it,
so the key was removed rather than left standing as a promise.

### 5.3 What the detector found, before any method ran

**Re-derived at protocol version 3**, at the re-frozen detector settings and over fifteen arms.
The version-2 table is kept below it, because the change in the floor is the reason the
detector was re-frozen at all.

`detected` is what the detector returned. One of those is the site pocket itself and the rest
of the difference is excluded by the halo rule, so `detected = 1 + halo + decoys` on every row.

| Arm                        | detected | halo | decoys | decoy residues | site coverage | min attainable p |
| -------------------------- | -------: | ---: | -----: | -------------: | ------------: | ---------------: |
| `kras_g12c_mandated`       |       16 |    2 |     13 |             76 |        0.8125 |     **0.071429** |
| `kras_g12c_corrected`      |       21 |    2 |     18 |             64 |        0.9375 |     **0.052632** |
| `bcr_abl1_mandated`        |       48 |    2 |     45 |            272 |        1.0000 |         0.021739 |
| `bcr_abl1_corrected`       |       35 |    3 |     31 |            198 |        0.9444 |         0.031250 |
| `cardiac_myosin_mandated`  |      144 |    4 |    139 |            537 |        0.9167 |         0.007143 |
| `cardiac_myosin_corrected` |       85 |    0 |     84 |            464 |        1.0000 |         0.011765 |
| `chk1`                     |       47 |    7 |     39 |            158 |        0.9167 |         0.025000 |
| `ecoli_cps`                |      100 |    4 |     95 |            576 |        0.9474 |         0.010417 |
| `glucokinase`              |       56 |    6 |     49 |            277 |        1.0000 |         0.020000 |
| `hiv_rt`                   |       72 |    3 |     68 |            383 |        0.6250 |         0.014493 |
| `mkp5`                     |       19 |    4 |     14 |             66 |        0.4545 |     **0.066667** |
| `ns5b`                     |       54 |    3 |     50 |            260 |        0.3125 |         0.019608 |
| `p97_vcp`                  |       71 |    3 |     67 |            391 |        0.7059 |         0.014706 |
| `ptp1b`                    |       41 |    7 |     33 |            175 |        0.3636 |         0.029412 |
| `smyd3`                    |       35 |    2 |     32 |            189 |        1.0000 |         0.030303 |

**CORRECTED 2026-09-03 by the round-5 audit.** The `detected` column held `decoys + 1` on every
row, which is the count after the halo rule and not what the detector found. The halo column is
new and makes the arithmetic checkable. `test_the_protocol_readme_quotes_the_decoys_the_freeze_derives`
re-derives every cell from `frozen.json`, so the column cannot drift from its own source again.

At the version-2 defaults the same five primary arms read **3 / 3 / 24 / 9 / 41** decoys, with
floors of **0.25 / 0.25 / 0.040 / 0.10 / 0.024** and site coverage 0.75 / 0.75 / 0.85 / 0.67 /
1.00. Total decoys went **311 → 777** and the median per arm **16 → 45**.

Three consequences, disclosed here rather than discovered later.

**The per-arm floor still binds, on three of fifteen arms rather than seven of fourteen.**
`kras_g12c_mandated` floors at 0.071, `mkp5` at 0.067 and `kras_g12c_corrected` at 0.053, so
none of those three can reject at α = 0.05 at any effect size. A 169-residue protein does not
carry 19 non-functional surface pockets. That is arithmetic about small proteins, and it is
why the combined test `decoy_pockets_combined` exists (ADR 0030).

**One of the three confirmatory arms is among them**, down from two. `kras_g12c_corrected`
floors at 0.053, just above α. `bcr_abl1_corrected` moved from a floor of 0.10 to 0.031 and can
now reject. The per-arm test is descriptive either way at version 3; the family is tested by
combination.

**What sets the floor is arm size, not difficulty.** The decoy count tracks the candidate count
at Spearman **ρ = +0.953** across the fifteen arms, essentially unchanged from version 2's
+0.95. Re-freezing the detector raised every arm's count; it did not decouple the count from
the protein's size, and nothing available would.

**The decoy null is conservative, from a size mismatch nobody chose — and version 3 made it
worse.** A decoy lining is smaller than the label set on **15 of 15 arms**, median ratio
**0.412**, against 0.55 at the version-2 settings. The re-frozen detector finds more pockets
and the extra ones are smaller, so the null gained replicates and lost comparability at the
same time. That trade was accepted because the per-arm test is descriptive at version 3 and the
decision runs on the combination (ADR 0030), but it is a cost and it is stated as one. The statistic is a mean
midrank, whose null variance goes as the reciprocal of the set size, so a decoy patch is
noisier than the observed one. **This null is never calibrated and never confirmatory.**
Size-standardising the linings would fix it and would also stop the statistic from being the
thing the challenge asked for, so the mismatch is disclosed instead.

**CORRECTED 2026-09-03: the direction is not the same for both endpoints, and the range this
paragraph gave was inferred rather than measured.** It said three audits put the real size
"somewhere near 0.008–0.022" and that the comparison is biased toward not rejecting. That was
an argument from the variance ratio, not a measurement, and version 4 reports **two** endpoints
on this null. Measured in `experiments/2026-09-03-endpoint-b/` over four distinct rank laws,
20 000 fields per cell, worst cell over four correlation lengths and three arms:

| endpoint | what it ranks | worst measured size |
| --- | --- | ---: |
| `p` | the detector's site-pocket lining | **0.0237** |
| `label_p` | the label set itself | **0.0548** |

`p` is conservative on all four laws, which vindicates the argument. `label_p` is **not**: on
`bcr_abl1_corrected` under a blocky distance-monotone field its 95 % interval is [0.0516,
0.0580], entirely above α. That is why ADR 0039 ships `label_p` as a descriptive percentile
carrying no rejection. Read the paragraph above as being about `p` alone.

**The detector covers the site poorly on four secondary arms.** At the version-3 settings,
site coverage runs 0.3125 on `ns5b`, 0.3636 on `ptp1b`, 0.4545 on `mkp5` and 0.6250 on
`hiv_rt` — the four values in the table above that sit below 0.70. That is the challenge's own
premise, static pocket detection failing on exactly these targets, measured on our benchmark
before any method existed. It is a difficulty axis, never a selection rule. **CORRECTED
2026-09-02:** this paragraph quoted 0.09 / 0.19 / 0.36, which were version-2 numbers left
standing under a version-3 heading, and two of the three contradicted the table forty lines
above.

---

## 6. The calibration gate, and what it found

ADR 0018 blocks scoring until both ends are measured. A null that rejects nothing passes a
type-I band perfectly, so one end is not enough.

1. **Type-I rate.** Draw a stochastic, site-uninformative, spatially autocorrelated score.
   Test the true label patch against the matched-patch null. Repeat 1000 times. The
   rejection rate must sit inside the exact central 95 % binomial prediction interval at
   α = 0.05, which is **[0.037, 0.064]** at 1000 replicates. Required across correlation
   lengths 4, 8, 12 and 20 Å, not at one value.
2. **Positive control.** A score built from the answer must reject on every arm. It is
   evaluation-side only and never touches the prediction path.

The experiment is `experiments/2026-08-25-null-calibration/`:

```bash
uv run allo evaluate calibrate experiments/2026-08-25-null-calibration/config.yaml
```

### 6.1 The gate failed, and the failure is reported rather than tuned away

Measured type-I rate of the matched-patch null at the frozen tolerance 0.10 and the frozen
replicate count 9999, for λ = 4 / 8 / 12 / 20 Å. Cells outside the band are marked. The
two right-hand columns are the remedy in §6.3: `alpha_star` is the nominal p whose measured
size is α, and `size_ratio` is what `score_arm` actually uses.

Read the two together. Three arms carry `alpha_star` = 0.05, meaning they need no tightening
**at α** — and two of them still carry a `size_ratio` above 1, because they are
anti-conservative at a tighter Holm step. That is the version-1 defect in one line.

| Arm                        |     λ = 4 |     λ = 8 |    λ = 12 |    λ = 20 | `alpha_star` | `size_ratio` |
| -------------------------- | --------: | --------: | --------: | --------: | -----------: | -----------: |
| `kras_g12c_mandated`       |     0.040 |     0.048 |     0.048 |     0.044 |      0.05000 |       1.0411 |
| `kras_g12c_corrected`      |     0.053 |     0.055 |     0.053 |     0.050 |      0.04326 |       1.0827 |
| `bcr_abl1_mandated`        |     0.054 | **0.071** | **0.069** | **0.079** |      0.02774 |       1.2073 |
| `bcr_abl1_corrected`       |     0.060 | **0.067** | **0.065** | **0.068** |      0.03558 |       1.0970 |
| `cardiac_myosin_mandated`  |     0.051 |     0.048 |     0.046 |     0.054 |      0.04848 |       1.0509 |
| `cardiac_myosin_corrected` |     0.037 | **0.034** |     0.037 | **0.035** |      0.05000 |       1.0000 |
| `chk1`                     | **0.073** | **0.069** | **0.069** | **0.066** |      0.03106 |       1.1832 |
| `ecoli_cps`                |     0.055 |     0.055 |     0.053 |     0.046 |      0.04559 |       1.0727 |
| `glucokinase`              |     0.051 |     0.062 | **0.066** | **0.065** |      0.03799 |       1.0788 |
| `hiv_rt`                   |     0.044 |     0.054 |     0.058 |     0.053 |      0.04689 |       1.1541 |
| `mkp5`                     | **0.068** | **0.071** | **0.077** | **0.069** |      0.03042 |       1.1398 |
| `ns5b`                     |     0.041 |     0.043 |     0.045 |     0.051 |      0.04954 |       1.0027 |
| `p97_vcp`                  | **0.068** | **0.071** | **0.072** |     0.061 |      0.02525 |       1.2487 |
| `ptp1b`                    |     0.059 |     0.063 |     0.060 |     0.057 |      0.03827 |       1.0768 |
| `smyd3`                    |     0.042 |     0.047 |     0.040 |     0.039 |      0.05000 |       1.0301 |

**Re-measured at protocol version 3 over fifteen arms.** Two rows changed: `bcr_abl1_mandated`
because the arm is a different chain, and `cardiac_myosin_mandated` because it is new. The
other thirteen reproduce their 2026-08-25 values to six decimals.

**Six of fifteen arms sit above the band and one sits below it**, and 14 of 15 need some
tightening once every Holm level is checked. The matched null holds its size on both KRAS arms,
on the mandated myosin arm and on five secondary arms, runs conservative on
`cardiac_myosin_corrected`, and runs anti-conservative on both BCR-ABL1 arms and on four
secondary arms. This is systematic, not a property of one protein.

**The organisers' chain B is worse than chain A was**, 0.054 / 0.071 / 0.069 / 0.079 against
0.059 / 0.066 / 0.069 / 0.075, which is what its `size_ratio` of 1.2073 pays for.

**The 20 Å homology model is the best-calibrated arm in the set**, inside the band at every
correlation length, while the _measured_ myosin structure is below it at two. That is
counter-intuitive and it is worth reading correctly: a calibrated null says the matched-patch
construction works on that arm's graph. It cannot see that the graph is largely invented, which
is a separate defect the arm discloses separately (long-range contact Jaccard 0.471, ADR 0031).

Tightening the tolerance does not fix it. At 0.05 the BCR-ABL1 rates are 0.066 / 0.072 /
0.074 / 0.089, which is worse than at 0.10, and the sampler's acceptance rate falls to 0.0027
on myosin.

**The positive control passes decisively.** A score built from the answer returns p = 0.0001
on all **15** arms, which is the smallest value 9999 replicates can produce. The null is not
inert.

### 6.2 Why, measured

Radius of gyration is the second moment of the patch about its centroid. What actually sets
the variance of a patch mean under a spatially autocorrelated score is the **whole**
within-patch distance distribution: Var = m⁻² Σᵢⱼ exp(−dᵢⱼ/λ). Two patches with equal size
and equal radius of gyration can differ in that sum.

The observed patch's own value of that sum, as a percentile of its matched pool, **orders the
arms the way the type-I rate does** — Spearman ρ = 0.821 over 12 arm-by-λ cells:

| Arm                        | percentile at λ = 8 | measured type-I at λ = 8 |
| -------------------------- | ------------------: | -----------------------: |
| `cardiac_myosin_corrected` |              32.5 % |                    0.034 |
| `kras_g12c_mandated`       |              55.6 % |                    0.048 |
| `kras_g12c_corrected`      |              57.3 % |                    0.055 |
| `bcr_abl1_mandated`        |              70.1 % |                    0.066 |
| `bcr_abl1_corrected`       |              76.7 % |                    0.067 |

**This table is version-2 data and was not re-measured at version 3.** The percentile comes
from `experiments/2026-08-25-null-repairs/`, which is a separate experiment from the
calibration, so `bcr_abl1_mandated`'s row is chain A's and `cardiac_myosin_mandated` has no
row. Neither omission changes anything, because §6.2 ends by **withdrawing** this relation as a
mechanism: an intervention that moves the percentile by 18 points moves the type-I rate by
0.0012. The table is kept as the description that failed, not as a working model.

Above the median the null's members have lower variance than the observed statistic and the
test over-rejects; below it, it under-rejects. That reading is consistent with every arm.

**It is a correlation, and it is not the mechanism. Direct intervention refutes it.**
`experiments/2026-08-25-null-repairs/` moves the percentile on purpose and measures what the
type-I rate does.

| Repair                                                      | mean move in percentile | mean move in type-I | ρ of the two moves |
| ----------------------------------------------------------- | ----------------------: | ------------------: | -----------------: |
| **C** — centre the acceptance window on the observed Rg     |        **−18.1 points** |             −0.0012 |             −0.193 |
| **D** — match the whole within-patch pairwise-distance ECDF |             −4.8 points |             −0.0011 |             +0.049 |

Repair C moves the percentile by up to 26 points and the type-I rate by about one thousandth.
Fitted on the frozen cells, the relation in the table above predicts a mean type-I of **0.0407**
after repair C; the measured value is **0.0500**. The sharpest single cell: repair C takes
`kras_g12c_corrected` at λ = 8 from percentile 57.3 to **31.0**, below the 32.5 this section
reads as the reason myosin under-rejects, and KRAS's type-I rate goes 0.055 to 0.056.

So the percentile is a marker for whatever varies between arms, not the cause. Read the table
above as a description and never as an explanation (ADR 0025 corrects ADR 0023 on this).

**Four candidate repairs have been tested and none closes the residual.** Mean within-patch
pairwise Cα distance is already satisfied by almost all of the pool. Internal contact count
correlates with the variance factor only weakly and orders the arms wrongly. Repairs C and D
are above: both leave BCR-ABL1 above the binomial band and myosin below it. Matching the
variance factor itself is not available in advance, because λ is a property of the **method's**
score field, not of the benchmark. Four failures are why the remedy below calibrates the
threshold rather than chasing a fifth.

### 6.3 The remedy: calibrate the threshold, at every level, and only downward

Each arm carries a frozen `size_ratio`, and `score_arm` reports

```
p_calibrated = max(p, sf(isf(p) / size_ratio))
```

which is the value the decision and the Holm step-down in §8 use.

**The rescale is on the probit scale, and it is calibrated at every Holm level.** The model has
one parameter: the observed statistic's null is `size_ratio` times as wide as the pool
members', and rescaling on the probit scale undoes exactly that. `size_ratio` is the largest
value of `z(qₜ) / z(t)` over the four correlation lengths **and** over every level Holm can
present — α/3, α/2 and α — floored at 1. The rescale is conservative at level `t` precisely
when the ratio is at least `z(qₜ) / z(t)`, so a maximum over all of them is conservative at all
of them by construction, with no case analysis about which level binds.

**This corrects the frozen version-1 protocol, which was not FWER-controlled.** Version 1 froze
`alpha_star` and rescaled linearly, `min(1, p × α / alpha_star)`. That is size-exact at α and
nowhere else, because the null's tail is convex, so at Holm's tighter steps the test ran above
nominal. On `kras_g12c_corrected` the ratio needed at α is 1.0421 and the ratio needed at α/3 is
1.0827 — about half the required tightening was missing. `alpha_star` stays frozen and reported
for disclosure; nothing computes with it. ADR 0025.

Three one-sided choices, every one toward a smaller test: the maximum over correlation lengths,
the maximum over Holm levels, and the floor at 1. **Calibration may tighten a test and may never
loosen one**, so cardiac myosin keeps the nominal threshold rather than buying power back from
its conservatism.

Three properties, stated plainly:

- `p_calibrated` is a **decision rule, not a calibrated p-value**. Do not read it as uniform
  under the null.
- Taking a maximum over twelve noisy tail-quantile estimates biases the ratio **upward**, which
  costs power and never costs size. The noise in any one estimate is symmetric and can land
  either way; the maximum is what makes the direction one-sided. An earlier draft claimed both
  error sources push toward a smaller test, and that was wrong.
- The `max(p, ...)` clamp matters only above p = 0.5, where the probit rescale would lower p —
  correctly under the model, since a wider null puts less mass above a point already below the
  null mean. No decision threshold lies above 0.5, so the clamp costs nothing and keeps the
  "may never loosen" rule true as written.
- This costs power on the **14 of 15 arms** whose ratio exceeds 1. Only
  `cardiac_myosin_corrected` sits at exactly 1.0000. §7 reports the minimum
  detectable effect at the **effective** threshold, at every Holm level, so the number a
  reader sees is the number the procedure delivers.
- **The ratio is an estimate, and it is frozen forever.** It comes from tail quantiles of 1000
  field draws, so it carries real sampling error. Measured out of sample by
  [`../review/21-protocol-v3-statistics.md`](../review/21-protocol-v3-statistics.md) §1.4,
  which draws 40 independent 1000-field blocks per arm against a 40 000-field reference: on
  `bcr_abl1_corrected` a 1000-field block returns 1.1061 with a standard deviation of 0.0438,
  against a reference of 1.0818 and a frozen value of 1.0970. Taking a maximum over twelve
  estimates biases the ratio up, so the direction is one-sided, but the magnitude is not zero
  and no later re-run may move it. **The chance that a block under-tightens is about 0.3 per
  arm** — 0.275 to 0.300 on the two arms above 1 — and on these arms it did not, since both
  frozen ratios sit above the out-of-sample reference. Review 21 finding S4 corrects ADR 0025
  on that point: maximising over twelve estimates rather than four does not shrink the chance,
  because the twelve cells are quantiles of the same 1000 p-values at three nearby levels.
  Re-running at 10 000 fields would tighten it and is the obvious improvement if this ever
  reopens.

  **CORRECTED 2026-09-03.** This bullet used to give `alpha_star` a 95 % interval of about
  [0.025, 0.048] and call it 14 to 19 % uncertainty. No record in the repository holds that
  interval, and review 21 measures the same quantity directly and out of sample, so the
  measured numbers replace the untraceable ones.
- **The pool is not centred on the observation, and that is a known residual.** The ±10 %
  matching band is symmetric, but the sampler's frontier growth populates it asymmetrically:
  the sampled patches' mean radius of gyration exceeds the observed value on **15 of 15 arms**,
  by **3.97 %** on average (sign test p = 3.05 × 10⁻⁵). Re-measured at version 3; at version 2
  it was 14 of 14 and 3.95 %, so adding an arm changed nothing about the direction or the size. Centring the window was tested as repair C
  and it does not fix the type-I rate (§6.2), so the bias is disclosed rather than corrected.

**Result: `metrics.json` in the experiment directory**, section `gate`, keys `size_ratio` and
`alpha_star` per arm. It runs on all 15 frozen arms, not only the six the tolerance sweep uses:
a threshold measured after a method is scored is a hyperparameter, and the secondary set is
where hyperparameters get chosen.

Distance-only and degree-only scores are diagnostics on the matching, not part of the gate.
Each yields one p-value per arm, which cannot separate 0.05 from 0.15.

## 7. Power, honestly

This is an a priori sensitivity analysis at the n the input layer already froze. It is not
observed power, and no method was measured.

**The method is simulation, not a formula, and that is a correction.** The draft carried two
closed-form columns and withdrew both. The rank-sum formula counts a contiguous label patch
as 12–20 independent observations, and under the spatially autocorrelated null that test does
not hold its size, so a power number from it is not a power number. The draft's replacement
asked every method to report its own correlation length and its own effective sample size.
That is a real property — effective sample size is a joint property of the label geometry and
the method's score field — but it is a burden with no payoff, because the permutation p-value
is exact and needs no effective sample size at all.

Simulating the real procedure removes the quantity entirely. The data-generating model is the
same site-uninformative field as the gate, plus a constant shift on the label residues. The
field has unit marginal variance, so the shift reads as Cohen's d, and the reported AUC is
the median actually achieved at that shift. **The threshold used is the effective one the
calibration produces, at every level Holm can present, not the nominal α**: a sensitivity
quoted at a threshold the procedure does not use is not the procedure's sensitivity.

An earlier draft quoted it at α alone. That understates the requirement, because Holm presents
α/3 to the first of three arms it tests and α/2 to the second, and which arm that is cannot be
known before the results exist. Every level is measured and all three are printed below.

### 7.1 The minimum detectable effect

80 % power, one-sided, at each arm's calibrated threshold. Each cell is the shift in
standard-deviation units and the median AUC-ROC achieved at that shift.

**At α, the loosest threshold Holm can present.**

| Arm                        | λ = 4 Å          | λ = 8 Å          | λ = 12 Å         | λ = 20 Å         |
| -------------------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| `kras_g12c_mandated`       | 1.01 / **0.776** | 1.21 / **0.841** | 1.21 / **0.860** | 1.17 / **0.888** |
| `kras_g12c_corrected`      | 1.05 / **0.786** | 1.24 / **0.842** | 1.28 / **0.868** | 1.23 / **0.895** |
| `bcr_abl1_mandated`        | 1.12 / **0.811** | 1.44 / **0.881** | 1.56 / **0.910** | 1.61 / **0.947** |
| `bcr_abl1_corrected`       | 1.00 / **0.762** | 1.31 / **0.850** | 1.38 / **0.880** | 1.36 / **0.908** |
| `cardiac_myosin_mandated`  | 1.05 / **0.772** | 1.42 / **0.861** | 1.57 / **0.898** | 1.66 / **0.929** |
| `cardiac_myosin_corrected` | 1.02 / **0.769** | 1.37 / **0.850** | 1.52 / **0.897** | 1.63 / **0.936** |

**At α/3, the tightest.** This is the threshold the first arm Holm tests must clear, and which
arm that is cannot be known in advance.

| Arm                        | λ = 4 Å          | λ = 8 Å          | λ = 12 Å         | λ = 20 Å         |
| -------------------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| `kras_g12c_mandated`       | 1.18 / **0.813** | 1.36 / **0.871** | 1.37 / **0.891** | 1.28 / **0.908** |
| `kras_g12c_corrected`      | 1.27 / **0.827** | 1.45 / **0.881** | 1.41 / **0.891** | 1.35 / **0.914** |
| `bcr_abl1_mandated`        | 1.32 / **0.849** | 1.64 / **0.908** | 1.73 / **0.932** | 1.76 / **0.960** |
| `bcr_abl1_corrected`       | 1.17 / **0.799** | 1.50 / **0.883** | 1.57 / **0.911** | 1.52 / **0.933** |
| `cardiac_myosin_mandated`  | 1.28 / **0.820** | 1.66 / **0.898** | 1.78 / **0.928** | 1.89 / **0.954** |
| `cardiac_myosin_corrected` | 1.22 / **0.810** | 1.62 / **0.892** | 1.79 / **0.931** | 1.89 / **0.961** |

The effective raw-p threshold behind each column, per arm:

| Arm                        |   at α | at α/2 | at α/3 |
| -------------------------- | -----: | -----: | -----: |
| `kras_g12c_mandated`       | 0.0434 | 0.0206 | 0.0134 |
| `kras_g12c_corrected`      | 0.0375 | 0.0169 | 0.0106 |
| `bcr_abl1_mandated`        | 0.0235 | 0.0090 | 0.0051 |
| `bcr_abl1_corrected`       | 0.0356 | 0.0158 | 0.0098 |
| `cardiac_myosin_mandated`  | 0.0419 | 0.0197 | 0.0127 |
| `cardiac_myosin_corrected` | 0.0500 | 0.0250 | 0.0167 |

**Read it as a band, never as one number: AUC-ROC 0.76 to 0.96.** Two axes make the band, and
both are real.

The wide one is the **correlation length of the method's own score field**. A method producing
a smooth long-range field needs a much larger effect to clear the same threshold than one
producing a short-range field. The draft's single number hid that.

The second is **which Holm step the arm draws**. At α the band is 0.762–0.947; at α/3 it is
**0.799–0.961**. A method must plan for the tighter one, because the assignment of steps to
arms is decided by the results.

The band is flat across arms at fixed λ, which is worth stating: prevalence spans
8.51× across all 15 arms and candidate counts span 6.38× across the six primary arms
(7.33× across all 15), yet the minimum detectable AUC moves by at most **0.0588** at any fixed
λ (0.0526 at α/3). The label patch geometry, not the arm size, sets the sensitivity.

Every cell above is read from `experiments/2026-09-02-null-recalibration/metrics.json`,
section `power`, and `test_the_protocol_readme_quotes_the_power_the_experiment_measured`
re-derives all three tables from it. **CORRECTED 2026-09-03 by the round-5 audit**, which
found the `bcr_abl1_mandated` row still carrying the version 2 chain-A numbers — its
`size_ratio` moved from 1.0960 to 1.2073 with the chain, which tightens its effective
threshold at α from 0.0357 to 0.0235 and raises every cell in its row. `cardiac_myosin_mandated`
was measured by the same run and was missing from all three tables.

### 7.2 What this means before any result exists

**There is no published AUC baseline for the elastic-network and network-communication
family, so this benchmark's requirement has no literature comparator.** A method whose score
field varies on a 12–20 Å scale must reach AUC **0.86–0.95** here to be detected at 80 % power
at α, and **0.89–0.96** at Holm's tightest step. Nothing in the published family can be placed
beside those numbers, and the reason is not that the field performs badly. It is that the
field does not report this statistic.

**Measured, not assumed.** A scoped literature verification ran on 2026-09-03 and its record
is [`../review/data/enm-auc-band-2026-09-03.md`](../review/data/enm-auc-band-2026-09-03.md).
Every unsupervised method in the family was read in full text and **none reports AUC**:
AlloPred gives a top-1 count, PARS's precursor gives PPV and sensitivity, Ohm gives TPR and
PPV, bond-to-bond propensity gives quantile scores, ESSA gives a hit count, STRESS gives site
overlap. The family's own five-method comparative benchmark — Wu, Strömich and Yaliraki,
_Patterns_ 2021, doi:10.1016/j.patter.2021.100408, over 432 structures and 146 proteins —
**reports no AUC anywhere**.

**The two numbers that used to stand here are real, and they are not this family.** Both were
verified and both are supervised classifiers that consume dynamics-derived features among
geometric, evolutionary and physicochemical ones:

| source | value | what it is | grade |
| ------ | ----- | ---------- | ----- |
| ZHMolEReP, doi:10.1021/acs.jcim.6c00141 | AUC 0.7858, recall 0.7037, 33 of 40 proteins on ASBench | supervised, PRS features, residue level. **Whether the AUC is ROC or PR is unresolved**: the full text is paywalled | `[VERIFIED-ABSTRACT]` |
| AR-Pred, doi:10.1002/prot.25749 | median ROC AUC 0.80 over residues | random forest with ANM features. The median is over **ten balanced training and validation sets**, not an independent test. Its independent test of 15 proteins reports **no AUC** | `[VERIFIED-FULLTEXT]` |

So the earlier sentence — "the published band and the detectable band do not overlap" — was
**mislabelled rather than wrong**. It attributed to the elastic-network family two numbers
from supervised residue-level predictors, one of them a balanced-validation median. The honest
form is the heading above.

**What follows for the report, and it is the more useful conclusion.** A measured AUC on this
benchmark cannot be argued good or bad by comparison with the literature, because the
comparison does not exist. It has to be judged against the controls this protocol already
freezes: the matched-patch null, the decoy pockets, and the nine required baselines, of which
`cavity_volume` is the one the claim threshold names. **Do not place a number from this
benchmark beside a published AUC without saying what that published AUC is computed over.**
One paper in the survey makes the point on its own data: Allo-PED reports **0.920 over pockets
and 0.563 over residues** from the same predictions on the same test set
(doi:10.1101/2025.03.28.645953).

**Three targets is a small family, and a negative result is weak evidence of absence.**

## 8. Multiplicity, and what generalises

**One confirmatory family, declared before any method exists:** the three `corrected` arms,
one per disease area, at α = 0.05 with Holm correction, one-sided upper.

**Holm runs on `p_calibrated`, never on the raw permutation p.** §6.3 gives the rescaling and
the reason. Quoting the raw p as a decision would use a test whose measured size is 0.067 on
BCR-ABL1.

One-sided is justified by design. A method ranking allosteric residues _below_ background is
a broken method, not a competing finding.

**Why three arms and not five.** The two `mandated` arms are the challenge's literal
assignment and are reported for that reason. Each shares a protein and a site with its
corrected arm, so including both would test one disease area twice. The corrected arm is
where methods are compared (`CONTEXT.md`, "Tier").

**Everything else is descriptive.** The distance-matched null, the decoy-pocket test and the
secondary set's `development` tier all produce p-values. None is FWER-protected, and none is
a confirmatory decision. Label them that way in the report.

**The across-target claim comes from one place.** The secondary set's `generalisation` tier
holds N = 5, so its minimum attainable one-sided p under a sign test is 2⁻⁵ = 0.03125. Any
correction to k ≥ 2 puts the threshold at 0.025 or below, and 0.03125 > 0.025, so a
corrected across-target sign test could not reject at any effect size. The project therefore
admits exactly one across-target decision at full α, and it is that one. It opens in Phase 5.

**What the primary set can claim.** The 2⁻ᴺ floor binds tests invariant to sign flips.
Combining three per-arm permutation p-values by Fisher or Stouffer is unbounded below: three
arms at p = 0.05 each give Fisher 6.3 × 10⁻³ and Stouffer 2.2 × 10⁻³. That licenses a
narrower claim and it must be labelled: Fisher and Stouffer test the **intersection null** —
no arm has signal — so rejecting says _at least one_ arm has signal. It is not a
generalisation claim.

**And the combination is far more conservative than its nominal level, which was measured
after it was adopted.** Disclosed 2026-09-03; the measurement is
[`../review/21-protocol-v3-statistics.md`](../review/21-protocol-v3-statistics.md) §3.2 and
§3.3, finding S3. ADR 0030 ran the type-I gate on the per-arm pocket test and on the two
replacements it rejected. It never ran the gate on the construction it adopted. Run on 20 000
site-uninformative fields per correlation length, the combined test's true size at nominal
α = 0.05 is:

| λ (Å) | Fisher | Stouffer |
| ---: | -----: | -------: |
| 4 | 0.0014 | 0.0051 |
| 8 | 0.0032 | 0.0089 |
| 12 | 0.0051 | 0.0121 |
| 20 | 0.0066 | 0.0141 |

**Between 7.6 and 36 times conservative.** Two mechanisms compound, and neither was chosen.
The per-arm p-values live on a discrete support of multiples of `1/(1 + n_decoys)`, which by
exact enumeration makes a nominal-0.05 Fisher test an actual-0.0206 test on its own. On top of
that sits the decoy-lining size mismatch §5.3 already discloses. ADR 0030's consequence
"negative class (b) becomes testable at α = 0.05, at the family level" is true about the
arithmetic floor and false about the size.

Two readings follow, and the report must carry both. **A rejection here is strong**, because
the test is conservative rather than anti-conservative, so nothing about validity is at risk.
**A non-rejection here means very little**, because the test spends most of its nominal α on
discreteness. And the protocol reports Fisher beside Stouffer without saying that the two
differ in robustness: under a Gaussian copula on the same discrete supports, Fisher stays
below nominal until ρ ≈ 0.30 while Stouffer passes it at ρ ≈ 0.15. The measured ρ across the
three arms is 0.00 to 0.01, so neither bites today. **Fisher is the reported statistic and
Stouffer is reported beside it for disclosure.** The frozen protocol does not move for this;
it is a disclosure, and tightening the size would be a hyperparameter chosen after the fact.

**The threat that N does not fix.** Every generalisation reading assumes the targets are
exchangeable with a population. The three primary arms were mandated by the challenge. The
nine secondary arms survived twelve admission clauses over an RCSB full-text query, and
[`../secondary/README.md`](../secondary/README.md) §7 records that the frame is non-random.
No N repairs a non-probability sampling frame. Generalisability here is at least as much a
frame problem as an N problem.

---

## 9. No tuning on this benchmark

Every hyperparameter — metric, Hamiltonian, cutoff, coarse-graining ratio — is chosen on the
secondary set's `development` tier and nowhere else. The `generalisation` tier is not opened
until the method is frozen. The frozen primary benchmark is scored **once**, with every
choice already fixed.

That set is disjoint from every primary target on accession, family, homologous site and
residue overlap (ADR 0012, ADR 0021).

**"Not opened" is a reading discipline, not a storage property.** The five
`generalisation` arms are **fully materialised** in two of the three `frozen.json` files —
the secondary set's and this layer's — carrying label
residues, positive counts, active sites, the matched-patch geometry, and the calibrated
null thresholds. They were derived and calibrated in August alongside the other ten arms,
because the freeze and the calibration both run over the whole set. Nothing about the seal
ever deleted them.

Two things enforce the seal, and each is partial. `PROTECTED_PATHS` in
`tests/test_no_leakage.py` stops a prediction-path module reading any of the three frozen
trees or the matched-patch cache. `allo.scoring.harness.score_arm` raises `PermissionError`
on a `generalisation` arm unless the caller passes `unseal="phase-5"`, so scoring one is a
deliberate act that leaves a string in the diff. Neither stops a person reading the file,
and no test can. ADR 0041 states this plainly and records that the tier was already read
during the August calibration, so its per-arm thresholds are known and the seal now covers
the **scores**, not the inputs.

---

## 10. Endpoints for the secondary objectives

`CHALLENGE.md` §4.2 asks for noise resilience, coarse-graining and a classical comparison.
Those endpoints are declared here for the same reason as everything above. Chosen after
seeing a result, each becomes a hyperparameter. The implementation belongs to Phases 3 and 4.

**Noise resilience.** Measure the stability of the **ranking**, not of the raw metric, since
the ranking is the deliverable. Statistics: Spearman ρ, Kendall τ, overlap@5 and Jaccard@5,
all four, following the only precedent that reports them together
(doi:10.1021/jacs.6c08053, preprinted as arXiv:2604.17486 — one paper, not two). That paper
computes its overlap at k = 10 and compares two methods rather than one ranking under noise;
we compute the same four statistics at **k = 5**, which is the deliverable. RBO is omitted because **overlap@5 already carries top-weighting at exactly the k that
ships**, so it adds nothing here. CORRECTED 2026-09-03: this read "principled and has no
use in this literature", which is a popularity argument, and R1 forbids one. ADR 0032
struck that sentence and mandated this rewrite; the rewrite reached the manifest and
missed this page.

**Coarse-graining.** Prove that compression retains the topological signal, using spectral
distance between the full and coarse propagators, rank correlation of residue scores, and
label recovery at k = 5. **Spectral, not mode overlap.** `exp(-iHt)` is a function of the
spectrum alone, and mode overlap needs a holo displacement vector, which C1 forbids on the
prediction path. Precedent for spectral coarse-graining of a walk on a graph: Gfeller & De
Los Rios, doi:10.1103/PhysRevLett.99.038701.

**Classical comparison.** The required baselines, in priority order, are listed in
`manifest.yaml`, with `cavity_volume` first. A method that does not beat it, distance-from-
source, its inverse and eigenvector centrality has demonstrated nothing.

**"Beat" has a definition, and it is frozen here rather than chosen later.** Until protocol
version 2 this document required a method to beat its baselines and specified no test, which
would have left the comparison rule to be picked with results in hand — a hyperparameter,
exactly like a threshold. `allo.scoring.harness.compare_methods` is that rule.

It is **paired on the residue**: take the difference of the two midrank vectors and test its
mean over the label patch against its mean over the same matched-patch pool the confirmatory
test uses. Pairing cancels every property of the arm that acts on both scores alike — size,
prevalence, patch compactness — so it is far more sensitive than comparing two separate
p-values, and both methods face the identical pool, so a difference between them cannot be
sampler noise.

It is **two-sided**, unlike the confirmatory test. There the one-sided rule has an argument: a
method ranking allosteric residues below background is broken, not competing. Between two
methods there is no such asymmetry, and a prior on which one wins is the bias this protocol
exists to prevent.

**It is not a formality.** Re-measured under version 3 on 2026-09-02, `cavity_volume` against
`distance_from_source_negated`:

| arm                        | AUC-ROC difference | `p_calibrated` | Holm threshold | reject |
| -------------------------- | -----------------: | -------------: | -------------: | ------ |
| `cardiac_myosin_corrected` |             +0.472 |         0.0343 |       0.016667 | no     |
| `bcr_abl1_corrected`       |             +0.348 |         0.0550 |          0.025 | no     |
| `kras_g12c_corrected`      |             +0.255 |         0.8281 |           0.05 | no     |

Comparing two AUC values would have called all three a win. The paired test calls none of
them. On `kras_g12c_corrected` a gap of a quarter of an AUC point reads p = 0.83, because a
gap that size is inside what patch geometry produces on that arm.

**Family 2 rejects nothing under version 3, where under version 2 it rejected on two arms**
(p = 0.0003 and 0.0001). **CORRECTED 2026-09-03:** this named a chain change on
`bcr_abl1_corrected` as the cause. That arm's apo input did not move; `manifest.yaml` records
it at `2G2H:A` under both versions, and what moved is the detector re-freeze (ADR 0030), which
changed the decoy set and so the paired comparison. Read this as the family having little power rather than as a negative finding:
review 21 of the audit measures it at 3.7x conservative at alpha on `kras_g12c_corrected`.

**Report the rank correlation against every baseline.** This is not decoration. The only
published quantum walk on protein residue networks reports per-protein Spearman ρ against
classical eigenvector centrality running from **0.582 to 1.000**, and declines the analysis
that would separate the two (Mohtashim, Sajjan & Kais, JACS 2026;148(27):29206–29219,
doi:10.1021/jacs.6c08053). The paper prints no summary statistic, so the range is quoted
rather than an average. A method that does not print this number has not answered the first
question a reader of that paper will ask.

---

## 11. How results are decomposed

Four factors, no more. At N ≤ 5 per cell no stratified comparison can support a test, so
these organise reporting and never a decision. State that before the first stratified table.

| Factor              | Source                                                |
| ------------------- | ----------------------------------------------------- |
| crypticity          | transplant clash fraction, frozen in `../frozen.json` |
| proximity to source | minimum Cα distance, scoreable set                    |
| tier                | mandated against corrected                            |
| prevalence          | a covariate, never a stratum                          |

**Four confounder columns print beside every result.** Controlling burial inside the null is
the stronger treatment, but it leaves the reader with no number, and the first question asked
of any distal-site score is whether it is a burial or flexibility proxy under another name.
`score_arm` answers it directly: one Spearman correlation between the method's score and each
of relative solvent accessibility, normalised B-factor and Kyte–Doolittle hydrophobicity.
Computed at score time, never frozen — a frozen value would be identical for every method.

They already earn their place. `distance_from_source_negated` correlates with normalised
B-factor at **ρ = −0.79** on cardiac myosin, so a "propagation" score of that shape is largely
re-measuring crystallographic disorder. `cavity_volume` correlates with all three at
|ρ| ≤ 0.22, so its rejections are a cavity-size signal and not a burial artefact.

**Conservation is the fourth column and it is absent.** It needs a multiple-sequence alignment
against an external database, which the offline gate cannot carry. It reads `null`, not a
number, because R3 requires "unknown" where evidence is absent. A reviewer will ask for it;
this is the honest answer until Phase 3 can fetch an alignment.

Burial is the strongest quantitative difficulty effect in the literature — a site in the
most buried **cluster** is about 28 times more likely to be functional than one in the least,
and the most exposed cluster held 0 of 29 known functional sites (Utgés et al. 2024,
doi:10.1038/s42003-024-05970-8, 293 unique sites). They are K-means clusters of unequal size,
not quartiles, and this is a different paper from the Utgés & Barton 2024 cited in §3.3. It
is controlled inside the null rather than used as a stratum, which is the stronger
treatment.

Modulator type is deliberately not a stratum. The site does not carry the sign of the
coupling: "the actual sign of the coupling can change, transforming an activator into a repressor,
or vice versa" (Motlagh et al., doi:10.1038/nature13001).

---

## 12. What this protocol will be criticised for

Written now, so the rebuttal is an argument rather than a scramble.

1. **"Residue-level metrics are the wrong frame; this field scores pockets."** Utgés & Barton
   2024 say so explicitly (doi:10.1186/s13321-024-00923-z), and top-N pocket rank is the
   near-universal convention. **Answer:** the challenge's scored artifact is a residue list
   (§5 of `CHALLENGE.md`), so residue-level scoring is the honest match to the deliverable.
   The objection targets threshold-dependent F1 and MCC, which §3.3 already drops. The
   pocket-level view is reported beside it: `score_arm` ranks every detected pocket by the
   mean midrank of its lining and reports `site_pocket_rank` out of `n_pockets_ranked`,
   which is the top-N convention APOP states. It is reported, never tested — the detector,
   not the method, fixes how many pockets exist.
2. **"Your decoys are method-specific."** SiteFerret's objection
   (doi:10.1021/acs.jctc.2c01306): a detector-derived negative set "is method-specific" and
   "false negatives cannot be ruled out". **Answer:** true and
   unavoidable. A pocket labelled non-functional here is a pocket with no _known_ function.
   The detector, its version and its full configuration are pinned before any method ran.
3. **"Your matched null has no precedent in allostery."** Nearly. Three surveyed papers do
   run a null — Amor et al. 2016 (doi:10.1038/ncomms12477), Wu et al. 2021
   (doi:10.1016/j.patter.2021.100408) and ProteinLens (doi:10.1093/nar/gkab350) — and the
   true statement is narrower and stronger than "nobody does it": they are **one group, one
   construction**, one-sided on pocket diameter, and that group dropped the null in its own
   later web server. No other group adopted it. Thirteen of eighteen surveyed papers state
   no test at all. **Answer:** the precedent is adjacent and thin, the confound is measured
   here (§4.1), and being ahead of a field that mostly reports no test is not a defect.
4. **"You resampled the region; you should have resampled the map."** The strongest technical
   objection available, and it comes from neuroimaging, which solved this exact problem
   first. Variogram-matched surrogates (Burt et al. 2020,
   doi:10.1016/j.neuroimage.2020.117038) estimate the autocorrelation **from the score field
   the method actually produced**, then generate surrogate maps with that autocorrelation.
   They need no λ in advance — which is the precise property §6.2 says is unobtainable, so
   the objection lands. **Answer:** it is the right design and it is not frozen here, for one
   reason: a surrogate-map null is a property of the method's own field, so two methods with
   different correlation lengths would be tested against two different nulls, and the
   protocol's purpose is that every method faces the identical null sample. The residual that
   costs is measured (§6.2) and calibrated away (§6.3) instead. A surrogate-map null is the
   first thing to try if the calibration ever has to move.
5. **"The tolerance was tuned."** It was calibrated, on a site-uninformative score, against a
   two-ended gate, before any method existed. The sweep is committed.
6. **"N = 3."** Stated in §8, with what each construction does and does not license.
7. **"Your confirmatory threshold is per-arm, which is a free parameter."** It is a
   parameter, and it is frozen before any method exists, measured on a site-uninformative
   score, floored so it can only tighten, and reproducible from a committed config. **"Can
   only tighten" is now true of the composed procedure and not only of one arm at α**, which
   is what the version-1 protocol got wrong: it calibrated at α and Holm then tested at α/3.
   The ratio is calibrated at every level Holm can present (§6.3). The
   alternative on offer was a test with a measured size of 0.067 on one of three mandated
   disease areas. Disclosing and correcting a miscalibration is not the same as tuning.

   Worth stating beside it, because it is the strongest defence available: spatially
   constrained nulls are a solved-looking problem that is not solved. After a decade of
   dedicated methodological work, Markello & Misic 2021 (doi:10.1016/j.neuroimage.2021.118052)
   report that **every** spatially constrained null they tested has an inflated false-positive
   rate, reaching about **13 %** for the best of them at high autocorrelation. The residual
   here is 6.6–7.7 % before calibration, and it is calibrated away rather than left standing.

8. **"Apo is harder than the numbers you are compared against."** For **allosteric and
   cryptic** sites, yes, and that must be said in the report rather than left for a
   reviewer: ESSA scores 10/14 on holo and 7/14 on apo, and AllositePro 8/14 against 2/14
   (doi:10.1016/j.csbj.2020.06.020). The claim must be scoped that way, because for pocket
   detection **in general** it is refutable: over 304 sequences and 2,528 structures, six of
   seven detectors show no significant apo/holo difference (doi:10.1038/s41598-020-72906-7).
   The penalty is specific to sites that are not formed in the apo state, which is exactly
   the class this benchmark is about. Any comparator evaluated on ligand-stripped holo is
   inflated. APOP is evaluated that way.

---

## 13. The gate before any number is quotable

All four, together:

1. `uv run allo benchmark verify` clean — the input layer still is what it claims.
2. `uv run allo evaluate verify --detect` clean — the evaluation layer too.
3. The patch null calibrated: type-I band **and** positive control, both in the committed
   experiment, and the arm's `size_ratio` read from it rather than restated.
4. Every method scored through `allo.scoring.score_arm` and no other path.
5. **Both controls run, and both behave.** One must reject nothing; the other must reject.

All five passed on 2026-08-25 under protocol version 2.

**The negative control rejects nothing.** `distance_from_source_negated` scores AUC-ROC
0.589 / 0.588 / 0.385 / 0.215 / 0.442 / 0.335 across the six primary arms, re-measured at
the 2026-09-02 re-freeze (§4, `experiments/REGISTRY.md`). On 2026-08-25, Holm on
`p_calibrated` gave 0.286, 0.920 and 0.656 on the confirmatory family. A geometry-only
control must not clear a geometry-matched null, and it does not.

**The positive control rejects on one of three, and that is still the uncomfortable one.**
`cavity_volume` — the volume of the largest detected cavity lining each residue, label-blind
and zero-parameter — was re-measured under version 3 on 2026-09-02:

| arm                        | AUC-ROC | `p_calibrated` | Holm threshold | reject  | site pocket rank | recall@5 |
| -------------------------- | ------- | -------------- | -------------- | ------- | ---------------- | -------- |
| `cardiac_myosin_corrected` | 0.8064  | **0.0046**     | 0.016667       | **yes** | 2 of 85          | 0.00     |
| `kras_g12c_corrected`      | 0.8430  | 0.0715         | 0.025          | no      | 1 of 19          | 0.00     |
| `bcr_abl1_corrected`       | 0.5626  | 0.3236         | 0.05           | no      | 8 of 32          | 0.00     |

Under version 2 it rejected on all three. **CORRECTED 2026-09-02, twice.** The sentence here
used to say version 3 "moved `bcr_abl1_corrected` to a different apo chain", and that is
false: ADR 0029 moved `bcr_abl1_**mandated**` to `1OPL:B` and states explicitly that `2G2H`
stays the comparison arm. `bcr_abl1_corrected` is and was `2G2H:A`. **The cause is the
detector re-freeze** (ADR 0030): `cavity_volume` is computed from the detector's own
cavities, so re-freezing the decoy detector redefined the baseline the claim is measured
against. Its median AUC over the arms runs 0.795 at the version-2 defaults and 0.696 at the
version-3 settings. And the version-2 triple itself is **disputed**: this file said
0.0073 / 0.0003 / 0.0001 and `manifest.yaml` said 0.0047 / 0.0001 / 0.0001. Neither has been
re-derived, so the honest record is that the version-2 numbers are unresolved and only the
version-3 triple above is measured. It still "succeeds" on two of three arms under the
field's own top-3 pocket convention.

**The point the version-2 text made survives, at reduced strength and on a different arm.**
`cardiac_myosin_corrected` rejects at `p_calibrated` 0.0046 with recall@5 = **0.00** and zero
label residues in its top five. A label-blind, zero-parameter detector score can still clear
the confirmatory null while naming no label residue at all.

**One half of the version-2 argument no longer holds and is withdrawn.** The arm whose
predicted centre pointed away from the site was `bcr_abl1_corrected`, at DCC 26.7 Å against a
chance line of 17.7 Å. That arm no longer rejects. On the arm that does reject, DCC is 26.1 Å
against a chance line of 28.7 Å — better than chance, not worse. No document may say that the
baseline rejects while pointing away from the site.

That is the whole reason gate item 5 exists. This benchmark's confirmatory null can be
cleared by a score whose top five contains no label residue. Clearing the null is a low bar.
**The claim threshold is beating
`cavity_volume`, not rejecting the null** (ADR 0025), and the report must print recall@5, DCC
against its chance line, and the pocket rank beside every p-value it quotes.
