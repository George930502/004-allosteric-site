"""Calibrating the matched-patch null, and the gate that says whether it may be used.

A null that rejects nothing passes a type-I band perfectly, so the gate has both ends:

1. **Type-I rate.** Draw a stochastic, site-uninformative, spatially autocorrelated score,
   test the true label patch against the matched-patch null, and repeat. The rejection
   rate must sit inside the exact central binomial interval at alpha. The field is
   site-uninformative by construction, so any rate above alpha is the test failing to hold
   its size, and any rate below it is the test throwing away power.
2. **Positive control.** A score built from the answer must reject on every arm. It is
   evaluation-side only and never touches the prediction path.

The unmatched background null is measured in the same loop, because the number that
justifies the whole matched construction is how badly the unmatched one fails.

**Disclosed limitation (ADR 0018).** Drawing a fresh patch pool per replicate is
prohibitive, so the pool is drawn once per arm and shared across the field draws. The
replicates are therefore conditionally independent given the pool, not independent, and
the binomial interval is a screen rather than a proof.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import binom, norm

from allo.groundtruth.manifest import read_manifest
from allo.inputs import apo_input
from allo.scoring.harness import _positives
from allo.scoring.metrics import rank_vector
from allo.scoring.nulls import (
    evaluation_graph,
    field_factor,
    matched_patches,
    permutation_p,
    smooth_field,
)

__all__ = [
    "binomial_band",
    "calibrate_arm",
    "detectable_effect",
    "run_calibration",
    "run_repairs",
]


def binomial_band(n: int, alpha: float = 0.05, coverage: float = 0.95) -> tuple[float, float]:
    """Exact central binomial prediction interval for a rejection rate at `alpha`.

    This is a *prediction* interval for the observed rate under a correctly sized test, not
    a confidence interval on it. A measured rate outside the band is evidence the test does
    not hold its size at this number of replicates.
    """
    tail = (1 - coverage) / 2
    lo = binom.ppf(tail, n, alpha) / n
    hi = binom.ppf(1 - tail, n, alpha) / n
    return float(lo), float(hi)


def calibrate_arm(
    target: str,
    *,
    tolerance: float,
    length_scales,
    alpha: float = 0.05,
    family_size: int = 3,
    replicates: int = 9999,
    n_fields: int = 1000,
    seed: int = 0,
    match_distance: bool = False,
    with_background: bool = True,
) -> dict:
    """Measure both ends of the gate on one frozen arm.

    Returns per-length-scale type-I rates for the matched-patch null and for the unmatched
    background null, the positive control's p-value, and `size_ratio` -- the one number the
    scoring path uses.

    `family_size` is the size of the confirmatory family, so `alpha/family_size ... alpha`
    are every threshold Holm can put to this arm. The ratio is calibrated at all of them,
    not only at `alpha`, because a one-parameter rescale fitted at one threshold is wrong at
    the others (ADR 0025).

    `with_background` exists because the unmatched null does not depend on `tolerance`, so
    measuring it once per tolerance repeats identical work. The tolerance sweep turns it
    off; the gate leaves it on. The two nulls draw from separate generators, so the field
    sequence is the same either way.
    """
    graph = evaluation_graph(apo_input(target))
    labels, _ = _positives(target)
    label_mask = np.array([r in set(labels) for r in graph.candidates], dtype=bool)

    # The cached pool, deliberately: the gate has to calibrate the pool that scoring will
    # actually use, not an independently drawn one.
    patches, diagnostics = matched_patches(
        graph,
        labels,
        n_patches=replicates,
        tolerance=tolerance,
        seed=seed,
        match_distance=match_distance,
    )
    candidate_patches = patches[:, graph.index(graph.candidates)].astype(np.float32)
    patch_sizes = candidate_patches.sum(1)

    # Ca coordinates restricted to the candidate set, so the field and the ranking share
    # one ordering.
    candidate_index = graph.index(graph.candidates)
    coords = graph.ca_coord[candidate_index]

    # The background null needs far fewer replicates than the matched one: it is being
    # measured for disclosure, not used for a decision, and 999 resolves a rate near 0.17
    # to about +/- 0.01.
    replicates_background = 999

    def p_values(scores: np.ndarray, rng: np.random.Generator | None) -> tuple[float, float]:
        ranks = rank_vector(scores).astype(np.float32)
        observed = float(ranks[label_mask].mean())
        matched = permutation_p(observed, (candidate_patches @ ranks) / patch_sizes)
        if rng is None:
            return matched, float("nan")
        # A uniform draw without replacement, vectorised: partition random keys and keep
        # the m smallest. One argpartition replaces m Python-level permutations.
        keys = rng.random((replicates_background, len(ranks)))
        drawn = np.argpartition(keys, len(labels), axis=1)[:, : len(labels)]
        return matched, permutation_p(observed, ranks[drawn].mean(1))

    # Every level Holm can test this arm at, tightest first.
    levels = [alpha / k for k in range(family_size, 0, -1)]

    rates = {}
    thresholds, ratios = [], []
    for length_scale in length_scales:
        field_rng = np.random.default_rng(seed + 1)
        null_rng = np.random.default_rng(seed + 11) if with_background else None
        factor = field_factor(coords, float(length_scale))
        matched_p, background_hits = [], 0
        for _ in range(n_fields):
            matched, background = p_values(smooth_field(factor, field_rng), null_rng)
            matched_p.append(matched)
            background_hits += background <= alpha
        # The nominal threshold whose measured size is alpha, at this correlation length.
        matched_p = np.asarray(matched_p)
        threshold = float(np.quantile(matched_p, alpha))
        thresholds.append(threshold)
        # The rescale is conservative at level `t` exactly when r >= z(q_t) / z(t), where
        # `q_t` is the raw p whose measured size is `t`. Capping `q_t` at `t` is the
        # "may tighten, may never loosen" rule, and it makes r >= 1 by construction.
        step_ratio = {}
        for level in levels:
            q = float(np.quantile(matched_p, level))
            step_ratio[round(level, 5)] = round(float(norm.isf(min(q, level)) / norm.isf(level)), 4)
        ratios.extend(step_ratio.values())
        rates[str(length_scale)] = {
            "matched_patch": round(float(np.mean(matched_p <= alpha)), 4),
            "alpha_star": round(threshold, 5),
            "step_ratio": step_ratio,
        }
        if with_background:
            rates[str(length_scale)]["background_residues"] = round(background_hits / n_fields, 4)

    # Positive control: minus the distance to the nearest label. Evaluation-side only.
    label_coords = coords[label_mask]
    oracle = -np.linalg.norm(coords[:, None, :] - label_coords[None, :, :], axis=-1).min(axis=1)
    oracle_matched, oracle_background = p_values(oracle, np.random.default_rng(seed + 2))

    return {
        "target": target,
        # The size-calibrated threshold. Two deliberate one-sided choices, both toward a
        # smaller test: the minimum across correlation lengths, and a cap at the nominal
        # alpha. Calibration may tighten a test and may never loosen one, so an arm whose
        # measured size is already below alpha keeps the nominal threshold rather than
        # buying power back.
        "alpha_star": round(min(min(thresholds), alpha), 5),
        # What `score_arm` actually uses. The maximum over correlation lengths AND over
        # Holm levels, so the calibrated test's size is at or below nominal at every
        # threshold the decision rule can present. Taking a maximum over noisy quantiles
        # biases it upward, which costs power and never costs size. ADR 0025.
        "size_ratio": round(max(ratios), 4),
        "family_size": family_size,
        "tolerance": tolerance,
        "match_distance": match_distance,
        "n_fields": n_fields,
        "replicates": replicates,
        "alpha": alpha,
        "type_one_rate": rates,
        "positive_control": {
            "score": "minus distance to nearest scoreable label",
            "matched_patch_p": oracle_matched,
            "background_residues_p": oracle_background,
        },
        "sampler": diagnostics,
    }


def detectable_effect(
    target: str,
    *,
    tolerance: float,
    length_scales,
    alpha: float = 0.05,
    power: float = 0.80,
    replicates: int = 9999,
    n_fields: int = 300,
    seed: int = 0,
    bisection_steps: int = 8,
    max_shift: float = 3.0,
) -> dict:
    """The smallest effect the confirmatory test detects at `power`, on this arm.

    **This is an a priori sensitivity analysis of the procedure that will actually run, not
    a formula.** The two closed-form columns the earlier draft carried were withdrawn: the
    rank-sum formula counts a contiguous label patch as 12-20 independent observations, and
    under the spatially autocorrelated null it does not hold its size, so a power number
    from it is not a power number. Simulating the real test removes the need to estimate an
    effective sample size at all -- which is the right move, because that quantity is a
    joint property of the label geometry and the *method's* correlation length, so no single
    value could be pinned in advance.

    `alpha` is the arm's **calibrated** threshold, not the nominal one. A sensitivity quoted
    at a threshold the procedure does not use is not the procedure's sensitivity.

    Data-generating model for the alternative: the same site-uninformative field as the
    type-I gate, plus a constant shift on the label residues. The field has unit marginal
    variance, so the shift is in standard-deviation units and reads as Cohen's d. The
    reported AUC is the median AUC-ROC actually achieved at that shift, which is the number
    a reader can compare against a published one.
    """
    graph = evaluation_graph(apo_input(target))
    labels, _ = _positives(target)
    label_mask = np.array([r in set(labels) for r in graph.candidates], dtype=bool)
    patches, _ = matched_patches(
        graph, labels, n_patches=replicates, tolerance=tolerance, seed=seed
    )
    candidate_index = graph.index(graph.candidates)
    candidate_patches = patches[:, candidate_index].astype(np.float32)
    patch_sizes = candidate_patches.sum(1)
    coords = graph.ca_coord[candidate_index]
    n_pos = int(label_mask.sum())
    n_neg = int(len(label_mask) - n_pos)

    results = {}
    for length_scale in length_scales:
        factor = field_factor(coords, float(length_scale))

        def measure(shift: float, factor=factor) -> tuple[float, float]:
            rng = np.random.default_rng(seed + 3)
            rejected, aucs = 0, []
            for _ in range(n_fields):
                scores = smooth_field(factor, rng) + shift * label_mask
                ranks = rank_vector(scores).astype(np.float32)
                observed = float(ranks[label_mask].mean())
                p = permutation_p(observed, (candidate_patches @ ranks) / patch_sizes)
                rejected += p <= alpha
                aucs.append((ranks[label_mask].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))
            return rejected / n_fields, float(np.median(aucs))

        low, high = 0.0, max_shift
        achieved = measure(high, factor)
        if achieved[0] < power:
            results[str(length_scale)] = {
                "shift": None,
                "auc_roc": None,
                "note": f"power {achieved[0]:.3f} at the largest shift tried ({max_shift})",
            }
            continue
        for _ in range(bisection_steps):
            middle = (low + high) / 2
            if measure(middle, factor)[0] >= power:
                high = middle
            else:
                low = middle
        final = measure(high, factor)
        results[str(length_scale)] = {
            "shift": round(high, 4),
            "power_at_shift": round(final[0], 4),
            "auc_roc": round(final[1], 4),
        }
    return {
        "target": target,
        "alpha": alpha,
        "power": power,
        "n_fields": n_fields,
        "by_length_scale": results,
    }


def run_calibration(config_path: Path) -> int:
    """Run one calibration experiment from its config and write `metrics.json` beside it.

    The command that makes the experiment reproducible: `allo evaluate calibrate <config>`.
    Two stages, and they answer different questions.

    * **search** -- sweep the tolerance at a reduced replicate count to find the value at
      which the test holds its size. This is where the tolerance is *chosen*.
    * **gate** -- run the chosen tolerance at the replicate count scoring actually uses,
      and check both ends: the type-I band and the positive control. This is where the
      tolerance is *verified*.

    Splitting them matters because a tolerance picked at one replicate count and used at
    another has not been calibrated for the procedure that will run.
    """
    config = read_manifest(config_path)
    common = {
        "length_scales": config["length_scales"],
        "alpha": float(config["alpha"]),
        "family_size": int(config["holm_family_size"]),
        "n_fields": int(config["n_fields"]),
        "seed": int(config["seed"]),
    }
    results: dict = {"config": config, "search": {}, "gate": {}}
    for tolerance in config["search"]["tolerances"]:
        results["search"][str(tolerance)] = {
            target: calibrate_arm(
                target,
                tolerance=float(tolerance),
                replicates=int(config["search"]["replicates"]),
                # The unmatched null does not depend on the tolerance. Measure it in the
                # gate, once, rather than three times here.
                with_background=False,
                **common,
            )
            for target in config["targets"]
        }
        print(f"search: tolerance {tolerance} done")
    for target in config["gate"].get("targets", config["targets"]):
        results["gate"][target] = calibrate_arm(
            target,
            tolerance=float(config["gate"]["tolerance"]),
            replicates=int(config["gate"]["replicates"]),
            **common,
        )
        print(f"gate: {target} done")
    if "power" in config:
        results["power"] = {}
        family = int(config["holm_family_size"])
        # Every level Holm can present, not only alpha. Quoting the sensitivity at alpha
        # understates what an arm tested at alpha/3 has to achieve, and the arm that Holm
        # tests at the tightest step is not knowable in advance.
        levels = {
            f"alpha/{k}" if k > 1 else "alpha": float(config["alpha"]) / k
            for k in range(1, family + 1)
        }
        for target in config["targets"]:
            ratio = float(results["gate"][target]["size_ratio"])
            results["power"][target] = {}
            for label, level in levels.items():
                results["power"][target][label] = detectable_effect(
                    target,
                    tolerance=float(config["gate"]["tolerance"]),
                    length_scales=config["length_scales"],
                    # The calibrated threshold, not the nominal one. The published
                    # sensitivity has to be the sensitivity of the test that will run.
                    alpha=float(norm.sf(ratio * norm.isf(level))),
                    power=float(config["power"]["target_power"]),
                    replicates=int(config["gate"]["replicates"]),
                    n_fields=int(config["power"]["n_fields"]),
                    seed=common["seed"],
                )
                print(f"power: {target} at {label} done")
    results["binomial_band"] = list(binomial_band(common["n_fields"], common["alpha"]))
    # default=str: the config carries a YAML date, which json cannot encode.
    (config_path.parent / "metrics.json").write_text(
        json.dumps(results, indent=2, default=str) + "\n"
    )
    return 0


# ---------------------------------------------------------------------------------------
# Repairs to the matching, and a test of the explanation (ADR 0025).
#
# Lives here rather than in the experiment directory because `experiments/` is scanned by the
# runner leakage gate and this code calls `_positives`. The calibration experiment uses the
# same split: code in the package, config and metrics beside the notes.
# ---------------------------------------------------------------------------------------


def variance_factor(members: np.ndarray, coords: np.ndarray, length_scale: float) -> np.ndarray:
    """`m^-2 sum_ij exp(-d_ij / lambda)` for each patch. The variance of its mean rank."""
    kernel = np.exp(
        -np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1) / length_scale
    )
    return np.einsum("pi,ij,pj->p", members, kernel, members) / members.sum(1) ** 2


def pairwise_ecdf(members: np.ndarray, coords: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Within-patch pairwise-distance ECDF on a fixed grid, one row per patch."""
    out = np.empty((len(members), len(grid)))
    for i, row in enumerate(members):
        picked = coords[row.astype(bool)]
        d = np.linalg.norm(picked[:, None, :] - picked[None, :, :], axis=-1)
        d = d[np.triu_indices(len(picked), 1)]
        out[i] = np.searchsorted(np.sort(d), grid, side="right") / len(d)
    return out


