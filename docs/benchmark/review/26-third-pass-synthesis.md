# Third-pass audit: the repairs, audited

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the nine required baselines are now
> `allo.scoring.baselines`.

**Closed 2026-09-02, after the second pass.** `11-synthesis.md` audited the three frozen
layers and produced ADRs 0029-0036, a six-arm primary re-freeze and protocol version 3.
`25-second-pass-synthesis.md` audited that work and produced five blockers and thirteen
further findings. **Its own repairs were then unaudited, and its disposition table was
wrong about what it had disposed of.** This pass audits the repairs.

**Scope.** Three delegated reviews, one constraint audit against C1-C6, one independent
`gpt-5.6-sol` pass over the whole repository, and my own measurements. Every finding below
was re-checked by me against the code or the deposited data before it was written down.
Where a delegated agent and I disagreed, the measurement is printed and it decides.

**Nothing here is frozen and nothing here moves a freeze.** Both freezes verify unchanged
after every repair in this document: `uv run allo benchmark verify --set all` and
`uv run allo evaluate verify --detect` both exit 0, and `make check` exits 0.

---

## 0. Headline

**Three C1 leaks, and one of them was reported as refuted.**

1. **The path guard could be walked past with `.joinpath`.** A module in `allo.network`
   recovered every arm's positive count — the sealed `generalisation` tier included — from
   the protected matched-patch cache, and **all 34 leakage tests passed**.
2. **`docs/targets.md` holds 12 of 12 cardiac myosin label residues.** The second pass
   refuted this finding. The refutation was a false negative in its own detector.
3. **Both benchmark READMEs publish the positive count** for every arm, beside the holo
   accession and the effector, for the five sealed arms as well.

**One frozen rule had no implementation.** `decision.alpha`, `decision.confirmatory_family`
and `decision.correction` had no reader in `src/` or `experiments/`, and `holm` had no caller
outside the tests. The only Holm actually run in the repository corrects over a **different
family**.

**One cache key was blind to the thing its own comment promised it covered.** The
matched-patch pool is matched on mean degree and radius of gyration; its key was identical at
contact cutoffs 4.5, 6.0 and 8.0 while the mean degree ran 9.531, 13.398 and 24.262.

**And a structural finding about the second pass.** Its §5 disposition table disposes of
**one** of its own thirteen §3 findings. Ten of the remaining twelve are open. Two of its row
labels do not match their content.

---

## 1. Blockers, all repaired in this pass

### 1.1 `.joinpath` and `os.path.dirname` walk past the path guard — **repaired**

`constant_paths_from_source` in `tests/test_no_leakage.py` models the `/` operator, f-strings,
`os.path.join` and string addition. It did not model `Path.joinpath`, which is the same
operation spelled as a method, and it did not model `os.path.dirname`, so any path built on a
`dirname` prefix evaluated to `None` and vanished from the scan.

Measured, before the repair:

| form                                                     | caught                         |
| -------------------------------------------------------- | ------------------------------ |
| `Path("data") / "patches"`                               | yes                            |
| `Path("data").joinpath("patches")`                       | **no**                         |
| `Path("docs/benchmark/primary").joinpath("frozen.json")` | **no** (token guard caught it) |
| `os.path.dirname(...) + "/metrics.json"`                 | **no**                         |

`data/patches` is the severe one, because it is protected as a path and is **not** a frozen
token, so nothing else backstops it. The decisive test: a module planted at
`src/allo/network/_probe_leak.py` reading the cache with `.joinpath` recovered the positive
count for 134 cached arms and the whole leakage suite passed. After the repair the same probe
fails `test_the_prediction_path_cannot_build_either_route_out_of_pieces`.

**This is the third instance of one failure mode.** The parent-package route (2026-08-27) and
the `src.` prefix (2026-09-02) were the first two: the guard reads the text correctly and the
interpreter accepts a form the text does not model. Three probes were added to
`test_constant_path_guard_catches_composition_and_quote_variants`.

### 1.2 `docs/targets.md` is an answer key, and the refutation was a detector failure — **repaired**

`25-second-pass-synthesis.md` §5 records:

> **Refuted as written.** `docs/targets.md` holds none of the twelve cardiac myosin label
> residues; the claim that it does was wrong.

`docs/ROADMAP.md` repeated it. **Both are false.** `docs/targets.md:170` reads:

