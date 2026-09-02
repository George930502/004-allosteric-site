# 27 — Fourth-pass synthesis: what was repaired, what is corrected, what is open

**Date:** 2026-09-03 · **Branch:** `main`, from `fcd78a2` · **Supersedes** `26` as the current
ranked list. `26`, `25` and `11` stay unedited as the record of what each pass found.

This pass audited the three frozen layers on `main` after the organisers answered on
2026-09-02. It ran eight instruments in parallel: an adversarial whole-repository pass by a
second coding agent, and seven scoped audits of the sealed tier, the occupant question, the
deposited structures, cross-set consistency, the extension pool, the C1 leak surface and the
statistics.

**Nothing here was decided from prose.** Every finding below was reproduced independently
before it was accepted, and every one that was rejected was rejected against a measurement.

---

## 0. Headline

Three things were wrong that would have invalidated a result, and all three are repaired.

1. **The claim family counted a rejection in the wrong direction.** Holm rejects a two-sided
   test either way, and the implementation counted a method significantly **worse** than
   `cavity_volume` as clearing the family that licenses "the method beats the reference".
   Six of 27 control comparisons have p at or below 0.05 and **all six are losses**; two
   clear Holm's first step.
2. **The C1 leak guard was scanning the wrong tree.** The package scans globbed `src/allo`
   while the runner scan exempted the whole of `src/`. A second package at `src/predict/` was
   read by neither, and the editable install puts it on `sys.path` the day it is written. A
   probe there recovered the positive count for all fifteen arms with the whole suite green.
3. **Negative class (b) did not measure the deliverable.** The shipped statistic ranks the
   detector's site-pocket lining. A shift of four standard deviations on every label residue
   gives power **0** on KRAS and on cardiac myosin.

One thing was wrong that would have made the protocol undecidable: **"clearing a family" had
no definition**, and the frozen layer held both readings in documents that cite each other.

---

## 1. Repaired, with the commit that did it

### 1.1 `f66bb38` — the guards and the scoring path

| # | What was wrong | Probe |
| --- | --- | --- |
| 1.1a | `confirmatory_verdict` family 2 was direction-blind | `test_the_claim_family_counts_a_rejection_only_when_the_method_wins` |
| 1.1b | `verify_evaluation` iterated the arms in the evaluation freeze, so an arm deleted from that file was not checked and the verifier exited 0 over fourteen arms | both freeze and verify now derive from the two INPUT freezes |
| 1.1c | 68 of 74 leaves of the frozen evaluation manifest bind nothing. `evaluation/README.md:3` says the verifier "exits 0 only if nothing moved" | `_conformance_problems` binds six normative fields; `nulls.IMPLEMENTED_GRAPH_RULE` states the graph rule beside the function that builds it |
| 1.1d | `Path("data") / Path("patches")` evaluated to None, so the composed path vanished from the scan. Fourth instance of the same failure mode | five probes in `test_constant_path_guard_catches_composition_and_quote_variants` |
| 1.1e | The package scans globbed `src/allo`; `NON_RUNNER_TREES` exempted all of `src/` | both scans glob `src/`; six tests fail on the `src/predict/` probe |
| 1.1f | 26 path spellings assembled a protected path out of separator-free components and vanished | `segment_cover_violations`, 21 probes |
| 1.1g | A rename left three per-target input audits reachable at a former name | former names derived from `git log --diff-filter=R`, not typed |
| 1.1h | `docs/adr/` was unprotected while ADR 0031 prints 12 of 12 myosin labels | protected whole |
| 1.1i | `.github/workflows/ci.yml` and `pyproject.toml` were scanned by nothing | `.yml`, `.yaml`, `.toml` in `RUNNER_SUFFIXES`; frozen manifests exempt as data |

**The mutation sweep behind 1.1c.** Every one of the 74 leaves of
`evaluation/manifest.yaml` was mutated in turn and the offline verifier re-run. Six produced a
problem. That generalises a single probe into a statement about the whole freeze, and it is
why the six normative fields are now bound by a conformance check rather than by a claim.

**Why 1.1f is a change of kind and not another patch.** The resolver is a whitelist of
spellings and a whitelist loses this race; it lost four times. The backstop asks the other
question — does this file hold every component of a protected path — which needs no
evaluation at all, because the interpreter must still get the characters from somewhere.

