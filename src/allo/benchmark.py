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
from allo.inputs import MANIFEST, RAW, ROOT, active_site, load
from allo.structure.pdb import Structure, fetch_mmcif, parse_mmcif, sha256

FROZEN = ROOT / "docs" / "benchmark" / "frozen.json"

__all__ = ["FROZEN", "MANIFEST", "RAW", "ROOT", "derive", "freeze", "load", "verify"]

# A label residue closer than this to the active site is not a *distal* regulatory residue,
# which is what the challenge asks us to find. See ADR 0005.
DISTAL_ANGSTROM = 5.0

# Radius of the shell the transplant superposition is fitted on, around the pocket centroid.
SHELL_ANGSTROM = 20.0


@dataclass
class Derived:
    """Everything the manifest pins about one target, recomputed from the files."""

    target: str
    n_residues: int
    label_residues: list[int]
    labels_by_cutoff: dict[str, list[int]]
    distal_label_residues: list[int]
    label_prevalence: float
    unmapped: list[str]
    active_site: list[int]
    distance_to_active_site: dict[str, float]
    distal_by_threshold: dict[str, int]
    apo_site_occupancy: dict[str, object]
    sequence_agreement: dict[str, object]
    transplant_min_distance: float
    transplant_clashes: str
    superposition_rmsd: float
    apo_holo_rmsd: dict[str, float]
    hashes: dict[str, str] = field(default_factory=dict)


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
    placed without clashing. A pre-formed pocket accepts it. This separates a genuine
    cryptic-site prediction task from a pocket-finding task — a fact about the
    benchmark that any comparison of methods has to be read against.

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
    than being absorbed into the fit. This is the number that says whether there is a
    conformational change to predict at all: on the mandated BCR-ABL1 pair there is not.
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
    distal = [r for r in label_numbers if distances.get(str(r), 0.0) > DISTAL_ANGSTROM]

    # Clause (ii) of the apo/holo definition, as a derived quantity rather than a hand-made
    # table: does anything already sit in the site we are about to ask a method to find?
    # This is the check that disqualified 1OPL, and it is the basis of the corrected tier,
    # so it has to regenerate rather than live in prose (docs/benchmark/README.md 1).
    from allo.structure.pdb import contacts

    # Every non-water heteroatom in the entry, not just those deposited on the apo chain.
    # 2G1T is the case that makes the difference: its ATP site is occupied by a bisubstrate
    # conjugate carried on chains E-H, 2.7 A from chain A's catalytic motif. A chain-scoped
    # check reports that entry as holding "MG" and nothing else.
    apo_ligands = apo.ligand
    occupancy: dict[str, object] = {
        "chain_components": sorted(
            {str(n) for n in apo.resname[apo.ligand & (apo.chain == apo_chain)]}
        ),
        "entry_components": sorted({str(n) for n in apo.resname[apo_ligands]}),
        "distal_labels_contacted": 0,
        "nearest_distal_label_angstrom": None,
    }
    if apo_ligands.any() and distal:
        distal_mask = apo.protein & (apo.chain == apo_chain) & np.isin(apo.seq_id, distal)
        touched = {n for _, n, _ in contacts(apo, apo_ligands, distal_mask, cutoff)}
        gap = np.linalg.norm(
            apo.coord[distal_mask][:, None, :] - apo.coord[apo_ligands][None, :, :], axis=-1
        )
        occupancy["distal_labels_contacted"] = len(touched)
        occupancy["nearest_distal_label_angstrom"] = round(float(gap.min()), 2)

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
        distal_label_residues=distal,
        label_prevalence=round(len(label_numbers) / len(apo_ca), 4),
        unmapped=[f"{c}:{n}{i}" for c, i, n in labels.unmapped],
        active_site=active,
        distance_to_active_site={
            "min": round(min(distances.values()), 1),
            "median": round(float(np.median(list(distances.values()))), 1),
            "max": round(max(distances.values()), 1),
        },
        # The contact cutoff's sensitivity is frozen; the distal threshold's was not, and
        # it selects the primary endpoint's positive set. Same reasoning, same treatment.
        distal_by_threshold={
            f"{t}": sum(1 for v in distances.values() if v > t) for t in (3.0, 4.0, 5.0, 6.0, 7.0)
        },
        apo_site_occupancy=occupancy,
        sequence_agreement=sequence_agreement,
        transplant_min_distance=round(min_distance, 2),
        transplant_clashes=clashes,
        superposition_rmsd=round(fit, 2),
        apo_holo_rmsd=rmsd,
        hashes={spec[r]["pdb"]: sha256(paths[r]) for r in ("apo", "holo")},
    )


def freeze(manifest: dict | None = None, raw: Path = RAW) -> dict:
    """Re-derive every pinned quantity for every scoreable target."""
    manifest = manifest or load()
    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    sensitivity = manifest["defaults"].get("cutoff_sensitivity", [])
    return {
        "frozen_on": str(manifest["frozen_on"]),
        "contact_cutoff_angstrom": cutoff,
        "targets": {
            spec["id"]: asdict(derive(spec, cutoff, raw, tuple(sensitivity)))
            for spec in manifest["targets"]
            if spec.get("status") != "excluded"
        },
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

    Three quantities, all on the **distal** label set that section 5 declares primary:

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
        n = derived["n_residues"]
        distal = len(derived["distal_label_residues"])
        rv = hypergeom(n, distal, 5)
        # Fixed real signal, varying only prevalence: the reason AUC-PR is co-primary.
        roc, pr = [], []
        for _ in range(out["draws"]):
            scores = rng.standard_normal(n)
            scores[:distal] += out["effect_size_d"]
            order = np.argsort(-scores)
            hit = (order < distal).astype(float)
            ranks = np.argsort(np.argsort(scores))
            roc.append((ranks[:distal].mean() - (distal - 1) / 2) / (n - distal))
            precision = np.cumsum(hit) / np.arange(1, n + 1)
            pr.append(float((precision * hit).sum() / distal))
        out["targets"][target] = {
            "n_residues": n,
            "n_labels": len(derived["label_residues"]),
            "n_distal": distal,
            "distal_prevalence": round(distal / n, 4),
            "expected_hits_at_5": round(float(rv.mean()), 2),
            "p_at_least_1_hit": round(float(1 - rv.pmf(0)), 3),
            "p_at_least_2_hits": round(float(1 - rv.pmf(0) - rv.pmf(1)), 3),
            "mde_auc_rank_sum": mde(n, distal),
            "mde_auc_one_patch": mde(n, 1),
            "simulated_auc_roc": round(float(np.mean(roc)), 3),
            "simulated_auc_pr": round(float(np.mean(pr)), 3),
        }
    return out
