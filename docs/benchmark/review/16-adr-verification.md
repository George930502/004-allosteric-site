# Verification of the eight ADRs written on 2026-09-02

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the required baselines are now
> `allo.scoring.baselines` -- eight of the nine, with `cavity_volume` in `allo.scoring.decoys`.

**Audited 2026-09-02**, read-only. Scope: `docs/adr/0029` to `docs/adr/0036` — the decisions
that came out of the audit in this directory, two of which moved a frozen layer. Each ADR was
checked on three questions: does the cited evidence say what the ADR says it says, does the
code and the freeze do what the ADR decided, and does it leave an earlier ADR standing whose
text is now false.

Every number below was re-derived in this session from the deposited files, the freezes or the
committed measurement data. Nothing was taken from a summary. Where a check needed a script it
was written outside the repository and its source is reproduced in §5.

---

## 0. Headline verdict

**No ADR in this batch rests on a number that fails to reproduce.** Every load-bearing
measurement re-derived exactly, including the four the recheck disputed — because ADR 0029
explicitly excludes them and rests on the convention-free interface counts instead.

**Three of the eight are sound and fully built:** 0029, 0030, 0034.
**Two are sound but carry an unbuilt promise inside an otherwise correct implementation:**
0031, 0033.
**One is half-built, and the contradiction it exists to close was moved rather than closed:** 0032.
**Two are decided-but-unbuilt, and both write their Consequences in the indicative as if the
work had happened:** 0035 and 0036.

**The single most serious finding is not inside any of the eight.** ADR 0030 re-freezes the
decoy detector off pyKVFinder's defaults. [ADR 0024](../../adr/0024-decoy-pockets-are-detector-defined.md)
is titled "Decoy pockets: **pyKVFinder at its defaults**", its Decision names the five default
values, and it is still listed `accepted` with no annotation. No 2026-09-02 ADR names it. That
is the one break in the supersession chain.

**The second most serious is a conformance claim that is not true.** ADR 0036 §Consequences
states "**All four minimum targets then have an arm.** The conformance gap the audit called
largest is closed." `1NKP` appears in no manifest and no freeze. The gap is open, and
`docs/report/substitutions.md` §1 — a submission-facing page — lists c-Myc under "What runs".

**Gate status.** `uv run pytest` passes, 136 tests. `uv run allo benchmark verify --set all`
exits 0. `uv run allo evaluate verify --detect` exits 0 at protocol version 3, fifteen arms,
777 decoy pockets. **`make check` exits 2**: five ruff `B905` errors, all in
`docs/benchmark/review/data/extract_refresh_2026_09.py`, which is untracked. `ruff check src
tests` is clean.

---

## 1. ADR 0029 — BCR-ABL1 uses chain B

**Sound. Fully built. Does not rest on a disputed number.**

### 1. Is the decision supported by the evidence it cites?

**Yes, and the evidence is the strongest in the batch** — every claim in the comparison table
was independently re-derived by a second reader who did not run the audit's code
([`15-blocking-measurement-recheck.md`](15-blocking-measurement-recheck.md) §0, rows A1–A11,
all `AGREES`): 16 of 20 labels contacted at 3.29 Å on chain A, nearest ligand 16.0 Å on chain
B, 3041 against 3 distinct polymer B-factor values, 20 of 20 against 17 of 20 labels modelled,
22.89 Å Cα RMSD, and `_refine.details` quoted verbatim.

**The disputed numbers are not used, and the ADR says so.**
`15-blocking-measurement-recheck.md` reports three disagreements. Two (B6/B7) belong to ADR 0031. The third is E3–E6, the four SH2-to-lobe centroid distances in
[`01-bcr-abl1-chain.md`](01-bcr-abl1-chain.md) §3.2, which reproduce under no canonical lobe
boundary. **ADR 0029 does not rest on them.** `0029:41-47` states this explicitly and pins the
argument to the interface residue counts instead, which are convention-free and reproduce
exactly (recheck E10/E11, 7 and 11 residues, identical lists). **The conclusion survives**: the
recheck confirms the inversion holds under every boundary from residue 320 to 355. E7 (32.66
against 32.51 Å) is not used either.

The "no myristate-free assembled ABL1 exists" finding is backed by a documented exhaustive
RCSB query with raw responses committed under `data/rcsb-abl1/`
([`data/abl1-apo-survey.md`](data/abl1-apo-survey.md) §1, eight retrieval steps including a
70 %-identity completeness search).

**One arithmetic note, against the survey and not the ADR.** `0029:55-56` reads "five for five
… two for two", which counts entries with `1OPL` on both sides of the split — correct against
the survey's own table, where five entries carry a myristoyl-pocket occupant (`1OPL`, `2FO0`,
`1OPK`, `5MO4`, `8SSN`) and two chains have it empty (`1OPL:B`, `4XEY:B`). The survey's own
headline at `data/abl1-apo-survey.md:11` says "**Four** have the pocket occupied", which does
not match its table. The ADR's reading is the right one.

### 2. Did the implementation match the decision?

