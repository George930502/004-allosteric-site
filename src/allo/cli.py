"""`allo` command line entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from allo.experiment import new_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="allo", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    exp = sub.add_parser("new-experiment", help="scaffold an experiment directory")
    exp.add_argument("name", help='short description, e.g. "ctqw time averaged transfer"')

    bench = sub.add_parser("benchmark", help="the frozen benchmark: freeze it or check it")
    bench.add_argument("action", choices=["freeze", "verify", "show"])
    bench.add_argument(
        "--set",
        dest="benchmark_set",
        default=None,
        choices=["primary", "secondary", "all"],
        help=(
            "which benchmark set to act on. `verify` and `show` default to `all`; `freeze` "
            "has NO default and must name one, because the primary freeze is a closed "
            "artifact (ADR 0021) and a default of `all` rewrites it as collateral"
        ),
    )

    ev = sub.add_parser("evaluate", help="the frozen evaluation layer")
    ev.add_argument("action", choices=["calibrate", "repairs", "freeze", "verify"])
    ev.add_argument(
        "config",
        nargs="?",
        help=(
            "calibrate and repairs only: path to an experiment config.yaml. Metrics are "
            "written to "
            "metrics.json beside it, so a rerun of the committed config reproduces the "
            "committed numbers"
        ),
    )
    ev.add_argument(
        "--detect",
        action="store_true",
        help=(
            "verify only: re-run the pocket detector as well. Needs the `eval` extra, so it "
            "belongs to `make verify` and not to the offline `make check`"
        ),
    )

    args = parser.parse_args(argv)
    if args.command == "evaluate":
        from allo.scoring import harness

        if args.action == "calibrate":
            from allo.scoring.calibration import run_calibration

            if args.config is None:
                print("evaluate calibrate needs a config path")
                return 2
            return run_calibration(Path(args.config))
        if args.action == "repairs":
            from allo.scoring.calibration import run_repairs

            if args.config is None:
                print("evaluate repairs needs a config path")
                return 2
            return run_repairs(Path(args.config))
        if args.action == "freeze":
            state = harness.freeze_evaluation()
            harness.EVALUATION_FROZEN.parent.mkdir(parents=True, exist_ok=True)
            harness.EVALUATION_FROZEN.write_text(json.dumps(state, indent=2) + "\n")
            print(f"evaluation: froze {len(state['targets'])} arms -> {harness.EVALUATION_FROZEN}")
            return 0
        problems = harness.verify_evaluation(detect=args.detect)
        if problems:
            print("evaluation: the frozen protocol has drifted:")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        scope = "including the pockets" if args.detect else "offline, pockets skipped"
        print(f"evaluation: verified, every derived value matches the freeze ({scope})")
        return 0
    if args.command == "new-experiment":
        print(new_experiment(args.name))
        return 0

    from allo import benchmark

    if args.action == "freeze" and args.benchmark_set is None:
        print("benchmark freeze needs an explicit --set: it overwrites a frozen artifact")
        return 2
    selected = args.benchmark_set or "all"
    names = list(benchmark.SETS) if selected == "all" else [selected]
    failed = False
    for name in names:
        manifest_path, frozen_path = benchmark.SETS[name]
        if not manifest_path.exists():
            # Skipping is right when the caller asked for everything: a clone may hold only
            # one set. Skipping a set the caller NAMED is a vacuous success, and
            # docs/ROADMAP.md makes a clean `verify` a phase exit criterion.
            print(f"{name}: no manifest at {manifest_path}; nothing to do")
            failed = failed or selected != "all"
            continue
        if args.action == "freeze":
            state = benchmark.freeze(benchmark.load(manifest_path))
            frozen_path.parent.mkdir(parents=True, exist_ok=True)
            frozen_path.write_text(json.dumps(state, indent=2) + "\n")
            print(f"{name}: froze {len(state['targets'])} targets -> {frozen_path}")
            continue
        if args.action == "show":
            print(json.dumps(benchmark.freeze(benchmark.load(manifest_path)), indent=2))
            continue
        problems = benchmark.verify(benchmark_set=name)
        if problems:
            failed = True
            print(f"{name}: benchmark has drifted from its freeze:")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"{name}: verified, every derived value matches the freeze")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
