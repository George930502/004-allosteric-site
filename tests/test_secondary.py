"""The four admission clauses that bind the secondary set, and the ledger behind them.

Clauses (i)-(viii) bind both benchmark sets, but `tests/test_benchmark.py` applies them to
the PRIMARY manifest only: its `manifest` fixture is `benchmark.load()`, which resolves to
`MANIFEST`, and every other test there reads `benchmark.FROZEN`. So the eight clauses are
enforced on six primary arms and on nothing else. `test_the_secondary_manifest_declares_what_
the_eight_clauses_require` below closes the part of that gap which is checkable from the
secondary artifacts alone.

The four clauses here exist because the secondary set was SELECTED from a pool, and a
selection rule only means something where there is a pool (ADR 0009's reasoning, applied
again in ADR 0021). Every one of them is checked against `frozen.json`, which is derived
from the deposited files, rather than against the prose that claims it -- except clause (ix),
which needs the biological assembly and therefore runs under `make verify`, not `make check`.
"""

from __future__ import annotations

import json

import pytest
import yaml

from allo.benchmark import size_stratified_split
from allo.groundtruth.manifest import read_manifest
from allo.inputs import MANIFEST, ROOT, SECONDARY_MANIFEST

# ADR 0042's own record: the accession, families and PANTHER assignment each arm was
# resolved to, at the releases the manifests pin. Not on the prediction path -- a test
# is not a prediction module, and `tests/test_no_leakage.py` names this tree too.
CLAUSE_XII_EVIDENCE = ROOT / "docs" / "benchmark" / "review" / "data" / "clause-xii-2026-09-03.json"

SECONDARY = ROOT / "docs" / "benchmark" / "secondary"
FROZEN = SECONDARY / "frozen.json"
SELECTION = SECONDARY / "selection.json"


@pytest.fixture(scope="module")
def frozen() -> dict:
    return json.loads(FROZEN.read_text())


@pytest.fixture(scope="module")
def manifest() -> dict:
    return yaml.safe_load(SECONDARY_MANIFEST.read_text())


@pytest.fixture(scope="module")
def ledger() -> dict:
    return json.loads(SELECTION.read_text())


def test_the_recorded_tiers_are_what_the_seeded_split_returns(frozen, manifest):
    """ADR 0021 section 5 promises nobody chose which targets carry the claim.

    A promise with no code behind it is decoration. Re-run the split from the frozen
    residue counts and require the recorded tiers back. If someone moves one target into
    `development` because the method does badly on it, this fails.
    """
    sizes = {name: values["n_residues"] for name, values in frozen["targets"].items()}
    expected = size_stratified_split(sizes)
    recorded = {spec["id"]: spec["tier"] for spec in manifest["targets"]}
    assert recorded == expected, (
        "recorded tiers are not the seeded size-stratified split -- either the seed moved "
        "or a target was reassigned by hand"
    )
    assert {values["tier"] for values in frozen["targets"].values()} == {
        "development",
        "generalisation",
    }


def test_the_generalisation_tier_is_large_enough_to_reject(frozen):
    """The tier exists to carry a hypothesis test, so it has to be able to fail one.

    A distribution-free one-sample test over N targets has a minimum attainable one-sided
    p of 2^-N. At N = 4 that is 0.0625 and no result can reach alpha = 0.05. This is the
    exact arithmetic that made three primary arms unable to support a cross-target claim
    (ADR 0021, Fact 3), so the same floor is enforced here rather than rediscovered later.
    """
    held_out = [n for n, v in frozen["targets"].items() if v["tier"] == "generalisation"]
    assert len(held_out) >= 5, (
        f"generalisation tier holds {len(held_out)} targets; below 5 the minimum attainable "
        f"one-sided p is 2^-{len(held_out)} = {2 ** -len(held_out):.4f}, so no outcome can "
        "reject at alpha = 0.05 and the tier cannot do the one job it has"
    )


