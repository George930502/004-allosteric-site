# 27 — Fourth-pass synthesis: what was repaired, what is corrected, what is open

**Date:** 2026-09-03 · **Branch:** `main`, from `fcd78a2` · **Supersedes** `26` as the current
ranked list. `26`, `25` and `11` stay unedited as the record of what each pass found.

This pass audited the three frozen layers on `main` after the organisers answered on
2026-09-02. It ran eight instruments in parallel: an adversarial whole-repository pass by a
second coding agent, and seven scoped audits of the sealed tier, the occupant question, the
deposited structures, cross-set consistency, the extension pool, the C1 leak surface and the
statistics.

**It now carries a fifth round as well.** §1.7 records it. The file keeps its name, because a
rename gives the same bytes a second name the former-name ledger has to be told about (ADR
0043), and every document that points here points at this name.

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

### 1.4 The second adversarial round, and one repair that was wrong

The adversarial agent ran a second time against the repaired state and returned eight
findings. All eight reproduced.

| # | What was wrong | Where it is closed |
| --- | --- | --- |
| 1.4a | The **comment explaining a leak route was the route.** `AGENTS.md` and the leakage test both quoted the twelve myosin label residues while describing why `docs/targets.md` and ADR 0031 are protected. Neither file is protected and neither is scanned | Both redacted. `test_no_unprotected_tracked_file_reproduces_a_label_set` makes the 2026-09-02 hand sweep a test, with three-letter codes normalised and a 400-character window, and it fails on a planted file |
| 1.4b | **Code points defeat both path defences.** `Path(*(bytes(x).decode() for x in [[100, 111, 99, 115], ...]))` reads the primary freeze and leaves no string and no bytes literal | Integer runs are decoded and harvested, with a probe. And the guard now states plainly what a static check over Python source cannot promise |
| 1.4c | **The version 4 measurements were not reproducible.** The simulation was an untracked script | `allo.scoring.simulate` and `experiments/2026-09-03-endpoint-b/` |
| 1.4d | **The version 4 endpoint and both sidedness declarations were unbound.** A probe removed the endpoint and flipped both, and the verifier stayed green. Turning `decision.sided` from `upper` to `two` halves every confirmatory tail without moving a pinned value | Three more conformance bindings, each probed |
| 1.4e | `confirmatory_verdict` **omitted `cleared`** when the claim family was absent, so a caller could not tell "not cleared" from an older record | Always present, and False with a reason |
| 1.4f | The former-path list was **derived from git at import time**, so it was empty in a shallow clone and in a `git archive` export | `tests/former_protected_paths.json` is the source; git cross-checks it. Verified by running the test inside a `--depth=1` clone |
| 1.4g | Current-state documents still said **protocol version 3**, and the roadmap still read one-of-three as a failure | Section 0a of the evaluation README, and every current-state version statement |
| 1.4h | **ADR 0039's size claim was wrong** | Below |

**1.4h is the important one, because the fourth pass got it wrong first.** ADR 0039 said
unequal set sizes make the label form "conservative, never anti-conservative". That was
inferred from a single null family. The objection was that the two sides are not exchangeable,
so the statistic's size is a property of the score field rather than a distribution-free
guarantee, and one generator cannot support "never".

Measured over four generators, 20 000 fields per cell, worst size across four correlation
lengths:

| generator | `site` | `label` |
| --- | ---: | ---: |
| `white_noise` | 0.0001 | 0.0086 |
| `smooth_gaussian` | 0.0049 | 0.0154 |
| `cluster_blocks` | 0.0067 | 0.0185 |
| `distance_shell` | 0.0237 | **0.0548** |

The label form **exceeds alpha**. On `bcr_abl1_corrected` under `distance_shell` it runs 0.0513
to 0.0548 across all four correlation lengths, and the worst cell's 95 % interval, [0.0516,
0.0580], is entirely above 0.05. That field is negated distance to a random residue, which is
the shape every distance-correlated baseline in this repository has.

So `label_p` ships as a **descriptive percentile and not a p-value**. It measures the
deliverable, which nothing else here does, and it carries no rejection. `p` holds on all four
generators, so review 25 §1.4's exchangeability argument is vindicated by measurement rather
than by principle.

---

### 1.5 The third adversarial round: six findings, five repairs and one half-refutation

Commit `f36ff67`. The round verified all eight round-2 repairs and returned six more. Two were
real defects in the repairs themselves.

