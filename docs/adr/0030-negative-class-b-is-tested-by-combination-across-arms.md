# 0030 — Negative class (b) is tested by combination across arms, and the detector is re-frozen on decoy count

**Status:** accepted · 2026-09-02 · opens evaluation **protocol version 3** · supersedes
item 1 of [`../benchmark/review/07-metrics-audit.md`](../benchmark/review/07-metrics-audit.md)

## Context

`CHALLENGE.md` §4.1 makes two negative classes half of the success criterion: random
background residues, and **non-functional surface pockets**. The frozen protocol tests the
second with a pocket-rank permutation. Each detected pocket contributes one number — the mean
midrank of its lining — and the site pocket is ranked against the decoys:

```
p = (1 + #{decoy_rank >= site_rank}) / (1 + n_decoys)
```

Version 2 disclosed a floor of `1/(1 + n_decoys)`, which is 0.25 on two of the three
confirmatory arms. The organisers answered on 2026-09-02 that no detector is prescribed and
that each team designs its own decoy set. That answer is new information arriving after the
version-2 freeze, which is the same kind of event that reopened version 1.

**The floor turned out to be a symptom.** The statistic is one draw per pocket, so its power
tends to `1 - Φ(z_{1-α} - δ)` where `δ` is the site pocket's separation from the decoy
distribution in standard deviations. Setting power to 0.80 gives

```
δ >= z_0.95 + z_0.80 = 1.645 + 0.842 = 2.487
```

**No decoy count changes that number.** A pocket-level effect of 2.5 standard deviations is
very large. The test is descriptive on the whole confirmatory family, whatever the detector
does.

**Three replacements were measured before any was recommended**, through the same type-I gate
ADR 0018 applies to the matched-patch null: draw a stochastic, site-uninformative, spatially
autocorrelated field, run the test, repeat 1000 times, and read the rejection rate against
the exact central 95 % binomial band, which is [0.037, 0.064].

| construction                              | measured type-I rate | verdict                                                        |
| ----------------------------------------- | -------------------- | -------------------------------------------------------------- |
| A — pocket permutation (frozen)           | 0.000–0.032          | conservative, consistent with the floor                        |
| B — residue-level rank test               | **0.132–0.384**      | anti-conservative by 3× to 8×                                  |
| C — size-matched patch in the decoy union | not computable       | on both KRAS arms no decoy pocket is as large as the label set |

Construction B is worse than the unmatched background null that §4.1 of the protocol already
rejects at 0.10–0.32. An independent metrics audit recommended it as a critical fix. Installed
unmeasured, it would have given the report a headline test with a true size near 0.35.

**Detector supply is the binding constraint, and it is arithmetic about small proteins.**
Nine pyKVFinder settings were swept on the five primary arms. `kras_g12c_corrected` reaches
at most 18 decoy pockets, a floor of 0.0526, still above α. A 169-residue protein does not
carry 19 non-functional surface pockets.

**The sweep also found a reporting defect that is independent of power.** Under the frozen
settings the pocket the protocol calls "the site" on `bcr_abl1_corrected` covers **two thirds**
of its label set. The published pocket-rank convention is being applied to a pocket that is
only partly the site.

| arm                        | site coverage, frozen | site coverage, loosest tried |
| -------------------------- | --------------------: | ---------------------------: |
| `kras_g12c_corrected`      |                  0.75 |                       0.9375 |
| `bcr_abl1_corrected`       |            **0.6667** |                       0.9444 |
| `bcr_abl1_mandated`        |                  0.85 |                         1.00 |
| `cardiac_myosin_corrected` |                  1.00 |                         1.00 |

## Decision

**1. Keep the pocket-rank test, and keep reporting it. It is never a decision.** It is the
field's own convention and it is what a reader compares to APOP and PASSer. Label it
descriptive.

**2. State the limit honestly, and stop calling it a floor on some arms.** The correct
statement is that the test needs `δ >= 2.49` for 80 % power at any decoy count, so it is
descriptive on the whole confirmatory family.

> **CORRECTED 2026-09-02, after this ADR was accepted.** `2.487` is the `n → ∞`
> normal-quantile limit, not the power of the discrete rank test the code runs. Integrating
> the exact binomial mixture at α = 0.05 gives power **0.7173 at 19 decoys, 0.6530 at 31,
> 0.7718 at 84, 0.7888 at 139, and only 0.7959 at 400** — and rejection is **impossible** at
> 18 decoys or fewer, where the floor `1/(1+n)` exceeds α. The conclusion is unchanged and
> strengthened: the test is **weaker** than `δ = 2.487` implies at every frozen decoy count,
> so the requirement stated above understates the effect it needs. Reproduced independently
> in [`../benchmark/review/26-third-pass-synthesis.md`](../benchmark/review/26-third-pass-synthesis.md).