def test_no_two_targets_share_a_pfam_family(manifest):
    """Clause (xii). Per-pair clauses say nothing about a set that is one fold repeated.

    Checked in both directions: inside the secondary set, and against every primary target.
    The cross-set half is what rejected SHP2, which passed clause (ii) and would otherwise
    have been admitted -- it shares PF00017 with BCR-ABL1. The ledger records that.
    """
    families: dict[str, list[str]] = {}
    for spec in manifest["targets"]:
        assert spec.get("pfam"), f"{spec['id']}: no pfam recorded, so clause (xii) is unchecked"
        for family in spec["pfam"]:
            families.setdefault(family, []).append(spec["id"])
    collisions = {f: ids for f, ids in families.items() if len(ids) > 1}
    assert not collisions, f"secondary targets share Pfam families: {collisions}"

    primary = yaml.safe_load(MANIFEST.read_text())
    primary_families: dict[str, list[str]] = {}
    for spec in primary["targets"]:
        assert spec.get("pfam"), f"{spec['id']}: no pfam recorded in the primary manifest"
        for family in spec["pfam"]:
            primary_families.setdefault(family, []).append(spec["id"])
    shared = set(families) & set(primary_families)
    assert not shared, "secondary targets share a Pfam family with the primary set: " + str(
        {f: (families[f], primary_families[f]) for f in sorted(shared)}
    )


def test_every_transferred_label_survives_into_the_node_set(frozen):
    """The on-chain half of clause (ix). It is NOT the clause itself, and the name says so.

    Clause (ix) asks whether the effector is lined by more than one chain. This test cannot
    answer that, and an earlier version of it pretended to: it read `holo_label_footprint`
    and asserted a single chain, but `benchmark.derive` builds that field from
    `labels.holo_residues`, which `groundtruth.labels` already filters to `holo_chain`. The
    assertion could not fail, so an interface site would have passed it in silence.

    Clause (ix) needs coordinates the deposited asymmetric unit does not carry, so the real
    check is `test_clause_ix_holds_on_the_biological_assembly_and_not_only_the_deposited_unit`
    below. That one is `@pytest.mark.network` and runs under `make verify`, not `make check`.

    What IS checkable offline is the consequence a single-chain node set must not have: a
    label that transferred but then fell outside the node set, or failed to map at all.
    Every assertion below can fail.
    """
    for name, values in frozen["targets"].items():
        footprint = values["holo_label_footprint"]
        assert not values["unmapped"], (
            f"{name}: labels {values['unmapped']} do not map into the apo"
        )
        assert not values["labels_outside_node_set"], (
            f"{name}: labels {values['labels_outside_node_set']} fall outside the node set"
        )
        assert len(values["label_residues"]) == len(footprint), (
            f"{name}: {len(footprint)} lining residues but {len(values['label_residues'])} labels"
        )


def test_clause_x_no_apo_occupant_touches_a_label(frozen):
    """Clause (x). Clause (iii) alone is not enough, and one candidate proved it.

    A second-site occupant is permitted -- the primary set's own 2G2H carries an ATP-site
    inhibitor 16 A away. What is not permitted is a component contacting the site being
    predicted. Checking only the SCOREABLE labels misses the real failure: a sibling
    fragment of the same series, in the same pocket, cleared that check by half an angstrom
    during screening. So this asserts on the FULL label set.
    """
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for name, values in frozen["targets"].items():
        checked += 1
        occupancy = values["apo_site_occupancy"]
        assert occupancy["scoreable_labels_contacted"] == 0, (
            f"{name}: an apo component contacts {occupancy['scoreable_labels_contacted']} "
            f"SCOREABLE label residues at {occupancy['nearest_scoreable_label_angstrom']} A "
            "-- the apo is not apo at the site it is asked to predict"
        )
        # A contact on a label that is ITSELF an active-site residue is permitted, because
        # clause (vii) already removed that residue from the candidate set and a residue
        # nobody scores cannot leak an answer. MKP5 is the case in this set: a sulfate sits
        # in the phosphate-binding catalytic site and contacts one label that is also an
        # active-site residue. So every contacted label must be an active-site residue, and
        # there must be enough of those to account for the count. An earlier version bounded
        # the count by `len(excluded_from_scoring)` instead, which the assertion above already
        # implies and which therefore could not fail on its own. This one can, and it sits at
        # its boundary on three arms rather than hanging slack: `mkp5` here at 1 == 1, and
        # both KRAS arms in the PRIMARY set at 5 == 5. One further contacted label with no
        # active-site overlap fails any of the three.
        #
        # Corrected 2026-09-03. This comment previously justified the assertion with
        # "`bcr_abl1_mandated` proves it: 16 labels contacted by myristate". That is false in
        # two ways. The arm contacts ZERO labels, and the 16 was read off
        # `nearest_scoreable_label_angstrom`, which is a DISTANCE of 16.0 A and not a count.
        # A stale falsifier is worse than none, because it stops the next reader checking.
        # The same edit redacted a real label residue number this comment used to print.
        overlap = set(values["label_residues"]) & set(values["active_site"])
        assert occupancy["labels_contacted"] <= len(overlap), (
            f"{name}: {occupancy['labels_contacted']} labels contacted by an apo component "
            f"but only {len(overlap)} labels are active-site residues, so at least one "
            "contact lands on a label that is allosteric and nothing else"
        )
    assert checked, "the freeze carried no target, so this asserted nothing"


