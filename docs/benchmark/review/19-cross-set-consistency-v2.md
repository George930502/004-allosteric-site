# Cross-set consistency, version 2: fifteen arms, twelve clauses

**Supersedes [`10-cross-set-consistency.md`](10-cross-set-consistency.md).** That pass was
written against a five-arm primary set on 2026-09-02 morning. The input layer was re-frozen the
same day: `bcr_abl1_mandated` moved to `1OPL` chain **B** (ADR 0029) and
`cardiac_myosin_mandated` was created, `5TBY`:A → `9GZ2`:A (ADR 0031). The primary set now has
**six** arms and the secondary set still has nine, so every count, every ratio and one clause
verdict in document 10 is stale. Nothing there was wrong when it was written; it is wrong now.

**Question.** Are the two frozen input sets built and scored by the same rules — vertically,
so every arm inside a set is treated alike, and horizontally, so a number from one set is
comparable with a number from the other?

**Answer.** The _machinery_ is genuinely shared and is the strongest part of the benchmark: one
`derive`, one 4.5 Å cutoff, one evaluation protocol over all fifteen arms. The _rules_ are not.
**Nine divergences.** One is fully disclosed (6.10), two are partly disclosed (6.4, 6.7), one is
disclosed but its numbers are stale (6.9), and **five are recorded nowhere** (6.2, 6.3, 6.5, 6.6,
6.8). One of the five — an arm that is scored but has no declared reporting role — is a
pre-registration hole and should be closed before any method runs.

Everything below is re-derived from the frozen artifacts and the tracked mmCIFs. The script is
reproduced verbatim in Appendix A; it was run from the scratchpad and is deliberately not
tracked, because a tracked file naming `frozen.json` fails `tests/test_no_leakage.py`.

---

## 1. What is genuinely identical

|                             | primary (6 arms)                          | secondary (9 arms)              |
| --------------------------- | ----------------------------------------- | ------------------------------- |
| contact cutoff              | 4.5 Å                                     | 4.5 Å                           |
| cutoff sensitivity recorded | 4.0, 5.0                                  | 4.0, 5.0                        |
| atom selection              | heavy                                     | heavy                           |
| model                       | 1                                         | 1                               |
| derivation code             | `allo.benchmark.derive`                   | the same function               |
| label transfer              | `allo.groundtruth.labels`                 | the same module                 |
| evaluation layer            | protocol **version 3**, frozen 2026-09-02 | the same protocol, same 15 arms |
| scoring entry point         | `allo.scoring.score_arm`                  | the same function               |
| decoy detector              | pyKVFinder 0.9.3, one settings block      | the same                        |
| null                        | matched-patch, per-arm `size_ratio`       | the same                        |

One `derive`, one cutoff, one protocol, one detector over all fifteen arms. This is what makes
a cross-set comparison possible at all, and it holds at the new shape. Six primary arms and
nine secondary arms give **224 positives over 6883 candidates** and **777 decoy pockets**.

---

## 2. Vertical axis — the primary set, six arms

`n_residues` is what a method **receives**; `n_candidates` is what it is **scored against**
(ADR 0011). `delta` is the gap, and it is the active site removed by clause (vii) plus nothing
else on any current arm.

| arm                        | tier      | nodes | candidates | delta | positives | prevalence | source rule                                        | \|source\| | decoys | site cov | identity | aligned | unmapped |
| -------------------------- | --------- | ----: | ---------: | ----: | --------: | ---------: | -------------------------------------------------- | ---------: | -----: | -------: | -------: | ------: | -------: |
| `kras_g12c_mandated`       | mandated  |   169 |        146 |    23 |        16 |     11.0 % | `from_ligands: GDP, MG`                            |         23 |     13 |   0.8125 |   0.9759 |     166 |        0 |
| `kras_g12c_corrected`      | corrected |   170 |        148 |    22 |        16 |     10.8 % | `from_ligands: GDP, MG`                            |         22 |     18 |   0.9375 |   0.9820 |     167 |        0 |
| `bcr_abl1_mandated`        | mandated  |   365 |        354 |    11 |        17 |      4.8 % | `from_motifs: VAIK, HRD, DFG`                      |         11 |     45 |   1.0000 |   0.9971 |     345 |    **3** |
| `bcr_abl1_corrected`       | corrected |   272 |        261 |    11 |        18 |      6.9 % | `from_motifs: VAIK, HRD, DFG`                      |         11 |     31 |   0.9444 |   0.9921 |     252 |    **2** |
| `cardiac_myosin_mandated`  | mandated  |   954 |        932 |    22 |        12 |      1.3 % | `from_motifs: MYO_PLOOP, MYO_SWITCH1, MYO_SWITCH2` |         22 |    139 |   0.9167 |   1.0000 |     761 |        0 |
| `cardiac_myosin_corrected` | corrected |   764 |        743 |    21 |        12 |      1.6 % | `from_ligands: ADP, MG, PO4`                       |         21 |     84 |   1.0000 |   1.0000 |     764 |        0 |

Supplementary, same six arms:

| arm                        | align coverage | holo footprint → labels kept | source→label distance min/med/max Å | labels at 4.0/4.5/5.0 Å | transplant clashes | superpos RMSD | lining RMSD |
| -------------------------- | -------------: | ---------------------------: | ----------------------------------: | ----------------------: | -----------------: | ------------: | ----------: |
| `kras_g12c_mandated`       |          0.982 |                      21 → 21 |                    0.0 / 9.5 / 18.3 |            17 / 21 / 22 |              14/41 |          0.68 |        2.61 |
| `kras_g12c_corrected`      |          0.982 |                      21 → 21 |                    0.0 / 9.2 / 18.2 |            17 / 21 / 22 |              18/41 |          0.58 |        2.62 |
| `bcr_abl1_mandated`        |          0.945 |                  20 → **17** |                  10.6 / 17.3 / 23.9 |            15 / 17 / 20 |               0/31 |          0.66 |   **26.31** |
| `bcr_abl1_corrected`       |          0.926 |                  20 → **18** |                  10.8 / 17.5 / 30.1 |            16 / 18 / 21 |               2/31 |          1.12 |        2.38 |
| `cardiac_myosin_mandated`  |      **0.798** |                      12 → 12 |                  16.8 / 27.9 / 41.1 |            10 / 12 / 14 |               8/20 |          1.96 |        2.94 |
| `cardiac_myosin_corrected` |          1.000 |                      12 → 12 |                  16.5 / 27.6 / 35.6 |            10 / 12 / 14 |               0/20 |          0.86 |        1.10 |

**Six things this table says that no repository document says.**

1. **Node count is not comparable within a target.** `bcr_abl1_mandated` receives 365 nodes and
   `bcr_abl1_corrected` 272 — the mandated arm carries the SH3-SH2 cap that `2G2H` truncates.
   `cardiac_myosin_mandated` receives 954 and its corrected sibling 764. A mandated-vs-corrected
   comparison inside one disease area is not a like-for-like comparison of the same graph.
2. **Positive count is not comparable within a target either.** Both ABL1 arms transfer labels
   from the same holo pocket, `5MO4`:A + `AY7`, 20 lining residues at 4.5 Å. The mandated arm
   keeps **17**, the corrected keeps **18**. The lost residues are C-terminal and are declared:
   `A:ILE521, A:VAL525, A:LEU529` for `1OPL`:B and `A:VAL525, A:LEU529` for `2G2H`. Section 6.2
   is where this becomes a cross-set inconsistency.
3. **Prevalence inside one target moves by 44 %.** `bcr_abl1_mandated` 4.8 % against
   `bcr_abl1_corrected` 6.9 %, from 17/354 against 18/261. Both the numerator and the
   denominator moved.
4. **The two myosin arms locate the active site by two different rules.** Mandated uses motifs,
   corrected uses ligands. It is the only such split in the benchmark, and section 6.3 prices it.
5. **The propagation source varies in size by 20×** across the fifteen arms, from 3 residues
   (`ns5b`, the `GDD` motif) to 61 (`ecoli_cps`). Inside the primary set it runs 11 to 23. The
   source is the boundary condition of every propagation method, and its size is a per-arm
   parameter nobody chose deliberately.
6. **`cardiac_myosin_mandated` aligns only 79.8 % of its own nodes to the holo.** Identity is
   1.0000 over the 761 residues that align, which is what a homology model of the correct
   sequence should give; the coverage number is the honest one. Its pocket-lining RMSD, 2.94 Å,
   is measured over those aligned residues only.

`bcr_abl1_mandated`'s pocket-lining RMSD is **26.31 Å** against a whole-chain superposition RMSD
of 0.66 Å and a core RMSD of 22.79 Å over 328 residues. The myristoyl pocket lining in the
extended `1OPL`:B conformation is 26 Å from where `5MO4` puts it. Its transplant clash count is
**0/31** — the pocket is wide open and in the wrong place. That combination is unique in the set
and is the measured form of ADR 0029's "domain placement" warning.

---

## 3. Vertical axis — the secondary set, nine arms

