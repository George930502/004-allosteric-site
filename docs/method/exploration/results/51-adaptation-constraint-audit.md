# 51 — Constraint ruling on the adaptation routes

**Design-stage audit, 2026-08-27.** Nothing here is built yet. This rules on admissibility
before implementation, against C1–C6 in `AGENTS.md` and the ADRs those constraints delegate to.

Proposals audited: `../../review/19-cross-protein-normalisation.md` §7 rows 1 and 2,
`48-adaptation-feasibility.md` §6, and `49-worst-case-selection.md`.

**One route is FORBIDDEN as written and it is P4b.** Everything else is admissible, three of
them with conditions. The audit also found **two live leakage routes that
`tests/test_no_leakage.py` does not catch**, one of which is already exercised by a tracked
file, and §3 gives the test for each.

---

## 1. Verdicts

| # | Proposal | Verdict | Decided by |
| --- | --- | --- | --- |
| P1 | Per-residue z-score against a size- and degree-matched random-source ensemble | **ADMISSIBLE WITH CONDITIONS** | C1, C6 |
| P2a | Radial-quantile strata **defined** from the protein's own candidate-to-source distances | **ADMISSIBLE** | C1 |
| P2b | Radial-quantile **stratified AUC** as a reported between-arm endpoint | **ADMISSIBLE WITH CONDITIONS** | evaluation protocol §11 |
| P3 | One pre-registered rule, tested once on the held-out arms | **ADMISSIBLE WITH CONDITIONS** | ADR 0012, ADR 0021 |
| P4a | Worst-arm AUC as a **reported column** | **ADMISSIBLE** — outside the frozen protocol | evaluation protocol §3.2, §11 |
| P4b | Worst-arm AUC as a **promoted endpoint** that decides anything | **FORBIDDEN** | evaluation protocol §3.1, §8, §9 + `AGENTS.md` |
| P5 | Pretrained model for structural features | **ADMISSIBLE WITH CONDITIONS**, tier-dependent | ADR 0027 |

---

## 2. The rulings

### P1 — Per-residue z-score against a matched random-source ensemble

**ADMISSIBLE WITH CONDITIONS.** The reference ensemble reads nothing it must not.

Traced: `src/allo/inputs.py:100` `_PREDICTION_SCHEMA` admits `active_site` and
`tests/test_no_leakage.py:499` `known_apo_side` confirms it is apo-side; `src/allo/inputs.py:161`
derives it from the apo structure by ligand and motif rules; `src/allo/network/graph.py:221`
carries it as `ResidueGraph.source`. The three inputs the construction needs — the apo contact
graph, the per-residue degree, and the **size** of the true source — are all on that path. No
label, no holo coordinate and no frozen-file read is required by the construction as specified in
`19-cross-protein-normalisation.md` §Q3.1.

**Where it lives.** `src/allo/classical/postprocess.py`, stage S6, which is where doc 19's own
"What this changes → S6" puts it and where the existing `decay_residual` detrend already lives.
It is a higher-order function over `(graph, scorer, M, seed)` that rebuilds the graph with a
randomised `source` and re-runs the scorer; it needs `allo.network.graph` and nothing else.

**Which module must not import which.** `allo.classical.postprocess` must not import
`allo.groundtruth`, `allo.scoring`, **or any `allo.scoring.*` submodule.** The last clause is not
redundant: §3.1 proves the import trace is blind to it today, and the matched-ensemble machinery
the author will be tempted to reuse (`allo.scoring.nulls.sample_matched_patches`,
`evaluation_graph`, `_grow`, `component_sizes`) is exactly there. Reuse it and the prediction
process holds `harness._positives` and the unredacted manifest in its own namespace.

_Conditions._

- [ ] The ensemble is built by randomising `ResidueGraph.source`, never by calling anything in
      `allo.scoring`. `rg -n "allo\.scoring" src/allo/classical/` returns nothing.
- [ ] `M` and the degree-bin rule are **required keyword arguments with no default**, on the
      `diversified_top_k` / `spatial_smoothing` precedent (`42-threats-and-confirmation.md` T10):
      a caller has to pass what it swept.
- [ ] The M-sweep of doc 19 §7 falsifier 1 (`M ∈ {25, 100, 400}`) is committed **before** any
      z-scored number is quoted.
