# 0015 — Every residue this benchmark labels leaves the background, whichever arm labelled it

**Status:** accepted · 2026-08-20

## Context

ADR 0011 removed the propagation source and **sibling functional sites** from the scoring
universe, on the reasoning that a residue this benchmark itself calls a functional site is
not a negative — scoring it as one "penalises a method for being right about biology we
curated". It then drew the sibling boundary in two places that its own reasoning does not
support, and an adversarial review found both.

**It excluded siblings by `site_id`, so the same site under a different effector stayed in
the background.** ADR 0011 says in as many words: "Two arms on the _same_ site with different
effectors (Site 1 under XB2 and under 2OW) are not siblings." `8QYP`:A freezes Site 1 under
both. Under omecamtiv the pocket contacts residues 146, 147, 160, 170, 492 and 771 that
mavacamten does not reach; under mavacamten it contacts 120 and 163 that omecamtiv does not.
Each set scored as false positives in the other arm. One ligand's contact footprint is not
the pocket — it is one sample of it — and a method that recovers the broader functional site
was marked wrong for doing so.

**It confined the rule to one apo entry, which excused the arm that matters most.** The
mavacamten confirmatory arm is on `9GZ3` and the omecamtiv arm on `8QYP`, so an entry-local
rule never reached the confirmatory family at all. Sibling Site 2 labels were likewise
excluded from the three arms sharing `8QYP` and left in the background of every myosin arm
that does not.

The reason the rule stopped at the entry boundary is real: **author numbering is not
comparable across entries.** This benchmark contains its own counterexample — `1OPL` is ABL1
1b numbering and `2G1T` is 1a. Comparing the integers directly would have excluded the wrong
residues. That is an argument for mapping them, not for leaving them.

Found by an adversarial review (Codex, `gpt-5.6-sol`), round 4. Its residue lists were wrong
in both directions — it named five omecamtiv-only residues where there are six, and
attributed 120 and 163 to an arm whose label set does not contain them — but the mechanism it
described is real and is the one repaired here.

## Decision

**Amended after round 5: the exclusion authority is an explicit per-protein functional-site
registry in `manifest.yaml`, not the union of arms currently curated. This was Claude's
call.** The former implementation made one arm's candidate universe depend on how many
sibling arms existed. Adding one novel Site 2 label moved the already-frozen Site 1 universe
from 716 to 715 candidates. MYH7 has six arms, ABL1 four and KRAS two, so union-over-arms gave
more richly curated proteins a cleaner negative class — the fairness asymmetry this freeze
is supposed to prevent.

1. Each protein declares one reference apo entry and one sorted functional-residue set under
   `functional_sites`. A residue in that registry leaves an arm's negatives unless it is a
   positive for that arm. Each arm retains its own effector-defined positive set.
2. Registry residues are carried from the reference entry to another entry by
   `align_numbering`, never integer equality. The ABL1 1a/1b numbering split remains the
   concrete reason.
3. Adding an arm does not edit the registry and therefore cannot move any existing universe.
   Changing biological site knowledge is a manifest edit plus re-freeze, visible in review.
4. The registry is scoped by `protein`; `site_id` and free-text `site` gate neither mapping
   nor exclusion.

## Alternatives recorded for challenge

- **Accept and disclose the arm-dependent union.** Rejected because disclosure does not
  remove the cross-protein fairness asymmetry.
- **Make the whole-node universe primary and candidate-set scoring a sensitivity.** Rejected
  here because it restores active-site and known functional residues as false negatives for
  connectivity methods (ADR 0011). It remains the mandatory reported sensitivity and should
  be challenged again if the registry itself proves too judgement-laden.

## Consequences

- Four myosin arms lose background residues, and the confirmatory one loses the most:
  `cardiac_myosin_site1_corrected` 743 → **716** candidates, `_sensitivity_srx` 886 → **861**,
  `_sensitivity_xray` 664 → **659**, `_omecamtiv` 664 → **662**. No KRAS or ABL1 arm moves —
  each of those proteins has one frozen site and the labels already agree across its arms.
- **The chance line rises on every arm that moved**, because a smaller universe makes a random
  top-5 more likely to hit. The baselines got harder, which is the correct direction.
- `freeze()` maps one explicit registry per protein; it never reads sibling labels to define
  an existing arm's universe.
- **The exclusion still never touches the input** (ADR 0011 clause 3). A method receives the
  whole admitted node set; this is a scoring-universe rule.
- Guarded by `test_same_site_labels_are_not_negatives_in_a_sibling_arm` and
  `test_an_added_arm_cannot_move_an_existing_candidate_universe`.
- Amends ADR 0011, which stated this rule and drew its boundary two places short.