| arm           | tier           | nodes | candidates | delta | positives | prevalence | source rule                   | \|source\| | decoys |   site cov | identity | aligned | unmapped |
| ------------- | -------------- | ----: | ---------: | ----: | --------: | ---------: | ----------------------------- | ---------: | -----: | ---------: | -------: | ------: | -------: |
| `mkp5`        | development    |   147 |        136 |    11 |        11 |      8.1 % | `from_motifs: PTP`            |         11 |     14 | **0.4545** |   1.0000 |     147 |        0 |
| `chk1`        | generalisation |   272 |        261 |    11 |        12 |      4.6 % | `from_motifs: VAIK, HRD, DFG` |         11 |     39 |     0.9167 |   1.0000 |     258 |        0 |
| `ptp1b`       | development    |   298 |        287 |    11 |        11 |      3.8 % | `from_motifs: PTP`            |         11 |     33 | **0.3636** |   1.0000 |     291 |        0 |
| `smyd3`       | generalisation |   425 |        408 |    17 |        12 |      2.9 % | `from_ligands: SAM`           |         17 |     32 |     1.0000 |   0.9976 |     425 |        0 |
| `glucokinase` | generalisation |   453 |        438 |    15 |        19 |      4.3 % | `from_ligands: GLC`           |         15 |     49 |     1.0000 |   1.0000 |     449 |        0 |
| `hiv_rt`      | development    |   543 |        534 |     9 |        16 |      3.0 % | `from_motifs: POLA, YXDD`     |          9 |     68 | **0.6250** |   1.0000 |     525 |        0 |
| `ns5b`        | development    |   553 |        550 |     3 |        16 |      2.9 % | `from_motifs: GDD`            |          3 |     50 | **0.3125** |   1.0000 |     512 |        0 |
| `p97_vcp`     | generalisation |   723 |        688 |    35 |        17 |      2.5 % | `from_ligands: ADP`           |         35 |     67 |     0.7059 |   1.0000 |     723 |        0 |
| `ecoli_cps`   | generalisation |  1058 |        997 |    61 |        19 |      1.9 % | `from_ligands: ADP, MN, PO4`  |         61 |     95 |     0.9474 |   0.9981 |    1058 |        0 |

Supplementary:

| arm           | align coverage | holo footprint → labels kept | source→label distance min/med/max Å | labels at 4.0/4.5/5.0 Å | transplant clashes | superpos RMSD | lining RMSD |
| ------------- | -------------: | ---------------------------: | ----------------------------------: | ----------------------: | -----------------: | ------------: | ----------: |
| `mkp5`        |          1.000 |                      12 → 12 |                    0.0 / 6.1 / 12.5 |            11 / 12 / 14 |              12/22 |          0.52 |        1.48 |
| `chk1`        |          0.949 |                      12 → 12 |                   7.1 / 15.3 / 19.0 |            11 / 12 / 12 |               3/23 |          0.14 |        0.29 |
| `ptp1b`       |          0.977 |                      11 → 11 |                  13.5 / 16.7 / 21.5 |            10 / 11 / 13 |              21/28 |          2.88 |        2.94 |
| `smyd3`       |          1.000 |                      12 → 12 |                  18.2 / 25.4 / 34.5 |            10 / 12 / 12 |               0/29 |          0.15 |        0.31 |
| `glucokinase` |          0.991 |                      19 → 19 |                   6.3 / 12.8 / 18.6 |            15 / 19 / 19 |               0/23 |          0.29 |        0.98 |
| `hiv_rt`      |          0.967 |                      16 → 16 |                   4.4 / 10.4 / 16.5 |            13 / 16 / 18 |              13/20 |          1.28 |        2.34 |
| `ns5b`        |          0.926 |                      16 → 16 |                  22.3 / 28.5 / 36.8 |            15 / 16 / 16 |              32/33 |          0.71 |        1.17 |
| `p97_vcp`     |          1.000 |                      17 → 17 |                  14.1 / 16.5 / 23.1 |            17 / 17 / 18 |               8/34 |          0.38 |        0.79 |
| `ecoli_cps`   |          1.000 |                      19 → 19 |                  12.5 / 18.9 / 28.7 |            17 / 19 / 22 |               3/21 |          0.16 |        0.24 |

**The secondary set is internally tidier than the primary set on every column that can be
tidy.** Nine of nine transfer their whole holo footprint. Identity is 0.9976–1.0000 against the
primary's 0.9759–1.0000. Alignment coverage is 0.926–1.000 against the primary's 0.798–1.000.
Superposition RMSD is 0.14–2.88 Å against 0.58–1.96 Å — comparable — but pocket-lining RMSD is
0.24–2.94 Å against 1.10–26.31 Å. That is a selected set behaving like a selected set, and it is
the reason `secondary/README.md` §5.2 exists. §5.2 now understates it; see 6.9.

---

## 4. Prevalence spread, re-derived

| scope       |   n | low                                | high                           |     ratio | median |
| ----------- | --: | ---------------------------------- | ------------------------------ | --------: | -----: |
| primary     |   6 | 1.29 % (`cardiac_myosin_mandated`) | 10.96 % (`kras_g12c_mandated`) | **8.51×** |  5.8 % |
| secondary   |   9 | 1.91 % (`ecoli_cps`)               | 8.09 % (`mkp5`)                |     4.24× |  3.0 % |
| all fifteen |  15 | 1.29 %                             | 10.96 %                        | **8.51×** |  3.8 % |

**"1.3 % to 11.0 %" still holds, and it is now a property of the primary set alone.** Both
extremes are primary arms, and both are `mandated`. The secondary set sits entirely inside the
primary range. Nothing about the spread was repaired by the re-freeze; it widened, because
`cardiac_myosin_mandated` at 12 positives in 932 candidates is the sparsest arm in the
benchmark.

**What it costs.** Precision@5, AUC-PR and "at least one hit at 5" all have a prevalence-linked
chance line, and the ratio of chance lines between the extreme arms is 8.51. The evaluation
freeze does carry a per-arm `chance` block, so the cost is bounded to _interpretation_ rather
than _validity_: any arm-to-arm quotation of AUC-PR without its chance line is meaningless, and
a mean over arms is dominated by the two KRAS arms. `evaluation/README.md` §3.2 already says
this. Two statements there are stale at the new shape and are listed in 6.9.

---

## 5. Decoy site coverage, re-derived

`label_coverage` is the fraction of the arm's positives that fall inside the pocket the detector
found at the true site. It is the answer to "would a static pocket detector even see this site".

| arm                        | set       | tier           |   coverage | labels covered | decoys | min attainable p |
| -------------------------- | --------- | -------------- | ---------: | -------------: | -----: | ---------------: |
| `ns5b`                     | secondary | development    | **0.3125** |           5/16 |     50 |         0.019608 |
| `ptp1b`                    | secondary | development    | **0.3636** |           4/11 |     33 |         0.029412 |
| `mkp5`                     | secondary | development    | **0.4545** |           5/11 |     14 |     **0.066667** |
| `hiv_rt`                   | secondary | development    | **0.6250** |          10/16 |     68 |         0.014493 |
| `p97_vcp`                  | secondary | generalisation |     0.7059 |          12/17 |     67 |         0.014706 |
| `kras_g12c_mandated`       | primary   | mandated       |     0.8125 |          13/16 |     13 |     **0.071429** |
| `cardiac_myosin_mandated`  | primary   | mandated       |     0.9167 |          11/12 |    139 |         0.007143 |
| `chk1`                     | secondary | generalisation |     0.9167 |          11/12 |     39 |         0.025000 |
| `kras_g12c_corrected`      | primary   | corrected      |     0.9375 |          15/16 |     18 |     **0.052632** |
| `bcr_abl1_corrected`       | primary   | corrected      |     0.9444 |          17/18 |     31 |         0.031250 |
| `ecoli_cps`                | secondary | generalisation |     0.9474 |          18/19 |     95 |         0.010417 |
| `bcr_abl1_mandated`        | primary   | mandated       |     1.0000 |          17/17 |     45 |         0.021739 |
| `cardiac_myosin_corrected` | primary   | corrected      |     1.0000 |          12/12 |     84 |         0.011765 |
| `smyd3`                    | secondary | generalisation |     1.0000 |          12/12 |     32 |         0.030303 |
| `glucokinase`              | secondary | generalisation |     1.0000 |          19/19 |     49 |         0.020000 |

**The four poorly-covered arms the repository names — `ns5b` 0.31, `ptp1b` 0.36, `mkp5` 0.45,
`hiv_rt` 0.63 — are confirmed unchanged at the new shape.** A fifth, `p97_vcp` at 0.71, sits
below three-quarters and is not named anywhere.

**And the defect is one-sided: all five are secondary arms.** The six primary arms run
0.8125 to 1.0000. That is not a rule applied differently; it is a rule applied identically
producing a systematically different result on the two sets, which for a cross-set comparison is
the same problem. `auc_roc_vs_decoy_linings` is a _reported_ endpoint on all fifteen arms
(`evaluation/manifest.yaml` `endpoints.reported`). On the five low-coverage arms it asks a
method to out-rank decoy linings when the detector's own "site" pocket holds under three-quarters
of the answer key, so the comparison is between a partial site and a set of complete decoys.
Four of the five sit in `development`, where the number only tunes; one, `p97_vcp`, sits in
`generalisation`, which carries the across-target claim.