### 1.2 `5d921df` — the current-state documents

Forty-one defects were reported and the current-state ones are repaired. Nearly every one was
a count or a version stale since 2026-09-02: arm count 5 to 6, protocol version 2 to 3, ADR
count 36 to 37, decision records 25 to 37, limitations 11 to 16. The front door's three target
rows contradicted ADRs 0029, 0031 and 0036 and are rewritten from them. `conformance.md`
carried a banner for ADR 0037 alone, so five statements written before the other four ADRs
stood unwarned.

The data-route list held eleven routes and two payload notes and called itself thirteen. The
duplicate is folded into the route it repeated, the two routes closed on 2026-09-03 are
written up, and the count is fourteen in all four places that state it.

### 1.3 `d25aa17` — protocol version 4

| ADR | Decision |
| --- | --- |
| [0038](../../adr/0038-a-family-is-cleared-when-holm-rejects-at-least-one-arm.md) | A family is cleared when Holm rejects at least one arm. The rule is in `confirmatory_verdict` as `cleared`, not in prose |
| [0039](../../adr/0039-negative-class-b-also-scores-the-label-set.md) | Negative class (b) also scores the label set, beside the site pocket. Both descriptive |
| [0040](../../adr/0040-the-sampler-budget-is-a-named-constant.md) | `nulls.MAX_ATTEMPTS_PER_PATCH = 4000`, named and explained |

Raw measurements: `data/endpoint-b-2026-09-03/`, with seeds, sample sizes and
Clopper-Pearson intervals. `allo evaluate verify` re-derives with zero problems.

---

## 2. Corrections to the frozen layers

A freeze is not repaired in place (`CONTRIBUTING.md` §3.2). These are the corrections. Read
this section before quoting any of these numbers.

| Where | Says | True |
| --- | --- | --- |
| `primary/README.md:3` | "Five scoreable arms" | six, since ADR 0031 |
| `secondary/README.md:502` | five arms | six |
| `primary/manifest.yaml:442`, `primary/README.md:265` | `6C1H` is "bovine" cardiac myosin S1 | rat unconventional myosin-Ib, UniProt Q05096, as `primary/README.md:202` says two pages away |
| `evaluation/README.md:185, 210, 222, 330` | "five primary arms" | six |
| `evaluation/README.md:221` | 6.79x | line 763 of the same file says 8.51x |
| `evaluation/README.md` §0.1 | the 0.05 tolerance rung is an arm the sampler cannot fill | the rung's **budget** was exhausted. At a cap of 10 000 it draws all 999 patches in 47.9 % of budget (ADR 0040) |
| `evaluation/README.md` §13 | "the positive control rejects on one of three", printed as adverse | one of three **is** clearing, under ADR 0038 |
| `secondary/evidence/extension-candidates.md` §4.1 | survivors span 158 to 1801 residues, 1.06 dex | that column is UniProt full length. Measured on the deposited entities the same pool spans 157 to 872, 0.74 dex, **narrower** than the frozen set's 0.86 |

---

## 3. Open, ranked. Each needs a decision, not an edit

### 3.1 The `generalisation` tier was burned before it was sealed — **ADR required**

The seal is broken in **23 tracked files on `main`**, and the commit that states the rule
already published all five arms' positive counts, prevalences and label residue lists on the
day it was written. No candidate method has ever been scored on a sealed arm, so what is lost
is storage secrecy, not scoring secrecy.

`26` §4b.1 calls this "the most important finding of the pass" and carries no row for it in
its own §5 tracker, which is the exact failure `26` §7 criticises in `25`.

**Closed on 2026-09-03 by [ADR 0041](../../adr/0041-the-generalisation-tier-was-never-sealed-against-storage.md).**
Rebuilding an unopened tier cannot be done from leads whose answer keys are already tracked, so
the rule is amended to what it can still deliver: the tier is sealed **against scoring**, not
against storage. `score_arm` raises on a `generalisation` arm unless the caller passes
`unseal="phase-5"`, held by `test_the_sealed_tier_cannot_be_scored_without_saying_so`. Any
generalisability claim must disclose that the counts and label sets were readable throughout
method design.

### 3.2 ADR 0012 clause 2 contradicts itself, and clause (xii) ships one level shallower