def test_every_frozen_target_is_an_admitted_row_in_the_ledger(frozen, ledger):
    """ADR 0021 section 6. A candidate absent from the ledger cannot enter the set.

    The byte-for-byte reproducibility ADR 0012 asked for is unachievable against a live
    database, so this is what replaced it: the set and the record of how it was chosen have
    to agree, in both directions.
    """
    admitted = {row["name"] for row in ledger["candidates"] if row["decided_by"] == "admitted"}
    frozen_ids = set(frozen["targets"])
    assert frozen_ids == admitted, (
        f"frozen but not admitted in the ledger: {sorted(frozen_ids - admitted)}; "
        f"admitted but not frozen: {sorted(admitted - frozen_ids)}"
    )
    assert set(ledger["admitted"]) == frozen_ids


def test_the_ledger_records_the_rejections_and_not_only_the_survivors(ledger):
    """A ledger holding only the admitted set records nothing about the selection.

    The rejections are the part a reviewer needs: they are what shows the clauses have
    teeth and what they cost. Every rejection must name a deciding clause and give a fact.
    """
    rejected = [
        row for row in ledger["candidates"] if row["decided_by"] not in ("admitted", "pending")
    ]
    assert len(rejected) >= 2 * len(ledger["admitted"]), (
        f"{len(rejected)} rejections against {len(ledger['admitted'])} admissions -- a "
        "selection that rejected almost nothing did not select"
    )
    for row in rejected:
        assert row["detail"].strip(), f"{row['name']}: rejected with no reason recorded"
    assert ledger["frame"]["primary_frame"]["retrieved_on"], "the frame has no retrieval date"


def test_the_admitted_entries_meet_the_resolution_ceiling(ledger):
    """Clause (xi) is ADR 0009 clause 2 unchanged, applied to a pool rather than a name.

    It is checked here rather than against `frozen.json` on purpose: resolution is a
    SELECTION fact, so it belongs in the record of the selection.
    """
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for row in ledger["candidates"]:
        if row["decided_by"] != "admitted":
            continue
        for role, entry in row["structure_admission"].items():
            checked += 1
            resolution, method = entry["resolution_angstrom"], entry["method"]
            assert resolution is not None, f"{row['name']} {role}: no resolution recorded"
            ceiling = 4.0 if "ELECTRON" in method.upper() else 2.5
            assert resolution <= ceiling, (
                f"{row['name']} {role}: {resolution} A by {method} exceeds the {ceiling} A "
                "ceiling for that method"
            )
    assert checked, "the ledger admitted no structure, so this asserted nothing"


def test_the_secondary_manifest_redacts_exactly_as_the_primary_one_does(manifest):
    """The secondary set doubled the answer key, so it doubled the leak surface.

    `tests/test_no_leakage.py` holds the general rule over both manifests. This is the
    narrower statement that the fields this set adds -- `tier` and `pfam` -- were reviewed
    and are evaluation-side, so a future reader does not have to re-derive that.
    """
    full = read_manifest(SECONDARY_MANIFEST)
    evaluation_only = {
        "tier",
        "pfam",
        "holo",
        "site",
        "state",
        "blind",
        "allosteric_evidence",
        "note",
    }
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for spec in full["targets"]:
        checked += 1
        assert evaluation_only & set(spec), f"{spec['id']}: nothing to redact, so nothing is proved"

    from allo.inputs import load

    for spec in load(SECONDARY_MANIFEST)["targets"]:
        leaked = evaluation_only & set(spec)
        assert not leaked, f"{spec['id']}: prediction path can see {sorted(leaked)}"
    assert checked, "the manifest declared no target, so this asserted nothing"


