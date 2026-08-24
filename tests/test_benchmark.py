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
        "orthosteric_vocabulary",
        "structure_provenance",
        "label_footprints",
        "targets",
    } == set(frozen)
    assert excluded and not (excluded & set(frozen["targets"]))


def test_frozen_assembly_is_biological_metadata_not_asymmetric_unit_count():
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    for target in frozen.values():
        apo = target["apo_site_occupancy"]
        holo = target["holo_site_occupancy"]
        assert "polymer_chains" not in apo and "polymer_chains" not in holo
        assert apo["biological_assembly"]["id"] == "1"
        assert holo["biological_assembly"]["id"] == "1"
        assert (
            apo["biological_assembly"]["selected_chain_entity_copies"]
            == holo["biological_assembly"]["selected_chain_entity_copies"]
        )
        agreement = target["assembly_agreement"]
        assert agreement["selected_target_copies_match"]
        assert agreement["polymer_composition_matches"] or agreement["exception"]
    assert frozen["kras_g12c_mandated"]["apo_site_occupancy"]["biological_assembly"] == {
        "id": "1",
        "polymer_entity_copies": {"1": 1},
        "selected_chain_entity_copies": 1,
    }
    # 4OBE's asymmetric unit holds two KRAS copies; assembly 1 is the monomer. The point of
    # the check is that the freeze records the biological assembly and not the ASU count.
    assert frozen["kras_g12c_corrected"]["apo_site_occupancy"]["biological_assembly"] == {
        "id": "1",
        "polymer_entity_copies": {"1": 1},
        "selected_chain_entity_copies": 1,
    }


def test_the_readme_table_matches_the_freeze():
    """Prose drifts from data silently; this is the cheapest way to stop it."""
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    readme = (benchmark.ROOT / "docs" / "benchmark" / "README.md").read_text()
    rows = {
        line.split("|")[1].strip().strip("`"): line
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
            f"{len(derived['scoreable_label_residues']) / derived['n_candidates'] * 100:.1f} %",
        ):
            assert value in cells, f"{target}: README row missing {value!r}\n  {row}"


# Every label an arm does not score, declared. A label vanishing silently -- through an
# alignment gap or a node-set trim -- would shrink the positive class without anyone seeing.
DECLARED_LABEL_LOSS = {
    "bcr_abl1_corrected": {"unmapped": ["A:VAL525", "A:LEU529"], "outside": []},
}


