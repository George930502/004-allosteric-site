"""The manifest is the benchmark. These guard the things that would silently rot it."""

from __future__ import annotations

import re

import numpy as np
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


def test_the_null_protocol_is_complete_and_schema_validated(manifest):
    """A null knob not represented here remains movable after results are seen."""
    null = manifest["null"]
    assert set(null) == {
        "graph",
        "surface_rule",
        "distance_statistics",
        "growth_algorithm",
        "replicates",
        "seed",
        "p_value",
        "calibration",
    }
    assert null["graph"] == {
        "atom_selection": "heavy",
        "contact_cutoff_angstrom": manifest["defaults"]["contact_cutoff_angstrom"],
    }
    assert null["surface_rule"] == {
        "statistic": "contact_degree",
        "maximum_quantile": 0.5,
    }
    # The lower quartile is independent of the minimum and median: [1,2,3,20,...] and
    # [1,19,19,20,...] can share the latter two while putting three versus one residues near
    # the source. Section 5 clause 4 must constrain that lower tail explicitly.
    assert [entry["statistic"] for entry in null["distance_statistics"]] == [
        "median_min_ca_distance_to_active_site",
        "minimum_min_ca_distance_to_active_site",
        "q25_min_ca_distance_to_active_site",
    ]
    for entry in null["distance_statistics"]:
        assert isinstance(entry["tolerance_angstrom"], float)
        assert entry["tolerance_angstrom"] > 0
    assert null["growth_algorithm"] == "uniform_contact_frontier"
    assert isinstance(null["replicates"], int) and null["replicates"] > 0
    assert isinstance(null["seed"], int)
    assert null["p_value"] == {"tail": "greater_equal", "plus_one_correction": True}
    assert null["calibration"] == {
        "alpha": 0.05,
        "independent_replicates": 1000,
        "prediction_interval_coverage": 0.95,
    }

    import copy

    broken = copy.deepcopy(manifest)
    broken["null"].pop("seed")
    with pytest.raises(ValueError, match="null fields"):
        benchmark._validate_protocol(broken)
    broken = copy.deepcopy(manifest)
    broken["orthosteric_vocabulary"]["additives"].append("ADP")
    with pytest.raises(ValueError, match="disjoint"):
        benchmark._validate_protocol(broken)


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
    assert {
        "frozen_on",
        "contact_cutoff_angstrom",
        "null",
        "orthosteric_vocabulary",
        "structure_provenance",
        "label_footprints",
        "functional_sites",
        "targets",
    } == set(frozen)
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
    calibration = computed["null_calibration"]
    assert calibration["accepted_rejection_counts"] == [37, 64]
    assert calibration["accepted_type_i_rate"] == [0.037, 0.064]
    assert "binom.ppf([0.025, 0.975], n=1000, p=0.05) / 1000" in readme


def test_stats_report_both_scoring_universes():
    """The candidate-set policy is ours, so every result needs the node-set sensitivity."""
    computed = benchmark.stats()
    for values in computed["targets"].values():
        sensitivity = values["scoring_universe_sensitivity"]
        assert set(sensitivity) == {"candidate_set", "whole_node_set"}
        assert sensitivity["candidate_set"]["n"] == values["n_candidates"]
        assert sensitivity["whole_node_set"]["n"] == values["n_residues"]
        assert sensitivity["candidate_set"]["n_scoreable"] == values["n_scoreable"]
        assert sensitivity["whole_node_set"]["n_scoreable"] == values["n_scoreable"]


def test_stats_for_one_arm_do_not_depend_on_other_manifest_arms():
    """Adding a sensitivity arm must not move an existing arm's simulated baseline."""
    import copy
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    baseline = benchmark.stats(frozen)["targets"]["kras_g12c_corrected"]
    widened = copy.deepcopy(frozen)
    widened["targets"]["extra_sensitivity_arm"] = copy.deepcopy(
        widened["targets"]["bcr_abl1_mandated"]
    )
    assert benchmark.stats(widened)["targets"]["kras_g12c_corrected"] == baseline


# Who is allowed to lose ground truth, through which channel, and exactly which residues.
# Derived once from the freeze and pinned here as a tripwire: an expectation that lives in
# the artifact it is checking can be silenced by editing the artifact, which is how the
# first version of this test came to pass on a freeze with every cut erased.
DECLARED_LABEL_LOSS = {
    "bcr_abl1_corrected": {"unmapped": ["A:VAL525", "A:LEU529"], "outside": []},
    "bcr_abl1_sensitivity": {"unmapped": ["A:VAL525", "A:LEU529"], "outside": []},
    "bcr_abl1_trimmed": {"unmapped": [], "outside": [521, 525, 529]},
}