**Yes, completely.** From `primary/frozen.json`, `bcr_abl1_mandated`: apo `1OPL` chain B,
`n_residues` 365, `n_candidates` 354, `label_residues` 17, `unmapped`
`['A:ILE521', 'A:VAL525', 'A:LEU529']`, `apo_site_occupancy.nearest_label_angstrom` 16.0,
`labels_contacted` 0. All four defects are in the machine-readable `defect` field of
`primary/manifest.yaml`, including the 22.89 Å with its 1.08 Å kinase-domain decomposition
beside it. The arm sits in `decision.supportive_only`; `bcr_abl1_corrected` (`2G2H:A`) is
unchanged and still in `decision.confirmatory_family`. `4XEY` was not substituted.

### 3. Does it contradict an earlier ADR it does not supersede?

**No ADR-level contradiction.** One document is now stale:
`docs/benchmark/primary/README.md:359` reads "`bcr_abl1_mandated` … is already the arm that
fails clause (iii)". Under 0029 that arm **passes** clause (iii) — 0029's own Consequences say
so — and it is `1OPL:A`, no longer a frozen arm, that fails it. §2's audit table
(`primary/README.md:201`) is correct as a record of the challenge's assignment but never says
which chain now runs.

---

## 2. ADR 0030 — negative class (b) by combination, detector re-frozen

**Sound. Fully built. The best-evidenced ADR in the batch. One unretired ADR behind it.**

### 1. Is the decision supported by the evidence it cites?

**Yes. Every number reproduces from committed data.**

| ADR claim                                                     | Source                                                         | Re-derived here                                                 |
| ------------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------- |
| `δ >= z_0.95 + z_0.80 = 2.487`                                | closed form                                                    | `2.486475` exact                                                |
| construction A type-I 0.000–0.032                             | `data/decoy-typeI.json`                                        | min 0.000, max 0.032 exact                                      |
| construction B type-I 0.132–0.384                             | `data/decoy-typeI.json`                                        | min 0.132, max 0.384 exact                                      |
| construction C not computable on KRAS                         | `data/decoy-power-sweep.json`                                  | KRAS decoy pool 23/25 residues over 3 pockets, none label-sized |
| v2 floors 0.25 / 0.10 / 0.024                                 | `data/decoy-power-sweep.json` `frozen` rows                    | 0.25 / 0.10 / 0.0238 exact                                      |
| `bcr_abl1_corrected` site coverage 0.6667                     | same                                                           | 0.6667 exact                                                    |
| `kras_g12c_corrected` reaches at most 18 decoys, floor 0.0526 | same                                                           | 18 decoys, 0.052632                                             |
| Fisher 0.0214 / Stouffer 0.0115 at v2                         | computed                                                       | 0.021562 / 0.011575                                             |
| Fisher 0.0014 / Stouffer 0.00045 at v3                        | `evaluation/frozen.json` floors 0.052632 / 0.031250 / 0.011765 | **0.001369 / 0.000453**                                         |

The v3 pair matches the exact frozen floors rather than the rounded ones printed in the ADR
table, which is the stronger reading. `harness.combine_arms`'s docstring quotes 0.00137 and
0.000453 — the exact values.

The re-frozen setting (`probe_out 8.0`, `removal_distance 1.2`, `volume_cutoff 1.0`) is the
`po 8 rd1.2 vol1` rung of the sweep, and it is the **maximum-`n_decoys` rung on all five arms
measured**. The ADR's claim that selection was on `n_decoys` is consistent. Worth recording
plainly: on this sweep `n_decoys` and site coverage co-move, so the two criteria are not
separable in the data — the ADR's "report site coverage as a consequence, never as the
selection target" is a discipline, not something the measurement can confirm independently.

### 2. Did the implementation match the decision?

**Yes.** `evaluation/manifest.yaml:15` `version: 3`; `:249-251` the three new detector values;
`:210-213` `decoy_pockets_combined` with `combine: fisher`, `also_reported: stouffer`;
`harness.py:412` `combine_arms` implements both, with `tests: "intersection null: no arm has
signal"` and the licensing sentence; `harness.py:376-381` marks the per-arm decoy test
`"confirmatory": False` with `"tested_form": "combine_arms over the confirmatory family"`.
Tested at `tests/test_scoring.py:650`. `evaluation/frozen.json` holds 15 arms and 777 decoy
pockets; `bcr_abl1_corrected` site coverage is now 0.9444. `evaluate verify --detect` exits 0.

### 3. Does it contradict an earlier ADR it does not supersede?

**Yes — this is the batch's one supersession-chain break.**
[ADR 0024](../../adr/0024-decoy-pockets-are-detector-defined.md) is titled "Decoy pockets:
pyKVFinder **at its defaults**, zero halo, power floor disclosed", `0024:16` names
`probe_out 4.0 Å, removal_distance 2.4 Å, volume_cutoff 5.0 Å³`, and its Decision reads
"Choosing the defaults is the choice not to tune a detector on the benchmark it will score."
ADR 0030 replaces all three values. Its per-arm consequence table (0.25 / 0.25 / 0.040 / 0.10 /
0.024 over five arms) is also stale against the frozen 0.0714 / 0.0526 / 0.0217 / 0.0312 /
0.0118 over six.

**ADR 0030 does not mention ADR 0024 anywhere.** Neither does any other ADR written on
2026-09-02, and `docs/adr/README.md` still lists 0024 as plain `accepted`. Nothing in
`docs/benchmark/evaluation/` references it either.

---

## 3. ADR 0031 — expose `5TBY` as a reported arm

