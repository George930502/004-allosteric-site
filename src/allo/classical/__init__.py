"""Classical baselines and coupling measures: pipeline stages S3-S7 in classical form.

`docs/ROADMAP.md` §1.4 lists what has to be here and why. The challenge asks for a
comparison to classical analogs, and the review makes three of them mandatory rather than
optional: a distance-only control, an eigenvector-centrality control, and the geometric
`cavity_volume` detector score. A method that does not beat all three has demonstrated
nothing.

Three registries. `baselines.SCORERS` is the standard battery any reviewer expects.
`coupling.SCORERS` is the set of candidates the Phase-2 exploration sweep added, each
answering a question the standard battery cannot -- interventional response, route
redundancy, and directional coupling. `mechanism.SCORERS` holds three constructions read off
the cross-system mechanism review rather than off any method paper. `SCORERS` is their
union.

Prediction-path code. It never imports `allo.groundtruth` or `allo.scoring`.
"""

from allo.classical import baselines, coupling, mechanism
from allo.classical.baselines import SOURCE_BLIND, SOURCE_CONDITIONED
from allo.classical.postprocess import (
    consensus,
    decay_residual,
    diversified_top_k,
    fit_decay,
    spatial_smoothing,
)

SCORERS = baselines.SCORERS | coupling.SCORERS | mechanism.SCORERS

__all__ = [
    "SCORERS",
    "SOURCE_BLIND",
    "SOURCE_CONDITIONED",
    "baselines",
    "consensus",
    "coupling",
    "decay_residual",
    "diversified_top_k",
    "fit_decay",
    "mechanism",
    "spatial_smoothing",
]