def test_every_arm_accounts_for_the_labels_it_does_not_score(manifest):
    """Ground truth may be lost to a construct or to a trim, but never unaccounted for.

    Two channels drop a label and they are not interchangeable. `unmapped` holds holo
    residues with no counterpart in the apo model - `bcr_abl1_corrected` loses Val525 and
    Leu529 because `2G2H` stops at 523. `labels_outside_node_set` holds residues the apo
    *does* model but the manifest node set excludes - `bcr_abl1_trimmed` loses 521, 525 and
    529 because the strict-C5 kinase boundary cuts through the myristoyl pocket (ADR 0010).

    The load-bearing assertion is the reconciliation, not the pins. Arms sharing a site and
    a holo entry describe one pocket, so `kept + unmapped + outside` must be the same number
    for all of them. That is derived from the other arms rather than read from the field
    under test, so erasing a declaration breaks the arithmetic instead of satisfying it.
    """
    import json
    from collections import defaultdict

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    spec = {t["id"]: t for t in manifest["targets"]}

    pockets = defaultdict(dict)
    for name, values in frozen.items():
        holo = spec[name]["holo"]
        key = (spec[name]["site_id"], holo["pdb"], holo["chain"], holo["ligand"])
        pockets[key][name] = (
            len(values["label_residues"])
            + len(values["unmapped"])
            + len(values["labels_outside_node_set"])
        )
    for key, arms in pockets.items():
        assert len(set(arms.values())) == 1, (
            f"arms on {key} disagree on the pocket size: {arms} - an arm has dropped a label "
            "without declaring it in `unmapped` or `labels_outside_node_set`"
        )

    for name, values in frozen.items():
        expected = DECLARED_LABEL_LOSS.get(name, {"unmapped": [], "outside": []})
        assert values["unmapped"] == expected["unmapped"], f"{name}: unmapped set moved"
        assert values["labels_outside_node_set"] == expected["outside"], f"{name}: cut set moved"

        cut = set(values["labels_outside_node_set"])
        assert not cut & set(values["label_residues"]), f"{name}: a cut label is still scored"
        assert not cut & set(values["residue_ids"]), f"{name}: a cut label is still a node"
        if cut:
            assert spec[name]["apo"].get("residue_range"), (
                f"{name} drops labels {sorted(cut)} with no manifest residue_range - a node "
                "set may only cut ground truth at a boundary it declares"
            )

    assert benchmark._label_accounting_problems(frozen, manifest) == []

    # An arm-to-arm reconciliation permits synchronized loss. The manifest footprint is an
    # independent authority, so deleting the same label from both KRAS arms is still caught.
    import copy

    synchronized = copy.deepcopy(frozen)
    for name in ("kras_g12c_mandated", "kras_g12c_corrected"):
        removed = synchronized[name]["label_residues"].pop()
        if removed in synchronized[name]["scoreable_label_residues"]:
            synchronized[name]["scoreable_label_residues"].remove(removed)
    assert benchmark._label_accounting_problems(synchronized, manifest)

    # A pocket represented by one arm has no sibling to disagree with. It must still
    # reconcile against the independently pinned holo ligand-contact footprint.
    single = copy.deepcopy(frozen)
    single["cardiac_myosin_site2_corrected"]["label_residues"].pop()
    assert benchmark._label_accounting_problems(single, manifest)


