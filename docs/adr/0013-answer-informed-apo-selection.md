# 0013 — Remove answer-informed apo selection from confirmatory claims

**Status:** accepted · 2026-08-20 — option 2 now, option 1 as Phase 1.8

## Context

The prediction path satisfies C1: it receives apo coordinates and the legitimate active-site
source, never holo labels. Benchmark construction has a separate bias. `8QYP` was chosen
after comparing apo candidates to holo-defined pocket geometry and apo↔holo RMSD; README §1
calls this the anti-conservative matched-frame criterion. Choosing the apo already closest to
the bound frame can make a site easier to recover and inflate a later confirmatory score.
Pre-registration and disclosure prevent hidden tuning, but they do not remove this selection
bias.

The scope and cost below regenerate from the manifest rather than from a prose count:

```bash
uv run python - <<'PY'
from allo.groundtruth.manifest import read_manifest
m = read_manifest()
scoreable = [s for s in m["targets"] if s.get("status") != "excluded"]
affected = [s["id"] for s in scoreable if s["apo"]["pdb"] == "8QYP"]
confirmatory = [s["id"] for s in scoreable if s["tier"] == "corrected"]
print(len(scoreable), len(confirmatory), affected, sorted(set(affected) & set(confirmatory)))
PY
```

At the current freeze it reports 11 scoreable arms, four confirmatory arms, and three arms
using `8QYP`; one of those three is confirmatory (`cardiac_myosin_site2_corrected`).

## Options

1. **Re-select on apo-only criteria.** Before examining any holo alignment or target-pocket
   geometry, enumerate eligible apo entries and rank them by pinned apo-side criteria:
   identity/construct compatibility, experimental method, resolution, model completeness and
   apo catalytic-state annotation. Apply the site-apo occupancy check only as a pass/fail
   leakage exclusion, not as a closeness objective. Re-freeze every arm whose apo changes.
2. **Quarantine affected arms from claims.** Keep their frozen descriptive results, but do
   not use them for confirmatory or robustness claims. With no replacement this removes three
   of 11 scoreable arms from claim-bearing evidence and one of four confirmatory tests.
3. **Accept and disclose.** Keep the tiers and report the direction of bias. This preserves
   every arm and number but leaves a known anti-conservative selection mechanism in the
   confirmatory family.

## Recommendation

Choose option 1. It preserves the biological sites while making apo accession choice
independent of the holo answer. Until that re-selection is complete, treat the three `8QYP`
arms as answer-informed in every report. If no apo-only candidate passes the predeclared
admission rules, fall back to option 2 rather than option 3.

## Decision

**Option 2 now, option 1 as the follow-up.** The three `8QYP` arms carry
`quarantine: answer-informed apo selection (ADR 0013)` in `manifest.yaml`. They stay frozen,
derived and reported; `claim_bearing_family()` and `robustness_family()` both exclude them,
so they carry no confirmatory or robustness claim.

Option 1 is better and is not available yet: re-selecting an apo means enumerating MYH7
candidates under predeclared apo-only criteria and re-freezing three arms with their labels,
geometry, audit rows and chance lines. That is a phase of work, not a repair, and doing it
badly under time pressure would substitute one selection bias for another. It is booked as
**Phase 1.8**; until it lands, option 2 is the conservative reading, and conservative is the
correct direction when the bias runs anti-conservative.

Option 3 was rejected outright: it leaves a known inflation mechanism inside the family whose
p-values carry the claim, which is the single thing freezing the input layer exists to prevent.

**Consequences.** The confirmatory family falls from four arms to three —
`bcr_abl1_corrected`, `cardiac_myosin_site1_corrected`, `kras_g12c_corrected` — so Holm
corrects across three. Myosin Site 2 has no claim-bearing arm until Phase 1.6. One incidental
gain: the family is now one arm per protein, where before two of four were myosin arms
sharing structures, so the family is less internally dependent than the count suggests.
`claim_bearing_family()` derives this from the manifest. The robustness family is likewise
explicit: `bcr_abl1_sensitivity`, `bcr_abl1_trimmed`, and
`cardiac_myosin_site1_sensitivity_srx`. A later un-quarantine is a manifest change and a
re-freeze, never an edit to a number in prose.

## Cost if accepted

- Reopens three frozen arms and every dependent label, geometry, chance-line and audit row.
- Re-runs `allo benchmark freeze`, `allo benchmark stats`, the structural audit, and both
  repository gates.
- If re-selection fails, the usable claim-bearing set falls from 11 to eight arms and the
  Holm family from four to three. Those are consequences, not changes made by this proposal.
- No tier or arm changes until the PI accepts an option.
