"""Quantum propagation: Hamiltonians, observables, and (later) circuits and noise models.

Pipeline stage S5. `docs/method/review/11-pipeline-decomposition.md` repaired an earlier
assignment that put quantum only at S9: `CHALLENGE.md` §4.1 requires the circuit to simulate
propagation and to output the ranking, so a quantum stage bolted on after the ranking exists
fails the primary objective on its own terms.

Callable without cloud credentials, by design (AGENTS.md, Package layout).
"""

from allo.quantum import connectivity, interference, quantumness
from allo.quantum.walk import SCORERS as WALK_SCORERS
from allo.quantum.walk import hamiltonian

# `interference` isolates the part of a walk that classical diffusion cannot produce, and
# normalises it by the part that classical diffusion can. Unioned here so that a screen sees
# one pool and cannot silently omit the family that tests the challenge's own advantage claim.
SCORERS = WALK_SCORERS | interference.SCORERS | connectivity.SCORERS | quantumness.SCORERS

__all__ = ["SCORERS", "connectivity", "hamiltonian", "interference", "quantumness"]
