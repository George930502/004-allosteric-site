# Conservation, measured

**Measured 2026-09-02.** ADR 0035 decided the fourth confounder column and did not build it.
`11-synthesis.md` item 3.1 calls it "the single highest-value addition in this audit".
This file builds it, measures it on all fifteen arms, and reports what it found.

**Nothing here is frozen.** The column is a review-side measurement. Promoting it into
`evaluation/manifest.yaml` needs an ADR, and §6 states exactly what that ADR must decide.

---

## 1. The headline

**Sequence conservation does not separate allosteric label residues from background on this
benchmark.** Over the eleven arms where the column covers at least 75 % of the candidate set,
the median AUC-ROC is **0.491**, five of eleven arms sit above chance, and a Wilcoxon
signed-rank test against 0.5 gives **p = 0.76**.

The objection the column exists to answer is "your allosteric hits are just the conserved
residues." The answer is now a number, and the number is no.

**Two further results matter more than the headline.**

1. **ADR 0035's stated blocker is dissolved.** The ADR records that artifact size blocks the
   column, because `PF07714` alone is 191 MB gzipped. The alignments are transient input, not
   the artifact. The 27 families this benchmark needs total **1 107 655 109 bytes** gzipped,
   and the committed artifact is **172 KB**: the derived per-residue column, the per-family
   SHA-256, and the tools. §4 gives the route.
2. **Coverage is the real blocker, and it is worse than the ADR predicted.** ADR 0035 named
   the 764-residue myosin arm as the specific risk. Myosin is fine at 0.88 and 0.92. Four
   other arms fall below 0.55, and **`ns5b` reads zero**. §5.

---

## 2. Method

Per-column Jensen-Shannon divergence in the Capra & Singh parameterisation
(doi:10.1093/bioinformatics/btm270), exactly as ADR 0035 specifies: BLOSUM62 background,
Henikoff-Henikoff sequence weights, lambda = 1/2, window heuristic **off**.

**Every constant is read from the authors' own source, not recalled.**
`score_conservation.py` was fetched on 2026-09-02 from
`https://compbio.cs.princeton.edu/conservation/score_conservation.py` (HTTP 200, 21 896 bytes).

| Constant                  | Line in that file | Value                                         |
| ------------------------- | ----------------- | --------------------------------------------- |
| `amino_acids`             | 66                | `ARNDCQEGHILKMFPSTWYV` plus `-`               |
| `PSEUDOCOUNT`             | 64                | `1e-7`                                        |
| `blosum_background_distr` | 585               | the 20-vector, in that order                  |
| `window_size`             | 597               | `0`, so the reference default is off too      |
| sequence cleaning         | 524, 555          | uppercase, `B` to `D`, `Z` to `Q`, `X` to gap |

**The implementation is verified against the reference, not against itself.**
`data/conservation/check_jsd.py` transcribes the reference's scalar `calculate_sequence_weights`
and `js_divergence` into Python 3 and compares them with the vectorised versions on a random
45 x 37 alignment:

```
OK  weights max|diff|=1.39e-17  jsd max|diff|=8.33e-17
```

That is floating-point noise. The vectorised code computes the published statistic.

---

## 3. The residue-to-column map needs no aligner

This is the part ADR 0035 left open, and it turns out to be free.

Pfam full alignments carry each member's UniProt accession in a `#=GS <name> AC <accession>`
line. Every arm's apo entry declares its accession in `_struct_ref`, so the arm's **own row**
is in the alignment and its gap pattern is an exact residue-to-column map. No HMM, no profile
alignment, no `hmmalign`, and therefore no second inference step to freeze and defend.

Worked example, `4OBE` chain A:

```
#=GS RASK_HUMAN/5-165            AC P01116.1
```

`_struct_ref_seq` gives the author-to-UniProt offset; the row gives UniProt-to-column. Match
columns are the uppercase-or-`-` positions and are shared across every row; insert columns are
lowercase-or-`.` and are not, so a residue sitting in one has no shared column and reads null.

**Cost.** `PF00071` holds 221 818 rows and 162 match columns. Reading it, weighting it and
scoring every column takes **2.2 s**.

---

## 4. What the pinned artifact is

ADR 0035 says the pinned artifact must be "the derived column plus the alignment hash, never
the alignment", and `evaluation/manifest.yaml` repeats it. That is what is committed here.

