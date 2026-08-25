"""Evaluation layer: the one scoring path every method is compared through.

Frozen separately from the input layer and with its own freeze date, because the two move
at different rates. `docs/benchmark/evaluation/README.md` is the protocol; this package is
its implementation.

Evaluation-side by construction: it reads the frozen label sets, so nothing on the
prediction path may import it.
"""

from allo.scoring.harness import compare_methods, holm, protocol, score_arm

__all__ = ["compare_methods", "holm", "protocol", "score_arm"]