def test_the_offline_structure_store_holds_both_sets(frozen):
    """ADR 0014's offline fallback has to cover the set that was just added.

    `tests/test_benchmark.py` asserts the store equals exactly the named accessions. That
    test is the reason this one is narrow: it only checks that every secondary entry is
    present, and leaves the equality to the existing guard.
    """
    named = set()
    for spec in yaml.safe_load(SECONDARY_MANIFEST.read_text())["targets"]:
        named.add(spec["apo"]["pdb"].upper())
        named.add(spec["holo"]["pdb"].upper())
    for store in (ROOT / "structures" / "apo", ROOT / "structures" / "holo"):
        if not store.exists():
            pytest.skip(f"{store} is absent; the offline fallback is not populated in this clone")
    present = {
        path.name.split(".")[0].upper()
        for store in ("apo", "holo")
        for path in (ROOT / "structures" / store).glob("*.cif*")
    }
    assert named <= present, f"offline store is missing {sorted(named - present)}"


def test_the_secondary_manifest_declares_what_the_eight_clauses_require(frozen, manifest):
    """Clauses (ii), (vii) and (viii) applied to the nine secondary arms.

    `tests/test_benchmark.py` enforces the eight on the PRIMARY manifest only, because its
    fixture is `benchmark.load()` and every other test there reads `benchmark.FROZEN`. That
    was invisible until an audit traced the fixture. This closes the checkable part of the
    gap; the rest (a live `pocket_residues` reconciliation) is what `allo benchmark verify
    --set secondary` does, and it runs under `make verify`.

    Deliberately not shared with `test_benchmark.py`: that module's version of clause (viii)
    asserts `tier in {mandated, corrected, sensitivity}` and would fail here on sight, which
    is the same `tier` ambiguity `docs/benchmark/secondary/README.md` section 2 warns about.
    """
    for spec in manifest["targets"]:
        name = spec["id"]

        # Clause (ii). The evidence, not the frame, decides admission.
        evidence = spec.get("allosteric_evidence", {})
        assert evidence.get("doi", "").startswith("10."), f"{name}: no DOI for the site"
        assert len(evidence.get("assay", "")) > 80, f"{name}: no assay described"

        # Clause (viii). State and blindness are disclosed, never required.
        state = spec.get("state", {})
        assert set(state) == {"apo", "holo", "matched"}, (
            f"{name}: state is {sorted(state)}. A YAML flow mapping whose value holds a comma "
            "parses the tail as a null key and truncates the state it meant to record"
        )
        assert isinstance(state["matched"], bool), f"{name}: matched is not a boolean"
        blind = spec.get("blind", {})
        assert blind.get("value") is False, f"{name}: no secondary arm is blind (ADR 0017)"
        assert len(blind.get("why", "")) > 40, f"{name}: blindness unjustified"

        # Clause (vii) and ADR 0011. Both classes lose the propagation source, or neither does.
        derived = frozen["targets"][name]
        excluded = set(derived["excluded_from_scoring"])
        assert set(derived["active_site"]) <= excluded, (
            f"{name}: active-site residues are still scored as negatives"
        )
        assert not excluded & set(derived["scoreable_label_residues"]), (
            f"{name}: a residue is in both the positives and the excluded set"
        )
        assert derived["n_candidates"] == derived["n_residues"] - len(excluded)
        assert derived["n_candidates"] > len(derived["scoreable_label_residues"])

        # Two records of the same bytes drift. This is the cheapest way to notice.
        pdb = spec["apo"]["pdb"]
        assert spec["apo"].get("sha256") == derived["hashes"][pdb], (
            f"{name}: manifest and freeze disagree on {pdb}'s bytes"
        )


def test_no_accession_is_pinned_at_two_versions_across_the_two_sets():
    """`_pinned_url` returns the FIRST manifest that names an accession, so a collision is
    silent.

    Two manifests pinning the same PDB id at different versions would make the fetched bytes
    depend on manifest order, and a target in one set would then be scored against a file the
    other set froze. Nothing in the code detects that. This does.
    """
    seen: dict[str, tuple] = {}
    checked = 0
    for path in (MANIFEST, SECONDARY_MANIFEST):
        provenance = read_manifest(path).get("structure_provenance", {})
        assert provenance, f"{path.name} pins no structure_provenance at all"
        for pdb_id, record in provenance.items():
            checked += 1
            key = (record["version"], record["sha256"])
            if pdb_id in seen:
                assert seen[pdb_id] == key, (
                    f"{pdb_id} is pinned at {seen[pdb_id]} in one set and {key} in the other; "
                    "which bytes are fetched depends on BENCHMARK_MANIFESTS order"
                )
            seen[pdb_id] = key
    # The two sets share no accession today, so the inner assertion never fires. Without this
    # the test would keep passing after someone emptied a provenance block.
    assert checked == 27, f"expected 27 pinned structures across both sets, walked {checked}"


