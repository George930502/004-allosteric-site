---
description: Scaffold and run an experiment under the project protocol
---

Follow `docs/playbooks/experiment.md`.

Start by writing the one-sentence question this run settles. Scaffold with
`uv run allo new-experiment`, fill `config.yaml` completely (seed included), score
through the shared harness in `src/allo/scoring/`, write `notes.md`, and add the line
to `experiments/REGISTRY.md` — including if the result is negative.

Experiment: $ARGUMENTS
