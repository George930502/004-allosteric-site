# 0022 — The confirmatory endpoint is the mean midrank, not AUC-PR

**Status:** accepted · 2026-08-25

## Context

The Phase 1.6 draft protocol made **AUC-PR the tested endpoint**, with AUC-ROC beside it as
the effect size. The reasoning was prevalence: the frozen arms run from 1.6 % to 11.0 %
positives, and AUC-ROC is known to look flattering on imbalanced data. That reasoning is
correct about *reporting* and wrong about *testing*.

Three measurements decided it.

1. **AUC-PR is the noisier statistic.** In the one paper that reports both with dispersion,
   AUC-PR reads 0.44 ± 0.12 against AUC-ROC at 0.83 ± 0.04 — roughly three times the spread
   (PocketMiner, doi:10.1038/s41467-023-36699-3).
2. **This benchmark has little power to spare.** The label sets are contiguous patches of 12
   to 20 residues, so the effective sample size is far below the residue count. The
   simulated sensitivity analysis in `experiments/2026-08-25-null-calibration/` measures what
   the procedure can detect. A noisier endpoint detects less.
3. **Both AUC-PR estimators are biased upward at this prevalence**, and the step estimator is
   the more biased of the two. No estimator choice removes it.

## Decision

The confirmatory statistic is the **mean midrank of the scoreable label set**.

Every null in the protocol holds the positive-class size fixed. Under that condition the mean
midrank is a strictly increasing function of AUC-ROC, so the permutation p-value is identical
to one computed on AUC-ROC, and the effect size printed beside it is the metric this field
actually reports. AUC-ROC is the residue-level convention across at least eight independent
groups, including CryptoSite (doi:10.1016/j.jmb.2016.01.029), PocketMiner
(doi:10.1038/s41467-023-36699-3) and CryptoBench (doi:10.1093/bioinformatics/btae745).

**AUC-PR stays, as a reported endpoint that is never a decision.** It must always be printed
against its chance line, which is the prevalence. The reason to keep it is that AUC-ROC hides
the hard arms: on one dataset with one split, AllositePro reads AUROC 0.68 with AUPRC 0.07
while PASSerRank reads 0.82 and 0.46 (Allo-Allo, doi:10.1101/2024.09.28.615583). The two
columns reorder the methods, and a reader needs both.

## Consequences

The p-value no longer depends on an estimator choice that has no settled convention. The
tie rule is midrank, once, for every method.

**The bias in AUC-PR is disclosed rather than corrected.** The step estimator is kept because
it is the scikit-learn convention and because it never interpolates between thresholds a
method did not produce. The argument for it is a *common* estimator across methods, not an
unbiased one.

This ADR reverses a drafted choice, not a frozen one. Nothing was scored under it.
