.PHONY: setup check verify lint fmt clean

setup:          ## Create .venv and install the project + dev extras
	uv sync --extra dev

check:          ## The one command agents run before claiming done
	./scripts/check.sh

verify:         ## Re-derive both frozen layers and fail on any drift (needs network + eval extra)
	uv run allo benchmark verify
	uv run allo evaluate verify --detect
	uv run pytest -q -m network

lint:
	uv run ruff check .

fmt:
	uv run ruff format . && uv run ruff check --fix .

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__