**The size mismatch behind the decoy null, re-derived.** A decoy lining is smaller than the label
set on **15 of 15 arms**, median ratio **0.412** — matching `evaluation/README.md` §5.3 exactly.
Per set: primary median 0.373, secondary median 0.412. The mismatch is uniform across the sets,
so it biases both toward not rejecting by the same amount, and the disclosure in §5.3 covers it.

---

## 6. Horizontal axis — twelve clauses over fifteen arms

Clauses (i)–(viii) are the pair definition in `primary/README.md` §1 and bind both sets.
Clauses (ix)–(xii) are the selection rules in `secondary/README.md` §4 and bind the secondary
set only. Applying all twelve to all fifteen arms is the horizontal-consistency test.

| arm                        | set       | (i)  | (ii) | (iii)    | (iv) | (v)      | (vi) | (vii) | (viii) | (ix)  | (x)  | (xi)     | (xii) |
| -------------------------- | --------- | ---- | ---- | -------- | ---- | -------- | ---- | ----- | ------ | ----- | ---- | -------- | ----- |
| `kras_g12c_mandated`       | primary   | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `kras_g12c_corrected`      | primary   | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `bcr_abl1_mandated`        | primary   | pass | pass | **pass** | pass | pass     | pass | pass  | pass   | pass  | pass | **FAIL** | pass  |
| `bcr_abl1_corrected`       | primary   | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `cardiac_myosin_mandated`  | primary   | pass | pass | pass     | pass | **FAIL** | pass | pass  | pass*  | pass† | pass | **FAIL** | pass  |
| `cardiac_myosin_corrected` | primary   | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `mkp5`                     | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `chk1`                     | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `ptp1b`                    | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `smyd3`                    | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `glucokinase`              | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `hiv_rt`                   | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `ns5b`                     | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `p97_vcp`                  | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |
| `ecoli_cps`                | secondary | pass | pass | pass     | pass | pass     | pass | pass  | pass   | pass  | pass | pass     | pass  |

\* clause (viii) passes on `cardiac_myosin_mandated` only in the sense the clause is written —
the state is **stated**, and what is stated is `apo: "unknown (homology model)"`. Read as a
disclosure rule that is a pass. Read as a knowledge claim it is a declared unknown.
† clause (ix) is inherited: `cardiac_myosin_mandated` shares its holo, `9GZ2`:A, with
`cardiac_myosin_corrected`, whose assembly measurement is in
`review/data/clause-ix-both-sets.json`. That file was built before the arm existed and covers
fourteen arms; the fifteenth's verdict is entailed by the shared holo, not measured separately.

### 6.0 The measurement behind every non-trivial cell

| clause | decided by                                                                                                  | note                                                                                                               |
| ------ | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| (i)    | `manifest.holo.ligand` present, `frozen.holo_label_footprint` non-empty at 4.5 Å                            | footprints 11–21 residues; all fifteen have one                                                                    |
| (ii)   | `manifest.allosteric_evidence.doi` present                                                                  | fifteen distinct DOIs. Presence is all that is machine-checkable; the reading is `14-clause-ii-literature-pass.md` |
| (iii)  | `frozen.apo_site_occupancy.scoreable_labels_contacted == 0`                                                 | zero on all fifteen                                                                                                |
| (iv)   | `frozen.sequence_agreement.identity ≥ 0.90`                                                                 | 0.9759–1.0000. The floor never binds                                                                               |
| (v)    | `assembly_agreement.selected_target_copies_match and .polymer_composition_matches`                          | one FAIL                                                                                                           |
| (vi)   | `frozen.orthosteric_state` has both members and the manifest states a source rule                           | fifteen of fifteen                                                                                                 |
| (vii)  | `set(active_site) ∩ set(scoreable_label_residues) == ∅`                                                     | residual overlap 0 on all fifteen                                                                                  |
| (viii) | `manifest.state.apo` and `.holo` non-empty, `apo_holo_rmsd.pocket_lining` recorded                          | fifteen of fifteen                                                                                                 |
| (ix)   | lining chains at 4.5 Å on the downloaded biological assembly                                                | one chain on all fifteen                                                                                           |
| (x)    | `scoreable_labels_contacted == 0`, with the apo component list printed                                      | zero on all fifteen                                                                                                |
| (xi)   | `experimental_method` and `resolution_combined_angstrom` from the tracked mmCIF, X-ray ≤ 2.5 Å / EM ≤ 4.0 Å | two entries FAIL                                                                                                   |
| (xii)  | Pfam disjointness against every arm of a **different** target                                               | no cross-target collision                                                                                          |

**Clause (iii) no longer fails anywhere.** Document 10 recorded `bcr_abl1_mandated` as the single
in-set failure — "20 of 20 labels contacted, nearest 3.29 Å" — because `1OPL`:A carries myristate
in the myristoyl pocket. Chain B does not: `MYR` appears in `entry_components` and not in
`chain_components`, and the nearest apo component to any label is `P16` at **16.0 Å**. The
organisers' chain choice repaired the most serious defect in the mandated set as a side effect.
Say so; it is a rare piece of good news.

**Clause (v) now fails once, and it is a new failure.** `cardiac_myosin_mandated`: `5TBY`
deposits the hexameric interacting-heads motif (two MYH7 heavy chains, two essential and two
regulatory light chains) and `9GZ2` is monomeric, so 6 against 1. It is declared in
`manifest.assembly_exception` and pinned by `tests/test_benchmark.py`. See 6.6 for why the
declaration route exists on one set and not the other.

**Clause (xii) at the target level passes; at the arm level it "fails by design".** Each disease
area contributes a mandated and a corrected arm on the same protein, the same site and the same
Pfam. `primary/README.md` §1 already records that as intentional. The script therefore excludes
same-target pairs and asks the question the clause was written to ask: does any arm share a
Pfam family with an arm of a _different_ target? No. See 6.4 for what that guarantee is worth.

### 6.1 Clause (xi) verified, and extended to six arms

`11-synthesis.md` item 3.6 first claimed (xi) "fails on `1OPL` alone", then corrected itself to
two entries, `1OPL` at 3.42 Å and `5TBY` at 20.00 Å. **The correction is right and the original
was wrong.** Re-derived over all 27 distinct entries in both sets:

| entry  | method |  resolution | ceiling | verdict                      | used by                        |
| ------ | ------ | ----------: | ------: | ---------------------------- | ------------------------------ |
| `1OPL` | X-ray  |  **3.42 Å** |     2.5 | **FAIL**                     | `bcr_abl1_mandated`:apo        |
| `5TBY` | EM     | **20.00 Å** |     4.0 | **FAIL**                     | `cardiac_myosin_mandated`:apo  |
| `4LDJ` | X-ray  |        1.15 |     2.5 | pass                         | `kras_g12c_corrected`:apo      |
| `6P7Z` | X-ray  |        1.19 |     2.5 | pass                         | `smyd3`:apo                    |
| `4OBE` | X-ray  |        1.24 |     2.5 | pass                         | `kras_g12c_mandated`:apo       |
| `3F9M` | X-ray  |        1.50 |     2.5 | pass                         | `glucokinase`:holo             |
| `1ZZW` | X-ray  |        1.60 |     2.5 | pass                         | `mkp5`:apo                     |
| `7BJ1` | X-ray  |        1.61 |     2.5 | pass                         | `smyd3`:holo                   |
| `6OIM` | X-ray  |        1.65 |     2.5 | pass                         | both KRAS arms:holo            |
| `1IA8` | X-ray  |        1.70 |     2.5 | pass                         | `chk1`:apo                     |
| `3JVR` | X-ray  |        1.76 |     2.5 | pass                         | `chk1`:holo                    |
| `1A9X` | X-ray  |        1.80 |     2.5 | pass                         | `ecoli_cps`:apo                |
| `7UMV` | X-ray  |        1.80 |     2.5 | pass                         | `mkp5`:holo                    |
| `1SUG` | X-ray  |        1.95 |     2.5 | pass                         | `ptp1b`:apo                    |
| `2G2H` | X-ray  |        2.00 |     2.5 | pass                         | `bcr_abl1_corrected`:apo       |
| `1T36` | X-ray  |        2.10 |     2.5 | pass                         | `ecoli_cps`:holo               |
| `3IDH` | X-ray  |        2.14 |     2.5 | pass                         | `glucokinase`:apo              |
| `5MO4` | X-ray  |        2.17 |     2.5 | pass                         | both ABL1 arms:holo            |
| `1T48` | X-ray  |        2.20 |     2.5 | pass                         | `ptp1b`:holo                   |
| `1VRT` | X-ray  |        2.20 |     2.5 | pass                         | `hiv_rt`:holo                  |
| `5FTJ` | EM     |        2.30 |     4.0 | pass                         | `p97_vcp`:holo                 |
| `2BRK` | X-ray  |        2.30 |     2.5 | pass                         | `ns5b`:holo                    |
| `1RTJ` | X-ray  |        2.35 |     2.5 | pass                         | `hiv_rt`:apo                   |
| `5FTK` | EM     |        2.40 |     4.0 | pass                         | `p97_vcp`:apo                  |
| `1QUV` | X-ray  |    **2.50** |     2.5 | pass, exactly at the ceiling | `ns5b`:apo                     |
| `9GZ2` | EM     |        2.90 |     4.0 | pass                         | both myosin arms:holo          |
| `9GZ3` | EM     |        3.40 |     4.0 | pass                         | `cardiac_myosin_corrected`:apo |