> The site is reproducible across all six copies: **Tyr164, Thr167, Asp168, His666, Pro710,
> Asn711, Arg712, Ile713, Glu774** in every one, plus Arg721, Tyr722, Leu770 in most.

Normalising the three-letter codes and checking against the freeze:

```
frozen label_residues : [164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770, 774]
recovered from targets.md : 12 of 12, for BOTH myosin arms
```

The sweep that produced the refutation matched bare integers on a word boundary, so `Tyr164`
never matched `164`. **A detector's false negative is the one kind of finding that closes a
question instead of opening it**, which is why this is ranked above the leak itself.

The sweep was re-run with codes normalised, over every tracked `.md`, `.yaml`, `.json`,
`.txt`, `.csv`, `.tsv`, `.toml`, `.py`, `.sh` and `.ipynb` outside the protected trees, at the
same 400-character window. It returns exactly three files that reproduce a complete label set:
the two manifests, which are route 2 and already guarded, and `docs/targets.md`, which was
not.

### 1.3 Both benchmark READMEs publish the positive count — **repaired**

`primary/README.md:243` and `secondary/README.md:178` tabulate a `Scoreable` column that is
the positive count, beside `Apo → holo` and `Effector`. Verified against the freeze for the
five arms that are **sealed until Phase 5**:

| sealed arm    | README `Scoreable` | `secondary/frozen.json` | holo published |
| ------------- | ------------------ | ----------------------- | -------------- |
| `chk1`        | 12                 | 12                      | `3JVR:A` `AGX` |
| `smyd3`       | 12                 | 12                      | `7BJ1:A` `QKT` |
| `glucokinase` | 19                 | 19                      | `3F9M:A` `MRK` |
| `p97_vcp`     | 17                 | 17                      | `5FTJ:A` `OJA` |
| `ecoli_cps`   | 19                 | 19                      | `1T36:A` `U5P` |

That is the payload `selection.json` became route 3 for and `data/patches/` became route 6
for, sitting unguarded beside the `frozen.json` protected on the first day.

**Repaired by protecting `docs/benchmark/primary/` and `docs/benchmark/secondary/` whole**,
on the argument `evaluation/` and `review/` already use: a file added later is protected by
default rather than leaked by default. `allo.inputs` must spell both manifests, so
`MANIFEST_READS` exempts the two manifests and the two directories and **nothing else** — the
READMEs stay guarded for that module too, and a test pins it.

The guarded route count goes from ten to **thirteen**.

---

## 2. The frozen decision rule had no implementation — **repaired**

`manifest.yaml` freezes a confirmatory family, an alpha and a correction. Nothing read them:

```
$ grep -rn '\["decision"\]' src/ experiments/
(nothing)
$ grep -rn "holm(" src/ experiments/ | grep -v "def holm"
experiments/2026-08-26-beats-distance/run.py:178:            reject = holm(pairs)
```

`harness.holm` had **no caller outside the tests**. The one Holm actually run in the
repository predates ADR 0032 and corrects over the whole scorer battery _within_ an arm
against `distance_from_source_negated` — a different family from the declared one. The same
runner reports `n_reject_confirmatory` as an uncorrected per-arm count over six arms.

`claim_family` — ADR 0032's second confirmatory family — was unbuilt entirely.

**Repaired.** `allo.scoring.confirmatory_verdict` reads `decision.alpha`,
`decision.confirmatory_family`, `decision.correction` and `decision.claim_family` from the
frozen manifest, runs Holm at the frozen alpha, and **raises** if the arms supplied are not
exactly the declared family. Nothing would previously have noticed a fourth arm entering the
family or Holm running over six.

**It returns per-arm verdicts and no aggregate, deliberately.** ADR 0032's own table says a
rejection licenses that _the arm_ has signal. Neither the ADR nor README §8 says what
"clearing a family" means — all three arms, or one — while the manifest requires a method to
"clear BOTH families". **That is an undefined term in a frozen decision rule** and it is
listed as open in §4. Choosing between the readings after seeing a result is exactly the
hyperparameter this layer exists to prevent, so the function reports `n_reject` and leaves
the rule to the ADR that states it.

---

## 3. The matched-patch cache key was blind to the contact cutoff — **repaired**

`nulls.py` builds the pool's cache key from the observed patch, the node order and the source
set, under a comment stating that leaving the graph out "meant a changed label set or contact
cutoff returned stale patches and `allo evaluate verify` still exited 0 — a false green in
exactly the case verification exists to catch."