| File                                      | What it is                                               | Size   |
| ----------------------------------------- | -------------------------------------------------------- | ------ |
| `data/conservation/per-residue-jsd.json`  | the column itself, author numbering, all fifteen arms    | 130 KB |
| `data/conservation/alignment-hashes.json` | 27 families: source, fetch date, row count, gzip SHA-256 | 3.3 KB |
| `data/conservation/jsd.py`                | the statistic                                            | 5.0 KB |
| `data/conservation/column.py`             | the residue-to-column map                                | 3.9 KB |
| `data/conservation/fetch_aln.py`          | the fetch, so the hashes are reproducible                | 1.5 KB |
| `data/conservation/check_jsd.py`          | the check against the reference                          | 2.1 KB |
| `data/conservation/per-arm-auc.json`      | the measurement below                                    | 15 KB  |

**172 KB against 1.108 GB of input.** The largest single family, `PF00069`, is 515 MB gzipped
and holds 1 051 874 rows.

**The alignments are transient input and are not committed.** Run `python fetch_aln.py full`
inside `data/conservation/` to rebuild `aln/`, then check each file against
`alignment-hashes.json`. Without it `column.residue_scores` returns
`{'status': 'alignment-missing'}` rather than a wrong number.

Every file under `data/conservation/` imports nothing from `allo` and names no path outside
`docs/benchmark/review/`, so ADR 0034's review-tool rule exempts it and
`tests/test_no_leakage.py` passes with it in place.

**The two scripts that open `frozen.json` are not committed and cannot be**, because the
leakage gate fails any tracked script naming that file. They stay in the scratchpad and their
source is reproduced in §7, which is the convention `12-dataset-eda.md` §9 set.

---

## 5. The measurement

Label sets are the frozen `scoreable_label_residues`; the background is the rest of the
candidate set. A residue covered by two families takes the higher value.

| arm                        | coverage  | labels scored | AUC-ROC |
| -------------------------- | --------- | ------------- | ------- |
| `kras_g12c_mandated`       | 0.931     | 16/16         | 0.6219  |
| `kras_g12c_corrected`      | 0.926     | 16/16         | 0.6250  |
| `bcr_abl1_mandated`        | 0.825     | 16/17         | 0.4907  |
| `bcr_abl1_corrected`       | 0.916     | 16/18         | 0.4893  |
| `cardiac_myosin_mandated`  | 0.880     | 10/12         | 0.4873  |
| `cardiac_myosin_corrected` | 0.918     | 10/12         | 0.4603  |
| `mkp5`                     | 0.882     | 11/11         | 0.7389  |
| `chk1`                     | 0.904     | 12/12         | 0.5428  |
| `ptp1b`                    | 0.767     | 6/11          | 0.3287  |
| `glucokinase`              | 0.934     | 15/19         | 0.6195  |
| `hiv_rt`                   | 0.805     | 14/16         | 0.2692  |
| `smyd3`                    | **0.253** | 2/12          | 0.0446  |
| `p97_vcp`                  | **0.432** | 8/17          | 0.2643  |
| `ecoli_cps`                | **0.513** | 15/19         | 0.4794  |
| `ns5b`                     | **0.000** | 0/16          | none    |

**Restricted to the eleven arms at coverage 0.75 or better:** median **0.4907**, mean 0.5158,
range 0.2692 to 0.7389, five of eleven above chance, Wilcoxon signed-rank against 0.5
**W = 29, p = 0.7646**.

**The direction is not even consistent.** `mkp5` reaches 0.739 and `hiv_rt` reaches 0.269. A
column that runs both ways across arms cannot be the thing a method is secretly re-measuring.

**This is consistent with both papers ADR 0035 cites and settles which one applies here.**
Cimermancic 2016 reports cryptic-site residues significantly more conserved than background;
Leander 2020 reports allosteric signalling residues surprisingly poorly conserved. Our label
sets are effector-contact linings, and they behave like neither: they sit at chance.

### 5.1 Why four arms fall short, and why one reads zero

Pfam covers the domain envelope, not the chain. The shortfall is structural, not a bug.

