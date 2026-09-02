"""Measure the between-protein spread of three derived contact cutoffs, and score nothing.

`docs/method/review/19-cross-protein-normalisation.md` §1.2 defines a pre-screen that any
derived normalisation must pass before it is worth implementing. It needs two numbers:

  (a) the between-protein spread of the quantity the rule equalises, and
  (b) `R_within`, the endpoint's sensitivity to that quantity inside one protein.

A rule needs both to be large. This file measures (a) for the three derived cutoff rules,
because (a) is the cheap half and because a small (a) closes the rule on its own: a
per-protein rule whose value is the same on every protein is a global constant in disguise.

§7 of that review states the falsifier in the form used here. If the derived `r*` varies by
less than 0.3 A across the arms, the rule is a constant and the experiment stops.

Apo side only. It imports `allo.inputs` and `allo.network`, reads no label and no holo
structure, and reaches neither the evaluation layer nor the label package by any route. The
runner gate in `tests/test_no_leakage.py` matches those package names as bare substrings, so
this note names them the long way round on purpose.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import yaml
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

from allo.inputs import apo_input
from allo.network.graph import residue_atom_index

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"
METRICS = HERE / "metrics.json"


def heavy_min_distances(apo, ceiling: float, min_seq_sep: int = 0) -> np.ndarray:
    """Residue-residue minimum heavy-atom distance, as a dense matrix capped at `ceiling`.

    `min_seq_sep` deletes every pair closer than that in author numbering, and it is not a
    convenience. The peptide bond puts every sequence-adjacent pair at about 1.32 A, which is
    1.4 A below the closest non-bonded contact in any of these structures. Two of the three
    rules solved here read the bottom of the distance distribution, so with the backbone left
    in they measure the peptide bond and nothing else. Both settings are reported.

    Pairs beyond the ceiling are left at infinity. Every rule solved here has its root well
    below the ceiling, so the cap costs nothing and keeps the KD-tree query sparse.
    """
    structure = apo.structure
    heavy = structure.protein
    order, _, atom_residue = residue_atom_index(apo)
    coord = np.asarray(structure.coord[heavy], dtype=float)

    n = len(order)
    best = np.full((n, n), np.inf)
    tree = cKDTree(coord)
    for i, j in tree.query_pairs(ceiling):
        a, b = atom_residue[i], atom_residue[j]
        if a == b:
            continue
        d = float(np.linalg.norm(coord[i] - coord[j]))
        if d < best[a, b]:
            best[a, b] = best[b, a] = d
    np.fill_diagonal(best, 0.0)

    if min_seq_sep > 0:
        number = np.asarray(order, dtype=int)
        separation = np.abs(number[:, None] - number[None, :])
        best[separation < min_seq_sep] = np.inf
        np.fill_diagonal(best, 0.0)
    return best


def mean_contact_number(distance: np.ndarray, radius: float) -> float:
    """Mean number of other residues within `radius`. The `z` of Maxwell counting."""
    within = (distance <= radius) & (distance > 0.0)
    return float(within.sum() / distance.shape[0])


def isostatic_cutoff(distance: np.ndarray, grid: np.ndarray, target: float) -> float | None:
    """Smallest cutoff whose mean contact number reaches the isostatic target `z = 2d = 6`."""
    for radius in grid:
        if mean_contact_number(distance, float(radius)) >= target:
            return float(radius)
    return None


def connectivity_cutoff(distance: np.ndarray, grid: np.ndarray) -> float | None:
    """Smallest cutoff at which the contact graph has exactly one component."""
    for radius in grid:
        adjacency = (distance <= radius) & (distance > 0.0)
        count, _ = connected_components(adjacency, directed=False)
        if count == 1:
            return float(radius)
    return None


def rdf_first_minimum(distance: np.ndarray, ceiling: float) -> float | None:
    """First minimum of the smoothed radial distribution of residue-residue distances.

    The raw histogram at 0.05 A is noisy enough to hold spurious local minima, so it is
    smoothed with a moving average of the configured width before the search. The search
    starts after the first maximum, which is what "first minimum" means for an RDF.
    """
    width = CONFIG["rdf"]["bin_width"]
    span = CONFIG["rdf"]["smoothing_bins"]
    upper = np.triu_indices_from(distance, k=1)
    values = distance[upper]
    values = values[np.isfinite(values) & (values > 0.0)]
    edges = np.arange(0.0, ceiling + width, width)
    counts, _ = np.histogram(values, bins=edges)

    # Normalise by the shell volume, which is what makes it a radial *distribution*
    # rather than a raw histogram. Without it every histogram rises monotonically and
    # has no first minimum at all.
    centres = 0.5 * (edges[:-1] + edges[1:])
    density = counts / (centres**2)
    kernel = np.ones(span) / span
    smooth = np.convolve(density, kernel, mode="same")

    peak = int(np.argmax(smooth))
    for i in range(peak + 1, len(smooth) - 1):
        if smooth[i] <= smooth[i - 1] and smooth[i] <= smooth[i + 1]:
            return float(centres[i])
    return None


def measure(target: str, tier: str) -> dict:
    apo = apo_input(target)
    grid = np.arange(
        CONFIG["grid"]["low"],
        CONFIG["grid"]["high"] + CONFIG["grid"]["step"],
        CONFIG["grid"]["step"],
    )
    frozen = float(apo.cutoff)
    record = {"target": target, "tier": tier, "frozen_cutoff": frozen}

    for label, sep in (("backbone", 0), ("tertiary", CONFIG["min_seq_sep"])):
        distance = heavy_min_distances(apo, CONFIG["grid"]["high"], min_seq_sep=sep)
        if label == "backbone":
            record["n_residues"] = int(distance.shape[0])
            record["mean_contact_number_at_frozen"] = mean_contact_number(distance, frozen)
            record["closest_pair"] = closest_pair(distance)
        record[f"isostatic_{label}"] = isostatic_cutoff(distance, grid, CONFIG["isostatic_target"])
        record[f"connectivity_{label}"] = connectivity_cutoff(distance, grid)
        record[f"rdf_first_minimum_{label}"] = rdf_first_minimum(distance, CONFIG["grid"]["high"])
    return record


def closest_pair(distance: np.ndarray) -> float:
    """Smallest non-zero residue-residue distance.

    It is the peptide bond on every arm, and that is the reason the two lower-tail rules
    need the backbone removed before they mean anything.
    """
    upper = np.triu_indices_from(distance, k=1)
    values = distance[upper]
    values = values[np.isfinite(values) & (values > 0.0)]
    return round(float(values.min()), 3)


def load_records() -> dict[str, dict]:
    if not RECORDS.exists():
        return {}
    return {
        json.loads(line)["target"]: json.loads(line)
        for line in RECORDS.read_text().splitlines()
        if line.strip()
    }


def run() -> list[dict]:
    done = load_records()
    with RECORDS.open("a") as handle:
        for tier, targets in CONFIG["arms"].items():
            for target in targets:
                if target in done:
                    continue
                record = measure(target, tier)
                handle.write(json.dumps(record) + "\n")
                handle.flush()
                done[target] = record
                print(
                    f"{target:28s} "
                    + "  ".join(
                        f"{k}={record[k]}"
                        for k in sorted(record)
                        if k.endswith(("_backbone", "_tertiary"))
                    )
                )
    return list(done.values())


def summarise(records: list[dict]) -> dict:
    """Spread of each derived cutoff, per tier and pooled, against the constant threshold."""
    rules = tuple(
        f"{rule}_{label}"
        for rule in ("isostatic", "connectivity", "rdf_first_minimum")
        for label in ("backbone", "tertiary")
    )
    threshold = CONFIG["constant_threshold_angstrom"]
    out: dict = {"n_arms": len(records), "constant_threshold_angstrom": threshold, "rules": {}}

    for rule in rules:
        entry: dict = {}
        for tier in ("development", "primary", "all"):
            chosen = [r for r in records if tier == "all" or r["tier"] == tier]
            values = [r[rule] for r in chosen if r[rule] is not None]
            if not values:
                entry[tier] = {"n": 0}
                continue
            entry[tier] = {
                "n": len(values),
                "min": min(values),
                "max": max(values),
                "spread": round(max(values) - min(values), 4),
                "mean": round(float(np.mean(values)), 4),
                "sd": round(float(np.std(values, ddof=1)) if len(values) > 1 else 0.0, 4),
                "is_constant": bool(max(values) - min(values) < threshold),
            }
        entry["unsolved"] = [r["target"] for r in records if r[rule] is None]
        out["rules"][rule] = entry

    contact = [r["mean_contact_number_at_frozen"] for r in records]
    out["mean_contact_number_at_frozen"] = {
        "min": round(min(contact), 3),
        "max": round(max(contact), 3),
        "ratio": round(max(contact) / min(contact), 3),
    }
    closest = [r["closest_pair"] for r in records]
    out["closest_pair"] = {"min": min(closest), "max": max(closest)}
    sizes = [r["n_residues"] for r in records]
    out["n_residues"] = {
        "min": min(sizes),
        "max": max(sizes),
        "ratio": round(max(sizes) / min(sizes), 2),
    }
    return out


if __name__ == "__main__":
    records = run()
    metrics = summarise(records)
    METRICS.write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics["rules"], indent=2))
