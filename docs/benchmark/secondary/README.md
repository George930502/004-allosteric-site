# Secondary benchmark — the generalisability and scalability set

`CHALLENGE.md` §6 asks participants to "test robustness on additional targets of their
choice to demonstrate **generalizability and scalability**". This set is that. It froze on
2026-08-24, alongside the primary set and through the same code.

**Read `docs/benchmark/primary/README.md` first.**

> **Read [`../review/README.md`](../review/README.md) before quoting a number from this page.**
> An audit closed on 2026-09-02, after the organisers answered four questions about the
> benchmark. It ratifies most of this document, corrects two stated facts in it, and lists the
> decisions it forces. Corrections are recorded there rather than edited in here, so that this
> freeze stays a freeze. Clauses (i)–(viii), the authority behind each of
them, and the freeze mechanics are all there and all bind this set unchanged. Only what
**differs** is explained here.

| Artifact                                                     | What it is                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------------ |
| `manifest.yaml`                                              | the choices. Hand-edited                                           |
| `frozen.json`                                                | their consequences, re-derived from the deposited files. Generated |
| `selection.json`                                             | every candidate considered and the clause that decided it          |
| `evidence/databases.md`                                      | why the frame is RCSB and not the Allosteric Database              |
| `../../adr/0021-secondary-benchmark-is-two-disjoint-sets.md` | the decision this set implements                                   |

Verify it with `uv run allo benchmark verify --set secondary`, or `--set all` for both.

---

## 1. Why this set exists, in one number

Three targets cannot make a **generalisation** claim. A sign test over N target-level effects
has a minimum attainable one-sided p of 2⁻ᴺ, because its null distribution has 2ᴺ atoms. At
N = 3 that is 0.125, so the primary benchmark's claim-bearing arms are not merely underpowered
for a statement about the method in general — they are **unable to make one** at α = 0.05,
whatever the result. N ≥ 5 is the floor. This set delivers 9 targets, split 4 and 5.