**Closed on 2026-09-03 by [ADR 0042](../../adr/0042-clause-xii-is-pfam-family-plus-panther-narrowing.md).**
The headline sentence names three biological groups; the operational sentence rejects on Pfam
**clan**, and the two disagree about `p97_vcp`. Measured live against InterPro 109.0: the two
anchor clans collapse to two because `PF00071` and `PF00063` are both in **CL0023**, which holds
**316 Pfam families** — effectively every P-loop NTP-binding enzyme. `PF00004` (AAA), which
`p97_vcp` carries, is that clan's first member. Applying the rule verbatim would drop `p97_vcp`,
take the `generalisation` tier from 5 arms to 4 and break the N greater than or equal to 5
floor; applied within the secondary set it would also collide `hiv_rt` with `ns5b` and `mkp5`
with `ptp1b`. And it cannot bind the primary set at all, because KRAS and cardiac myosin are
both in CL0023 and `CHALLENGE.md` mandates both.

The clan sentence is withdrawn. The rule is Pfam family, narrowed by PANTHER where families
collide. PANTHER cannot be the primary instrument: fourteen of fifteen arms carry one distinct
PANTHER family and `ns5b` carries none at all. Per-arm assignment and the releases are in
`data/clause-xii-2026-09-03.json`.

**Still open, and it is work rather than a decision:** pin `interpro_release`, `pfam_release`
and `panther_release` in both manifests and add `uniprot:` per target, so the clause derives
from an accession rather than from a hand-typed family list. Both manifests are frozen input
artifacts, so this needs the PI's call on whether provenance fields may be added to a freeze.
Note that `ns5b`'s `pfam` value cannot have come from RCSB, which carries no Pfam annotation for
either of that arm's entries. The value is right; its stated provenance is not.

### 3.3 The occupant instrument is undefined — **ADR required**

Clause (iii) says "no ligand of any kind" and clause (x) says "no apo component may contact a
scoreable label", and neither defines *ligand* or *component*. Water, glycerol, sulfate and PEG
have no declared side. The audit assembled the rosters eight published instruments actually
use — Binding MOAD, BioLiP2, LigExtract, the RCSB Ligand-of-Interest criteria, sc-PDB,
fpocket, CASTp, PDBbind — and proposes a three-class procedure: `APO`,
`APO_WITH_ADDITIVE_IN_POCKET`, `NOT_APO`. The middle class is the one the repository needs and
no single published instrument provides.

### 3.4 `bcr_abl1_corrected` loses 2 of 20 labels, and the truncation is directional

The **count is disclosed**, at `primary/manifest.yaml:387`: "Kinase domain only, so 2 of the 20
labels (525, 529) fall outside the model and are reported as unmapped." The audit brief said no
shipped document says so; the frozen manifest does. What no document states is the
**direction**.

Measured on `1OPL:A`, the only ABL1 apo entry in the repository that models all 20 label
residues, through the frozen default graph and the eight frozen `REQUIRED_BASELINES`. 440
candidates, chance 220.5. Reproduced independently:

| baseline | 20 labels | 18 labels | shift |
| --- | ---: | ---: | ---: |
| `closeness` | 299.85 | 315.47 | **+15.62** |
| `gnm_or_essa` | 304.85 | 318.00 | **+13.15** |
| `eigenvector_centrality` | 350.90 | 362.67 | **+11.77** |
| `distance_from_source_negated` | 212.50 | 222.94 | **+10.44** |
| `betweenness` | 259.60 | 267.33 | **+7.73** |
| `degree` | 274.20 | 278.03 | **+3.83** |
| `perturbation_response_scanning` | 65.90 | 58.28 | −7.62 |
| `distance_from_source` | 228.50 | 218.06 | −10.44 |

**Six of eight inflate, by up to 3.5 percentile points of the candidate set**, and the arm sits
in both confirmatory families. That reproduces exactly.

**The geometric explanation offered for it does not reproduce, and is withdrawn here.** The
audit's prose says the two lost residues are "the two most distal, 22.0 and 25.9 Å against a
kept range of 7.7 to 21.3". The audit's own script prints the opposite on minimum heavy-atom
distance to the source: kept 18 at median 4.3 Å over 0.0 to 12.6, lost two at **3.9 Å and 7.7
Å**, both inside the kept range. So the shift is real and its cause is not established.

