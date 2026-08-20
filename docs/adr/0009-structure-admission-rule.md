# 0009 — Structure admission: resolution is a selection rule, so it binds only where we select

**Status:** accepted · 2026-08-20

## Context

`docs/benchmark/README.md` §7 carried "No resolution ceiling is declared" as an open item,
together with a draft rule — **X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å, mandated tier exempt** —
and the observation that "every `corrected` and `sensitivity` entry is 1.15–3.7 Å and would
clear a 4.0 Å cryo-EM-inclusive bar". Those two sentences contradict each other, and both
are wrong on the numbers. Read out of the deposited files:

| entry  | method  |  resolution | R-free | tiers it serves                  |
| ------ | ------- | ----------: | -----: | -------------------------------- |
| `4LDJ` | X-ray   |      1.15 Å | 0.1622 | corrected                        |
| `4OBE` | X-ray   |      1.24 Å | 0.1686 | mandated                         |
| `6OIM` | X-ray   |      1.65 Å | 0.2152 | mandated, corrected              |
| `2G1T` | X-ray   |      1.80 Å |  0.244 | sensitivity                      |
| `8QYR` | X-ray   |      1.80 Å |  0.227 | sensitivity                      |
| `8QYU` | X-ray   |      1.96 Å |  0.235 | sensitivity                      |
| `2G2H` | X-ray   |      2.00 Å |  0.213 | corrected                        |
| `5MO4` | X-ray   |      2.17 Å | 0.2170 | mandated, corrected, sensitivity |
| `9F6C` | X-ray   |      2.33 Å | 0.2440 | corrected                        |
| `8QYP` | X-ray   | **2.759 Å** | 0.2478 | **corrected**, sensitivity       |
| `9GZ2` | cryo-EM |      2.90 Å |      — | corrected                        |
| `9YR7` | cryo-EM |      3.00 Å |      — | sensitivity                      |
| `9YRG` | cryo-EM |      3.20 Å |      — | sensitivity                      |
| `9GZ3` | cryo-EM |      3.40 Å |      — | corrected                        |
| `1OPL` | X-ray   |      3.42 Å |  0.315 | mandated                         |
| `6C1H` | cryo-EM |      3.90 Å |      — | mandated                         |
| `5TBY` | model   |     20.00 Å |      — | mandated                         |

The true corrected/sensitivity span is **1.15–3.40 Å**, not 1.15–3.7. And the draft rule
does not survive contact with it: **`8QYP` at 2.759 Å fails an X-ray ≤ 2.5 Å ceiling**, and
`8QYP` is the apo input of three frozen arms — including `cardiac_myosin_site2_corrected`,
which is a _corrected_ tier arm and the benchmark's only deliberately proximal site. A rule
that silently deletes a corrected arm is not a rule anyone had checked.

The obvious repair — move the X-ray bar to 2.8 Å so everything fits — is the one to refuse.
That is choosing a threshold by looking at which structures we already picked, which is the
same species of error as tuning a hyperparameter on the test set.

## Decision

**A resolution ceiling is a _selection_ rule. It binds only where there is a selection to
make.** The two halves of this benchmark differ in exactly that respect, so they get
different treatment.

1. **Primary benchmark (KRAS, BCR-ABL1, cardiac myosin): no resolution ceiling.** These
   arms are not sampled from a pool. Each is hand-specified per target as the best available
   structure of _that_ biology — for several sites, the only one that exists. Filtering here
   would not raise quality, it would delete targets the challenge names. Instead:
   **resolution, method and R-free are disclosed per entry** (the table above; regenerate
   from the deposited files) and any entry that would fail the clause-2 bar is flagged where
   it is used.
2. **ASD selection set and every generalisability set: X-ray ≤ 2.5 Å, cryo-EM ≤ 4.0 Å,
   experimental structures only.** Applied as a _pre-filter over candidates_, before any
   target's identity or difficulty is examined. This is where a pool exists and therefore
   where a ceiling does work. The bar matches PocketMiner / CryptoBench / Binding MOAD
   (2.5 Å) rather than the stricter Wankowicz 2.0 Å, which would leave the candidate pool
   too thin after the other clauses.
3. **Computational models are excluded everywhere except the mandated tier**, where
   `CHALLENGE.md` Table 1 forces `5TBY` on us. A homology model is not an experimental
   observation and cannot ground a ground truth.
4. **No entry is admitted or rejected on resolution alone after the fact.** Changing an
   arm's structure remains a manifest edit plus a re-freeze, visible in the diff.

Resolutions are not added to `frozen.json`. They are already pinned transitively: every
entry's file `sha256` is frozen, so a changed deposition fails `allo benchmark verify`
before its resolution could drift.

## Consequences

- The `8QYP` arms stay, and the reason they stay is stated rather than assumed. `8QYP`
  (2.759 Å) is now explicitly the lowest-resolution X-ray input in the scoreable set, and
  the report says so when it reports Site 2.
- `1OPL` (3.42 Å, R-free 0.315, **6.50 % RSRZ outliers** — read from the wwPDB validation
  report; a 22 % figure circulated in this repo and was a percentile mistaken for a
  percentage) and `5TBY` (20 Å model) remain in the
  mandated tier under clause 1, which is the only way to report what the challenge asked for.
  Their quality is a stated property of that tier, and part of why the corrected tier exists.
- The ASD set will be smaller than an unfiltered pull. That is the intended cost: the
  selection set is where hyperparameters get chosen, so its inputs must not be the excuse
  for a later failure.
- **Risk accepted.** Clause 1 means the primary benchmark's inputs are heterogeneous in
  quality — 1.15 Å to 3.9 Å across tiers. A method could look better on KRAS partly because
  KRAS has the sharpest structures. The mitigation is disclosure plus the per-target
  reporting the evaluation layer already mandates; there is no pooled cross-target claim for
  the heterogeneity to contaminate (`docs/benchmark/README.md` §5).
- Supersedes nothing. Completes the input-layer admission criteria begun in ADR 0003
  (tiers), ADR 0004 (identity), ADR 0005 (active site), ADR 0006 (nodes), ADR 0007
  (allosteric ground truth) and ADR 0008 (one target per site).
