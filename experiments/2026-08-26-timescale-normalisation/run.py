"""Does a spectrally normalised clock make the coherence window portable across proteins?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable: a key already in `records.jsonl` is not recomputed.

The continuous-time walk needs an upper limit on its time grid, and that limit is the one
free hyperparameter the observables carry. `allo.quantum.walk._time_grid` sets the unit of
time from the operator's own spectrum, so the limit is dimensionless -- but *which* spectral
quantity supplies the unit decides what the limit means:

* `range` divides by the spectral range, the fastest phase in the operator. The range is
  nearly constant across proteins, so a fixed window is a fixed number of fast revolutions.
  It is **not** a fixed number of slow beats, because the gap is not constant.
* `gap` divides by the gap next to the dominant eigenvalue, the slowest beat the walk can
  produce. A fixed window is then a fixed number of slow periods on every protein.

The earlier window sweep used `range` and found opposite optima on two arms. If the cause is
the gap disparity, `gap` reduces the between-arm spread. If the spread survives, the cause is
elsewhere and the timescale is not the sensitive factor.

The readout is deliberately not "which setting scores best". It is **spread**: the range of
AUC across arms at one setting, and whether the per-arm optimum lands in the same place. A
setting that scores well on one arm and badly on another is the failure being measured.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import yaml

from allo import network
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.quantum.walk import _eigen
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"
FORM = "laplacian"  # the walk's default generator; the sweep is over time, not over form


def spectral_units(graph) -> tuple[float, float]:
    """The two candidate units of time, in the operator's own eigenvalues."""
    values, _ = _eigen(graph, FORM)
    return float(values.max() - values.min()), float(abs(values[-1] - values[-2]))


def steps_for(window: float, scale: str, rng: float, gap: float) -> int:
    """Nyquist on the fastest phase, with headroom, clipped to the configured band.

    Over a grid spanning `window * 2 pi / unit` the fastest phase turns `window * rng / unit`
    times. Sampling it below twice per turn aliases, and the alias is not visible in the
    output -- it just returns a different number. So the step count is derived, never fixed.
    """
    unit = rng if scale == "range" else gap
    fast_periods = window * rng / max(unit, 1e-12)
    want = math.ceil(CONFIG["steps_per_fast_period"] * fast_periods)
    return int(min(max(want, CONFIG["steps_floor"]), CONFIG["steps_cap"]))


def settings(rng: float, gap: float) -> list[tuple[str, dict]]:
    out = []
    for scale, key in (("range", "range_windows"), ("gap", "gap_windows")):
        for window in CONFIG[key]:
            steps = steps_for(float(window), scale, rng, gap)
            out.append(
                (
                    f"{scale}|{window}",
                    {"scale": scale, "window": float(window), "steps": steps},
                )
            )
    return out


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    started = time.time()
    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            graph = network.build(apo_input(arm), **CONFIG["graph"])
            rng, gap = spectral_units(graph)

            for label, spec in settings(rng, gap):
                for name in CONFIG["scorers"]:
                    key = f"{arm}|{label}|{name}"
                    if key in done:
                        continue
                    try:
                        values = np.asarray(QUANTUM[name](graph, **spec), dtype=float)
                    except (MemoryError, ArithmeticError, ValueError) as refused:
                        print(f"  skip {key}: {refused}", flush=True)
                        continue
                    if not np.isfinite(values).all():
                        print(f"  skip {key}: non-finite scores", flush=True)
                        continue

                    record = score_arm(arm, graph.as_scores(values), method=f"{name}[{label}]")
                    sink.write(
                        json.dumps(
                            {
                                "key": key,
                                "arm": arm,
                                "scorer": name,
                                "scale": spec["scale"],
                                "window": spec["window"],
                                "steps": spec["steps"],
                                "auc_roc": record["endpoints"]["auc_roc"],
                                "hits_at_5": record["endpoints"]["hits_at_5"],
                                "dcc_angstrom": record["endpoints"]["dcc_angstrom"],
                                "p_calibrated": record["nulls"]["matched_patch"]["p_calibrated"],
                                "spectral_range": round(rng, 4),
                                "spectral_gap": round(gap, 6),
                                "slow_periods": round(spec["window"] * gap / rng, 4)
                                if spec["scale"] == "range"
                                else spec["window"],
                            }
                        )
                        + "\n"
                    )
                    sink.flush()
                print(f"{arm}/{label}: {time.time() - started:.0f}s", flush=True)

    summarise()
    return 0


def summarise() -> None:
    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    arms = CONFIG["arms"]

    spread = []
    for scale in ("range", "gap"):
        windows = CONFIG["range_windows" if scale == "range" else "gap_windows"]
        for window in windows:
            for scorer in CONFIG["scorers"]:
                cell = {
                    r["arm"]: r["auc_roc"]
                    for r in rows
                    if r["scale"] == scale
                    and r["window"] == float(window)
                    and r["scorer"] == scorer
                }
                if len(cell) < len(arms):
                    continue
                vals = [cell[a] for a in arms]
                spread.append(
                    {
                        "scale": scale,
                        "window": float(window),
                        "scorer": scorer,
                        "mean_auc": round(float(np.mean(vals)), 4),
                        "min_auc": round(float(min(vals)), 4),
                        "auc_spread": round(float(max(vals) - min(vals)), 4),
                        "per_arm": {a: round(cell[a], 4) for a in arms},
                    }
                )

    # Does the per-arm optimum land in the same place? One index per (scale, scorer, arm).
    alignment = []
    for scale in ("range", "gap"):
        windows = [float(w) for w in CONFIG["range_windows" if scale == "range" else "gap_windows"]]
        for scorer in CONFIG["scorers"]:
            best = {}
            for arm in arms:
                curve = {
                    r["window"]: r["auc_roc"]
                    for r in rows
                    if r["scale"] == scale and r["scorer"] == scorer and r["arm"] == arm
                }
                if len(curve) < len(windows):
                    continue
                best[arm] = max(curve, key=curve.get)
            if len(best) == len(arms):
                idx = [windows.index(best[a]) for a in arms]
                alignment.append(
                    {
                        "scale": scale,
                        "scorer": scorer,
                        "argmax_window": best,
                        "index_spread": max(idx) - min(idx),
                        "n_windows": len(windows),
                    }
                )

    best_by_scale = {}
    for scale in ("range", "gap"):
        cells = [s for s in spread if s["scale"] == scale]
        if cells:
            best_by_scale[scale] = {
                "mean_auc_spread": round(float(np.mean([c["auc_spread"] for c in cells])), 4),
                "best_min_auc": max(cells, key=lambda c: c["min_auc"]),
            }

    (HERE / "metrics.json").write_text(
        json.dumps(
            {
                "config": CONFIG,
                "n_records": len(rows),
                "summary": best_by_scale,
                "alignment": alignment,
                "spread": sorted(spread, key=lambda s: -s["min_auc"]),
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