def test_the_freeze_recovers_its_bytes_with_no_network(tmp_path, monkeypatch, manifest):
    """ADR 0014. A pinned hash detects an RCSB revision; it cannot undo one.

    `data/raw/` is not tracked, so before the store existed a clean clone could reproduce
    `frozen.json` only for as long as RCSB kept serving byte-identical mmCIF. This restores
    every pinned entry from the partitioned root `structures/` mirror with the network
    refused outright,
    and checks the recovered bytes against the hashes the freeze itself records.
    """
    import json
    import urllib.request

    from allo.groundtruth.structures import fetch_mmcif
    from allo.structure.pdb import APO_STRUCTURES, sha256

    def refuse(*args, **kwargs):
        raise AssertionError("fetch_mmcif went to the network; the tracked store missed an entry")

    monkeypatch.setattr(urllib.request, "urlopen", refuse)

    pinned: dict[str, str] = {}
    for values in json.loads(benchmark.FROZEN.read_text())["targets"].values():
        pinned.update(values["hashes"])
    assert pinned, "the freeze pins no hashes, so this test would pass vacuously"
    for pdb, digest in sorted(pinned.items()):
        assert sha256(fetch_mmcif(pdb, tmp_path)) == digest, f"{pdb} did not restore to its pin"

    # The store covers every accession the manifest names, not merely every one the freeze
    # derives: `cardiac_myosin_site1_mandated` is excluded and so pins nothing, but `5TBY`
    # and `6C1H` are the evidence for why it is excluded and have to survive too.
    named = {
        spec[role]["pdb"]
        for spec in manifest["targets"]
        for role in ("apo", "holo")
        if role in spec
    }
    root = APO_STRUCTURES.parent
    assert {path.name for path in root.iterdir() if path.is_dir()} == {"apo", "holo"}
    stored = {
        path.name.removesuffix(".cif.gz")
        for partition in (root / "apo", root / "holo")
        for path in partition.glob("*.cif.gz")
    }
    assert named <= stored, f"the tracked store is missing {sorted(named - stored)}"
    assert stored <= named, f"the tracked store holds unreferenced entries {sorted(stored - named)}"


def test_prediction_side_has_no_free_form_accession_resolver(tmp_path):
    """C1: prediction inputs are target-bound; callers cannot ask the store for a PDB id."""
    from allo.structure.pdb import fetch_mmcif

    for pdb in ("6OIM", "5MO4", "9F6C", "9GZ2", "8QYR", "8QYU", "9YRG", "6C1H"):
        with pytest.raises(PermissionError, match="apo_input"):
            fetch_mmcif(pdb, tmp_path)


@pytest.mark.network
def test_versioned_archive_reproduces_every_pinned_structure(manifest):
    """ADR 0014 option 1: every decompressed versioned artifact matches its frozen hash."""
    import gzip
    import hashlib
    import urllib.request

    provenance = manifest["structure_provenance"]
    assert len(provenance) == 15
    for pdb, record in sorted(provenance.items()):
        assert record["version"] in record["url"]
        request = urllib.request.Request(record["url"], headers={"User-Agent": "allo/0.1"})
        with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310
            restored = gzip.decompress(response.read())
        assert hashlib.sha256(restored).hexdigest() == record["sha256"], pdb


def test_same_site_labels_are_not_negatives_in_a_sibling_arm(manifest):
    """ADR 0015. A residue this benchmark labels is not a negative in a sibling arm.

    The first half needs no mapping at all — arms sharing an apo entry share its author
    numbering — so it checks the freeze without reusing the alignment the rule is built on.
    The second half pins the case the rule exists for: the confirmatory mavacamten arm is on
    `9GZ3` and the omecamtiv arm on `8QYP`, so the entry-local rule that preceded ADR 0015
    left the omecamtiv-only residues of the same pocket scoring as false positives in the one
    arm whose p-value carries a claim.
    """
    import json
    from itertools import permutations

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    spec = {t["id"]: t for t in manifest["targets"]}

    def negatives(name: str) -> set[int]:
        values = frozen[name]
        scored = set(values["residue_ids"]) - set(values["excluded_from_scoring"])
        return scored - set(values["label_residues"])

    entry = lambda name: (spec[name]["apo"]["pdb"], spec[name]["apo"]["chain"])  # noqa: E731
    checked = 0
    for arm, other in permutations(frozen, 2):
        if spec[arm]["protein"] != spec[other]["protein"] or entry(arm) != entry(other):
            continue
        checked += 1
        intruders = negatives(arm) & set(frozen[other]["label_residues"])
        assert not intruders, f"{arm} scores {sorted(intruders)} as negatives; {other} labels them"
    assert checked, "no same-entry arm pair found; this half would pass vacuously"

    omecamtiv_only = {146, 147, 160, 170, 492, 771}
    leaked = negatives("cardiac_myosin_site1_corrected") & omecamtiv_only
    assert not leaked, (
        f"the confirmatory myosin arm scores {sorted(leaked)} as negatives, and the omecamtiv "
        "arm labels them as the same pocket -- ADR 0015 must carry them across entries"
    )


