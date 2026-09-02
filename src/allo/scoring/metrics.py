"""Ranking metrics and their chance lines.

Every metric here takes a residue-indexed score map and the frozen positive class, and
returns a number. Nothing in this module opens a file, knows a target, or holds a random
seed. That keeps it testable against hand-computed values, which is the only way to know
an estimator is the one it claims to be.

Two things move an AUC without any protocol appearing to change -- the estimator and the
tie rule -- so both are fixed here and stated in the docstrings rather than left to a
library default (`docs/benchmark/evaluation/README.md` section 3).
"""

from __future__ import annotations

import numpy as np
from scipy.stats import hypergeom, rankdata

__all__ = [
    "auc_pr",
    "auc_roc",
    "chance_dcc",
    "dcc",
    "expected_precision_at_k",
    "p_at_least_one_hit",
    "precision_at_k",
    "rank_vector",
]


def rank_vector(scores: np.ndarray) -> np.ndarray:
    """Midrank of every score, largest score getting the largest rank.

    Midrank is what makes `U / (n_pos * n_neg) == auc_roc` exact under ties. A method that
    emits coarse or integer-valued scores would otherwise be ranked by array order.
    """
    return rankdata(scores, method="average")


def auc_roc(scores: np.ndarray, positive: np.ndarray) -> float:
    """Rank-based Mann-Whitney AUC-ROC, midrank ties.

    Reported because it is the near-universal metric in this literature (PocketMiner
    doi:10.1038/s41467-023-36699-3, CryptoBench doi:10.1093/bioinformatics/btae745), and
    because it is prevalence-invariant, which the 6.79x prevalence span across the frozen
    arms makes necessary to state beside AUC-PR rather than instead of it.
    """
    n_pos = int(positive.sum())
    n_neg = int(len(scores) - n_pos)
    if n_pos == 0 or n_neg == 0:
        raise ValueError("AUC-ROC needs both classes present")
    ranks = rank_vector(scores)
    u = ranks[positive].sum() - n_pos * (n_pos + 1) / 2
    return float(u / (n_pos * n_neg))


def auc_pr(scores: np.ndarray, positive: np.ndarray) -> float:
    """Average precision by the step estimator: AP = sum_i (R_i - R_{i-1}) * P_i.

    Thresholds are the distinct score values, so no within-tie ordering is ever used. This
    is the scikit-learn convention and it never interpolates between operating points a
    method did not produce.

    **It is biased upward at this prevalence, and so is the trapezoid.** Neither estimator
    removes that bias; a common estimator across methods is what makes the comparison fair.
    Do not read a bare AP as an unbiased population value.
    """
    n_pos = int(positive.sum())
    if n_pos == 0:
        raise ValueError("AUC-PR needs at least one positive")
    order = np.argsort(-scores, kind="stable")
    ranked = positive[order]
    tp = np.cumsum(ranked)
    fp = np.cumsum(~ranked)
    # Keep only the last index of each run of equal scores: one operating point per
    # distinct threshold, which is what the tie rule above means operationally.
    distinct = np.r_[np.diff(scores[order]) != 0, True]
    tp, fp = tp[distinct], fp[distinct]
    precision = tp / (tp + fp)
    recall = tp / n_pos
    return float((np.diff(np.r_[0.0, recall]) * precision).sum())


def precision_at_k(scores: np.ndarray, positive: np.ndarray, k: int) -> float:
    """Fraction of the top `k` that is positive, ties broken pessimistically.

    The scored artifact of this challenge is a top-5 residue list (`CHALLENGE.md` section
    5), so this is the metric closest to the deliverable. Pessimistic tie-breaking means a
    method cannot gain from emitting a plateau: where a tie straddles the cut, the
    positives inside it are counted last.
    """
    if k <= 0 or k > len(scores):
        raise ValueError(f"k={k} is outside 1..{len(scores)}")
    # Sort negatives ahead of positives within a tie, then take the first k.
    order = np.lexsort((positive, -scores))
    return float(positive[order][:k].sum() / k)


def expected_precision_at_k(n_positive: int, n_candidates: int, k: int) -> float:
    """Chance precision@k for a uniformly random ranking. Exactly `n_positive / n`."""
    return float(hypergeom.mean(n_candidates, n_positive, k) / k)


def p_at_least_one_hit(n_positive: int, n_candidates: int, k: int) -> float:
    """Exact hypergeometric P(at least one positive in a random top-`k`).

    The bar a top-5 list has to clear before it means anything. Computed from the frozen
    candidate-set size, never from the node count: `n_residues` is what a method receives
    and `n_candidates` is what it is scored against (ADR 0011).
    """
    return float(hypergeom.sf(0, n_candidates, n_positive, k))


def top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """The `k` rows a method's list holds. Ties break by candidate order, never by label.

    This is the deliverable itself, not a metric about it: `CHALLENGE.md` section 5 asks for
    a top-5 residue list, and `top_k_components` and `dcc` both describe that list. Until
    2026-09-02 the tie rule here was the pessimistic one `precision_at_k` uses, which sorts
    negatives ahead of positives inside a tie. That is right for a metric, where it stops a
    method gaining from a plateau, and wrong for an artifact: it made the residues a reader
    is handed a function of the answer key, which is what C1 forbids. `precision_at_k` and
    `recall_at_k` keep the pessimistic rule and do not come through here.
    """
    if k <= 0 or k > len(scores):
        raise ValueError(f"k={k} is outside 1..{len(scores)}")
    return np.argsort(-scores, kind="stable")[:k]


def dcc(coordinates: np.ndarray, chosen: np.ndarray, labels: np.ndarray) -> float:
    """Distance in angstrom between the centre of the predicted list and the centre of the site.

    The one published criterion purpose-built for the artifact this challenge scores: a
    residue list, not a pocket. STINGAllo (doi:10.1093/bib/bbaf424) is the single allosteric
    use; the measure is ubiquitous in ligand-site prediction, where "DCC" means centre to
    centre and "DCA" means centre to the nearest ligand heavy atom. The two names are swapped
    in some papers, P2Rank among them, so the definition is written out here rather than
    named (`docs/benchmark/evidence/evaluation-metrics.md` section 2.2).

    **Reported as a distance, never as a success rate, and that is deliberate.** The usual
    threshold is 4 A, from doi:10.1023/A:1008124202956. LIGYSIS-bench measured that threshold
    and rejected it for centre-to-centre use: "a DCC threshold of 4 A is too conservative, and
    a more flexible DCC threshold of 10-12 A should be used for comparable performance with
    DCA = 4 A". Freezing either number would take a side in a live disagreement, so the
    continuous distance is frozen and both conventions are printed beside it.
    """
    return float(np.linalg.norm(coordinates[chosen].mean(0) - coordinates[labels].mean(0)))


def chance_dcc(
    coordinates: np.ndarray, labels: np.ndarray, k: int, *, draws: int = 10000, seed: int = 0
) -> float:
    """Median DCC of a uniformly random `k`-residue list. The chance line for `dcc`.

    Every other top-k number in this protocol prints against an exact hypergeometric chance
    line. A distance has no closed form here, because it depends on where the label centroid
    sits inside the candidate cloud, so the chance line is a seeded Monte Carlo median frozen
    per arm. The median rather than the mean, because the null distribution of a distance is
    skewed.
    """
    rng = np.random.default_rng(seed)
    centre = coordinates[labels].mean(0)
    picks = rng.random((draws, len(coordinates))).argpartition(k, axis=1)[:, :k]
    return float(np.median(np.linalg.norm(coordinates[picks].mean(1) - centre, axis=1)))
