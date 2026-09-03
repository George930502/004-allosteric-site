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
    # Counted, because every assertion below is inside the loop: a filter that matched
    # everything, or an emptied source, would make this test pass by asserting nothing.
    checked = 0
    for target in manifest["targets"]:
        checked += 1
        assert {"id", "tier", "protein", "site", "apo", "holo"} <= set(target)
        assert target["tier"] in {"mandated", "corrected", "sensitivity"}
        assert {"pdb", "chain"} <= set(target["apo"])
        assert {"pdb", "chain"} <= set(target["holo"])
    assert checked, "the manifest declared no target, so this asserted nothing"


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
    """If CHALLENGE.md is ever re-read and differs, this fails rather than drifting.

    The organisers sanctioned documented substitution on 2026-09-02, and one arm uses it:
    the cardiac myosin holo is `9GZ2` and not the `6C1H` of Table 1 (ADR 0031). So the
    assertion is not "the manifest equals the table". It is "the manifest equals the table
    once every declared substitution is put back", which fails on an undeclared change and
    passes on a declared one.
    """
    table = CHALLENGE.read_text()
    mandated = [t for t in manifest["targets"] if t["tier"] == "mandated"]
    tabled = {
        t["id"]: t.get("substituted_from", {}).get("holo", t["holo"]["pdb"]) for t in mandated
    }
    assert {(t["apo"]["pdb"], tabled[t["id"]]) for t in mandated} == {
        ("4OBE", "6OIM"),
        ("1OPL", "5MO4"),
        ("5TBY", "6C1H"),
    }
    for target in mandated:
        substituted = target.get("substituted_from", {})
        assert not substituted or substituted.get("reason"), (
            f"{target['id']} substitutes an accession and records no reason"
        )
        for pdb in (target["apo"]["pdb"], tabled[target["id"]]):
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
    assert not (excluded & set(frozen["targets"]))
    # `excluded` is empty since ADR 0031 exposed the cardiac myosin arm, so the line above
    # is vacuous on its own. This is what stops it passing vacuously: every manifest arm
    # that is not excluded has to be in the freeze, and nothing else may be.
    assert {t["id"] for t in manifest["targets"]} - excluded == set(frozen["targets"])