**Evidence sound and re-derived exactly. Built in the freeze. Two of its own printing and
pinning promises are unbuilt.**

### 1. Is the decision supported by the evidence it cites?

**Yes. I re-derived the source-rule evidence from the deposited coordinates and it is exact.**

| ADR claim                                                 | Re-derived                                                                             |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| PS00016 matches **twice** in MYH7                         | `5TBY:A` 2 matches, spans 61–68 and 178–185; `9GZ3:A` identical                        |
| PS00016 matches once in KRAS                              | `4OBE:A` and `4LDJ:A`, 1 match, span 10–17                                             |
| motif triple matches once each in MYH7, zero in KRAS/ABL1 | 1/1/1 on `5TBY:A`, `9GZ3:A`, `9GZ2:A`; 0/0/0 on `4OBE:A`, `1OPL:A`, `1OPL:B`, `2G2H:A` |
| Jaccard 0.483 on `9GZ3:A`, 0.516 on `9GZ2:A`              | **0.4828** and **0.5161**                                                              |
| centroid offset 5.96 Å and 5.92 Å                         | **5.96** and **5.92**                                                                  |
| overlap 14 of 21/22 and 16 of 25/22                       | exact                                                                                  |

The label transfer (12 mavacamten contacts, none unmapped) is confirmed independently by
recheck rows C1–C3, and the frozen `label_residues` for `cardiac_myosin_mandated` are the same
twelve as `cardiac_myosin_corrected`. The contact-topology numbers (Jaccard 0.471, recall
0.569, edges 1103/1419/807, mean degree 8.48/9.53, degree Spearman 0.741) are all `AGREES` in
the recheck.

**The two disputed numbers belong here, and the ADR handles them correctly.** Recheck B6/B7:
pairwise Cα Spearman 0.9724 against 0.9742, and median absolute distance difference 2.08 Å
against 1.95 Å. `0031:71-76` names the disagreement, records that the cause was not isolated,
and instructs "**Quote the range rather than either endpoint**." The decision does not rest on
either value.

### 2. Did the implementation match the decision?

**Mostly. Three gaps.**

Built: `cardiac_myosin_mandated` is frozen (954 nodes, 932 candidates, 12 labels, 0 unmapped);
`status: excluded` and `prediction_status: blocked` are gone from the manifest entirely;
`MYO_PLOOP` / `MYO_SWITCH1` / `MYO_SWITCH2` are in `CATALYTIC_MOTIFS` (`inputs.py:100-102`)
and the frozen `active_site` `[178–185, 238–245, 461–466]` re-derives from them exactly;
`tests/test_scoring.py:124` pins `(7, 4, 1)` against `(8, 4)`; `docs/report/substitutions.md`
exists.

- **Gap A — the promised test does not exist.** `0031:115`: "A test pins the validation
  numbers, so a later change to the motif set fails the suite rather than moving a source
  silently." No test in `tests/` names `MYO_PLOOP`, the Jaccard values or the offsets; they
  live only in a code comment at `src/allo/inputs.py:97-98`. The motif _spans_ are pinned
  indirectly, because `benchmark verify` re-derives `active_site` from them.
- **Gap B — half of the mandatory print is not machine-readable.** `0031:96`: "Print with it,
  always: source Jaccard 0.48–0.52 … with a 5.9 Å centroid offset, and long-range contact
  Jaccard 0.471." The `defect` field of `primary/manifest.yaml` carries the **contact** Jaccard
  and not the **source** Jaccard. The source numbers appear only in a YAML comment
  (`primary/manifest.yaml:448`), which `allo.inputs.load()` never reads and no report path
  emits.
- **Gap C — the defect string quotes a point value the ADR told it not to.** It prints
  "Spearman 0.9724" where 0031 says quote the range 0.9724–0.9742.

**One measured defect the ADR does not name.** `cardiac_myosin_mandated.apo_holo_rmsd.core` is
**6.82 Å over 749 residues**, against 1.18 Å over 752 on `cardiac_myosin_corrected` — the same
holo, the same twelve labels. ADR 0031 declares "both defects" (source rule, contact graph) and
this is a third, sitting inside the freeze unremarked.

### 3. Does it contradict an earlier ADR it does not supersede?

**No.** ADR 0016 is correctly marked superseded, carries a header note saying what became false
and what survives as a disclosure, and is indexed as such. 0031 addresses 0016's "no
myosin-only motif" prohibition head-on by showing every existing entry in `CATALYTIC_MOTIFS` is
a family motif. ADR 0005's derived-rule requirement is satisfied — the source is a regex over
the apo sequence, not a written residue list.

---

## 4. ADR 0032 — the claim threshold is its own confirmatory family

**Evidence sound. Declaration built in the manifest, and NOT built in the protocol README —
so the contradiction the ADR exists to close was moved, not closed.**

### 1. Is the decision supported by the evidence it cites?

**Yes.** "`cavity_volume` rejects on all three confirmatory arms" is a repository experiment
with a stated null: `experiments/REGISTRY.md:163`, `p_calibrated` 0.0073 / 0.0003 / 0.0001,
AUC-ROC 0.830 / 0.795 / 0.977, each below its Holm threshold. The non-redundancy measurement
(DCC 26.5 Å against a chance line of 17.7 Å on `bcr_abl1_corrected`, recall@5 0.00 on every
arm) is at `evaluation/README.md:1019` and `ADR 0025:149`.