**What to do:** disclose the direction and the magnitude wherever the arm's confirmatory
p-value is quoted. It is not repairable — `2G2H` stops at residue 523 — so disclosure is the
whole remedy. Do not attach the distal-residue explanation to it until something reproduces it.

### 3.5 The orthosteric vocabulary is not shared across the sets

Glycerol is a catalytic-state component on one set and unlisted on the other. Either reconcile
the vocabulary or state why they differ.

### 3.6 What N supports, stated honestly

N = 5 cannot support a generalisation claim. N = 8 is the floor. `secondary/README.md` §6 must
say which claim the achieved N licenses, in the same words the protocol uses elsewhere.

### 3.7 Smaller, and each measured

- ~~Add `cardiac_myosin_mandated` to `clause-ix-both-sets.json`~~ **done 2026-09-03.** Measured from the tracked `9GZ2` copy: the `XB2` protein lining at 4.5 angstrom is 12 residues, all in chain A, so clause (ix) passes. ADR 0031 gives both myosin arms the same holo, so the two entries agree, and this one was measured rather than entailed. The file now holds fifteen arms and all fifteen pass.
- Say in `evaluation/README.md` that the sealed tier is fully materialised in `frozen.json`,
  geometry and positive counts included, and that the seal is a reading discipline enforced by
  `PROTECTED_PATHS`.
- Pin the primary set's (x), (xi) and (xii) verdicts in a test. A stale falsifier survived a
  re-freeze in both a test docstring and an accepted ADR, which is what unpinned prose does.
- ~~`docs/adr/0005` and `docs/adr/0007` contradict each other~~ **refuted, see §4.**

---

## 4. Refuted, so that it is not raised a fifth time

- **The myosin B-factor defects are undisclosed.** They are disclosed, in the same table cell,
  at `primary/README.md:235` rather than at line 232.
- **`kras_g12c` review 26 §5.3's Fisher p = 0.0154 is wrong.** It is **stale**, not wrong: it
  reproduces exactly from the label-set mean midrank, which review 25 §1.4 replaced on
  2026-09-02. The shipped statistic gives 0.01291807.
- **ADR 0035's conservation artifact is a 196 KB committed blob.** Seven files, 166,605 bytes,
  163 KiB, tracked since `fcd78a2`. The 196 KB figure was `du` including an ignored
  `__pycache__`. The live error was the retraction's own replacement claim, "untracked today",
  now repaired.
- **`AHoJ-DB`'s `allostery_lig` field is an allostery claim.** It is not.
- **The false "cannot reject at any data" on `ptp1b` and `ns5b`.** The floors are 0.000276 and
  0.000104, below Holm step 1. Both surviving copies sit under staleness banners, so under this
  repository's own rule they are pass records and not defects.
- **Every number in `evaluation/manifest.yaml`.** Checked and correct, including 777 decoys,
  median 45 and 12 of 15 arms at or above the per-arm rejection floor.
- **ADR 0005 and ADR 0007 flatly contradict each other.** They do not. ADR 0007 keeps "ADR 0005
  (active site as a rule)" in force, which is 0005's decision and its title. What 0007 withdrew
  is a different sentence in 0005, about the **distal label set** the evaluation reports over,
  and 0005's own amendment box says exactly that. Both statements are true and they are about
  different things.
- **`bcr_abl1_corrected`'s truncation is undisclosed.** The count is disclosed, at
  `primary/manifest.yaml:387`. The direction is not, which is §3.4.
- **The two lost BCR-ABL1 labels are the two most distal.** They are not, on minimum
  heavy-atom distance to the source: 3.9 and 7.7 angstrom, inside a kept range of 0.0 to 12.6.
  The endpoint shift is real; that explanation for it is withdrawn.

---

## 5. What this pass did not do

- It did not open the sealed `generalisation` tier, and it reproduced no label residue
  identity for a sealed arm.
- It did not score a method. There is no method layer on `main`.
- It did not re-run the detector. `allo evaluate verify --detect` needs the `eval` extra and
  was not run; the offline verifier was, and re-derives clean.
- The occupant instrument's sources are tagged by provenance and most passed through a
  fetch-and-summarise step. Nothing from it is quotable into `docs/report/` until re-read at
  the raw source.