None of the three terms depends on the cutoff for a motif-sourced arm. Measured on
`cardiac_myosin_corrected`:

| cutoff | digest         | mean degree |
| ------ | -------------- | ----------- |
| 4.5 Å  | `827dacf174f1` | 9.531       |
| 6.0 Å  | `827dacf174f1` | 13.398      |
| 8.0 Å  | `827dacf174f1` | 24.262      |

The pool is matched on `mean_degree` and `radius_of_gyration`, and both move with the cutoff.
`_derive_arm` writes the cached diagnostics into the freeze, so the verification compared
stale against stale. The guard the comment promised did not exist.

**Repaired** by adding the degree sequence to the digest; the key now moves at every cutoff.
The cutoff has never moved, so **no recorded number was affected** — confirmed by re-running
`uv run allo evaluate verify --detect`, which re-drew all fifteen pools and reported every
derived value matching the freeze.

---

## 4. Documents that stated a refuted or stale fact — **repaired**

| where                          | what it said                                                                                   | what is true                                                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `evaluation/README.md:53`      | "`n_decoys` is **label-free**: it is a sample size, not a property of the answer key"          | False. `decoys.classify` picks the site pocket by maximum label coverage. The manifest was corrected on 2026-09-02 and this cell was not |
| `adr/0030` decision 5          | "selecting on `n_decoys` alone … `n_decoys` is label-free and is a sample-size criterion"      | Same false sentence, in the **ADR of record**. The criterion is `n_detected`, which selects the identical setting on all five arms       |
| `evaluation/manifest.yaml:224` | header still read "SELECTING ON `n_decoys` ALONE" twelve lines above its own correction        | Now reads `n_detected`                                                                                                                   |
| `evaluation/README.md:483`     | "Site coverage runs 0.09 on `mkp5`, 0.19 on `ns5b` and 0.36 on `ptp1b`"                        | Version-2 numbers under a version-3 heading. The v3 table forty lines above says 0.4545, 0.3125, 0.3636                                  |
| `scoring/decoys.py:192`        | `cavity_volume` "**clears the confirmatory family**: … rejects on all three confirmatory arms" | Under v3 it rejects on **one** of three. The manifest says no document may say otherwise; this was the last one that did                 |
| `primary/README.md:434`        | "**Re-frozen at protocol version 3** on `n_decoys` alone"                                     | A **frozen-layer README** describing current state, missed by the 2026-09-02 correction sweep. Now reads `n_detected`                    |

No frozen value moved for any of these. They are documentation repairs.

**Four pass records still carry the withdrawn criterion and are deliberately not edited**: `04-decoys-and-power.md:118`, `11-synthesis.md:24` and `:140`, `21-protocol-v3-statistics.md:632`, and `22-dataset-eda-v2.md:165` and `:516`. Each was true when written and each is the record of what a pass concluded. This tree's rule is that a correction lives in the newer document, not in the older one. Read them against ADR 0030's own correction block. The distinction that decides which way an occurrence goes: a document describing **current state** is repaired, a document recording **what a pass found** is left standing.

---

## 4b. Adjudicating the adversarial pass

`gpt-5.6-sol` audited the whole repository from the first commit and returned twelve findings.
Judged one at a time, against the code or a measurement I ran myself.

| #   | Claim                                                                     | Verdict                                                                      |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1   | The sealed `generalisation` tier has already been consumed                | **Confirmed. The most important finding of the pass.** §4b.1                 |
| 2   | The in-process scoring boundary exposes the answer key                    | **Route demonstrated is refuted; a variant is real and now closed.** §4b.2   |
| 3   | The cross-run record rule is bypassable by `glob`                         | **Confirmed. Closed for `glob` and `rglob`; `iterdir` is a stated residual** |
| 4   | The repaired decoy statistic has no matching type-I validation            | **Confirmed. Open** (5.16)                                                   |
| 5   | The detector-selection history is circular                                | **Documents fixed; the prospective-criterion point stands. Open** (5.17)     |
| 6   | The tie repair changed stored DCC values and records were not regenerated | **Confirmed by re-running. Open** (5.18)                                     |
| 7   | The cache key still does not hash the graph                               | **Confirmed. Closed** — §3 now hashes adjacency and coordinates              |
| 8   | The Faccin repair withdraws the theorem and then reinvokes it             | **Confirmed. Open** (5.19), Phase 2                                          |
| 9   | The finite-sample decoy power claim is false                              | **Confirmed by independent integration. Closed as a correction**             |
| 10  | The cavity triple's causal explanation is false                           | **Confirmed. Closed** — §4                                                   |
| 11  | `supportive_only` omits `cardiac_myosin_mandated`                         | **Confirmed. Closed**, with a test that partitions every primary arm         |
| 12  | Human-facing operating documents are outdated                             | **Confirmed. Closed** — §4                                                   |

