# 0043 — A former name is protected too, and the ledger of them is tracked rather than derived

**Status:** accepted · 2026-09-03 · extends the C1 file-read guard · no protocol version change

## Context

`PROTECTED_PATHS` protects a path **by its name**. `tests/test_no_leakage.py` refuses a
prediction-path module that spells `docs/benchmark/primary/audit/kras-g12c.md`, and every
other route named in `AGENTS.md`.

A rename gives the same bytes a second name that no entry covers. The three per-target input
audits moved from `docs/benchmark/audit/` to `docs/benchmark/primary/audit/` on 2026-08-31,
and `git show <sha>:docs/benchmark/audit/kras-g12c.md` still returns the whole KRAS contact
shell — from `main`, with no network, under a path the guard reads as ordinary documentation.
Two of the five renames carried a `FROZEN_TOKEN` in the file name and were backstopped by the
token scan; the three audits carried none. That is the same asymmetry that left `data/patches`
readable for nine days in September.

A first fix derived the list from `git log --diff-filter=R` at import time. An adversarial pass
broke it two ways on the same day.

1. **Clone depth.** A `git fetch --depth=1` and a `git archive` export both produce an empty
   set, and a machine with no `git` binary raises during collection. **A guard that is weaker
   in an export than in a working clone is weakest exactly where a release is verified.**
2. **A conversion is not a rename.** The same three audits had existed as `.json` before the
   Markdown conversion. Git recorded a delete plus an add, because the bytes changed too much
   for rename detection, so `--diff-filter=R` never saw them. Those files reproduce every
   primary label set and stay readable through `git show <sha>^:<path>`. The ledger was stale
   the day it was written and no test could tell.

## Decision

**1. A former name is protected, and the tracked ledger is the source.**
`tests/former_protected_paths.json` is the authority. The guard reads it, so it is equally
strong in a shallow clone, in a `git archive` export, and with no `git` binary at all.

**2. Git cross-checks the ledger and never replaces it.** `renamed_into_protected_from_git`
returns `None` where there is no history to read, and the test skips the cross-check rather
than passing over an empty set. Where history exists, any path it finds that the ledger lacks
is a failure.

**3. The filter is `RD`, and a directory that lost a file to a protected tree is itself a
former protected tree.** A deletion leaves the same artefact as a rename: content that was
protected, under a name that is not. The second half is what covers a format conversion, whose
whole signature is that git sees no rename. Eight ledger entries became sixteen.

## Consequences

- The guard binds prediction modules, not people. A reader may open any of these files; a
  module on the prediction path may not name one, in any spelling the segment cover reaches.
- **This does not make the boundary airtight and the test says so.** A syntax denylist cannot
  enforce an information-flow boundary against a Turing-complete language. An adversarial pass
  built a path out of arithmetic on character codes, with no string, no bytes literal and no
  integer run, and read a protected manifest with all tests green. The ledger closes a class of
  accident, not a class of intent.
- **Regenerating the ledger is a deliberate act.** It is written by running
  `renamed_into_protected_from_git` and saving the result, never at import time, so an entry
  cannot disappear because a clone was shallow.
- **What this still does not reach.** Objects on other branches, on tags, and in the reflog. A
  path that only ever existed on `method-layer-archive` is not in this ledger. That is recorded
  rather than fixed, because the prediction path is built on `main`.