Two failures, both apo, both primary, both `mandated`. All eighteen secondary entries pass and
all three corrected primary arms pass. So `secondary/README.md` §5.2 Axis B — "`1OPL` is the only
structure in either set that fails" — was true on 2026-08-24 and is false now.

**A caveat the ceiling hides.** `5TBY` is admitted to the cryo-EM branch of clause (xi) because
its `_exptl.method` is `ELECTRON MICROSCOPY` and RCSB reports
`structure_determination_methodology = experimental`. Its own title says otherwise: "…OBTAINED BY
HOMOLOGY MODELING (USING SWISS-MODEL) OF HUMAN SEQUENCE FROM APHONOPELMA HOMOLOGY MODEL
(PDB-3JBH), RIGIDLY FITTED TO HUMAN BETA-CARDIAC NEGATIVELY STAINED THICK FILAMENT 3D
RECONSTRUCTION (EMD-2240)". 20.00 Å is the resolution of the _map it was fitted into_, not of a
reconstruction of this molecule. The arm fails (xi) by a factor of five either way, so nothing
turns on it here — but a clause that reads a metadata field would admit a 3.9 Å rigid-fitted
homology model without comment, and it should be read as a floor, not a guarantee.

### 6.2 Divergence 1 — complete label transfer is required of one set only

**Recorded nowhere. The highest-cost finding after 6.5.**

`tests/test_secondary.py::test_every_transferred_label_survives_into_the_node_set` asserts, for
every secondary arm:

```
assert not values["unmapped"]
assert not values["labels_outside_node_set"]
assert len(values["label_residues"]) == len(footprint)
```

There is no primary equivalent. `tests/test_benchmark.py::test_every_arm_accounts_for_the_labels_
it_does_not_score` requires the loss to be **declared** in `unmapped` and to **reconcile** across
arms sharing a pocket — a bookkeeping rule, not a prohibition. Measured over both sets:

| arm                        | holo footprint | labels kept | unmapped | would the secondary test pass? |
| -------------------------- | -------------: | ----------: | -------: | ------------------------------ |
| `bcr_abl1_mandated`        |             20 |          17 |        3 | **no**                         |
| `bcr_abl1_corrected`       |             20 |          18 |        2 | **no**                         |
| every other arm, both sets |              — | = footprint |        0 | yes                            |

**Cost.** Two arms are scored against a truncated answer key: `bcr_abl1_mandated` misses 15 % of
the asciminib pocket and `bcr_abl1_corrected` 10 %. One of them, `bcr_abl1_corrected`, is in the
**confirmatory family** and in the **claim family**. Recall@5, AUC-PR and DCC on those arms are
computed against a smaller pocket than exists, and a method that ranks Ile521 first is penalised
for being right. The reconciliation test guarantees the loss is _visible_; it does not make the
number comparable to a secondary arm's. If the rule is right for nine arms it needs a reason not
to bind six, and no document gives one.

### 6.3 Divergence 2 — two arms of one target use two different source rules

**Recorded nowhere.**

| arm                        | source rule                                          | \|active site\| |
| -------------------------- | ---------------------------------------------------- | --------------: |
| `cardiac_myosin_mandated`  | `from_motifs: [MYO_PLOOP, MYO_SWITCH1, MYO_SWITCH2]` |              22 |
| `cardiac_myosin_corrected` | `from_ligands: [ADP, MG, PO4]`                       |              21 |

Every other target uses one rule across all its arms. The cause is forced — `5TBY` has **zero
heteroatoms**, so no ligand rule can run on it — but the consequence is not disclosed: the two
myosin arms have different sources, therefore different clause-(vii) exclusion sets, therefore
different candidate sets, and any mandated-vs-corrected myosin comparison confounds the input
defect with the source definition.

**And it makes a pre-registered experiment free.** ADR 0033 settled the organisers' "uniformly
stripped" sentence on the narrow reading and pre-registered a _descriptive_ motif-vs-ligand
source comparison on KRAS over a 15-residue intersection, because residue 10 is a scoreable KRAS
label and a motif source would move it out of the positive class. Myosin already runs both rules
on one target with **identical label sets** (12 labels, same residues, both arms) and **zero**
clause-(vii) loss on either. It is the cleaner instrument for exactly that question, and it is not
named in ADR 0033 or anywhere else.

**The 7/7 ligand-motif split in document 10 §4 is now 7 ligand / 8 motif**, and the myosin row
moved sides: the target that was ligand-derived now contributes one arm to each column.

| `from_ligands` — 7 arms                   | `from_motifs` — 8 arms                                          |
| ----------------------------------------- | --------------------------------------------------------------- |
| `kras_g12c_mandated` (GDP, MG)            | `bcr_abl1_mandated` (VAIK, HRD, DFG)                            |
| `kras_g12c_corrected` (GDP, MG)           | `bcr_abl1_corrected` (VAIK, HRD, DFG)                           |
| `cardiac_myosin_corrected` (ADP, MG, PO4) | `cardiac_myosin_mandated` (MYO_PLOOP, MYO_SWITCH1, MYO_SWITCH2) |
| `smyd3` (SAM)                             | `mkp5` (PTP)                                                    |
| `glucokinase` (GLC)                       | `chk1` (VAIK, HRD, DFG)                                         |
| `p97_vcp` (ADP)                           | `ptp1b` (PTP)                                                   |
| `ecoli_cps` (ADP, MN, PO4)                | `hiv_rt` (POLA, YXDD)                                           |
|                                           | `ns5b` (GDD)                                                    |

Per set: primary 3 ligand / 3 motif; secondary 4 ligand / 5 motif. The split is balanced across
both sets, so no partial fix exists and the disclosure recommendation in document 10 §4 stands
unchanged — report the source rule per arm.

### 6.4 Divergence 3 — rule-level redundancy, wider than limitation 14 records

`secondary/README.md` §7 limitation 14 records that `chk1` shares the VAIK/HRD/DFG source rule
with BCR-ABL1 (`11-synthesis.md` item 3.3, done). Three facts sit beside it and are not recorded:

1. **The sharing spans three reporting roles, not two arms.** `bcr_abl1_mandated`
   (primary, supportive-only), `bcr_abl1_corrected` (primary, **confirmatory and claim-family**)
   and `chk1` (secondary, **generalisation**) are located by one regex. The generalisation tier's
   independence from the confirmatory family is what the across-target claim rests on.
2. **`{from_motifs: [PTP]}` is shared by `mkp5` and `ptp1b`**, both in `development`. Recorded in
   document 10 §3 and in no shipped document.
3. **Clause (xii) is enforced one level shallower than the ADR that authorises it, and the
   difference is measurable.** `secondary/README.md` §4 states the clause as "No two secondary
   targets share a Pfam **family**", and `tests/test_secondary.py::test_no_two_targets_share_a_
pfam_family` implements exactly that: a string comparison of the manifests' `pfam` lists.
   **ADR 0012 clause 2 states the rule at Pfam _clan_ level** — "No member of a primary target's
   family, by Pfam **clan** and by UniProt-level orthology" — and makes it operational as "reject
   if the candidate's UniProt accession maps, via InterPro/Pfam at a **release pinned and recorded
   in the artifact**, to any clan containing `PF00071` (Ras), `PF07714` (PK_Tyr_Ser-Thr) narrowed
   to the ABL/SRC branch by its InterPro/PANTHER family assignment, or `PF00063` (Myosin_head)".
   No Pfam or InterPro release is pinned anywhere in the repository, so the clan half of that rule
   has never been run.

   Measured instead from the InterPro annotations RCSB already carries for each arm's holo polymer
   entity, cached in `data/rcsb-raw/`: **17 cross-target collisions over 10 distinct target
   pairs**, against zero at Pfam-family level.

   | target pair                                      | shared InterPro entries                                                                                                             |
   | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
   | both ABL1 arms × `chk1`                          | IPR000719 Protein kinase domain; **IPR011009 Protein kinase-like domain superfamily**; IPR017441 Protein kinase, ATP binding site   |
   | `mkp5` × `ptp1b`                                 | IPR000387 Tyrosine-specific protein phosphatases domain; IPR016130 PTP active site; **IPR029021 Protein-tyrosine phosphatase-like** |
   | `hiv_rt` × `ns5b`                                | IPR043128 Reverse transcriptase/Diguanylate cyclase domain; **IPR043502 DNA/RNA polymerase superfamily**                            |
   | KRAS (both) × myosin (both) × `ns5b` × `p97_vcp` | **IPR027417 P-loop containing nucleoside triphosphate hydrolase**, linking four targets across both sets                            |

   The three bolded entries are superfamily-level, which is the level ADR 0012 meant by "clan".
   So `secondary/README.md` §5.1's "two phosphatases of different families" is right at family
   level and shares a fold at superfamily level; the same is true of the two viral polymerases;
   and the generalisation tier does contain a second protein kinase.

Cost is bounded — a sequence-motif regex is not a fitted parameter, so no information flows from
arm to arm, and ADR 0012's narrowing of the kinase clause to "the ABL/SRC branch by its
InterPro/PANTHER family assignment" deliberately admits a Ser/Thr kinase like CHK1. But the
guarantee that ships is family-level, the ADR promises clan-level, and the pinned release the ADR
requires does not exist. A reviewer asking "is the generalisation set really independent?" gets a
weaker answer than the ADR led them to expect, and the honest answer is the table above.

### 6.5 Divergence 4 — `cardiac_myosin_mandated` has no declared reporting role

**Recorded nowhere. This is the one to fix before a method runs.**

`evaluation/manifest.yaml` `decision`:

```yaml
confirmatory_family:
  [kras_g12c_corrected, bcr_abl1_corrected, cardiac_myosin_corrected]