### 4b.1 The sealed tier is not sealed

`secondary/manifest.yaml` states the rule in its own words:

> `generalisation` — the generalisability and scalability claims. Phase 5, and **NOT BEFORE
> the method is frozen. Reading it early destroys the only thing it is for.**

`24-conservation-measured.md` says it "measures it on all fifteen arms" and publishes a
label-derived AUC-ROC for each of the five sealed arms — `chk1` 0.5428, `glucokinase` 0.6195,
`smyd3` 0.0446, `p97_vcp` 0.2643, `ecoli_cps` 0.4794 — beside per-arm coverage. `22-dataset-eda-v2.md`
does the same for seven apo-only descriptors across "all fifteen label sets", and `12` did it
before at fourteen.

**`25-second-pass-synthesis.md` §2.1 defends protocol version 3 with the sentence "the
`generalisation` tier is still sealed and is the set that carries the generalisation claim".
That sentence is false**, and it is the load-bearing half of that defence.

**Severity, stated honestly.** What leaked is not a method's score. It is the separating power
of confounder and descriptor columns on the held-out arms — which is exactly the information a
method designer would use to decide whether to include such a column. The tier's own rule
admits no degree: reading it early is what the rule forbids.

**This needs an ADR and I have not written one**, because the choice is a research decision
with two defensible answers: declare the tier burned and rebuild an unopened one from the 34
ASD leads `20-extension-closure.md` catalogued, or declare descriptor-level reads permitted
and amend the rule to say so prospectively. Both change what the generalisation claim means.

### 4b.2 The scoring boundary, adjudicated precisely

The adversarial model measured this runner expression and reported zero violations:

```python
getattr(importlib.import_module("allo.scoring.harness"), "_" + "positives")(target)
```

**It tested `runner_violations` alone.** The whole suite catches it:
`test_the_prediction_path_cannot_build_either_route_out_of_pieces` asserts that `importlib`
and `__import__` appear nowhere in a run script. The demonstrated route was already closed.

**The underlying hole is real by a different spelling.** Dropping `importlib` —
`from allo.scoring import harness` then `getattr(harness, "_" + "positives")` — evades both the
frozen-token guard, because `_positives` never appears as a literal, and the dynamic-import
ban, because there is no dynamic import. A runner must be able to import `allo.scoring`, since
that is the scoring path, so the ingredient is removed instead: an attribute name built at
runtime is now a violation in `src/` and in every run script, with three probes pinning it.

**What no static guard can fix** is the model's structural point: `score_arm` returns
`n_positive`, `prevalence` and the true site's geometry, and a runner holds the module object
in its own process. That is item 5.11 and it needs an ADR, not a token.

---

## 4c. What protocol version 3 moved in the committed sweeps — **measured**

The second pass recorded that the committed experiment records were stale and cited three
`dcc_angstrom` values. That was true and it was the wrong headline. Every record in the three
2026-08-26 experiments carries `protocol_frozen_on: 2026-08-25`, which is **protocol version
1**. Version 3 re-froze the decoy detector (ADR 0030), so the question is which columns moved.

It was measured rather than argued. 216 records were re-scored through the current `score_arm`
— all 54 swept scorers, all four `development` arms, the evaluation-default graph, no
detrending — reproducing the runner's own construction and changing only the code and the
freeze underneath it.

| field                                                                         | moved       |
| ----------------------------------------------------------------------------- | ----------- |
| `nulls.decoy_pockets.n_decoys`, `.p`, `.site_pocket_rank`, `.n_pockets_ranked`, `.minimum_attainable_p` | ~all        |
| `endpoints.auc_roc_vs_decoy_linings`                                          | 216 / 216   |
| `nulls.decoy_pockets.site_pocket_label_coverage`                              | about half  |
| `endpoints.dcc_angstrom`                                                      | **6 / 216** |
| `mean_rank`, `auc_roc`, `auc_pr`, `precision_at_5`, `hits_at_5`, `recall_at_5` | **0 / 216** |
| `nulls.matched_patch.p_calibrated`                                            | **0 / 216** |