def test_the_frozen_set_reports_the_difficulty_it_actually_spans(frozen):
    """Not an admission clause. A guard against the set quietly becoming uniform.

    The set exists to test generalisability and scalability, and both need spread: in size,
    and in how far the apo is from the holo. If a later edit narrows either, the set stops
    measuring the thing it was built for, and that must be a visible event.
    """
    sizes = [v["n_residues"] for v in frozen["targets"].values()]
    assert max(sizes) / min(sizes) >= 3.0, (
        f"size ladder spans {min(sizes)}-{max(sizes)} residues, a factor of "
        f"{max(sizes) / min(sizes):.1f}; a scalability slope needs a wider base"
    )
    clashes = [
        int(v["transplant_clashes"].split("/")[0])
        / max(1, int(v["transplant_clashes"].split("/")[1]))
        for v in frozen["targets"].values()
    ]
    assert max(clashes) - min(clashes) >= 0.5, (
        "every arm has a similar transplant clash fraction, so the set no longer spans "
        "cryptic and non-cryptic pockets"
    )


@pytest.mark.network
def test_clause_ix_holds_on_the_biological_assembly_and_not_only_the_deposited_unit():
    """Clause (ix) again, on the assembly. The deposited unit is not the protein.

    This test exists because measuring on the asymmetric unit gave a FALSE PASS. Most
    depositions of an interface site put one chain in the ASU, so a single-chain lining
    check finds one chain and reports success. Glycogen phosphorylase was admitted that
    way and then rejected here: on the `1FA9` dimer the AMP site draws 8 lining residues
    from one protomer and 3 from the other, so a third of its positive class could never
    enter a single-chain node set.

    It is a network test rather than a frozen field because the assembly coordinates are a
    separate download, and adding the measurement to `derive()` would rewrite the primary
    freeze, which ADR 0021 keeps closed. Both sets are checked.
    """
    import urllib.request
    from collections import defaultdict

    import numpy as np

    from allo.structure.pdb import parse_mmcif_text

    agent = {"User-Agent": "allo-benchmark/0.1"}
    for path in (MANIFEST, SECONDARY_MANIFEST):
        for spec in yaml.safe_load(path.read_text())["targets"]:
            holo = spec.get("holo")
            if not holo or spec.get("status") == "excluded":
                continue
            url = f"https://files.rcsb.org/download/{holo['pdb']}-assembly1.cif"
            request = urllib.request.Request(url, headers=agent)
            with urllib.request.urlopen(request, timeout=180) as response:  # noqa: S310
                structure = parse_mmcif_text(response.read().decode(), holo["pdb"])
            heavy = structure.element != "H"
            protein = np.flatnonzero(structure.protein & heavy)
            effector = structure.ligand & (structure.resname == holo["ligand"]) & heavy
            assert effector.any(), f"{spec['id']}: {holo['ligand']} absent from the assembly"
            for copy in sorted(set(structure.chain[effector].tolist())):
                position = structure.coord[effector & (structure.chain == copy)]
                distance = np.linalg.norm(
                    structure.coord[protein][:, None, :] - position[None, :, :], axis=2
                ).min(axis=1)
                lining: dict[str, set] = defaultdict(set)
                for index in protein[distance <= 4.5]:
                    lining[str(structure.chain[index])].add(int(structure.seq_id[index]))
                assert len(lining) == 1, (
                    f"{spec['id']}: in the {holo['pdb']} biological assembly, effector copy "
                    f"{copy} lines { {c: len(v) for c, v in sorted(lining.items())} } -- this "
                    "is an interface site and a single-chain node set cannot hold its labels"
                )