claim_family:
  { arms: [kras_g12c_corrected, bcr_abl1_corrected, cardiac_myosin_corrected] }
supportive_only: [kras_g12c_mandated, bcr_abl1_mandated]
across_target_claim: secondary/generalisation
```

Fifteen arms are frozen in `evaluation/frozen.json`. Fourteen have a role: three confirmatory,
two supportive-only, four `development`, five `generalisation`. **`cardiac_myosin_mandated` has
none.** It is fully scored — 932 candidates, 12 positives, 139 decoy pockets, a calibrated
matched-patch null with `size_ratio` and `alpha_star`, a `chance` block — and the decision layer
never says what its number is for.

**Cost.** An arm that is measured but unassigned is a researcher degree of freedom of exactly the
kind pre-registration exists to remove: if it reads well it can be quoted as support, if it reads
badly it can be called the 20 Å homology model. The other two mandated arms are pinned as
`supportive_only`; this one is not, and the omission looks like an oversight of the re-freeze
rather than a decision, because ADR 0031 describes the arm as non-confirmatory and the manifest
does not encode that. **Add it to `supportive_only`.** One line, and it closes the hole.

### 6.6 Divergence 5 — clause (v) is an admission rule in one set and a disclosure rule in the other

`tests/test_benchmark.py::test_frozen_assembly_is_biological_metadata_not_asymmetric_unit_count`
says so in its own docstring: "this asserts the declaration, not the equality." The primary
manifest has an `assembly_exception` field, `cardiac_myosin_mandated` uses it, and the test
requires only that the exception state both copy counts. The secondary manifest has **no
`assembly_exception` key on any target** — clause (v) there is an admission rule, and a candidate
whose oligomeric state disagreed was rejected rather than declared.

**Cost.** Modest and mostly already priced by ADR 0031, but it is the sharpest instance of the
general pattern: the primary set is _disclosed_, the secondary set is _selected_. A reader who
takes "the eight clauses bind both sets" at face value will assume clause (v) has one meaning. It
has two, and only the code says so.

### 6.7 Divergence 6 — enforcement is split, and each set is machine-checked on a different half of the rulebook

`tests/test_secondary.py`'s module docstring states half of this and is worth quoting because it
is the most honest sentence in the test suite:

> Clauses (i)-(viii) bind both benchmark sets, but `tests/test_benchmark.py` applies them to the
> PRIMARY manifest only: its `manifest` fixture is `benchmark.load()`, which resolves to
> `MANIFEST`, and every other test there reads `benchmark.FROZEN`. So the eight clauses are
> enforced on six primary arms and on nothing else.

The other half is not stated anywhere:

| clause     | primary enforcement                                               | secondary enforcement                                                                                                                                         |
| ---------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (i)–(viii) | `tests/test_benchmark.py`, per-clause, against `frozen.json`      | one test, `test_the_secondary_manifest_declares_what_the_eight_clauses_require`, "the part of that gap which is checkable from the secondary artifacts alone" |
| (ix)       | covered — the network test loops **both** manifests               | covered, same test                                                                                                                                            |
| (x)        | **prose only** (`primary/README.md` §1: "passes by construction") | `test_clause_x_no_apo_occupant_touches_a_label` against `frozen.json`                                                                                         |
| (xi)       | **prose only** (`primary/README.md` §1, a table of resolutions)   | `test_the_admitted_entries_meet_the_resolution_ceiling` against `selection.json`                                                                              |
| (xii)      | **prose only** ("fails by design")                                | `test_no_two_targets_share_a_pfam_family`, which does read the primary manifest for the cross-set half                                                        |

Clause (xi) cannot be tested against a `selection.json` on the primary set, because the primary
set has no selection ledger — there was no pool. That is ADR 0009's reasoning and it is sound.
But the _verdict_ is now a load-bearing disclosure in `primary/README.md` §1, and it is unpinned:
a future re-freeze that swapped an entry would move the two failures and break no test.

**Cost.** Low today — the verdicts in §1 are correct, as this document re-derives. Medium over
time: prose rots and `make check` does not.

### 6.8 Divergence 7 — the primary freeze carries the wrong freeze date

`docs/benchmark/primary/frozen.json` reads `"frozen_on": "2026-08-24"` and
`docs/benchmark/primary/manifest.yaml` reads `version: 2` with `frozen_on: 2026-08-24`. The
artifact demonstrably changed on 2026-09-02: `git diff --stat` shows 1356 changed lines in
`frozen.json`, chain A → B on `1OPL`, a new `5TBY` provenance block and a new sixth target. The
version field moved; the date field did not. `docs/benchmark/evaluation/frozen.json` reads
`2026-09-02`, so the three sibling freezes now disagree about when the input layer was frozen.
The secondary set's `2026-08-24` is correct — it did not change.

**Cost.** Small but it is exactly the class of error the freeze discipline exists to catch: a
reader comparing `frozen_on` across the three sets concludes the input layer is older than the
evaluation layer, when in fact both were re-derived on the same day.

### 6.9 Divergence 8 — nine stated facts are stale at the six-arm shape

Numbers come from code, and these do not. None changes a decision; all are the kind a reviewer
checks.

| #   | Location                                   | Says                                                                                      | Measured now                                                                                                                |
| --- | ------------------------------------------ | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | `primary/README.md` line 3                 | "frozen 2026-08-24. **Five** scoreable arms"                                              | six arms, re-derived 2026-09-02. The body of the same file already says "all six arms"                                      |
| 2   | `benchmark/README.md` §`primary/`          | "Frozen **2026-08-24**. **Five** scoreable arms… **One is unscoreable**"                  | six arms; none is unscoreable — `cardiac_myosin_mandated` is frozen and scored                                              |
| 3   | `evaluation/README.md` §5.3                | "over **sixteen** arms", "three of **sixteen** arms", "across the **sixteen** arms"       | fifteen. Its own table has fifteen rows, and its own next paragraph says "15 of 15 arms"                                    |
| 4   | `evaluation/README.md` §5.3 last paragraph | "Site coverage runs **0.09** on `mkp5`, **0.19** on `ns5b` and **0.36** on `ptp1b`"       | version-2 values. Its own version-3 table, six lines above, reads 0.4545 / 0.3125 / 0.3636                                  |
| 5   | `evaluation/README.md` §3.2                | "Prevalence spans **6.79×** across the five primary arms"                                 | **8.51×** across six                                                                                                        |
| 6   | `evaluation/README.md` §3.3                | "At **1.6–11 %** prevalence… scores 0.89–0.98"                                            | 1.29–10.96 %; the all-negatives ceiling is 0.891–0.987                                                                      |
| 7   | `secondary/README.md` §5.2 Axis B          | "**`1OPL` is the only structure in either set that fails**"                               | two: `1OPL` 3.42 Å and `5TBY` 20.00 Å                                                                                       |
| 8   | `secondary/README.md` §5.2 Axis C          | "**4 of 5** primary arms exceed [0.3 Å]… primary worst case is **1.25 Å** against 0.64 Å" | **5 of 6**; worst case **17.10 Å** (`5TBY` 20.0 against `9GZ2` 2.9). Secondary's 3 of 9 and 0.64 Å are unchanged            |
| 9   | `review/data/clause-ix-both-sets.json`     | fourteen arms                                                                             | fifteen exist; `cardiac_myosin_mandated` is absent. Its verdict is entailed by the shared `9GZ2`:A holo, so no number moves |

Item 8 is the one that matters. Axis C is the repository's own statement that the primary set
carries more resolution confound than the secondary set, and at the new shape the gap is not
1.25 Å against 0.64 Å — it is **17.10 Å** against 0.64 Å. Every transplant-clash count and
pocket-lining RMSD on `cardiac_myosin_mandated` is a comparison between a 20 Å rigid-fitted
homology model and a 2.9 Å cryo-EM structure.

Space groups, re-derived for completeness, because document 10 §5 corrected them at five arms:
two of the four crystallographic primary arms differ (`kras_g12c_mandated` `C 1 2 1` → `P 21 21
21`; `bcr_abl1_corrected` `P 21 21 2` → `C 2 2 21`), and both myosin arms are EM/EM with no
crystal form. "Two, not three" survives the re-freeze unchanged.

### 6.10 Divergence 9 — the synthetic-effector gap, now promoted but not re-counted

`11-synthesis.md` item 3.4 promoted the synthetic-effector gap to `benchmark/README.md`, which is
the right home. At the new shape the count is **fifteen of fifteen**: `MOV`, `AY7`, `XB2`, `NUU`,
`AGX`, `BB3`, `QKT`, `MRK`, `NVP`, `CMF`, `OJA`, `U5P` — every admitted effector is a synthetic
small molecule. Classical allosteric enzymology, cooperativity and feedback inhibition by a
metabolite, is untested across the whole benchmark. The one physiological candidate, AMP on
glycogen phosphorylase, was rejected by clause (ix). This is the only divergence in the list that
is genuinely **shared** — the two sets have the identical gap, and that is why it belongs at
`benchmark/README.md` rather than in either set's page.

---

## 7. Judgement

**Is the benchmark internally consistent — same rules, same definitions, same processing, same
standard — across both sets and both axes?**

**Same processing: yes, and it is not close.** One `derive`, one cutoff, one label-transfer
module, one detector, one null, one `score_arm`, over fifteen arms. This is the part that would
be hardest to retrofit and it was built right.

**Same definitions: yes.** All twelve clauses are measurable on all fifteen arms, and every cell
in §6 resolved to pass or fail — no cell came back "unknown" and no clause turned out to mean
something different on the other set. That is a real result and it is the answer to the "different
rules for different sets" objection.

**Same rules: no, in five places.** Complete label transfer is required of the secondary set and
not the primary (6.2). Clause (v) admits on one set and merely discloses on the other (6.6).
Clauses (x), (xi) and (xii) are executable on the secondary set and prose on the primary (6.7).
The source rule is fixed per target everywhere except myosin (6.3). And the redundancy guarantee
is family-level where the reader will read it as fold-level (6.4).

**Same standard: no.** The three that cost the most are asymmetric in the same direction — the
primary set is held to a lower bar and the difference is _disclosed_ rather than _repaired_,
which is the right policy but must be priced when the two sets are compared. Both clause-(xi)
failures, the only clause-(v) failure, both label-transfer failures and the resolution-mismatch
worst case are all primary arms. The secondary set's own §5.2 anticipated this and named three
axes; there are now five, and two of the three it named have stale numbers.

**One hole, not a difference.** 6.5 is not an inconsistency between the sets — it is a missing
line. `cardiac_myosin_mandated` is scored with no declared role.

**Disposition, ranked by cost.**

1. **Add `cardiac_myosin_mandated` to `decision.supportive_only`** in
   `evaluation/manifest.yaml` (6.5). One line. Do it before a method runs, or the arm is an
   unpriced degree of freedom.
2. **Decide the label-transfer standard** (6.2). Either extend the secondary set's rule to the
   primary set and re-open the two ABL1 arms, or record in `primary/README.md` §1 that the two
   ABL1 arms are scored against 17/20 and 18/20 of the asciminib pocket and that a cross-set
   recall comparison is not like-for-like. The second is cheap and probably right; leaving it
   unrecorded is not an option, because `bcr_abl1_corrected` is a claim-family arm.
3. **Correct the eight stale facts** in 6.9 and add the ninth arm to
   `review/data/clause-ix-both-sets.json`. Axis C first: 5 of 6 and a 17.10 Å worst case.
4. **Record the myosin source-rule split** (6.3) and name it in ADR 0033 as the cleaner
   instrument for the motif-vs-ligand question the ADR pre-registers on KRAS.
5. **Reconcile clause (xii) with ADR 0012** (6.4). Either pin an InterPro/Pfam release and run
   the clan-level rule the ADR specifies, or amend `secondary/README.md` §4 to say the shipped
   guarantee is family-level and carry the 17-collision InterPro table beside it. Extend
   limitation 14 with the three-role span and the `PTP` pair at the same time.
6. **Fix `frozen_on` in the primary freeze and manifest** (6.8), or state why a re-derived
   artifact keeps its old date.
7. **Pin the primary set's (x)/(xi)/(xii) verdicts in a test** (6.7), so `primary/README.md` §1
   cannot silently rot.
8. **Name `p97_vcp` beside the four low-coverage arms** (§5), and state that all five are
   secondary.

Nothing in this list blocks scoring except item 1.

---

## Appendix A — the script, verbatim

Run as `uv run python consistency.py` from the session scratchpad. It is not tracked: a tracked
file naming `frozen.json` fails `tests/test_no_leakage.py`, and this script names all three
freezes plus both manifests plus `selection.json`'s sibling artifacts. It writes nothing.

```python
"""Cross-set consistency at the six-arm primary shape. Read-only.

Every number is re-derived from the frozen artifacts and the cached deposited
mmCIF files. Nothing is written back into the repository.
"""