**Narrowed 2026-08-24.** This section used to add "no analysis rescues it", and that sentence
was too strong. The 2⁻ᴺ floor binds tests **invariant to sign flips of the N effects**. Two
constructions escape it, and each licenses something different: a binomial count against
π₀ = α rather than ½ (three arms can then reject, but only license "the population success rate
exceeds 5 %"), and Fisher or Stouffer combination of the per-arm permutation p-values, which is
unbounded below but tests the **intersection null** and so licenses "at least one arm has
signal" — not generalisation. Full statement: `../evaluation/README.md` §8.
The reason this set exists is unchanged; the primary set simply has a claim available to it
that the old wording denied.

---

## 2. Two tiers, one freeze

| Tier             | N   | Purpose                                                  | When it may be looked at                |
| ---------------- | --- | -------------------------------------------------------- | --------------------------------------- |
| `development`    | 4   | every hyperparameter: metric, Hamiltonian, cutoff, ratio | Phase 2 onward. Burned by construction  |
| `generalisation` | 5   | the generalisability and scalability claims              | Phase 5, **after the method is frozen** |

Both tiers froze at the same moment, from one manifest, through the same `derive()` the
primary set uses. That is what makes a number from one comparable with a number from the
other. They are **looked at** at different times, and that is what makes the second tier
worth anything. ADR 0012 already said the tuning set is "burned by construction"; this set
does not repeat that mistake, it separates the two jobs.

Tier assignment is a **seeded, size-stratified split**, not a judgement. Targets are
ordered by `n_residues`, consecutive pairs are the strata, and `random.Random(0)` decides
which member of each pair is held out. An odd target always joins `generalisation`, because
that tier carries a hypothesis test and `development` only tunes.

Nobody chose which targets carry the claim, so nobody could put the easy ones there.
`allo.benchmark.size_stratified_split` reproduces the assignment from the frozen residue
counts, and `tests/test_secondary.py` fails if the recorded tiers are not what it returns.

**A word of warning about the field name.** Both freezes carry a `tier` key and it does not
mean the same thing in the two files. In the primary freeze it is `mandated` or `corrected`
and it records how a defective pair was repaired (ADR 0016). Here it is `development` or
`generalisation` and it records when an arm may be looked at. Code that reads `tier` from a
frozen record must know which set the record came from.

---

## 3. The candidate frame is RCSB, not ASD

`CHALLENGE.md` §6 points at the Allosteric Database. We surveyed it and every comparable
source, and used RCSB instead. The full survey is `evidence/databases.md`. The short form:

- **No database certifies allostery per record, per site, per structure.** ASD v1 certifies
  _proteins_, ASD 2023 mixes 3102 curated sites with 66,589 machine-predicted ones and
  publishes no inclusion criteria, ASBench's rules are behind a paywall and its licence
  forbids redistribution, CASBench unions its site over every deposited structure, and
  AlloBench has no apo step at all.
- **ASD is reachable, and the 2026-08-24 claim that it is not was a method failure.**
  Corrected 2026-09-02. HTTPS still fails on the deployed certificate, but plain HTTP serves
  all twelve release archives — 143 687 774 bytes, on disk and re-measured. The anonymous
  download page builds its list from a `dataRecord2023` JavaScript array rather than from
  `<a href>` elements, which is what the 2026-08-24 scrape missed. What ASD supplies is
  unchanged and is the reason the frame is still RCSB: its evidence bar sits on the protein,
  not the site, and its 2023 release mixes 3102 curated sites with 66,589 machine-predicted
  ones. **It is a recall device, not a certification.** A 2026-09-02 sweep took 34 leads from
  it and **zero** new admissible arms, because none has been through clause (ii). ASD states
  a research-use-only licence and forbids redistribution, so no ASD file is ever committed.
  `../review/09-extension-sweep.md` §1.3 holds the retrieval recipe.
- **AHoJ-DB's apo call is not our clause (iii).** Queried for `AY7` it returns `1opl` — the
  exact pair this repo's own audit rejected, because myristate contacts 16 of 20 labels at
  3.29 Å.

The frame is therefore a recorded RCSB full-text query, filtered to experimental structures
at the ADR 0009 resolution ceiling, plus targeted literature sweeps for families the
full-text frame misses. Classical effectors are the reason for the second frame: a PDB title
rarely calls an AMP site "allosteric".

**This does not weaken clause (ii), and it cannot.** No database satisfies clause (ii)
either. The functional-evidence DOI is re-established per target from primary literature.
That is the expensive part of building a set like this, and no choice of frame avoids it.
The frame is a **recall device**; clause (ii) decides.

---

## 4. Four admission clauses beyond the eight

These bind this set and not the primary one, because they are **selection** rules and a
selection only exists where there is a pool. That is ADR 0009's reasoning, applied again.

> **(ix) Single-chain lining.** Every protein residue lining the effector at 4.5 Å must lie
> in the modelled chain. Measured, not assumed.
>
> **(x) Apo occupant classification.** No apo component may contact a **scoreable** label.
> A contact is permitted only on a label that is itself an active-site residue, which clause
> (vii) has already removed from the scoring universe.
>
> **(xi) Structure admission.** ADR 0009 clause 2: X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å.
>
> **(xii) Within-set redundancy.** No two secondary targets share a Pfam family, and none
> shares one with a primary target.

Each clause has a test in `tests/test_secondary.py`. Which artifact each one reads, and
which gate runs it, differ — and an audit found that difference hidden, so it is stated here:

| Clause | Read against                            | Gate                                 |
| ------ | --------------------------------------- | ------------------------------------ |
| (ix)   | the **biological assembly**, downloaded | `make verify` — **not** `make check` |
| (x)    | `frozen.json`                           | `make check`                         |
| (xi)   | `selection.json`                        | `make check`                         |
| (xii)  | `manifest.yaml`                         | `make check`                         |

Clause (ix) is the one that cannot run offline, and that is not a shortcut. The measurement
needs coordinates the deposited asymmetric unit does not carry. An earlier offline test read
`holo_label_footprint` and asserted a single chain, which `benchmark.derive` guarantees by
construction: the field is built from an already chain-filtered list, so the assertion could
not fail and an interface site would have passed it in silence. That test has been renamed to
what it does check, and the clause itself is enforced by the network test.

**Clause (ix) is the expensive one, and its cost is stated rather than hidden.** ADR 0010
fixes the node set to one chain, so `transfer_labels` drops any lining residue on a second
subunit **in silence**. The clause removes a class of allosteric site the MWC picture makes
central: the subunit-interface site. In CASBench's 91 curated enzymes, 27 % of entries have
at least one of the two annotated sites formed at an intersubunit contact
(doi:10.32607/20758251-2019-11-1-74-80). Eleven candidates were rejected on this clause,
the largest single cause of rejection after an underivable active site.

**Clause (x) exists because clause (iii) alone is not enough.** A second-site occupant is
permitted — the primary set's own `2G2H` carries an ATP-site inhibitor 16 Å away. What is
not permitted is a component in the pocket being predicted. A blanket "no drug-like
component in the apo" was tried first and was **wrong**: it would have disqualified `2G2H`
itself, and `2G2H` is in the primary set. The clause as written catches the real failure
mode, which is a sibling fragment of the same series clearing a scoreable-set check by half
an ångström. One candidate was rejected on it, and three more on clause (iii).

**Clause (xii) has teeth, and it cost a good target.** SHP2 passed clause (ii) with the
strongest pharmacology in the candidate pool — SHP099, doi:10.1038/nature18621 — and was
rejected because it shares Pfam PF00017 (SH2) with the primary BCR-ABL1 arm. The ledger
records that.

---

## 5. The admitted set

Nine targets. All numbers below are from `frozen.json`, re-derived from the deposited files.

| Target        | Tier             |    N | Scoreable | Candidates | Prev. | Apo → holo          | Effector | Source rule      |
| ------------- | ---------------- | ---: | --------: | ---------: | ----: | ------------------- | -------- | ---------------- |
| `mkp5`        | `development`    |  147 |        11 |        136 | 8.1 % | `1ZZW:A` → `7UMV:A` | `NUU`    | `PTP`            |
| `chk1`        | `generalisation` |  272 |        12 |        261 | 4.6 % | `1IA8:A` → `3JVR:A` | `AGX`    | `VAIK, HRD, DFG` |
| `ptp1b`       | `development`    |  298 |        11 |        287 | 3.8 % | `1SUG:A` → `1T48:A` | `BB3`    | `PTP`            |
| `smyd3`       | `generalisation` |  425 |        12 |        408 | 2.9 % | `6P7Z:A` → `7BJ1:A` | `QKT`    | `SAM`            |
| `glucokinase` | `generalisation` |  453 |        19 |        438 | 4.3 % | `3IDH:A` → `3F9M:A` | `MRK`    | `GLC`            |
| `hiv_rt`      | `development`    |  543 |        16 |        534 | 3.0 % | `1RTJ:A` → `1VRT:A` | `NVP`    | `POLA, YXDD`     |
| `ns5b`        | `development`    |  553 |        16 |        550 | 2.9 % | `1QUV:A` → `2BRK:A` | `CMF`    | `GDD`            |
| `p97_vcp`     | `generalisation` |  723 |        17 |        688 | 2.5 % | `5FTK:A` → `5FTJ:A` | `OJA`    | `ADP`            |
| `ecoli_cps`   | `generalisation` | 1058 |        19 |        997 | 1.9 % | `1A9X:A` → `1T36:A` | `U5P`    | `ADP, MN, PO4`   |

The `Scoreable` column is the label set after clause (vii), which is what a method is
scored against. 133 scoreable labels across 4299 candidate residues. Only `mkp5` loses a
label to that clause. Section 5.2 says why that matters. Every arm's functional-evidence DOI,
the sentence that carries it, and the caveat a reviewer will raise are in `manifest.yaml`.

### 5.1 What the set spans

A benchmark for generalisability has to vary along more than one axis, or it measures one
thing repeatedly.

- **Size:** 147 to 1058 modelled residues, a factor of 7.2, or 0.86 dex.
- **Crypticity:** the transplant clash fraction runs from 0/29 (`smyd3`) and 0/23
  (`glucokinase`), where the pocket is open in the apo, to 32/33 (`ns5b` — the pocket is not empty space but is
  occupied **by protein**, a helix from the fingers-thumb loop). `ptp1b` at 21/28,
  `hiv_rt` at 13/20 and `mkp5` at 12/22 sit between. A geometry-first baseline sees nothing
  at all in `1QUV`.
- **Distance from the source:** nearest label ranges from 0.0 Å (`mkp5`, where one label is
  itself an active-site residue) and 4.4 Å (`hiv_rt`) to 22.3 Å (`ns5b`). `hiv_rt` is the
  set's argument in one arm — the NNRTI pocket is close to the catalytic aspartates and the
  inhibition is nonetheless cleanly non-competitive.
- **Biology:** two phosphatases of different families, a kinase, a methyltransferase, a
  hexokinase, two viral polymerases, an AAA+ ATPase and a ligase. Four organisms.

### 5.2 Three axes on which this set is easier than the primary set

Found by adversarial audits, and recorded here rather than left for a reviewer. **A cross-set
comparison in Phase 5 is not like-for-like on any of the three, and the report must say so
before it quotes one.**

**Axis A — clause (vii) overlap.** Clause (vii) removes a label that is itself an active-site
residue, because a residue that scores maximally by construction measures nothing. That clause
costs this set almost nothing: **8 of 9 arms have no overlap at all**, and `mkp5` loses exactly
one label. Both primary KRAS arms lose **5 of 21**.

That is not the result of a filter — the ledger's single clause-(vii) rejection, `p38a`,
was rejected for labels that did not map into the node set, not for active-site overlap.

**Axis B — structure quality.** Clause (xi) is a selection rule, so it never applied to the
primary set. Applied to it anyway, **`1OPL` is the only structure in either set that fails**:
X-ray at 3.42 Å against the 2.5 Å ceiling, with 22.18 % RSRZ outliers, the 0.4th absolute
percentile of the PDB. All 18 secondary structures pass. `1QUV` passes at exactly 2.50 Å.
So the tuning and generalisation tiers are built from better-resolved coordinates than one
claim-bearing primary arm, and a contact network is a function of coordinate quality.

**Axis C — resolution matching.** Neither set applies the 0.3 Å community guidance
(`../README.md` §4a), but they fail it at different rates: **4 of 5** primary arms exceed it,
against **3 of 9** here, and the primary worst case is 1.25 Å against 0.64 Å. Every transplant
clash count and pocket-lining RMSD is a two-crystal difference, so the primary set's difficulty
axes carry more resolution confound than this set's.

**A gap this set does not fill.** Every admitted effector is a synthetic compound. The one
candidate with a **physiological** effector, AMP on glycogen phosphorylase, was rejected by
clause (ix). Classical allosteric enzymology — cooperativity and feedback inhibition by a
metabolite — is therefore untested here, and that is the oldest and best-attested form of
the phenomenon the method claims to predict.

---

## 6. What the achieved N supports, and what it does not

Stated plainly, because a set this size is easy to over-claim.

- **`generalisation` supports a hypothesis test, and exactly one.** N = 5 gives a minimum
  attainable one-sided p of 2⁻⁵ = 0.031, so a clean sweep rejects at α = 0.05 and nothing
  weaker does. There is no margin: one failure in five leaves p = 0.19. **And 0.031 > α/2 =
  0.025**, so any correction to k ≥ 2 makes this test unable to reject at any effect size.
  The project therefore has one confirmatory decision at full α and it is this one; the primary
  arms are supportive (`../evaluation/README.md` §8).
- **The detectable success rate is 0.956, not "near 0.9" — corrected 2026-08-24.** This bullet
  read "near 0.9, not near 0.8". Measured: at 80 % power and one-sided α = 0.05 the smallest
  detectable per-target success rate is **0.956**. Power against π = 0.9 is only **0.590**, and
  a clean 5/5 estimates π ≥ 0.549 at 95 % one-sided confidence. The tier can detect a method
  that almost never fails. It cannot distinguish 0.9 from 0.55.
- **Using all nine arms with leave-one-target-out nested tuning would be better, and it is not
  what this freeze does.** That design raises power against π = 0.9 from 0.590 to 0.775 and
  tolerates one failure. It is recorded as the alternative that was not taken, because
  re-splitting a frozen set after seeing this analysis is the thing the seeded rule exists to
  prevent (§7.12).
- **The scalability slope is the weaker claim of the two.** 0.86 dex of span across 9 points
  gives a slope with wide confidence limits. Report the interval, never the point estimate.
- **`development` cannot test anything, and is not meant to.** N = 4 has a minimum
  attainable p of 0.0625. It exists to tune on, and every number from it is contaminated by
  construction.
- **The tuning tier is narrower than the set it was drawn from.** The seeded split put
  `mkp5`, `ptp1b`, `hiv_rt` and `ns5b` in `development`: two phosphatases — both using the
  same `PTP` motif rule — and two viral polymerases. Two biological classes, against five in
  `generalisation`. A hyperparameter chosen on four arms spanning two classes will transfer
  worse than the N alone suggests, and that is a property of this particular seed, not of the
  method. **Quantified 2026-08-24: seed 0 is the single worst of the 16 attainable splits for
  biological-class diversity in `development`** — a 1-in-16 draw. It is disclosed rather than
  reseeded, because reseeding until the split looks good is the thing the seeded rule exists to
  prevent.
- **No arm is blind.** Every admitted site is curated or published as allosteric.
  `blind.value` is `false` on all nine and the reason is recorded per arm. A comparator
  trained on ASD, ASBench or CASBench and evaluated here **is not blind** and must be
  labelled (ADR 0017).

---

## 7. Limitations

Recorded rather than absorbed. Each is a thing a reviewer would find. Twelve were written on
2026-08-24; items 13 to 16 were added by the 2026-09-02 audit, and the last two are properties
of the **whole** benchmark rather than of this set.

1. **The set is smaller than the power analysis asked for, and the reason is now measured
   rather than asserted.** 12 development and 16 generalisation targets were the design
   target. 4 and 5 were achieved. 97 candidates were considered, 73 screened to a deciding
   clause, and 9 admitted.

   The 24 rows recorded `pending` in `selection.json` **were screened on 2026-08-24** and are
   no longer an unknown. A wider sweep ran beside them: 1061 RCSB full-text entries over 12
   phrases, plus a 1049-accession merge of AlloBench, CASBench, GtoPdb, AHoJ-DB and UniProt
   activity-regulation text. About 55 candidates reached a geometric measurement. The screening
   record, with manifest-row fields for every survivor, is `evidence/extension-candidates.md`.
   It corrects this limitation in two places.

   | Clause                       | Denominator                             | Killed | Rate     |
   | ---------------------------- | --------------------------------------- | -----: | -------- |
   | **(ix)** single-chain lining | 32 physiological-effector holo entries  |     23 | **72 %** |
   | (ix)                         | all 44 holo entries measured            |     28 | 64 %     |
   | **(ii)** functional evidence | 7 that survived every structural clause |      2 | **29 %** |
   | (x)/(iii) apo occupant       | 10 that survived (ix)                   |      4 | 40 %     |
   | (xii) within-set redundancy  | 380 accessions, unrestricted RCSB frame |     47 | 12 %     |
   | (xii)                        | 865 accessions, merged 6-route harvest  |    119 | 14 %     |
   | (xii)                        | the 24 pending rows                     |     11 | 46 %     |
   | (xi) resolution              | 13 pending holo entries                 |  **0** | 0 %      |
   | (iv) identity                | 14 pairs measured, 98.1-100 %           |  **0** | 0 %      |

   - **Clause (ix) is the binding constraint, and this document understated it.** §4 calls it
     "the largest single cause of rejection after an underivable active site" at 11 of 97.
     Measured prospectively on candidates chosen _for_ the gap §5.2 admits to, the rate is
     **72 %**, and end-to-end survival is 3 of 32. Clause (ix) and that gap are the same fact:
     metabolite feedback and cooperativity are quaternary phenomena, so the class the set is
     missing is exactly the class the clause excludes. **Gap (a) cannot be filled at scale
     without amending clause (ix) or ADR 0010's one-chain node set.**
   - **Clause (ii) is the second most expensive, and it bills at the end.** It killed 2 of the
     7 candidates that had already passed every structural clause. Both looked admissible until
     someone read the paper. §3 predicts this cost. It is now measured at 29 %.
   - **Clause (xii) is not the binding constraint**, though the pending list makes it look that
     way — that list is ten protein kinases deep and the set had already spent its two kinase
     families. It costs 12-14 % on two independent frames. The fix is to stop proposing
     kinases, not to relax the clause.
   - **Clauses (xi) and (iv) cost nothing** and must be dropped from the story about why N is
     small. Resolution killed one candidate in the whole sweep. Identity killed none.
   - **A fifth cost has no ledger category**: the effector turns out not to occupy a
     topographically distinct site. Rat MVK, _Pyrococcus_ UMP kinase and legumain all failed
     this way, and no database row shows it. **The ledger must record it as its own clause.**

   **Five further arms are reachable and none was added.** `pkm2`, `fbpase` and `gdh` carry
   **physiological** effectors — FBP, AMP and GTP — which is the gap §5.2 names, closed three
   times over. `fbpase`/AMP is the same chemistry as the glycogen-phosphorylase arm the set
   lost. All five take N from 9 to 14 and the `generalisation` tier from 5 to about 7 or 8. The
   minimum attainable one-sided p moves from 2⁻⁵ = 0.031 to 2⁻⁷ = 0.0078 or 2⁻⁸ = 0.0039. At
   N = 5 one failure leaves p = 0.19 and the tier is dead. At N = 8 one failure leaves
   p = 0.035 and the tier still rejects. That is real margin. It was not taken for three stated
   reasons: it re-runs the seeded split and so changes every existing tier assignment, which is
   a re-freeze rather than a repair (§7.10's own argument); `gdh` needs one more literature pass
   on clause (ii); and three of the five apo entries have no primary citation.

   **The design target of 28 is not reachable from this frame.** Two independent exhaustive
   frames produced 5 further admissible targets between them. That is the supply. The size
   ladder is **not** repairable either. No new admissible target is below 272 residues **from
   that frame** — the qualifier matters and was missing until 2026-09-02 — and the mechanism is
   now measured rather than inferred: small catalytic domains are overwhelmingly obligate
   oligomers, so they fail clause (ix) before size is ever the question. §7.2 stands, with that
   as its cause.

   **A third frame was swept on 2026-09-02 and it changes the supply estimate, not the
   decision.** ASD proved reachable over plain HTTP after all — the 2026-08-24 "a script cannot
   fetch ASD" conclusion was falsified — and 3147 site records yielded **34 survivors of every
   structural clause the sweep could measure**. Four of them are under 272 residues, the
   smallest at **158**, so the sentence above is frame-bound and not a fact about the world.
   Thirteen carry a **physiological** effector, against zero in the frozen set, which is the
   one gap §5.2 admits to. Then clause (ii) was read for all 34
   ([`../review/14-clause-ii-literature-pass.md`](../review/14-clause-ii-literature-pass.md)):
   **13 pass, 5 fail, 16 unread behind publisher paywalls**, and seven of the thirteen passes
   carry a separate structural problem. **The honest count of new admissible arms today is
   zero, and the honest count of new leads is 13.** Six of those thirteen have no known
   structural blocker — `hisG`, `UBE2I`, `PDC1`, `LGMN`, `proRS`, `fbpC` — and `hisG` is the
   best single lead: a metabolite effector, a new organism, 284 residues, inhibition kinetics
   measured three ways in an open-access primary paper. **The set is not re-frozen for this
   submission**, because adding an arm re-runs the seeded tier split and reassigns every
   existing arm. That is a re-freeze, not a repair. `../review/09-extension-sweep.md`.

2. **The size ladder is thin at the bottom, and one arm carries it.** Eleven candidates
   with a recorded size below 272 residues reached a deciding clause. One survived: `mkp5`,
   at 147. The other ten failed across five distinct clauses — four on an underivable active
   site, three on clause (ii), one each on clause (ix), clause (xi) and a construct artefact.
   That spread is the shape of a supply problem rather than of one bad filter. The count is a
   floor, not a total: 35 of the 73 screened rows record `n_res_est: "?"`, so the ledger
   cannot say how many small candidates were really considered. HIV-1 integrase failed twice — first because `1ITG:A` does not model
   catalytic E152, then, on the repaired `1BL3:C`, because every ALLINI pocket sits at the
   CCD dimer interface. Cathepsin K also failed twice — first because its own discoverers
   coined "ectosteric" expressly to distinguish those sites from allosteric ones, then
   because the alternative holo `5J94` builds part of its pocket from an N-terminal
   expression tag at residues −7 to 0. Remove `mkp5` and the span falls from 0.86 dex to
   0.59, so the scalability claim rests on one target more than a reader would guess.

3. **Interface sites are absent by construction, and the check for them needs the
   assembly.** Clause (ix) removes them, and the population it removes is not a random
   sample — the MWC-style interface site is exactly the class excluded. Worse, the obvious
   way to check it is **wrong**: measuring on the deposited asymmetric unit gives a false
   pass whenever an interface site is deposited with one chain in the unit. Glycogen
   phosphorylase was admitted that way and then rejected, when the same measurement on the
   `1FA9` dimer showed the AMP site drawing 8 lining residues from one protomer and 3 from
   the other. `tests/test_secondary.py` now measures on the biological assembly, for both
   benchmark sets. Extending the node set past one chain is a Phase 4 coarse-graining
   question, and is recorded there.

4. **Non-catalytic targets are out of scope entirely.** A pair whose apo admits no
   `{from_ligands: …}` or `{from_motifs: …}` rule is unusable, because the active site is
   the propagation source. Nuclear receptors, transcription factors and pure scaffolds
   cannot enter. Twelve candidates were rejected on this. The admitted set therefore leans
   toward cofactor-bearing enzymes, and a claim about "proteins" from this set is really a
   claim about catalytic domains.

5. **One arm's evidence is fragment-grade.** `smyd3` rests on KD 42 and 84 µM with about
   45 % inhibition at 100 µM, and the authors call the compounds "very weak inhibitors".
   It is admitted because the orthosteric alternative **is** excluded by SPR competition
   against both canonical sites, which is the test clause (ii) applies. Weak potency is not
   a wrong mechanism. A reviewer who discounts this arm should re-read §6 with N = 4.

6. **Only two apo entries are globally ligand-free.** `1QUV` (`ns5b`) and `1RTJ` (`hiv_rt`),
   both with an empty `apo_site_occupancy.entry_components`. The other seven arms survive
   clause (iii) on the **site-apo** reading — apo with respect to the site being predicted,
   not free of all ligands. That reading is declared in `docs/benchmark/primary/README.md` §1 clause
   (iii) and is the repo's, not the field's.

7. **One arm has an unmatched orthosteric state**, recorded as `matched: false`.
   `smyd3`'s apo carries `O41` in its substrate channel, so the channel is blocked in the
   input and empty in the holo. Two cleaner SMYD3 apo entries were tested and both failed
   worse; the ledger records them.

   `glucokinase` was declared unmatched too, and was wrong. An audit measured `3IDH` against
   its own title and against the freeze: it is the glucose-bound closed form, not the
   super-open unliganded one, and its core RMSD to `3F9M` is 0.39 Å with 0 transplant clashes
   of 23. It is now `matched: true`. The direction of the error matters — it made a
   `generalisation` arm read as the hardest in the set when it is the easiest on both axes.

   A separate trap in the same field. The **derived** `orthosteric_state.matches_apo` and the
   **hand-declared** `state.matched` disagree on **four** of nine arms — `mkp5`, `chk1`,
   `ptp1b` and `ns5b`. The derived field compares component lists; the declared field is a
   curator's judgement about conformation. Neither is redundant and neither overrides the
   other. Quote which one you mean. (This count read "five" until 2026-08-24. The fifth was
   `glucokinase`, repaired to `matched: true` two paragraphs above, and the count was not
   updated with the repair.)

8. **The frame is a depositor's own word.** An RCSB full-text hit on "allosteric" is a
   claim, not curation. It is a recall device only. The risk it carries is missed targets,
   not admitted bad ones, because clause (ii) is applied afterwards to every survivor.

9. **`selection.json` is not byte-reproducible, and cannot be.** ADR 0012 required that;
   ADR 0021 §6 amended it, because RCSB gains entries every week and the same query returns
   a superset later. What replaced it: the ledger records the frame, the retrieval date,
   every candidate and its deciding clause; admitted rows re-derive from the deposited files
   under `verify`; and a test holds that a candidate absent from the ledger cannot enter the
   set.

10. **One clause (ii) rejection rests on a repository principle, not on a cited threshold.**
    IUPHAR XC's full text was retrieved on 2026-08-24, after the freeze. Two things in it
    change how clause (ii) reads. Its §III is protein-general — "the properties of one ligand
    **(small molecule or protein)** are altered upon binding of a second ligand at a
    nonoverlapping, topographically distinct site" — and an earlier version of
    `docs/benchmark/primary/README.md` quoted that sentence with the parenthetical silently dropped.
    And the same article permits a **bitopic** ligand to occupy both sites at once and still
    behave competitively, so competitive kinetics do not by themselves refute an allosteric
    site.

    `usp7` was rejected for exactly that: "GNE-6640 competes with ubiquitin, a natural binding
    partner. Partner competition is not allostery." That is this repo's reading, not IUPHAR's,
    and the ledger row now says so. `acly` was rejected on the same argument plus an unmatched
    apo, so it stands on the second ground. Neither arm was reopened, because re-admitting one
    changes N and reruns the seeded tier split — that is a re-freeze, and a re-freeze is a
    decision, not a repair.

11. **The split is a large source of variance at this N, and the seed drew badly.** Added
    2026-08-24. Seed 0 is the worst of the 16 attainable splits for class diversity in
    `development` (§6). On the other side, at N = 5 a single hard target moves P(reject) between
    **0.774 and 0.000**, so the generalisation verdict is one target away from flipping. The
    better design — all nine arms with leave-one-target-out nested tuning — raises power against
    π = 0.9 from 0.590 to 0.775 and tolerates one failure. It was not taken, because changing
    the split after measuring its cost is exactly the move a seeded rule exists to forbid. The
    consequence is priced here instead: report the per-target outcomes, never only the combined
    verdict.

12. **The ledger is itself an answer key, and is guarded as one.** For every admitted arm it
    carries `holo`, `holo_chain` and `effector` as structured fields, and its prose names
    real label residues. `tests/test_no_leakage.py` names it in `PROTECTED_PATHS` and in
    `FROZEN_TOKENS`, so no prediction-path module and no experiment runner can open it.
    It is the **third** data route that bypasses the import graph, after `frozen.json` and
    `manifest.yaml`.

13. **Four pinned X-ray entries have no released structure factors, so density validation is
    unavailable for them.** Added 2026-09-02, measured: `https://files.rcsb.org/download/<id>-sf.cif.gz`
    returns **404** for `1IA8`, `1RTJ`, `1A9X` and `1VRT`, and 200 for the entries that do have
    them. **Both halves of `hiv_rt` are in that list** (`1RTJ` and `1VRT`), so no real-space
    validation of either member is possible: no RSRZ per residue, no real-space correlation, no
    independent check on the label residues' own density. `1IA8` and `1A9X` are single members
    of two further arms. These are pre-2000 depositions, when structure-factor release was not
    mandatory, and nothing can repair it. Record it as a difficulty axis: on `hiv_rt` the label
    set's coordinate quality rests on the depositors' R-factors alone.

14. **Family disjointness was achieved. Rule-level disjointness was not.** Added 2026-09-02.
    `chk1` sits in the `generalisation` tier and derives its propagation source with
    `{from_motifs: [VAIK, HRD, DFG]}` — the identical rule that locates BCR-ABL1's active site
    in the primary set. ADR 0012 asks for family disjointness and site disjointness, and both
    hold: CHK1 and ABL1 are different Pfam families at different sites. But the *rule* is
    shared, so an error in that rule would move a primary arm and a generalisation arm the same
    way, and the generalisation set would not detect it. Nothing is repaired here. It is
    disclosed because a shared rule is a shared failure mode, and the set's whole purpose is to
    be an independent check.

15. **All nine arms use a synthetic small molecule as the effector, and so do all five primary
    arms.** Added 2026-09-02, promoted from §5.2 because it is a property of the **whole**
    benchmark and not of this set. Classical allosteric enzymology — cooperativity, metabolite
    feedback, a physiological effector such as AMP, GTP or acetyl-CoA — is untested on all
    fifteen arms. The cause is measured and is clause (ix): of 32 physiological-effector holo
    entries screened, **23 were killed by the single-chain lining requirement**, because
    metabolite feedback and cooperativity are quaternary phenomena. The gap and the clause are
    the same fact. Any claim about "allosteric sites" from this benchmark is a claim about
    **drug-like allosteric pockets in a single chain**, and the report says it that way.

16. **The negative class has an unknown false-negative rate.** Added 2026-09-02. Every arm
    labels one site positive and everything else negative. Beltran 2026
    (doi:10.1126/sciadv.aea2726) reports dozens of functionally allosteric surfaces on Src
    alone, and that computational methods fail to find them. A residue this benchmark scores as
    a false positive may be a real allosteric site nobody has annotated. The consequence is
    directional and it is worth stating: **precision-style endpoints are more trustworthy here
    than recall-style ones**, and a low AUC-ROC against this negative class is weaker evidence
    against a method than a low precision@5 is.