**The screening statistic did not move.** The sweep ranks variants on `mean_auc_roc`, and no
`auc_roc` changed on any of the 216. The selection the sweep made stands, and so does every
`n_reject_matched_patch_uncorrected` in `metrics.json`.

**The decoy columns moved a long way, and in the direction ADR 0030 predicted.** On `mkp5` the
decoy count goes 3 to 14 and the site pocket's label coverage 0.0909 to 0.4545; on `ns5b`, 19
to 50 and 0.1875 to 0.3125. Those coverage figures are the same ones the layer README publishes
for version 3, so the re-freeze is what produced them and the committed records predate it.

**The six `dcc_angstrom` moves are all on `hiv_rt` and all downward**: `degree` and
`contact_number` 32.530 to 21.655, `clustering_coefficient` 30.006 to 18.212,
`sequence_distance_from_source_negated` 13.014 to 9.164, `hop_distance_from_source_negated` and
`ohm_path_probability` 11.788 to 10.654. The cause is the `top_k_indices` repair. The withdrawn
rule sorted positives last inside a tie, so it reported the predicted list as further from the
site than it is. One-sided drift is exactly what a label-informed pessimistic rule predicts, and
it appears only where scores are integer-valued and only on the largest arm.

**Not re-run, and that is a decision rather than an omission.** A refresh costs about 2.4 hours
and would change no number that decided anything. It also cannot be done in place: the resume
key is `arm|graph|scorer|detrend` and carries no protocol version, so a re-run appends nothing
until `records.jsonl` is deleted. The three `notes.md` files now carry the table above, the
registry carries three rows, and `docs/playbooks/experiment.md` carries the rule that would have
made the staleness visible.

**One coverage gap came out of the same measurement.** The scorer registry holds 69 entries
today and the sweep covered 54, with nothing removed. The fifteen unscreened are the whole of
`interference`, `connectivity` and `quantumness` plus `gnm_transfer_entropy_net` — the same
modules that carry the open C3 resource-accounting gap.

---

## 5. What is open

Ranked by what it costs. Each names the ADR that would have to accept it.

> **FIVE OF THESE CLOSED ON 2026-09-02 WHEN THE METHOD LAYER LEFT `main` (ADR 0037).** Their
> subject is archived, so they bind nothing on this branch. They are **not** answered, and
> every one of them returns the moment Phase 2 restarts.
>
> | #    | why it closed here                                                          |
> | ---- | ----------------------------------------------------------------------------- |
> | 5.6  | the 14 unpriced quantum scorers are on `method-layer-archive`. C3 has nothing to price on `main` |
> | 5.18 | the stale records went with the runs. Their measured drift is recorded in section 4c |
> | 5.19 | `quantum/quantumness.py` and `walk.py` are archived. The two misstatements go with them |
> | 5.20 | the 15 unscreened scorers are archived. Nothing on `main` is unscreened          |
> | 5.21 | the resume key was in an archived runner. The rule it needed is now in `docs/playbooks/experiment.md` |
>
> **Sixteen remain open**, and every one of them is a frozen-layer item. That is the point of
> the removal: what is left to fix is all in one layer.


