# Multi-axis review of the three frozen sets

**Opened 2026-09-02**, when the organisers answered four questions about the benchmark. This
directory is the audit those answers forced, plus the wider re-audit run beside it.

**What this is.** `primary/`, `secondary/` and `evaluation/` are the frozen artifacts.
`evidence/` is the literature they rest on. This directory is the **review**: an adversarial
re-examination of all three, from outside, against new information. It mirrors
`docs/evidence/method-landscape/`, which does the same job for the method layer.

**What this is not.** Nothing here is frozen and nothing here changes a freeze. Every
recommendation names the ADR that would have to accept it. A freeze moves when an ADR says
so, never because a review said it should.

**This directory is a protected answer key, and so is everything under it.** It carries
per-arm positive counts and, in `03-kras-mask.md`, five real label residues. C1 names the
residue count directly: "not even the residue count". `tests/test_no_leakage.py` lists the
tree in `PROTECTED_PATHS`, so no prediction-path module and no experiment runner may open it.
Its own tools are exempt by a **rule**, not by a name list: a file is a review tool when it is
tracked inside this tree **and** imports nothing from `allo`. Two tests pin that rule
(ADR 0034). It is the **seventh** data route that bypasses the import graph; six more were found on 2026-09-02 and there are now thirteen (`AGENTS.md`).

**What has since been done.** Read
[`11-synthesis.md`](11-synthesis.md) §"Disposition". Eight ADRs, 0029 to 0036, came out of this
audit, and the primary input layer was re-frozen at six arms on the same day. Protocol version
3 is frozen: `docs/benchmark/evaluation/frozen.json` carries `protocol_version: 3` and
`uv run allo evaluate verify --detect` exits 0 over fifteen arms and 777 decoy pockets.

**A second pass ran the same day, and it audited the first one.** Files `16` to `25`. It found
four blockers the first pass did not, and `25-second-pass-synthesis.md` is its ranked list. Read
that one for the current state; `11-synthesis.md` is the record of the first pass, unedited.

**A third pass then audited the second pass's repairs.** File `26`. It found three C1 leaks —
one of them a finding the second pass had **refuted**, using a detector that could not see
`Tyr164` — a frozen decision rule with no implementation, and a matched-patch cache key that
was identical at three different contact cutoffs. All are repaired.
`26-third-pass-synthesis.md` is the current state; `25` is kept as the record of the second
pass, unedited.

---

## Start here

| Read                                                         | When                                                                                          |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| [`00-official-reply.md`](00-official-reply.md)               | **Always first.** The organisers' four answers, verbatim, and what each one forces            |
| [`27-fourth-pass-synthesis.md`](27-fourth-pass-synthesis.md) | **The current ranked list.** What the fourth pass repaired, the corrections to the freezes, and seven open items |
| [`26-third-pass-synthesis.md`](26-third-pass-synthesis.md)   | The third pass's ranked list, kept as the record of what it found                              |
| [`25-second-pass-synthesis.md`](25-second-pass-synthesis.md) | The second pass's ranked list, kept as the record of what it found                             |
| [`11-synthesis.md`](11-synthesis.md)                         | The first pass's ranked list, kept as the record of what it found                             |

---

## The files

### The organisers' four answers, one file each

| File                                               | Question                            | Headline                                                                    |
| -------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------- |
| [`01-bcr-abl1-chain.md`](01-bcr-abl1-chain.md)     | Which `1OPL` chain?                 | Chain B empties the pocket and deletes the mechanism. Measured both ways    |
| [`02-cardiac-myosin.md`](02-cardiac-myosin.md)     | May `9GZ2` replace `6C1H`?          | The label blocker is gone. Both input blockers are now measured, not argued |
| [`03-kras-mask.md`](03-kras-mask.md)               | Mask the five overlapping residues? | Already done, exactly. Clause (vii) is ratified                             |
| [`04-decoys-and-power.md`](04-decoys-and-power.md) | Is a decoy set prescribed?          | No — and the test we froze cannot reject at any decoy count                 |

### The independent re-audits