**One qualification.** Both were measured under protocol **version 2**
(`evaluation/README.md:1006`, "All five passed on 2026-08-25 under protocol version 2"). They
have not been re-run at v3. That is defensible — `evaluation/README.md` §0.1 records that the
three confirmatory arms' `size_ratio` and `alpha_star` reproduce bit-for-bit and only the two
`mandated` arms moved — but the ADR asserts the v2 result as current without saying so.

### 2. Did the implementation match the decision?

**Half.** `evaluation/manifest.yaml:289-298` declares `decision.claim_family` with the test,
the reference, the three arms, Holm and two-sided. `evaluation/README.md:52` (§0, change 4)
declares it in prose.

- **Defect — `evaluation/README.md` §8 is unchanged.** `:773` still opens "**One confirmatory
  family**, declared before any method exists", and `:788` still reads "**Everything else is
  descriptive.** … None is FWER-protected, and none is a confirmatory decision." The claim
  family is not named in §8 at all, and neither is `decoy_pockets_combined`. §0 says two
  families; §8 says one. AGENTS.md sends every reader to this file for "how a score is
  computed". The internal contradiction ADR 0032 was written to close now sits between §0 and
  §8 of the same frozen document.
- **Defect — nothing enforces the declaration.** No module reads `decision.claim_family`;
  `holm()` (`harness.py:480`) is wired to neither family. The only test on the block is
  `tests/test_scoring.py:320`, named
  `test_protocol_declares_one_confirmatory_family_of_three`, which asserts family 1 only and
  passes unchanged. Deleting `claim_family` from the manifest breaks no test.

### 3. Does it contradict an earlier ADR it does not supersede?

**It amends ADR 0025 and 0025 does not say so.** `0032` header reads "amends ADR 0025"; ADR
0025 carries no reciprocal note and `docs/adr/README.md` lists it as plain `accepted`. 0025's
text is not falsified — the claim threshold it set is preserved — so this is a cross-reference
gap, not a false statement.

---

## 5. ADR 0033 — "uniformly stripped" scopes the node set

**The decisive measurement reproduces exactly. One consequence is factually false. One
promised test does not exist.**

### 1. Is the decision supported by the evidence it cites?

**Yes, including the measurement that changed the design.** ADR 0033's turning point is that
residue 10 is a scoreable KRAS label and not a source residue, so a motif-only source is not a
drop-in substitution. Re-derived from `primary/frozen.json`: `kras_g12c_corrected`
`scoreable_label_residues` begins `[9, 10, 58, …]`, and `active_site` is
`[11, 12, 13, 14, 15, 16, 17, 18, 28, 30, 32, 33, 34, 36, 57, 116, 117, 119, 120, 145, 146,
147]` — residue 10 is absent. Exact.

The PS00016 uniqueness claim also re-derives exactly: one match at 10–17 on `4OBE:A` and on
`4LDJ:A`. The 7-against-7 ligand/motif split matches both manifests.

### 2. Did the implementation match the decision?

**Partly.**

- Built: `PLOOP` is in `CATALYTIC_MOTIFS` (`inputs.py:92`) with the PROSITE line and the
  uniqueness note; no freeze moved on account of this ADR; the descriptive comparison is
  correctly deferred to Phase 2 and has not run.
- **Defect — `0033:89-90` states "`primary/frozen.json` and `evaluation/frozen.json` keep
  **fourteen** arms."** They hold **six** and **fifteen**. The statement was already false on
  the day it was written, because ADR 0031 added `cardiac_myosin_mandated` the same day.
- **Gap — `0033:91-92` promises PS00016's "uniqueness on both KRAS apo entries pinned by a
  test."** No such test exists. `PLOOP` is named by no frozen arm, so `benchmark verify` does
  not exercise it either; `active_site()` only raises on a non-unique match when a rule
  actually invokes the motif. The regex can be changed and the whole suite still passes.

### 3. Does it contradict an earlier ADR it does not supersede?

**No.** The narrow reading is consistent with ADR 0005 (source derived from the apo entry) and
with C1, and 0033 argues the C1 point explicitly.

---

## 6. ADR 0034 — the review directory is a protected answer key

**Sound and fully built. Three stated facts about the tree are stale or wrong.**

### 1. Is the decision supported by the evidence it cites?

**Yes.** The premise is C1's own wording ("not even the residue count") plus the existing
precedent of `secondary/evidence/extension-candidates.md`. The claim that the one-line fix
fails, with the five paths it flags, is reproducible from the guard's own resolution of
`Path(__file__).resolve().parent`.

### 2. Did the implementation match the decision?

**Yes, and this is the cleanest implementation of the eight.**
`tests/test_no_leakage.py:65` adds `docs/benchmark/review` to `PROTECTED_PATHS`; `:78`
`REVIEW_TOOLS`; `:843` the exemption predicate — tracked inside the tree **and** importing
nothing from `allo` — as a rule, not a name list; `:928`
`test_every_review_tool_imports_no_package_module` and `:948`
`test_the_review_exemption_stops_at_the_review_tree`. The full suite passes.

Three stated facts do not hold:

