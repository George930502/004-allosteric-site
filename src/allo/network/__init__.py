"""Stage S1: the residue graph a method propagates on.

Separate from `allo.scoring.nulls.evaluation_graph`, and the separation is the point. The
evaluation graph is fixed at the input layer's cutoff and never moves, so two methods'
p-values are comparable. This package builds the graph a *method* chooses, whose cutoff,
node representation and edge weighting are hyperparameters -- chosen on the secondary set's
`development` tier and nowhere else (ADR 0021).

Prediction-path code. It never imports `allo.groundtruth` or `allo.scoring`.
"""

from allo.network.graph import (
    ResidueGraph,
    build,
    min_heavy_distance_to,
    residue_atom_index,
)

__all__ = ["ResidueGraph", "build", "min_heavy_distance_to", "residue_atom_index"]