**The size run measured three null laws while reporting four.** `smooth_t` divided a Gaussian
field by ONE chi-square draw per replicate — the standard multivariate-t construction, and
monotone within each column. Every statistic in that module is a midrank, so its ranks were
bit-identical to `smooth_gaussian`'s at the same seed. **The lesson is larger than the bug: a
rank test cannot see a marginal distribution at all.** Heavy tails, log-normal marginals and
any rescaling are the same null; only the copula moves the answer. `cluster_blocks` replaces
it — piecewise constant over a random Voronoi partition — chosen in the adversarial direction,
because blockiness is what made `distance_shell` the worst case. The whole run was repeated at
the same seed and **every conclusion survived**. Round 4 then found that the replacement's own
two cells were ranked ordinally rather than by midrank, and the run was repeated once more; see
§1.6. The table above is that second repeat.

**The sealed tier had a public bypass.** `score_arm` checked `unseal`. `compare_methods` was
exported beside it, takes the same arm and the same score map, reads the same frozen labels,
and had no check at all — so a caller could score a `generalisation` arm through the paired
test and receive calibrated p-values. This is the fourth instance of one shape in this
repository: **the rule was placed in one caller instead of at the boundary.** Both now call
`_require_unseal`, and the test asserts on the SET of public entry points, so a new scorer
cannot forget. It is deliberately not in `_positives`, because calibration and the size
simulation read every arm's labels by design and a check on the read would break the freeze it
protects.

**The decision level was mutable while the release gate stayed green.** `confirmatory_verdict`
reads `decision.alpha` from the manifest and no frozen value records it. A probe moved it from
0.05 to 0.90; every decision changed and `verify_evaluation` returned no problems. Bound twice
now: a literal from above, and from below by the calibration invariant that no arm's
`alpha_star` may exceed the decision level — three of fifteen arms sit exactly at it.

**The former-path ledger was already stale.** It derived from `--diff-filter=R`, and the three
per-target audits were CONVERTED from JSON to Markdown, which git records as a delete plus an
add rather than a rename. They reproduce every primary label set and stay readable through
`git show`. The filter is `RD` now, and a directory that lost any file to a protected tree is
treated as a former protected tree itself, so the conversion is covered by a rule instead of
three names. Eight entries became sixteen, and the shallow-clone property holds: git returns
nothing there and the tracked ledger is the source.

**Two document defects.** The decoy-null paragraph gave a size range inferred from a variance
argument, 0.008 to 0.022, and claimed a bias toward not rejecting — for a null that now
carries two endpoints with opposite verdicts. Replaced with the measured numbers, split by
endpoint. Version 3 was still named current in three current-state documents.

**One finding was half right.** It reported that ADR 0042's PANTHER narrowing "is not
operational" because the clause test rejects every shared Pfam family and never reads PANTHER.
The test is **stricter** than the ADR, not weaker: no two arms share a family, so the
narrowing branch is unreachable and a stricter test cannot admit a bad set. What was genuinely
undone were the ADR's own consequences 1 and 2, and the question blocking them is now answered
by measurement: **adding a provenance field to a manifest moves no frozen value**, because
`freeze` builds `frozen.json` from six named keys and echoes no other. Both manifests pin the
three releases and all fifteen arms carry a `uniprot` accession, with a test asserting that
none of the five reaches the prediction path.


### 1.6 The fourth adversarial round: four findings, four repairs, none refuted

The round verified the round-3 repairs and returned four more. Every one was reproduced here
before it was accepted, and three of the four are defects in round 3's own repairs.

**The replacement generator was scored with ordinal ranks.** `simulate._ranks` used `argsort`
and not midranks. Three of the four generators are continuous and tie nothing, so the two
forms agree on them exactly. `cluster_blocks` is the one exception, and it is the generator
round 3 had just added: it is piecewise constant, and a column of 80 residues holds a median
of **3** distinct values. Every tie was therefore broken by residue index, which runs along
the chain and correlates with space, so the published cells were not the statistic the ADR
names. This is round 3's own lesson recurring one level down — that round found a generator
whose ranks were not what they looked like, and the fix introduced a second. `_ranks` now
calls `scipy.stats.rankdata(..., method="average")`, which is what the shipped
`metrics.rank_vector` always did, and the run was repeated in full at the same seed. Only the
`cluster_blocks` row moved, to 0.0067 and 0.0185; the other three are bit-identical, which is
the check that the defect was confined to ties. Every conclusion survives.

**Conformance was a deny-list, and it bound 6 of 74 manifest leaves.** `_conformance_problems`
named the settings it checked, so a setting nobody thought to name was unchecked, and the
evaluation manifest is prose and normative settings in one file. A sweep mutated all 74 leaves:
**6 were caught**. The rule is inverted now. `DECLARATIVE_SETTINGS` lists the 19 leaves that
are reviewed prose, `NORMATIVE_DIGEST` hashes everything else, and a changed leaf is named in
the failure. Re-swept: **55 of 74 caught, and the 19 that survive are exactly the declared
set**. This is the same inversion `allo.inputs.load` already used for C1 — allow-list, so the
default for anything new is protected — applied to the second boundary that needed it.

