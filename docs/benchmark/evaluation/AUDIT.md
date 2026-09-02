# Audit of the frozen evaluation layer

**Date: 2026-08-25. Verdict at audit: NOT CONFIRMED — two defects blocked scoring.
Status now: CONFIRMED at protocol version 2. Every finding in this file is repaired,
disclosed, or declined with a reason. Nothing is left silently open.**

> **This file audits version 2. The layer is now at version 4, frozen 2026-09-03.** Nothing
> here was reopened by that: version 3 was forced by the **input** layer moving, not by a
> defect found here. What changed, and why each change is not a hyperparameter, is in
> [`README.md`](README.md) §0. The wider audit that produced it is
> [`../review/`](../review/), and the decisions are ADRs 0029 to 0036. Read this file for the
> version-1 defects and their repairs; read §0 for what version 3 does differently.

Eight independent audits ran against `README.md`, `manifest.yaml`, `frozen.json`,
`src/allo/scoring/`, ADRs 0022–0024, `docs/benchmark/evidence/evaluation-metrics.md` and
`experiments/2026-08-25-null-calibration/`. Every number below was recomputed from a
committed file or measured by a script. Nothing is quoted from prose.

The layer's **design** is strong. The calibration gate, the two-ended test, the honest power
analysis and the disclosed decoy floor are ahead of the published field. The defects were in
the **composition** of the procedure, in **numbers that no committed code produces**, and in
**one baseline nobody ran**.

## What changed, and where to read it

| Finding                        | Repair                                                                                                                  | Record                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **B1** FWER not controlled     | `size_ratio` calibrated at every Holm level, probit rescale. Re-ran the calibration on all 14 arms.                      | ADR 0025, README section 6.3                        |
| **B2** trivial baseline passes | `cavity_volume` is now the first required baseline; `allo.scoring.decoys.cavity_volume_score` implements it.            | ADR 0025, `manifest.yaml`                           |
| **B3** (downgraded) misquote   | One dropped word restored. It is not a fabrication and it was not a blocker.                                             | Section 1 below                                     |
| Mechanism claim unfalsified    | Two further repairs run. Both fail, and both refute the explanation ADR 0023 gave.                                       | `experiments/2026-08-25-null-repairs/`, README 6.2  |
| Claims no code produced        | recall@5 and the site pocket's rank are now computed and reported.                                                       | `harness.py`, README section 3.2                    |
| Two endpoints the field expects | DCC and three confounder columns were first deferred to Phase 3. Wrong for DCC, which needs no method. Both frozen now. | ADR 0025 amendment, README sections 3.2 and 11      |
| Leakage, cache, unrun gates    | `_positives` token, cache key digest, detector-version assert, `--detect` in `make verify`.                              | Section 2 below                                     |
| Seven wrong numbers            | All corrected against their generators. One of them was in this file and is corrected here.                             | Sections 1 and 3                                    |
| Fourteen citations             | Corrected, with two claims narrowed and one withdrawn as false.                                                          | Section 4                                           |
| M9-M11, M14 disclosures        | The decoy null's size bias, its unreachable floor, the ratio's sampling error and the pool's off-centre draw are stated. | README sections 5.3 and 6.3                         |
| M13 sensitivity at the wrong level | The minimum detectable effect is now measured at **every** Holm level, not only at alpha.                            | README section 7.1, `run_calibration` power stage   |
| M15 c-Myc                      | ADR 0020's blocker was recorded nowhere on the roadmap. It is recorded now, and it is still live.                        | `docs/ROADMAP.md`, Phase 2 entry gate               |
| No test for "beat a baseline"  | The manifest required beating the baselines and defined none. `compare_methods` is that test, frozen before any method. | ADR 0025, README section 8, `manifest.yaml`         |
| Bootstrap CI, redundancy cut   | Declined with reasons: the label patch is not exchangeable, and redundancy is controlled at family level upstream.       | README section 3.3                                  |

