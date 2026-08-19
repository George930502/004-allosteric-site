"""`allo` command line entry point."""

from __future__ import annotations

import argparse

from allo.experiment import new_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="allo", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    exp = sub.add_parser("new-experiment", help="scaffold an experiment directory")
    exp.add_argument("name", help='short description, e.g. "ctqw time averaged transfer"')

    args = parser.parse_args(argv)
    if args.command == "new-experiment":
        print(new_experiment(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