def test_an_added_arm_cannot_move_an_existing_candidate_universe(manifest):
    """ADR 0015: the registry, not however many arms were curated, defines exclusions."""
    import copy
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    baseline = frozen["cardiac_myosin_site1_corrected"]["n_candidates"]
    planted_targets = copy.deepcopy(frozen)
    planted_targets["new_myosin_arm"] = copy.deepcopy(frozen["cardiac_myosin_site2_corrected"])
    planted_targets["new_myosin_arm"]["label_residues"].append(100)
    planted_manifest = copy.deepcopy(manifest)
    planted_spec = copy.deepcopy(
        next(s for s in manifest["targets"] if s["id"] == "cardiac_myosin_site2_corrected")
    )
    planted_spec["id"] = "new_myosin_arm"
    planted_manifest["targets"].append(planted_spec)

    benchmark._exclude_functional_sites(planted_targets, planted_manifest, benchmark.RAW)
    assert planted_targets["cardiac_myosin_site1_corrected"]["n_candidates"] == baseline


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


def test_claim_and_robustness_families_exclude_every_quarantined_arm(manifest):
    """Section 5 Holm-corrects across the confirmatory family. Its size must not be hand-typed.

    It was, once: "three tests" counted proteins, but a target is a protein *plus a site*
    (ADR 0008), so myosin's two sites make four corrected arms. Either Site 2 was being
    dropped from the family or the family-wise error rate was under-corrected. It is three
    again now, for the opposite reason and by derivation rather than by counting: ADR 0013
    quarantines the `8QYP` arms because that apo was chosen against holo-defined geometry,
    and `cardiac_myosin_site2_corrected` is one of them.
    """
    computed = benchmark.stats()
    corrected = {
        s["id"]
        for s in manifest["targets"]
        if s.get("tier") == "corrected" and not s.get("quarantine")
    }
    assert any(s.get("quarantine") for s in manifest["targets"]), (
        "no arm is quarantined, so this test no longer distinguishes the two rules"
    )
    sensitivity = {
        s["id"]
        for s in manifest["targets"]
        if s.get("tier") == "sensitivity" and not s.get("quarantine")
    }
    assert set(computed["claim_bearing_family"]) == corrected, (
        f"stats() family {sorted(computed['claim_bearing_family'])} != corrected arms "
        f"{sorted(corrected)}"
    )
    assert set(computed["robustness_family"]) == sensitivity
    quarantined = {s["id"] for s in manifest["targets"] if s.get("quarantine")}
    assert not quarantined & set(computed["claim_bearing_family"])
    assert not quarantined & set(computed["robustness_family"])
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    spelled = {2: "Two", 3: "Three", 4: "Four", 5: "Five"}[computed["family_size"]]
    assert f"{spelled} tests, Holm-corrected across the {spelled.lower()}" in readme, (
        f"README section 5 does not say '{spelled} tests' for a family of {computed['family_size']}"
    )
    section = readme.split("**Multiplicity", 1)[1].split("**No tuning", 1)[0]
    contradictory = re.findall(
        r"(?i)(?:\b(?:three|3)\s+confirmatory tests\b|"
        r"\bHolm across (?:the )?(?:three|3)\b|"
        r"\bsignificance only for (?:the )?(?:three|3)\b)",
        section,
    )
    assert not contradictory, f"contradictory confirmatory-family statements: {contradictory}"

    renamed = {**manifest, "targets": [dict(s) for s in manifest["targets"]]}
    corrected_spec = next(s for s in renamed["targets"] if s["tier"] == "corrected")
    corrected_spec["id"] = "name_without_a_tier_suffix"
    fake_frozen = {"targets": {"name_without_a_tier_suffix": {}}}
    assert benchmark.claim_bearing_family(fake_frozen, renamed) == ["name_without_a_tier_suffix"]

    section = readme.split("**Multiplicity", 1)[1].split("**No tuning", 1)[0]
    for family in (*computed["claim_bearing_family"], *computed["robustness_family"]):
        assert f"`{family}`" in section, f"README reporting family omits {family}"


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


