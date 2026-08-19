# Playbook: doing a unit of phase work

Tool-agnostic. Claude Code reaches it via `/phase`; in Codex, say "follow the
phase-work playbook".

The four research principles (R1–R4 in `AGENTS.md`) are checked at the points marked
**[R1]**–**[R4]** below. They are not a preamble to skim.

## Before writing code

0. **[R4]** For anything methodological, read `docs/FIELD.md` — what counts as expert
   practice here, and the traps that produce a confident wrong answer.
1. Read `docs/ROADMAP.md` — which phase is current, what its exit criterion is.
2. Read `experiments/REGISTRY.md` — what has already been tried and what failed.
   Do not re-run a dead end.
3. Read the relevant ADRs in `docs/adr/` for the area you are touching.
4. Re-read the relevant part of `CHALLENGE.md`. The spec, not your memory of it.
5. **[R2]** State the task's success criterion as something a command can check. If
   you cannot, the task is underspecified — say so and ask before building.
6. **[R1]** For each method you are about to use, state in one sentence what physical
   quantity it computes and what assumption makes that quantity meaningful here.
   "It is standard practice" is not a reason.

## While building

- Smallest change that satisfies the criterion. No speculative abstraction, no config
  knob for a value that never changes.
- Every stochastic step takes an explicit seed.
- Numbers come from code, never from recall. No hand-typed residue lists, PDB chain
  IDs, or literature values without a citation in `docs/`.
- If you discover the task conflicts with a hard constraint (C1–C6 in `AGENTS.md`), stop and
  flag it. Never quietly work around C1 (apo-only) or C2 (no MD).

## Before saying done

1. `make check` passes.
2. Run the constraint audit (`docs/playbooks/constraint-audit.md`) if the change
   touches the prediction path, ground truth, or a quantum method.
3. Update the artifacts that carry memory:
   - new comparable number → `experiments/REGISTRY.md`
   - decision that constrains later phases → new ADR
   - phase exit criterion met → `docs/ROADMAP.md` and the README status table
4. **[R3]** Every claim in the writeup names its evidence: an experiment directory, a
   statistical test with its null, a DOI, or an observation with the code path that
   produced it.
5. Report honestly: what passed, what was skipped, what is still open. A partial
   result reported as partial is useful; one reported as complete is a trap.

## Handoff at end of session

Leave the repo readable by an agent with no memory of this session:

- Working tree committed or the uncommitted state explained in the experiment notes.
- The registry reflects every number produced.
- `docs/ROADMAP.md` says what is actually next, not what was next this morning.