**A whole documentation tree reproduced positive counts.** `docs/evidence/method-landscape/`
prints a per-arm scoreable count in a power table and four more in a variance note, and it was
not among the thirteen protected routes. C1 names the count directly. Protected as route 14.
Sweeping for the same shape then found three more instances **in test comments written during
round 3**, which are redacted, and a standing sweep now fails on any tracked unprotected file
that puts an arm identifier, its exact count and a count cue word inside one 250-character
window.

**Pinning a release did not make the values that release.** Round 3 added `pfam_release: 38.2`
to both manifests and left the family lists, whose comment said they came from RCSB at
assignment version 34.0. Measuring the objection made it larger: the two are **different
quantities**, not two releases of one. RCSB annotates the deposited entity and ADR 0042 decides
on the accession, so `bcr_abl1_corrected` carried one family where P00519 has four. The
manifest set is a strict subset of the accession set on all fifteen arms and seven were short,
`ns5b` by fourteen families. Both manifests now carry the accession-derived Pfam 38.2 sets, and
**the verdict is unchanged at that full width**: the only two family collisions among fifteen
arms are between two arms of one protein. The test re-derives both the lists and the verdict.
See ADR 0042.


### 1.7 The fifth adversarial round: the guards were reading the wrong thing, twice

Round 5 ran a `gpt-5.6-sol` adversarial pass over the whole repository beside three scoped
audits — the C1 leak surface, the statistics, and the documents. It returned the largest C1
finding this repository has had, and it found that round 4's own repair had been passing over
every prose document on `main`.

**An enumeration sees what it contains, and neither guard could ask that question.**
`ROOT.rglob("*.npz")` hands back every file in the matched-patch cache. It resolves to no
protected path, so the constant-path resolver clears it, and it spells no protected component,
so the segment cover clears it too. **Both mechanisms miss it by construction**: the resolver
models a glob pattern as a path component, which works only where the component is written
out, and a wildcard is the one spelling where it never has to be. Ten spellings were installed
as live prediction modules and recovered the positive count for all fifteen arms, the sealed
`generalisation` tier included, with the whole suite green. C1 names that exact payload. The
fix asks a third question — not "which path is this" and not "are the pieces present", but
**can this call see a protected path** — which is a containment test in both directions and
needs no pattern analysis. Three more spellings fell out of the same pass: case folding, since
`Path("DATA")/"patches"` opens the cache on this filesystem; `list(x.parents)[i]`, which the
resolver modelled without the sequence conversion around it; and `"".join([...])`, whose
`+` twin constant folding already caught.

**The round-4 count sweep matched identifiers, and prose does not use identifiers.** The sweep
looked for an arm's exact positive count beside its identifier. Every document writes "both
myosin arms", never `cardiac_myosin_corrected`, so the whole documentation set passed over it.
Widening the needles to the identifier's own underscore-separated tokens found **nine real
instances in eight files**, and the worst are the four most-read files on `main`: `AGENTS.md`,
which is in context for every session, `README.md` and `docs/ROADMAP.md`. **Each of them was
describing a leak route and reproducing its payload while doing it.** The rule they break is
stated in the guard's own comment: describe an answer key by its shape and its location, never
by its contents. Three more sites spelled the count as an English word, which a numeral sweep
cannot see, and one printed real label residues in three-letter codes, which is below the
complete-set floor the identity sweep uses.

**Four smaller routes, each reproduced before it was accepted.** The manifest redaction
allow-list bound only beside a schema key and never underneath one, so turning any of eight
leaves from a scalar into a mapping put everything inside it on the prediction path; a leaf
must now be a scalar or a flat sequence and fails closed otherwise. A shell runner's check ran
only over extracted Python, so a bare `sed` on a protected path passed. `docs/report/` was
unprotected and its substitutions page names the effector component ID beside the holo
accession. And the contract itself was one route behind the code.

**The conformance rule called nine operational leaves prose.** `DECLARATIVE_SETTINGS` was
inverted in round 4 and the exempt list was drawn too wide. `pairwise_test` is the frozen
definition of "beat", and an adversarial probe changed it to a Wilcoxon signed-rank test with
the verifier silent. The exempt set is now the ten rationale leaves, the digest covers 64
leaves instead of 55, and each of the nine is probed.

**A freeze claim was false inside the ADR that made the change.** ADR 0044 said the primary
freeze is byte-identical; the same commit moved `orthosteric_vocabulary.additives`, because
the vocabulary is echoed into the freeze verbatim. What is true is that no primary target
moved. Both input manifests also kept one version number across two different sets of bytes.

