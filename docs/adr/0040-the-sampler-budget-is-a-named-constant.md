# 0040 — The matched-patch sampler's rejection budget is a named constant

**Status:** accepted · 2026-09-03 · no protocol version change

## Context

`nulls.matched_patch` took `max_attempts_per_patch: int = 4000` as a default argument. The
constant appears in no frozen document. A `grep` over the whole of `docs/benchmark/` returns
nothing.

It decided a recorded outcome. On the 0.05 tolerance rung of the sweep,
`cardiac_myosin_mandated` drew 822 of 999 patches and the run was written up as an arm the
sampler cannot fill. 999 × 4000 = 3,996,000, which is exactly the attempt count
`evaluation/README.md` §0.1 records. The budget was exhausted, not the arm.

## What the audit measured

Script and raw output:
`../benchmark/review/data/endpoint-b-2026-09-03/s5_t005_n999_cap10000.json` and
`s5_t010_n999_cap4000.json`, `s5_t005_n999_cap10000.json`,
`s5_t010_n999_cap4000.json`.

- Re-drawn fresh at cap 4000, the rung reproduces 822 of 999 at acceptance 0.000206.
- **At cap 10 000 the same rung draws all 999**, in 4,784,846 attempts, 47.9 % of budget.
- At the frozen tolerance of 0.10 it draws in 1,130,304 attempts, 28.3 % of budget, acceptance
  0.000884, which matches the probe already cited in the README.
- The cap binds only when acceptance falls below 2.5 × 10⁻⁴. The worst margin over all fifteen
  gate arms is 3.5× on `cardiac_myosin_mandated`, and the next is 44.8×.


**These are the recorded outputs, not a re-runnable script.** The simulations import
`allo.inputs` and `allo.scoring`, and a tracked file inside the review tree may import no
`allo` module (ADR 0034), so the scripts could not live beside their output and
`experiments/` could not hold them either. Each JSON carries the seed, the sample size, the
arm and the interval, which is enough to check the arithmetic and to rebuild the run, and it
is less than the repository asks for elsewhere. `../benchmark/review/data/endpoint-b-2026-09-03/README.md`
states the rule that produced the gap. The endpoint-b measurement was afterwards moved into
`allo.scoring.simulate` and re-run as a tracked experiment; the FWER and budget simulations
were not, and that is recorded here rather than claimed away.

## Decision

Name it `nulls.MAX_ATTEMPTS_PER_PATCH = 4000` and keep the value. A constant that can decide
an outcome must be visible to the reader who quotes the outcome.

The value stays at 4000 because raising it changes no scored number at the frozen tolerance of
0.10, and changing a sampler setting to alter an outcome is what this layer exists to prevent.

## Consequences

- No frozen value moves and no protocol version opens.
- `evaluation/README.md` §0.1 describes the 0.05 rung as an arm the sampler cannot fill. It is
  a rung whose budget was exhausted. The correction is recorded in
  `../benchmark/review/27-fourth-pass-synthesis.md`, not edited into the freeze.
- If a future tolerance rung falls below 3.5× the binding acceptance, raise the constant and
  say so in an ADR rather than in a run script.
