"""Size and power of the negative-class-(b) endpoints, under several site-uninformative nulls.

This is evaluation-side code and it reads the answer key, which is why it lives here. The
measurements behind ADR 0039 were first made in an untracked script, and a frozen protocol
whose evidence cannot be re-run is not evidence -- found 2026-09-03 by an adversarial pass.

**What it measures.** The frozen test ranks pockets by the mean midrank of their linings and
asks where a positive set lands among the decoy linings:

    p = (1 + #{decoy_mean >= positive_mean}) / (1 + n_decoys)

`site` puts the detector's site-pocket lining on the positive side, which is the ADR 0030
statistic and the one `score_arm` reports as `p`. `label` puts the label set there, which is
ADR 0039's `label_p`. Both use the real linings from the freeze and the real coordinates, so
"matched in size distribution and spatial correlation" holds by construction rather than by a
synthetic matcher.

**Why four generators and not one.** The first version drew one family, a stationary Gaussian
field with exponential covariance, and concluded the label form is "never anti-conservative".
The two sides of that test have different set sizes and are NOT exchangeable, so its size is a
property of the score field and not a distribution-free guarantee. One family cannot support
"never". These four span the shapes a real scorer takes: no spatial structure at all, smooth
and Gaussian, smooth and heavy-tailed, and the blocky monotone-in-distance shape that every
distance-correlated baseline in this repository actually has.
"""

from __future__ import annotations

import json

import numpy as np

from allo.inputs import apo_input
from allo.scoring.harness import EVALUATION_FROZEN, _positives
from allo.scoring.nulls import evaluation_graph, field_factor

BLOCK = 2500
GENERATORS = ("white_noise", "smooth_gaussian", "smooth_t", "distance_shell")


def _ranks(fields: np.ndarray) -> np.ndarray:
    """Column-wise midranks. The fields are continuous, so there are no ties."""
    order = np.argsort(fields, axis=0, kind="stable")
    out = np.empty_like(order, dtype=np.float32)
    n, b = fields.shape
    rows = np.arange(1, n + 1, dtype=np.float32)[:, None]
    np.put_along_axis(out, order, np.broadcast_to(rows, (n, b)), axis=0)
    return out


def _p_values(fields: np.ndarray, positive: np.ndarray, decoys: list[np.ndarray]) -> np.ndarray:
    ranks = _ranks(fields)
    observed = ranks[positive].mean(0)
    ge = np.zeros(fields.shape[1], dtype=int)
    for idx in decoys:
        ge += (ranks[idx].mean(0) >= observed).astype(int)
    return (1 + ge) / (1 + len(decoys))


def _draw(generator: str, factor: np.ndarray, coords: np.ndarray, rng, b: int) -> np.ndarray:
    """One batch of site-uninformative score fields, `n_candidates` by `b`.

    Site-uninformative means the draw uses no label and no site: `distance_shell` picks its
    centre uniformly among the candidates, so it knows the protein's shape and nothing else.
    """
    n = len(coords)
    if generator == "white_noise":
        return rng.standard_normal((n, b))
    if generator == "smooth_gaussian":
        return factor @ rng.standard_normal((factor.shape[1], b))
    if generator == "smooth_t":
        # The same covariance, with Student-t marginals at 3 degrees of freedom. Heavy tails
        # change which residues take the extreme ranks without changing the spatial scale.
        normal = factor @ rng.standard_normal((factor.shape[1], b))
        return normal / np.sqrt(rng.chisquare(3, size=(1, b)) / 3)
    if generator == "distance_shell":
        # Negated distance to a random candidate, plus a small smooth perturbation. This is
        # the shape every distance-correlated baseline in this repository has, and it is the
        # adversarial case for a test whose two sides differ in size: it is maximally blocky.
        centres = rng.integers(0, n, size=b)
        distance = np.linalg.norm(coords[:, None, :] - coords[None, centres, :], axis=-1)
        return -distance + 0.25 * (factor @ rng.standard_normal((factor.shape[1], b)))
    raise ValueError(f"unknown generator {generator!r}")


def endpoint_b_size_and_power(
    target: str,
    *,
    generators: tuple[str, ...] = GENERATORS,
    correlation_lengths: tuple[float, ...] = (4.0, 8.0, 12.0, 20.0),
    deltas: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0),
    n_size: int = 20000,
    n_power: int = 10000,
    alpha: float = 0.05,
    seed: int = 0,
) -> dict:
    """Size under each null, and power against a shift on the label set, for one arm.

    Power is measured with the shift on the LABEL set for both endpoints, because that is the
    signal a method is asked to produce. `site` scoring near zero there is the finding ADR
    0039 rests on, not a bug in the simulation.
    """
    graph = evaluation_graph(apo_input(target))
    candidates = list(graph.candidates)
    at = {residue: i for i, residue in enumerate(candidates)}
    coords = graph.ca_coord[graph.index(candidates)]
    frozen = json.loads(EVALUATION_FROZEN.read_text())["targets"][target]
    site = np.array([at[r] for r in frozen["decoys"]["site_pocket"]["lining"]])
    decoys = [
        np.array([at[r] for r in pocket["lining"]])
        for pocket in frozen["decoys"]["pockets"].values()
    ]
    labels = np.array([at[r] for r in _positives(target)[0]])
    positives = {"site": site, "label": labels}
    factors = {lam: field_factor(coords, lam) for lam in correlation_lengths}

    def run(generator, lam, n, shift, stream):
        rng = np.random.default_rng([seed, stream])
        out = []
        for start in range(0, n, BLOCK):
            b = min(BLOCK, n - start)
            fields = _draw(generator, factors[lam], coords, rng, b)
            if shift is not None:
                fields = fields.copy()
                fields[labels] += shift
            out.append(fields)
        return out

    result = {
        "target": target,
        "seed": seed,
        "n_candidates": len(candidates),
        "n_labels": int(len(labels)),
        "site_lining": int(len(site)),
        "n_decoys": len(decoys),
        "decoy_lining_sizes": sorted(int(len(d)) for d in decoys),
        "minimum_attainable_p": frozen["decoys"]["minimum_attainable_p"],
        "size": {},
        "power": {},
    }
    stream = 0
    for generator in generators:
        for lam in correlation_lengths:
            stream += 1
            batches = run(generator, lam, n_size, None, stream)
            for name, idx in positives.items():
                p = np.concatenate([_p_values(f, idx, decoys) for f in batches])
                key = f"{generator}/lambda={lam}/{name}"
                result["size"][key] = {
                    "stream": stream,
                    "n": n_size,
                    "size": round(float((p <= alpha).mean()), 6),
                    "median_p": float(np.median(p)),
                    "min_p": float(p.min()),
                }
    for delta in deltas:
        stream += 1
        batches = run("smooth_gaussian", 8.0, n_power, delta, stream)
        for name, idx in positives.items():
            p = np.concatenate([_p_values(f, idx, decoys) for f in batches])
            result["power"][f"delta={delta}/{name}"] = {
                "stream": stream,
                "n": n_power,
                "power": round(float((p <= alpha).mean()), 6),
            }
    return result