import json
import pathlib
import statistics
import yaml

ROOT = pathlib.Path("/Users/george0502/dev/004-allosteric-site")
B = ROOT / "docs/benchmark"

prim_f = json.loads((B / "primary/frozen.json").read_text())
sec_f = json.loads((B / "secondary/frozen.json").read_text())
eval_f = json.loads((B / "evaluation/frozen.json").read_text())
prim_m = yaml.safe_load((B / "primary/manifest.yaml").read_text())
sec_m = yaml.safe_load((B / "secondary/manifest.yaml").read_text())
eval_m = yaml.safe_load((B / "evaluation/manifest.yaml").read_text())
struct = json.loads((B / "review/data/structure-evidence.json").read_text())["entries"]
cix = json.loads((B / "review/data/clause-ix-both-sets.json").read_text())

PRIM = list(prim_f["targets"])
SEC = list(sec_f["targets"])
ARMS = PRIM + SEC
FROZEN = {**prim_f["targets"], **sec_f["targets"]}
MAN = {t["id"]: t for t in prim_m["targets"]} | {t["id"]: t for t in sec_m["targets"]}
SETOF = {a: ("primary" if a in PRIM else "secondary") for a in ARMS}


def rule(a):
    s = MAN[a]["active_site"]
    kind = "ligands" if "from_ligands" in s else "motifs"
    return kind, tuple(s.get("from_ligands") or s.get("from_motifs"))


def emit(title, header, rows):
    print(f"\n### {title}\n")
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join("---" for _ in header) + "|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


# ---------------------------------------------------------------- vertical
def vertical(names, label):
    rows = []
    for a in names:
        f, e = FROZEN[a], eval_f["targets"][a]
        kind, terms = rule(a)
        d = e["decoys"]
        sp = d["site_pocket"]
        rows.append(
            [
                a,
                f["tier"],
                f["n_residues"],
                e["n_candidates"],
                f["n_residues"] - e["n_candidates"],
                e["n_positive"],
                f"{100 * e['prevalence']:.1f}%",
                f"{kind}:{'+'.join(terms)}",
                len(f["active_site"]),
                len(d["pockets"]),
                f"{sp['label_coverage']:.4f}",
                f"{f['sequence_agreement']['identity']:.4f}",
                f["sequence_agreement"]["aligned"],
                len(f["unmapped"]),
                len(f["labels_outside_node_set"]),
            ]
        )
    emit(
        f"Vertical — {label}",
        [
            "arm",
            "tier",
            "n_residues",
            "n_candidates",
            "delta",
            "n_positive",
            "prevalence",
            "source rule",
            "|source|",
            "decoys",
            "site cov",
            "identity",
            "aligned",
            "unmapped",
            "labels outside nodes",
        ],
        rows,
    )
    return rows


vertical(PRIM, "primary, six arms")
vertical(SEC, "secondary, nine arms")

# ------------------------------------------------------- prevalence spread
prev = {a: eval_f["targets"][a]["prevalence"] for a in ARMS}
print("\n### Prevalence spread\n")
for grp, names in (("primary", PRIM), ("secondary", SEC), ("all", ARMS)):
    v = [prev[a] for a in names]
    lo, hi = min(v), max(v)
    alo = min(names, key=prev.get)
    ahi = max(names, key=prev.get)
    print(
        f"- **{grp}** (n={len(v)}): {100 * lo:.1f}% ({alo}) to {100 * hi:.1f}% "
        f"({ahi}); ratio {hi / lo:.2f}x; median {100 * statistics.median(v):.1f}%"
    )

# -------------------------------------------------------- decoy site cover
print("\n### Decoy site coverage\n")
cov = {a: eval_f["targets"][a]["decoys"]["site_pocket"]["label_coverage"] for a in ARMS}
for a in sorted(ARMS, key=cov.get):
    d = eval_f["targets"][a]["decoys"]
    print(
        f"- {a:26s} {SETOF[a]:9s} cov={cov[a]:.4f} "
        f"labels_covered={d['site_pocket']['labels_covered']}/"
        f"{eval_f['targets'][a]['n_positive']} "
        f"n_detected={d['n_detected']} halo_excluded={len(d['excluded_by_halo'])} "
        f"decoys={len(d['pockets'])} min_p={d['minimum_attainable_p']}"
    )