**Five documents asserted four different ADR counts.** Each had been repaired once and
re-broke with the next batch, so the repair is a test that derives every drifting count rather
than a sixth retyping.

**Six numeric drifts, all in the same class: a document restating a number a machine already
holds.** The protocol README's `detected` column held decoys plus one on every row rather than
what the detector returned; its calibration table quoted an `alpha_star` the freeze
contradicts at the fifth decimal; its three power tables still held the version 2 chain-A row
for `bcr_abl1_mandated`, whose `size_ratio` moved with the chain, and omitted
`cardiac_myosin_mandated` entirely, which moves the published band and the flatness bound. The
primary README's crypticity table carried a stale distance, and the round-4 note beside it
asserted that neither quantity is in the freeze when both are. Every one of these tables is
now derived by a test, with a mutation probe per table.

**And three numbers traced to nothing.** A 95 % interval for `alpha_star` that no record
holds, replaced by review 21's out-of-sample measurement of the same quantity; ADR 0023's
claim that twelve estimates shrink the under-tightening chance below the four-estimate
scheme's 0.27, which review 21 measures at 0.275 to 0.300 and refutes; and ADR 0038's 0.2631
for the uncorrected conjunction, which is in neither cited record while its other five numbers
are, now marked `[UNVERIFIED]` with the bound the records do support.

**Two claims were stated more strongly than their evidence.** §7.2's conclusion that the
published AUC band and the detectable band do not overlap rests, on the published half, on two
data points its own source file marks `[UNVERIFIED]`. And the reason given for printing
recall@5 was a field convention, citing 17 of 22 surveyed tools — where the count is right and
the inference is a category error, since the field's top-N is a per-protein binary over
detected pockets. Both now say what they rest on. Neither number changed.

**One finding was disclosed rather than repaired, and it is the most consequential.** Review
21's S3 measured the combined decoy test's true size at nominal 0.05 as **0.0014 to 0.0066**
by Fisher — 7.6 to 36 times conservative — and no frozen document carried it. ADR 0030 ran the
type-I gate on the per-arm test and on the two replacements it rejected, never on the
construction it adopted. Most of the gap is the discrete support of the per-arm p-value: by
exact enumeration a nominal-0.05 Fisher test is an actual-0.0206 test on its own. **A
rejection there is strong and a non-rejection means very little**, and both readings are now
in §8 and in the manifest. Nothing is retuned, because a size fitted after the construction
was adopted is a hyperparameter chosen with the design in hand.

**One refutation.** §6.2's version-2 percentiles were flagged as stale. The table already
declares itself version-2 data and says it was not re-measured, so nothing is wrong with it.

### 1.8 The sixth round: a declaration and a decision record that each described code they did not have

Round 6 ran a `gpt-5.6-sol` contract audit over the code, at effort high. Sixteen findings,
of which six were code defects, five were prose that had gone wrong against correct code, and
the rest were refuted or already caveated. Three commits: `b88789b`, `db752ff`, `5488e18`.
The three verifiers re-derive every frozen value unchanged at each of them.

**The six code defects, and one of them lets a NaN win.** `_aligned` passed non-finite scores
straight into the ranking, where a NaN sorts to the top of every endpoint and every null at
once — a method returning NaN would have rejected the confirmatory null on every arm. It now
refuses them by residue name. `auc_pr` called `np.diff` on scores that could be infinite, so a
tie run of infinities read as distinct; the tie detection is now a direct comparison.
`_gate` accepted a matched-patch record calibrated at a tolerance the manifest does not
declare. `detect_pockets` based its settings on the package defaults rather than on the frozen
manifest, so a detector change would not have been a protocol change. `classify` started
`best_cover` above zero. The power stage hardcoded a correlation length the sweep was already
varying. `src/allo/scoring/properties.py` was deleted: a byte-identical duplicate of
`structure/properties.py`, importable and imported by nothing, on the wrong side of the C1
import boundary.

**Two findings had the same shape, and it is the shape worth naming.** In both, a declaration
said what the code does and nothing checked the two against each other.

`endpoints.reported` did not list `top_5_components`, which `score_arm` has written into every
record since ADR 0030, while `omitted.top_5_fragmentation` pointed at that list and said
"added, see `reported` above". A reported endpoint that no declaration names is the mirror of
the rule the list exists to enforce. The fix derives the written endpoint set from the source
by AST parse rather than restating it, so the next undeclared endpoint fails.
`NORMATIVE_DIGEST` moved, which is what made the manifest edit deliberate; `protocol_version`
stays at 4, because `reported` is not echoed into `frozen.json`.