| File                                                                       | Scope                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`05-fact-check.md`](05-fact-check.md)                                     | Every checkable claim in the organisers' reply, and the repository's claims about the same entries                                                                                                                                                                                                                                                                                                                         |
| [`06-definition-audit.md`](06-definition-audit.md)                         | The eight-clause apo/holo pair definition, re-attacked against 2025-2026 literature and against the pharma frame                                                                                                                                                                                                                                                                                                           |
| [`07-metrics-audit.md`](07-metrics-audit.md)                               | The frozen evaluation protocol's endpoints, nulls, omissions and multiplicity                                                                                                                                                                                                                                                                                                                                              |
| [`07a-metrics-fact-check.md`](07a-metrics-fact-check.md)                   | Independent verification of the new citations in `07`                                                                                                                                                                                                                                                                                                                                                                      |
| [`08-structure-evidence.md`](08-structure-evidence.md)                     | Live RCSB evidence for all 28 entries: validation percentiles, ligand fit, assemblies, gaps                                                                                                                                                                                                                                                                                                                                |
| [`09-extension-sweep.md`](09-extension-sweep.md)                           | Every allosteric and structural database, reachability today, and how far the benchmark can grow                                                                                                                                                                                                                                                                                                                           |
| [`10-cross-set-consistency.md`](10-cross-set-consistency.md)               | All twelve clauses against all fourteen arms. Horizontal and vertical alignment. **Superseded by `19` — it was written before the primary set gained a sixth arm**                                                                                                                                                                                                                                                         |
| [`12-dataset-eda.md`](12-dataset-eda.md)                                   | The five apo-only descriptors, as standalone predictors, on all fourteen label sets. What a method has to beat                                                                                                                                                                                                                                                                                                             |
| [`22-dataset-eda-v2.md`](22-dataset-eda-v2.md)                             | **Supersedes `12`.** Seven apo-only descriptors on all fifteen label sets after the six-arm re-freeze, plus graph properties and label geometry. `cavity_volume` is the shortcut `12` missed, at median AUC 0.795                                                                                                                                                                                                          |
| [`11-synthesis.md`](11-synthesis.md)                                       | What must change, ranked, with the ADR each item needs. **Its first section is the disposition table: what has since been done**                                                                                                                                                                                                                                                                                           |
| [`13-correction-verification.md`](13-correction-verification.md)           | Independent verification of the corrections §2 of the synthesis proposes. **Two are refuted**, and one would have put a wrong number into a freeze                                                                                                                                                                                                                                                                         |
| [`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md)       | Clause (ii) read, target by target, for the 34 extension survivors. 13 pass, 5 fail, 16 unread behind publisher paywalls                                                                                                                                                                                                                                                                                                   |
| [`15-blocking-measurement-recheck.md`](15-blocking-measurement-recheck.md) | Independent re-derivation, from the deposited coordinates, of every number the five pending ADRs rest on. Three disagreements, none of which moves a conclusion; the four SH2 centroid distances in `01` §3.2 do not reproduce under any canonical lobe boundary                                                                                                                                                           |
| [`20-extension-closure.md`](20-extension-closure.md)                       | Second pass at the sixteen rows `14` left unread, plus every allostery/pocket resource beyond ASD. Four rows close (1 PASS, 3 FAIL), twelve remain; **still zero new admissible arms**. Read its §0.2 before quoting any reachability claim — it was measured without a shell and is weaker than `data/database-reachability.json`                                                                                         |
| [`19-cross-set-consistency-v2.md`](19-cross-set-consistency-v2.md)         | `10` re-run at the six-arm shape: all twelve clauses against all **fifteen** arms, both axes. Nine divergences, five recorded nowhere; `cardiac_myosin_mandated` is scored with no declared reporting role                                                                                                                                                                                                                 |
| [`21-protocol-v3-statistics.md`](21-protocol-v3-statistics.md)             | Statistical attack on protocol **version 3**: is the probit rescale FWER-controlled, is the calibration circular, is Fisher valid, what is the real power. FWER is controlled (measured 0.038-0.045 out of sample) and the midrank/AUC identity holds exactly. **`cavity_volume` no longer clears family 1 under v3 — 1 of 3 arms, not 3 of 3 — and it clears the tested form of negative class (b) at Fisher p = 0.0154** |
| [`16-adr-verification.md`](16-adr-verification.md)                         | The eight ADRs 0029-0036, audited against their own evidence and against the code. No ADR rests on a number that fails to reproduce; **0035 and 0036 are decided-but-unbuilt and write their Consequences as if built**, and ADR 0024 is orphaned by 0030 |
| [`17-definition-and-metrics-standard.md`](17-definition-and-metrics-standard.md) | Second, independent pass at the formal definition of an allosteric apo/holo pair and at the metrics the field recognises. **No single formal definition exists**: shells span 3.5-8 A and three published instruments disagree on what breaks apo-ness. The mean midrank is exactly AUC-ROC, and Amor 2016 is an in-domain precedent the repository already cites for something else |
| [`18-structure-evidence-refresh.md`](18-structure-evidence-refresh.md)     | Live RCSB re-fetch after the six-arm re-freeze, plus the deposited mmCIF for all nine accessions. **175 of 175 paired values agree with `08` — nothing drifted.** New: `5TBY`'s B column has no `refine` block behind it, and `9GZ2`'s mavacamten carries B = 0.00 on all 20 atoms |
| [`23-document-alignment.md`](23-document-alignment.md)                     | Every contradiction, broken reference, superseded statement, duplication and orphan left by the re-freeze. 34 / 18 / 15 / 10 / 10. Three different ADR counts, none of them 36 |
| [`24-conservation-measured.md`](24-conservation-measured.md)               | ADR 0035's fourth confounder column, **built and measured**. Conservation does not separate the labels from the background: median AUC 0.491 over eleven arms, Wilcoxon p = 0.76. The ADR's artifact-size blocker dissolves — 1.11 GB of alignments become a 172 KB pinned artifact |
| [`25-second-pass-synthesis.md`](25-second-pass-synthesis.md)               | **The second pass's ranked list.** Four blockers, and a verdict on every adversarial-model finding with the measurement that settles it |
| [`26-third-pass-synthesis.md`](26-third-pass-synthesis.md)                 | **The third pass's ranked list, and the current state.** It audits the second pass's repairs. Three C1 leaks (a `.joinpath` guard evasion, `docs/targets.md`, both benchmark READMEs), a frozen decision rule with no reader, and a cache key blind to the contact cutoff. All repaired. 16 frozen-layer items left open |

### `data/`

Machine-readable outputs, so no number in the prose above is only prose.

```
structure-evidence.json        RCSB metadata and validation for every entry
rcsb-raw/                      the raw API responses behind it
database-reachability.json     what answered, and when
extension-candidates-*.json    the candidate ledger from the 2026-09 sweep
decoy-power-sweep.json         nine detector settings x five primary arms
decoy-typeI.json               type-I rate of two candidate decoy tests
decoy_power_sim.py             the Monte-Carlo power calculation
clause-ix-both-sets.json       single-chain lining, measured on both sets
conservation/                  the jsd_conservation column, its 27 Pfam SHA-256s and its tools
rcsb-2026-09-refresh/          the 2026-09-02 evening re-fetch behind `18`
abl1-apo-survey.md             every ABL1 entry modelling more than the kinase domain
```

---

## How to read a finding here

The repository's evidence rules apply unchanged. A claim rests on a repository measurement, a
statistic with a stated null, or a citation with a DOI — in that order. Where evidence is
absent, the text says "unknown" rather than guessing.

Two extra rules apply to this directory, because it was written partly by delegated agents.

1. **A delegated claim is verified before it moves a freeze.** `07a` exists for that reason.
   A recommendation whose evidence is one agent's summary is marked as such and is not
   actionable until checked.
2. **Probe scripts are not experiments.** The measurements here ran outside
   `experiments/`, under `scratchpad/probe/`, because they test whether a change is worth
   making rather than producing a comparable number. Anything promoted to a decision moves
   into `experiments/` under the protocol in `docs/playbooks/experiment.md` first.
3. **A probe that opens a label set cannot be committed anywhere.**
   `tests/test_no_leakage.py` scans every tracked `.py`, `.sh`, `.ipynb` and `Makefile`
   outside `src/`, `tests/`, `data/` and `structures/`, and fails any file naming
   `frozen.json`. The gate is correct, so the repository has no home for a committed
   evaluation-side analysis script. Such a probe stays in the scratchpad and its source is
   reproduced verbatim in the prose. `12-dataset-eda.md` §9 is the worked example.
