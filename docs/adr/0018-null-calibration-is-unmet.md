# 0018 — Matched-patch null calibration is unmet

**Status:** accepted · 2026-08-21

## Context

The manifest's 0.20 exposure tolerance and 20,000,000-attempt budget were justified by
session observations for which the repository has no generator, configuration, raw metrics,
or experiment directory. They move scores and cannot be frozen under R2/R3.

## Decision

Choose option (b): record calibration as unmet. Withdraw both numbers from the manifest,
generated freeze, benchmark prose, and executable schema. Do not score a method with the
matched-patch null until a seeded implementation and complete experiment artifact regenerate
the parameters.

## Consequences

Phase 2 is blocked. The cost is loss of the presently described patch-null endpoint, not a
substitute value inferred from unreproducible notes. The blocker clears when a committed
experiment contains the question, versioned config, seed, implementation, raw/derived
metrics, and notes, and the chosen tolerance and attempt budget are then re-frozen.