# decoy lining size vs label set
print("\ndecoy lining size vs label set (median lining / n_positive):")
ratios = []
for a in ARMS:
    e = eval_f["targets"][a]
    sizes = [len(p["lining"]) for p in e["decoys"]["pockets"].values()]
    r = statistics.median(sizes) / e["n_positive"]
    ratios.append(r)
    print(
        f"- {a:26s} median lining {statistics.median(sizes):6.1f} / {e['n_positive']:2d} = {r:.3f}"
    )
print(
    f"median over {len(ratios)} arms = {statistics.median(ratios):.3f}; "
    f"smaller-than-label on {sum(r < 1 for r in ratios)}/{len(ratios)}"
)

# ------------------------------------------------------------- clause xi
print("\n### Clause (xi) — structure admission, both members of every arm\n")
CEIL = {"X-ray": 2.5, "EM": 4.0, "Electron Microscopy": 4.0}
rows = []
for a in ARMS:
    m = MAN[a]
    for role in ("apo", "holo"):
        pdb = m[role]["pdb"]
        s = struct.get(pdb)
        if s is None:
            rows.append([a, role, pdb, "unknown", "unknown", "unknown"])
            continue
        meth = s["experimental_method"]
        res = s.get("resolution_combined_angstrom")
        ceil = CEIL.get(meth)
        ok = "unknown" if (res is None or ceil is None) else ("pass" if res <= ceil else "FAIL")
        rows.append([a, role, pdb, meth, res, f"{ok} (ceiling {ceil})"])
emit("clause (xi) per entry", ["arm", "role", "pdb", "method", "res A", "verdict"], rows)

print("\nDistinct entries and their admission:\n")
seen = {}
for a in ARMS:
    for role in ("apo", "holo"):
        pdb = MAN[a][role]["pdb"]
        seen.setdefault(pdb, []).append(f"{a}:{role}")
for pdb in sorted(seen):
    s = struct.get(pdb, {})
    meth = s.get("experimental_method", "unknown")
    res = s.get("resolution_combined_angstrom")
    ceil = CEIL.get(meth)
    ok = "unknown" if (res is None or ceil is None) else ("pass" if res <= ceil else "FAIL")
    print(f"- {pdb} {meth:22s} res={res} -> {ok}   used by {', '.join(seen[pdb])}")

# 5TBY detail: the homology-model resolution claim
t = struct.get("5TBY", {})
print(
    "\n5TBY detail:",
    {
        k: t.get(k)
        for k in (
            "experimental_method",
            "exptl_methods",
            "resolution_combined_angstrom",
            "structure_determination_methodology",
            "title",
            "space_group",
        )
    },
)

# ------------------------------------------------------------ space groups
print("\n### Space group / resolution matching per arm\n")
rows = []
for a in ARMS:
    m = MAN[a]
    sa, sh = struct.get(m["apo"]["pdb"], {}), struct.get(m["holo"]["pdb"], {})
    ra, rh = (
        sa.get("resolution_combined_angstrom"),
        sh.get("resolution_combined_angstrom"),
    )
    delta = "unknown" if None in (ra, rh) else f"{abs(ra - rh):.2f}"
    ga, gh = sa.get("space_group"), sh.get("space_group")
    xtal = sa.get("experimental_method") == "X-ray" and sh.get("experimental_method") == "X-ray"
    same = "n/a (not both X-ray)" if not xtal else ("same" if ga == gh else "differ")
    rows.append(
        [
            a,
            m["apo"]["pdb"],
            sa.get("experimental_method"),
            ra,
            ga,
            m["holo"]["pdb"],
            sh.get("experimental_method"),
            rh,
            gh,
            delta,
            same,
        ]
    )
emit(
    "space group + resolution",
    [
        "arm",
        "apo",
        "apo method",
        "apo res",
        "apo SG",
        "holo",
        "holo method",
        "holo res",
        "holo SG",
        "|dres|",
        "SG",
    ],
    rows,
)

# ------------------------------------------------------- clauses i - xii
print("\n### Twelve-clause matrix\n")


def clause_cells(a):
    f, m = FROZEN[a], MAN[a]
    out = {}
    # (i) effector present, site residues at declared 4.5 A radius
    lig = m["holo"].get("ligand")
    fp = f["holo_label_footprint"]
    out["i"] = ("pass" if lig and fp else "FAIL", f"{lig}, {len(fp)} lining at 4.5 A")
    # (ii) functional evidence DOI
    ev = m.get("allosteric_evidence", {})
    out["ii"] = ("pass" if ev.get("doi") else "FAIL", ev.get("doi", "none"))
    # (iii) site-apo on the scoreable portion
    occ = f["apo_site_occupancy"]
    sc = occ["scoreable_labels_contacted"]
    out["iii"] = (
        "pass" if sc == 0 else "FAIL",
        f"scoreable contacted {sc}; all-label {occ['labels_contacted']}"
        f"/{len(f['label_residues'])}, nearest "
        f"{occ['nearest_label_angstrom']} A",
    )
    # (iv) identity
    idn = f["sequence_agreement"]["identity"]
    out["iv"] = ("pass" if idn >= 0.90 else "FAIL", f"{idn:.4f}")
    # (v) assembly
    ag = f["assembly_agreement"]
    ok = ag["selected_target_copies_match"] and ag["polymer_composition_matches"]
    out["v"] = (
        "pass" if ok else "FAIL",
        f"copies_match={ag['selected_target_copies_match']}, "
        f"composition_match={ag['polymer_composition_matches']}",
    )
    # (vi) orthosteric state recorded both members, active-site rule stated
    os_ = f["orthosteric_state"]
    kind, terms = rule(a)
    ok = ("apo" in os_) and ("holo" in os_) and bool(terms)
    out["vi"] = (
        "pass" if ok else "FAIL",
        f"apo={os_.get('apo')}, holo={os_.get('holo')}, rule from_{kind}",
    )
    # (vii) non-circularity
    overlap = sorted(set(f["active_site"]) & set(f["scoreable_label_residues"]))
    lost = sorted(set(f["label_residues"]) & set(f["active_site"]))
    out["vii"] = (
        "pass" if not overlap else "FAIL",
        f"{len(lost)} of {len(f['label_residues'])} labels removed; "
        f"residual overlap {len(overlap)}",
    )
    # (viii) state disclosure
    st = m.get("state", {})
    rms = f["apo_holo_rmsd"]
    ok = bool(st.get("apo")) and bool(st.get("holo")) and rms.get("pocket_lining") is not None
    out["viii"] = (
        "pass" if ok else "FAIL",
        f"apo='{st.get('apo')}', holo='{st.get('holo')}', lining RMSD {rms.get('pocket_lining')} A",
    )
    # (ix) single-chain lining, measured on the biological assembly
    key = a if a in cix else None
    if key is None:  # share the holo with a sibling arm
        for other, rec in cix.items():
            if rec["holo"] == f"{m['holo']['pdb']}:{m['holo']['chain']}":
                key = other
                break
    if key:
        r = cix[key]
        out["ix"] = (
            "pass" if r["single_chain_in_AU"] else "FAIL",
            f"holo {r['holo']}, lining chains {r['lining_chains_in_AU']}, "
            f"{r['lining_residues_by_chain']}"
            + ("" if key == a else f" [inherited from {key}, same holo]"),
        )
    else:
        out["ix"] = ("unknown", "no assembly measurement")
    # (x) apo occupant classification
    out["x"] = (
        "pass" if sc == 0 else "FAIL",
        f"apo components {occ['chain_components']}; "
        f"scoreable contacted {sc}, nearest scoreable "
        f"{occ['nearest_scoreable_label_angstrom']} A",
    )
    # (xi) structure admission
    verdicts = []
    for role in ("apo", "holo"):
        s = struct.get(m[role]["pdb"], {})
        meth, res = s.get("experimental_method"), s.get("resolution_combined_angstrom")
        ceil = CEIL.get(meth)
        verdicts.append(
            (
                m[role]["pdb"],
                meth,
                res,
                None if ceil is None or res is None else res <= ceil,
            )
        )
    bad = [v for v in verdicts if v[3] is False]
    unk = [v for v in verdicts if v[3] is None]
    tag = "FAIL" if bad else ("unknown" if unk else "pass")
    out["xi"] = (tag, "; ".join(f"{p} {m_} {r}" for p, m_, r, _ in verdicts))
    return out


PF = {a: set(MAN[a]["pfam"]) for a in ARMS}
PROT = {a: MAN[a]["protein"] for a in ARMS}


def clause_xii(a):
    """Pfam disjointness against every arm of a DIFFERENT target."""
    hits = []
    for b in ARMS:
        if b == a or PROT[b].split()[0] == PROT[a].split()[0]:
            continue
        shared = PF[a] & PF[b]
        if shared:
            hits.append(f"{b}:{'/'.join(sorted(shared))}")
    return (
        "pass" if not hits else "FAIL",
        "no shared Pfam with any other target" if not hits else "; ".join(hits),
    )


CL = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]
cells = {}
for a in ARMS:
    c = clause_cells(a)
    c["xii"] = clause_xii(a)
    cells[a] = c

emit(
    "verdicts",
    ["arm", "set"] + [f"({c})" for c in CL],
    [[a, SETOF[a]] + [cells[a][c][0] for c in CL] for a in ARMS],
)