def test_frozen_assembly_is_biological_metadata_not_asymmetric_unit_count(manifest):
    """Clause (v) asks the two members to model the same oligomeric state.

    One arm fails it and says so: `5TBY` deposits the hexameric interacting-heads motif and
    `9GZ2` is monomeric (ADR 0031). A failure is admissible only when the manifest declares
    it and states both copy counts, so this asserts the declaration, not the equality.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    declared = {t["id"]: t.get("assembly_exception", "") for t in manifest["targets"]}
    for name, target in frozen.items():
        apo = target["apo_site_occupancy"]
        holo = target["holo_site_occupancy"]
        assert "polymer_chains" not in apo and "polymer_chains" not in holo
        assert apo["biological_assembly"]["id"] == "1"
        assert holo["biological_assembly"]["id"] == "1"
        agreement = target["assembly_agreement"]
        assert (agreement["exception"] or "") == declared[name], f"{name}: freeze/manifest differ"
        copies = (
            apo["biological_assembly"]["selected_chain_entity_copies"],
            holo["biological_assembly"]["selected_chain_entity_copies"],
        )
        assert agreement["selected_target_copies_match"] == (copies[0] == copies[1])
        if agreement["selected_target_copies_match"] and agreement["polymer_composition_matches"]:
            assert not agreement["exception"], f"{name}: declares an exception it does not need"
            continue
        note = agreement["exception"]
        assert note, f"{name}: the two assemblies differ with no declared exception"
        assert f"apo {copies[0]}, holo {copies[1]}" in note, (
            f"{name}: the declared exception does not state both copy counts"
        )
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
    readme = (benchmark.ROOT / "docs" / "benchmark" / "primary" / "README.md").read_text()
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
    "bcr_abl1_mandated": {"unmapped": ["A:ILE521", "A:VAL525", "A:LEU529"], "outside": []},
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
    # An accession the manifest substituted away from is still referenced: the organisers
    # asked that substitutions be documented, and the evidence for one is the file it
    # replaced. `6C1H` reaches the store this way and no other (ADR 0031).
    named |= {
        spec["substituted_from"]["holo"]
        for path in BENCHMARK_MANIFESTS
        if path.exists()
        for spec in yaml.safe_load(path.read_text())["targets"]
        if "substituted_from" in spec
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
def test_versioned_archive_reproduces_every_pinned_structure():
    """ADR 0014 option 1: every decompressed versioned artifact matches its frozen hash.

    Walks BOTH manifests. It covered the primary set's 8 entries only until 2026-08-24, while
    `docs/benchmark/primary/README.md` claimed the archive test downloads every URL. The secondary
    set's 18 pinned URLs were therefore never fetched, so its offline fallback and its
    versioned provenance had no common check.
    """
    import gzip
    import hashlib
    import urllib.request

    from allo.groundtruth.manifest import read_manifest
    from allo.inputs import MANIFEST, SECONDARY_MANIFEST

    checked = 0
    for path in (MANIFEST, SECONDARY_MANIFEST):
        provenance = read_manifest(path)["structure_provenance"]
        for pdb, record in sorted(provenance.items()):
            checked += 1
            assert record["version"] in record["url"]
            request = urllib.request.Request(record["url"], headers={"User-Agent": "allo/0.1"})
            with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310
                restored = gzip.decompress(response.read())
            assert hashlib.sha256(restored).hexdigest() == record["sha256"], pdb
    assert checked == 27, f"expected 27 pinned structures across both sets, fetched {checked}"


def test_the_scoring_universe_excludes_what_scores_by_construction():
    """ADR 0011. Nothing that a connectivity score ranks top by construction is a negative.

    Removing propagation-source residues from the positives and leaving them in the
    negatives penalises the method class the challenge asked for -- 44-62 % of AUC-PR at a
    fixed real effect -- and penalises no other. Both classes lose them, or neither does.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for target, derived in frozen["targets"].items():
        checked += 1
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
    assert checked, "the freeze carried no target, so this asserted nothing"