| arm         | families                           | residues covered | of   |
| ----------- | ---------------------------------- | ---------------- | ---- |
| `smyd3`     | PF00856 (90), PF01753 (39)         | 112              | 425  |
| `p97_vcp`   | PF00004, PF02359, PF02933, PF17862 | 309              | 723  |
| `ecoli_cps` | PF02786, PF02787, PF25596, PF02142 | 540              | 1058 |

**`ns5b` reads zero for a different reason, and it is fixable.** `1QUV` declares UniProt
**P26663** (HCV genotype 1b, isolate BK). `PF00998` holds 267 rows and P26663 is not one of
them, but **P27958** is — `POLG_HCV77/2423-2934`, a different isolate of the same virus. The
exact-accession rule this probe uses therefore fails on an arm whose family is present.

---

## 6. What an ADR would have to decide

Three things block promotion into the freeze, and none is artifact size.

1. **The frozen harness rejects a partial column.** `score_arm` raises
   `ValueError: no score for candidate residues [...]` when any candidate is missing. ADR 0035
   says uncovered residues "read null"; the harness has no null. **An imputation rule is
   required and the ADR does not state one.** The measurement in §5 avoids the question by
   scoring only covered residues, which is a different estimand from a full-column AUC.
2. **A coverage floor.** At `smyd3`'s 0.253 and two labels of twelve, the AUC of 0.0446 is
   not a measurement of anything. A floor — 0.75 is the natural break in the data — must be
   declared before the column is reported, not after.
3. **The fallback for a missing accession.** `ns5b` needs either a same-species-homolog rule
   or an honest `null`. Both are defensible; picking one after seeing which arm it rescues is
   not.

**Not yet measured.** The column has not been run end to end through `score_arm` with the
median filler. The run was started and is still on `cardiac_myosin_mandated`, whose 954-node
permutation null is the slowest in the benchmark. **No calibrated p-value for
`jsd_conservation` is claimed anywhere in this file.** The AUC table in §5 needs no null.

---

## 7. The two scripts that cannot be committed

Reproduced verbatim so the numbers in §5 are re-derivable. Both read `frozen.json`.

`score.py` builds the per-arm column and the AUC table. `harness_run.py` routes the column
through `allo.scoring.score_arm`; it imports `allo`, so ADR 0034's review-tool exemption does
not reach it either way.

```python
# score.py -- per-arm conservation column and its AUC against the frozen label sets.
# REVIEW-SIDE PROBE. Opens `frozen.json`, so it stays in the scratchpad.
def auc(pos, neg):
    a = np.concatenate([pos, neg])
    order = np.argsort(a, kind="stable")
    r = np.empty(len(a))
    r[order] = np.arange(1, len(a) + 1)
    s = a[order]
    rr = r[order]
    i = 0
    while i < len(s):  # midranks for ties
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            rr[i : j + 1] = rr[i : j + 1].mean()
        i = j + 1
    r[order] = rr
    n1 = len(pos)
    return (r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * len(neg))


# per arm: candidates = residue_ids minus excluded_from_scoring, asserted against n_candidates;
# labels = scoreable_label_residues; author numbering mapped to UniProt through
# `_struct_ref_seq` (`pdbx_auth_seq_align_beg` against `db_align_beg`, one offset per block);
# a residue covered by two families takes max(values).
```

```python
# harness_run.py -- the same column through the frozen harness.
# `score_arm` requires a score for EVERY candidate. Uncovered residues are filled with the
# arm's own median JSD: label-blind, and the most conservative filler, because it places every
# uncovered residue in the middle of the ranking. THE RULE IS THIS PROBE'S, NOT ADR 0035's,
# which is the point of §6 item 1.
med = float(np.median(list(col.values())))
scores = {r: col.get(r, med) for r in cand}
result = score_arm(arm, scores, method="jsd_conservation")
```

---

## 8. What the report gains

One sentence it could not previously write, with a number behind it:

> Residue conservation, measured as Jensen-Shannon divergence over pinned Pfam 38.2 full
> alignments, does not separate the allosteric label residues from the background on this
> benchmark (median AUC-ROC 0.491 over eleven arms with adequate alignment coverage,
> Wilcoxon p = 0.76). The predicted sites are therefore not a restatement of sequence
> conservation.

Nothing in the literature reports a conservation-only baseline for allosteric site
prediction, so this number is new.
