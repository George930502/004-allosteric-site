# 0034 — The review directory is a protected answer key, and its own tools are exempt by a stated rule

**Status:** accepted · 2026-09-02 · adds the seventh data route to
[`tests/test_no_leakage.py`](../../tests/test_no_leakage.py)

## Context

`CLAUDE.md` names six data routes that bypass the import graph, each guarded separately by
`PROTECTED_PATHS` in `tests/test_no_leakage.py`. C1 forbids holo-derived information on the
prediction path and states the bar explicitly: "not even the residue count".

`docs/benchmark/review/` is a seventh route and it was unguarded.

- `03-kras-mask.md` names five real label residues.
- `01`, `02`, `10` and `12` carry per-arm positive counts. C1 names that case directly.
- `data/extension-candidates-2026-09.json` carries holo accessions and effector component IDs
  for candidate arms, which is the same shape as `secondary/selection.json`, already protected.
- `data/structure-evidence.json` carries RCSB metadata for all 28 entries, both halves of
  every pair.

`secondary/evidence/extension-candidates.md` is already a protected **Markdown** answer key on
the identical argument, so the precedent exists and the gap is an omission rather than a
judgement.

**The one-line fix does not work, and it was tried.** Adding the directory to
`PROTECTED_PATHS` fails the suite. Measured: `data/fetch_structure_evidence.py` then names
five protected paths, and all five are its own output.

```
docs/benchmark/review/data
docs/benchmark/review/data/fetch_structure_evidence.py
docs/benchmark/review/data/rcsb-raw
docs/benchmark/review/data/rcsb-raw/_chemcomp
docs/benchmark/review/data/structure-evidence.json
```

The guard resolves `Path(__file__).resolve().parent`, so a script cannot escape by deriving
its output directory from its own location.

**There is nowhere to move the scripts to, and that is a real gap.** `data/` is documented as
holding nothing committed except its README and `.gitkeep` markers. `experiments/` is scanned.
The review README already states the consequence: a probe that opens a label set has no
committed home, so it stays in the scratchpad and its source is reproduced in the prose.

## Decision

**Protect `docs/benchmark/review/` whole**, so a file added there later is protected by
default rather than leaked by default. That is the same rule the evaluation directory was
given, for the same reason.

**Exempt the review's own tools, by a stated rule and not by a list of names.** A file is
exempt from the runner scan when both hold:

1. it is tracked inside `docs/benchmark/review/`, and
2. **it imports nothing from `allo`.**

Condition 2 is what makes the exemption safe. A prediction runner must import the package to
run a method. A file that imports no `allo` module cannot be one. Both current tools —
`fetch_structure_evidence.py` and `decoy_power_sim.py` — use the standard library only, and
that is now a test rather than an observation.

**Keep the third option rejected.** Protecting individual prose files by name would weaken the
protected-by-default rule, and every file added to the directory later would be leaked until
somebody remembered to list it.

## Consequences

- `PROTECTED_PATHS` gains `docs/benchmark/review`. `CLAUDE.md` and `data/README.md` gain the
  seventh route.
- `tests/test_no_leakage.py` gains one exemption predicate and two tests: one that the
  exemption applies only inside the review tree, and one that every exempt file imports no
  `allo` module. A future tool that reaches for the package fails the suite instead of
  silently gaining the answer key.
- The exemption is narrow. It does **not** widen `ALLOWED_PREDICTION_PATHS`, so no prediction
  module gains a route into the tree.
- **The underlying gap is recorded, not closed.** The repository still has no sanctioned home
  for a committed evaluation-side analysis script. The review README states the workaround.
  This ADR exempts two review-side fetchers; it does not create that home.

## Alternatives rejected

**Move both scripts out of the tree.** Rejected: there is nowhere to move them to. `data/`
commits nothing, `experiments/` is scanned, and `src/` is the prediction package.

**Exempt the two files by name.** Rejected: a name list needs maintenance and states no
reason. The import rule states the reason and needs none.

**Protect the prose files individually.** Rejected: it inverts the protected-by-default rule
that the evaluation directory was given for a stated reason, and the next file added would be
unprotected.

**Leave the directory unprotected.** Rejected: it carries per-arm positive counts, which C1
names, and a Markdown answer key is already protected elsewhere on the identical argument.