- **`0034:58-60`: "Both current tools — `fetch_structure_evidence.py` and `decoy_power_sim.py`
  — use the standard library only."** `decoy_power_sim.py:15` imports `numpy`, which is not the
  standard library. The **rule** the exemption rests on ("imports nothing from `allo`") is
  unaffected and is what the test checks, so the guard is correct; the sentence justifying it
  is false.
- **The census is stale.** The tree now holds four `.py` tools, not two:
  `extract_refresh_2026_09.py` (imports `Bio`) and `fetch_refresh_2026_09.py` are present and
  **untracked**, so condition 1 of the exemption does not even reach them.
  `extract_refresh_2026_09.py` is what turns `make check` red.
- **`0034:68-69`: "`CLAUDE.md` and `data/README.md` gain the seventh route."** `CLAUDE.md`
  did. `data/README.md` does not name `docs/benchmark/review/` as a protected route anywhere —
  and it cites `docs/benchmark/review/data/extension-candidates-2026-09.json` by path without
  noting that the file is now protected.

### 3. Does it contradict an earlier ADR it does not supersede?

**No.** It extends the same protected-by-default rule the evaluation directory already had, and
it explicitly does not widen `ALLOWED_PREDICTION_PATHS`.

---

## 7. ADR 0035 — conservation is the fourth confounder column

**Evidence sound. DECIDED-BUT-UNBUILT — and the ADR states the unbuilt work in the indicative.**

### 1. Is the decision supported by the evidence it cites?

**Yes, and the evidence file carries verification tags.**
[`../evidence/conservation-confounder.md`](../evidence/conservation-confounder.md) holds
Cimermancic's `P = 3.4 × 10⁻⁶⁷` at `:61` marked `[VERIFIED-FULLTEXT]`; Leander's "surprisingly
poorly conserved" verbatim at `:64` marked `[VERIFIED-ABSTRACT]`; Capra & Singh's AUC₁ 0.9440
against Shannon's 0.9235 at `:187`; the ConSurf-DB `ECONNREFUSED 132.66.243.136:443` on three
paths at `:260`; Pfam 38.2 with `Pfam-A.full.gz` at 22 GB at `:256`. The CryptoSite "AUC = 0.74"
misquote is documented with the full source sentence at `:118`, which is exactly the kind of
number R3 exists to catch.

The coevolution rejection is argued as a category error rather than as absent evidence, and it
names the counter-evidence (Teşileanu 2015, Chi 2008) rather than asserting a conclusion.

### 2. Did the implementation match the decision?

**No. The column is not built.**

- `src/allo/scoring/harness.py:391` writes `record["confounders"]["conservation"] = None`.
- `allo.structure.properties` has no conservation column. `0035:89` says it "gains the column".
- No Pfam alignment is committed anywhere (`git ls-files | grep -i pfam` returns zero).
  `0035:92` says "The mirrored alignments **are** committed, one gzipped Stockholm file per
  Pfam family."
- `0035:87` says "`evaluation/manifest.yaml` §11 **names** `jsd_conservation`". It does not —
  the key is `conservation` with `source: unknown`. Its `note` does carry the full
  parameterisation, the disabled window, Pfam 38.2, the PF07714 size blocker, and the sentence
  "**The METHOD is decided and the COLUMN is not built**", which is the honest statement the
  ADR itself omits.

`11-synthesis.md` labels this "decided, not built". The ADR does not, and its Consequences read
as a description of finished work.

**Related staleness in the same section.** `evaluation/README.md:896` says "**Four** confounder
columns print beside every result" and `:908` says conservation is absent "until **Phase 3** can
fetch an alignment" — no mention of ADR 0035 or of the method it decided. §11 also does not
mention `degree` or `distance_to_source`, which `harness.py:394-401` now computes at v3 and the
manifest declares, so `score_arm` writes six confounder entries where §11 describes four.

### 3. Does it contradict an earlier ADR it does not supersede?

**No.** It fills a `null` ADR 0025 left and keeps the column on the apo-only side, so C1 and C2
are untouched. The placement argument (keep it in `allo.structure.properties`, outside
`allo/scoring/`) is consistent with the parent-package rule in AGENTS.md.

---

## 8. ADR 0036 — c-Myc is a reported deliverable

**Evidence sound and independently verified from the deposited file. DECIDED-BUT-UNBUILT, and
its central conformance claim is not true today.**

### 1. Is the decision supported by the evidence it cites?

**Yes. I fetched `1NKP.cif` from RCSB and checked every structural claim.**

`_struct_ref_seq`, verbatim from the deposited file:

```
1 1 1NKP A 4 ? 85 ? P01106 353 ? 434 ? 900 981
2 1 1NKP D 4 ? 85 ? P01106 353 ? 434 ? 500 581
```

- Offset `chain A auth = lit439 + 547`: `900 − 353 = 547` and `981 − 434 = 547`. **Exact.**
- Chain D offset 147: `500 − 353 = 147`. **Exact.**
- Chain A polymer range auth **897–984**, 88 residues, entity positions 1–88 complete. Chain D
  **499–581**, 83 residues, entity 3–85. **Exact.**
- Entity 2 sequence `GHMNVKRRTHNVLERQRRNELKRSFFALRDQIPELENNEKAPKVVILKKATAYILSVQAEEQKLISEEDLLRKRREQLKHKLEQLGGC`,
  88 aa; native content entity 4–85 = **82 residues**. **Exact.**
