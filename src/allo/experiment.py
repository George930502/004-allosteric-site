"""Experiment scaffolding.

Every run that produces a comparable number gets a directory here: the config that
produced it, the metrics it produced, and notes on what it meant. The registry of
those runs is the project's memory across sessions (see docs/playbooks/experiment.md).
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"

CONFIG_TEMPLATE = """\
# Every knob that affects the result belongs here, including the seed.
# A rerun of this config must reproduce metrics.json exactly.
name: {slug}
date: {day}
seed: 0

target: null          # e.g. kras_g12c
method: null          # e.g. ctqw_time_averaged
params: {{}}
"""

NOTES_TEMPLATE = """\
# {slug}

**Date:** {day}

## Question
What is this run supposed to settle? One sentence.

## Setup
What differs from the previous run. Point at `config.yaml` rather than restating it.

## Result
Numbers from `metrics.json`, and whether they answer the question.

## Interpretation
What we now believe, and what we would have to see to stop believing it.
Negative results stay written down.
"""


def slugify(text: str) -> str:
    """Lowercase, hyphen-separated, filesystem-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        raise ValueError(f"cannot slugify {text!r}")
    return slug


def new_experiment(name: str, day: date | None = None, root: Path | None = None) -> Path:
    """Create `experiments/<date>-<slug>/` with config and notes templates."""
    slug = slugify(name)
    day = day or date.today()
    directory = (root or EXPERIMENTS) / f"{day.isoformat()}-{slug}"
    directory.mkdir(parents=True, exist_ok=False)
    fields = {"slug": slug, "day": day.isoformat()}
    (directory / "config.yaml").write_text(CONFIG_TEMPLATE.format(**fields))
    (directory / "notes.md").write_text(NOTES_TEMPLATE.format(**fields))
    return directory