def test_manifest_registries_are_complete_and_independently_regenerable(manifest):
    """Label footprints and functional-site registries are authorities, not prose counts."""
    import json

    from allo.groundtruth.labels import align_numbering, pocket_residues
    from allo.groundtruth.structures import fetch_mmcif
    from allo.structure.pdb import parse_mmcif

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    scoreable = [spec for spec in manifest["targets"] if spec.get("status") != "excluded"]
    expected_keys = {
        f"{spec['holo']['pdb']}:{spec['holo']['chain']}:{spec['holo']['ligand']}"
        for spec in scoreable
    }
    assert set(manifest["label_footprints"]) == expected_keys
    assert set(manifest["functional_sites"]) == {spec["protein"] for spec in scoreable}

    parsed = {}
    for key, authority in manifest["label_footprints"].items():
        pdb, chain, ligand = key.split(":")
        if pdb not in parsed:
            parsed[pdb] = parse_mmcif(fetch_mmcif(pdb, benchmark.RAW), pdb)
        live = [
            f"{c}:{name}{number}"
            for c, number, name in pocket_residues(
                parsed[pdb], ligand, manifest["defaults"]["contact_cutoff_angstrom"], chain
            )
            if c == chain
        ]
        assert live == authority, key

    for protein, registry in manifest["functional_sites"].items():
        assert set(registry) == {"reference", "residues"}
        assert registry["residues"] == sorted(set(registry["residues"]))
        assert registry["reference"] in {
            f"{spec['apo']['pdb']}:{spec['apo']['chain']}"
            for spec in scoreable
            if spec["protein"] == protein
        }

        # The residues themselves, not just the shape. This registry is the exclusion
        # authority (ADR 0015): a residue quietly dropped from it returns to the negative
        # class, which is the bug the registry was built to remove, and an invented one
        # shrinks a candidate set for no reason. Neither was caught until the shape check
        # was mutation-tested. Derived from the frozen labels rather than read back.
        reference, reference_chain = registry["reference"].split(":")
        if reference not in parsed:
            parsed[reference] = parse_mmcif(fetch_mmcif(reference, benchmark.RAW), reference)
        union: set[int] = set()
        for spec in scoreable:
            if spec["protein"] != protein or spec["id"] not in frozen:
                continue
            labels = frozen[spec["id"]]["label_residues"]
            if (spec["apo"]["pdb"], spec["apo"]["chain"]) == (reference, reference_chain):
                union.update(labels)
                continue
            if spec["apo"]["pdb"] not in parsed:
                parsed[spec["apo"]["pdb"]] = parse_mmcif(
                    fetch_mmcif(spec["apo"]["pdb"], benchmark.RAW), spec["apo"]["pdb"]
                )
            mapping = align_numbering(
                parsed[spec["apo"]["pdb"]],
                parsed[reference],
                spec["apo"]["chain"],
                reference_chain,
            )
            union.update(mapping[residue] for residue in labels if residue in mapping)
        assert set(registry["residues"]) == union, (
            f"{protein} registry {sorted(set(registry['residues']) ^ union)} disagrees with the "
            "union of that protein's frozen labels"
        )

    assert benchmark._label_accounting_problems(frozen, manifest) == []


def test_repository_memory_regenerates_from_the_freeze_and_protocol(manifest):
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    computed = benchmark.stats(frozen, manifest=manifest)
    registry = (benchmark.ROOT / "experiments" / "REGISTRY.md").read_text()
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    adrs = {
        number: (benchmark.ROOT / "docs" / "adr" / name).read_text()
        for number, name in {
            "0006": "0006-cofactors-and-modified-residues-as-nodes.md",
            "0013": "0013-answer-informed-apo-selection.md",
            "0014": "0014-retain-exact-benchmark-structure-bytes.md",
            "0015": "0015-same-site-labels-leave-the-background.md",
        }.items()
    }
    myosin = computed["targets"]["cardiac_myosin_site1_corrected"]
    excluded = [values["n_excluded"] for values in computed["targets"].values()]
    candidates = [values["n_candidates"] for values in computed["targets"].values()]
    assert f"/ {myosin['p_at_least_1_hit']:.3f}**" in registry
    assert f"{min(excluded)}–{max(excluded)}" in registry
    assert f"{min(candidates)}–{max(candidates)}" in registry
    assert "17 unique benchmark entries" in registry
    assert "17 are retained" in registry
    assert "q25_min_ca_distance_to_active_site" in readme
    assert "ADR 0013" in readme and "ADR 0013 records" not in readme.split("## 2.", 1)[0]
    for number, text in adrs.items():
        assert "**Status:** accepted" in text, number
    assert "## Superseded: pending owner decision" not in adrs["0014"]