- **The identifier-space collision is real.** `label_asym_id` `A`, `B`, `C`, `D` are the four
  DNA strands (entity 1); c-Myc is auth `A`/`D` = label `E`/`G` (entity 2); Max is auth `B`/`E`
  = label `F`/`H` (entity 3). **Exact.**
- Space group `P 1`, resolution 1.80 Å, and the only non-polymer component in the entry is
  `HOH`. **Exact**, and consistent with "no deposited structure shows a drug-like small
  molecule bound to human c-Myc".
- Site arithmetic under +547: 402→949, 409→956, 366→913, 375→922, 385→932. **Consistent.**

The ADR's own correction — that an earlier draft wrote the UniProt span as 368–449, the
454-residue Myc-1 convention — is right, and the deposited file settles it against 353–434.
`../evidence/cmyc-contract.md:95` still prints "auth 900–981 ↔ P01106 **368–449**" unqualified
in its §1.3 table, though the file reconciles the three conventions thirty lines later at
`:139`. That is a defect in the evidence file, not in the ADR.

### 2. Did the implementation match the decision?

**No. Nothing was built.**

- `1NKP` appears in **none** of `primary/manifest.yaml`, `primary/frozen.json`,
  `evaluation/manifest.yaml`, `evaluation/frozen.json`. `primary/frozen.json` holds six
  targets, all KRAS / BCR-ABL1 / cardiac myosin.
- The structure is in neither `structures/` nor `data/raw/eval/`.
- `0036:101` states "`1NKP` **enters** `primary/manifest.yaml` as a c-Myc arm."
- **`0036:105-106` states "All four minimum targets then have an arm. The conformance gap the
  audit called largest is closed."** It is not closed. `11-synthesis.md` §5 names this gap and
  the disposition table above it claims ADR 0036 settled it.
- `allo.quantum.connectivity` (decision 4) does exist, so the source-free scorer the ADR names
  is available.

**This propagates into a submission-facing page.** `docs/report/substitutions.md:28` lists, in
a table headed "**What runs**", the row `c-Myc | 1NKP | — | 1NKP:A, no holo member | no`.
Nothing runs.

### 3. Does it contradict an earlier ADR it does not supersede?

**Yes, one.** [ADR 0007](../../adr/0007-ground-truth-is-the-allosteric-site.md) Decision clause
1: "**The ground-truth concept is the allosteric site.** A pair earns its place by the holo
member containing an effector at a site that is functionally coupled to the active site,
evidenced by cited experiment. **Nothing else is an entry criterion.**"

ADR 0036 admits an arm with no holo member, no effector, no active site, and — in its own
words at `0036:47` — three sites that are "interface disruption, not a topographically distinct
site conformationally linked to a functional site". 0036 neither names nor amends 0007. The
mitigation is real and stated (descriptive, never confirmatory, outside `score_arm`, outside
every Holm family, declared non-blind), but ADR 0007's "nothing else is an entry criterion" is
now false and no later ADR retires it.

[ADR 0017](../../adr/0017-normative-pair-definition-and-comparator-blindness.md) is a second,
weaker case: it makes `primary/README.md` the normative pair definition and says "Changing any
normative clause now requires amending this ADR". A member with no pair is outside that
definition rather than a change to it, but the relationship is unstated. This becomes live the
moment `1NKP` enters the manifest.

ADR 0022 (mean midrank) and ADR 0011 (candidate set) are not contradicted, because the c-Myc
statistic is declared descriptive and outside `score_arm`.

---

## 9. Ranked defects

Severity: **A** blocks or falsifies a stated result; **B** a decision is recorded as done and
is not; **C** a stated fact is wrong but nothing downstream depends on it.

