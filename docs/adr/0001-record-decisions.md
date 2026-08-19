# 0001 — Record research decisions as ADRs

**Status:** accepted · 2026-08-19

## Context

This is a multi-phase research project executed largely by agents across many
sessions with no shared memory. The expensive failure mode is not bad code — it is
silently re-deciding a settled question, or losing the reason behind a choice and
later "fixing" it back to something already ruled out.

## Decision

Every decision that constrains a later phase gets a short ADR in `docs/adr/`.
Every run that produces a comparable number gets an entry in `experiments/REGISTRY.md`.
Together these are the project's long-term memory; an agent starting cold reads
`docs/ROADMAP.md`, then the registry, then the relevant ADRs.

## Consequences

Slight overhead per decision. In exchange, the methodological report at the end is
largely assembled from artifacts written while the reasoning was fresh, rather than
reconstructed from memory at deadline.
