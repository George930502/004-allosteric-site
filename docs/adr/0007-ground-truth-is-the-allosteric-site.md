# 0007 — Ground truth is the allosteric site; crypticity is a difficulty axis

**Status:** accepted · 2026-08-20

## Context

The frozen benchmark was assembled with the cryptic-pocket literature as its
definitional backbone — AHoJ for apo/holo pairing, CryptoBench and CryptoSite for what
counts as a real pair, PocketMiner for what counts as a hard one. That machinery is
sound; it answers a different question.

`CHALLENGE.md` is unambiguous about which question. The deliverable "identifies
potential **allosteric sites**" (line 22); the primary objective is accuracy "in
identifying experimentally validated **allosteric sites**" (line 65); the scored
criterion is overlap with "known **distal regulatory residues**" (lines 71, 152); the
submission is a "top 5 predicted **allosteric sites**" list (line 97); the method is
framed as an "**allosteric scanner**" upstream of classical screening (line 46). The
word "cryptic" appears three times, twice inside the compound phrase "cryptic/allosteric
binding sites" and once in a reference title. Line 119 states the selection rationale
outright: these are targets "historically considered undruggable **until a specific
allosteric pocket was characterized**".

The two properties are orthogonal, and the literature is explicit about it:

- Of 19 validated cryptic sites, **8 are allosteric** — the majority are not
  (Vajda et al., _Curr Opin Chem Biol_ 2018;44:1-8, doi:10.1016/j.cbpa.2018.05.003).
  Precisely: 19 table rows over 18 distinct proteins, 8 typed allosteric.
- Roughly **30 % of catalogued allosteric sites overlap or border the catalytic site**
  (CASBench, doi:10.32607/20758251-2019-11-1-74-80) — so distance from the active site is not
  definitional either.
- Allosteric sites are frequently **pre-formed** in the apo state, which is precisely
  the case a crypticity test rejects.

Under the crypticity lens `docs/benchmark/README.md` §4 tabulates several arms as
failing a 2 Å pocket-lining floor. That floor is CryptoBench's entry criterion for a
cryptic-site benchmark. Applied here it imports a pass/fail test from a different task
and would discard valid allosteric pairs for the sin of having an open pocket.

## Decision

1. **The ground-truth concept is the allosteric site.** A pair earns its place by the
   holo member containing an effector at a site that is _functionally coupled to the
   active site_, evidenced by cited experiment. Nothing else is an entry criterion.
2. **Crypticity is measured, reported, and never scored.** Ligand-transplant clash count
   and pocket-lining RMSD stay in `frozen.json` as a per-target **difficulty axis** — a
   pre-formed site is an easier prediction, and a benchmark that cannot say which of its
   targets were easy cannot interpret its own aggregate. There is no threshold and no
   pass/fail.
3. **A pre-formed allosteric site is a valid target.** It is not a defect and is not
   recorded as one.
4. **Proximity to the active site is not a validity criterion either.** Where a distance
   cutoff appears it is a guard against a metric ranking residues by the very quantity
   it was given (`scoreable label set`, CONTEXT.md), never a claim about which residues are
   allosteric.
5. **The settled vocabulary lives in `CONTEXT.md`** and is used consistently in code,
   docs and report. "Cryptic site" is never written where "allosteric site" is meant.

## Consequences

- **No _label set_ changes.** Label sets are geometric effector footprints and are
  unaffected: coordinates, chains, residue counts and label residues all stand. What changes
  is the _entry criterion_ and the _framing_ — which is why this is cheap to do now and
  expensive after the report is written.
  **Correction, same day:** an earlier draft of this bullet said "no frozen number changes"
  and "the eight arms". Both became wrong once the work this ADR authorises was carried out.
  `frozen.json` gained `scoreable_label_residues` in place of `distal_label_residues` (KRAS
  14 → 16), a rewritten `apo_site_occupancy`, `labels_beyond_angstrom` in place of
  `distal_by_threshold`, and `holo_site_occupancy`; and that freeze had **ten** scoreable
  arms, not eight, because ADR 0008 added myosin Site 2 and the omecamtiv sensitivity arm.
  ADR 0010's later strict-C5 sensitivity adds an eleventh scoreable arm without changing the
  underlying label definition. The claim that survives is the one about label sets.
- `docs/benchmark/README.md` §1 must be re-anchored on the allostery literature rather
  than the cryptic-pocket literature, and §4's pass/fail table recast as a difficulty
  table. Tracked as the work this ADR authorises.
- **The negative sets need re-derivation.** "Surface pockets that are not the answer" is
  a structural decoy class built for a structural ground truth. Under a functional
  ground truth the decoy must be _a pocket with no demonstrated coupling to the active
  site_, which is a stronger and rarer claim than "no ligand was crystallised here".
  Deferred to the evaluation layer, where the negative sets are defined.
- **Unchanged and explicitly still in force:** ADR 0004 (residue identity by alignment),
  ADR 0005 (active site as a rule), ADR 0006 (cofactors as nodes), constraint C1 and the
  leakage machinery in `tests/test_no_leakage.py`. None of them depended on the cryptic
  framing.
- Accepting this closes off the cheapest available shortcut: choosing pairs by how
  visibly the pocket opens. That shortcut correlates with allostery only weakly, and a
  benchmark built on it would have measured pocket detection while claiming to measure
  allosteric prediction.

## Amendment, 2026-08-20 (ADR 0011)

This ADR removed propagation-source residues from the **positive** class and stopped there,
leaving them in the negative class. That is not neutral: it costs a connectivity-to-active-site
method 44–62 % of its AUC-PR at a fixed real effect and costs a geometric detector nothing.
The reason given here — such a residue "scores maximally by construction and therefore
measures nothing" — removes it from **both** classes. Superseded on that point by
[ADR 0011](0011-scoring-universe-is-the-candidate-set.md); everything else here stands.

---

**Amendment, 2026-08-24 — the four-complex problem, stated.** A stronger version of this
ADR's reasoning is available and should be quoted in the report. Fenton: allostery "is more
strictly defined in functional terms as a comparison of how one ligand binds in the absence,
versus the presence, of a second ligand … a study of allostery must consider **four complexes
and not just two**" (doi:10.1016/j.tibs.2008.05.009; restated in McCullagh 2024,
doi:10.1016/j.jbc.2024.105672). An apo/holo pair supplies one corner of that cycle. No
structural benchmark in the field implements the requirement, which is exactly why the
allostery must be inherited from the cited functional experiment and never read off the
coordinates. `docs/benchmark/evidence/allosteric-pair-audit.md` §0 shows what that looks like
in practice on these five arms: not one of them isolates an active-site response
attributable to the effector.

Authority for the definition itself is IUPHAR XC (doi:10.1124/pr.114.008862), which is
retrievable via PMC11060431 and was previously recorded here as unreachable. It requires the
site to be "nonoverlapping and spatially distinct from, but **conformationally linked to**,
the orthosteric binding site", and recommends reserving the word for cases where
"**reciprocity in this interaction can be demonstrated**". That is stricter than ASD's
three-experiment rule and is the sharpest statement that spatial separation is not sufficient.
