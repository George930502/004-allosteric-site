"""`allo` command line entry point."""

from __future__ import annotations

import argparse
import json

from allo.experiment import new_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="allo", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    exp = sub.add_parser("new-experiment", help="scaffold an experiment directory")
    exp.add_argument("name", help='short description, e.g. "ctqw time averaged transfer"')

    bench = sub.add_parser("benchmark", help="the frozen benchmark: freeze it or check it")
    bench.add_argument("action", choices=["freeze", "verify", "show", "stats"])

    args = parser.parse_args(argv)
    if args.command == "new-experiment":
        print(new_experiment(args.name))
        return 0

    from allo import benchmark

    if args.action == "freeze":
        state = benchmark.freeze()
        benchmark.FROZEN.write_text(json.dumps(state, indent=2) + "\n")
        print(f"froze {len(state['targets'])} targets -> {benchmark.FROZEN}")
        return 0
    if args.action == "stats":
        print(json.dumps(benchmark.stats(), indent=2))
        return 0
    if args.action == "show":
        print(json.dumps(benchmark.freeze(), indent=2))
        return 0

    problems = benchmark.verify()
    if problems:
        print("benchmark has drifted from its freeze:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("benchmark verified: every derived value matches the freeze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
