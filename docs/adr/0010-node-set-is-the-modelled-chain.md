# 0010 — The frozen node set is the modelled chain, not a trimmed catalytic domain

**Status:** accepted · 2026-08-20 (proposed and accepted the same day by the PI)

## Context

`allo.inputs.apo_input()` returns `residues = every modelled residue of the selected
chain`, and `frozen.json`'s `n_residues` is the same set. No domain trimming happens
anywhere. That choice was never recorded — it was inherited from the first implementation —
and it is load-bearing, because N determines label prevalence, the hypergeometric top-5
baseline, and AUC-PR. **Refined by ADR 0011:** the denominator of all three is the smaller
`n_candidates` — N minus the propagation source and the protein's functional-site registry.
N is what a method *receives* and still bounds everything downstream, but it is not itself
the denominator any more.

Two things make it worth an ADR rather than a code comment.

**First, C5.** `CHALLENGE.md` §5 says "**Included:** the **catalytic domains** of the
proteins." Read strictly, a 451-residue SH3–SH2–kinase construct is not a catalytic domain.
Read in context — the same sentence's exclusions are waters, cofactors and PTMs — it is
scoping the _system_ rather than prescribing a domain boundary within a chain. The repo has
been operating on the second reading without saying so.

**Second, it makes arms of the same target unequal.** Measured spans of the frozen apo
chains:

| arm                    | apo    | span    |   N | contents                          |
| ---------------------- | ------ | ------- | --: | --------------------------------- |
| `bcr_abl1_mandated`    | `1OPL` | 81–531  | 451 | SH3 + SH2 + linker + kinase       |
| `bcr_abl1_corrected`   | `2G2H` | 252–523 | 272 | kinase domain only                |
| `bcr_abl1_sensitivity` | `2G1T` | 232–502 | 271 | kinase domain only (1a numbering) |

The mandated ABL1 arm carries roughly **179 extra non-catalytic residues**. That alone
moves scoreable prevalence from 6.6 % to 4.4 % and the top-5 baseline P(≥1 hit) from
**0.292 to 0.204**. `docs/benchmark/README.md` presently attributes the mandated arm's
harder baseline to nothing in particular; most of it is construct extent, not the myristate
defect the tier exists to expose. The same effect is smaller but present on myosin, where
`9YRG` models to residue 943 and `8QYP` stops at 780 (N = 912 against 706).

## Decision

1. **No domain trimming. The node set is every modelled residue of the frozen chain.**
   Three reasons, in order of weight:
   - **The severed contacts are real.** Under the elastic network hypothesis (C6) the
     contact topology _is_ the model. Cutting a domain boundary deletes contacts that exist
     in the deposited structure and changes the network spectrum — it does not neutrally
     "focus" the model.
   - **On ABL1 the excluded domains are the mechanism.** The SH3–SH2 clamp is how myristate
     binding inhibits the kinase. Trimming to the kinase domain would delete the coupling
     path the benchmark is asking a method to find.
   - **A domain boundary is a knob.** There is no canonical residue at which the SH2 domain
     ends. Any number we pick becomes a hyperparameter that could later be moved to flatter
     a result, which is precisely what freezing the input layer is for.
2. **The consequence is disclosed, not absorbed.** N and its span are reported per arm, and
   any comparison of baselines _across arms of the same target_ must say how much of the
   difference is construct extent. Specifically, the mandated-vs-corrected ABL1 baseline gap
   is not evidence about the myristate defect.
3. **Cross-arm difficulty comparisons use the per-arm chance line**, never a shared one.
   This is already how `docs/benchmark/README.md` §5 reports the hypergeometric table; this
   ADR states the reason it has to be.
4. **If trimming is ever adopted**, it is a manifest field with an explicit residue range per
   arm and a re-freeze — never an implicit default inside loading code.

## Consequences

- **Primary-arm numbers did not change when this decision was accepted.** The later strict-C5
  sensitivity arm adds a second, explicitly ranged view of `1OPL`; it does not trim the
  mandated arm silently.
- **Accepted by the PI.** The strict reading of C5 — trim to the catalytic domain — was the
  live alternative and is now declined. Adopting it would have shrunk the ABL1 mandated arm by
  ~40 % and changed every ABL1 baseline, and on that arm it would have deleted the SH3–SH2
  clamp, which is the mechanism the myristoyl pocket acts through. Reopening this is a
  manifest change plus a re-freeze, not a code default.
- **Enforced, not just recorded.** `tests/test_benchmark.py::test_methods_and_the_benchmark_agree_on_the_node_set`
  asserts that what `apo_input` hands a method is exactly the `n_residues` the benchmark
  scores against. **The two paths are not as independent as this bullet claimed**: both call
  `allo.inputs.admitted_residue_numbers`, so they agree by construction on the node set itself.
  What the test genuinely catches is a divergence introduced *after* that call — trimming added
  to either loading path, or a modelled residue without a Cα, since `derive` additionally
  requires one and `apo_input` does not. That is narrower than "computed independently", and it
  is what the test is worth. Flagged by adversarial review 2026-08-21.
- **The SH3–SH2 argument above does not reach the arm that carries the ABL1 claim, and that
  has to be said plainly.** Reason 2 of the decision — trimming would delete the coupling path
  — protects `bcr_abl1_mandated` (`1OPL`:A, 81–531, SH3 + SH2 + linker + kinase). But the
  claim-bearing arm is `bcr_abl1_corrected` (`2G2H`:A, **252–523**) and the robustness arm is
  `bcr_abl1_sensitivity` (`2G1T`:A, **232–502**); both are kinase-domain-only constructs in
  which SH3 and SH2 were never deposited. No trimming policy could have removed them, and no
  policy can put them back. Two consequences, and the ADR asserts neither over the other:
  either the clamp is less necessary to locating the pocket than reason 2 implies, or the
  claim-bearing arm is asking a method to find the myristoyl site with the mechanism that
  makes it allosteric absent from the input — in which case that arm is harder than this ADR's
  reasoning suggests, for a cause this ADR itself names. What is *not* legitimate is quoting
  reason 2 as if it applied to the whole target. It applies to the descriptive arm only.
- A reviewer applying C5 strictly will ask about `1OPL`'s SH3–SH2. The organiser question is
  still open, but the experimental follow-up is built: `bcr_abl1_trimmed` uses the same
  `1OPL`:A bytes with explicit `apo.residue_range`. UniProtKB P00519 release 2026_02 supplies
  canonical kinase residues 242–493; the manifest pins the P00519-1/P00519-2 substitution,
  code derives the deposited +19 offset, verifies boundaries 261–512 exist, and freezes 252
  admitted nodes. This reports both C5 readings without replacing the accepted primary arm.
- **The trim is not label-neutral, and that is the sharpest argument for decision 1.**
  Deposited 513–531 lies outside the annotated domain and carries labels 521, 525 and 529, so
  the arm freezes **17 positives against the mandated arm's 20** (`labels_outside_node_set` in
  `frozen.json`). A mandated-vs-trimmed baseline gap mixes scope with a 15 % smaller positive
  set and must not be read as a scope effect alone. Applied to `1OPL`, the strict reading of
  C5 does not merely drop scaffolding — it deletes part of the myristoyl pocket itself.
  Guarded by `test_every_arm_accounts_for_the_labels_it_does_not_score`.
- The ASD selection set will contain multi-domain proteins where this bites harder than it
  does on three hand-picked targets. Revisit before that set is frozen (ROADMAP 1.7).
