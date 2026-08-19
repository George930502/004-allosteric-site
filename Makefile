.PHONY: setup check test lint fmt clean

setup:          ## Create .venv and install the project + dev extras
	uv sync --extra dev

check:          ## The one command agents run before claiming done
	./scripts/check.sh

test:
	uv run pytest -q -m "not slow and not network"

lint:
	uv run ruff check .

fmt:
	uv run ruff format . && uv run ruff check --fix .

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__