> **Correction, same day.** B3 was first written as "the quotation is not in the paper".
> That was wrong. The sentence is in the paper, verbatim except for one dropped word. It
> is a misquote, not a fabrication, and it is not a blocker. B3 is rewritten below and
> moved to the corrections list.
>
> **Correction, same day.** Section 6 first proposed about 4 500 lines of deletions. Half of
> that was wrong: sections 8 and 9 of the evidence file are its most valuable parts under R3,
> and deleting the superseded literature review would have broken 18 live cross-references in
> the file that supersedes it. 2 075 lines were deleted, and section 6 records both lists.
>
> **Correction, same day.** Section 5 listed residue-centroid DCC and four confounder columns
> as missing, and the first repair deferred them to Phase 3 because "they need a method to
> correlate against". That is false for DCC: it is a function of the top-5 list, the labels and
> coordinates, so nothing blocked it, and deferring it past the freeze is the move this
> manifest forbids. Both are frozen at protocol version 2. DCC justified itself on first use —
> see ADR 0025.
>
> **Numbers below are the audit's, measured under protocol version 1.** Where version 2
> changed one — the cavity-volume p-values tightened, for instance — ADR 0025 and
> `experiments/REGISTRY.md` carry the current value. This file is not re-run; it is the record
> of what the audit found.
---

## 1. Blockers

### B1 — The confirmatory procedure is not FWER-controlled at α = 0.05

`p_calibrated = p × α / α*` is a linear rescale. It is exact only at `t = α`. The null CDF is
convex in the tail, so at the tighter Holm steps the test is **larger** than nominal.

| Arm                        | size at α/3 | size at α/2 | size at α |
| -------------------------- | ----------: | ----------: | --------: |
| `kras_g12c_corrected`      |       1.08× |       1.05× |     1.00× |
| `bcr_abl1_corrected`       |   **1.18×** |       1.11× |     1.00× |
| `cardiac_myosin_corrected` |       1.00× |       1.00× |     1.00× |

Simulated through `allo.scoring.harness.holm`: **FWER = 0.0535** at λ = 8 Å with two true
nulls (± 0.0007). The three-null case passes at 0.0463 only because myosin is conservative.
If myosin were correctly sized, the three-null case gives 0.0543.

README §12 rebuttal 6 says calibration is "capped so it can only tighten". That is true of one
arm at α. It is **false of the composed procedure**.

**Fix, first attempt — insufficient.** A probit rescale driven by the same `alpha_star`,
`r̂ = max(Φ⁻¹(1−α*) / Φ⁻¹(1−α), 1)`. It beats the linear rescale at every measured step and
still leaves `kras_g12c_corrected` above nominal at α/3, because a one-parameter model fitted
at one threshold is not exact at another. Recorded because it was tried and reported as the
fix before it was measured.

**Fix, applied.** Calibrate the ratio at **every** Holm level, not only at α, and take the
maximum. The rescale is conservative at level `t` exactly when the ratio is at least
`z(qₜ)/z(t)`, so a maximum over all levels and all correlation lengths is conservative at all
of them by construction. `size_ratio` replaces `alpha_star` in the scoring path; `alpha_star`
stays frozen for disclosure. This needed a re-run of the calibration on all 14 arms, not
"no new simulation". The measured cost: `kras_g12c_corrected` needs 1.0421 at α and 1.0827 at
α/3. ADR 0025.

### B2 — A trivial geometric baseline passes the whole confirmatory family

Score each residue by the volume of the largest pyKVFinder cavity that lines it. The score is
label-blind, apo-only, zero-parameter, and uses the detector already frozen in
`manifest.yaml`.

| Arm                        | AUC-ROC | `p_calibrated` | Holm threshold | Reject  |
| -------------------------- | ------: | -------------: | -------------: | ------- |
| `bcr_abl1_corrected`       |   0.795 |         0.0001 |         0.0167 | **yes** |
| `cardiac_myosin_corrected` |   0.977 |         0.0001 |         0.0250 | **yes** |
| `kras_g12c_corrected`      |   0.830 |         0.0047 |         0.0500 | **yes** |

