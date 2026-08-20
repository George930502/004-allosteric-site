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
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from allo.groundtruth.labels import align_numbering, transfer_labels
from allo.groundtruth.manifest import read_manifest as load
from allo.inputs import MANIFEST, RAW, ROOT, active_site
from allo.structure.pdb import Structure, fetch_mmcif, parse_mmcif, sha256

FROZEN = ROOT / "docs" / "benchmark" / "frozen.json"

__all__ = ["FROZEN", "MANIFEST", "RAW", "ROOT", "derive", "freeze", "load", "verify"]

# Radius of the shell the transplant superposition is fitted on, around the pocket centroid.
SHELL_ANGSTROM = 20.0

# There is no distance threshold here, and that is deliberate (ADR 0007). An earlier version
# dropped labels within 5 A of the active site as "not distal"; the allostery literature
# states no such convention -- CASBench reports ~30 % of allosteric sites overlapping or
# bordering the catalytic site. What *is* published is AlloPred's rule: "Active site residues
# were not counted as being in any pocket ... to avoid direct perturbation of the site at
# which the effect was measured" (doi:10.1186/s12859-015-0771-1). A label that is itself
# a source residue scores maximally by construction, so it measures nothing. That is set
# membership, not distance. Proximity is handled in the evaluation layer by a distance-matched
# null (Amor et al., doi:10.1038/ncomms12477), which costs no labels.


@dataclass
class Derived:
    """Everything the manifest pins about one target, recomputed from the files."""

    target: str
    n_residues: int
    label_residues: list[int]
    labels_by_cutoff: dict[str, list[int]]
    scoreable_label_residues: list[int]
    excluded_from_scoring: list[int]
    n_candidates: int
    label_prevalence: float
    unmapped: list[str]
    active_site: list[int]
    distance_to_active_site: dict[str, float]
    labels_beyond_angstrom: dict[str, int]
    apo_site_occupancy: dict[str, object]
    holo_site_occupancy: dict[str, object]
    sequence_agreement: dict[str, object]
    transplant_min_distance: float
    transplant_clashes: str
    superposition_rmsd: float
    apo_holo_rmsd: dict[str, float]
    hashes: dict[str, str] = field(default_factory=dict)


def _components(structure: Structure, chain: str) -> dict[str, object]:
    """Non-water heteroatom components, plus the entry's polymer chain count.

    The chain count is clause (v): Amor et al. exclude pairs on "a mismatch between the
    oligomeric state of the active and inactive structures", and Wu et al. flag ASBench
    entries that are one part of a multimer "where the effect of cooperativity might play
    a crucial role". Deriving it beats asserting it in a note.
    """
    return {
        "chain_components": sorted(
            {str(n) for n in structure.resname[structure.ligand & (structure.chain == chain)]}
        ),
        "entry_components": sorted({str(n) for n in structure.resname[structure.ligand]}),
        "polymer_chains": len({str(c) for c in structure.chain[structure.protein]}),
    }


def _chain_ca(structure: Structure, chain: str) -> dict[int, np.ndarray]:
    mask = structure.protein & (structure.atom == "CA") & (structure.chain == chain)
    coords: dict[int, np.ndarray] = {}
    for index in np.where(mask)[0]:
        coords.setdefault(int(structure.seq_id[index]), structure.coord[index])
    return coords


def _superpose(mobile: dict[int, np.ndarray], target: dict[int, np.ndarray], keys: list[int]):
    """Transform putting `mobile`'s frame onto `target`'s, fitted on `keys` only."""
    P = np.array([mobile[k] for k in keys])
    Q = np.array([target[k] for k in keys])
    p_bar, q_bar = P.mean(0), Q.mean(0)
    V, _, W = np.linalg.svd((P - p_bar).T @ (Q - q_bar))
    rotation = V @ np.diag([1, 1, np.sign(np.linalg.det(V @ W))]) @ W
    return lambda X: (X - p_bar) @ rotation + q_bar


def _transplant(
    apo: Structure, holo: Structure, spec: dict, pocket: list[int]
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
    protein = apo.coord[apo.protein & (apo.chain == apo_chain)]
    closest = np.linalg.norm(moved[:, None, :] - protein[None, :, :], axis=-1).min(1)
    return float(closest.min()), f"{int((closest < 2.5).sum())}/{len(closest)}", fit


def _apo_holo_rmsd(
    apo: Structure, holo: Structure, spec: dict, pocket: list[int]
) -> dict[str, float]:
    """How far apart the two entries are, globally and across the pocket lining.

    Fitted on the non-label residues so the pocket figure measures the pocket rather
    than being absorbed into the fit.

    Two uses, only the first of which is a verdict. As **pair-matching quality control**
    the `core` figure is decisive: it is what caught the 8ACT/9GZ1 mismatch at 11.78 A.
    As a *pocket* measure it is descriptive only — a small lining change means the site is
    pre-formed, which under ADR 0007 says the geometric half of the problem is easy, not
    that there is "nothing to predict". What remains to be predicted on a pre-formed
    pocket is which of the many pre-formed pockets is the coupled one, and that is the
    whole task.
    """
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]
    apo_ca, holo_ca = _chain_ca(apo, apo_chain), _chain_ca(holo, holo_chain)
    mapping = align_numbering(holo, apo, holo_chain, apo_chain)
    paired = [(h, mapping[h]) for h in holo_ca if h in mapping and mapping[h] in apo_ca]
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