ADR 0006 clause 3 says a modified residue contributes its parent's topology, and claimed a
named test made a target impossible to add on the untested path. **That test does not exist.**
The one that did asserted two `M3L` residues on one arm by number, so it could not see a
different modification on a different arm, and it left the suite with that arm in `0f1fe3f`.
`hiv_rt` then entered the secondary set carrying `CSD` — oxidised cysteine — at 280, kept its
two sulfinyl oxygens, and in `allo.structure.properties` took the hydropathy fallback (0.0,
where cysteine is 2.5) and the RSA denominator fallback (200.0, where cysteine is 167.0).
Neither fallback is a measured value and both print as plausible numbers, so both now raise.
The sweep that replaced the old test asks the general question over every arm. **The graph does
not move**: removing the two oxygens changes zero graph edges, so no null, no endpoint and no
scored value moves.

**One frozen value does move, and the first report of this repair missed it.** That report ran
`allo evaluate verify` offline, which skips the pocket detector by design, and the detector
reads the atoms. Under `--detect`, one decoy's cavity volume on `hiv_rt` moved by 0.54 %.
**A verifier that skips a stage cannot certify that stage.** The full extent is that one
number: 72 pockets before and after with the same identifiers, `n_scoreable`, the halo
exclusions and `minimum_attainable_p` unchanged, and the site pocket keeping its identifier,
its lining and its volume. Re-frozen at `protocol_version: 4` on ADR 0044's precedent, since
no endpoint, null, decoy rule or decision changed.

**One finding was real, measured, and deliberately not acted on.** Four frozen apo entries
model alternate conformations, and three code paths answered that question three ways by
accident — last conformer's CA in `evaluation_graph`, first in `_chain_ca`, and every
conformer in the contact graph and the SASA integration. ADR 0045 states the policy, measures
it — 0.335 % of edges on the worst arm, at most 0.100 angstrom of CA, up to 0.213 of RSA — and
declines the change, because adopting the better primary-conformer rule is a protocol v5 and a
re-freeze of three layers for an effect that is **identical for every method**. What is closed
is the part that was a defect rather than a choice: two functions computed the same quantity
and disagreed, with nothing to notice.

**The ADR 0006 finding generalised, and the sweep that generalised it found five more.**
`gpt-5.6-sol` ran the same sweep and returned zero issues on the round's diff, so this half is
a Claude finding, reproduced before it was accepted. Every `test_*` symbol any tracked document
or comment names was resolved against the symbols the suite defines. **Five citations resolved
to nothing.** Three were stale names: one in the leakage guard's own comment for a test that
was renamed, and two per-table names in the protocol README for tests that round 5
consolidated into one. Two named guarantees nobody had written: ADR 0011's second half,
that a residue the ground truth calls allosteric in one arm is not a negative in a sibling arm
of the same protein; and `simulate.py`'s claim that its ranks are pinned against the shipped
statistic — which is the exact guarantee whose absence let the ordinal-rank defect ship in
round 3. Both were measured first and both hold, so both are now tests rather than sentences.

**The class is closed rather than the five instances.**
`test_no_document_cites_a_test_the_suite_does_not_define` resolves every citation in every
tracked document. It un-wraps a Markdown line break inside an identifier, which the first
hand-run of the sweep needed and did not have — three real citations read as missing for that
reason alone. A citation spelled with its `.py` extension names a file, and a removed file is
legitimate history, so those pass. One name is allowed: ADR 0006 records the guard it wrongly
claimed to have, and naming it is the correction.

**The second codex pass found three more, after the first one approved.** The first pass on
the round's diff returned zero issues while running the very sweep that had just found five
citation defects. Told that, and told to treat its own approve as unreliable, it returned
three findings and all three reproduce.

**A seventh spelling of the enumeration hole, and the first that defeats the enumeration guard
itself.** `enumeration_violations` inspects a call whose callee is an attribute, so
`scan = ROOT.rglob` followed by `scan("*.json")` escapes it: at the call site the callee is a
bare name, and at the assignment there is no call. Installed as a live method on
`allo.structure.graph` it enumerated 1304 files including all three `frozen.json`, with all 48
tests green. The fix is the third question again, the one round 5 arrived at for paths: not
"which path is this", not "are the pieces present", but **does this file obtain a traversal
capability at all**. `traversal_capability_violations` answers it with no dataflow analysis,
and it is free because no module under `src/allo` names a traversal function in any position.
Four aliasing spellings are now permanent probes, the `getattr` string form among them.