def test_trimmed_abl1_range_is_derived_from_the_pinned_authority(manifest):
    spec = next(s for s in manifest["targets"] if s["id"] == "bcr_abl1_trimmed")
    mandated = next(s for s in manifest["targets"] if s["id"] == "bcr_abl1_mandated")
    assert spec["tier"] == "sensitivity"
    assert spec["apo"]["pdb"] == mandated["apo"]["pdb"] == "1OPL"
    assert spec["apo"]["chain"] == mandated["apo"]["chain"] == "A"

    residue_range = spec["apo"]["residue_range"]
    authority = residue_range["authority"]
    assert authority["database"] == "UniProtKB"
    assert authority["accession"] == "P00519"
    assert authority["release"] == "2026_02"
    assert str(authority["retrieved_on"]) == "2026-08-20"
    assert authority["record_url"] == "https://www.uniprot.org/uniprotkb/P00519/entry"
    assert authority["release_url"].endswith("/2026-06-10-release")
    assert authority["canonical_isoform"] == "P00519-1"
    assert authority["deposited_isoform"] == "P00519-2"
    domain = authority["canonical_domain"]
    substitution = authority["isoform_substitution"]
    offset = substitution["replacement_length"] - (
        substitution["canonical_end"] - substitution["canonical_start"] + 1
    )
    assert offset == 19
    assert [residue_range["start"], residue_range["end"]] == [
        domain["start"] + offset,
        domain["end"] + offset,
    ]


def test_prediction_structure_is_an_immutable_single_chain_protein_view():
    """The ordinary offline gate must catch ligand, water, chain and mutability leaks."""
    from allo.inputs import _prediction_structure
    from allo.structure.pdb import Structure

    full = Structure(
        pdb_id="TEST",
        chain=np.array(["A", "B", "A", "A"]),
        seq_id=np.array([1, 2, 3, 4]),
        resname=np.array(["ALA", "GLY", "LIG", "HOH"]),
        atom=np.array(["CA", "CA", "C1", "O"]),
        element=np.array(["C", "C", "C", "O"]),
        altloc=np.array(["."] * 4),
        coord=np.zeros((4, 3)),
        hetatm=np.array([False, False, True, True]),
        in_polymer=np.array([True, True, False, False]),
    )
    supplied = _prediction_structure(full, "A", (1,))
    assert supplied.residues() == [("A", 1, "ALA")]
    assert not supplied.ligand.any()
    assert all(
        not value.flags.writeable
        for value in vars(supplied).values()
        if isinstance(value, np.ndarray)
    )
    with pytest.raises(ValueError, match="read-only"):
        supplied.coord[0, 0] = 1.0

    # A cleared WRITEABLE flag was not a guarantee: NumPy lets the owner of a buffer set it
    # back, and a review did exactly that and wrote to `coord` in place. The arrays are now
    # views onto `bytes`, so the flag cannot be restored on the view or on its base either.
    for value in vars(supplied).values():
        if isinstance(value, np.ndarray):
            with pytest.raises(ValueError, match="WRITEABLE"):
                value.setflags(write=True)
            with pytest.raises(ValueError, match="WRITEABLE"):
                value.base.setflags(write=True)


def test_orthosteric_state_uses_only_contacting_vocabulary_components(manifest):
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    vocab = manifest["orthosteric_vocabulary"]
    assert set(vocab) == {"state_components", "additives"}
    assert not set(vocab["state_components"]) & set(vocab["additives"])

    xray = frozen["targets"]["cardiac_myosin_site1_sensitivity_xray"]["orthosteric_state"]
    xray_spec = next(
        s for s in manifest["targets"] if s["id"] == "cardiac_myosin_site1_sensitivity_xray"
    )
    assert xray_spec["state"]["matched"] is False
    assert xray["apo"]["state_components"] == ["ADP", "MG", "VO4"]
    assert xray["holo"]["state_components"] == ["ADP", "BEF", "MG"]
    assert xray["holo"]["additives"] == ["SO4"]
    assert xray["matches_apo"] is False

    omecamtiv = frozen["targets"]["cardiac_myosin_site1_omecamtiv"]["orthosteric_state"]
    omecamtiv_spec = next(
        s for s in manifest["targets"] if s["id"] == "cardiac_myosin_site1_omecamtiv"
    )
    assert omecamtiv_spec["state"]["matched"] is True
    assert omecamtiv["holo"]["additives"] == ["DMS"]
    assert omecamtiv["matches_apo"] is True
    site2 = frozen["targets"]["cardiac_myosin_site2_corrected"]["orthosteric_state"]
    assert site2["matches_apo"] is True


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


