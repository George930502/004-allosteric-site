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
"never". These four span the DEPENDENCE shapes a real scorer takes: none at all, smooth and
Gaussian, piecewise-constant over spatial clusters, and the blocky monotone-in-distance shape
that every distance-correlated baseline in this repository actually has.

**A rank test cannot see a marginal distribution, and the first four generators forgot it.**
The set replaced `smooth_t` on 2026-09-03, after an adversarial pass showed its ranks are
IDENTICAL to `smooth_gaussian`'s at the same seed. The construction was the standard
multivariate-t one, a Gaussian field divided by a single chi-square draw per replicate, and
dividing a whole column by one positive scalar is monotone within that column. Every statistic
here is a midrank, so the two generators are one law and the run measured three, not four.

The lesson generalises past that one bug: **no elementwise monotone transform of a field can
change this test**, so heavy tails, log-normal marginals and rescaling are all the same null.
Only the copula moves the answer. `cluster_blocks` replaces it with a genuinely different
copula rather than a different marginal -- each residue takes its nearest random centre's
i.i.d. value, so the field is piecewise constant with hard boundaries. It is chosen in the
adversarial direction, because blockiness is what made `distance_shell` the worst case.
"""

from __future__ import annotations

import json

import numpy as np
from scipy.stats import rankdata

from allo.inputs import apo_input
from allo.scoring.harness import EVALUATION_FROZEN, _positives
from allo.scoring.nulls import evaluation_graph, field_factor

BLOCK = 2500
GENERATORS = ("white_noise", "smooth_gaussian", "cluster_blocks", "distance_shell")


def _ranks(fields: np.ndarray) -> np.ndarray:
    """Column-wise midranks, the same statistic `allo.scoring.metrics.rank_vector` computes.

    **Corrected 2026-09-03.** This assigned ORDINAL ranks by stable sort, with a docstring
    saying "the fields are continuous, so there are no ties". That held for the first three
    generators and stopped holding when `cluster_blocks` arrived, whose whole construction is
    tied blocks -- a hundred residues take about four distinct values. Residue index was
    breaking those ties, and residue index runs along the chain, so it correlates with space.
    The published `cluster_blocks` cells were not the statistic they claimed to be.

    The shipped scoring path never had this defect: `metrics.rank_vector` calls
    `rankdata(..., method="average")` and says why. This is the same call, over columns, and
    `test_the_simulation_ranks_agree_with_the_shipped_statistic` pins that they agree.
    """
    return rankdata(fields, method="average", axis=0).astype(np.float32)


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
    if generator == "cluster_blocks":
        # Piecewise constant over a random Voronoi partition: pick `k` centres uniformly among
        # the candidates and give every residue its nearest centre's i.i.d. value. Hard
        # boundaries, so the copula is unlike the smooth field's, which is the point --
        # see the module docstring on why a heavy-tailed MARGINAL was no null at all.
        k = max(2, n // 25)
        centres = np.stack([rng.choice(n, size=k, replace=False) for _ in range(b)])
        value = rng.standard_normal((k, b))
        out = np.empty((n, b), dtype=np.float64)
        for j in range(b):
            nearest = np.linalg.norm(coords[:, None, :] - coords[centres[j]][None], axis=-1)
            out[:, j] = value[nearest.argmin(1), j]
        return out
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
    # The power stage used to hardcode lambda = 8.0 and then index `factors[8.0]`, so any
    # `correlation_lengths` without it completed the size stage and died with a KeyError.
    # It takes the middle of the sweep now, and the default sweep still gives 8.0.
    # Round 6, 2026-09-03.
    power_lambda = sorted(correlation_lengths)[max(0, (len(correlation_lengths) - 1) // 2)]
    result["power_correlation_length"] = power_lambda
    for delta in deltas:
        stream += 1
        batches = run("smooth_gaussian", power_lambda, n_power, delta, stream)
        for name, idx in positives.items():
            p = np.concatenate([_p_values(f, idx, decoys) for f in batches])
            result["power"][f"delta={delta}/{name}"] = {
                "stream": stream,
                "n": n_power,
                "power": round(float((p <= alpha).mean()), 6),
            }
    return result