**3. Do not add a residue-level decoy test.** Its measured size is 0.13 to 0.38. This
supersedes item 1 of the metrics audit, which was written before the calibration ran.

**4. Add a Fisher combination across the three confirmatory arms as the tested form of
negative class (b).** Report Stouffer beside it. Both are declared here, before any method is
scored.

| family                                      | per-arm floors      | Fisher minimum p | Stouffer |
| ------------------------------------------- | ------------------- | ---------------: | -------: |
| three confirmatory arms, frozen detector    | 0.25, 0.10, 0.024   |       **0.0214** |   0.0115 |
| three confirmatory arms, re-frozen detector | 0.053, 0.031, 0.012 |           0.0014 |  0.00045 |

**Label it correctly.** Fisher and Stouffer test the intersection null — no arm has signal —
so a rejection licenses "at least one arm distinguishes the site from non-functional surface
pockets". It is not a generalisation claim. That is the same scope §8 of the protocol already
declares for the confirmatory arms.

**5. Re-freeze the detector settings, selecting on `n_detected` alone.** The new settings are
`probe_out 8.0`, `removal_distance 1.2`, `volume_cutoff 1.0`, with `step` and `probe_in`
unchanged.

> **CORRECTED 2026-09-02, after this ADR was accepted.** This decision was written as
> "selecting on `n_decoys` alone", justified by "`n_decoys` is label-free and is a
> sample-size criterion". **That justification is false.** `allo.scoring.decoys.classify`
> picks the site pocket by maximum label coverage, and admits a pocket as a decoy only when
> its lining holds no label and clears the halo, so `n_decoys` is a function of the answer
> key by construction. The criterion that is genuinely label-free is `n_detected`, the number
> of pockets the detector returns before any label is consulted.
>
> **The freeze does not move.** `n_detected` selects `probe_out 8.0, removal_distance 1.2,
volume_cutoff 1.0` on all five arms in the committed sweep, with no tie — the same setting
> `n_decoys` selects. Only the criterion of record changes. Measured in
> `../benchmark/review/data/decoy-power-sweep.json`; the manifest and the layer README carry
> the same correction.
>
> One residual cost stands. The committed sweep holds five arms while the manifest describes
> it over fifteen, so the agreement between the two criteria cannot be re-checked on the
> sealed `generalisation` tier without opening it. Selecting on `n_detected` removes the need
> to, because it never consults a label at all.

**Report site coverage as a consequence, never as the selection target.** Choosing a setting
because it covers more labels would shape the negative class with the answer key.

**6. Do all of it before any candidate method is scored on the primary arms**, and record it
as **protocol version 3**.

## Consequences

- `evaluation/manifest.yaml` moves to `version: 3`. `detector_settings` changes, and
  `nulls.decoy_pockets` gains the combination test. `evaluation/frozen.json` is re-derived,
  so every arm's decoy pocket set and lining moves.
- `uv run allo evaluate verify --detect` must be re-run. The offline verify alone does not
  re-derive the pockets.
- The `bcr_abl1_corrected` site pocket stops covering two thirds of its label set.
- **The family floor falls from 0.021 to 0.0014.** Negative class (b) becomes testable at
  α = 0.05, at the family level, with no input-layer change.
- **Per-arm negative-class-(b) p-values stay descriptive on every arm.** The combination is
  the only tested form. Nothing about the per-arm numbers becomes a decision.
- The decoy construction is documented in the submission. The organisers require it, and no
  other team's negative class will be comparable to ours.
- Version 2's disclosed power floor is not withdrawn. It was true. Version 3 replaces the
  remedy, not the disclosure.

## Alternatives rejected

**More decoy pockets.** Rejected on the ceiling: 80 % power at `δ = 2.5` needs 289 decoys, and
`δ <= 2.0` is unreachable at 400. KRAS cannot supply 19.

**Construction B, the residue-level test.** Rejected on its measured size of 0.13 to 0.38.
The mechanism is known: the label set is one contiguous blob and a uniform draw from a pool
spread over 3 to 41 discrete pockets scatters it, so the null has too little variance.

**Construction C, patches inside the decoy union.** Rejected as not drawable. On both KRAS
arms no decoy pocket is as large as the label set, and on `bcr_abl1_corrected` exactly one is,
which floors that construction at 0.5.

**Leaving negative class (b) untested.** Rejected: it is half of the challenge's stated
success criterion, and a tested form exists that needs no input-layer change.