| #    | Finding                                                                                                                                                                                                                                                                                                                                                            | Needs              |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| 5.1  | **The myosin B-factor defects are undisclosed and one document asserts the opposite.** `5TBY`'s B column runs 0.00-7.30 and `9GZ2`'s mavacamten carries B = 0.00 on all 20 atoms — the ligand that defines **both** myosin label sets. `primary/README.md:232` says "Label residues are as ordered as the chain or better … The sites are not modelled into noise" | ADR 0031 amendment |
| 5.2  | **A claim-family arm is scored against a truncated answer key.** `bcr_abl1_corrected` loses 2 of 20 transferred labels and is in both families. The completeness test exists for the nine secondary arms (`test_every_transferred_label_survives_into_the_node_set`) and has no primary equivalent                                                                 | ADR required       |
| 5.3  | **Negative class (b) has no baseline threshold.** A label-blind cavity ruler reaches Fisher p = 0.0154 on that endpoint. ADR 0025 set a "beat the baseline" bar for the matched-patch endpoint only                                                                                                                                                                | ADR 0032 amendment |
| 5.4  | **"Clearing a family" is undefined** while the manifest requires clearing both. All-of-three and one-of-three are both readable and they give opposite verdicts                                                                                                                                                                                                    | ADR 0032 amendment |
| 5.5  | **The combined (b) test is 7.6x to 36x conservative** (measured size 0.0014-0.0066 against nominal 0.05), and ADR 0030 still calls it "testable at α = 0.05"                                                                                                                                                                                                       | ADR 0030 amendment |
| 5.6  | **C3 is an open violation of record.** 14 of the 25 quantum scorers have no resource account — the whole of `interference`, `connectivity` and `quantumness`. Finding C-8 was marked Confirmed by the second pass and never entered its disposition table. `docs/report/conformance.md` discloses it honestly                                                      | Phase 2            |
| 5.7  | **Four documents state a false "cannot reject at any data"** on `ptp1b` and `ns5b`. The true permutation floors are 0.000276 and 0.000104, below Holm step 1. Two of the four are the ROADMAP and the experiment registry                                                                                                                                          | repair             |
| 5.8  | **Clause (xii) ships one taxonomic level shallower than ADR 0012** — Pfam family where the ADR says clan — and no InterPro or Pfam release is pinned, so the clan rule cannot be run                                                                                                                                                                               | ADR 0012 amendment |
| 5.9  | **ADR 0024's title, decision and consequences are still version 2** (`probe_out 4.0 / removal_distance 2.4 / volume_cutoff 5.0`), and ADR 0030 does not name it, so the supersession is asserted from one side only                                                                                                                                                | repair             |
| 5.10 | **A prediction-path module carries a holo-derived number.** `inputs.py:97` records the myosin motif validation as "Jaccard 0.483 on `9GZ3`:A and 0.516 on `9GZ2`:A"; `9GZ2` is the holo entry. The apo row is within 0.03, so the decision stands on apo evidence alone and the holo number is redundant. C-5 was Confirmed and never dispositioned                | repair             |
| 5.11 | **`score_arm` still writes `n_positive`, `prevalence` and the true site's geometry** into every record. The second pass recommended stripping them at write time and closed the item a different way, by narrowing the read route. The payload is unchanged                                                                                                        | ADR required       |
| 5.12 | **`max_attempts_per_patch = 4000` is an unfrozen constant that decided a documented outcome.** The `cardiac_myosin_mandated` 0.05 rung is recorded as undrawable; it drew 822 of 999 and stopped at exactly `999 x 4000` attempts. The frozen 0.10 tolerance is not at risk                                                                                        | repair             |
| 5.13 | **ADR 0035 calls an untracked directory a "196 KB committed artifact".** Both halves are wrong: the content is ~163 KiB and `data/conservation/` is untracked. Review `24` says 172 KB, which matches neither                                                                                                                                                      | repair             |
| 5.14 | **Roughly 28 of review `23`'s 34 documentation contradictions are open**, including `CONTRIBUTING.md` instructing a contributor to file the next data route as "a sixth" when there are thirteen, two files still giving the ADR count as 25, and `docs/report/conformance.md` describing pre-ADR-0031 and pre-ADR-0036 reality with no staleness banner           | repair             |
| 5.15 | **No occupant instrument is published** for clause (iii) or clause (x). Water, glycerol, sulfate and PEG have no declared side, and review `17` found no single formal definition exists in the field either                                                                                                                                                       | ADR required       |
| 5.16 | **The tested form of negative class (b) has no type-I measurement that covers it.** Review `21`'s family gate computed the observed value as the whole label set's mean midrank — the statistic §1.4 of the second pass replaced. The shipped statistic is the site pocket's lining, and the replacement power simulation draws the site and every decoy from the same unit-variance law, which the real linings do not satisfy: they differ in size and are spatially correlated. An independent 10 000-field rerun with the current statistic gave Fisher sizes 0 to 0.0005, so the direction is conservative — but the cited number does not describe the shipped test | ADR 0030 amendment |
| 5.17 | **`n_detected` may be a post-hoc justification.** It selects the same setting on all five swept arms, so no value moved, and the correction is now in every document. What does not exist is a timestamped record showing `n_detected` was named **before** the label-dependent `n_decoys` was inspected. The honest statement is that the freeze is defensible and its prospective status is unevidenced | disclosure |
| 5.18 | **The committed experiment records are stale against the current protocol, and the extent is now measured.** All 6480 method-sweep records carry `protocol_frozen_on: 2026-08-25` and the protocol is version 3, frozen 2026-09-02. Re-scoring **216 records** through the current `score_arm` — all 54 swept scorers on all four `development` arms — moves **every** `nulls.decoy_pockets` field and `auc_roc_vs_decoy_linings`, and moves `dcc_angstrom` on **6 of 216**. It moves `mean_rank`, `auc_roc`, `auc_pr`, `precision_at_5`, `hits_at_5`, `recall_at_5` and the matched-patch `p_calibrated` on **0 of 216**. The screening statistic is unmoved, so the sweep's variant selection stands. **This row previously said "every DCC and top-5-derived field is affected", which the measurement refutes** | banner, not re-run |
| 5.20 | **Fifteen scorers have never been screened.** `allo.classical.SCORERS | allo.quantum.SCORERS` holds 69 today; the sweep covered 54 and nothing was removed. The fifteen added since are the whole of `interference`, `connectivity` and `quantumness` plus `gnm_transfer_entropy_net` — **the same modules that carry the C3 gap in 5.6**. No arm has a screened number for any of them | Phase 2 |
| 5.21 | **The sweep's resume key cannot see a protocol change.** `run.py` keys a completed record on `arm\|graph\|scorer\|detrend` and skips it if present. The protocol version is not in the key, so re-running against version 3 keeps every version-1 row and appends nothing. A refresh has to delete `records.jsonl` first, which is why the staleness in 5.18 was invisible | repair |
| 5.19 | **`quantum/quantumness.py` withdraws the Faccin theorem and then keeps invoking it** — a site-basis adjacency state is still called "the zero-energy case the theorem describes", the top adjacency gap is still called the theorem's denominator, and `docs/ROADMAP.md` still carries the `E/Δ` diagnosis as settled causation. `walk.py` also calls the Perron vector the ground state of `H = A`, where it is the maximum-eigenvalue state | Phase 2 |