def derive(
    spec: dict, cutoff: float, raw: Path = RAW, sensitivity: tuple[float, ...] = ()
) -> Derived:
    """Recompute every pinned quantity for one target from the deposited files."""
    paths = {role: fetch_mmcif(spec[role]["pdb"], raw) for role in ("apo", "holo") if role in spec}
    apo = parse_mmcif(paths["apo"], spec["apo"]["pdb"])
    holo = parse_mmcif(paths["holo"], spec["holo"]["pdb"])
    apo_chain, holo_chain = spec["apo"]["chain"], spec["holo"]["chain"]

    labels = transfer_labels(holo, apo, spec["holo"]["ligand"], holo_chain, apo_chain, cutoff)
    label_numbers = [number for _, number, _ in labels.apo_residues]

    apo_ca = _chain_ca(apo, apo_chain)
    active = active_site(apo, apo_chain, spec["active_site"], cutoff)
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
    holo_occupancy = _components(holo, holo_chain)
    holo_occupancy["matches_apo"] = sorted(
        set(holo_occupancy["entry_components"]) - {spec["holo"]["ligand"]}
    ) == sorted(occupancy["entry_components"])

    # ADR 0004 excludes a pair whose members are not the same protein, and the KRAS
    # "wrong genotype" defect is exactly a sequence difference inside the label set.
    # Both are one number each; neither was checkable while they lived in prose.
    holo_names = {n: r for c, n, r in holo.residues() if c == holo_chain}
    apo_names = {n: r for c, n, r in apo.residues() if c == apo_chain}
    pairs = [
        (holo_names[h], apo_names[a])
        for h, a in align_numbering(holo, apo, holo_chain, apo_chain).items()
        if h in holo_names and a in apo_names
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

    min_distance, clashes, fit = _transplant(apo, holo, spec, label_numbers)
    rmsd = _apo_holo_rmsd(apo, holo, spec, label_numbers)
    return Derived(
        target=spec["id"],
        n_residues=len(apo_ca),
        label_residues=label_numbers,
        labels_by_cutoff=by_cutoff,
        scoreable_label_residues=scoreable,
        excluded_from_scoring=excluded,
        n_candidates=len(apo_ca) - len(excluded),
        label_prevalence=round(len(label_numbers) / len(apo_ca), 4),
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
        sequence_agreement=sequence_agreement,
        transplant_min_distance=round(min_distance, 2),
        transplant_clashes=clashes,
        superposition_rmsd=round(fit, 2),
        apo_holo_rmsd=rmsd,
        hashes={spec[r]["pdb"]: sha256(paths[r]) for r in ("apo", "holo")},
    )


def _exclude_sibling_sites(targets: dict[str, dict], manifest: dict) -> None:
    """Widen each arm's excluded set with the other functional sites on its own apo entry.

    A residue that this benchmark itself labels as a functional site is not a negative. On
    `8QYP`:A we freeze both myosin Site 1 and Site 2, so scoring Site 1 with Site 2's
    residues in the background penalises a method for finding a site we told it was real --
    the same error as leaving the propagation source in, one step further out. Section 5
    already excludes sibling sites from the *decoy* set for this reason; the background has
    to agree.

    `derive` holds one arm and cannot see this, so the cross-arm pass lives here. Sibling =
    another frozen arm on the same apo entry and chain whose `site` differs. Two arms on the
    same site with different effectors (Site 1's XB2 and 2OW) are not siblings. Only myosin
    has a second frozen site, so no other arm moves.
    """
    where = {
        s["id"]: (s.get("site"), s["apo"]["pdb"], s["apo"]["chain"]) for s in manifest["targets"]
    }
    for target, derived in targets.items():
        site, pdb, chain = where[target]
        siblings = {
            residue
            for other, other_derived in targets.items()
            if other != target and where[other][1:] == (pdb, chain) and where[other][0] != site
            for residue in other_derived["label_residues"]
        }
        excluded = set(derived["excluded_from_scoring"]) | (
            siblings - set(derived["label_residues"])
        )
        derived["excluded_from_scoring"] = sorted(excluded)
        derived["n_candidates"] = derived["n_residues"] - len(excluded)


def freeze(manifest: dict | None = None, raw: Path = RAW) -> dict:
    """Re-derive every pinned quantity for every scoreable target."""
    manifest = manifest or load()
    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    sensitivity = manifest["defaults"].get("cutoff_sensitivity", [])
    targets = {
        spec["id"]: asdict(derive(spec, cutoff, raw, tuple(sensitivity)))
        for spec in manifest["targets"]
        if spec.get("status") != "excluded"
    }
    _exclude_sibling_sites(targets, manifest)
    return {
        "frozen_on": str(manifest["frozen_on"]),
        "contact_cutoff_angstrom": cutoff,
        "targets": targets,
    }


def verify(manifest: dict | None = None, frozen: dict | None = None, raw: Path = RAW) -> list[str]:
    """Differences between the recorded freeze and what the files say today.

    An empty list is the exit criterion: the benchmark still is what it claims. A
    non-empty list means RCSB re-versioned an entry or someone moved a parameter —
    either way a visible event, which is the whole point of freezing.
    """
    frozen = frozen if frozen is not None else json.loads(FROZEN.read_text())
    current = freeze(manifest, raw)
    problems: list[str] = []
    if frozen.get("contact_cutoff_angstrom") != current["contact_cutoff_angstrom"]:
        problems.append(
            f"contact cutoff moved: {frozen.get('contact_cutoff_angstrom')} -> "
            f"{current['contact_cutoff_angstrom']}"
        )
    for target, now in current["targets"].items():
        was = frozen["targets"].get(target)
        if was is None:
            problems.append(f"{target}: not in the recorded freeze")
            continue
        for key, value in now.items():
            if was.get(key) != value:
                problems.append(f"{target}.{key}: frozen {was.get(key)!r} != current {value!r}")
    for target in frozen["targets"]:
        if target not in current["targets"]:
            problems.append(f"{target}: in the recorded freeze but no longer derivable")
    return problems


def stats(frozen: dict | None = None, seed: int = 0) -> dict:
    """The benchmark's own difficulty, derived from the freeze rather than asserted.

    Every number in `docs/benchmark/README.md` section 5 that is a pure function of the
    frozen label sets is computed here, so the protocol's justification regenerates
    instead of living as prose nobody can re-run (AGENTS.md: numbers come from code).

    Three quantities, all on the **scoreable** label set that section 5 declares primary
    (every label that is not itself a propagation-source residue, ADR 0007), against the
    **candidate set** rather than the whole node set: the propagation source and any sibling
    functional site leave both classes, because a residue that scores maximally by
    construction measures nothing whichever class it is filed under (ADR 0011).

    - hypergeometric baselines for the top-5 hit list under a uniform random ranking,
      which is the bar "we found it in the top 5" has to clear;
    - the minimum AUC a rank-sum test could detect at 80 % power (Noether), reported
      both for the real positive count and for one effectively independent patch --
      the two ends of the spatial-autocorrelation argument;
    - AUC-ROC against AUC-PR at a *fixed* real effect, to show how far prevalence alone
      moves AUC-PR while leaving AUC-ROC unmoved.
    """
    from scipy.stats import hypergeom, norm

    frozen = frozen if frozen is not None else json.loads(FROZEN.read_text())
    z = norm.ppf(0.95) + norm.ppf(0.80)  # alpha = 0.05 one-sided, power = 0.80

    def mde(n: int, positives: int) -> float | None:
        """Smallest detectable AUC. None when no effect size suffices at this size."""
        c = positives / n
        auc = 0.5 + z / np.sqrt(12 * c * (1 - c) * n)
        return round(float(auc), 3) if auc < 1.0 else None

    rng = np.random.default_rng(seed)
    out = {"seed": seed, "effect_size_d": 0.8, "draws": 2000, "targets": {}}
    for target, derived in frozen["targets"].items():
        n = derived["n_candidates"]
        scoreable = len(derived["scoreable_label_residues"])
        rv = hypergeom(n, scoreable, 5)
        # Fixed real signal, varying only prevalence: the reason AUC-PR is co-primary.
        roc, pr = [], []
        for _ in range(out["draws"]):
            scores = rng.standard_normal(n)
            scores[:scoreable] += out["effect_size_d"]
            order = np.argsort(-scores)
            hit = (order < scoreable).astype(float)
            ranks = np.argsort(np.argsort(scores))
            roc.append((ranks[:scoreable].mean() - (scoreable - 1) / 2) / (n - scoreable))
            precision = np.cumsum(hit) / np.arange(1, n + 1)
            pr.append(float((precision * hit).sum() / scoreable))
        out["targets"][target] = {
            "n_residues": derived["n_residues"],
            "n_candidates": n,
            "n_excluded": len(derived["excluded_from_scoring"]),
            "n_labels": len(derived["label_residues"]),
            "n_scoreable": scoreable,
            "scoreable_prevalence": round(scoreable / n, 4),
            "expected_hits_at_5": round(float(rv.mean()), 2),
            "p_at_least_1_hit": round(float(1 - rv.pmf(0)), 3),
            "p_at_least_2_hits": round(float(1 - rv.pmf(0) - rv.pmf(1)), 3),
            "mde_auc_rank_sum": mde(n, scoreable),
            "mde_auc_one_patch": mde(n, 1),
            "simulated_auc_roc": round(float(np.mean(roc)), 3),
            "simulated_auc_pr": round(float(np.mean(pr)), 3),
        }
    return out