**A NaN defeats the multiplicity path, and this one is my own miss.** `_aligned` was given a
non-finite guard earlier in this round, for the reason that one NaN score sorts to the top of
every endpoint and every null at once. The same argument applies to every p-value a decision
reads, and `np.any((values <= 0) | (values > 1))` does not reject a NaN because every
comparison with a NaN is false. The consequence is worse than a record that serialises as bare
`NaN`, which is not JSON: `holm` sorts the NaN **first**, gives it the tightest threshold,
fails to reject it, and the step-down then stops. Measured on the frozen confirmatory family,
one NaN turned two rejections at p = 0.01 into none. Patching one entry point and not the
class is the lesson; the check now lives in one function that `holm`, `combine_arms` and
`calibrated_p` all call.

**A third pass then found two more, and refuted one of its own.** Told that its second pass
had been right and to try to defeat each fix, it returned four. **`settings` was a way to
supply your own test**: `confirmatory_verdict` takes a settings override so a test can run a
cheap protocol, and it also accepted a replacement DECISION block, so
`settings["decision"]["alpha"] = 2.0` clears both families at p = 0.6 with every guard green.
`holm` did not check alpha either. This is the argument `apo_input` makes for having no
`manifest` parameter — "every method saw identical inputs" has to be true by construction, and
so does "every method faced the same decision rule" — so the frozen decision block is now the
only one the verdict will apply. Two more rows of `docs/report/conformance.md` made the
instrument-versus-result error this round had already corrected in three others: a classical
comparison of 43 scorers against 11 marked "done and measured" when every one of those scorers
left with the method layer, and statistical enrichment marked the same because the protocol is
frozen. Its §6 said the N × N construction "exists and is verified" two pages after row 1 of
the same table says it does not.

**One of the four is refuted, and it is the one marked high.** A traversal name built from
`chr()` arithmetic defeats both the composed-`getattr` ban and the new capability scan. It
reproduces, and it is **the limit ADR 0043 already records**, in those words, for the same
construction applied to a path. The pass was asked not to report what the repository documents
as known. What was genuinely missing is that the limit was written at the path guard and not at
the capability guard, so it is now stated at both and in the ADR, with the runtime boundary
that would close it named as the next step rather than attempted at the end of an audit round.

**A fourth pass found one more, one argument over from the third.** `calibrated_p` was given
the non-finite guard on its p-value and not on its size ratio, and `max(float(ratio), 1.0)`
keeps a NaN. `norm.sf(nan)` is nan, `max(p, nan)` returns p, so **the calibration silently
disappears and the raw p-value reaches Holm untightened** — the one direction that matters,
since the rescale exists to tighten. A ratio below 1 was clamped up, which hid a broken gate
rather than reporting it, and the function's own docstring says `ratio >= 1` holds by
construction. Both now raise. That makes four separate places in this round where a guard was
added at one entry point and not at the class: `_aligned`, then the p-value functions, then
`holm`'s alpha, then this. **The recurring lesson of round 6 is not any one defect. It is that
fixing the instance is what leaves the next one.**

**And the shipping conformance artifact understated the guarded surface.**
`docs/report/conformance.md` said sixteen protected file routes where the other three
documents said nineteen — and it was the one page of the four that the derived count test did
not bind, which is exactly why the other three stayed in step. It is bound now.

**Four sentences were wrong where the code was right.** `site_pocket_rank` ranks the site
against the decoy linings and not against every detected pocket, and the halo rule makes the
published number optimistic against APOP by an unstated amount. `holm` never reads
`decision.sided`. `_gate` inlined two type-I bands that went stale when the input layer moved
to fifteen arms. `DECLARATIVE_SETTINGS` said "the 18 leaves" when the count is derived.

**The round's document half withdrew a comparator outright, in `fccaa31`.** §1.7 had flagged
the published 0.75-0.82 AUC band for the elastic-network family as resting on two data points
its own source marks `[UNVERIFIED]`, and left the number in place. Round 6 read the primary
sources. **There is no published AUC baseline for that family at all.** AlloPred, PARS's
precursor, Ohm, bond-to-bond propensity, ESSA and STRESS report no AUC in full text, and the
family's own five-method benchmark over 432 structures (doi:10.1016/j.patter.2021.100408)
reports none either. The two points that made the band are both **supervised** residue-level
predictors — ZHMolEReP and AR-Pred — so the band was mislabelled rather than wrong. A measured
AUC here therefore has no literature comparator and must be judged against this protocol's own
controls. Allo-PED makes the point alone: **0.920 over pockets and 0.563 over residues, same
predictions, same test set** (doi:10.1101/2025.03.28.645953). The same commit stopped three
documents claiming results no method on `main` has produced, since ADR 0037 removed the method
layer. Record: `data/enm-auc-band-2026-09-03.md`.


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
| `secondary/evidence/extension-candidates.md` §5, and its per-arm family tables | "clause (xii) costs only 12 % of an unrestricted frame", screened against the manifests' family lists | those lists were RCSB per-entity assignments and a strict subset of the accession sets the clause resolves on (ADR 0042). A wider blocking set can only reject more, so 12 % is a **lower bound**. No admitted arm moves: all fifteen were re-measured at full width and the clause still holds |

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