Median AUC-ROC 0.789 over 14 arms. Above 0.7 on 9 of 14. That sits inside the 0.75–0.82 band
the protocol cites for the published elastic-network literature.

README §13 validated the null with `distance_from_source_negated`, which rejects nothing, and
concluded the null was sound. That was the wrong control. `manifest.yaml`
`required_baselines` lists eight baselines and **no cavity-volume baseline**.

This is not a defect in the null. The null controls patch size, compactness and burial. It
does not control cavity volume, and it is not asked to. What the result shows is that
**clearing the confirmatory null is a low bar**. A quantum result that clears it has cleared a
bar that "biggest cavity wins" also clears.

Two independent audits reached this conclusion from different directions. The literature
review found the same gap without seeing the data: DeepAllo and PASSer2.0 both report
"rank by fpocket score alone" as the baseline to beat.

**Fix.** Add the cavity-volume baseline to `required_baselines`. Make the claim threshold
_beating the baseline_, not _rejecting the null_.

### B3 (downgraded) — A verbatim quotation drops a word

`README.md` §11 and `docs/benchmark/evidence/evaluation-metrics.md` §6.1 attribute this to Motlagh et al.,
doi:10.1038/nature13001:

> "the sign of the coupling can change, transforming an activator into a repressor, or vice versa"

The paper's sentence is:

> "...but the actual sign of the coupling can change, transforming an activator into a
> repressor, or vice versa."

Retrieved this session from PMC4224315. One word, `actual`, is missing inside quotation
marks. Everything else matches, the attribution is right, and the claim the sentence
supports is right. This is a transcription slip in a frozen document, which is worth fixing
because a frozen document's quotations have to be exact. It does not block scoring.

**Fix.** Restore `actual`, in both files.

---

## 2. Major defects

