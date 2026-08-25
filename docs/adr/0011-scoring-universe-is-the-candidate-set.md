# 0011 — Residues that score by construction leave both classes, not just the positives

**Status:** accepted · 2026-08-20

## Context

ADR 0007 removed propagation-source residues from the **positive** class under this
repository's anti-circularity policy. AlloPred is a methodological analogy: its
spring-perturbation procedure did not count active-site residues in candidate pockets, to
avoid perturbing the site where the effect was measured
([10.1186/s12859-015-0771-1](https://doi.org/10.1186/s12859-015-0771-1)); it did not define a
benchmark universe.
`docs/benchmark/primary/README.md` §5 states the reason in its own words — such a residue "scores
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
   - **Registered functional sites.** Residues in the explicit per-protein registry amended
     by ADR 0015. Scoring one functional site with another as negatives penalises a method
     for being right about biology we curated. The registry is independent of the number of
     arms, and the background and decoy rules use the same authority.
2. **`n_candidates` and `excluded_from_scoring` are frozen per arm** in `frozen.json`, and
   every hypergeometric baseline, prevalence and simulated AUC in §5 is computed on them.
   The node set `n_residues` stays frozen and reported: it is what a method _receives_
   (ADR 0010), and the two are different quantities that were previously one.
3. **The exclusion never touches the input.** A method still receives the whole modelled
   chain on primary arms, or the explicit manifest-admitted range on a scope sensitivity,
   active site included — it needs the source set, that is what it propagates from. This is a
   scoring-universe rule, not a node-set rule.
4. **Adding a ground for exclusion is a manifest change plus a re-freeze**, never a filter
   applied when a result is read.

## Consequences

- **Every §5 number moved.** KRAS `P(≥1 hit)` 0.396 → **0.445**, ABL1 corrected 0.292 →
  **0.302**, myosin Site 1 corrected 0.076 → **0.078** (**0.081** once
  ADR 0015 widened the rule); scoreable prevalence rises on every
  arm (KRAS 9.5 % → **11.0 %**). The baselines got _harder_, which is the correct direction:
  a smaller universe makes a random top-5 more likely to hit.
- The current registry-backed counts include
  `_sensitivity_xray` **659**,
  `_omecamtiv` **662** and
  `site2_corrected` **662**, against 706 nodes.
- Because the exclusion is this repository's policy rather than a published benchmark rule,
  every confirmatory result is also reported over the whole node set with the same scoreable
  positives. `allo benchmark stats` regenerates both chance lines under
  `scoring_universe_sensitivity`; the candidate set remains primary.
- **This is the last moment it was cheap.** It changes the chance line for every claim the
  report will make. Done after a method had been scored, it would have been indistinguishable
  from moving the goalposts.
- Guarded by `test_the_scoring_universe_excludes_what_scores_by_construction` and
  `test_same_site_labels_are_not_negatives_in_a_sibling_arm`, so the two halves of the rule cannot
  drift apart again.
- The same explicit registry form applies when the ASD selection set contains several sites.
- Amends ADR 0007, which stated the positive-class half of this rule and stopped there.
- **Amended in turn by ADR 0015.** The first amendment replaced the entry-local `site_id`
  boundary with a same-protein union carried across entries. Round 5 found that union still
  made an arm depend on how many siblings were curated. ADR 0015 now replaces the union with
  an explicit per-protein functional-site registry, still carried across entries by
  alignment. Adding an arm cannot move another arm's universe.

---

**Amendment, 2026-08-24.** The **propagation-source** half of this decision stands unchanged
and is what `excluded_from_scoring` implements. The **sibling functional site** half is
withdrawn with [ADR 0015](0015-same-site-labels-leave-the-background.md): after the arm
reduction each protein carries one site, the registry that implemented it was measured to be
a no-op on all five arms, and it was removed. On the current freeze
`excluded_from_scoring == active_site` and `n_candidates == n_residues - len(active_site)`.
