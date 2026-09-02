"""Stages S6 and S7: remove the distance confound, then assemble the top-5 list.

`docs/method/review/11-pipeline-decomposition.md` calls S6 "the single most valuable open
experiment in the review" and S7 the stage that decides the deliverable. Both are classical,
both are cheap, and neither had been implemented. This module implements both to the spec
that file gives, including the parts it wrote out because prose was not implementable.

**S6 — the decay residual.** Five independent routes agree that the ground truth decays
exponentially with distance from the active site, and that real sites decay *more slowly*
than background. If that holds, the right estimator is not "beat distance": it is fit
`exp(-k d)` as the null and score the residual.

The C1 spec, verbatim from that file, and the reason each clause is there:

* **Fit universe** — `ApoInput.residues` minus `ApoInput.active_site`, derived from the apo
  input alone. Deliberately *not* the evaluation layer's candidate set. The two coincide on
  the current freeze, but that is a fact about this freeze and not an invariant (ADR 0011,
  amended), and naming the evaluation term here would couple the prediction path to the
  evaluation layer.
* **Rule** — `k` is always fitted, never quoted, and never carried between targets.
* **Test** — permute the labels, refit, and require `k` to be bit-identical. It is, by
  construction: no function in this module takes a label set as an argument. That is what
  makes the guarantee checkable rather than promised.

**S7 — site assembly.** Four routes converge on one failure: ranking improves while
localisation degrades. Five residues from one pocket is one prediction, not five, so the
top-5 is a set-selection problem rather than a cut through a ranked list.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "DECAY_FORMS",
    "consensus",
    "decay_residual",
    "diversified_top_k",
    "fit_decay",
    "midrank",
    "spatial_smoothing",
]

DECAY_FORMS = (
    "exponential",
    "linear",
    "binned_rank",
    "binned_median",
    "gaussian_kernel",
)
_EPSILON = 1e-12


def midrank(values: np.ndarray) -> np.ndarray:
    """Midranks of `values`, scaled to (0, 1].

    Every endpoint the evaluation layer computes is a rank statistic, so a monotone
    transform of a score is invisible to it. Working in midrank space therefore costs
    nothing and buys two things: the residual of a raw score and the residual of its
    logarithm become the same object, and scores whose units differ by ten orders of
    magnitude become comparable in one regression.
    """
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="stable")
    ranks = np.empty(len(values), dtype=float)
    ranks[order] = np.arange(1, len(values) + 1, dtype=float)
    # Average the ranks inside each tie group, which is what "midrank" means and what the
    # confirmatory statistic in `allo.scoring` uses.
    unique, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    totals = np.zeros(len(unique))
    np.add.at(totals, inverse, ranks)
    return (totals / counts)[inverse] / len(values)


def fit_decay(
    values: np.ndarray,
    distance: np.ndarray,
    *,
    form: str = "exponential",
    bins: int = 8,
) -> dict:
    """Fit the distance trend of a score, label-free. Returns the fit and its parameters.

    `values` and `distance` cover the **fit universe** only — the caller removes the source
    before calling, and nothing here can see a label. `distance` is minimum heavy-atom
    distance to the source, which `allo.network.min_heavy_distance_to` computes and which
    file 06 identifies as the variable the biological law is exponential in.

    Three forms, because the spec names one and the other two bound it:

    * `exponential` — ordinary least squares of `log(midrank)` on distance. The form the
      review specifies. Working on the midrank rather than the raw score is what makes the
      logarithm defined for a score that goes negative, and it changes nothing the
      evaluation can see.
    * `linear` — least squares of the midrank on distance. The control that says how much of
      the residual is the exponential form and how much is any monotone detrending at all.
    * `binned_rank` — no functional form: subtract the bin mean within equal-count distance
      bins. Fully non-parametric, and the closest implementable form of the distance
      stratification the teammate's repository used to show that plain AUC is confounded.
    * `binned_median` — the same, with the bin median. The published treatment of this
      confound in the allostery literature is quantile regression rather than mean
      regression (Amor et al., doi:10.1038/ncomms12477), and a median is the one-quantile
      form of it. It resists the long upper tail every propagation score has.

    The returned `k` for the exponential form is the decay constant in inverse angstrom, so
    a half-distance is `log(2) / k`. It is reported for its own sake: file 06's claim that
    real sites decay more slowly than background is a claim about this number.
    """
    if form not in DECAY_FORMS:
        raise ValueError(f"unknown decay form {form!r}; have {DECAY_FORMS}")
    values = np.asarray(values, dtype=float)
    distance = np.asarray(distance, dtype=float)
    if values.shape != distance.shape:
        raise ValueError(f"shape mismatch: {values.shape} scores, {distance.shape} distances")
    ranked = midrank(values)

    if form in ("binned_rank", "binned_median"):
        centre = np.mean if form == "binned_rank" else np.median
        edges = np.quantile(distance, np.linspace(0.0, 1.0, bins + 1))
        edges[-1] = np.inf
        which = np.clip(np.searchsorted(edges, distance, side="right") - 1, 0, bins - 1)
        fitted = np.zeros_like(ranked)
        for b in range(bins):
            inside = which == b
            if inside.sum() > 1:
                fitted[inside] = centre(ranked[inside])
            elif inside.any():
                fitted[inside] = ranked[inside]
        return {
            "form": form,
            "bins": bins,
            "fitted": fitted,
            "residual": ranked - fitted,
            "k": None,
            "r_squared": _r_squared(ranked, fitted),
        }

    if form == "gaussian_kernel":
        # The distance-conditional z-score the teammate benchmark's best method uses. The
        # local mean and the local standard deviation are both Nadaraya-Watson estimates
        # with a Gaussian kernel in distance, so the residual is a local z-score rather than
        # a local mean subtraction. `bins` carries the bandwidth in angstrom, because the
        # caller has one knob for this stage and this form spends it here.
        bandwidth = float(bins)
        kernel = np.exp(-0.5 * ((distance[:, None] - distance[None, :]) / bandwidth) ** 2)
        mass = np.maximum(kernel.sum(axis=1), _EPSILON)
        local_mean = kernel @ ranked / mass
        local_variance = kernel @ (ranked**2) / mass - local_mean**2
        local_sd = np.sqrt(np.maximum(local_variance, _EPSILON))
        return {
            "form": form,
            "bandwidth_angstrom": bandwidth,
            "fitted": local_mean,
            "residual": (ranked - local_mean) / local_sd,
            "k": None,
            "r_squared": _r_squared(ranked, local_mean),
        }

    response = np.log(np.maximum(ranked, _EPSILON)) if form == "exponential" else ranked
    design = np.column_stack([np.ones_like(distance), distance])
    coefficients, *_ = np.linalg.lstsq(design, response, rcond=None)
    fitted_response = design @ coefficients
    return {
        "form": form,
        "intercept": float(coefficients[0]),
        "slope": float(coefficients[1]),
        # k is the decay constant of exp(-k d), so it is the negated slope of log y on d.
        "k": float(-coefficients[1]) if form == "exponential" else None,
        "half_distance_angstrom": (
            float(np.log(2.0) / -coefficients[1])
            if form == "exponential" and coefficients[1] < 0
            else None
        ),
        "fitted": fitted_response,
        "residual": response - fitted_response,
        "r_squared": _r_squared(response, fitted_response),
    }


def _r_squared(observed: np.ndarray, fitted: np.ndarray) -> float:
    total = float(((observed - observed.mean()) ** 2).sum())
    if total <= _EPSILON:
        return 0.0
    return float(1.0 - ((observed - fitted) ** 2).sum() / total)


def decay_residual(
    scores: dict[int, float],
    distance: dict[int, float],
    source,
    *,
    form: str = "exponential",
    bins: int = 8,
) -> tuple[dict[int, float], dict]:
    """Apply S6 to one method's scores. Returns the residual scores and the fit record.

    Source residues are removed from the fit universe and then handed back with the lowest
    residual in the set, so the returned mapping still covers every node the caller passed
    in. The evaluation ignores source scores in any case (ADR 0011); filling them rather
    than dropping them means the caller's key set is preserved and no downstream alignment
    has to special-case the source.
    """
    excluded = {int(r) for r in source}
    # Sorted, not in insertion order. The fit is a floating-point sum, so a caller that
    # builds its score mapping in a different order would otherwise get a `k` that differs
    # in the last two digits -- and "bit-identical under permutation" is the C1 guarantee
    # this stage is checked against.
    universe = sorted(r for r in scores if r not in excluded)
    if not universe:
        raise ValueError("fit universe is empty after removing the source")
    missing = [r for r in universe if r not in distance]
    if missing:
        raise ValueError(f"no distance for residues {missing}")

    values = np.array([scores[r] for r in universe], dtype=float)
    to_source = np.array([distance[r] for r in universe], dtype=float)
    fit = fit_decay(values, to_source, form=form, bins=bins)
    residual = fit.pop("residual")
    fit.pop("fitted", None)

    out = {r: float(v) for r, v in zip(universe, residual, strict=True)}
    floor = float(residual.min()) - 1.0
    for r in scores:
        out.setdefault(r, floor)
    fit["n_fit_universe"] = len(universe)
    return out, fit


def diversified_top_k(
    scores: dict[int, float],
    coord: dict[int, np.ndarray],
    *,
    k: int = 5,
    exclusion_radius: float = 0.0,
    exclude=(),
) -> list[int]:
    """Greedy top-k with a spatial exclusion radius (stage S7).

    Take the highest-scoring residue, remove every residue within `exclusion_radius` of it,
    and repeat. If the pool empties before k residues are chosen, fall back to the plain
    score order for the remainder, so the function always returns exactly k residues.

    The parameter is the radius, and it is a hyperparameter like any other: it is chosen on
    the secondary set's `development` tier and nowhere else. At radius 0 this reduces
    exactly to the plain score cut, which is the control the falsifier in
    `docs/method/review/11-pipeline-decomposition.md` §S7 asks for.

    **The default is 0, which is the control and not a choice.** An earlier default of 8.0
    was removed: the nearest documented number is the teammate benchmark's measured 8.2 A
    mean pairwise separation on its own held-out set, and ADR 0026 clause 2 names "a
    diversification radius" as forbidden from that source by default. Any non-zero radius
    must be passed in by a caller that swept it, which is
    `experiments/2026-08-26-fusion-probe` and nothing else.
    """
    excluded = {int(r) for r in exclude}
    pool = sorted((r for r in scores if r not in excluded), key=lambda r: -scores[r])
    chosen: list[int] = []
    blocked: set[int] = set()
    for residue in pool:
        if len(chosen) == k:
            break
        if residue in blocked:
            continue
        chosen.append(residue)
        if exclusion_radius > 0:
            here = np.asarray(coord[residue], dtype=float)
            for other in pool:
                if np.linalg.norm(np.asarray(coord[other], dtype=float) - here) <= exclusion_radius:
                    blocked.add(other)
    for residue in pool:
        if len(chosen) == k:
            break
        if residue not in chosen:
            chosen.append(residue)
    return chosen[:k]


def spatial_smoothing(
    scores: dict[int, float],
    coord: dict[int, np.ndarray],
    *,
    radius: float = 0.0,
) -> dict[int, float]:
    """Replace each residue's score by the mean over its spatial neighbourhood.

    The ground truth is a contiguous pocket lining, not a scattered residue set, so a score
    that is right about the region and noisy within it loses top-5 hits it should have won.
    Averaging inside a ball recovers them. The PPI hot-spot literature reaches the same
    construction from the other direction: hot spots cluster into cooperative "hot regions"
    that behave additively between clusters and cooperatively within one
    (Keskin et al., doi:10.1016/j.jmb.2004.10.077).

    At radius 0 this is the identity, which is the control the sweep needs, and it is the
    default. A stage default that is a tuned value would set a hyperparameter by import,
    which ADR 0021 forbids. The radius is swept in `experiments/2026-08-26-fusion-probe`.
    """
    residues = sorted(scores)
    points = np.array([np.asarray(coord[r], dtype=float) for r in residues])
    values = np.array([scores[r] for r in residues], dtype=float)
    if radius <= 0:
        return dict(scores)
    distance = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    inside = distance <= radius
    smoothed = (inside * values[None, :]).sum(axis=1) / inside.sum(axis=1)
    return {r: float(v) for r, v in zip(residues, smoothed, strict=True)}


def consensus(*score_maps: dict[int, float]) -> dict[int, float]:
    """Unsupervised rank average of several scores.

    Legal where a learned combiner is not: it fits nothing, so it needs no labels and burns
    no budget. It is also the combination the review's own evidence favours -- a trained
    combiner raised AUC while dropping top-5 hit rate, and top-5 is what is scored
    (`docs/method/review/11-pipeline-decomposition.md`, S7).

    Every input must cover the same residues, or the average would silently rank a residue
    against a different denominator in each column.
    """
    if not score_maps:
        raise ValueError("consensus needs at least one score map")
    residues = sorted(score_maps[0])
    for other in score_maps[1:]:
        if sorted(other) != residues:
            raise ValueError("consensus inputs cover different residue sets")
    total = np.zeros(len(residues))
    for column in score_maps:
        total += midrank(np.array([column[r] for r in residues], dtype=float))
    return {r: float(v / len(score_maps)) for r, v in zip(residues, total, strict=True)}