| #   | Defect                                                                                                                                                                                                                         | Evidence                                                                                                         | Fix                                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| M1  | The patch cache key omits the label set and the graph. Change `scoreable_label_residues` or the contact cutoff and `allo evaluate verify` still exits 0 against stale patches.                                                 | `nulls.py:353`. `data/patches/` is gitignored, so CI on a fresh clone is honest; a warm tree gets a false green. | Add a hash of `observed` and of the apo bytes to the key.                                                                    |
| M2  | `from allo.scoring.harness import _positives` returns the label set and passes every leakage test.                                                                                                                             | `harness.py:52`. Probed clean by three runner sources.                                                           | Add `"_positives"` to `FROZEN_TOKENS`, `test_no_leakage.py:609`.                                                             |
| M3  | The variance-factor percentile table has no committed generator. Neither do "97–99 % of the pool" or "ρ ≈ 0.6–0.8".                                                                                                            | `metrics.json` holds only `config`, `search`, `gate`, `power`, `binomial_band`. `percentile` appears zero times. | Commit the generator, or withdraw the numbers. R3 forbids a recalled number as evidence.                                     |
| M4  | `metrics.mean_rank` — the manifest's declared confirmatory statistic — has zero callers. `score_arm` inlines it.                                                                                                               | `manifest.yaml` `endpoints.confirmatory: mean_rank`.                                                             | Call it, or drop the manifest key.                                                                                           |
| M5  | `allo evaluate verify --detect` is README §13 gate item 2 and runs in no Makefile target, no `check.sh`, no CI. It runs offline in 14 s and passes.                                                                            | Zero hits for `--detect` outside its own argparse.                                                               | Add it to `make verify`.                                                                                                     |
| M6  | `detector_version: 0.9.3` is checked by nothing. `pyproject.toml` permits any 0.9.x.                                                                                                                                           | `decoys.py:58` does a bare `import pyKVFinder`.                                                                  | Assert `pyKVFinder.__version__`.                                                                                             |
| M7  | The offline verify strips the whole `decoys` block, and `score_arm` reads it raw. A hand edit to a decoy lining changes two endpoints while every committed gate reports "verified".                                           | `harness.py:355`.                                                                                                | Covered by M5.                                                                                                               |
| M8  | The protocol claims a pocket-level number in three places and computes none. `site_pocket` is frozen and never read.                                                                                                           | `decoys.py:11`, `README.md:582`, `manifest.yaml:132` `pocket_rank_permutation`.                                  | `frozen.json` already holds all three pocket classes. A pocket ranking needs no re-detection.                                |
| M9  | The decoy null was never calibrated, and it is 2.3× to 5.3× conservative from a size mismatch alone. Real size at α = 0.05 is 0.008–0.022. Decoy linings are smaller than the label set on 14/14 arms, median ratio 0.55.      | Measured independently by three audits.                                                                          | Size-standardise each lining, or drop the p-value and report the site's rank among pockets.                                  |
| M10 | Seven of 14 arms cannot reach p ≤ 0.05 on the challenge's negative class (b) at any effect size. Two of them are confirmatory. The floor is arm size, not difficulty: ρ(n_decoys, n_candidates) = +0.95.                       | `minimum_attainable_p` per arm.                                                                                  | Declare the class unscoreable on those arms rather than printing a p that cannot reject.                                     |
| M11 | `alpha_star` is 14–19 % uncertain and frozen forever. `bcr_abl1_corrected`'s 95 % CI is [0.025, 0.048].                                                                                                                        | 5th percentile of 1000 draws, then a minimum over four λ.                                                        | Re-run at n_fields ≥ 10 000. Report the interval.                                                                            |
| M12 | ADR 0023 says both error sources in `alpha_star` "push toward a smaller test". The sampling error does not. P(the frozen `alpha_star` is looser than truth) ≈ 0.27 per arm, ≈ 0.61 for at least one confirmatory arm.          | Beta(50, 951) on the quantile, ρ ≈ 0.7 across λ from common random numbers.                                      | Correct the claim.                                                                                                           |
| M13 | The minimum detectable effect is quoted at `alpha_star`, not at Holm's `alpha_star`/3. §7 states the rule that this breaks.                                                                                                    | At the real tightest step the band is **AUC 0.80–0.96**, not 0.76–0.94.                                          | Re-quote. This flips §7.2 from "overlaps only the short-correlation end" to _does not overlap published performance at all_. |
| M14 | The matched pool is not centred on the observation. Sampled patch mean Rg exceeds the observed value on **14/14 arms**, mean +3.95 % (sign test p = 1.2 × 10⁻⁴). The bias size predicts the type-I rate at ρ = +0.60 to +0.74. | The ±10 % band is symmetric; frontier growth populates it asymmetrically.                                        | λ-free and available in advance — which is what ADR 0023 says is impossible. Post-stratify acceptance across the band.       |
| M15 | c-Myc appears nowhere in the evaluation freeze. ADR 0020's Phase 2 blocker was dropped from the ROADMAP with no superseding decision.                                                                                          | `1NKP` is 1 of the 4 minimum deliverables in `CHALLENGE.md`.                                                     | Scope it out explicitly, or write the ADR that supersedes 0020.                                                              |

---

## 3. Wrong numbers in frozen files

| Location                             | Says                                          | Is                                    | Note                                                         |
| ------------------------------------ | --------------------------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| `README.md:403`                      | "the 9 arms where `alpha_star` lands below α" | **11 arms**                           | Only 3 sit at α.                                             |
| `manifest.yaml:84`                   | unmatched type-I "0.14-0.30"                  | **0.096–0.323**                       | The frozen manifest contradicts the experiment it cites.     |
| `manifest.yaml:99`                   | "0.062-0.073 on the two BCR-ABL1 arms"        | **0.059–0.075**                       | README and ADR 0023 are correct; the manifest is stale.      |
| `manifest.yaml:100`, `harness.py:85` | "0.034-0.039 on cardiac myosin"               | **0.034–0.037**                       | Same.                                                        |
| `README.md` §3.3                     | Jaccard "caps at about 0.31"                  | **0.4167** on myosin (5/12)           | 0.31 is the KRAS value. Conclusion survives.                 |
| `REGISTRY.md:130`                    | MDE band flat "to within 0.03"                | **0.0533** at λ = 20 Å                | README §7.1's "less than 0.06" is correct. Fix the registry. |
| `README.md` §7.1                     | "candidate counts span 5×"                    | 5.09× primary, **7.33×** over 14 arms | Correct as scoped. It reads as a claim about the benchmark.  |

