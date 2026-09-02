"""Run the negative-class-(b) size and power measurement behind ADR 0039.

The simulation itself is `allo.scoring.simulate`, because it reads the answer key and that is
evaluation-side work. This script is the record: it reads the config beside it, calls that
function once per arm, and writes `metrics.json` beside itself.

    uv run python experiments/2026-09-03-endpoint-b/run.py
"""

import json
import time
from pathlib import Path

import yaml

from allo.scoring.simulate import endpoint_b_size_and_power

HERE = Path(__file__).resolve().parent
config = yaml.safe_load((HERE / "config.yaml").read_text())

result = {"config": config, "arms": {}}
for target in config["targets"]:
    started = time.time()
    result["arms"][target] = endpoint_b_size_and_power(
        target,
        generators=tuple(config["generators"]),
        correlation_lengths=tuple(config["correlation_lengths"]),
        deltas=tuple(config["deltas"]),
        n_size=int(config["n_size"]),
        n_power=int(config["n_power"]),
        alpha=float(config["alpha"]),
        seed=int(config["seed"]),
    )
    # Wall time is printed and NOT persisted. It was written into `metrics.json` until
    # 2026-09-03, which made the config's promise of an exact rerun impossible to keep for a
    # reason that has nothing to do with the science. A rerun now reproduces the artifact
    # byte for byte.
    print(target, "done", round(time.time() - started, 1), "s", flush=True)
    (HERE / "metrics.json").write_text(json.dumps(result, indent=1) + "\n")
print("written", HERE / "metrics.json")