| #   | Sev   | Where                                                                         | The claim                                                                                                                        | The contradicting evidence                                                                                                                                                                     | The one check that settles it                               |
| --- | ----- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1   | **A** | `docs/adr/0024-decoy-pockets-are-detector-defined.md:16` (title and Decision) | "pyKVFinder 0.9.3 at its published defaults — probe_out 4.0, removal_distance 2.4, volume_cutoff 5.0"; status `accepted`         | `evaluation/manifest.yaml:249-251` freezes 8.0 / 1.2 / 1.0 under ADR 0030. No ADR names 0024; `docs/adr/README.md` lists it unannotated                                                        | `grep -rn "0024" docs/adr/003*.md` returns nothing          |
| 2   | **A** | `docs/adr/0036:105`                                                           | "All four minimum targets then have an arm. The conformance gap the audit called largest is closed"                              | `grep -rn 1NKP docs/benchmark/*/manifest.yaml docs/benchmark/*/frozen.json` returns nothing; `primary/frozen.json` holds six targets, no c-Myc                                                 | that grep                                                   |
| 3   | **A** | `docs/report/substitutions.md:28`                                             | c-Myc row under the heading "What runs": "`1NKP`:A, no holo member"                                                              | no c-Myc arm exists in any freeze                                                                                                                                                              | same grep                                                   |
| 4   | **A** | `docs/benchmark/evaluation/README.md:773` and `:788`                          | "**One confirmatory family**, declared before any method exists" and "Everything else is descriptive … none is FWER-protected"   | `evaluation/manifest.yaml:289` declares `decision.claim_family`; `README.md:52` (§0 row 4) declares two families. §0 and §8 of the same frozen document disagree                               | read §8 against §0                                          |
| 5   | **B** | `docs/adr/0035:87,89,92`                                                      | "manifest §11 names `jsd_conservation`"; "`allo.structure.properties` gains the column"; "The mirrored alignments are committed" | `harness.py:391` writes `None`; no `jsd` symbol in `src/`; `git ls-files \| grep -i pfam` = 0; manifest key is `conservation`, `source: unknown`                                               | `grep -rn conservation src/allo/`                           |
| 6   | **B** | `docs/adr/0031:115`                                                           | "A test pins the validation numbers" (Jaccard 0.483/0.516, offsets 5.96/5.92)                                                    | no test in `tests/` names `MYO_PLOOP` or any of those values; they exist only in the comment at `src/allo/inputs.py:97-98`                                                                     | `grep -rn "MYO_PLOOP\|0.483" tests/`                        |
| 7   | **B** | `docs/adr/0033:91`                                                            | PS00016's "uniqueness on both KRAS apo entries pinned by a test"                                                                 | no test names `PLOOP`; no frozen arm uses it, so `benchmark verify` never exercises it either                                                                                                  | `grep -rn PLOOP tests/ docs/benchmark/*/manifest.yaml`      |
| 8   | **B** | `docs/adr/0031:96`                                                            | "Print with it, always: source Jaccard 0.48–0.52 … and long-range contact Jaccard 0.471"                                         | the manifest `defect` field carries only the contact Jaccard; the source numbers are in a YAML **comment** at `primary/manifest.yaml:448`, which `allo.inputs.load()` never reads              | read the `defect` string via `read_manifest()`              |
| 9   | **B** | `docs/adr/0032` implementation                                                | a second confirmatory family is declared and load-bearing                                                                        | no module reads `decision.claim_family`; the only test on the block is `tests/test_scoring.py:320` `test_protocol_declares_one_confirmatory_family_of_three`, which checks family 1 and passes | delete `claim_family` from the manifest and run `pytest`    |
| 10  | **B** | `Makefile` gate                                                               | "Run `make check` before reporting any task complete" (AGENTS.md)                                                                | `make check` exits 2 on five ruff `B905` errors in the **untracked** `docs/benchmark/review/data/extract_refresh_2026_09.py`. `ruff check src tests` is clean; `pytest` is green               | `make check; echo $?`                                       |
| 11  | **C** | `docs/adr/0033:90`                                                            | "`primary/frozen.json` and `evaluation/frozen.json` keep **fourteen** arms"                                                      | they hold **six** and **fifteen**; ADR 0031 added the sixth primary arm the same day                                                                                                           | count `targets` in both files                               |
| 12  | **C** | `docs/adr/0034:58`                                                            | "Both current tools … use the **standard library only**"                                                                         | `decoy_power_sim.py:15` imports `numpy`. Also four `.py` tools now exist, two untracked. The exemption _rule_ ("imports nothing from `allo`") is correct and is what the test checks           | `head -20 docs/benchmark/review/data/*.py`                  |
| 13  | **C** | `docs/adr/0034:68`                                                            | "`CLAUDE.md` and `data/README.md` gain the seventh route"                                                                        | `data/README.md` names no route list and never mentions `docs/benchmark/review/` as protected, while citing a file inside it by path                                                           | `grep -n review data/README.md`                             |
| 14  | **C** | `docs/benchmark/primary/README.md:359`                                        | "`bcr_abl1_mandated` … is already the arm that fails clause (iii)"                                                               | ADR 0029's Consequences: "The arm now **satisfies** clause (iii), which no BCR-ABL1 mandated arm did before". `frozen.json` gives `labels_contacted: 0`, nearest ligand 16.0 Å                 | read the frozen `apo_site_occupancy`                        |
| 15  | **C** | `docs/benchmark/evaluation/README.md:896,908`                                 | "Four confounder columns print beside every result"; conservation absent "until Phase 3"                                         | `harness.py:385-401` writes six entries (three properties, `conservation: None`, `degree`, `distance_to_source`); the method is decided by ADR 0035, not deferred to Phase 3                   | read the `record["confounders"]` block                      |
| 16  | **C** | `docs/adr/0031` Consequences                                                  | "both measured defects" printed beside the arm                                                                                   | a third sits in the freeze unremarked: `cardiac_myosin_mandated.apo_holo_rmsd.core` = **6.82 Å** over 749 residues, against 1.18 Å on `cardiac_myosin_corrected` — same holo, same labels      | read `apo_holo_rmsd` for both myosin arms                   |
| 17  | **C** | `docs/benchmark/review/data/abl1-apo-survey.md:11`                            | "**Four** have the pocket occupied"                                                                                              | its own table at `:88-95` lists five entries with a myristoyl-pocket occupant. ADR 0029's "five for five" matches the table; the survey headline does not                                      | count the occupancy column                                  |
| 18  | **C** | `docs/adr/README.md:17` and `AGENTS.md:110`                                   | "Thirty-three decisions" / "indexes all **33** by topic"                                                                         | 36 ADR files exist and the README table has 36 rows                                                                                                                                            | `ls docs/adr/0*.md \| wc -l`                                |
| 19  | **C** | `../evidence/cmyc-contract.md:95`                                             | "auth 900–981 ↔ P01106 **368–449**", unqualified, in the §1.3 table                                                              | the deposited `_struct_ref_seq` gives `A 4–85 ↔ P01106 353–434`. The file reconciles the conventions at `:139`; the table does not                                                             | `grep -A2 _struct_ref_seq.pdbx_auth_seq_align_end 1NKP.cif` |
| 20  | **C** | `docs/adr/0032` evidence                                                      | "`cavity_volume` rejects on all three confirmatory arms" asserted as current                                                     | measured under protocol v2 (`evaluation/README.md:1006`). Defensible — §0.1 shows those three arms' calibration is unchanged bit-for-bit — but not re-run at v3 and not qualified              | re-score `cavity_volume` through `score_arm` at v3          |

