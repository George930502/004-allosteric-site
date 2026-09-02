"""Exploratory data analysis of every frozen apo residue graph. Apo-only, label-free."""

from __future__ import annotations

import json
import sys

import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import connected_components, shortest_path

from allo import network
from allo.classical import baselines
from allo.inputs import apo_input, load, one_letter
from allo.network.graph import residue_atom_index
from allo.structure.properties import residue_properties

ARMS = [
    "kras_g12c_mandated",
    "kras_g12c_corrected",
    "bcr_abl1_mandated",
    "bcr_abl1_corrected",
    "cardiac_myosin_corrected",
    "mkp5",
    "ptp1b",
    "hiv_rt",
    "ns5b",
    "chk1",
    "smyd3",
    "glucokinase",
    "p97_vcp",
    "ecoli_cps",
]


def spacing_statistics(values: np.ndarray) -> dict:
    """Unfolded nearest-neighbour level spacings, and the ratio statistic.

    The ratio statistic r = min(s_n, s_n+1) / max(s_n, s_n+1) needs no unfolding at all and
    has known means: 0.386 for Poisson (integrable, localised) and 0.536 for the Gaussian
    orthogonal ensemble (chaotic, delocalised). It is the cleanest one-number statement of
    whether a spectrum has level repulsion, and level repulsion is what decides whether a
    continuous-time quantum walk can do anything a spectral readout cannot.
    """
    spacing = np.diff(np.sort(values))
    spacing = spacing[spacing > 0]
    if len(spacing) < 3:
        return {"mean_ratio": None, "near_degenerate_pairs": None}
    ratio = np.minimum(spacing[:-1], spacing[1:]) / np.maximum(spacing[:-1], spacing[1:])
    return {
        "mean_ratio": round(float(ratio.mean()), 4),
        "near_degenerate_pairs": int((spacing < 0.01 * spacing.mean()).sum()),
        "median_spacing": round(float(np.median(spacing)), 6),
    }


def profile(arm: str) -> dict:
    apo = apo_input(arm)
    graph = network.build(apo)
    binary = (graph.weight > 0).astype(int)
    degree = binary.sum(axis=1)

    n_components, membership = connected_components(binary, directed=False)
    hops = shortest_path(binary, method="D", unweighted=True)
    finite = hops[np.isfinite(hops)]

    adjacency_values, adjacency_vectors = eigh(graph.adjacency)
    laplacian_values, _ = eigh(graph.laplacian)
    gap = float(adjacency_values[-1] - adjacency_values[-2])
    spacing = np.diff(np.sort(adjacency_values))
    mean_spacing = float(spacing[spacing > 0].mean())

    to_source = network.min_heavy_distance_to(apo, apo.active_site)
    candidate = np.array([d for r, d in to_source.items() if r not in set(apo.active_site)])

    properties = residue_properties(apo)
    order, _, _ = residue_atom_index(apo)
    rsa = np.array([properties["relative_solvent_accessibility"][r] for r in order])
    bfactor = np.array([properties["normalised_b_factor"][r] for r in order])

    source_mask = graph.index(apo.active_site)
    sequence = one_letter(
        [(apo.chain, r, n) for _, r, n in apo.structure.residues() if r in set(apo.residues)]
    )

    # The one correlation that decides how much of any propagation score is geometry.
    control = -np.array([to_source[r] for r in order])
    eigen = baselines.eigenvector_centrality(graph)

    return {
        "arm": arm,
        "pdb_id": apo.pdb_id,
        "chain": apo.chain,
        "n_residues": graph.n,
        "n_edges": int(binary.sum() // 2),
        "cutoff_angstrom": apo.cutoff,
        "source": {
            "n_residues": len(apo.active_site),
            "mean_relative_solvent_accessibility": round(float(rsa[source_mask].mean()), 4),
            "mean_degree": round(float(degree[source_mask].mean()), 3),
        },
        "degree": {
            "mean": round(float(degree.mean()), 3),
            "median": float(np.median(degree)),
            "min": int(degree.min()),
            "max": int(degree.max()),
            "std": round(float(degree.std()), 3),
        },
        "topology": {
            "n_components": int(n_components),
            "largest_component": int(np.bincount(membership).max()),
            "diameter_hops": int(finite.max()),
            "mean_hop_distance": round(float(finite.mean()), 3),
            "mean_clustering": round(float(baselines.clustering_coefficient(graph).mean()), 4),
            "edge_density": round(float(2 * binary.sum() / 2 / (graph.n * (graph.n - 1))), 5),
        },
        "adjacency_spectrum": {
            "lambda_1": round(float(adjacency_values[-1]), 4),
            "lambda_2": round(float(adjacency_values[-2]), 4),
            "gap": round(gap, 4),
            "gap_in_mean_spacings": round(gap / mean_spacing, 2),
            "perron_inverse_participation_ratio": round(
                float(
                    (adjacency_vectors[:, -1] ** 4).sum()
                    / (adjacency_vectors[:, -1] ** 2).sum() ** 2
                ),
                6,
            ),
            **spacing_statistics(adjacency_values),
        },
        "laplacian_spectrum": {
            "algebraic_connectivity": round(float(laplacian_values[1]), 6),
            "lambda_max": round(float(laplacian_values[-1]), 4),
            "spectral_ratio": round(
                float(laplacian_values[-1] / max(laplacian_values[1], 1e-12)), 1
            ),
        },
        "distance_to_source": {
            "min": round(float(candidate.min()), 3),
            "median": round(float(np.median(candidate)), 3),
            "max": round(float(candidate.max()), 3),
            "fraction_within_10A": round(float((candidate <= 10.0).mean()), 4),
        },
        "confounders": {
            "mean_relative_solvent_accessibility": round(float(rsa.mean()), 4),
            "fraction_buried_rsa_below_0.2": round(float((rsa < 0.2).mean()), 4),
            "b_factor_available": bool(np.std(bfactor) > 0),
            "sequence_length": len(sequence),
        },
        "geometry_vs_spectrum": {
            "spearman_eigenvector_vs_negated_distance": round(
                float(np.corrcoef(_rank(eigen), _rank(control))[0, 1]), 4
            ),
            "spearman_degree_vs_negated_distance": round(
                float(np.corrcoef(_rank(degree.astype(float)), _rank(control))[0, 1]), 4
            ),
        },
    }


def _rank(values: np.ndarray) -> np.ndarray:
    order = np.argsort(np.argsort(values))
    return order.astype(float)


def main() -> int:
    known = {spec["id"] for spec in load()["targets"]}
    profiles = []
    for arm in ARMS:
        try:
            profiles.append(profile(arm))
            print(f"  {arm}: done", flush=True)
        except Exception as failure:  # noqa: BLE001
            print(f"  {arm}: SKIPPED ({type(failure).__name__}: {failure})", flush=True)
    out = {"n_arms": len(profiles), "primary_ids_seen": sorted(known), "profiles": profiles}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