def test_every_arm_accounts_for_the_labels_it_does_not_score(manifest):
    """Ground truth may be lost to a construct or to a trim, but never unaccounted for.

    Two channels drop a label and they are not interchangeable. `unmapped` holds holo
    residues with no counterpart in the apo model - `bcr_abl1_corrected` loses Val525 and
    Leu529 because `2G2H` stops at 523. `labels_outside_node_set` holds residues the apo
    *does* model but the manifest node set excludes; no current arm loses a label that way.

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
        key = (spec[name]["site"], holo["pdb"], holo["chain"], holo["ligand"])
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
        assert not cut, (
            f"{name} drops labels {sorted(cut)} from the node set - under ADR 0010 the node "
            "set is the whole modelled chain, so no label can fall outside it"
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
    single["cardiac_myosin_corrected"]["label_residues"].pop()
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

    from allo.groundtruth.structures import STRUCTURES, fetch_mmcif
    from allo.structure.pdb import sha256

    def refuse(*args, **kwargs):
        raise AssertionError("fetch_mmcif went to the network; the tracked store missed an entry")

    monkeypatch.setattr(urllib.request, "urlopen", refuse)

    pinned: dict[str, str] = {}
    for _, frozen_path in benchmark.SETS.values():
        if not frozen_path.exists():
            continue
        for values in json.loads(frozen_path.read_text())["targets"].values():
            pinned.update(values["hashes"])
    assert pinned, "the freeze pins no hashes, so this test would pass vacuously"
    for pdb, digest in sorted(pinned.items()):
        assert sha256(fetch_mmcif(pdb, tmp_path)) == digest, f"{pdb} did not restore to its pin"

    # The store covers every accession the manifest names, not merely every one the freeze
    # derives: `cardiac_myosin_site1_mandated` is excluded and so pins nothing, but `5TBY`
    # and `6C1H` are the evidence for why it is excluded and have to survive too.
    # Both sets share one store, so both sets define what belongs in it. Checking only the
    # primary manifest would read every secondary entry as an unreferenced stray.
    import yaml

    from allo.inputs import BENCHMARK_MANIFESTS

    named = {
        spec[role]["pdb"]
        for path in BENCHMARK_MANIFESTS
        if path.exists()
        for spec in yaml.safe_load(path.read_text())["targets"]
        for role in ("apo", "holo")
        if role in spec
    }
    del manifest
    # Reached through the evaluation-side root. `allo.inputs` deliberately exports only the
    # apo partition, so there is no prediction-path constant one `/ "holo"` from the answers.
    root = STRUCTURES
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

    for pdb in ("6OIM", "5MO4", "9GZ2", "6C1H", "4OBE", "9GZ3"):
        with pytest.raises(PermissionError, match="apo_input"):
            fetch_mmcif(pdb, tmp_path)


@pytest.mark.network
def test_versioned_archive_reproduces_every_pinned_structure(manifest):
    """ADR 0014 option 1: every decompressed versioned artifact matches its frozen hash."""
    import gzip
    import hashlib
    import urllib.request

    provenance = manifest["structure_provenance"]
    assert len(provenance) == 8
    for pdb, record in sorted(provenance.items()):
        assert record["version"] in record["url"]
        request = urllib.request.Request(record["url"], headers={"User-Agent": "allo/0.1"})
        with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310
            restored = gzip.decompress(response.read())
        assert hashlib.sha256(restored).hexdigest() == record["sha256"], pdb


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


def test_label_footprints_are_an_authority_not_a_prose_count(manifest):
    """Each arm's ground truth must reconcile to an independently re-derived holo footprint."""
    import json

    from allo.groundtruth.labels import pocket_residues
    from allo.groundtruth.structures import fetch_mmcif, parse_mmcif

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    scoreable = [spec for spec in manifest["targets"] if spec.get("status") != "excluded"]
    assert set(manifest["label_footprints"]) == {
        f"{spec['holo']['pdb']}:{spec['holo']['chain']}:{spec['holo']['ligand']}"
        for spec in scoreable
    }

    parsed = {}
    for key, authority in manifest["label_footprints"].items():
        pdb, chain, ligand = key.split(":")
        if pdb not in parsed:
            parsed[pdb] = parse_mmcif(fetch_mmcif(pdb, benchmark.EVAL_CACHE), pdb)
        live = [
            f"{c}:{name}{number}"
            for c, number, name in pocket_residues(
                parsed[pdb], ligand, manifest["defaults"]["contact_cutoff_angstrom"], chain
            )
            if c == chain
        ]
        assert live == authority, key

    assert benchmark._label_accounting_problems(frozen, manifest) == []


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
    """Catalytic state is decided by vocabulary components that touch the active site.

    Effectors are never state components, and a component the vocabulary does not name makes
    the freeze fail rather than pass silently.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    vocab = manifest["orthosteric_vocabulary"]
    assert set(vocab) == {"state_components", "additives"}
    assert not set(vocab["state_components"]) & set(vocab["additives"])

    # Matched: 9GZ3 and 9GZ2 hold the same Mg-ADP-Pi, and the effector is excluded from state.
    myosin = frozen["targets"]["cardiac_myosin_corrected"]["orthosteric_state"]
    assert myosin["apo"]["state_components"] == ["ADP", "MG", "PO4"]
    assert myosin["holo"]["state_components"] == ["ADP", "MG", "PO4"]
    assert myosin["matches_apo"] is True
    assert "XB2" not in myosin["holo"]["state_components"]

    # Unmatched: 1OPL's ATP site holds P16, 5MO4's holds nilotinib.
    abl1 = frozen["targets"]["bcr_abl1_mandated"]["orthosteric_state"]
    assert abl1["apo"]["state_components"] == ["P16"]
    assert abl1["holo"]["state_components"] == ["NIL"]
    assert abl1["matches_apo"] is False

    for name, derived in frozen["targets"].items():
        for half in ("apo", "holo"):
            named = set(derived["orthosteric_state"][half]["state_components"])
            assert named <= set(vocab["state_components"]), f"{name}: {half} names an unknown state"


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

    from allo.groundtruth.structures import EVAL_CACHE, fetch_mmcif, parse_mmcif
    from allo.structure.pdb import contacts

    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        holo = parse_mmcif(fetch_mmcif(spec["holo"]["pdb"], EVAL_CACHE), spec["holo"]["pdb"])
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