---

## 4. Citation corrections

| Claim                                                                           | Problem                                                                                                                                                                                      | Fix                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Pržulj et al.", doi:10.1371/journal.pone.0005967                               | Authors are **Milenković, Filippis, Lappe & Pržulj**. Pržulj is last. Three sites: `README.md` §4.1, §12, `nulls.py:14`.                                                                     | Rename. The paper's own recommendation — a geometric null on the **graph** (GEO-3D) — is quoted for its warning and skipped for its prescription, with no comment.                                                                                  |
| "Utgés 2024, n = 293", the 28× burial figure                                    | No DOI, in a document that cites a **different** Utgés 2024 twice.                                                                                                                           | Cite doi:10.1038/s42003-024-05970-8. They are K-means clusters of unequal size, not quartiles.                                                                                                                                                      |
| `arXiv:2604.17486` and doi:10.1021/jacs.6c08053                                 | **The same paper**, cited four paragraphs apart as two independent precedents.                                                                                                               | Collapse to the published version. ADR 0002 already cites it correctly.                                                                                                                                                                             |
| "Spearman ρ ≈ 0.94–0.96"                                                        | The paper prints no summary statistic. Per-protein values run **0.582 to 1.000**.                                                                                                            | Quote the paper's own wording, or give the real range.                                                                                                                                                                                              |
| The noise-resilience precedent                                                  | Its k is **10**, not 5, and it compares two methods rather than a ranking under noise.                                                                                                       | State that we compute the same four statistics at k = 5.                                                                                                                                                                                            |
| Guharoy & Chakrabarti, §4.1                                                     | Their random subsets are drawn **from the interface**. The result is within-region clustering. It supports "labels are contiguous", not "any buried blob scores like a label set".           | Swap for Zheng & Tekpinar 2009, doi:10.1186/1472-6807-9-45 — ENM perturbation-response residues cluster at **3.56–3.69× random** over 502 structure pairs. The confound, quantified, in this method's own family.                                   |
| §3.3, DVO                                                                       | "no standard threshold for it exists" is **false**. `DVO > 0.2` is verbatim in doi:10.1021/acs.jcim.5c00336.                                                                                 | Delete the clause. "No volume is predicted" is decisive alone.                                                                                                                                                                                      |
| §3.3, MCC and F1                                                                | The Utgés & Barton quote is about **prediction-set size**, not thresholds. At fixed k = 5 it does not apply, because every method predicts the same number.                                  | The honest argument is "k = 5 is too small". Both are field conventions; CAPASP 2026 names them among its five evaluation dimensions.                                                                                                               |
| §3.3, Jaccard                                                                   | AlloBench also tabulates 0.1–0.4, which a 0.31 ceiling clears.                                                                                                                               | Restate.                                                                                                                                                                                                                                            |
| §12.3, "No allosteric-site paper surveyed uses a statistical null model at all" | **False.** Three do: Amor 2016, Wu 2021, ProteinLens 2021.                                                                                                                                   | The true statement is stronger: one group, one construction, one-sided on diameter, **dropped in that group's own web server**, adopted by nobody.                                                                                                  |
| §12.7, "Apo is harder"                                                          | Refutable in one citation for pocket detection in general: doi:10.1038/s41598-020-72906-7, n = 304 sequences / 2528 structures, **no significant apo/holo difference for 6 of 7 detectors**. | Narrow to allosteric and cryptic sites, where it is strongly supported: AllositePro 8/14 → 2/14.                                                                                                                                                    |
| §12.6                                                                           | Undersells.                                                                                                                                                                                  | Markello & Misic 2021 report ≈ **13 % FPR** for the best spatial nulls at high autocorrelation, after a decade of dedicated work, and state that **every** spatially constrained null they tested has inflated FPR. Ours sits at 6.6–7.7 %. Say so. |
| Allo-Allo Table 1 numbers                                                       | Could not be verified — the table is a bitmap.                                                                                                                                               | Verified replacements exist: CryptoBench ACC 0.93 with MCC 0.39; the 2025 pLM paper, accuracy 0.953 with precision 0.329.                                                                                                                           |
| APOP and SiteFerret quotes                                                      | Verbatim and correct, with no DOI anywhere.                                                                                                                                                  | doi:10.1093/bioinformatics/btad275 and doi:10.1021/acs.jctc.2c01306.                                                                                                                                                                                |
| pyKVFinder "published defaults"                                                 | The five values are the **package's** documented defaults. The cited paper states none of them.                                                                                              | Cite the package version for the numbers.                                                                                                                                                                                                           |

