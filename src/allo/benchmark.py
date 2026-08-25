"""The frozen benchmark: what the input layer is, and a command that proves it hasn't moved.

Freezing matters because every knob here — which entry, which chain, which residues,
which contact cutoff — changes the ranking a method is scored on. Fixing them once, in
`docs/benchmark/manifest.yaml`, is what makes two methods' numbers comparable at all.

`verify()` re-derives every recorded quantity from the deposited files and reports
differences. A drift means either RCSB re-versioned an entry or someone changed a
parameter; both must be a visible event, not a silent one.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from allo.groundtruth.labels import align_numbering, transfer_labels
from allo.groundtruth.manifest import read_manifest as load
from allo.groundtruth.structures import EVAL_CACHE, biological_assembly, fetch_mmcif, parse_mmcif
from allo.inputs import MANIFEST, ROOT, SECONDARY_MANIFEST, active_site, admitted_residue_numbers
from allo.structure.pdb import Structure, sha256

FROZEN = ROOT / "docs" / "benchmark" / "frozen.json"
SECONDARY_FROZEN = ROOT / "docs" / "benchmark" / "secondary" / "frozen.json"

# Which manifest produces which freeze. Both sets run through the same `derive`, which is
# what makes a number from one comparable with a number from the other.
SETS = {"primary": (MANIFEST, FROZEN), "secondary": (SECONDARY_MANIFEST, SECONDARY_FROZEN)}

__all__ = [
    "FROZEN",
    "SECONDARY_FROZEN",
    "SETS",
    "EVAL_CACHE",
    "MANIFEST",
    "SECONDARY_MANIFEST",
    "ROOT",
    "derive",
    "freeze",
    "load",
    "size_stratified_split",
    "verify",
]

# Radius of the shell the transplant superposition is fitted on, around the pocket centroid.
SHELL_ANGSTROM = 20.0

# There is no distance threshold here, and that is deliberate (ADR 0007). An earlier version
# dropped labels within 5 A of the active site as "not distal"; the allostery literature
# states no such convention -- CASBench reports ~30 % of allosteric sites overlapping or
# bordering the catalytic site. This repo's anti-circularity policy has a methodological
# analogy in AlloPred, which excluded active-site residues from candidate pockets during its
# spring-perturbation procedure (doi:10.1186/s12859-015-0771-1); it was not a published
# benchmark-universe rule. A label that is itself a source residue scores maximally by
# construction, so it measures nothing. That is set membership, not distance. Proximity is
# handled by a distance-matched null (Amor et al., doi:10.1038/ncomms12477), which costs no
# labels.


@dataclass
class Derived:
    """Everything the manifest pins about one target, recomputed from the files."""

    target: str
    n_residues: int
    residue_ids: list[int]
    label_residues: list[int]
    holo_label_footprint: list[str]
    labels_outside_node_set: list[int]
    labels_by_cutoff: dict[str, list[int]]
    scoreable_label_residues: list[int]
    excluded_from_scoring: list[int]
    n_candidates: int
    unmapped: list[str]
    active_site: list[int]
    distance_to_active_site: dict[str, float]
    labels_beyond_angstrom: dict[str, int]
    apo_site_occupancy: dict[str, object]
    holo_site_occupancy: dict[str, object]
    orthosteric_state: dict[str, object]
    sequence_agreement: dict[str, object]
    assembly_agreement: dict[str, object]
    transplant_min_distance: float
    transplant_clashes: str
    superposition_rmsd: float
    apo_holo_rmsd: dict[str, float]
    hashes: dict[str, str] = field(default_factory=dict)


def _components(structure: Structure, chain: str) -> dict[str, object]:
    """Non-water heteroatom components in the selected chain and full entry."""
    return {
        "chain_components": sorted(
            {str(n) for n in structure.resname[structure.ligand & (structure.chain == chain)]}
        ),
        "entry_components": sorted({str(n) for n in structure.resname[structure.ligand]}),
    }


def _chain_ca(structure: Structure, chain: str) -> dict[int, np.ndarray]:
    mask = structure.protein & (structure.atom == "CA") & (structure.chain == chain)
    coords: dict[int, np.ndarray] = {}
    for index in np.where(mask)[0]:
        coords.setdefault(int(structure.seq_id[index]), structure.coord[index])
    return coords


def _transplant(
    apo: Structure,
    holo: Structure,
    spec: dict,
    pocket: list[int],
    node_residues: set[int],
) -> tuple[float, str, float]:
    """Crypticity: collide the holo ligand into the apo frame, pocket excluded from the fit.

    A cryptic pocket is one the apo structure does not have, so the ligand cannot be
    placed without clashing. A pre-formed pocket accepts it.

    This is a **difficulty axis, not a validity test** (ADR 0007). Crypticity is a
    structural property and allostery is a functional one; they are orthogonal, and most
    validated cryptic sites are not allosteric. A pre-formed allosteric site is a harder
    target for a cavity detector and an easier one for a geometric method, which is worth
    knowing when reading an aggregate — it is never grounds to reject a pair.

    Residues are paired through the sequence alignment, never by author number: apo
    and holo entries of the same protein are routinely deposited under different
    numbering conventions, and pairing by number would superpose the wrong residues
    and manufacture a clash.
    """
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]
    apo_ca = _chain_ca(apo, apo_chain)
    holo_ca = _chain_ca(holo, holo_chain)
    holo_to_apo = align_numbering(holo, apo, holo_chain, apo_chain)
    # Fit locally, on the shell around the pocket rather than the whole chain: on a
    # multi-domain protein a global fit is dominated by inter-domain motion (a myosin
    # lever arm swinging tens of angstroms) and would report that motion as a clash.
    centre = np.array([apo_ca[r] for r in pocket if r in apo_ca]).mean(0)
    paired = [
        (h, holo_to_apo[h])
        for h in holo_ca
        if h in holo_to_apo
        and holo_to_apo[h] in apo_ca
        and holo_to_apo[h] in node_residues
        and holo_to_apo[h] not in pocket
        and np.linalg.norm(apo_ca[holo_to_apo[h]] - centre) <= SHELL_ANGSTROM
    ]
    P = np.array([holo_ca[h] for h, _ in paired])
    Q = np.array([apo_ca[a] for _, a in paired])
    p_bar, q_bar = P.mean(0), Q.mean(0)
    V, _, W = np.linalg.svd((P - p_bar).T @ (Q - q_bar))
    rotation = V @ np.diag([1, 1, np.sign(np.linalg.det(V @ W))]) @ W
    fit = float(np.sqrt(((((P - p_bar) @ rotation) - (Q - q_bar)) ** 2).sum(1)).mean())

    ligand = holo.coord[
        holo.ligand & (holo.resname == spec["holo"]["ligand"]) & (holo.chain == holo_chain)
    ]
    moved = (ligand - p_bar) @ rotation + q_bar
    protein = apo.coord[
        apo.protein & (apo.chain == apo_chain) & np.isin(apo.seq_id, list(node_residues))
    ]
    closest = np.linalg.norm(moved[:, None, :] - protein[None, :, :], axis=-1).min(1)
    return float(closest.min()), f"{int((closest < 2.5).sum())}/{len(closest)}", fit


def _apo_holo_rmsd(
    apo: Structure,
    holo: Structure,
    spec: dict,
    pocket: list[int],
    node_residues: set[int],
) -> dict[str, float]:
    """How far apart the two entries are, globally and across the pocket lining.

    Fitted on the non-label residues so the pocket figure measures the pocket rather
    than being absorbed into the fit.

    Two uses, only the first of which is a verdict. As **pair-matching quality control**
    the `core` figure is decisive: it is what caught an 8ACT/9GZ1 mismatch during the myosin
    sweep. That arm is not in the freeze and the figure is recorded nowhere, so no number is
    quoted here (the repo's own rule: numbers come from code, never from memory).
    As a *pocket* measure it is descriptive only — a small lining change means the site is
    pre-formed, which under ADR 0007 says the geometric half of the problem is easy, not
    that there is "nothing to predict". What remains to be predicted on a pre-formed
    pocket is which of the many pre-formed pockets is the coupled one, and that is the
    whole task.
    """
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]
    apo_ca, holo_ca = _chain_ca(apo, apo_chain), _chain_ca(holo, holo_chain)
    mapping = align_numbering(holo, apo, holo_chain, apo_chain)
    paired = [
        (h, mapping[h])
        for h in holo_ca
        if h in mapping and mapping[h] in apo_ca and mapping[h] in node_residues
    ]
    core = [(h, a) for h, a in paired if a not in pocket]
    P = np.array([holo_ca[h] for h, _ in core])
    Q = np.array([apo_ca[a] for _, a in core])
    p_bar, q_bar = P.mean(0), Q.mean(0)
    V, _, W = np.linalg.svd((P - p_bar).T @ (Q - q_bar))
    rotation = V @ np.diag([1, 1, np.sign(np.linalg.det(V @ W))]) @ W
    apply = lambda X: (X - p_bar) @ rotation + q_bar  # noqa: E731
    lining = [(h, a) for h, a in paired if a in pocket]
    core_dev = np.linalg.norm(apply(P) - Q, axis=1)
    lining_dev = np.linalg.norm(
        apply(np.array([holo_ca[h] for h, _ in lining])) - np.array([apo_ca[a] for _, a in lining]),
        axis=1,
    )
    return {
        "n_core": len(core),
        "core": round(float(np.sqrt((core_dev**2).mean())), 2),
        "n_lining": len(lining),
        "pocket_lining": round(float(np.sqrt((lining_dev**2).mean())), 2),
        "pocket_max": round(float(lining_dev.max()), 1),
    }


def _contacting_components(
    structure: Structure, chain: str, residues: list[int], cutoff: float
) -> set[str]:
    """Entry-level non-polymer components that contact the mapped catalytic site."""
    from allo.structure.pdb import contacts

    target = structure.protein & (structure.chain == chain) & np.isin(structure.seq_id, residues)
    contacting: set[str] = set()
    for component in sorted({str(name) for name in structure.resname[structure.ligand]}):
        source = structure.ligand & (structure.resname == component)
        if contacts(structure, source, target, cutoff):
            contacting.add(component)
    return contacting


def _orthosteric_state(
    apo: Structure,
    holo: Structure,
    spec: dict,
    active: list[int],
    cutoff: float,
    vocabulary: dict,
) -> dict[str, object]:
    """Compare catalytic-site ligands, ignoring declared additives and the effector."""
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]
    mapping = align_numbering(holo, apo, holo_chain, apo_chain)
    holo_active = sorted(h for h, a in mapping.items() if a in set(active))
    if not holo_active:
        raise ValueError(f"{spec['id']}: no active-site residue maps into the holo entry")

    state_vocabulary = set(vocabulary["state_components"])
    additives = set(vocabulary["additives"])
    if state_vocabulary & additives:
        raise ValueError("orthosteric state components and additives must be disjoint")
    effector = spec["holo"]["ligand"]

    def classify(components: set[str], allowed_effector: str | None) -> dict[str, list[str]]:
        known = state_vocabulary | additives
        if allowed_effector:
            known.add(allowed_effector)
        unknown = components - known
        if unknown:
            raise ValueError(
                f"{spec['id']}: catalytic-site components {sorted(unknown)} are absent from "
                "orthosteric_vocabulary"
            )
        return {
            "state_components": sorted(components & state_vocabulary),
            "additives": sorted(components & additives),
            "effector_contacts": sorted(components & {allowed_effector})
            if allowed_effector
            else [],
        }

    apo_state = classify(_contacting_components(apo, apo_chain, active, cutoff), None)
    holo_state = classify(_contacting_components(holo, holo_chain, holo_active, cutoff), effector)
    return {
        "apo": apo_state,
        "holo": holo_state,
        "matches_apo": apo_state["state_components"] == holo_state["state_components"],
    }


def derive(
    spec: dict,
    cutoff: float,
    raw: Path = EVAL_CACHE,
    sensitivity: tuple[float, ...] = (),
    orthosteric_vocabulary: dict | None = None,
) -> Derived:
    """Recompute every pinned quantity for one target from the deposited files."""
    paths = {role: fetch_mmcif(spec[role]["pdb"], raw) for role in ("apo", "holo") if role in spec}
    apo = parse_mmcif(paths["apo"], spec["apo"]["pdb"])
    holo = parse_mmcif(paths["holo"], spec["holo"]["pdb"])
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]
    assemblies = {
        role: biological_assembly(paths[role], spec[role]["chain"]) for role in ("apo", "holo")
    }
    target_copies_match = (
        assemblies["apo"]["selected_chain_entity_copies"]
        == assemblies["holo"]["selected_chain_entity_copies"]
    )
    composition_matches = (
        assemblies["apo"]["polymer_entity_copies"] == assemblies["holo"]["polymer_entity_copies"]
    )
    assembly_exception = spec.get("assembly_exception")
    if not (target_copies_match and composition_matches) and not assembly_exception:
        raise ValueError(
            f"{spec['id']}: apo/holo biological assembly state differs; declare and justify "
            "assembly_exception before re-freezing"
        )
    if target_copies_match and composition_matches and assembly_exception:
        raise ValueError(f"{spec['id']}: assembly_exception is declared but no mismatch exists")

    labels = transfer_labels(holo, apo, spec["holo"]["ligand"], holo_chain, apo_chain, cutoff)
    transferred_labels = [number for _, number, _ in labels.apo_residues]
    node_ids = admitted_residue_numbers(apo, apo_chain)
    node_set = set(node_ids)
    label_numbers = [number for number in transferred_labels if number in node_set]
    labels_outside_node_set = sorted(set(transferred_labels) - node_set)

    apo_ca = {r: xyz for r, xyz in _chain_ca(apo, apo_chain).items() if r in node_set}
    missing_node_ca = sorted(node_set - set(apo_ca))
    if missing_node_ca:
        raise ValueError(f"{spec['id']}: admitted residues {missing_node_ca} have no CA")
    active = active_site(apo, apo_chain, spec["active_site"], cutoff)
    outside_active = sorted(set(active) - node_set)
    if outside_active:
        raise ValueError(
            f"{spec['id']}: active-site residues {outside_active} lie outside node set"
        )
    anchor = np.array([apo_ca[r] for r in active if r in apo_ca])
    missing = [r for r in label_numbers if r not in apo_ca]
    if missing:
        raise ValueError(f"{spec['id']}: label residues {missing} have no CA; cannot rank them")
    distances = {
        str(r): float(np.linalg.norm(apo_ca[r] - anchor, axis=1).min()) for r in label_numbers
    }
    # The cutoff is the knob most able to move the label set, so every declared value is
    # frozen. Reporting a sensitivity that was never run leaves a tuning surface open.
    by_cutoff = {
        f"{c}": [
            number
            for _, number, _ in transfer_labels(
                holo, apo, spec["holo"]["ligand"], holo_chain, apo_chain, c
            ).apo_residues
            if number in node_set
        ]
        for c in sorted({cutoff, *sensitivity})
    }
    scoreable = [r for r in label_numbers if r not in set(active)]

    # The scoring universe, and the half of it one arm can see on its own.
    #
    # Dropping propagation-source residues from the *positives* and leaving them in the
    # *negatives* is not a neutral half-measure: it hands a systematic penalty to exactly
    # the method the challenge asks for. A connectivity-to-active-site score ranks the
    # source set at the top by construction -- that is what it computes -- so every one of
    # those residues scores as a false positive, while a geometric pocket detector takes no
    # such hit. Simulated at a fixed real effect, that costs 44-62 % of AUC-PR across these
    # arms for no difference in the signal. The reason section 5 gives for removing them
    # from the labels -- "scores maximally by construction and therefore measures nothing"
    # -- is a reason to remove them from *both* classes. Section 5 already applies exactly
    # this rule to the decoy set; this makes the background agree with it.
    #
    # Sibling functional sites are excluded too, but only `freeze` can see those.
    excluded = sorted(r for r in active if r in apo_ca)

    # Clause (iii), site-apo: does anything already sit in the site we are about to ask a
    # method to find? This is the check that disqualified 1OPL and is the basis of the
    # corrected tier, so it regenerates rather than living in prose.
    #
    # Every non-water heteroatom in the entry, not just those deposited on the apo chain.
    # 2G1T is the case that makes the difference: its ATP site is occupied by a bisubstrate
    # conjugate carried on chains E-H, 2.7 A from chain A's catalytic motif. A chain-scoped
    # check reports that entry as holding "MG" and nothing else.
    #
    # Reported over BOTH label sets, because they answer different questions and only the
    # second decides the clause. Over the full label set, the catalytic cofactor registers as
    # an occupant wherever the allosteric site abuts the active site: GDP-Mg contacts KRAS
    # labels 11/12/13/16/34 and ADP-VO4 contacts myosin Site 2 labels 242/243/463 -- every
    # one of which is itself an active-site residue. That is the two sites sharing a border,
    # not a modulator sitting in the pocket. Over the *scoreable* set -- the residues a method
    # is actually asked to find -- those contacts vanish and only a genuine occupant survives,
    # which is why 1OPL is the one arm that fails.
    from allo.structure.pdb import contacts

    apo_ligands = apo.ligand
    occupancy: dict[str, object] = {
        **_components(apo, apo_chain),
        "biological_assembly": assemblies["apo"],
        "labels_contacted": 0,
        "nearest_label_angstrom": None,
        "scoreable_labels_contacted": 0,
        "nearest_scoreable_label_angstrom": None,
    }
    for residues, count_key, gap_key in (
        (label_numbers, "labels_contacted", "nearest_label_angstrom"),
        (scoreable, "scoreable_labels_contacted", "nearest_scoreable_label_angstrom"),
    ):
        if not (apo_ligands.any() and residues):
            continue
        mask = apo.protein & (apo.chain == apo_chain) & np.isin(apo.seq_id, residues)
        gap = np.linalg.norm(
            apo.coord[mask][:, None, :] - apo.coord[apo_ligands][None, :, :], axis=-1
        )
        occupancy[count_key] = len({n for _, n, _ in contacts(apo, apo_ligands, mask, cutoff)})
        occupancy[gap_key] = round(float(gap.min()), 2)

    # Clause (vi): the orthosteric state has to be recorded for *both* members, or an
    # apo->holo difference cannot be attributed to the modulator. The cardiac myosin x-ray
    # arm is the live case -- ADP-VO4 (apo) against ADP-BeF3 (holo), so the members differ
    # in nucleotide analogue as well as in drug.
    holo_occupancy = {
        **_components(holo, holo_chain),
        "biological_assembly": assemblies["holo"],
    }
    if orthosteric_vocabulary is None:
        raise ValueError(f"{spec['id']}: orthosteric_vocabulary is required")
    orthosteric = _orthosteric_state(apo, holo, spec, active, cutoff, orthosteric_vocabulary)
    holo_occupancy["matches_apo"] = orthosteric["matches_apo"]

    # ADR 0004 excludes a pair whose members are not the same protein, and the KRAS
    # "wrong genotype" defect is exactly a sequence difference inside the label set.
    # Both are one number each; neither was checkable while they lived in prose.
    holo_names = {n: r for c, n, r in holo.residues() if c == holo_chain}
    apo_names = {n: r for c, n, r in apo.residues() if c == apo_chain}
    pairs = [
        (holo_names[h], apo_names[a])
        for h, a in align_numbering(holo, apo, holo_chain, apo_chain).items()
        if h in holo_names and a in apo_names and a in node_set
    ]
    in_label = [
        f"{apo_names[a]}{a}->{holo_names[h]}"
        for h, a in align_numbering(holo, apo, holo_chain, apo_chain).items()
        if h in holo_names
        and a in apo_names
        and holo_names[h] != apo_names[a]
        and a in label_numbers
    ]
    sequence_agreement = {
        "aligned": len(pairs),
        "identity": round(sum(x == y for x, y in pairs) / len(pairs), 4),
        "differences_in_label_set": in_label,
    }

    min_distance, clashes, fit = _transplant(apo, holo, spec, label_numbers, node_set)
    rmsd = _apo_holo_rmsd(apo, holo, spec, label_numbers, node_set)
    return Derived(
        target=spec["id"],
        n_residues=len(node_ids),
        residue_ids=list(node_ids),
        label_residues=label_numbers,
        holo_label_footprint=[f"{c}:{name}{number}" for c, number, name in labels.holo_residues],
        labels_outside_node_set=labels_outside_node_set,
        labels_by_cutoff=by_cutoff,
        scoreable_label_residues=scoreable,
        excluded_from_scoring=excluded,
        n_candidates=len(apo_ca) - len(excluded),
        unmapped=[f"{c}:{n}{i}" for c, i, n in labels.unmapped],
        active_site=active,
        distance_to_active_site={
            "min": round(min(distances.values()), 1),
            "median": round(float(np.median(list(distances.values()))), 1),
            "max": round(max(distances.values()), 1),
        },
        # A pure descriptor, selecting nothing (ADR 0007). It is how the benchmark states
        # which of its targets are proximal: on KRAS the count collapses with distance,
        # which is the honest way to say that a rank-by-distance baseline will do well there.
        labels_beyond_angstrom={
            f"{t}": sum(1 for v in distances.values() if v > t) for t in (3.0, 5.0, 10.0, 15.0)
        },
        apo_site_occupancy=occupancy,
        holo_site_occupancy=holo_occupancy,
        orthosteric_state=orthosteric,
        sequence_agreement=sequence_agreement,
        assembly_agreement={
            "selected_target_copies_match": target_copies_match,
            "polymer_composition_matches": composition_matches,
            "exception": assembly_exception,
        },
        transplant_min_distance=round(min_distance, 2),
        transplant_clashes=clashes,
        superposition_rmsd=round(fit, 2),
        apo_holo_rmsd=rmsd,
        hashes={spec[r]["pdb"]: sha256(paths[r]) for r in ("apo", "holo")},
    )


def _label_accounting_problems(targets: dict[str, dict], manifest: dict) -> list[str]:
    """Reconcile every arm against an independent holo ligand-contact authority."""
    specs = {spec["id"]: spec for spec in manifest["targets"]}
    authorities = manifest["label_footprints"]
    problems: list[str] = []
    for target, values in targets.items():
        holo = specs[target]["holo"]
        key = f"{holo['pdb']}:{holo['chain']}:{holo['ligand']}"
        authority = authorities.get(key)
        if authority is None:
            problems.append(f"{target}: no label authority for {key}")
            continue
        if values.get("holo_label_footprint") != authority:
            problems.append(f"{target}: live holo footprint differs from authority {key}")
        accounted = (
            len(values["label_residues"])
            + len(values["unmapped"])
            + len(values["labels_outside_node_set"])
        )
        if accounted != len(authority):
            problems.append(
                f"{target}: kept+unmapped+outside={accounted}, authority {key}={len(authority)}"
            )
    return problems


def _validate_protocol(manifest: dict) -> None:
    """Fail closed if an input-layer knob is implicit.

    Only the input layer is checked here. How a score is computed -- estimator, null model,
    multiplicity -- is a separate layer with its own lifecycle and its own document
    (docs/benchmark/evaluation/); pinning it in the input manifest coupled two
    freezes that move at different rates.
    """
    vocabulary = manifest.get("orthosteric_vocabulary")
    if not isinstance(vocabulary, dict) or set(vocabulary) != {"state_components", "additives"}:
        raise ValueError("manifest orthosteric_vocabulary fields are invalid")
    if set(vocabulary["state_components"]) & set(vocabulary["additives"]):
        raise ValueError("orthosteric state components and additives must be disjoint")

    scoreable = [spec for spec in manifest["targets"] if spec.get("status") != "excluded"]
    expected_footprints = {
        f"{spec['holo']['pdb']}:{spec['holo']['chain']}:{spec['holo']['ligand']}"
        for spec in scoreable
    }
    if set(manifest.get("label_footprints", {})) != expected_footprints:
        raise ValueError("manifest label_footprints do not exactly cover scoreable holo pockets")

    named_pinned = {spec[role]["pdb"] for spec in scoreable for role in ("apo", "holo")}
    provenance = manifest.get("structure_provenance", {})
    if set(provenance) != named_pinned:
        raise ValueError("manifest structure_provenance does not exactly cover pinned entries")
    for pdb, record in provenance.items():
        if set(record) != {"version", "url", "sha256"}:
            raise ValueError(f"structure provenance for {pdb} has unexpected fields")
        low = pdb.lower()
        stem = f"pdb_0000{low}"
        expected_url = (
            "https://files-versioned.wwpdb.org/pdb_versioned/data/entries/"
            f"{low[1:3]}/{stem}/{stem}_xyz_v{record['version']}.cif.gz"
        )
        if record["url"] != expected_url:
            raise ValueError(f"structure provenance URL for {pdb} is not its pinned version")
        if len(record["sha256"]) != 64:
            raise ValueError(f"structure provenance hash for {pdb} is invalid")
    for spec in scoreable:
        apo = spec["apo"]
        if apo.get("sha256") != provenance[apo["pdb"]]["sha256"]:
            raise ValueError(f"{spec['id']}: apo hash differs from structure provenance")


def freeze(manifest: dict | None = None, raw: Path = EVAL_CACHE) -> dict:
    """Re-derive every pinned quantity for every scoreable target."""
    manifest = manifest or load()
    _validate_protocol(manifest)
    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    sensitivity = manifest["defaults"].get("cutoff_sensitivity", [])
    targets = {
        spec["id"]: asdict(
            derive(
                spec,
                cutoff,
                raw,
                tuple(sensitivity),
                manifest["orthosteric_vocabulary"],
            )
        )
        for spec in manifest["targets"]
        if spec.get("status") != "excluded"
    }
    if problems := _label_accounting_problems(targets, manifest):
        raise ValueError("label accounting failed: " + "; ".join(problems))
    # `tier` is pinned into the freeze rather than read live from the manifest. It decides
    # which arm carries a claim, so a post-freeze edit to it would move a result while
    # `verify` stayed green -- it would be comparing nothing that had changed.
    for target, derived in targets.items():
        derived["tier"] = next(s["tier"] for s in manifest["targets"] if s["id"] == target)
    return {
        "frozen_on": str(manifest["frozen_on"]),
        "contact_cutoff_angstrom": cutoff,
        "orthosteric_vocabulary": manifest["orthosteric_vocabulary"],
        "structure_provenance": manifest["structure_provenance"],
        "label_footprints": manifest["label_footprints"],
        "targets": targets,
    }


def size_stratified_split(sizes: dict[str, int], seed: int = 0) -> dict[str, str]:
    """Assign each secondary target to `development` or `generalisation` (ADR 0021).

    Consecutive size-ordered pairs are the strata, which is the finest stratification
    available, and the seeded shuffle picks which member of each pair is held out. Nobody
    chooses, so nobody can put the easy targets in the set that carries the claim.

    An odd target always joins `generalisation`. That tier carries a hypothesis test and
    needs every arm it can get -- a distribution-free one-sample test over N targets cannot
    reach p < 0.05 below N = 5 -- while `development` only tunes.

    Note what that rule is NOT. `ordered` is ascending and the unpaired element is
    `ordered[-1]`, so the LARGEST target always lands in `generalisation`, deterministically
    and not by the seed. With nine arms that is `ecoli_cps` at 1058 residues, which pulls the
    held-out tier's mean size to 586 against `development`'s 385. The no-hand-picking promise
    holds for the paired arms; for the odd one it is a fixed rule, and a reader comparing tier
    means must know that the rule, not chance, put the biggest target there.
    """
    ordered = sorted(sizes, key=lambda name: (sizes[name], name))
    rng = random.Random(seed)
    tiers: dict[str, str] = {}
    for i in range(0, len(ordered) - 1, 2):
        pair = ordered[i : i + 2]
        rng.shuffle(pair)
        tiers[pair[0]], tiers[pair[1]] = "development", "generalisation"
    if len(ordered) % 2:
        tiers[ordered[-1]] = "generalisation"
    return tiers


def deep_diff(recorded, derived, path: str, problems: list[str]) -> None:
    """Append every difference between a frozen value and a re-derived one.

    Type-strict and recursive: a list that became a tuple, or an int that became a
    float, is drift. Shared with the evaluation layer, which freezes and verifies on
    exactly this contract.
    """
    if type(recorded) is not type(derived):
        problems.append(
            f"{path or '<root>'}: frozen type {type(recorded).__name__} != "
            f"current type {type(derived).__name__}"
        )
        return
    if isinstance(recorded, dict):
        for key in sorted(set(recorded) | set(derived)):
            child = f"{path}.{key}" if path else key
            if key not in recorded:
                problems.append(f"{child}: absent from frozen, present in current")
            elif key not in derived:
                problems.append(f"{child}: present in frozen, absent from current")
            else:
                deep_diff(recorded[key], derived[key], child, problems)
        return
    if isinstance(recorded, list):
        if len(recorded) != len(derived):
            problems.append(f"{path}: frozen length {len(recorded)} != current {len(derived)}")
        for index, (was, now) in enumerate(zip(recorded, derived, strict=False)):
            deep_diff(was, now, f"{path}[{index}]", problems)
        return
    if recorded != derived:
        problems.append(f"{path}: frozen {recorded!r} != current {derived!r}")


def verify(
    manifest: dict | None = None,
    frozen: dict | None = None,
    raw: Path = EVAL_CACHE,
    benchmark_set: str = "primary",
) -> list[str]:
    """Differences between the recorded freeze and what the files say today.

    An empty list is the exit criterion: the benchmark still is what it claims. A
    non-empty list means RCSB re-versioned an entry or someone moved a parameter —
    either way a visible event, which is the whole point of freezing.
    """
    manifest_path, frozen_path = SETS[benchmark_set]
    frozen = frozen if frozen is not None else json.loads(frozen_path.read_text())
    current = freeze(manifest if manifest is not None else load(manifest_path), raw)
    problems: list[str] = []

    deep_diff(frozen, current, "", problems)
    return problems
