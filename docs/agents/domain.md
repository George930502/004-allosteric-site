# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## This repo

**Single-context.** No `CONTEXT-MAP.md`, no per-context `src/<context>/docs/adr/`.
`CONTEXT.md` exists at the repo root and is the settled vocabulary. Read it before you
name a domain concept. It is hand-written, not generated, so do not let
`/domain-modeling` overwrite it.

`docs/adr/` is already populated and is the project's decision record; see
`docs/adr/README.md` for the local conventions (statuses, when to write one). ADRs here
cover research decisions as well as architectural ones — e.g. `0002` records the
working quantum-metric hypothesis.

## File structure

Single-context repo (most repos):

This repo, as it actually stands:

```
/
├── CONTEXT.md                         ← the settled vocabulary
├── docs/adr/                          ← 41 records, indexed by topic in README.md
│   ├── 0001-record-decisions.md
│   └── 0025-the-size-rescale-is-calibrated-at-every-holm-level.md
└── src/allo/                          ← organised by pipeline stage
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
