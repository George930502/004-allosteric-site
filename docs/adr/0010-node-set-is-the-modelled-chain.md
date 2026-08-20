# 0010 — The frozen node set is the modelled chain, not a trimmed catalytic domain

**Status:** proposed · 2026-08-20

## Context

`allo.inputs.apo_input()` returns `residues = every modelled residue of the selected
chain`, and `frozen.json`'s `n_residues` is the same set. No domain trimming happens
anywhere. That choice was never recorded — it was inherited from the first implementation —
and it is load-bearing, because N is the denominator of label prevalence, of the
hypergeometric top-5 baseline, and of AUC-PR.

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

- **No frozen number changes.** This records what the benchmark already does, which is why
  it is cheap now and expensive after the report quotes an N.
- Status is **proposed**, not accepted: the strict reading of C5 is a live alternative, and
  adopting it would shrink the ABL1 mandated arm by ~40 % and change every ABL1 baseline. The
  choice belongs to the principal investigator, and leaving it unrecorded was the one option
  with no defence.
- A reviewer applying C5 strictly will ask about `1OPL`'s SH3–SH2. The answer is here rather
  than improvised.
- The ASD selection set will contain multi-domain proteins where this bites harder than it
  does on three hand-picked targets. Revisit before that set is frozen (ROADMAP 1.7).
