#!/usr/bin/env bash
# The single verification gate. Agents (and CI) run this; it must pass before
# any task is reported as done. Fast by design: no network, no slow tests.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> ruff format --check"
uv run ruff format --check .

echo "==> ruff check"
uv run ruff check .

echo "==> pytest (fast subset)"
uv run pytest -q -m "not slow and not network"

echo "==> OK"
