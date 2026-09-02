"""How much of the sweep's best variant is selection, and what can four arms resolve?

Three passes, all reading `config.yaml` beside this file:

1. `null_auc` -- score B label-blind spatially autocorrelated fields through the frozen
   harness on each arm, and keep the AUC. This is the distribution a method that knows
   nothing about the site, but has the spatial structure every real method has, draws from.
2. `effective_dimension` -- the participation ratio of the eigenvalue spectrum of the
   variant-by-variant Spearman correlation matrix. It converts "we screened 792 variants"
   into "we screened this many independent things".
3. `detectable_effect` -- the frozen calibration module's own sensitivity pass, run on the
   four `development` arms, which the committed calibration only ran on the primary five.

Writes `metrics.json`. Nothing here can change a frozen value.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml
from scipy.stats import rankdata

from allo import network
from allo.classical import SCORERS as CLASSICAL
from allo.classical import postprocess
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.scoring.calibration import detectable_effect
from allo.scoring.harness import protocol, score_arm
from allo.scoring.nulls import evaluation_graph, field_factor, smooth_field

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
GRAPHS = yaml.safe_load((HERE.parent / "2026-08-26-method-sweep" / "config.yaml").read_text())


def null_auc(arm: str) -> dict:
    """AUC of `fields_per_scale` label-blind smooth fields per correlation length."""
    apo = apo_input(arm)
    graph = evaluation_graph(apo)
    coords = graph.ca_coord[graph.index(graph.candidates)]
    settings = protocol()
    out: dict[str, list[float]] = {}
    for length_scale in CONFIG["length_scales"]:
        rng = np.random.default_rng(int(CONFIG["seed"]) + int(length_scale))
        factor = field_factor(coords, float(length_scale))
        values = []
        for _ in range(int(CONFIG["fields_per_scale"])):
            field = smooth_field(factor, rng)
            scores = dict(zip(graph.candidates, field.tolist(), strict=True))
            scores |= dict.fromkeys(graph.source, 0.0)
            record = score_arm(arm, scores, method="null_field", config=settings)
            values.append(record["endpoints"]["auc_roc"])
        out[str(length_scale)] = values
        print(f"  {arm} lambda={length_scale}: median {np.median(values):.4f}", flush=True)
    return out


def _screen_columns(arm: str) -> dict[tuple[str, str, str], np.ndarray]:
    """Every (graph, scorer, detrend) score vector the method sweep produces, for one arm.

    The sweep's own config supplies the axes, so this measures the screen that actually ran
    rather than a subset of it. The first pass measured 150 variants and scaled the ratio
    linearly to the full sweep; that extrapolation was wrong by an order of magnitude,
    because added variants are mostly copies of directions already present.
    """
    apo = apo_input(arm)
    distance = network.min_heavy_distance_to(apo, apo.active_site)
    columns: dict[tuple[str, str, str], np.ndarray] = {}
    for graph_name in GRAPHS["graphs"]:
        knobs = dict(GRAPHS["graphs"][graph_name])
        kwargs = {
            "contact": knobs["contact"],
            "cutoff": float(knobs["cutoff"]),
            "weighting": knobs["weighting"],
        }
        if "decay_length" in knobs:
            kwargs["decay_length"] = float(knobs["decay_length"])
        if knobs["weighting"] == "edge_class":
            kwargs["class_weights"] = dict(GRAPHS["edge_class_weights"])
        graph = network.build(apo, **kwargs)
        order = list(graph.order)
        extra = GRAPHS["detrend_extra"] if graph_name in GRAPHS["detrend_extra_graphs"] else []
        for scorer_name, scorer in (CLASSICAL | QUANTUM).items():
            params = dict(GRAPHS["scorer_params"].get(scorer_name, {}))
            try:
                raw = graph.as_scores(scorer(graph, **params))
            except (MemoryError, ArithmeticError):
                continue
            for mode in list(GRAPHS["detrend"]) + list(extra):
                if mode == "raw":
                    scores = raw
                else:
                    bins = (
                        float(GRAPHS["gaussian_bandwidth"])
                        if mode == "gaussian_kernel"
                        else int(GRAPHS["binned_rank_bins"])
                    )
                    scores, _ = postprocess.decay_residual(
                        raw, distance, apo.active_site, form=mode, bins=bins
                    )
                columns[graph_name, scorer_name, mode] = np.asarray(
                    [scores[key] for key in order], dtype=float
                )
    return columns


def _participation(columns: dict, keys: list) -> dict:
    """Participation ratio of the rank-correlation spectrum over `keys`."""
    matrix = np.stack([_rank(columns[key]) for key in keys])
    correlation = np.nan_to_num(np.corrcoef(matrix), nan=0.0)
    eigenvalues = np.clip(np.linalg.eigvalsh(correlation), 0.0, None)
    participation = float(eigenvalues.sum() ** 2 / np.maximum((eigenvalues**2).sum(), 1e-12))
    return {
        "n_variants": len(keys),
        "effective_independent_variants": round(participation, 2),
        "fraction_independent": round(participation / len(keys), 4),
        "top_eigenvalue_share": round(float(eigenvalues.max() / eigenvalues.sum()), 4),
        "median_absolute_pairwise_rho": round(
            float(np.median(np.abs(correlation[np.triu_indices(len(keys), 1)]))), 4
        ),
    }


def effective_dimension() -> dict:
    """Participation ratio over the whole screen, plus which axis buys a direction."""
    spec = CONFIG["effective_dimension"]
    zero, control, probe = spec["zero_graph"], spec["control_detrend"], spec["probe_scorer"]
    out: dict[str, dict] = {"per_arm": {}}
    for arm in spec["arms"]:
        columns = _screen_columns(arm)
        keys = sorted(columns)
        out["per_arm"][arm] = _participation(columns, keys)
        if arm != spec["arms"][0]:
            continue
        out["axis_slices"] = {
            "scorers_only": _participation(
                columns, [k for k in keys if k[0] == zero and k[2] == control]
            ),
            "plus_graph_axis": _participation(columns, [k for k in keys if k[2] == control]),
            "plus_detrend_axis": _participation(columns, [k for k in keys if k[0] == zero]),
            "everything": out["per_arm"][arm],
            "one_scorer_all_cells": _participation(columns, [k for k in keys if k[1] == probe]),
        }
        out["axis_slices_arm"] = arm
    return out


def _rank(values: np.ndarray) -> np.ndarray:
    """Midranks, not ordinal ranks. Several scorers tie heavily -- `degree`, `core_number`,
    `hop_distance_from_source_negated` -- and `argsort(argsort(...))` breaks those ties by
    array position, which makes the correlation depend on residue order and overstates how
    independent two scorers are. Spearman is defined on midranks."""
    return rankdata(values).astype(float)


def selection_ceiling(per_arm: dict) -> dict:
    """The mean-across-arms AUC a null method reaches when the best of V variants is kept.

    Variants are drawn independently across arms, which is the conservative direction: real
    variants are correlated across arms, so a real screen's maximum is if anything larger.
    """
    rng = np.random.default_rng(int(CONFIG["seed"]) + 777)
    pooled = {arm: np.concatenate(list(scales.values())) for arm, scales in per_arm.items()}
    arms = sorted(pooled)
    draws = 20000
    means = np.zeros((draws, max(CONFIG["variant_counts"])))
    for column in range(means.shape[1]):
        means[:, column] = np.mean([rng.choice(pooled[arm], size=draws) for arm in arms], axis=0)
    out = {}
    for count in CONFIG["variant_counts"]:
        best = means[:, :count].max(axis=1)
        out[str(count)] = {
            "median": round(float(np.median(best)), 4),
            "p95": round(float(np.quantile(best, 0.95)), 4),
            "max": round(float(best.max()), 4),
        }
    return out


def main() -> int:
    started = time.time()
    per_arm = {}
    for arm in CONFIG["arms"]:
        per_arm[arm] = null_auc(arm)

    summary = {
        "config": CONFIG,
        "null_auc": {
            arm: {
                "by_length_scale": {
                    scale: {
                        "median": round(float(np.median(values)), 4),
                        "p95": round(float(np.quantile(values, 0.95)), 4),
                        "p99": round(float(np.quantile(values, 0.99)), 4),
                        "max": round(float(np.max(values)), 4),
                    }
                    for scale, values in scales.items()
                },
                "pooled": {
                    "median": round(float(np.median(np.concatenate(list(scales.values())))), 4),
                    "p95": round(
                        float(np.quantile(np.concatenate(list(scales.values())), 0.95)), 4
                    ),
                    "p99": round(
                        float(np.quantile(np.concatenate(list(scales.values())), 0.99)), 4
                    ),
                },
            }
            for arm, scales in per_arm.items()
        },
        "selection_ceiling": selection_ceiling(per_arm),
    }
    print(f"null pass done at {time.time() - started:.0f}s", flush=True)

    summary["effective_dimension"] = effective_dimension()
    print(f"dimension pass done at {time.time() - started:.0f}s", flush=True)

    spec = CONFIG["detectable_effect"]
    summary["detectable_effect"] = {}
    for arm in CONFIG["arms"]:
        summary["detectable_effect"][arm] = detectable_effect(
            arm,
            tolerance=float(spec["tolerance"]),
            length_scales=CONFIG["length_scales"],
            alpha=0.05 / int(spec["family_size"]),
            power=float(spec["power"]),
            replicates=int(spec["replicates"]),
            n_fields=int(spec["n_fields"]),
            seed=int(CONFIG["seed"]),
        )
        print(f"  mde {arm} done at {time.time() - started:.0f}s", flush=True)

    (HERE / "metrics.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    print(f"total {time.time() - started:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
