---
description: Audit the working diff against the challenge's hard constraints
---

Run the audit in `docs/playbooks/constraint-audit.md` against the current diff
(`git diff` plus untracked files; if arguments name a range or path, use that).

Trace imports for real — the C1 apo-only check means following what actually reaches
the prediction path, not reading module names. Report findings most severe first with
file and line, and say plainly if nothing is wrong.

Scope: $ARGUMENTS