def test_the_manifest_pins_the_same_apo_bytes_as_the_freeze(manifest):
    """`apo_input` fails closed on the manifest hash, so it has to equal the frozen one.

    Two records of the same fact drift. This is the cheapest way to notice.
    """
    import json

    frozen = json.loads(benchmark.FROZEN.read_text())
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        checked += 1
        pdb = spec["apo"]["pdb"]
        assert spec["apo"].get("sha256") == frozen["targets"][spec["id"]]["hashes"][pdb], (
            f"{spec['id']}: manifest and freeze disagree on {pdb}'s bytes"
        )
    assert checked, "every target was excluded, so this asserted nothing"


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
        bfactor=np.zeros(4),
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
    has a CA — true on all fifteen arms of both freezes today, but nothing made it true.

    If they ever diverge, methods are scored against a denominator that is not the node set
    they were given, and no other test would notice. This is also the guard on ADR 0010
    itself: silently trimming a domain inside the loading code fails here.

    **Both freezes, since 2026-09-03.** ADR 0010 names this test as its enforcement and the
    test read the primary freeze only, so all nine secondary arms were unenforced -- two
    thirds of the arms, and the whole tier the generalisation claim rests on. Found by codex
    pass 9. The ADR's own docstring said "11 scoreable arms" while the two freezes hold
    fifteen, which is the same defect stated in prose.
    """
    import json

    frozen = {
        "targets": {
            **json.loads(benchmark.FROZEN.read_text())["targets"],
            **json.loads(benchmark.SECONDARY_FROZEN.read_text())["targets"],
        }
    }
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
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        checked += 1
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
    assert checked, "every target was excluded, so this asserted nothing"


def test_the_four_secondary_clauses_still_give_the_verdicts_the_readme_prints(manifest):
    """Clauses (ix)-(xii) as a DIAGNOSTIC on the primary set. Added 2026-09-03.

    `docs/benchmark/primary/README.md` section 1 applies the secondary set's four
    selection clauses to this set and prints four verdicts. They are diagnostic: no arm is
    admitted or rejected on them. Until now they were prose only, and prose does not fail
    when the set moves. Two of the six arms changed accession on 2026-09-02 and nothing
    re-derived these rows.

    The failure mode this pins is not hypothetical. A stale falsifier survived a re-freeze
    in `tests/test_secondary.py`, where a comment justified a live assertion with an arm
    that contacts ZERO labels, having read a 16.0 A DISTANCE as a count of 16 labels.

    Clause (ix) is left out. It needs the biological assembly and the effector lining, and
    `tests/test_secondary.py` already measures it against the shared holo entries.
    """
    import json
    import re

    from allo.groundtruth.structures import EVAL_CACHE

    frozen = json.loads(benchmark.FROZEN.read_text())

    # (x) apo occupant classification -- "passes by construction". It is clause (iii)
    # restricted to the scoreable set, so no apo component may touch a scoreable label.
    for name, values in frozen["targets"].items():
        contacted = values["apo_site_occupancy"]["scoreable_labels_contacted"]
        assert contacted == 0, (
            f"{name}: clause (x) now FAILS -- an apo component contacts {contacted} "
            "scoreable labels. The README prints 'passes by construction'"
        )

    # (xi) structure admission -- "fails on two entries", and the README names which two
    # and every resolution. Re-derived from the tracked mmCIFs, never from the prose.
    ceilings, measured, failing = {"ELECTRON MICROSCOPY": 4.0}, {}, set()
    for accession in frozen["structure_provenance"]:
        for cache in (EVAL_CACHE, EVAL_CACHE.parent / "apo"):
            path = cache / f"{accession}.cif"
            if not path.exists():
                continue
            text = path.read_text(errors="ignore")
            method = re.search(r"_exptl\.method\s+(?:'([^']*)'|\"([^\"]*)\"|(\S+))", text)
            assert method, f"{accession}: no _exptl.method in the tracked mmCIF"
            method = "".join(part for part in method.groups() if part)
            key = (
                "_em_3d_reconstruction.resolution"
                if "ELECTRON" in method
                else ("_refine.ls_d_res_high")
            )
            value = re.search(rf"{re.escape(key)}\s+([\d.]+)", text)
            assert value, f"{accession}: no {key} in the tracked mmCIF"
            measured[accession] = (float(value.group(1)), method)
            if float(value.group(1)) > ceilings.get(method, 2.5):
                failing.add(accession)
            break
        else:  # pragma: no cover - a missing cache is a setup failure, not a verdict
            raise AssertionError(f"{accession}: no tracked mmCIF under data/raw/")

    assert failing == {"1OPL", "5TBY"}, (
        f"clause (xi) now fails on {sorted(failing)}, and the README says exactly "
        "{'1OPL', '5TBY'}. Every other pinned entry must clear its method's ceiling"
    )
    assert measured["1OPL"][0] == pytest.approx(3.42), measured["1OPL"]
    assert measured["5TBY"][0] == pytest.approx(20.00), measured["5TBY"]

    # (xii) within-set redundancy -- "fails by design": every protein appears twice,
    # once mandated and once corrected. That is the tier split, not an accident, and if
    # it ever stopped being true the README's justification would stop applying.
    by_protein: dict[str, set[str]] = {}
    for spec in manifest["targets"]:
        if spec.get("status") == "excluded":
            continue
        by_protein.setdefault(spec["protein"], set()).add(spec["tier"])
    assert all(tiers == {"mandated", "corrected"} for tiers in by_protein.values()), (
        f"clause (xii) verdict moved: {by_protein}. The README says it fails by design "
        "because each protein contributes exactly one mandated and one corrected arm"
    )


def test_the_primary_readme_quotes_the_rmsd_the_freeze_derives():
    """A number a reader classifies an arm with must come from the freeze, not from prose.

    Added 2026-09-03. The page said `bcr_abl1_mandated` has a pocket-lining RMSD of 0.50 A,
    one sentence before CryptoBench's 2 A cryptic-site criterion, so the arm read as
    maximally pre-formed. The freeze says 26.31 A -- a factor of 52, and the opposite
    conclusion. The value was stale from before ADR 0029 moved that arm to `1OPL` chain B,
    and the correct one had been sitting in the review tree since 2026-09-02.
    """
    import json

    from allo.inputs import ROOT

    frozen = json.loads((ROOT / "docs/benchmark/primary/frozen.json").read_text())["targets"]
    page = (ROOT / "docs/benchmark/primary/README.md").read_text()
    header = "| arm | core RMSD | pocket-lining RMSD | pocket max |"
    assert header in page, "the re-derived RMSD table is gone from the page"
    table = page[page.index(header) :].split("\n\n")[0].splitlines()
    for arm, values in frozen.items():
        rmsd = values["apo_holo_rmsd"]["pocket_lining"]
        rows = [one for one in table if one.startswith(f"| `{arm}` |")]
        assert len(rows) == 1, f"{arm} has {len(rows)} rows in the RMSD table"
        assert f"{rmsd:.2f}" in rows[0], (
            f"{arm}: the table row is {rows[0].strip()}, and the freeze says {rmsd}"
        )


def test_the_primary_readme_quotes_the_transplant_the_freeze_derives():
    """The crypticity table too, and the note beside it was wrong about its own source.

    Added 2026-09-03 by the round-5 audit. A note added the day before declared two rows of
    this table stale and then asserted that neither quantity is in `frozen.json`, so neither
    could be re-derived. Both are, per arm, for all six arms: `bcr_abl1_mandated` reads
    2.63 A and 0/31, not 2.60 A, and `cardiac_myosin_mandated` was missing entirely. A claim
    that a number cannot be derived is itself a claim and needs the same check as the number.
    """
    import json

    from allo.inputs import ROOT

    frozen = json.loads((ROOT / "docs/benchmark/primary/frozen.json").read_text())["targets"]
    page = (ROOT / "docs/benchmark/primary/README.md").read_text()
    header = (
        "| Arm                        | Nearest apo atom to the transplanted effector | Clashes |"
    )
    assert header in page, "the crypticity table is gone from the page"
    table = page[page.index(header) :].split("\n\n")[0].splitlines()
    for arm, values in frozen.items():
        rows = [one for one in table if one.startswith(f"| `{arm}`")]
        assert len(rows) == 1, f"{arm} has {len(rows)} rows in the crypticity table"
        cells = [cell.strip() for cell in rows[0].split("|")]
        assert cells[2] == f"{values['transplant_min_distance']:.2f} Å", (
            f"{arm}: the row says {cells[2]}, the freeze says {values['transplant_min_distance']}"
        )
        assert cells[3] == values["transplant_clashes"], (
            f"{arm}: the row says {cells[3]}, the freeze says {values['transplant_clashes']}"
        )


def test_no_modified_residue_reaches_a_prediction_structure():
    """ADR 0006 clause 3, swept over every frozen arm instead of two named residues.

    The ADR says a target "cannot be added on the untested path" and names a test as the
    reason. That test pinned M3L at 129 and 549 on one arm by number, so it could not see a
    different modification on a different arm, and it left the suite with that arm in
    `0f1fe3f`. `hiv_rt` then entered the secondary set carrying `CSD` -- oxidised cysteine --
    at 280, and took the hydropathy and RSA fallbacks in `allo.structure.properties` silently
    for as long as it was frozen.

    So the guard asks the general question. Every residue a method receives must carry a
    standard three-letter name and no atom the parent does not have. Both property tables are
    keyed on exactly that set, and both now raise rather than substitute, so this is what
    keeps them reachable.
    """
    import numpy as np

    from allo.inputs import (
        _PARENT_TOPOLOGY,
        _THREE_TO_ONE,
        SECONDARY_MANIFEST,
        apo_input,
        load,
    )
    from allo.structure.properties import KYTE_DOOLITTLE, MAX_ACCESSIBLE_AREA

    standard = set(KYTE_DOOLITTLE)
    assert standard == set(MAX_ACCESSIBLE_AREA), "the two property tables disagree on the set"

    arms = [t["id"] for t in load()["targets"]]
    arms += [t["id"] for t in load(SECONDARY_MANIFEST)["targets"]]
    seen: set[str] = set()
    for arm in arms:
        structure = apo_input(arm).structure
        names = {str(n) for n in np.unique(structure.resname[structure.protein])}
        seen |= names
        assert names <= standard, (
            f"{arm}: {sorted(names - standard)} reaches a prediction structure unmapped. "
            "Add it to allo.inputs._PARENT_TOPOLOGY with its parent_comp_id and the atoms "
            "the parent does not have."
        )
    assert seen, "no arm loaded, so this asserted nothing"

    # Every entry in the table is live and correctly shaped: a real parent, and the sequence
    # map agrees with the topology map. A table entry that names a parent the property tables
    # do not hold would move the failure from here to a scoring run.
    for modified, (parent, added) in _PARENT_TOPOLOGY.items():
        assert parent in standard, f"{modified} maps to non-standard parent {parent}"
        assert added, f"{modified} lists no PTM-specific atom"
        assert _THREE_TO_ONE.get(modified) == _THREE_TO_ONE[parent], (
            f"{modified}: the sequence map and the topology map disagree on the parent"
        )


def test_the_altloc_policy_is_the_one_this_adr_states():
    """ADR 0045. Three code paths answered the alternate-conformer question three ways.

    `evaluation_graph` takes the LAST conformer's CA, `_chain_ca` takes the FIRST, and the
    contact graph and the SASA integration consult no altloc field at all. None of the three
    was a stated policy and two of them disagree, so nothing would have noticed the gap
    widening. ADR 0045 states the policy in force, measures it, and declines to change it
    because the effect is uniform across methods and inside the rounding digit.

    This is the pin. Every number in that ADR's three tables is re-derived here, so the
    disagreement can neither widen nor silently vanish.
    """
    import dataclasses

    import numpy as np

    from allo.benchmark import _chain_ca
    from allo.inputs import apo_input
    from allo.scoring.nulls import evaluation_graph
    from allo.structure.pdb import Structure
    from allo.structure.properties import solvent_accessibility

    # arm -> (CA disagreements, largest in A, altloc-only edges, RSA moves, largest RSA move)
    expected = {
        "smyd3": (15, 0.1003, 14, 56, 0.1921),
        "glucokinase": (3, 0.0496, 2, 12, 0.2130),
        "ptp1b": (0, 0.0, 0, 2, 0.0933),
        "ecoli_cps": (0, 0.0, 2, 22, 0.1572),
    }
    for arm, (n_ca, max_ca, altloc_edges, n_rsa, max_rsa) in expected.items():
        apo = apo_input(arm)
        structure = apo.structure
        altloc = np.asarray([str(a) for a in structure.altloc])
        assert not np.isin(altloc, [".", "?", ""]).all(), f"{arm} has no altloc to measure"

        graph = evaluation_graph(apo)
        first_wins = _chain_ca(structure, apo.chain)
        gaps = [
            float(np.linalg.norm(graph.ca_coord[graph.position[r]] - first_wins[r]))
            for r in graph.order
            if r in first_wins
        ]
        assert sum(gap > 1e-9 for gap in gaps) == n_ca, arm
        assert round(max(gaps), 4) == max_ca, (arm, round(max(gaps), 4))

        primary = np.isin(altloc, [".", "?", "", "A"])
        kept = Structure(
            **{
                field.name: (
                    getattr(structure, field.name)[primary]
                    if isinstance(getattr(structure, field.name), np.ndarray)
                    else getattr(structure, field.name)
                )
                for field in dataclasses.fields(structure)
            }
        )
        without = evaluation_graph(dataclasses.replace(apo, structure=kept))
        assert list(graph.order) == list(without.order), f"{arm}: the node set is not stable"
        edges = {(r, n) for r, ns in zip(graph.order, graph.adjacency, strict=True) for n in ns}
        primary_edges = {
            (r, n) for r, ns in zip(without.order, without.adjacency, strict=True) for n in ns
        }
        assert len(edges - primary_edges) == altloc_edges, (arm, len(edges - primary_edges))
        assert not primary_edges - edges, (
            f"{arm}: a primary-only edge exists, which the geometry forbids -- a union of "
            "conformers can only bring atom pairs closer"
        )

        with_all = solvent_accessibility(apo)
        primary_only = solvent_accessibility(dataclasses.replace(apo, structure=kept))
        moves = [abs(with_all[r] - primary_only[r]) for r in with_all]
        assert sum(move > 1e-6 for move in moves) == n_rsa, (arm, sum(m > 1e-6 for m in moves))
        assert round(max(moves), 4) == max_rsa, (arm, round(max(moves), 4))


def test_same_site_labels_are_not_negatives_in_a_sibling_arm():
    """ADR 0011 names this test as the second half of its rule. It did not exist until round 6.

    The first half, `test_the_scoring_universe_excludes_what_scores_by_construction`, is
    within-arm: a residue that a connectivity score ranks top by construction is in neither
    class. The second half is across arms of the same protein. Two arms of one protein are two
    entries of the same molecule, so a residue the ground truth calls allosteric in one of them
    is not a negative in the other merely because the other's holo did not resolve it.

    Measured at the time of writing: the rule holds. One `bcr_abl1_corrected` label is absent
    from its sibling's positive and excluded sets, and it is absent because that residue is not
    modelled in the sibling at all, so it is in neither class there either.
    """
    import json

    from allo.inputs import apo_input

    frozen = json.loads(benchmark.FROZEN.read_text())["targets"]
    siblings: dict[str, list[str]] = {}
    for arm in frozen:
        siblings.setdefault(arm.rsplit("_", 1)[0], []).append(arm)
    pairs = [(a, b) for arms in siblings.values() for a in arms for b in arms if a != b]
    assert pairs, "no protein has two arms, so this asserted nothing"

    for source, other in pairs:
        labels = set(frozen[source]["scoreable_label_residues"])
        neither = (
            labels
            - set(frozen[other]["scoreable_label_residues"])
            - set(frozen[other]["excluded_from_scoring"])
        )
        scored_as_negative = neither & set(apo_input(other).residues)
        assert not scored_as_negative, (
            f"{other} scores {len(scored_as_negative)} of {source}'s labels as negatives; "
            "ADR 0011 requires both classes to lose a residue or neither"
        )


def test_no_document_cites_a_test_the_suite_does_not_define():
    """Round 6's two largest findings were declarations describing code that is not there.

    ADR 0006 named a guard that does not exist, so the path it promised was closed had been
    open since the arm that carried the real test left the suite. A sweep then found four more
    citations of the same shape: three stale names -- a test renamed, two consolidated into one
    -- and `simulate.py` naming a test that pins its ranks against the shipped statistic, which
    nobody had written. A citation that resolves to nothing is worse than no citation, because
    it reads as a guarantee.

    So the class is closed rather than the five instances. Any tracked document or comment that
    names a `test_*` symbol must name one the suite defines.
    """
    import ast
    import pathlib
    import re
    import subprocess

    root = pathlib.Path(benchmark.ROOT)
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, cwd=root, check=True
    ).stdout.split()

    defined = set()
    modules = set()
    for name in (path for path in tracked if path.startswith("tests/") and path.endswith(".py")):
        modules.add(pathlib.Path(name).stem)
        for node in ast.walk(ast.parse((root / name).read_text())):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith(
                "test"
            ):
                defined.add(node.name)
    assert len(defined) > 100, "the suite did not parse"

    # A citation may wrap across lines inside a Markdown paragraph, so join a line that ends
    # mid-identifier to the next one before matching. The round-6 sweep read three real
    # citations as missing for exactly this reason.
    unwrap = re.compile(r"(test_[a-z0-9_]*[a-z0-9_])\n\s*([a-z0-9_]+)")
    symbol = re.compile(r"\btest_[a-z0-9_]{4,}\b")
    # The one deliberate reference to a test that no longer exists. ADR 0006 records the guard
    # it wrongly claimed to have, by name, because naming it is the correction.
    allowed = {"test_modified_residues_are_parent_normalized_before_prediction"}

    missing: dict[str, set[str]] = {}
    for name in tracked:
        path = pathlib.Path(name)
        # Third-party skill documentation is not this repository's claim to keep true.
        if path.suffix not in {".md", ".py", ".yaml", ".yml", ".txt", ".json"}:
            continue
        if name.startswith(".claude/"):
            continue
        try:
            text = (root / name).read_text()
        except (OSError, UnicodeDecodeError):
            continue
        while unwrap.search(text):
            text = unwrap.sub(r"\1\2", text)
        for match in symbol.finditer(text):
            cited = match.group(0)
            # A citation spelled with its extension names a FILE, and a removed file is
            # legitimate history: ADR 0037 records `tests/test_method.py` leaving with the
            # method layer. A bare name is a claim about a symbol, and that is what this
            # checks. `modules` covers the bare spelling of a module that still exists.
            if text[match.end() : match.end() + 3] == ".py":
                continue
            if cited in defined or cited in modules or cited in allowed:
                continue
            missing.setdefault(cited, set()).add(name)

    assert not missing, "documents cite tests that do not exist: " + "; ".join(
        f"{cited} in {sorted(where)}" for cited, where in sorted(missing.items())
    )


@pytest.mark.network
def test_the_claim_reference_is_every_detected_cavity():
    """Which pocket set is `cavity_volume`? Settled by measurement, 2026-09-03.

    Codex pass 9 showed that the frozen reference was a NAME a caller supplied, so
    `compare_methods` now derives it. Deriving it needs a definition, and choosing one after
    seeing a result is the hyperparameter this layer exists to prevent. So the two candidate
    definitions were both measured against the triple ADR 0025 and the manifest already quote:

    | pocket set                        | kras   | abl1   | myosin |
    | --------------------------------- | ------ | ------ | ------ |
    | frozen decoys plus the site pocket | 0.0695 | 0.3304 | 0.0046 |
    | **every detected cavity**         | 0.0715 | 0.3236 | 0.0046 |
    | quoted                            | 0.0715 | 0.3236 | 0.0046 |

    Every detected cavity reproduces it and the freeze-only set does not, so the reference
    cannot be rebuilt from `frozen.json`: `excluded_by_halo` is stored as identifiers with no
    lining and no volume. This test runs the detector and pins the count, which is what makes
    a detector drift a failure here rather than a silent redefinition of the baseline.
    """
    import json
    import math

    from allo.scoring.harness import EVALUATION_FROZEN, frozen_reference

    frozen = json.loads(EVALUATION_FROZEN.read_text())["targets"]
    arm = "kras_g12c_corrected"
    reference = frozen_reference(arm)
    assert len(reference) == frozen[arm]["n_candidates"]
    assert all(math.isfinite(v) and v >= 0 for v in reference.values())
    # The site pocket lines candidates, so the reference is not the all-zero vector the pass
    # substituted for it.
    assert max(reference.values()) > 0