def run_repairs(config_path: Path) -> int:
    """Measure two further repairs, and test whether the variance-factor percentile is causal.

    ADR 0023 explains the null's residual by the percentile of the observed patch's variance
    factor inside its own pool. Both repairs below move that percentile on purpose, so the
    explanation becomes measurable rather than arguable. It does not survive: see
    `experiments/2026-08-25-null-repairs/notes.md` and ADR 0025.

    Both repairs post-stratify the cached pool and keep the closest half. Neither redraws at
    full size, so the surviving pool is less diverse. That bounds the conclusion about the
    repairs and not the conclusion about the percentile, which is a within-pool comparison.
    """
    config = read_manifest(config_path)
    alpha = float(config["alpha"])
    n_fields = int(config["n_fields"])
    seed = int(config["seed"])
    keep = float(config["keep_fraction"])
    length_scales = [float(value) for value in config["length_scales"]]

    results = {}
    for target in config["arms"]:
        graph = evaluation_graph(apo_input(target))
        labels, _ = _positives(target)
        label_mask = np.array([r in set(labels) for r in graph.candidates], dtype=bool)
        observed_patch = label_mask.astype(np.float32)
        coords = graph.ca_coord[graph.index(graph.candidates)]
        patches, _ = matched_patches(
            graph,
            labels,
            n_patches=int(config["pool_replicates"]),
            tolerance=float(config["tolerance"]),
            seed=seed,
        )
        members = patches[:, graph.index(graph.candidates)].astype(np.float32)
        sizes = members.sum(1)

        def gyration(row, coords=coords):
            picked = coords[row.astype(bool)]
            return float(np.sqrt(((picked - picked.mean(0)) ** 2).sum(1).mean()))

        pool_gyration = np.array([gyration(row) for row in members])
        observed_gyration = gyration(observed_patch)

        # Repair C -- centre the acceptance window on the observed radius of gyration. The
        # frozen window is a relative bound, so it is not symmetric about the observed value.
        keep_c = np.argsort(np.abs(pool_gyration - observed_gyration))[: int(keep * len(members))]

        # Repair D -- match the whole within-patch pairwise-distance distribution rather than
        # its second moment. L1 on the ECDF is the Wasserstein distance between the two.
        grid = np.linspace(0.0, float(np.linalg.norm(np.ptp(coords, axis=0))), 60)
        observed_ecdf = pairwise_ecdf(observed_patch[None, :], coords, grid)[0]
        pool_ecdf = pairwise_ecdf(members, coords, grid)
        keep_d = np.argsort(np.abs(pool_ecdf - observed_ecdf).sum(1))[: int(keep * len(members))]

        arm = {"observed_radius_of_gyration": round(observed_gyration, 4), "by_length_scale": {}}
        for length_scale in length_scales:
            rng = np.random.default_rng(seed + 1)
            factor = field_factor(coords, length_scale)
            ranks = [
                rank_vector(smooth_field(factor, rng)).astype(np.float32) for _ in range(n_fields)
            ]
            observed_factor = float(
                variance_factor(observed_patch[None, :], coords, length_scale)[0]
            )

            def measure(
                index,
                ranks=ranks,
                members=members,
                sizes=sizes,
                coords=coords,
                length_scale=length_scale,
                observed_factor=observed_factor,
                label_mask=label_mask,
            ):
                pool, weights = members[index], sizes[index]
                hits = sum(
                    permutation_p(float(r[label_mask].mean()), (pool @ r) / weights) <= alpha
                    for r in ranks
                )
                factors = variance_factor(pool, coords, length_scale)
                return {
                    "type_one": hits / len(ranks),
                    "variance_factor_percentile": round(
                        100.0 * float((factors < observed_factor).mean()), 1
                    ),
                }

            arm["by_length_scale"][str(length_scale)] = {
                "frozen": measure(np.arange(len(members))),
                "repair_c_centred_gyration": measure(keep_c),
                "repair_d_matched_distance_ecdf": measure(keep_d),
            }
            print(f"repairs: {target} lambda {length_scale} done")
        results[target] = arm

    (config_path.parent / "metrics.json").write_text(
        json.dumps({"config": config, "arms": results}, indent=2, default=str) + "\n"
    )
    return 0