**Closed 2026-09-03.** Both manifests pin `interpro_release: 109.0`, `pfam_release: 38.2`
and `panther_release: 19.0`, and all fifteen arms carry `uniprot`, so the clause derives from
an accession rather than from a hand-typed family list. **The question that blocked it is
answered by measurement, not by a ruling: adding a provenance field to a manifest moves no
frozen value.** `benchmark.freeze` builds `frozen.json` from six named keys and echoes no
other, and `derive` builds its record from named fields, so neither freeze moved by one byte.
`allo.inputs.load` rebuilds from an allow-list, so all five fields are redacted from the
prediction path by default, and a test asserts that rather than assuming it.

**Amended the same day, by round 4.** Pinning the release did not make the recorded lists that
release. They were RCSB per-entity assignments, which is a different quantity from the
accession assignment the clause resolves on, and a strict subset of it on all fifteen arms.
Both manifests now carry the accession-derived Pfam 38.2 sets, which resolves the `ns5b`
provenance note with them, and the clause's verdict is re-derived at that full width and holds.
See §1.6.

### 3.3 The occupant instrument is undefined — **closed 2026-09-03 by ADR 0044**

Clause (iii) says "no ligand of any kind" and clause (x) says "no apo component may contact a
scoreable label", and neither defines *ligand* or *component*. Water, glycerol, sulfate and PEG
have no declared side. The audit assembled the rosters eight published instruments actually
use and proposed a three-class procedure: `APO`, `APO_WITH_ADDITIVE_IN_POCKET`, `NOT_APO`.

**The three-class proposal is withdrawn, and the reason is a search rather than an opinion.**
A scoped literature review on 2026-09-03 looked for a published scheme with that middle class,
including under "pseudo-apo", "apo-like" and "quasi-apo". **None exists.** Every instrument in
the field is binary, and each folds the middle case into one of the other two: Wankowicz's
ten-heavy-atom floor and PocketMiner's five-species whitelist put it in apo; AHoJ puts it in
holo, deliberately, on the ground that a crystallographic agent perturbs local geometry
whatever its biological relevance. Inventing the class would have been a hyperparameter chosen
after seeing the data.

**The larger finding is that the annotation was never the instrument.** Clause (iii) and
clause (x) both decide from `apo.ligand`, a name-blind mask over every non-water heteroatom.
It is stricter than any roster in the survey, and it consults no vocabulary. So the benchmark's
apo-ness never rested on this judgement call, and what was wrong is that the annotation says
something false while reading as though it were the gate.

**What the classification is now, and on what.** `GOL`, `SO4` and `CL` are additives; the `K`
in `ecoli_cps` stays a state component. No published roster classes glycerol or sulfate as a
functional occupant. `1SUG`'s depositors publish it as apo in the title, with four ordered
waters in the catalytic pocket — and measured here, two of its four glycerols never reach the
motif site and the two that do graze one residue each. In a phosphatase sulfate is a positional
phosphate mimic that leaves the WPD loop open, so it does not produce the substrate-like state.
`1A9X` was grown from 0.65 to 1.35 M tetraethylammonium chloride. The potassium, by contrast,
is called "physiologically important" by the depositing laboratory.

**One case points the other way and is disclosed rather than acted on.** Measured here, the
`1IA8` sulfate contacts residues 54, 129, 153, 162, 164 and 166 — Chen 2000's Lys54, Arg129,
Thr153 and Arg162 plus Lys166 — and exactly one of the eleven motif residues. It sits in the
activation-segment phospho-cradle, not the ATP cleft, and for a kinase such a sulfate is
reported to support the active conformation of an unphosphorylated segment. That reading is
`[UNVERIFIED]`, the per-set vocabulary cannot express a per-arm class, and ADR 0044 records
what would settle it.

**The input layer was re-frozen and no number moved.** Twenty-one leaf changes across both
freezes, every one inside the occupant annotation, and zero outside it. The primary set changed
only its vocabulary.

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

### 3.5 The orthosteric vocabulary is not shared across the sets — **closed 2026-09-03 by ADR 0044**

Glycerol is a catalytic-state component on one set and unlisted on the other.