def test_clause_xii_pins_its_releases_and_derives_from_an_accession(manifest):
    """ADR 0042 consequences 1 and 2, in code. Added 2026-09-03.

    Clause (xii) resolves against three moving databases. The manifests recorded a hand-typed
    Pfam family list and no release at all, so the rule was frozen in name and floating in
    fact -- and `ns5b`'s value cannot have come from its stated source, RCSB, which carries no
    Pfam annotation for either of that arm's entries.

    Neither field moves a frozen value: `benchmark.freeze` builds `frozen.json` from six named
    keys and echoes no other. Both are redacted from the prediction path, because
    `allo.inputs.load` rebuilds from an allow-list, and the last assertion here says so rather
    than trusting that it stays true.

    Strengthened 2026-09-03, the same day, because pinning a release does not make the values
    that release. The recorded lists were RCSB per-entity assignments at 34.0 while the field
    said 38.2, and the two are different quantities: RCSB annotates the deposited construct,
    so `bcr_abl1_corrected` carried one family where its accession has four. This now checks
    every list against the accession that produced it, and re-derives the clause's verdict at
    the full 38.2 width -- where it still holds, with the only collisions between two arms of
    one protein.
    """
    import itertools
    import re

    import yaml as _yaml

    from allo.inputs import load as prediction_load

    record = json.loads(CLAUSE_XII_EVIDENCE.read_text())
    assert record["releases"]["pfam"]["version"] == "38.2"

    recorded: dict[str, set[str]] = {}
    for name, path in (("secondary", SECONDARY_MANIFEST), ("primary", MANIFEST)):
        raw = _yaml.safe_load(path.read_text())
        for field, expected in (
            ("interpro_release", "109.0"),
            ("pfam_release", "38.2"),
            ("panther_release", "19.0"),
        ):
            assert raw.get(field) == expected, (
                f"{name}: {field} is {raw.get(field)!r}, not {expected!r}. Clause (xii) "
                "resolves against a moving database and the release it was decided against "
                "is what makes the verdict reproducible (ADR 0042)"
            )
        for spec in raw["targets"]:
            accession = spec.get("uniprot")
            # UniProt's own published accession pattern, both forms.
            uniprot_pattern = (
                r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
            )
            assert accession and re.fullmatch(uniprot_pattern, accession), (
                f"{name}/{spec['id']}: uniprot is {accession!r}. Clause (xii) must derive "
                "from an accession, not from a hand-typed family list"
            )
            arm = record["arms"][spec["id"]]
            assert arm["uniprot"] == accession, (
                f"{name}/{spec['id']}: manifest accession {accession!r} is not the one the "
                f"families were resolved from, {arm['uniprot']!r}"
            )
            assert set(spec["pfam"]) == set(arm["pfam_families"]), (
                f"{name}/{spec['id']}: pfam is {sorted(spec['pfam'])}, but accession "
                f"{accession} resolves to {sorted(arm['pfam_families'])} at Pfam 38.2. The "
                "manifest carried the RCSB per-entity assignment at 34.0 until 2026-09-03, "
                "which is a strict subset of this and is not what ADR 0042 decides on"
            )
            recorded[spec["id"]] = set(arm["pfam_families"])

    # And the clause's verdict holds at that full width, not only on the truncation. Two
    # arms of one protein are one target, so they are allowed to share; nothing else is.
    same_protein = {
        frozenset(pair)
        for pair in itertools.combinations(recorded, 2)
        if pair[0].rsplit("_", 1)[0] == pair[1].rsplit("_", 1)[0]
    }
    collisions = {
        f"{a} / {b}": sorted(recorded[a] & recorded[b])
        for a, b in itertools.combinations(sorted(recorded), 2)
        if recorded[a] & recorded[b] and frozenset((a, b)) not in same_protein
    }
    assert not collisions, (
        f"clause (xii) fails at Pfam 38.2 width: {collisions}. It passes on the manifest "
        "only because the recorded family lists were truncated"
    )

    # And none of the four reaches a method. The allow-list redacts by default, so this fails
    # only if someone adds them to `_PREDICTION_SCHEMA` on purpose.
    visible = prediction_load()
    leaked = {
        field
        for field in ("uniprot", "pfam", "interpro_release", "pfam_release", "panther_release")
        if field in visible or any(field in target for target in visible["targets"])
    }
    assert not leaked, f"clause (xii) provenance reached the prediction path: {sorted(leaked)}"