def test_verify_is_exact_and_recursive():
    """Metadata and unknown keys are part of the freeze, not ignored decoration."""
    import copy
    import json

    recorded = json.loads(benchmark.FROZEN.read_text())
    mutations = []
    changed_date = copy.deepcopy(recorded)
    changed_date["frozen_on"] = "2099-01-01"
    mutations.append((changed_date, "frozen_on"))
    top_level = copy.deepcopy(recorded)
    top_level["planted"] = True
    mutations.append((top_level, "planted"))
    per_target = copy.deepcopy(recorded)
    per_target["targets"]["kras_g12c_corrected"]["planted"] = True
    mutations.append((per_target, "targets.kras_g12c_corrected.planted"))

    for mutated, path in mutations:
        problems = benchmark.verify(frozen=mutated)
        assert any(path in problem for problem in problems), (path, problems)


@pytest.mark.network
def test_methods_and_the_benchmark_agree_on_the_node_set(manifest):
    """ADR 0010 clause 1: the node set is every modelled residue of the frozen chain.

    Two code paths compute it independently. `allo.inputs.apo_input` is what a *method*
    receives, and counts modelled polymer residues; `benchmark.derive` sets `n_residues`,
    the denominator of label prevalence and of every hypergeometric baseline, and counts
    residues carrying a CA atom. Those are the same set only while every modelled residue
    has a CA — true on all 11 scoreable arms today, but nothing made it true.

    If they ever diverge, methods are scored against a denominator that is not the node set
    they were given, and no other test would notice. This is also the guard on ADR 0010
    itself: silently trimming a domain inside the loading code fails here.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    from allo.inputs import apo_input

    for target, derived in frozen["targets"].items():
        supplied = apo_input(target)
        given = supplied.residues
        assert list(given) == derived["residue_ids"]
        assert len(given) == derived["n_residues"], (
            f"{target}: methods receive {len(given)} nodes but the benchmark scores against "
            f"n_residues={derived['n_residues']}"
        )
        structure = supplied.structure
        assert set(structure.chain.tolist()) == {supplied.chain}
        assert not structure.ligand.any()
        assert not np.any(structure.resname == "HOH")
        assert {number for _, number, _ in structure.residues()} == set(given)
        for array in vars(structure).values():
            if isinstance(array, np.ndarray):
                assert not array.flags.writeable
        with pytest.raises(ValueError, match="read-only"):
            structure.coord[0, 0] = 0.0

    trimmed = apo_input("bcr_abl1_trimmed")
    assert trimmed.residues[0] == 261
    assert trimmed.residues[-1] == 512
    assert set(trimmed.active_site) <= set(trimmed.residues)


def test_modified_residues_are_parent_normalized_before_prediction():
    """ADR 0006: M3L contributes lysine topology, not trimethyl-group contact edges."""
    from allo.inputs import apo_input

    supplied = apo_input("cardiac_myosin_site1_sensitivity_xray")
    for number in (129, 549):
        residue = (supplied.structure.chain == "A") & (supplied.structure.seq_id == number)
        assert set(supplied.structure.resname[residue]) == {"LYS"}
        assert not {"CM1", "CM2", "CM3"} & set(supplied.structure.atom[residue])
        assert set(supplied.structure.atom[residue]) == {
            "N",
            "CA",
            "C",
            "O",
            "CB",
            "CG",
            "CD",
            "CE",
            "NZ",
        }


def test_the_pair_audit_covers_every_frozen_arm_and_records_its_command():
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    audit = (
        benchmark.ROOT / "docs" / "benchmark" / "evidence" / "allosteric-pair-audit.md"
    ).read_text()
    assert "UV_CACHE_DIR=/tmp/allo-uv-cache uv run python -" in audit
    assert "ARMS = sorted(frozen)" in audit
    for target in frozen["targets"]:
        assert f"`{target}`" in audit, f"audit has no result row for {target}"
    assert not re.search(r"\b(?:eight|ten) (?:frozen|scoreable|current) arms\b", audit)
    assert "clean 2×2" not in audit
    assert "is caused by the ATP-site ligand swap" not in audit


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

    from allo.groundtruth.structures import fetch_mmcif
    from allo.inputs import RAW
    from allo.structure.pdb import contacts, parse_mmcif

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