**Measured 2026-09-03, and the answer narrows the finding.** The vocabulary is a declared
allow-list that makes the freeze fail closed: `_orthosteric_state` raises if a component
contacting the active site is not named, so each set's list is forced to cover exactly what
that set observed. The two differ because the structures differ, and no classification
decision differs. What IS a decision, and an undeclared one, is that `additives` is **empty in
both sets**. The schema has a class for crystallisation additives and nothing has ever landed
in it, so glycerol in the PTP1B apo entry, sulfate in the MKP5 and CHK1 apo entries, and
chloride and potassium in both halves of `ecoli_cps` are all recorded as catalytic-state
components.

**Three things follow, each measured rather than argued.**

1. **No score, verdict or gate reads it.** `matches_apo` is written at `benchmark.py:281` and
   copied at `:422`; the only readers anywhere are two test assertions and one review tool.
   The three functions that read the input freezes from the scoring harness take
   `scoreable_label_residues`, `n_candidates`, `tier` and the target key set, and nothing else.
2. **No clause verdict depends on the bucket.** Clause (iii) and clause (x) both decide from
   `apo.ligand`, a name-blind mask defined at `structure/pdb.py:87`. Clause (vi) requires
   presence, not match. Clause (viii) reads the hand-declared `manifest.state.matched`, which
   `secondary/README.md` already says is independent of the derived field. The sulfate that
   puts clause (x) at its exact boundary on `mkp5` is the same object classed as a state
   component, and reclassifying it moves one and not the other, because the two instruments
   never touch.
3. **A re-freeze would move ten fields and no number.** `matches_apo` would flip on `mkp5`,
   `chk1` and `ptp1b`; `smyd3` keeps its verdict but moves two bucket lists; the primary set is
primary freeze moved exactly one leaf, `orthosteric_vocabulary.additives`, and no primary
   target moved, because neither component contacts a primary active site. One sentence in
   `secondary/README.md` would go stale, the one saying the derived and declared fields
   disagree on four arms.

So this is **not** a benchmark-validity defect and it does not block a result. It is the same
undeclared instrument as §3.3, seen from the vocabulary side, and **ADR 0044 settles both
together on 2026-09-03.** Both sets now carry the identical `additives` roster, so an arm added
later cannot be classed differently by accident.

**One further correction came out of the same review, and it is the sharper of the two.** The
`ptp1b` arm records `apo: WPD-loop open` and `holo: WPD-loop open`, `matched: true`. The
deposition paper's headline result is that the apo WPD loop is **closed**. Measured here as the
Asp181 carboxylate to Cys215 sulfur distance, with the arm's own holo as the control: `1SUG`
**6.52 A**, `1T48` **12.62 A**. A 6.1 angstrom separation on one arm. Both strings were wrong
and the halves do not match. Clause (viii) discloses state and never gates on it — three
admitted arms already carry `matched: false` — so the arm stays and nothing is re-admitted.

### 3.6 What N supports, stated honestly — **closed 2026-09-03**

N = 5 cannot support a generalisation claim. **The floor this section asserted had no
derivation anywhere in the repository**, which is the defect it was complaining about. Both
floors are now computed, by `scipy.stats.binomtest` against p = 0.5, one-sided: a clean sweep
needs **N >= 6** to survive a two-way correction (p = 0.0156), and tolerating one failure needs
**N >= 8** (p = 0.0352, against 0.0625 at N = 7). The achieved N = 5 clears neither.
`secondary/README.md` §6 states both.

### 3.7 Smaller, and each measured

- ~~Add `cardiac_myosin_mandated` to `clause-ix-both-sets.json`~~ **done 2026-09-03.** Measured from the tracked `9GZ2` copy: the `XB2` protein lining at 4.5 angstrom is 12 residues, all in chain A, so clause (ix) passes. ADR 0031 gives both myosin arms the same holo, so the two entries agree, and this one was measured rather than entailed. The file now holds fifteen arms and all fifteen pass.
- ~~Say in `evaluation/README.md` that the sealed tier is fully materialised in
  `frozen.json`~~ **done 2026-09-03**, §9. It names the two partial enforcements and says that
  neither stops a person reading the file, and that no test can.
- ~~Pin the primary set's (x), (xi) and (xii) verdicts in a test~~ **done 2026-09-03.** All
  three re-derive from the freeze and the tracked mmCIFs, and every number in the README
  reproduces: two of nine entries fail their method's resolution ceiling, `1OPL` at 3.42 and
  `5TBY` at 20.00. Closing it found the predicted defect: `tests/test_secondary.py` justified
  a live assertion with "`bcr_abl1_mandated` proves it: 16 labels contacted by myristate". That
  arm contacts **zero** labels, and the 16 was read off a field whose units are angstroms. The
  comment also printed a real label residue number. Both corrected. The assertion is live and
  sits at its boundary on three arms.
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
