"""The manifest is the benchmark. These guard the things that would silently rot it."""

from __future__ import annotations

import re

import pytest

from allo import benchmark

CHALLENGE = benchmark.ROOT / "CHALLENGE.md"


@pytest.fixture(scope="module")
def manifest() -> dict:
    return benchmark.load()


def test_target_ids_are_unique(manifest):
    ids = [t["id"] for t in manifest["targets"]]
    assert len(ids) == len(set(ids))


def test_every_target_declares_what_it_is(manifest):
    for target in manifest["targets"]:
        assert {"id", "tier", "protein", "pocket", "apo", "holo"} <= set(target)
        assert target["tier"] in {"mandated", "corrected", "sensitivity"}
        assert {"pdb", "chain"} <= set(target["apo"])
        assert {"pdb", "chain"} <= set(target["holo"])


def test_a_defective_target_says_so(manifest):
    """A pair we keep only because the challenge mandates it must carry its defect."""
    for target in manifest["targets"]:
        if target["tier"] == "mandated":
            assert target.get("defect"), f"{target['id']} is mandated but records no defect"


def test_mandated_tier_still_matches_the_challenge_table(manifest):
    """If CHALLENGE.md is ever re-read and differs, this fails rather than drifting."""
    table = CHALLENGE.read_text()
    mandated = [t for t in manifest["targets"] if t["tier"] == "mandated"]
    assert {(t["apo"]["pdb"], t["holo"]["pdb"]) for t in mandated} == {
        ("4OBE", "6OIM"),
        ("1OPL", "5MO4"),
        ("5TBY", "6C1H"),
    }
    for target in mandated:
        for pdb in (target["apo"]["pdb"], target["holo"]["pdb"]):
            assert re.search(rf"\b{pdb}\b", table), f"{pdb} is no longer in CHALLENGE.md"


def test_excluded_targets_are_not_frozen(manifest):
    excluded = {t["id"] for t in manifest["targets"] if t.get("status") == "excluded"}
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    assert excluded and not (excluded & set(frozen["targets"]))


def test_the_readme_table_matches_the_freeze():
    """Prose drifts from data silently; this is the cheapest way to stop it."""
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    rows = {
        line.split("|")[1].strip(): line
        for line in readme.splitlines()
        if line.startswith("| ") and line.count("|") > 6
    }
    for target, derived in frozen["targets"].items():
        row = rows.get(target)
        assert row, f"{target} has no row in the README table"
        cells = (
            f"| {derived['n_residues']} | {len(derived['label_residues'])} | "
            f"{derived['label_prevalence'] * 100:.1f} % |"
        )
        assert cells in row, f"{target}: README row disagrees with the freeze\n  {row}"


def test_stats_regenerate_the_protocol_numbers():
    """Section 5 justifies the endpoint choice with numbers. They must come from code."""
    computed = benchmark.stats()
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    for target, values in computed["targets"].items():
        if "corrected" not in target:
            continue
        assert f"**{values['p_at_least_1_hit']:.3f}**" in readme, (
            f"{target}: P(>=1 hit) {values['p_at_least_1_hit']} differs from README section 5"
        )


@pytest.mark.network
def test_frozen_values_still_derive_from_the_deposited_files():
    assert benchmark.verify() == []