---

## 6. What held

A clean check is a result.

- **Both freezes re-derive**, before and after every repair here. `allo benchmark verify --set
all` over six primary and nine secondary arms; `allo evaluate verify --detect` at protocol
  version 3 over fifteen arms and 777 decoy pockets.
- **The decoy pocket count reconciles.** 844 pockets detected, 777 scoreable decoys after the
  site pocket and its halo are removed. The two numbers appear in different documents and are
  the same measurement.
- **The prevalence spread does not touch the confirmatory endpoint.** Prevalence runs 1.29 %
  to 10.96 %, an 8.5-fold range, and 1.62 % to 10.81 % inside the confirmatory family. The
  confirmatory endpoint is the mean midrank, which is exactly AUC-ROC, and AUC-ROC is
  prevalence-invariant. AUC-PR and precision@5 are prevalence-dependent, are reported rather
  than tested, and the layer README already says so.
- **Every stochastic step is seeded.** Nine `default_rng` sites in the scoring path, every one
  from an explicit seed; no global generator.
- **`compare_methods` is genuinely paired**, per residue on the rank difference, against the
  byte-identical cached null the confirmatory test uses.
- **The probit rescale is applied at every Holm level**, floored at 1 twice, verified
  numerically at the α/3 step.
- **The Fisher combination reproduces the manifest** to the printed digits: 0.00136894 against
  0.00137, 0.00045299 against 0.000453.
- **`top_k_indices` no longer depends on the answer key** — the second pass's repair holds, and
  its own §2.7 description of the code is now the stale text.
- **C2, C5 and C6 pass.** No trajectory and no MD-derived covariance anywhere; every
  `covariance` in the tree is analytic. Node sets recomputed from the mmCIF agree with the
  freeze on all six primary arms. The contact graph is geometric.
- **C1 by import is clean**, parent-package edges included, and the `src.` prefix repair is
  correct and probed.

---

## 7. A note on the second pass's disposition table

`25-second-pass-synthesis.md` §3 lists thirteen findings. Its §5 disposition table disposes of
**one** of them — the row labelled `§4`, which refutes 3.3. The row labelled `§3` disposes of
the two code defects from §2.6 and §2.7, not of any §3 finding, and the row labelled `§2 C-4`
disposes of C-2. Findings C-1, C-4, C-5, C-6 and C-8 were each marked **Confirmed** in §2 and
none has a disposition row.

That is not a scientific defect and it produced no wrong number. It is why ten open items in
§5 above read as new: they were found, written down, and then lost between two sections of the
same document. **A disposition table that does not enumerate every finding it is disposing of
will drop findings**, and this one dropped eleven.