print("\n#### The measurement behind each cell\n")
for a in ARMS:
    print(f"\n**{a}** ({SETOF[a]}, {FROZEN[a]['tier']})\n")
    for c in CL:
        v, why = cells[a][c]
        print(f"- ({c}) **{v}** — {why}")

# ---------------------------------------------------- rule-level redundancy
print("\n### Source-rule sharing across arms\n")
by_rule = {}
for a in ARMS:
    by_rule.setdefault(rule(a), []).append(a)
for (kind, terms), arms in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
    prots = sorted({PROT[x].split()[0] for x in arms})
    print(
        f"- `from_{kind}: {list(terms)}` -> {arms}  "
        f"[{len(prots)} distinct proteins: {prots}] "
        f"[sets: {sorted({SETOF[x] for x in arms})}]"
    )

nlig = sum(1 for a in ARMS if rule(a)[0] == "ligands")
print(f"\nligand-derived source: {nlig}/{len(ARMS)}; motif-derived: {len(ARMS) - nlig}/{len(ARMS)}")
for grp, names in (("primary", PRIM), ("secondary", SEC)):
    n = sum(1 for a in names if rule(a)[0] == "ligands")
    print(f"  {grp}: {n} ligand / {len(names) - n} motif")

print("\nSame target, different source rule:")
for p in sorted({PROT[a].split()[0] for a in ARMS}):
    arms = [a for a in ARMS if PROT[a].split()[0] == p]
    rules = {rule(a) for a in arms}
    if len(rules) > 1:
        print(f"  {p}: " + "; ".join(f"{a} -> from_{rule(a)[0]}{list(rule(a)[1])}" for a in arms))

# ------------------------------------------------------- blind / tier / role
print("\n### Reporting role per arm\n")
dec = eval_m["decision"]
conf = set(dec["confirmatory_family"])
claim = set(dec["claim_family"]["arms"])
supp = set(dec["supportive_only"])
across = dec["across_target_claim"]
for a in ARMS:
    role = (
        "confirmatory"
        if a in conf
        else "supportive-only"
        if a in supp
        else "across-target (generalisation)"
        if FROZEN[a]["tier"] == "generalisation"
        else "development (tuning)"
    )
    m = MAN[a]
    blind = m.get("blind", {}).get("value")
    defect = (
        "defect" if "defect" in m else ("assembly_exception" if "assembly_exception" in m else "-")
    )
    print(
        f"- {a:26s} set={SETOF[a]:9s} tier={FROZEN[a]['tier']:14s} "
        f"role={role:32s} blind={blind} {defect}"
    )
print(f"\nclaim_family={sorted(claim)}  across_target_claim='{across}'")

# ------------------------------------------------- primary README stale count
print("\n### Stale-count checks\n")
print(
    "evaluation/README.md v3 decoy table row count vs prose 'sixteen arms':",
    len(ARMS),
    "arms exist",
)
print("primary/README.md status line says 'Five scoreable arms'; frozen has", len(PRIM))
print(
    "primary frozen_on =",
    prim_f["frozen_on"],
    " secondary frozen_on =",
    sec_f["frozen_on"],
    " evaluation frozen_on =",
    eval_f["frozen_on"],
    "protocol",
    eval_f["protocol_version"],
)
print("clause-ix-both-sets.json covers", len(cix), "arms:", sorted(cix))
print("arms missing from clause-ix file:", sorted(set(ARMS) - set(cix)))

# --------------------------------------- supplementary vertical measurements
print("\n### Alignment coverage, source separation, label-set stability\n")
rows = []
for a in ARMS:
    f, e = FROZEN[a], eval_f["targets"][a]
    sa = f["sequence_agreement"]
    d = f["distance_to_active_site"]
    bc = f["labels_by_cutoff"]
    rows.append(
        [
            a,
            SETOF[a],
            f["n_residues"],
            sa["aligned"],
            f"{sa['aligned'] / f['n_residues']:.3f}",
            f"{sa['identity']:.4f}",
            len(sa["differences_in_label_set"]),
            len(f["holo_label_footprint"]),
            len(f["label_residues"]),
            len(f["unmapped"]),
            f"{d['min']}/{d['median']}/{d['max']}",
            f"{len(bc['4.0'])}/{len(bc['4.5'])}/{len(bc['5.0'])}",
            f["transplant_clashes"],
            f["superposition_rmsd"],
            f["apo_holo_rmsd"]["pocket_lining"],
        ]
    )
emit(
    "supplementary",
    [
        "arm",
        "set",
        "nodes",
        "aligned",
        "coverage",
        "identity",
        "diffs in labels",
        "holo footprint",
        "labels kept",
        "unmapped",
        "src dist min/med/max",
        "labels at 4.0/4.5/5.0",
        "clashes",
        "superpos RMSD",
        "lining RMSD",
    ],
    rows,
)

# resolution matching, at the 0.3 A community guidance
print("\n### Resolution matching against the 0.3 A guidance\n")
for grp, names in (("primary", PRIM), ("secondary", SEC)):
    over = []
    for a in names:
        m = MAN[a]
        ra = struct.get(m["apo"]["pdb"], {}).get("resolution_combined_angstrom")
        rh = struct.get(m["holo"]["pdb"], {}).get("resolution_combined_angstrom")
        if None in (ra, rh):
            continue
        if abs(ra - rh) >= 0.3:
            over.append((a, round(abs(ra - rh), 2)))
    worst = max((x[1] for x in over), default=0)
    print(f"- {grp}: {len(over)} of {len(names)} at or above 0.3 A -> {over}; worst {worst} A")

# clause (vii) cost per set
print("\n### Clause (vii) cost per arm\n")
for a in ARMS:
    f = FROZEN[a]
    lost = sorted(set(f["label_residues"]) & set(f["active_site"]))
    print(
        f"- {a:26s} {SETOF[a]:9s} removes {len(lost)}/{len(f['label_residues'])} "
        f"labels ({len(lost) / len(f['label_residues']):.1%}) -> {lost}"
    )
```

## Appendix B — clause (xii) at InterPro level, verbatim

Section 6.4's table. It reads the InterPro annotations RCSB already returned for each arm's
holo polymer entity, cached under `data/rcsb-raw/`, so it needs no network and pins nothing
new. It is not a substitute for the pinned-release clan lookup ADR 0012 asks for; it is the
cheapest available evidence that the family-level check and the clan-level rule differ.

```python
"""Clause (xii) at InterPro level, from the cached RCSB polymer-entity annotations."""

import glob
import json
import pathlib

import yaml

B = pathlib.Path("/Users/george0502/dev/004-allosteric-site/docs/benchmark")
RAW = B / "review/data/rcsb-raw"
man = [
    *yaml.safe_load((B / "primary/manifest.yaml").read_text())["targets"],
    *yaml.safe_load((B / "secondary/manifest.yaml").read_text())["targets"],
]


def annotations(pdb, kind):
    out = {}
    for f in glob.glob(str(RAW / pdb / "polymer_entity_*.json")):
        for a in json.load(open(f)).get("rcsb_polymer_entity_annotation") or []:
            if a.get("type") == kind:
                out[a["annotation_id"]] = a.get("name")
    return out


ipr = {t["id"]: annotations(t["holo"]["pdb"], "InterPro") for t in man}
pfam = {t["id"]: annotations(t["holo"]["pdb"], "Pfam") for t in man}
prot = {t["id"]: t["protein"].split()[0] for t in man}
for a, v in ipr.items():
    print(f"{a:26s} holo-entity InterPro n={len(v):2d} Pfam={sorted(pfam[a])}")
print()
seen = set()
for a in ipr:
    for b in ipr:
        if a >= b or prot[a] == prot[b]:
            continue
        shared = set(ipr[a]) & set(ipr[b])
        if shared:
            print(f"{a} x {b}: {len(shared)} shared InterPro")
            for s in sorted(shared):
                print(f"    {s}  {ipr[a][s]}")
            seen.add((a, b))
print("\ncross-target InterPro collisions:", len(seen))
```

## Appendix C — what neither script derives

**One derivation is a read of the test suite rather than of an artifact.** Section 6.7's
enforcement table comes from `grep -n "^def test" tests/test_benchmark.py tests/test_secondary.py`
plus the fixtures at the top of each file, and section 6.2's assertion block is quoted from
`tests/test_secondary.py::test_every_transferred_label_survives_into_the_node_set`. Section 6.8's
"the artifact changed on 2026-09-02" comes from `git diff --stat` against the working tree.

**Three things are unknown and are recorded as unknown.** Clause (ii) cannot be decided by code —
this document checks only that a DOI is present, and the reading is
`14-clause-ii-literature-pass.md`. And clause (ix) for `cardiac_myosin_mandated` is _entailed_
rather than _measured_: the arm shares `9GZ2`:A with `cardiac_myosin_corrected`, whose assembly
was downloaded and measured, so the verdict is sound but the artifact has fourteen rows. And
**clause (xii) at Pfam-clan level is unknown**, because ADR 0012 requires a pinned Pfam/InterPro
release and no release is pinned; Appendix B measures the InterPro annotations RCSB happened to
return when `08-structure-evidence.md` cached them, which is evidence of a collision but is not
the pinned lookup the ADR specifies.
