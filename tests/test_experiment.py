from datetime import date

import pytest

from allo.experiment import new_experiment, slugify


def test_slugify():
    assert slugify("CTQW time-averaged transfer!") == "ctqw-time-averaged-transfer"
    with pytest.raises(ValueError):
        slugify("!!!")


def test_new_experiment_scaffolds_config_and_notes(tmp_path):
    directory = new_experiment("noise sweep", day=date(2026, 1, 2), root=tmp_path)
    assert directory.name == "2026-01-02-noise-sweep"
    assert "seed: 0" in (directory / "config.yaml").read_text()
    assert (directory / "notes.md").exists()
