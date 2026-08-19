#!/usr/bin/env bash
# Format Python the moment an agent writes it, so `make check` never fails on
# formatting alone and the agent loop does not spend a turn on whitespace.
cd "$(dirname "$0")/.." || exit 0
file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
case "$file" in
  *.py) [ -x .venv/bin/ruff ] && .venv/bin/ruff format -q "$file" ;;
esac
exit 0
