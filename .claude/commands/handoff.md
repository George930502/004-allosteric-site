---
description: Leave the repo readable by an agent with no memory of this session
---

Follow the handoff section of `docs/playbooks/phase-work.md`:

1. Every number produced this session has a line in `experiments/REGISTRY.md`.
2. Every decision that constrains later phases has an ADR in `docs/decisions/`.
3. `docs/ROADMAP.md` states what is actually next, and the phase status table in
   `README.md` matches.
4. `make check` passes; the working tree is committed, or the uncommitted state is
   explained in the relevant experiment notes.

Then give a five-line summary: what changed, what is verified, what is open.