**Not defects, recorded because they were checked.** ADR 0029 does **not** rest on the four
disputed SH2 centroid distances and says so at `0029:41-47`; its conclusion survives on the
interface counts, which reproduce exactly. ADR 0031's two disputed values (Spearman
0.9724/0.9742, median 2.08/1.95 Å) are named as disputed in the ADR and are not load-bearing.
Every arithmetic claim in ADR 0030 reproduces to the digits printed. Every structural claim in
ADR 0036 reproduces from the deposited `1NKP` file. `benchmark verify --set all` and
`evaluate verify --detect` both exit 0, and `pytest` passes 136 tests.

---

## 10. Reproduction

The motif checks were run from a script outside the repository, because a tracked file naming
`frozen.json` fails `tests/test_no_leakage.py`. Source, verbatim:

```python
"""Re-derive the motif claims ADR 0031 and ADR 0033 rest on. Read-only."""

import re, sys, numpy as np

sys.path.insert(0, "src")
from allo.inputs import CATALYTIC_MOTIFS, one_letter, contacts


def load(pdb, sub):
    import gzip, pathlib
    from allo.structure.pdb import parse_mmcif_text

    p = pathlib.Path("structures") / sub / f"{pdb}.cif.gz"
    return parse_mmcif_text(gzip.decompress(p.read_bytes()).decode(), pdb)


def seq(st, ch):
    res = [r for r in st.residues() if r[0] == ch]
    return res, one_letter(res)


def spans(st, ch, motif):
    res, s = seq(st, ch)
    return [
        [res[i][1] for i in range(m.start(), m.end())]
        for m in re.finditer(CATALYTIC_MOTIFS[motif], s)
    ]


for pdb, sub, ch in [
    ("4OBE", "apo", "A"),
    ("4LDJ", "apo", "A"),
    ("5TBY", "apo", "A"),
    ("1OPL", "apo", "A"),
    ("1OPL", "apo", "B"),
    ("2G2H", "apo", "A"),
    ("9GZ3", "apo", "A"),
]:
    sp = spans(load(pdb, sub), ch, "PLOOP")
    print(f"{pdb}:{ch} PLOOP n={len(sp)} spans={[(x[0], x[-1]) for x in sp]}")

for pdb, sub, ch in [
    ("5TBY", "apo", "A"),
    ("9GZ3", "apo", "A"),
    ("9GZ2", "holo", "A"),
    ("4OBE", "apo", "A"),
    ("1OPL", "apo", "A"),
    ("1OPL", "apo", "B"),
    ("2G2H", "apo", "A"),
]:
    st = load(pdb, sub)
    print(pdb, ch, {m: len(spans(st, ch, m)) for m in ("MYO_PLOOP", "MYO_SWITCH1", "MYO_SWITCH2")})

CUT = 4.5
for pdb, sub, ligs in [
    ("9GZ3", "apo", ["ADP", "MG", "PO4"]),
    ("9GZ2", "holo", ["ADP", "MG", "PO4"]),
]:
    st, ch = load(pdb, sub), "A"
    motif = sorted(
        n
        for m in ("MYO_PLOOP", "MYO_SWITCH1", "MYO_SWITCH2")
        for sp in spans(st, ch, m)
        for n in sp
    )
    src = st.ligand & np.isin(st.resname, ligs) & (st.chain == ch)
    tgt = st.protein & (st.chain == ch)
    lig = sorted({n for _, n, _ in contacts(st, src, tgt, CUT)})
    a, b = set(lig), set(motif)
    ca = {
        int(st.seq_id[i]): st.coord[i]
        for i in range(len(st.resname))
        if st.protein[i] and st.chain[i] == ch and st.atom[i] == "CA"
    }
    c1 = np.mean([ca[r] for r in lig if r in ca], axis=0)
    c2 = np.mean([ca[r] for r in motif if r in ca], axis=0)
    print(
        f"{pdb}:{ch} ligand={len(a)} motif={len(b)} overlap={len(a & b)} "
        f"jaccard={len(a & b) / len(a | b):.4f} offset={np.linalg.norm(c1 - c2):.2f}"
    )
```

The Fisher and Stouffer floors were recomputed as
`chi2.sf(-2 * np.log(p).sum(), 2 * len(p))` and
`norm.sf(norm.isf(p).sum() / np.sqrt(len(p)))` over the `minimum_attainable_p` values read
from `docs/benchmark/evaluation/frozen.json`.

`1NKP.cif` was fetched from `https://files.rcsb.org/download/1NKP.cif` into the scratchpad and
read with `Bio.PDB.MMCIF2Dict`. It is **not** committed, and no structure was added to the
repository.