- [ ] The degree-bin rule's provenance is in its own docstring. Guney's ≥ 100-node bins do not
      transfer to a 3–61 residue source (§Q3.1's own caveat); whatever replaces them was chosen
      on a stated argument, not on which choice scored better.
- [ ] Matched and unmatched numbers are reported together, per §Q3.1, because over-matching
      discards genuine signal.
- [ ] The falsifier is pre-committed: spread must fall by > 0.05, and mean |ρ| to negated
      distance must not rise above the unnormalised control.

### P2 — Radial-quantile stratification

**Two objects wear this name and they get different rulings.**

**P2a — defining the strata: ADMISSIBLE.** The quantiles come from each candidate's distance to
the source, and both halves are input-side. ADR 0011's 2026-08-24 amendment settles it in one
line: *"On the current freeze `excluded_from_scoring == active_site` and
`n_candidates == n_residues - len(active_site)`."* Node set minus active site is exactly what a
method already holds. `src/allo/scoring/nulls.py:119` builds the evaluation graph's `candidates`
the same way, from an `ApoInput` and nothing else. So the candidate-to-source distance
distribution is a quantity a blind method can compute for itself.

- [ ] The method **derives** its strata. It must not read `n_candidates` or
      `excluded_from_scoring` from either `frozen.json`, and it must not assume its strata equal
      the evaluation's candidate set — ADR 0011 clause 4 makes that identity a re-freezable thing,
      not an invariant.

**P2b — the stratified AUC: ADMISSIBLE WITH CONDITIONS.** A within-stratum AUC needs labels. It
is an evaluation-side quantity and it belongs after `score_arm`, never inside a method, and the
strata must not travel back into the method.

**On the risk that the evaluation layer also stratifies by distance:** it does, and the two are
not the same quantity, which is the trap. `docs/benchmark/evaluation/manifest.yaml:311` freezes
`proximity_to_source # min Ca distance, scoreable set` — the distance from *the arm's label set*
to the source, an arm-level factor. P2b stratifies *candidates* by their own distance. Different
objects, one word.

The good news is that changing 2 Å bins to deciles **does not touch the frozen protocol**: the
frozen manifest names the factor and no bin rule at all, and the fixed 2 Å convention comes from
`../../review/00-conventions.md` §5, which ADR 0026 has already re-opened.

- [ ] No file under `docs/benchmark/evaluation/` is edited.
- [ ] The stratified mean is reported and never tested. README §11: *"At N ≤ 5 per cell no
      stratified comparison can support a test, so these organise reporting and never a
      decision."* Promoting it to a tested endpoint falls under P4b.
- [ ] Fixed-Å and quantile strata are never mixed in one table (doc 19 §S9).
- [ ] The falsifier is pre-committed: it is a pure re-scoring of existing runs, so failure is
      "the decile-stratified spread is no smaller than the 2 Å-stratified one" and it costs
      nothing to find out.

### P3 — One pre-registered rule, tested once on the held-out arms

**ADMISSIBLE WITH CONDITIONS**, and this is the route where the conditions *are* the ruling.
`docs/benchmark/secondary/README.md` §2 fixes when the tier may be looked at: *"Phase 5, **after
the method is frozen**"*, and ADR 0012 gives the reason — the `development` tier is burned by
construction, and *"Phase 5's generalisability number comes from a further set … never looked at
until the method is frozen."*

**What has to be written down, and where.** An **ADR**, accepted and committed, before any
`generalisation` arm is opened. `docs/ROADMAP.md` ("written into an ADR — plus a pre-registered
prediction, before the `generalisation` tier is opened"), `42-threats-and-confirmation.md` §4
steps 1–2, and doc 48 §6.3 ("The rule and the endpoint go into an ADR before the tier opens") all
name the same artifact. It must contain, with no gaps:

1. **The frozen method.** One graph, one scorer, one confound-removal form, one site-assembly
   rule, every parameter and every seed. Not a family, not "best of three" (42 §4 step 1).
2. **The one descriptor**, named, with the apo-side procedure that computes it. One. Regime B in
   doc 48 §4 is only worth 8 proteins instead of 13 because nothing else is screened.
3. **The rule** — the exact map from descriptor to the thing it changes, with its direction.
4. **The endpoint and the test**, with N, the null and the alternative fixed.
5. **The predicted value** of AUC and recall@5 on the tier, and **the value at which the method
   is abandoned** (42 §4 step 2). Without the abandonment threshold the run is a measurement, not
   a test.
6. **The tier's arms are not named** in the ADR, and the ADR does not open
   `docs/benchmark/secondary/frozen.json` or `selection.json`.

**What burns the tier.** Any one of these and the generalisation claim is gone, permanently:

- Any `score_arm` call on a `generalisation` arm before that ADR is committed.
- A second call on any arm of it, for any reason, including "the first run had a bug".
- Any change to the rule, the descriptor, the endpoint or the threshold after a
  generalisation-tier number exists.
- Reading `docs/benchmark/secondary/selection.json` or `evidence/extension-candidates.md` for
  those arms — both are answer keys and both are in `PROTECTED_PATHS`.
- Screening more than the one descriptor and reporting the best. That is Regime A, which doc 48
  §5 records as *"unavailable and will stay unavailable"*.

**One correction to doc 48 §5.** Its table row *"Held-out total | 10 | Available once, to a
pre-registered rule"* pools `generalisation` (5) with `primary` (5). The primary five are not a
held-out surface for this question — the same table's own row calls them *"Confirmatory. Never a
tuning surface"*, ADR 0012 records that *"no arm in the primary benchmark is blind"*, and
evaluation README §9 says the primary benchmark is scored **once** with every choice already
fixed. Admissible only in this shape:

- [ ] The descriptor test runs on `generalisation` (N = 5) as its pre-registered endpoint.
- [ ] The primary arms enter only as a **post-hoc re-analysis of the single frozen scoring** of
      42 §4 step 4 — no second `score_arm` call — and the result is labelled exploratory.
- [ ] Nothing the primary arms show may change the method. If it would, the tier is burned.
- [ ] The power claim is restated at N = 5, not N = 10. Doc 48 §4 Regime B needs 6 proteins for
      80 % power at ρ = 0.95 and 8 at ρ = 0.90, so at 5 the test is underpowered for anything
      weaker than a near-perfect ordering, and the ADR says so before the run.

### P4 — Worst-arm AUC as a promoted endpoint

**This is the one that needed a clear answer, so here it is in two parts.**

**P4a — reporting the worst arm beside the mean: ADMISSIBLE, and it is not a protocol change.**
`score_arm` already returns per-arm AUC-ROC (evaluation README §3.2). The minimum over a set of
arms is an aggregation of numbers the frozen protocol already emits, taken outside
`allo.scoring`. The protocol freezes *what is computed per arm* — endpoint, estimator, tie rule,
null, decoys, multiplicity — and it does not enumerate which summaries a report may take over
per-arm outputs. §11 puts cross-arm organisation explicitly on the reporting side: *"these
organise reporting and never a decision."* Doc 49 §12.1 asks for exactly this and it costs one
column. Do it.

**P4b — promoting worst-arm AUC to an endpoint that decides anything: FORBIDDEN.** Three
independent sentences each close it, and the third closes it permanently.

1. **It changes the confirmatory statistic.** README §3.1: *"The mean midrank of the scoreable
   label set."* That statistic is frozen, and its permutation p is identical to one on AUC-ROC
   *because every null holds the positive-class size fixed*. A minimum over arms has no such
   equivalence and no null in the frozen protocol.
2. **It changes the multiplicity structure.** README §8: *"One confirmatory family, declared
   before any method exists: the three `corrected` arms, one per disease area, at α = 0.05 with
   Holm correction, one-sided upper"*, and *"The project therefore admits exactly one
   across-target decision at full α."* A worst-arm criterion is an across-target decision.
   Adding one, or substituting it for the declared sign test, edits the family.
3. **The window for re-freezing is shut.** `AGENTS.md`, the evaluation row: *"Nothing in it may
   change once a method has been scored."* Methods have been scored — 69 scorers × 4
   `development` arms in `experiments/2026-08-26-beats-distance`, plus 6 480 records in
   `2026-08-26-method-sweep`. So this is not "a protocol change requiring a re-freeze" that
   someone can go and do. It is a protocol change that is no longer available.

And the evidence points the same way, which is worth saying because it removes the temptation to
argue around the process. Doc 49 §4 measured it: selecting on the worst arm buys **0.5632 against
0.5639** on the held-out worst arm — 0.0007 in the wrong direction — and costs **0.058** of
held-out mean. Doc 49's own §12.2 concludes *"Do not switch the selection rule to the worst
arm."* Promoting it now would be adopting an endpoint after seeing that it changes the winner
(`eigenvector_centrality` → `gnm_fluctuation`), which is the pattern README §9 exists to forbid.

**Where the worst arm may legitimately decide something:** as a **pre-declared level floor on the
`development` tier**, inside the method-selection step that ADR 0012 already licenses. Doc 49
§12.2's own formulation — *"select on the mean and report the minimum, then treat any scorer with
a worst arm below ~0.60 as unproven"* — is a hyperparameter choice on the tuning set, not an
evaluation endpoint. That is admissible, in the P3 ADR, with the 0.60 named before it is applied.

### P5 — A pretrained model for structural features

**ADMISSIBLE WITH CONDITIONS, and the tier decides which conditions.** ADR 0027 replaces C2's
single ban with three tiers, and `AGENTS.md` C2 now reads *"MD-**trained** weights are a separate
tier: admissible, disclosed, and never load-bearing for the primary result."*

| If the component is | Tier | Ruling |
| --- | --- | --- |
| Trained only on static structures and sequences — pLMs, foldseek, AlphaFold pLDDT/PAE, geometric pocket detectors, alignment conservation and coupling; or not trained at all | **A** | Admissible without qualification. The primary result may stand on it |
| Trained on MD trajectories — PocketMiner, AlphaFlow, BioEmu, learned flexibility predictors | **B** | Admissible, disclosed, reported separately, **never load-bearing**. Enters only as a labelled ablation beside the tier A number it is compared against |
| An MD trajectory or MD-derived covariance passed at inference; **anything trained on this benchmark's holo structures or label sets** | **C** | Forbidden |

**The C1 sub-clause that decides most real candidates, and it is not the MD question.** ADR
0027's tier C forbids *"Anything trained on this benchmark's holo structures or label sets"*.
Every allosteric- and cryptic-site predictor is trained on curated site labels, and ADR 0012
records the specific exposure: ASD2023 ran AlloSitePro over all 20 386 human proteins and
predicted 66 589 sites, MYH7 among them, and *"no exclusion rule can remove a predicted pocketome
from a method's training history."* So a site predictor used as a feature source needs its
training corpus checked against all 14 frozen arms — and where the corpus cannot be determined,
ADR 0027 is explicit: *"'Training data not determined' disqualifies a component from use, because
an undetermined provenance cannot be placed in a tier."*

_Conditions._

- [ ] Tier assigned and stated in the report, per component.
- [ ] Training corpus named and cited. Undetermined provenance ⇒ not used.
- [ ] Corpus checked against the 14 arms' holo accessions and site annotations. Any hit ⇒ tier C.
- [ ] Tier B never carries the primary result; it appears beside the tier A number it ablates.
- [ ] ADR 0027's disclosure that has no clean fix is reproduced in the report: a PDB-wide
      pretrained model has seen holo entries that appear in our label sets, and date-based
      holdout cannot be applied retroactively to weights.
- [ ] C3 still applies to any hybrid: a learned front end that changes a quantum stage's
      hyperparameter changes its depth and qubit count, and both are reported.

---

## 3. Leakage these routes open that the suite does not catch

Ordered by severity. Each is a route no import trace and no current string guard sees.

### L1 — A prediction module can import any `allo.scoring.*` submodule and every guard stays green

**Proven, not argued.** Planting `from allo.scoring.nulls import evaluation_graph,
sample_matched_patches` into a prediction-path module and running the suite's own detectors over
it returns: `is_prediction_path` True, `reaches(... GROUND_TRUTH)` **None**,
`protected_path_violations` **empty**, `FROZEN_TOKENS` hits **none**, `runner_violations`
**empty**. The mechanism: `tests/test_no_leakage.py:249` builds the graph from each file's direct
imports, so `allo.scoring.nulls` → `{allo.inputs}` and the walk stops. At runtime the same import
executes `src/allo/scoring/__init__.py`, which imports `harness`, which imports
`allo.groundtruth.manifest` — the unredacted manifest — and binds `harness._positives` and
`harness.INPUT_FROZEN` in the prediction process. `allo/scoring/__init__.py`'s own docstring
claims *"nothing on the prediction path may import it"*; nothing enforces that claim.

**It is already exercised.** `docs/method/exploration/data/profile_graphs.py:16` reads

```python
from allo.scoring.properties import residue_properties
```

That script produces `frozen-graph-profile.json`, which is the descriptor source for docs 48 §3
and 49 §9 and therefore for P3's descriptor. Its first line says *"Apo-only, label-free."*
`residue_properties` is in fact apo-only (`src/allo/scoring/properties.py:23` imports
`allo.inputs` and nothing else), so **no label value flows today** — but the file is a
prediction-side descriptor generator whose import chain reaches the answer key, and the docstring
is doing the work a test should do. P1 and P2 put more code on exactly this route.

**The test, in two parts, both verified against the current tree.**

*Inside `src/`* — one line in the graph fixture: when a module imports `a.b.c`, add the package
edges `a.b` and `a.b.c`, because Python executes them. Re-running
`test_prediction_path_never_reaches_ground_truth` with that edge gives **zero false positives** on
the real tree, and the planted module reports
`allo.classical.zscore -> allo.scoring -> allo.scoring.harness -> allo.groundtruth.manifest`.

*Outside `src/`* — `FORBIDDEN_OUTSIDE` deliberately omits `allo.scoring`, because an experiment
must be able to score (`docs/playbooks/experiment.md`, evaluation README §13 item 4). The
distinction that holds is **package versus submodule**: forbid any imported name that resolves to
a file in `src/allo/scoring/`, computed rather than listed, so a submodule added later is covered:

```python
SCORING_SUBMODULES = {f"allo.scoring.{p.stem}" for p in (SRC / "scoring").glob("*.py")} - {
    "allo.scoring.__init__"
}
```

Measured on six probes: `from allo.scoring import score_arm, compare_methods` and
`from allo import scoring` are **clean**, while `from allo.scoring.nulls import ...`,
`import allo.scoring.harness as h`, `from allo.scoring.harness import _positives` and
`from allo.scoring.properties import residue_properties` are all **caught**. It flags
`profile_graphs.py` and nothing else in the repository.

### L2 — `data/patches/` is an unprotected, label-derived cache

`src/allo/scoring/nulls.py:325` puts the matched-patch pool in `ROOT/"data"/"patches"`. It is not
in `PROTECTED_PATHS`, which holds `data/raw` and `data/raw/eval` and not this. Reading one file
from the current tree:

- `members` has shape **(999, 18)** — 18 is `bcr_abl1_corrected`'s label patch size. C1 forbids
  *"not even the residue count."*
- `diagnostics` carries `observed_components`, `observed_mean_degree`,
  `observed_radius_of_gyration` and `observed_median_distance_to_source` — a four-number
  geometric fingerprint of the true site.
- The 999 patches are drawn *to match that fingerprint* over the candidate set, so their
  empirical per-residue occupancy is a smoothed localisation of the site. A method scoring each
  residue by its frequency in the pool would be scoring "how site-like is this residue" using the
  site's own geometry, with no label ever read by name.

Gitignored is not protected: the cache exists on disk after any evaluation run, and it is the
first thing an author implementing "a matched random ensemble" will find.

**The test.** Add `(ROOT / "data" / "patches").resolve()` to `PROTECTED_PATHS` and
`"PATCH_CACHE"` to `FROZEN_TOKENS`. With L1's fix, the import route closes at the same time.

### L3 — The runner gate does not inspect `docs/`

`tests/test_no_leakage.py:625` lists `docs` in `NON_RUNNER_TREES` on the argument that it holds
"non-executable evidence and freeze artifacts". `profile_graphs.py` is executable Python that
imports `allo.*` and writes a descriptor file the method will consume. This compounds the gap
`42-threats-and-confirmation.md` §3 already named for untracked experiment directories.

**The test.** Drop `docs` from `NON_RUNNER_TREES`. No suffix exemption is needed — `is_runner`
already returns False for `.md`, `.json` and `.yaml`, so the freeze artifacts stay out by
construction. Verified: the gate then inspects exactly one additional file,
`docs/method/exploration/data/profile_graphs.py`.

**On its own this fixes nothing**, and that is the part worth carrying: with `docs` dropped, that
file still reports **zero violations**, because `FORBIDDEN_OUTSIDE` omits `allo.scoring` by
design. L3 and L1 have to land together — the tree fix makes the file visible, the submodule rule
makes it fail.

### L4 — The new constants are hand-carried, and that is the T10 class

P1 introduces `M` and a degree-bin rule; P2 introduces a decile count; P4's floor introduces
0.60. None is visible to any import or path guard. `42-threats-and-confirmation.md` T10 is the
worked example — three constants re-tuned on curated labels reached the prediction path because
*"A person read three numbers and typed them in"* — and its lesson is the right one: *"The only
defence is that every constant on the prediction path names its provenance in its own
docstring, and that an audit reads them."* The specific failure to watch for here is a bin rule
or a decile count settled on because the four `development` arms looked better with it, which
doc 48 §6 rules out by name.

**The test.** Make them required keyword arguments with no default, as
`diversified_top_k`/`spatial_smoothing` now are; plus a test asserting that every module-level
numeric default in `src/allo/classical/` and `src/allo/quantum/` is either 0 or has a
`provenance:` line in its function docstring.

### L5 — Nothing records which arms have been scored, so P3's tier can be burned silently

A single `score_arm("<generalisation arm>", ...)` before the P3 ADR exists ends the
generalisability claim, and it leaves no trace anywhere the suite looks. The five protected data
routes guard *reading the answer key*; they do not guard *spending* a tier.

**The test.** Scan committed `experiments/**/records.jsonl` for any target id in the
`generalisation` tier, and fail unless the freeze ADR exists and is `accepted`. `tests/` may name
`docs/benchmark/secondary/frozen.json` — the tree is exempt from the runner gate — so the tier
membership is readable test-side.

---

## 4. What was traced to conclude the rest is clean

Named so a reader can re-run the same checks rather than trust this file.

- **C1, import graph.** Full transitive closure over `src/allo/**.py` with
  `tests/test_no_leakage.py`'s own `direct_imports`/`reaches`: no prediction-path module reaches
  `allo.groundtruth`. The single chain that exists is
  `allo.scoring -> allo.scoring.harness -> allo.groundtruth.manifest`, and `allo.scoring` is
  allow-listed. L1 is a gap in the *guard*, not a violation in the tree.
- **C1, the inputs boundary.** `src/allo/inputs.py:100–160` — `_PREDICTION_SCHEMA` is an
  allow-list, `active_site` is on it, `read_manifest` is not exported. P1 and P2 need `active_site`
  and the node set, and both are inside that allow-list.
- **C1, the candidate set.** ADR 0011's 2026-08-24 amendment plus `src/allo/scoring/nulls.py:119`:
  candidates are the node set minus the active site, apo-derivable, so P2a needs no label.
- **C1, the descriptor file.** `src/allo/scoring/properties.py` computes RSA, B-factor and
  hydrophobicity from the `ApoInput` alone, and `frozen-graph-profile.json`'s keys
  (`source`, `degree`, `topology`, `adjacency_spectrum`, `laplacian_spectrum`,
  `distance_to_source`, `confounders`, `geometry_vs_spectrum`) contain no label-derived field.
  P3's descriptor is input-side. It does profile all 14 arms including the primary five, which is
  legitimate — a method receives the apo structure — but it is why P3's conditions bar the
  primary arms from feeding back into the method.
- **C2.** No proposal reads a trajectory or an MD-derived covariance. P5 is the only route that
  touches training provenance, and ADR 0027 tiers it.
- **C3/C4.** None of P1–P4 is a quantum method. P1 multiplies the cost of any quantum scorer it
  wraps by `M`, and P5's front end can move a quantum stage's hyperparameter; both must carry the
  resource restatement, which is recorded as a condition rather than as a finding.
- **C5/C6.** Untouched. Every proposal acts on the frozen chain's contact topology.
- **The scoring API whitelist already holds.** `test_scoring_public_api_never_returns_a_label_set`
  asserts `scoring.__all__ == {compare_methods, holm, protocol, score_arm}`, so a `worst_arm`
  helper added inside `allo.scoring` fails today. P4a's column belongs outside the package, and
  the existing test enforces that without amendment.
