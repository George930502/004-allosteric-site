# Architecture / research decision records

One file per decision that is expensive to reverse or that a future reader would
otherwise re-litigate. Format: `NNNN-short-slug.md`, statuses `proposed` /
`accepted` / `superseded by NNNN`.

Write one when: a modelling choice constrains later phases, a method is chosen over a
credible alternative, or a constraint interpretation is settled. Do not write one for
routine implementation details.

Statuses also include `withdrawn`, for a decision whose subject matter no longer exists. A
withdrawn ADR keeps the rule it established, in case it becomes live again, and says why it
stopped binding. It is never deleted.

## Reading ADRs written before 2026-08-24

On 2026-08-24 the benchmark was reduced from eleven arms to five, and the evaluation protocol
was separated from the input layer. Earlier ADRs therefore refer to things that have moved:

| An older ADR says | It now lives at |
| --- | --- |
| `docs/benchmark/README.md` §5 | `docs/benchmark/evaluation/README.md` (frozen 2026-08-25) |
| `cardiac_myosin_site1_*` | `cardiac_myosin_*` — there is one myosin site |
| `bcr_abl1_sensitivity`, `bcr_abl1_trimmed`, `cardiac_myosin_site2_corrected`, the `8QYP`, `9YRG` and `2G1T` arms | removed; recoverable from git at `363633c` and listed in `docs/ROADMAP.md` Phase 5 |
| `docs/benchmark/audit/*.json` | deleted — they were self-declared duplicates of the `.md` and nothing loaded them |

The reasoning in those ADRs is unchanged. Only the names are stale.
