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
        assert {"id", "tier", "protein", "site", "apo", "holo"} <= set(target)
        assert target["tier"] in {"mandated", "corrected", "sensitivity"}
        assert {"pdb", "chain"} <= set(target["apo"])
        assert {"pdb", "chain"} <= set(target["holo"])


def test_every_target_says_why_its_site_is_allosteric(manifest):
    """Clause (ii). The ground-truth concept, made checkable instead of assumed.

    A 4.5 A contact shell around a bound drug is a *drug footprint*; what makes it an
    allosteric site is a functional experiment somebody ran. Without this field the
    benchmark asserts its own ground truth (ADR 0007).
    """
    for target in manifest["targets"]:
        evidence = target.get("allosteric_evidence", {})
        assert evidence.get("doi", "").startswith("10."), f"{target['id']}: no DOI for the site"
        assert len(evidence.get("assay", "")) > 80, f"{target['id']}: no assay described"


def test_every_target_declares_state_and_blindness(manifest):
    """Clauses (viii) and (ix).

    State is *disclosed, not required* — no allostery source demands an apo/holo state
    difference, and requiring one would exclude dynamic allostery by construction. What
    is required is saying which it is. Blindness likewise: an ASD-trained comparator on
    an ASD-curated target is not blind, and a results table that does not say so misleads.
    """
    for target in manifest["targets"]:
        assert {"apo", "holo", "matched"} <= set(target.get("state", {})), target["id"]
        blind = target.get("blind", {})
        assert isinstance(blind.get("value"), bool), f"{target['id']}: blindness undeclared"
        assert len(blind.get("why", "")) > 40, f"{target['id']}: blindness unjustified"


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
        # Cell-wise, not substring: the markdown formatter re-pads these columns on every
        # write, so an exact-width match would fail on formatting rather than on content.
        cells = [c.strip() for c in row.split("|")]
        for value in (
            str(derived["n_residues"]),
            str(len(derived["label_residues"])),
            str(len(derived["scoreable_label_residues"])),
            f"{derived['label_prevalence'] * 100:.1f} %",
        ):
            assert value in cells, f"{target}: README row missing {value!r}\n  {row}"


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
    # The AUC-ROC/AUC-PR pair is what makes AUC-PR co-primary, and it drifted once because
    # only the hypergeometric line above was guarded: the README claimed PR 0.243 -> 0.066
    # where the code says 0.263 -> 0.065. Same protection, same three arms the prose names.
    for target in (
        "kras_g12c_corrected",
        "bcr_abl1_corrected",
        "cardiac_myosin_site1_sensitivity_srx",
    ):
        values = computed["targets"][target]
        for key in ("simulated_auc_roc", "simulated_auc_pr"):
            assert f"**{values[key]:.3f}**" in readme, (
                f"{target}: {key} {values[key]} differs from README section 5"
            )


@pytest.mark.network
def test_frozen_values_still_derive_from_the_deposited_files():
    assert benchmark.verify() == []


@pytest.mark.network
def test_label_sets_do_not_depend_on_a_minor_conformer(manifest):
    """`parse_mmcif` keeps every altloc and nothing filters by occupancy.

    That is tolerable only while no label set depends on it. Four holo entries carry
    alternate conformations (5MO4, 8QYR, 8QYU, 9F6C), so a residue whose *minor*
    conformer swings inside the 4.5 A shell would be labelled on the strength of a
    partially occupied atom. README section 7 asserts no frozen arm is affected; this
    re-derives that instead of trusting a one-off check, because the day it stops being
    true is the day the assertion is worth having.
    """
    import numpy as np

    from allo.inputs import RAW
    from allo.structure.pdb import contacts, fetch_mmcif, parse_mmcif

    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        holo = parse_mmcif(fetch_mmcif(spec["holo"]["pdb"], RAW), spec["holo"]["pdb"])
        chain, comp = spec["holo"]["chain"], spec["holo"]["ligand"]
        ligand = holo.ligand & (holo.resname == comp) & (holo.chain == chain)
        primary = np.isin(holo.altloc, [".", "?", "", "A"])
        full = {n for c, n, _ in contacts(holo, ligand, holo.protein, cutoff) if c == chain}
        prim = {
            n
            for c, n, _ in contacts(holo, ligand & primary, holo.protein & primary, cutoff)
            if c == chain
        }
        assert full == prim, (
            f"{spec['id']}: labels {sorted(full - prim)} enter only via a minor conformer"
        )
