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


def test_the_scoring_universe_excludes_what_scores_by_construction():
    """ADR 0011. Nothing that a connectivity score ranks top by construction is a negative.

    Removing propagation-source residues from the positives and leaving them in the
    negatives penalises the method class the challenge asked for -- 44-62 % of AUC-PR at a
    fixed real effect -- and penalises no other. Both classes lose them, or neither does.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    for target, derived in frozen["targets"].items():
        excluded = set(derived["excluded_from_scoring"])
        assert set(derived["active_site"]) <= excluded, (
            f"{target}: active-site residues {sorted(set(derived['active_site']) - excluded)} "
            "are still scored as negatives"
        )
        assert not excluded & set(derived["scoreable_label_residues"]), (
            f"{target}: a residue is in both the positives and the excluded set"
        )
        assert derived["n_candidates"] == derived["n_residues"] - len(excluded)
        assert derived["n_candidates"] > len(derived["scoreable_label_residues"])


def test_sibling_functional_sites_leave_the_background(manifest):
    """The cross-arm half of the same rule: our own Site 2 labels are not Site 1 negatives."""
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    where = {
        s["id"]: (s["site_id"], s["apo"]["pdb"], s["apo"]["chain"]) for s in manifest["targets"]
    }
    checked = 0
    for target, derived in frozen["targets"].items():
        site, pdb, chain = where[target]
        for other, other_derived in frozen["targets"].items():
            if other == target or where[other][1:] != (pdb, chain) or where[other][0] == site:
                continue
            checked += 1
            excluded = set(derived["excluded_from_scoring"])
            foreign = set(other_derived["label_residues"]) - set(derived["label_residues"])
            assert foreign <= excluded, (
                f"{target}: {other}'s labels {sorted(foreign - excluded)} are scored as negatives"
            )
    assert checked, "no sibling-site pair found; this test would pass vacuously"
    # The converse, which is where the free-text bug lived: two arms on the *same* site must
    # never mask each other. Site 1's XB2 and 2OW arms share `8QYP`:A and share `myh7_site1`.
    for target, derived in frozen["targets"].items():
        for other, other_derived in frozen["targets"].items():
            if other == target or where[other] != where[target]:
                continue
            own = set(other_derived["label_residues"]) - set(derived["label_residues"])
            assert not (own & set(derived["excluded_from_scoring"])), (
                f"{target}: excludes {sorted(own & set(derived['excluded_from_scoring']))}, "
                f"which are {other}'s labels for the *same* site"
            )


def test_the_confirmatory_family_is_every_corrected_arm(manifest):
    """Section 5 Holm-corrects across the confirmatory family. Its size must not be hand-typed.

    It was, once: "three tests" counted proteins, but a target is a protein *plus a site*
    (ADR 0008), so myosin's two sites make four corrected arms. Either Site 2 was being
    dropped from the family or the family-wise error rate was under-corrected.
    """
    computed = benchmark.stats()
    corrected = {s["id"] for s in manifest["targets"] if s.get("tier") == "corrected"}
    assert set(computed["confirmatory_family"]) == corrected, (
        f"stats() family {sorted(computed['confirmatory_family'])} != corrected arms "
        f"{sorted(corrected)}"
    )
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    spelled = {2: "Two", 3: "Three", 4: "Four", 5: "Five"}[computed["family_size"]]
    assert f"{spelled} tests, Holm-corrected across the {spelled.lower()}" in readme, (
        f"README section 5 does not say '{spelled} tests' for a family of {computed['family_size']}"
    )


def test_site_identity_is_canonical_not_free_text(manifest):
    """ADR 0011's sibling rule keys on `site_id`, because `site` is a display string.

    It once keyed on `site`, and the two halves of myosin Site 1 read "mavacamten site" and
    "mavacamten/omecamtiv pocket (Site 1)" -- so they masked each other's labels as if they
    were different pockets and both candidate counts were wrong. A benchmark invariant may
    not depend on how a label happened to be worded.
    """
    for spec in manifest["targets"]:
        site_id = spec.get("site_id", "")
        assert re.fullmatch(r"[a-z0-9_]+", site_id), f"{spec['id']}: site_id {site_id!r}"
    # Arms of the same site must agree, arms of different sites must not collide.
    by_id: dict[str, set[str]] = {}
    for spec in manifest["targets"]:
        by_id.setdefault(spec["site_id"], set()).add(spec["site"])
    assert by_id["myh7_site1"] > {"mavacamten site"}, (
        "the two spellings of Site 1 no longer differ; this test has stopped testing anything"
    )
    assert len(by_id) == 4, f"expected 4 distinct sites across the freeze, got {sorted(by_id)}"


def test_the_manifest_pins_the_same_apo_bytes_as_the_freeze(manifest):
    """`apo_input` fails closed on the manifest hash, so it has to equal the frozen one.

    Two records of the same fact drift. This is the cheapest way to notice.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        pdb = spec["apo"]["pdb"]
        assert spec["apo"].get("sha256") == frozen["targets"][spec["id"]]["hashes"][pdb], (
            f"{spec['id']}: manifest and freeze disagree on {pdb}'s bytes"
        )


def test_apo_input_refuses_a_structure_that_is_not_the_frozen_one(tmp_path, manifest):
    """A guard that cannot fail is not a guard: plant a wrong file and watch it refuse."""
    from allo.inputs import apo_input

    spec = next(s for s in manifest["targets"] if s["id"] == "kras_g12c_mandated")
    (tmp_path / f"{spec['apo']['pdb']}.cif").write_text("data_NOT_THE_FROZEN_FILE")
    with pytest.raises(ValueError, match="not the frozen file"):
        apo_input("kras_g12c_mandated", raw=tmp_path)


@pytest.mark.network
def test_frozen_values_still_derive_from_the_deposited_files():
    assert benchmark.verify() == []


@pytest.mark.network
def test_methods_and_the_benchmark_agree_on_the_node_set(manifest):
    """ADR 0010 clause 1: the node set is every modelled residue of the frozen chain.

    Two code paths compute it independently. `allo.inputs.apo_input` is what a *method*
    receives, and counts modelled polymer residues; `benchmark.derive` sets `n_residues`,
    the denominator of label prevalence and of every hypergeometric baseline, and counts
    residues carrying a CA atom. Those are the same set only while every modelled residue
    has a CA — true on all ten arms today, but nothing made it true.

    If they ever diverge, methods are scored against a denominator that is not the node set
    they were given, and no other test would notice. This is also the guard on ADR 0010
    itself: silently trimming a domain inside the loading code fails here.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    from allo.inputs import apo_input

    for target, derived in frozen["targets"].items():
        given = apo_input(target).residues
        assert len(given) == derived["n_residues"], (
            f"{target}: methods receive {len(given)} nodes but the benchmark scores against "
            f"n_residues={derived['n_residues']}"
        )


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