def test_the_occupant_annotation_holds_its_evidence_based_classification(frozen, manifest):
    """ADR 0044. The four occupants, and the one measurement that separates them.

    An apo entry's active site may hold something. The annotation says whether that something
    is functional or is there because of how the crystal was grown. It **decides nothing** --
    clause (iii) and clause (x) both count every non-water heteroatom through a name-blind
    mask -- but it says something, and until 2026-09-03 what it said was false: `additives`
    was empty in both sets, so glycerol, sulfate and chloride were recorded as catalytic-state
    components.

    Pinned here because the classification rests on evidence a future reader will not have to
    hand. `GOL`, `SO4` and `CL` are additives: no published roster classes either of the first
    two as a functional occupant, `1SUG`'s depositors publish it as apo with ordered water in
    the catalytic pocket, and `1A9X` was grown from 0.65 to 1.35 M tetraethylammonium chloride.
    `K` is a state component: "Glu215 plays a key allosteric role by coordinating to the
    physiologically important potassium ion" (doi:10.1107/S0907444998006234).

    The `ptp1b` state correction is pinned with it, because it came from the same review and is
    the sharper measurement of the two.
    """
    import numpy as np

    from allo.groundtruth.structures import fetch_mmcif, parse_mmcif

    additives, state = {"CL", "GOL", "SO4"}, {"K"}
    for name, path in (("secondary", SECONDARY_MANIFEST), ("primary", MANIFEST)):
        vocabulary = yaml.safe_load(path.read_text())["orthosteric_vocabulary"]
        declared, kept = set(vocabulary["additives"]), set(vocabulary["state_components"])
        assert declared == additives, (
            f"{name}: additives are {sorted(declared)}, not {sorted(additives)}. ADR 0044 "
            "classifies these three from the deposition literature and BioLiP2's roster"
        )
        assert not (declared & kept), f"{name}: a component is in both classes"
        # `K` only exists in the secondary set's structures, so this binds where it applies.
        if "K" in kept | declared:
            assert state <= kept, f"{name}: K is functional in E. coli CPS and must not move"

    # The `ptp1b` correction, re-measured rather than quoted. The WPD loop's position is the
    # Asp181 carboxylate to Cys215 sulfur distance, and the arm's own holo is the control.
    spec = next(
        t for t in yaml.safe_load(SECONDARY_MANIFEST.read_text())["targets"] if t["id"] == "ptp1b"
    )
    assert spec["state"]["matched"] is False, (
        "ptp1b's two halves do not match: the apo WPD loop is closed and the holo's is open"
    )
    assert "closed" in spec["state"]["apo"], spec["state"]["apo"]
    distances = {}
    for role, cache in (("apo", "apo"), ("holo", "eval")):
        entry = spec[role]["pdb"]
        # `fetch_mmcif`, not a path into `data/raw`. That directory is a reproducible download
        # and CI does not carry it, so asserting the file was already there passed on a
        # developer machine and failed on a clean checkout. Both entries are in the committed
        # `structures/` archive, so this restores with no network and the test stays in the
        # offline gate, which is where a measurement that CAN run offline belongs. Found by CI
        # on 2026-09-03, on the first push of round 6.
        structure = parse_mmcif(fetch_mmcif(entry, ROOT / "data" / "raw" / cache), entry)
        chain = spec[role]["chain"]
        acid = (
            (structure.chain == chain)
            & (structure.seq_id == 181)
            & np.isin(structure.atom, ["OD1", "OD2"])
        )
        thiol = (structure.chain == chain) & (structure.seq_id == 215) & (structure.atom == "SG")
        distances[role] = float(
            np.linalg.norm(
                structure.coord[acid][:, None, :] - structure.coord[thiol][None], axis=-1
            ).min()
        )
    assert distances["apo"] < 7.5 < distances["holo"], (
        f"the WPD measurement moved: apo {distances['apo']:.2f} A, holo "
        f"{distances['holo']:.2f} A. ADR 0044 recorded 6.52 and 12.62"
    )
    # And the freeze agrees that the annotation now separates them.
    for arm in ("mkp5", "chk1", "ptp1b"):
        apo_state = frozen["targets"][arm]["orthosteric_state"]["apo"]
        assert not apo_state["state_components"], (
            f"{arm}: {apo_state['state_components']} is recorded as a catalytic-state "
            "component, and ADR 0044 classifies this arm's only occupant as an additive"
        )