---

## 5. What the field measures, and what we do not

Of 22 allostery tools surveyed, **17 score at pocket level**. The modal number is a top-3
pocket success rate. Two published named criteria exist for scoring a **residue list** against
a site, and the protocol uses neither:

- **Residue-centroid DCC ≤ 4 Å** — STINGAllo, doi:10.1093/bib/bbaf424. Purpose-built for
  exactly our deliverable. Needs no volume, no detector, no threshold sweep.
- **Jaccard on residue sets** — AlloBench, doi:10.1021/acsomega.5c01263.

Missing, ranked by how loudly a reviewer asks: **recall@5** (one division from `hits_at_5`,
and the number the field reads first), residue-centroid DCC, pocket-level top-N recall, F1 and
MCC at k = 5, a bootstrap CI on the effect size, a paired method-versus-method test, and a
sequence-identity redundancy threshold.

**Four confounders are printed nowhere and cost about a dozen lines**: relative solvent
accessibility, normalised B-factor, Kyte–Doolittle hydrophobicity, and sequence conservation.
One Spearman column each. The first question asked of any propagation score is whether it is a
burial or flexibility proxy, and §10's table answers only the centrality third of it. Chea &
Livesay, doi:10.1186/1471-2105-8-153, is why this matters: a **residue-identity filter alone**
moves top-5 accuracy from 6.3 % to 16.5 %.

**The design the protocol should name and reject explicitly.** Neuroimaging solved this exact
problem by resampling the **map** rather than the **region**: variogram-matched surrogates,
Burt et al. 2020, doi:10.1016/j.neuroimage.2020.117038. They estimate the autocorrelation from
the score field the method actually produced, so they need no λ in advance — which is the
precise property §6.2 says is unobtainable. A reviewer with a neuroimaging background will ask.

**The abandoned repair was rejected on the wrong test.** §6.2 dismisses distance-distribution
matching because the _mean_ pairwise distance is already satisfied by 97–99 % of the pool. The
mean is the first moment and Rg is the second. The variance factor is a functional of the
**whole** ECDF. A Kolmogorov–Smirnov or Wasserstein tolerance on it matches the variance factor
for **all λ at once**. That experiment was not run.

---

## 6. Deletions

**Applied: 2 075 lines. Proposed and declined: 2 033.** The first draft of this section
proposed about 4 500 lines. Re-reviewing each target against what it actually costs to remove
cut that in half, and the reasons are recorded here rather than left as a silent shortfall.

### Applied

