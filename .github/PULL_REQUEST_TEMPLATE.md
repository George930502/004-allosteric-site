## What and why

<!-- One paragraph. Link the phase in docs/ROADMAP.md or the experiment directory. -->

## Checks

- [ ] `make check` passes
- [ ] No holo-derived data reaches the prediction path (constraint C1)
- [ ] No MD trajectories introduced as input (C2)
- [ ] Any new quantum method reports qubit count and circuit depth (C3)
- [ ] Stochastic steps take an explicit seed
- [ ] No frozen artifact was edited in place (`docs/benchmark/**/frozen.json`). A freeze
      changes only through an ADR that supersedes it, and a new protocol version
- [ ] Every score goes through `allo.scoring.score_arm`, and no other path
- [ ] `make verify` run and pasted, if this touches a freeze
- [ ] Registry / ADR / roadmap updated if this changes what we believe
