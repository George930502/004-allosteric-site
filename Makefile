.PHONY: setup check verify test lint fmt clean

setup:          ## Create .venv and install the project + dev extras
	uv sync --extra dev

check:          ## The one command agents run before claiming done
	./scripts/check.sh

verify:         ## Re-derive the frozen benchmark from RCSB and fail on any drift (needs network)
	uv run allo benchmark verify
	uv run pytest -q -m network

test:
	uv run pytest -q -m "not slow and not network"

lint:
	uv run ruff check .

fmt:
	uv run ruff format . && uv run ruff check --fix .

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__