| Target                                      |    Lines | Why it went                                                                                                                                                            |
| ------------------------------------------- | -------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frozen.json` -> `decoys.residues`          | **2064** | Derivable from the decoy linings on 14/14 arms, checked. 30 % of the file, carrying nothing the linings do not. `harness.py` now derives it inline.                     |
| `metrics.mean_rank`                         |       10 | The manifest's declared confirmatory statistic, with zero callers. `score_arm` inlines it.                                                                              |
| `decoys.classify` -> `decoy_residues`       |        1 | The field that produced the 2 064 lines above.                                                                                                                          |
| `manifest.yaml` `halo_sensitivity_angstrom` |        1 | Zero references repo-wide. A pre-registered sensitivity that nothing runs is not pre-registered.                                                                        |

### Proposed, then declined

| Target                                              | Lines | Why it stayed                                                                                                                                                                                                                                    |
| --------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/benchmark/evidence/evaluation-metrics.md` section 8 and 9    |  ~800 | Section 8 is every place two sources disagree, unresolved. Section 9 is every number the review wanted and could not get. R3 asks for exactly this and says to write "unknown" where evidence is absent. Deleting them would remove the honesty, not the bloat. |
| `docs/benchmark/evidence/evaluation-metrics.md` section 0          |  ~146 | The evidence rules and verification tags. A literature review that claims rigour has to state how it verified.                                                                                                                                    |
| `docs/benchmark/evidence/evaluation-protocol-lit.md`               |   503 | Superseded, and 17 of its 18 DOIs are duplicated. But the file that supersedes it cites it 18 times to record **what changed between the two reviews**, and section 9.1 is a resolution table keyed to its section 5. Removing 503 lines at the cost of rewriting 18 live cross-references in the file we keep is not a simplification. `docs/benchmark/evidence/README.md` already labels it as superseded provenance. |
| `score_arm(against=...)`                            |    15 | Zero callers **today**. It implements the rank correlation against every baseline, which README section 8 requires and Phase 3 will call. Not dead, unbuilt.                                                                                       |
| `nulls.smooth_field`                                |    10 | Not dead — it was duplicated. Now called from both sites in `calibration.py` that had inlined it.                                                                                                                                                 |

`matched_patch_distance` is a judgement call, not a clear deletion. It is a fourth null
answering a question the challenge does not ask, it can never decide anything, and it costs
more sampler attempts than the confirmatory null. Its question is already answered by two
required baselines and a Spearman correlation. Kept as a pre-registered secondary for the
report's rebuttal section.

---

## 7. What the audit confirms is correct

- The C1 import trace is clean. No prediction-path module reaches `allo.scoring` or
  `allo.groundtruth` by any chain.
- `docs/benchmark/evaluation/` is protected by three independent guards, at directory level,
  so a file added later is protected by default.
- `make check` passed at audit time: 102 tests, 0 failures, 11.9 s. At protocol version 2 it
  passes 115, the added ones covering the every-level calibration, the rescale clamp, the
  cavity-volume baseline, the pocket rank, DCC and the Shrake-Rupley cross-check.
  `allo evaluate verify` passes offline.
  `allo evaluate verify --detect` passes in 14 s.
- Every cell of the §6.1 type-I table, every `alpha_star`, the §5.3 decoy table, the §7.1 MDE
  table and the §13 baseline numbers reproduce exactly from committed files.
- The mean-midrank ↔ AUC-ROC equivalence is algebraically exact for the three patch nulls.
- The background permutation is a correct draw without replacement.
- The float32 matmul is safe, because every matched patch has exactly the same size. That
  invariant is load-bearing and has no assert behind it.
- The `holm` step-down, the plus-one correction, the pessimistic tie-break and the `auc_pr`
  step estimator are all correct.
- The halo was frozen at 0 Å in the direction that **hurts** the project's own numbers.
- Version discipline is genuinely above the field. No allosteric-site paper surveyed states its
  detector version.
- The residual over-rejection reads in §6.1 as a failure. Against the only field that has
  measured this, it is at or above the state of the art.

---

## 8. Two claims the report must make before its numbers

Both were already required. Both are now stronger.

1. **A cavity-volume baseline passes the confirmatory family.** Until the report states this,
   "we rejected the matched-patch null on all three confirmatory arms" is not evidence of
   allosteric signal.
2. **Competent apo residue-level AUC-ROC in this field is 0.72–0.87.** At Holm's real threshold
   this benchmark needs 0.80–0.96. The published band does not overlap the detectable band.
   An ordinary publishable result in this sub-field fails here.
