# 0011 — Residues that score by construction leave both classes, not just the positives

**Status:** accepted · 2026-08-20

## Context

ADR 0007 removed propagation-source residues from the **positive** class, on a rule
published in this field: AlloPred's "Active site residues were not counted as being in any
pocket … in order to avoid direct perturbation of the site at which the effect was
measured" ([10.1186/s12859-015-0771-1](https://doi.org/10.1186/s12859-015-0771-1)).
`docs/benchmark/README.md` §5 states the reason in its own words — such a residue "scores
maximally by construction and therefore measures nothing".

It then left them in the **negative** class. `src/allo/benchmark.py` computed every
baseline against `n_residues`, the whole node set, with only the scoreable labels as
successes. The reason given for removing a residue from the positives applies with equal
force to keeping it as a negative, and nobody noticed for the same reason nobody notices
any self-consistent argument: the two halves were written in different paragraphs.

**It is not a neutral half-measure. It is a per-method-class handicap.** The challenge asks
for "a ranking of residues based on their dynamic connectivity — in most cases, connectivity
**to an active site**" (`CHALLENGE.md` §4.1). A method that computes that ranks the active
site at the top; that is not a flaw in the method, it is the quantity. Every one of those
residues then scores as a false positive. A geometric pocket detector has no such tendency
and takes no such hit. Simulated at a fixed real effect (d = 1.2, 400 draws, identical
signal, the only difference being whether the method also ranks the source set high):

| arm                              | AUC-ROC geo → conn | AUC-PR geo → conn | AUC-PR lost |
| -------------------------------- | ------------------ | ----------------- | ----------: |
| `kras_g12c_mandated`             | 0.799 → 0.679      | 0.386 → 0.146     |    **62 %** |
| `bcr_abl1_corrected`             | 0.799 → 0.765      | 0.314 → 0.165     |    **47 %** |
| `cardiac_myosin_site1_corrected` | 0.809 → 0.787      | 0.146 → 0.057     |    **61 %** |

The active site is 2.4–13.6 % of the node set depending on arm; on KRAS it is 23 of 169
residues. An input layer that costs one method class half its retrieval score before any
method exists is not neutral, which is the one thing the freeze is for.

The benchmark already knew this. §5's decoy rules exclude the active site from the second
negative set, and say why in as many words: "it is a pocket, it does not overlap the true
site, and a connectivity-to-active-site score ranks it top by construction". The primary
background was never brought into line.

Found by an adversarial review (Codex, `gpt-5.6-sol`), not by us.

## Decision

1. **The scoring universe is the candidate set, not the node set.** A residue is excluded
   from **both** classes — never scored, never counted in `N` — when it scores by
   construction rather than by evidence. Two grounds, both frozen:
   - **The propagation source.** Every residue of the frozen active site (ADR 0005). Set
     membership, not distance — the same rule ADR 0007 already applies to the positives.
   - **Sibling functional sites.** Residues this benchmark itself labels as a _different_
     functional site on the same apo entry and chain. On `8QYP`:A we freeze both myosin
     Site 1 and Site 2; scoring Site 1 with Site 2's residues as negatives penalises a
     method for being right about biology we curated. §5 already excludes sibling sites
     from the decoys; the background now agrees. Two arms on the _same_ site with different
     effectors (Site 1 under XB2 and under 2OW) are not siblings.
2. **`n_candidates` and `excluded_from_scoring` are frozen per arm** in `frozen.json`, and
   every hypergeometric baseline, prevalence and simulated AUC in §5 is computed on them.
   The node set `n_residues` stays frozen and reported: it is what a method _receives_
   (ADR 0010), and the two are different quantities that were previously one.
3. **The exclusion never touches the input.** A method still receives the whole modelled
   chain, active site included — it needs the source set, that is what it propagates from.
   This is a scoring-universe rule, not a node-set rule.
4. **Adding a ground for exclusion is a manifest change plus a re-freeze**, never a filter
   applied when a result is read.

## Consequences

- **Every §5 number moved.** KRAS `P(≥1 hit)` 0.396 → **0.445**, ABL1 corrected 0.292 →
  **0.302**, myosin Site 1 corrected 0.076 → **0.078**; scoreable prevalence rises on every
  arm (KRAS 9.5 % → **11.0 %**). The baselines got _harder_, which is the correct direction:
  a smaller universe makes a random top-5 more likely to hit.
- The three `8QYP` arms lose 20–23 further residues to the sibling rule, so myosin Site 1's
  x-ray arm and Site 2 are now scored on 659 and 662 candidates against 706 nodes.
- **This is the last moment it was cheap.** It changes the chance line for every claim the
  report will make. Done after a method had been scored, it would have been indistinguishable
  from moving the goalposts.
- Guarded by `test_the_scoring_universe_excludes_what_scores_by_construction` and
  `test_sibling_functional_sites_leave_the_background`, so the two halves of the rule cannot
  drift apart again.
- **Open:** the ASD selection set will contain proteins with several curated sites and no
  `site` field to separate them. The sibling rule needs a general form before that set is
  frozen (ROADMAP 1.7).
- Amends ADR 0007, which stated the positive-class half of this rule and stopped there.
