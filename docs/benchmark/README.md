# The frozen benchmark

**Status: input layer and positives frozen 2026-08-20. The negatives are not, and until
they are, no method may be scored here.** Every method receives identical structures,
identical residue sets and identical labels, pinned to the byte — `apo_input` refuses a file
whose sha256 is not the frozen one. What is *not* yet fixed is the second negative class the
challenge requires (§4.1: enrichment against "non-functional surface pockets") and the
calibration of the patch null. Both are listed in §7 with the gate they have to clear.

An earlier version of this line said "identical negatives", which was not true and would have
left the pocket detector's configuration, surface definition and merging rules choosable
*after* methods had been seen — the exact tuning surface freezing exists to close. **Scoring
gate: `allo benchmark verify` clean, decoy artifacts committed, and the null calibrated
(§5) — all three, before any method's number is quotable.**

```bash
uv run allo benchmark show      # what is frozen, derived live from the deposited files
uv run allo benchmark verify    # exit 0 iff nothing has moved since the freeze
```

| File            | What it is                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| `manifest.yaml` | the choices — entries, chains, ligands, cutoffs, active sites. Hand-edited.                                  |
| `frozen.json`   | the consequences — residue counts, label sets, scoreable label sets, geometry. Generated; never hand-edited. |
| `audit/`        | forensic dossier per target pair, every fact carrying its provenance                                         |
| `evidence/`     | literature basis — eleven reviews, indexed in [`evidence/README.md`](evidence/README.md). Every non-derived claim below traces to one |

---

## 1. What an apo/holo pair is, operationally

"Apo" is used loosely in this literature, and the looseness is exactly what lets a broken
benchmark through. Three readings circulate: ligand-free of _anything_; ligand-free _at the
site of interest_; ligand-free _with respect to the drug under study_. They give different
answers for every target here — `4OBE` holds GDP·Mg, `9GZ3` holds ADP·Mg·Pi, and both are
routinely called apo.

**We adopt the site-apo reading, made operational.** The clauses below are the allostery
field's own, assembled from the sources that build allosteric-site datasets rather than from
the cryptic-pocket literature — the distinction matters, because a cryptic site is a
structural property and an allosteric site is a functional one, and most validated cryptic
sites are not allosteric (ADR 0007). Full clause-by-clause traces with quotes:
[`evidence/allosteric-pair-definition.md`](evidence/allosteric-pair-definition.md).

> An **apo/holo pair for allosteric-site prediction** is an ordered pair of experimentally
> determined structures of the same gene product satisfying:
>
> **(i) Effector.** The _holo_ member contains the allosteric effector, identified by its PDB
> chemical component ID, at the site to be predicted; site residues are those within a
> **declared** radius of its heavy atoms.
> **(ii) Provenance of label.** The site is allosteric because _functional_ evidence says so.
> Distance from the active site is neither necessary nor sufficient. (ASD v1 pairs the
> functional requirement with a _topographic_ one — the site must be "topographically distinct
> from the orthosteric functional site" — so this clause narrows ASD rather than restating it,
> and it does so because ~30 % of CASBench's allosteric sites border the catalytic site.)
> **(iii) Site-apo.** The _apo_ member contains **no ligand of any kind within the
> _scoreable_ portion of that site** — the labels a method is actually asked to find. Contacts
> to the full label set are recorded beside it and do not disqualify: where the allosteric and
> orthosteric sites share a border, the catalytic cofactor touches labels that are *themselves*
> active-site residues, which is two sites adjoining, not a modulator in the pocket.
> **(iv) Identity.** Same protein at **≥ 90 % sequence identity**, differences enumerated.
> **(v) Assembly.** Same oligomeric state. (The second half of this clause — that the modelled
> state should _be_ the biological assembly — is **ours**; Amor supplies same-oligomeric-state
> and Wu supplies the multimer-fragment caution, but no source states it.)
> **(vi) Second site.** Orthosteric occupancy recorded for **both** members, and the
> active-site rule stated.
> **(vii) Non-circularity.** The propagation source must not be perturbed by the site being
> predicted.
> **(viii) State disclosure.** The functional state of each member is **stated**, and the
> pocket-lining change reported. State difference is _disclosed, not required_.
> **(ix) Blindness.** A comparator trained on ASD/ASBench/CASBench, evaluated on a target
> those databases curate, **is not blind**, and must be labelled.

Where each clause comes from, and it is worth naming because none of it is ours:

| Clause     | In-domain source                                                                                                                                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| (i) radius | ASD v2.0 **6 Å** ("residues … automatically extracted … by 6 Å around allosteric modulator"); CASBench **5 Å** (verbatim). Two weaker entries, marked because they are often quoted as peers of the first two: **ASBench 4 Å** is _not_ in ASBench's paper — it is Wu et al.'s reading of ASBench's files, its construction rules being in the paywalled SI; and **Amor 3.5 Å** is a caspase-1 result ("residues within 3.5 Å of the allosteric **site** of caspase-1"), not a set-wide convention. Our 4.5 Å matches none exactly and is declared at first use |
| (ii)       | ASD v1 requires "at least three cases of experimental evidence … inactive mutation of allosteric residue, cooperativity of kinetic effect from two ligands and uncompetitive-binding assay"                                          |
| (iii)      | ⚠️ **borrowed, and narrowed by us twice.** ASD's "apo" is _modulator_-relative; no allostery source states the site-relative reading. The **scoreable-portion** qualifier is ours too — it is the only reading under which a benchmark that deliberately keeps proximal labels (ADR 0007) can have any site-apo clause at all, since the cofactor would otherwise disqualify every arm whose sites adjoin. Both narrowings are stated rather than assumed; see the paragraph below |
| (iv)       | ESSA — "at least 90% sequence identity". The field's **only** published pairing threshold                                                                                                                                            |
| (v)        | Amor et al. exclude on "a mismatch between the oligomeric state of the active and inactive structures"; Wu et al. flag ASBench entries that are one part of a multimer "where the effect of cooperativity might play a crucial role" |
| (vii)      | AlloPred — "Active site residues were not counted as being in any pocket … in order to avoid direct perturbation of the site at which the effect was measured"                                                                       |

**Clause (viii) is disclosure-only on purpose.** Requiring an apo↔holo conformational change
would exclude dynamic allostery by construction — allostery can proceed purely through
fluctuation entropy with no mean-coordinate signature. No allostery source states a
requirement in either direction; the only state-aware criterion in the reviewed corpus is
Amor's oligomeric one. So pocket-lining change is reported as a diagnostic and never used as
an inclusion filter.

**Clause (iii) is checked over the scoreable set, and an earlier version of this document
said "no ligand of any kind within that site" while the code checked the narrower thing.**
The wording is now what `derive()` does. The narrowing is defensible — on `4OBE` the five
contacted labels are all active-site residues, so the clause would otherwise reject a pair
for the very geometry ADR 0007 chose to keep — but it uses a *scoring* construct to make a
*structural* admission, and that is worth seeing rather than discovering. The full-set counts
stay in the table below so the decision can be re-litigated on the numbers. `1OPL` fails on
either reading: none of its 16 contacted labels is an active-site residue.

**Selecting the apo entry is not blind to the answer, and that is fine — but the bias runs
in both directions and an earlier draft claimed only one.** Clause (iii) uses the holo-defined
pocket to decide whether an apo candidate is ligand-free there. That is holo used to _validate
the benchmark_, not to predict, and its bias runs **against** us: the filter discards apo
structures that would have leaked conformational information.

A second, **anti-conservative** criterion is also in force and has to be named. Every arm
declares `state: {..., matched: true|false}`, and matched-ness is an apo↔holo comparison; the
Site 2 arm's note says outright that "`8QYP` is the closest matched frame available, 1.02 Å
all / 0.33 Å core", and the `srx` arm's predecessor (`8ACT`→`9GZ1`) was rejected on an 11.78 Å
apo↔holo core RMSD. Choosing the apo frame that sits closest to the holo selects apo
structures already near the bound conformation, which makes the pocket **easier**, not harder.

Both are defensible — one is a leakage filter, the other is pair-matching quality control
without which the pair measures the wrong thing (§4) — and both are pre-registered before any
method ran. Stating the direction of each is what makes them admissible; claiming only the
conservative one is what would not.

Two consequences we apply without exception:

- **A pair fails clause (iii) even if the occupying ligand is deleted during cleaning.** A
  structure crystallised with something in the pocket is in the pocket-bound conformation.
  Removing the atoms does not remove the information. This is what disqualifies `1OPL`.
- **Clause (i) is checked by reading the chemical component ID out of the file**, never by
  trusting a table. This is what disqualifies `6C1H`.
- **Clause (ii) is checked by requiring a DOI and a named assay per target**, enforced by
  `tests/test_benchmark.py`. A 4.5 Å shell around a bound drug is a _drug footprint_; what
  makes it an allosteric site is an experiment somebody ran, and the manifest now has to
  cite it.

**Where this sits in the literature.** The site-relative reading is published, not invented
here: AHoJ annotates chains "as holo or apo respective to the presence or absence of ligands
in the defined binding site(s)" ([10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701)),
PocketMiner scopes its ligand exclusion to 5 A of the site
([10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)), and CryptoBench
inherits that annotation ([10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)).
It is also contested. Wankowicz et al. define apo _globally_ -- any heteroatom group of >=10
heavy atoms disqualifies a structure
([10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114)) -- and classical IUPAC/NC-IUBMB
enzymology inverts the label outright, making a cofactor-bound form holo unconditionally. No
shared term for the site-relative concept exists in the sources reviewed, so "site-apo" is
this repo's coinage and the report states the sense in use at first use. Because the readings
disagree, we record what each structure _contains_ rather than relying on the word. Full
review, including the tolerated-ligand whitelists that disagree between benchmarks:
[`evidence/apo-holo-definition.md`](evidence/apo-holo-definition.md).

**The cost of getting clause (iii) wrong has been measured inside the allostery field**, and
this is the argument that matters — it needs no cryptic-pocket criterion at all. ESSA reports
**10 of 14** top-3 successes on ligand-stripped holo structures against **7 of 14** on true
apo: roughly a 30 % relative inflation from evaluating on a structure that was crystallised
around its ligand. APOP's headline numbers are explicitly on "holo-structures formed simply
by removing any ligand(s)", and AlloBench strips heteroatoms from holo. Pryakhin 2026 names
the mechanism directly — running a pocket detector on a holo structure without removing the
modulator is data leakage, which is the same defect our `1OPL` audit reached independently.

Two consequences. First, deleting the atoms does not remove the information, so a pair fails
clause (iii) even after cleaning — this is what disqualifies `1OPL`. Second, **every published
number we compare against must be labelled** with which kind of structure produced it; most
of the field's headline accuracies are ligand-stripped-holo numbers and are not commensurable
with an apo-only result.

**"Holo" is used in two opposite senses in this field**, so the word alone never identifies
which ligand is meant. ASD's holo is _allosteric-modulator_-bound; AlloReverse defines its
RAE "between the apo and orthosteric ligand-bound (holo) states". We always name the
component ID.

**What the apo structures actually contain.** Measured, not assumed -- heavy atoms, 4.5 A,
via `allo.structure.pdb`, and reported **per arm rather than per entry**, because occupancy is
a property of a structure *and a site*: `8QYP` is the apo of three arms and answers differently
for each. None of the eight distinct apo entries is globally ligand-free, so under the
Wankowicz reading this benchmark would have no apo members at all. Under clause (iii) exactly
one arm fails.

Two columns, because they answer different questions and only the second decides the clause.
Over the **full** label set the catalytic cofactor registers as an occupant wherever the
allosteric site abuts the active site. Over the **scoreable** set -- the residues a method is
actually asked to find -- those contacts vanish and only a genuine occupant survives.

| arm | apo | non-water components | nearest label | contacted | nearest scoreable | scoreable contacted | clause (iii) |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `kras_g12c_mandated` | `4OBE` | GDP, MG | 2.78 A | 5 | 4.57 A | 0 | passes |
| `kras_g12c_corrected` | `4LDJ` | GDP, MG | 2.79 A | 5 | 4.58 A | 0 | passes |
| `bcr_abl1_mandated` | `1OPL` | **MYR**, P16 | **3.29 A** | **16** | **3.29 A** | **16 of 20** | **FAILS** |
| `bcr_abl1_corrected` | `2G2H` | P16 | 16.27 A | 0 | 16.27 A | 0 | passes |
| `bcr_abl1_sensitivity` | `2G1T` | 112 (chain E), MG | 13.15 A | 0 | 13.15 A | 0 | passes |
| `cardiac_myosin_site1_corrected` | `9GZ3` | ADP, MG, PO4 | 20.52 A | 0 | 20.52 A | 0 | passes |
| `cardiac_myosin_site1_sensitivity_xray` | `8QYP` | ADP, MG, VO4 | 18.83 A | 0 | 18.83 A | 0 | passes |
| `cardiac_myosin_site1_sensitivity_srx` | `9YRG` | ADP, PO4 | 20.03 A | 0 | 20.03 A | 0 | passes |
| `cardiac_myosin_site1_omecamtiv` | `8QYP` | ADP, MG, VO4 | 17.65 A | 0 | 17.65 A | 0 | passes |
| `cardiac_myosin_site2_corrected` | `8QYP` | ADP, MG, VO4 | 2.47 A | 3 | 4.58 A | 0 | passes |

**The two KRAS rows and the Site 2 row are the case the second column exists for.** GDP-Mg
contacts KRAS labels **11, 12, 13, 16 and 34**; ADP-VO4 contacts myosin Site 2 labels **242,
243 and 463**. Every one of those eight residues is *itself an active-site residue* under the
frozen rule, so what the first column is detecting is the two sites sharing a border -- not a
modulator sitting in the pocket. Those residues leave the scoreable set for exactly that
reason (section 5), and over the scoreable set both arms are clean at 4.57-4.58 A.
`1OPL` is the opposite: **none** of its 16 contacted labels is an active-site residue, and the
count does not move between the two columns.

An earlier version of this table was per-entry and quoted 5.35 A / 0 for `4OBE`. Those were
scoreable-set numbers computed under a since-withdrawn definition, printed under a full-set
heading; both columns are now derived and pinned in `frozen.json` (`apo_site_occupancy`).

`1OPL` does not merely resemble a holo structure, it _is_ one with respect to the site being
predicted: myristate contacts 16 of the 20 label residues. It is retained only
as the `mandated` tier, to show what the challenge's own assignment scores.

The passing rows carry a modelling caveat that the word "apo" hides. C5 excludes cofactors
from the network, so ADP/Mg/Pi in the myosin entries and GDP/Mg in the KRAS entries are
modelled as absent while their conformational imprint remains in the coordinates. That is a
stated approximation, not a free pass -- a bound nucleotide is a constraint on precisely the
elastic network being simulated.

**Where we deviate from the field standard, and why.** CryptoSite's own criteria are now read
from its full text rather than inferred
([10.1016/j.jmb.2016.01.029](https://doi.org/10.1016/j.jmb.2016.01.029)): binding residues are
those with **any atom within 5 A of any ligand atom**; redundancy is removed at a **40 %
sequence-identity** threshold; cryptic sites are separated from ordinary binding pockets by
**Fpocket and ConCavity pocket scores** being bad in the unbound and good in the bound form;
and its ligands come from **Binding MOAD**, whose validity rule is hand curation against the
crystallography paper -- "valid ligands are biologically relevant small molecules ... agonists,
antagonists, cofactors, inhibitors, allosteric regulators, enzymatic products", excluding the
crystallisation matrix (solvents, buffers, detergents, salts), while glycosylation, catalytic
metal and HEME count as _part of the protein_
([10.1093/nar/gkm911](https://doi.org/10.1093/nar/gkm911), full text).

Three deviations, each deliberate:

1. **Contact cutoff 4.5 A heavy-atom, not 5.0 A any-atom.** Ours is the stricter rule. 4.0 and
   5.0 are frozen alongside it, so the field's cutoff is recoverable from `frozen.json` without
   re-deriving anything.
2. **We retain a covalent ligand; MOAD would not.** Binding MOAD states plainly that
   "covalently attached molecules (covalent inhibitors or posttranslational modifications to
   the protein) are not considered valid ligands". `6OIM` records
   `covale CYS 12 SG - MOV C25, 1.805 A` in `_struct_conn` -- read from the file, not assumed --
   so **KRAS G12C/sotorasib would be excluded from CryptoSite's benchmark outright**. We keep
   it, because covalent inhibition is the modality that made this target druggable at all and
   the S-IIP is defined by the ligand's occupancy irrespective of its warhead. `5MO4` (AY7) and
   `9GZ2` (XB2) carry no covalent link and are unaffected. This is the deviation most likely to
   be challenged, which is why it is stated here rather than in a footnote.
3. **No sequence-identity de-duplication.** At three hand-specified targets the 40 % rule has
   nothing to act on; it matters only for the ASD generalisability set, where it will be applied.

The pocket residue set itself: protein residues with **any heavy atom within 4.5 Å of any
heavy atom** of the named ligand. 4.0 Å and 5.0 Å are frozen alongside it in
`frozen.json` (`labels_by_cutoff`), so a later run cannot quietly report whichever cutoff
flatters a method. Label counts move materially — KRAS 17/21/22, BCR-ABL1 16/18/21, myosin
10/12/14 — which is exactly why they are pinned rather than merely promised. Rationale and alternatives: ADR 0004.

---

## 2. Audit of the challenge's assignments

All three assigned pairs are defective. Full dossiers in `audit/`; the deciding facts:

| Pair                         | Verdict                | Deciding evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KRAS `4OBE`→`6OIM`           | usable, wrong genotype | `4OBE` `_struct_ref_seq_dif` lists no mutation; residue 12 is **GLY** in both chains. `6OIM` is G12C + C51S/C80L/C118S. The apo input lacks the cysteine the holo drug is covalently bonded to.                                                                                                                                                                                                                                                                        |
| BCR-ABL1 `1OPL`→`5MO4`       | not a blind prediction | `1OPL` contains `MYR` **in the myristoyl pocket** (chain A) and `P16` in the ATP site. Its 16 myristate-contact residues are a strict subset of asciminib's 20. Apo↔holo Cα RMSD **1.00 Å** over 409 paired residues and **0.50 Å** across the pocket lining, fitted on the non-label residues.                                                                                                                                                                        |
| Cardiac myosin `5TBY`→`6C1H` | **unscoreable** | `6C1H` is rat unconventional **myosin-Ib** (Q05096) + rabbit actin (P68135) + calmodulin (P0DP23), a **heptameric** assembly (Mentes 2018, doi:10.1073/pnas.1718316115). Ligands: ADP and Mg, all ten copies on the _actin_ chains A–E; nearest approach to myosin chain P is 6.66 Å. No mavacamten; mavacamten is component `XB2` and appears in exactly six entries — `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7` — none of them this one. `5TBY` is a SWISS-MODEL homology model on a **tarantula** template (`3JBH`), rigid-body fitted (`_em_3d_fitting.ref_protocol = RIGID BODY FIT`); the entry records 20 Å (`_em_3d_reconstruction.resolution`) and its source map `EMD-2240` is 28 Å. `3JBH` is itself a 20 Å EM-docked model, so `5TBY` is a model built on a model. |

The myosin failure is a factual error in the challenge statement rather than a judgement
call, and is worth reporting upstream. The other two are defensible-but-suboptimal choices.

### 2b. Dimensions checked beyond ligand identity

An audit that only reads the ligand list misses the ways a pair fails quietly. Re-audit
2026-08-20 swept the following, all from RCSB records and the deposited coordinates. Six of
eight came back clean; the two that did not are recorded rather than smoothed over.

| Dimension                                       | Method                                                                               | Result                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ligand fit to density**                       | RCSB `nonpolymer_entity_instance` validation                                         | `6OIM` MOV **RSCC 0.908**, `5MO4` AY7 **0.946**, `8QYR` XB2 **0.915** — all strong. **Cryo-EM entries carry no deposited ligand-fit score at all**, so `9GZ2` and `9YR7` (the `corrected` and `srx` myosin holos) rest on an unscored placement. `9GZ1`, considered and replaced, additionally reported 9 intermolecular clashes in chain B.                                                                                                                       |
| **Crystal packing at the pocket**               | `REMARK 290` symmetry expansion, ±1 unit cell, Fisher test vs. the rest of the chain | Not enriched anywhere (`4OBE` 48 % of labels vs 40 % background, OR 1.37, **p = 0.33**) — so no crypticity verdict is a lattice artefact. But `4OBE`'s switch-II _is_ lattice-engaged (10 of 21 labels, closest 2.58 Å) where `4LDJ`'s is not (2 of 21) — and `4LDJ`, the _less_ packed structure, clashes _more_ on transplant (18/41 vs 14/41). The confound was tested and the cryptic verdict survives it.                   |
| **Sequence identity, apo↔holo** | pairwise alignment of modelled chains | 97.6–100 % on every frozen arm; pinned as `sequence_agreement.identity`. ADR 0004's exclusion rule is now a number rather than a promise. **Clause (iv) also asks for differences to be _enumerated_, and four sit outside the modelled spans where the alignment cannot see them**: `8QYR` carries **F735D** (typed _conflict_ vs Q9BE39 — Asp735 is 17.9 Å from XB2 and residue 735 is unmodelled in the `8QYP` apo, so no label set is touched); `9GZ1`/`9GZ2`/`9GZ3` carry A1124S, beyond their 3–796 span; `9YRG`/`9YR7` carry M1055V, F1118L, S1119T and H1285L, all inside the EGFP moiety, beyond their 4–943 span. Read from `_struct_ref_seq_dif`. |
| **Mutations inside the label set**              | per-residue comparison across the alignment                                          | Exactly one, and it is the KRAS defect: `kras_g12c_mandated` has **`GLY12->CYS`** — the residue sotorasib is covalently bonded to does not exist in the input. Every other arm: zero. `kras_g12c_corrected` is clean, which is the sharpest single argument for `4LDJ`.                                                                                                                                                          |
| **Alternate conformations / partial occupancy** | `label_alt_id`, `occupancy`                                                          | Present in `5MO4` and `8QYR`; **no label residue in any arm has one**. The parser ignores altloc, so this is currently true by luck, not by design — see open items.                                                                                                                                                                                                                                                             |
| **Chain breaks near the site**                  | gaps in modelled author numbering                                                    | None abuts a label in any arm. Myosin has gaps at 202–214 and 624–645; both are far from the site.                                                                                                                                                                                                                                                                                                                               |
| **Order at the site**                           | median B-factor, labels vs chain                                                     | Label residues are as ordered as the chain or better (ratio 0.78–1.10). The sites are not modelled into noise.                                                                                                                                                                                                                                                                                                                   |
| **Biological assembly vs. the frozen input**    | RCSB `assembly` records                                                              | Every `corrected` arm is a **monomeric** assembly, so chain A _is_ the biological unit. Three exceptions: `2G1T` is dimeric, `8QYU` (the omecamtiv holo) is a hetero-dimer with its essential light chain, and the IHM entries (`9YRG`/`9YR7`) are **hexameric**. Freezing chain A of the IHM discards the inter-head interface the arm exists to study — label residue 721 sits in a 3.34 Å inter-chain contact — which is the open question the coarse-graining phase has to answer, not a defect in the pair. |

---

## 3. The frozen input layer

Three tiers, all reported (ADR 0003). `mandated` is exactly what `CHALLENGE.md` Table 1
specifies; `corrected` is the defensible pair for the same biology; `sensitivity` tests
whether a conclusion survives a different structure. Everything was fixed **before any
method was run**.

| Target                                | Tier        | Site   | Apo      | Holo     | Effector | N   | \|GT\| | scoreable | prevalence | blind                                |
| ------------------------------------- | ----------- | ------ | -------- | -------- | -------- | --- | ------ | --------- | ---------- | ------------------------------------ |
| kras_g12c_mandated                    | mandated    | —      | `4OBE`:A | `6OIM`:A | MOV      | 169 | 21     | 16        | 12.4 %     | ❌ not blind                         |
| kras_g12c_corrected                   | corrected   | —      | `4LDJ`:A | `6OIM`:A | MOV      | 170 | 21     | 16        | 12.3 %     | ❌ not blind                         |
| bcr_abl1_mandated                     | mandated    | —      | `1OPL`:A | `5MO4`:A | AY7      | 451 | 20     | 20        | 4.4 %      | ❌ not blind                         |
| bcr_abl1_corrected                    | corrected   | —      | `2G2H`:A | `5MO4`:A | AY7      | 272 | 18     | 18        | 6.6 %      | ❌ not blind                         |
| bcr_abl1_sensitivity                  | sensitivity | —      | `2G1T`:A | `5MO4`:A | AY7      | 271 | 18     | 18        | 6.6 %      | ❌ not blind                         |
| cardiac_myosin_site1_mandated         | mandated    | Site 1 | `5TBY`   | `6C1H`   | —        | —   | —      | —         | —          | **excluded: no ground truth exists** |
| cardiac_myosin_site1_corrected        | corrected   | Site 1 | `9GZ3`:A | `9GZ2`:A | XB2      | 764 | 12     | 12        | 1.6 %      | ❌ not blind                             |
| cardiac_myosin_site1_sensitivity_xray | sensitivity | Site 1 | `8QYP`:A | `8QYR`:B | XB2      | 706 | 15     | 15        | 2.1 %      | ❌ not blind                             |
| cardiac_myosin_site1_sensitivity_srx  | sensitivity | Site 1 | `9YRG`:A | `9YR7`:A | XB2      | 912 | 12     | 12        | 1.3 %      | ❌ not blind                             |
| cardiac_myosin_site1_omecamtiv        | sensitivity | Site 1 | `8QYP`:A | `8QYU`:A | 2OW      | 706 | 18     | 18        | 2.5 %      | ❌ not blind                             |
| cardiac_myosin_site2_corrected        | corrected   | Site 2 | `8QYP`:A | `9F6C`:A | 6I6      | 706 | 21     | 18        | 3.0 %      | ❌ not blind                         |

Two `bcr_abl1_corrected` labels (Val525, Leu529) fall outside the kinase-domain-only apo
model and are reported as unmapped rather than silently dropped. N counts every polymer
residue including modified ones — the `8QYP` total includes two trimethyl-lysines, which
the ATOM/HETATM flag would have dropped.

**N is the whole modelled chain, never a trimmed catalytic domain** (ADR 0010, accepted).
On `1OPL` that is 451 residues including SH3 and SH2, against 272 for the kinase-only
`2G2H` — so the mandated ABL1 arm's harder chance line is mostly construct extent, not the
myristate defect its tier exists to expose, and the two must not be compared as if it were.

**N is what a method _receives_, not what it is _scored against_.** The scoring universe is
the smaller **candidate set** — N minus the propagation source, minus any sibling functional
site on the same apo chain (ADR 0011) — because a residue that a connectivity score ranks top
by construction is no more a negative than it is a positive. It runs 146 to 886 against N of
169 to 912, and every chance line in §5 is computed on it. The input is untouched: a method
still gets the whole chain, source set included.

The N, |GT| and prevalence columns are read back from `frozen.json` by
`tests/test_benchmark.py`, so they cannot drift from the freeze. The remaining columns are
in `frozen.json` but are not yet compared against this prose.

---

## 4. The benchmark's difficulty axes

**The benchmark poses one cryptic-pocket problem, one proximal-site problem, and several
"which pre-formed surface pocket is the coupled one" problems.** Freezing the inputs let us
measure that before measuring any method on it — which is the difference between crediting a
method and crediting an easy instance.

Nothing in this section is a validity test. Crypticity is a **structural** property; allostery
is a **functional** one; they are orthogonal, and fewer than half of validated cryptic sites
are allosteric (ADR 0007). A pre-formed allosteric site is a perfectly good target — it is the
target the field's canonical example, the ABL1 myristoyl pocket, actually is. What these
numbers do is say which instances were easy, so a strong average cannot hide behind them.

**Axis 1 — crypticity.** Superpose the holo entry onto the apo locally (the shell within
**20 Å** of the pocket centroid, `SHELL_ANGSTROM`, pocket residues excluded from the fit,
residues paired through the sequence alignment), carry the ligand across, and count how hard
it collides. A cryptic pocket does not exist in the apo input, so the ligand cannot be placed;
a pre-formed pocket accepts it. "Clash" means a transplanted ligand atom within **2.5 Å** of
an apo protein heavy atom. Both constants are declared here because they define a column
below; neither is load-bearing — sweeping the shell 12/16/20/25 Å and global moves
`transplant_min_distance` by ≤ 0.4 Å and never reorders the three difficulty classes, which
separate on that threshold-free number alone.

**Axis 2 — proximity to the active site.** How far the labels sit from the propagation source.
This is the axis that says whether a rank-by-distance baseline would ace the target, and it is
reported precisely so that it cannot be quietly ignored.

| Target                                  | core RMSD | pocket lining | worst | transplant clashes | min d→active | median d→active |
| --------------------------------------- | --------: | ------------: | ----: | -----------------: | -----------: | --------------: |
| `kras_g12c_mandated`                    |      1.07 |      **2.61** |   8.9 |              14/41 |          0.0 |             9.5 |
| `kras_g12c_corrected`                   |      1.05 |      **2.62** |   8.9 |              18/41 |          0.0 |             9.2 |
| `bcr_abl1_mandated`                     |      1.00 |      **0.50** |   1.0 |               0/31 |         10.6 |            18.3 |
| `bcr_abl1_corrected`                    |      1.72 |      **2.38** |   9.6 |               2/31 |         10.8 |            17.5 |
| `bcr_abl1_sensitivity`                  |      2.56 |      **2.28** |   9.0 |               2/31 |         10.8 |            17.6 |
| `cardiac_myosin_site1_corrected`        |      1.18 |      **1.10** |   1.9 |               0/20 |         16.5 |            27.6 |
| `cardiac_myosin_site1_sensitivity_xray` |      1.22 |      **1.79** |   3.4 |               0/20 |         13.3 |            22.2 |
| `cardiac_myosin_site1_sensitivity_srx`  |      0.88 |      **0.46** |   0.8 |               0/20 |         18.3 |            24.1 |
| `cardiac_myosin_site1_omecamtiv`        |      1.13 |      **1.90** |   3.4 |               0/29 |         12.3 |            21.2 |
| `cardiac_myosin_site2_corrected`        |      1.01 |      **0.46** |   0.7 |               1/25 |          0.0 |             8.4 |

For reference only: CryptoBench admits a site to its _cryptic-site_ dataset at ≥ 2 Å lining
RMSD ([10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)).
CryptoBench never uses the word "allosteric". That threshold is quoted here as a yardstick for
reading the middle column, **not** as a criterion any arm passes or fails.

What the two axes say, target by target:

- **KRAS is the only genuinely cryptic case, and also the most proximal.** The switch-II
  segment swings out to create the pocket: 1.05 Å core against **2.62 Å lining, 8.9 Å at its
  worst**, with 18 of 41 ligand atoms clashing. But 5 of its 21 labels _are_ active-site
  residues under the frozen rule, the remaining 16 sit at a median 9.2 Å, and sotorasib is
  covalently bonded to Cys12. Easy on axis 2, hard on axis 1.
- **The myristoyl pocket is not cryptic, and the literature agrees.** Asciminib transplants
  into _every_ myristate-free ABL1 apo candidate tested — `1M52`, `2G1T`, `2G2H`, `4WA9` — with
  at most 2 of 31 atoms clashing. Paladini et al. (_eLife_ 2024) describe the αI helix as
  adopting "a straight conformation in crystal structures of the isolated Abl kinase domain
  with an **empty myristoyl binding pocket** (PDB 1M52)"; Wylie et al. (_Nature_ 2017) call it
  a "vacant pocket". A constitutive cavity gated by helix conformation — and in `1OPL` it is
  filled with its native ligand. **We must not claim to discover a cryptic pocket in ABL1.**
  It remains a fully valid allosteric target: it is the field's canonical _allosteric but not
  cryptic_ example, and what is left to predict is which of the many pre-formed pockets is the
  coupled one.
- **Site 1 on myosin is pre-formed and well separated from the active site.** Zero clashes on every arm, lining
  0.46–1.90 Å, labels 12.3–18.3 Å from the source at closest. Hard on neither axis in the
  cryptic sense, and hard in the way that matters: nothing about the apo geometry marks it out.
- **Site 2 on myosin is pre-formed and proximal**, and is in the benchmark for that reason.
  Median label→source distance **8.4 Å**, minimum 0.0. Roughly 30 % of catalogued allosteric
  sites overlap or border the catalytic site (CASBench), and without an arm in that class the
  benchmark cannot distinguish "predicts allostery" from "predicts distance".

**The two crypticity proxies disagree on `bcr_abl1_corrected`, and that is a result about the
measure.** Transplant says pre-formed (2 of 31 atoms clashing, closest approach 1.95 Å); lining
RMSD says changed (2.38 Å). Both regenerate from `frozen.json`. The lining figure is αI-helix
conformation plus the two unmapped labels, not pocket closure — which is a caution against
treating either proxy as definitive, and a reason the corrected tier rests on myristate-freedom
and numbering agreement (ADR 0003) rather than on any crypticity number.

**The `srx` arm is the control on the whole measure.** Its pair (`9YRG`→`9YR7`, same study,
same construct) gives **0.88 Å core over 900 paired residues at 100 % sequence identity** —
what a genuinely matched pair looks like. The arm it replaced (`8ACT`→`9GZ1`) gave an 11.78 Å
core, which is how it was caught. Pair-matching is the one job this measure does as a verdict
rather than as a descriptor.

**Prediction, recorded now so it counts as one.** A pure geometric pocket finder should score
near zero on KRAS and respectably on the pre-formed sites; a rank-by-inverse-distance-to-active-site
baseline should score well on KRAS and Site 2 and poorly on Site 1. Both baselines are therefore
mandatory on every arm. If the quantum method does not beat inverse distance on KRAS and Site 2,
that is the finding.

**What a high score here does and does not demonstrate.** The label set is a **binding-site**
label set, not a coupling label set — it is the residue shell around an effector whose
allosteric action is established by the cited assay, not a set of residues measured to carry
signal. An audit of **eight of the ten frozen arms** (`evidence/allosteric-pair-audit.md`, which predates ADR 0008 and so covers neither `cardiac_myosin_site1_omecamtiv` nor `cardiac_myosin_site2_corrected`) finds **no active-site response attributable to the allosteric ligand** in any of them: in six of those eight the active site is the most rigid part of the chain. That is consistent with the ensemble view of allostery —
coupling can proceed through fluctuation entropy with no mean-coordinate signature — and it is
not grounds to reject a pair. It does mean a high benchmark score demonstrates **site
identification, not coupling recovery**, and the report must not claim the latter from the
former. (Read the audit's p-values with care: its null is "active site vs rest of chain", and
active sites are the most conserved and buried part of an enzyme almost regardless of ligand.)

**The KRAS pocket has already been predicted classically, in 2011.** Grant et al. ran 120 ns
of MD from `2PMX` with FTMap/AutoLigand and reported a pocket "between helices α2 and α3" at
residues **61–65 and 90–99** ([10.1371/journal.pone.0025711](https://doi.org/10.1371/journal.pone.0025711))
— **two years before** Ostrem et al. characterised the switch-II pocket experimentally. Against
our frozen scoreable label set that prediction contains **6 of 16 residues (61, 62, 63, 95, 96, 99)**, Jaccard 0.24. A ranking that returned five residues drawn from their pocket would be
expected to score ~2 true hits, against a hypergeometric expectation of **0.47**
(`expected_hits_at_5`; an earlier draft said 0.41, which is 5 x 14/170 under the withdrawn
14-label distal set).

This is the single most important calibration fact in the benchmark and it must appear in the
report. It does not disqualify anything — Grant's input was an MD trajectory, which C2 forbids
us — but it means **the S-IIP is not an open prediction problem**, and any claim that a quantum
method "discovers" it is a claim about efficiency and about doing it without MD, never about
priority. Stating this ourselves is worth more than having a reviewer state it.

**Separation from the active site — reported, not required.** The challenge speaks of "distal
regulatory residues", but distance is not what makes a site allosteric: CASBench reports ~30 %
of catalogued allosteric sites overlapping or bordering the catalytic site
([10.32607/20758251-2019-11-1-74-80](https://doi.org/10.32607/20758251-2019-11-1-74-80)), so
this is a descriptor of each target, not an admission criterion (ADR 0007). CASBench's 30 % is quoted often enough here to need its own limit stated: the sentence immediately before it reads "In all the CASBench annotations, different sites are topologically independent from each other (i.e., they are represented by separate cavities in the enzyme structure)", and the paper gives **no distance or geometric criterion** for "overlap or share a common border". So it establishes that the field applies **no minimum separation convention** -- which is all we use it for -- and it does *not* license treating a residue that is itself an active-site residue as an ordinary label. That case is handled by AlloPred's set-membership rule instead. Minimum Cα distance from a
label residue to the active site is 10.6 Å for `bcr_abl1_mandated`, 10.8 Å for
`bcr_abl1_corrected` and 16.5 Å for `cardiac_myosin_site1_corrected`; medians run 17–28 Å.
(The ABL1 minima moved from 12.1/12.7 Å when all three ABL1 arms adopted the catalytic-motif
source rule ADR 0005 prescribes; the drug-footprint source they previously used was larger
and sat further from the myristoyl pocket.) KRAS is the
exception and needs care: **5 of its 21 label residues (11, 12, 13, 16, 34) are themselves
active-site residues**, at 0.0 Å, because the switch-II pocket abuts the nucleotide site and
sotorasib is anchored at Cys12. Those five leave the scoreable set for that reason.
**Site 2 on myosin is the deliberate case of the same kind**: median 8.4 Å, minimum 0.0 Å,
3 of 21 labels in the source set. Scoring "connectivity to the active site" ranks such residues
top trivially, which is why the null is distance-matched rather than uniform. See ADR 0005,
ADR 0007 and §5.

---

## 5. The evaluation protocol

Fixed here, before any method exists, so that no test can be chosen after seeing scores.

**Primary endpoint.** Within a target: **AUC-ROC _and_ AUC-PR of the residue score for
ground-truth pocket residues against background residues**, each reported with the chance
line (0.5 for ROC; the label prevalence for PR). AUC is simultaneously the test statistic
and the effect size, which avoids reporting significance without magnitude.

**Both, because one is not enough at this prevalence.** Scoreable-label prevalence over the
candidate set runs from 10.8 % (`kras_g12c_corrected`, 16/148) to
1.4 % (`cardiac_myosin_site1_sensitivity_srx`, 12/886) -- a **8.0x** span.
Simulating a _fixed_ real signal (d = 0.8, 2000 draws, seed 0; regenerate with
`uv run allo benchmark stats`) across that range gives AUC-ROC **0.716** / **0.713** /
**0.714** -- flat -- while AUC-PR falls **0.292** -> **0.208** -> **0.066**, a 4.4x span. AUC-ROC is
blind to the imbalance, so a single ROC number would present myosin as an equally solved
problem when its retrieval task is far harder. The field's own results show the same gap on
the same predictor: CryptoBench reports AUC 0.86 against AUPRC 0.36
([10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)),
PocketMiner 0.83 +/- 0.04 against 0.44 +/- 0.12
([10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)); the general
argument for PR over ROC under imbalance is Saito & Rehmsmeier
([10.1371/journal.pone.0118432](https://doi.org/10.1371/journal.pone.0118432)). P2Rank
rejects residue-level AUC altogether in favour of pocket-centric top-n
([10.1186/s13321-018-0285-8](https://doi.org/10.1186/s13321-018-0285-8)), which is why the
top-5 endpoint below is not decorative.

**AUC-ROC and the Mann-Whitney U test are one procedure, not two.** `U / (n_pos * n_neg)`
equals AUC-ROC exactly (verified numerically: 0.755273 both). They are reported as statistic
and effect size of a single test, and never as two independent lines of evidence.

**The primary endpoint is computed on the _scoreable_ label set** — every label that is not
itself a propagation-source residue. This is set membership, not distance: a label that is in
the source set scores maximally by construction and therefore measures nothing. The rule is
AlloPred's, published in this field — "Active site residues were not counted as being in any
pocket … in order to avoid direct perturbation of the site at which the effect was measured"
([10.1186/s12859-015-0771-1](https://doi.org/10.1186/s12859-015-0771-1)).

**…and against the _candidate_ set, not the node set. Those residues leave the negatives
too** (ADR 0011). An earlier version of this protocol removed them from the positives and
left them in the background, which is not a neutral half-measure — it is a handicap aimed at
one method class. The challenge asks for connectivity **to an active site**; a method that
computes it ranks the source set top *because that is the quantity*, and every one of those
residues then scores as a false positive. A geometric detector takes no such hit. At a fixed
real effect the cost is **44–62 % of AUC-PR** across these arms, on identical signal:

| arm                              | AUC-ROC geo → conn | AUC-PR geo → conn | AUC-PR lost |
| -------------------------------- | ------------------ | ----------------- | ----------: |
| `kras_g12c_mandated`             | 0.799 → 0.679      | 0.386 → 0.146     |    **62 %** |
| `bcr_abl1_corrected`             | 0.799 → 0.765      | 0.314 → 0.165     |    **47 %** |
| `cardiac_myosin_site1_corrected` | 0.809 → 0.787      | 0.146 → 0.057     |    **61 %** |

Excluded from both classes, frozen per arm as `excluded_from_scoring` / `n_candidates`: the
**propagation source** (2.4–13.6 % of the node set; 23 of 169 residues on KRAS), and any
**sibling functional site** — residues this benchmark labels as a *different* site on the
same apo chain, which is the three `8QYP` arms where Site 1 and Site 2 are both frozen. The
rule below for the decoy set was always this; the background now matches it. **The input is
untouched:** a method still receives the whole modelled chain, source set included.

It bites on exactly two arms. KRAS drops 21 → **16** (residues 11, 12, 13, 16, 34 are
active-site residues under the frozen `{from_ligands: [GDP, MG]}` rule), and Site 2 on myosin
drops 21 → **18**. Every other arm is unaffected. Both sets are pinned in `frozen.json`.

**No distance threshold is applied, and an earlier version of this benchmark was wrong to
apply one.** It dropped labels within 5 Å of the active site as "not distal", which asserted a
convention the allostery literature does not contain: ASD v1/v2/v3 and CASBench specify no
minimum separation, and CASBench reports ~30 % of allosteric sites overlapping or bordering the
catalytic site (limit of that number: section 4). On KRAS that threshold discarded residues **10 and 58**, neither of which is an
active-site residue under our own rule — a second, undeclared criterion operating silently.
Proximity is a real confound and it is handled where it belongs, in the null: scores are
compared against residues **at similar distance from the active site**, which is Amor et al.'s
construction ([10.1038/ncomms12477](https://doi.org/10.1038/ncomms12477)) and costs no labels.

**The null is the opponent, and it is not the rank-sum null.** Residue scores are spatially
autocorrelated and the label set is a single contiguous patch, so residues are nowhere near
independent draws. We use a **matched patch null**: sample B = 10,000 connected patches of
the same size as the label set by nearest-neighbour growth on the contact graph, drawn from
the candidate set, recompute the statistic on each, and take the empirical p-value. Four
properties are matched, and the fourth was missing until an adversarial review found the
paragraph above promising it and this one not delivering it:

1. **size** — same residue count as the label set;
2. **contiguity** — connected on the contact graph, by nearest-neighbour growth;
3. **surface exposure** — seeds drawn from the surface set;
4. **distance to the active site** — the patch's distance-to-source distribution must match
   the label patch's, seeds accepted by rejection sampling against it.

Without (4) the null is **anti-conservative on exactly our proximal arms**. KRAS labels sit
at 0 Å from the source and Site 2's median is low; uniformly seeded patches are farther away,
so a bare *distance-to-active-site* score — which contains no allosteric information at all —
clears the null. Matching (1)–(3) controls the confound `docs/FIELD.md` §3 names, that any
residue score correlates with burial and degree; matching (4) controls the one this benchmark
creates for itself by keeping proximal labels (ADR 0007).

**The null is not frozen until it is calibrated.** Before it is used to report any p-value, a
**distance-only score and a degree-only score must be run through it on every arm and must
fail to reach significance**. A null whose type-I error has not been measured is a claim, not
a control. That calibration is a Phase 1.6 exit criterion, and until it passes no p-value
from this benchmark is quotable.

**The matched-patch idea has one clear precedent, and it is the canonical paper.** CryptoSite
builds its dataset as 84 cryptic sites, 92 binding pockets **and 705 concave surface
patches**, then compares site properties across those three classes with p-values -- pocket
score 0.07 vs 0.42 (P = 1.7e-31), protruding atoms 170 vs 183 (P = 8.0e-3), convexity 2.4 vs
1.9 (P = 0.8) -- and states a random-residue baseline for its predictions (19 residues tested
at random to find one true cryptic residue)
([10.1016/j.jmb.2016.01.029](https://doi.org/10.1016/j.jmb.2016.01.029), full text). So the
control class we need is not an invention, and the concave-patch construction is close to our
patch null by design.

**What is still missing is using it as a null for a predictor.** CryptoSite's patches
characterise what cryptic sites _are_; they do not calibrate what a ranking _scores_. And in
the other full texts reviewed -- PocketMiner, CryptoBench, DeepAllo
([10.1093/bioinformatics/btaf294](https://doi.org/10.1093/bioinformatics/btaf294)), Ohm
([10.1038/s41467-020-17618-2](https://doi.org/10.1038/s41467-020-17618-2)), P2Rank -- there
are no permutation tests, no p-values and no random baselines; MEF-AlloSite
([10.1186/s13321-024-00882-5](https://doi.org/10.1186/s13321-024-00882-5)) reports
uncorrected one-sided t-tests. None addresses spatial autocorrelation explicitly. Two adjacent
literatures supply the justification the field leaves implicit: on residue-contact graphs a
non-geometric null declares "almost all analyzed subgraphs" significant
([10.1371/journal.pone.0005967](https://doi.org/10.1371/journal.pone.0005967)), and
clustering alone lets labelled residues beat _size-matched_ random subsets in 96.7 % and
87.7 % of interfaces
([10.1186/1471-2105-11-286](https://doi.org/10.1186/1471-2105-11-286)) -- a confound our
patch null is built to absorb and a uniform-residue null is not. Full review:
[`evidence/evaluation-protocol-lit.md`](evidence/evaluation-protocol-lit.md).

**Second negative set.** The challenge scores against non-functional surface pockets as well
as random background. Under a _functional_ ground truth "non-functional" cannot mean "no
ligand was crystallised here", so three classes are reported separately and never pooled:

1. **Random background residues.**
2. **Geometric surface pockets on the apo input**, excluding the true site, **the active
   site** (it is a pocket, it does not overlap the true site, and a connectivity-to-active-site
   score ranks it top by construction), and any documented sibling functional site — every
   target has at least one, and scoring those as decoys penalises a method for being right.
3. **Cryptic non-allosteric sites**, the discriminating control: it holds crypticity fixed and
   varies function, which is the only way to show a method finds coupling rather than
   cavity-opening. Vajda 2018 Table 1 supplies **eleven** with named apo/holo pairs -- nine orthosteric (five of them enzyme active sites) plus two protein-protein interfaces. Note that class 2
   _structurally cannot_ produce these — a cryptic pocket is by definition absent from the apo,
   so an apo-side detector will never return one.

**Secondary endpoints.** Precision@5 and P(≥1 true residue in the top 5) — the top-5 hit
list is the scored artifact. Exact hypergeometric baselines under a uniform random ranking,
computed on the **scoreable** label set against the **candidate** set that is the primary
endpoint's universe (ADR 0011), per frozen target:

| Target                                  | N   | excluded | candidates | \|GT\| | \|scoreable\| | prevalence | E[hits@5] | P(≥1 hit) | P(≥2 hits) |
| --------------------------------------- | --- | -------- | ---------- | ------ | ------------- | ---------- | --------- | --------- | ---------- |
| `kras_g12c_mandated` | 169 | 23 | 146 | 21 | 16 | 11.0 % | 0.55 | **0.445** | 0.093 |
| `kras_g12c_corrected` | 170 | 22 | 148 | 21 | 16 | 10.8 % | 0.54 | **0.440** | 0.091 |
| `bcr_abl1_mandated` | 451 | 11 | 440 | 20 | 20 | 4.5 % | 0.23 | **0.208** | 0.018 |
| `bcr_abl1_corrected` | 272 | 11 | 261 | 18 | 18 | 6.9 % | 0.34 | **0.302** | 0.040 |
| `bcr_abl1_sensitivity` | 271 | 11 | 260 | 18 | 18 | 6.9 % | 0.35 | **0.303** | 0.040 |
| `cardiac_myosin_site1_corrected` | 764 | 21 | 743 | 12 | 12 | 1.6 % | 0.08 | **0.078** | 0.002 |
| `cardiac_myosin_site1_sensitivity_xray` | 706 | 47 | 659 | 15 | 15 | 2.3 % | 0.11 | **0.109** | 0.005 |
| `cardiac_myosin_site1_sensitivity_srx` | 912 | 26 | 886 | 12 | 12 | 1.4 % | 0.07 | **0.066** | 0.002 |
| `cardiac_myosin_site1_omecamtiv` | 706 | 44 | 662 | 18 | 18 | 2.7 % | 0.14 | **0.129** | 0.007 |
| `cardiac_myosin_site2_corrected` | 706 | 44 | 662 | 21 | 18 | 2.7 % | 0.14 | **0.129** | 0.007 |

**One hit in the top five means very different things across targets** — close to a
1-in-2 coin flip on KRAS, roughly 14:1 against on myosin's srx arm. Reporting "we found the pocket in the top
5" without this table would be reporting a coin flip as a discovery. Two hits is the level
at which a single target carries evidence on its own.

**Power, honestly.** Treating residues as independent, a rank-sum test at α = 0.05
one-sided and 80 % power detects, on the scoreable label sets that are the primary endpoint,
AUC ≈ 0.69 (KRAS), 0.675 (ABL1 corrected), 0.709 (myosin Site 1 corrected) -- all from
`uv run allo benchmark stats`. Under the patch null those numbers are optimistic by a wide
margin, and the honest figure is starker than a number: if the pocket contributes **one**
effectively independent observation rather than twelve, the Noether bound has **no solution
below AUC = 1.0** at any of these sizes. A single target cannot carry the claim on its own. **We report the patch-null p-value as primary and the rank-sum p-value only as
a labelled upper bound on the evidence.**

**Across targets we claim nothing quantitative.** Three proteins cannot support a pooled
p-value (`docs/FIELD.md` trap 5). Significance lives within a target; the cross-target
statement is qualitative and is reported as such.

**Multiplicity — one confirmatory rule, declared here, because "AUC-ROC _and_ AUC-PR" above
is two endpoints and this section previously promised "one primary metric" without saying
which.** The full hypothesis family, fixed before any method runs:

- **Confirmatory: AUC-PR on the `corrected` arm of each target, against the matched patch
  null. Three tests, Holm-corrected across the three.** AUC-PR because prevalence is the
  thing that varies across these arms and ROC is blind to it; the `corrected` arm because it
  is the defensible pair for the biology, which is what the tier exists to be.
- **AUC-ROC is reported for every arm and tested nowhere.** It is the effect size that makes
  AUC-PR readable, and it is identical to the Mann-Whitney statistic, so testing both would
  be counting one experiment twice.
- **`mandated` and `sensitivity` arms are supportive, never confirmatory.** They are reported
  with p-values labelled *descriptive*. A conclusion that holds on `corrected` and fails on
  `sensitivity` is reported as not robust — that is what the sensitivity tier is for — but
  the reverse never rescues a failed confirmatory test.
- **Arms are not independent and are never pooled.** Five arms share `8QYP`; three share
  `5MO4`. Holm across the three confirmatory tests is valid without an independence
  assumption, which is why it is Holm and not Fisher.
- **When claiming one method beats another**, Holm extends across the methods compared as
  well, and the comparison is declared before the methods are run.

Effect size is reported always; significance only for the three confirmatory tests.

**No tuning on this benchmark.** Any hyperparameter selected by looking at enrichment here
is test-set fitting even with no holo import (`docs/playbooks/constraint-audit.md`).
Selection happens on the ASD generalisability set and is frozen before the primary targets
are touched; anything not selected that way is fixed a priori and declared.

**And the selection set has to be disjoint from the primary targets, which raw ASD is not**
(ADR 0012). §7 records that ASD curates the myristoyl pocket twice and that one of those
records lists `1OPL`/`MYR` as a related complex — our mandated apo is itself an ASD entry —
while ASBench's HRAS record carries 4 of our 5 KRAS label residues past any 30–40 % identity
dedup. Selecting hyperparameters on that set is tuning on the answers by a longer route, and
there is no blind arm left to absorb it. A candidate is admitted only if it is disjoint from
every primary target on **accession, protein family, homologous site, and residue overlap**
— the four clauses of ADR 0012, applied as a pre-filter and frozen as a list before a single
parameter is chosen. The generalisability number in Phase 5 comes from a further set,
disjoint from both and unopened until the method is frozen.

---

## 6. Provenance of every structure used

| PDB            | What it is                                                                           | Primary citation as deposited                                                                            |
| -------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `4OBE`, `4LDJ` | KRAS WT and G12C, GDP·Mg                                                             | Hunter et al., _PNAS_ 2014, doi:10.1073/pnas.1404639111                                                  |
| `6OIM`         | KRAS G12C + sotorasib (`MOV`)                                                        | Canon et al., _Nature_ 2019, doi:10.1038/s41586-019-1694-1                                               |
| `1OPL`         | autoinhibited c-Abl, `MYR` + `P16`                                                   | Nagar et al., _Cell_ 2003                                                                                |
| `2G1T`, `2G2H` | Abl kinase domain, Src-like inactive                                                 | Levinson et al., _PLoS Biol_ 2006                                                                        |
| `5MO4`         | ABL1 **ternary**: asciminib (`AY7`) **and** nilotinib (`NIL`), T334I/D382N           | Wylie et al., _Nature_ 2017, doi:10.1038/nature21702                                                     |
| `5TBY`         | homology model of the human IHM                                                      | Alamo et al., _eLife_ 2017                                                                               |
| `6C1H`         | rat myosin-Ib + actin + calmodulin                                                   | Mentes et al., _PNAS_ 2018, doi:10.1073/pnas.1718316115                                                  |
| `8QYP`, `8QYR` | bovine MYH7 motor domain ± mavacamten (`XB2`)                                        | bioRxiv 2023 → Auguin et al., _Nat Commun_ 2024, doi:10.1038/s41467-024-47587-9                          |
| `9GZ1`–`9GZ3`  | human MYH7 ± mavacamten                                                              | bioRxiv 2025 (deposited citation is a preprint) → McMillan et al., _Sci Adv_ 2026                        |
| `8ACT`         | human β-cardiac myosin folded-back off state                                         | Grinzato et al., _Nat Commun_ 2023, doi:10.1038/s41467-023-38698-w — **considered and replaced**, see §7 |
| `9YRG`, `9YR7` | human β-cardiac myosin IHM (undocked S2-FH) ± mavacamten, Myosin-7/GCN4/EGFP chimera | Somavarapu et al., _Sci Adv_ 2026, doi:10.1126/sciadv.aed6472                                            |

Two forensic notes. `5TBY` has clean provenance — Anderson et al. _PNAS_ 2018, the
challenge's own reference [23], cites it by accession. `6C1H` has none: the other two rows'
holo IDs are the depositions of their cited references, and the myosin holo is the only ID
in Table 1 with no basis anywhere in the document's bibliography. How it got there is
**unverifiable** from public sources — we report what `6C1H` is and do not speculate.

---

## 7. Open items

- **Resolution ceiling — settled, ADR 0009.** The field near-universally applies one — 2.0 Å
  (Wankowicz), 2.5 Å (PocketMiner, CryptoBench, Binding MOAD), 3.0 Å (PASSer/DeepAllo). An
  earlier draft of this bullet proposed **X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å, mandated tier
  exempt**, and claimed every `corrected` and `sensitivity` entry fell in 1.15–3.7 Å. Both
  were wrong. The real span is **1.15–3.40 Å**, and the draft rule would have deleted
  **`8QYP` (2.759 Å)** — the apo of three arms, one of them the _corrected_ Site 2 arm.
  (A related slip in the same sentence: `1OPL`'s RSRZ-outlier figure is **6.5 %**, not 22 % —
  the wwPDB validation report gives `percent-RSRZ-outliers = 6.50`; 22 was a percentile
  slider read as a percentage. Its 3.42 Å and R-free 0.315 are exact.)
  ADR 0009 resolves it: a resolution ceiling is a **selection** rule, so it binds on the ASD
  and generalisability sets (X-ray ≤ 2.5 Å, cryo-EM ≤ 4.0 Å, experimental only, applied
  before any target is examined) and **not** on the primary benchmark, whose arms are
  hand-specified per target rather than drawn from a pool. Resolution, method and R-free are
  disclosed per entry instead.
- **No arm in the primary benchmark is blind.** Corrected 2026-08-20; an earlier version of
  this bullet claimed myosin Site 1 was, and called it "the benchmark's only clean
  measurement". It is not. Every ASD/ASBench record below was re-pulled live rather than
  recalled; the per-arm verdict is the `blind:` field in `manifest.yaml` and the last column
  of §3, now `false` on all eleven.
  - **BCR-ABL1 — not blind.** ASD curates the myristoyl pocket **twice** (`AS001006501`,
    `3PYY`, DPH activator; `AS002023501`, `3K5V`, GNF-2 analogue `STJ`, inhibitor — note the
    second record is *mouse* P00520), so every ASD-trained method has seen it. It is also an
    **APOP** case study (pocket ranked 3 of 14) and an **ESSA** case study — the two leading
    ENM methods, which is the comparison class that matters most to us. The `3PYY` record
    additionally lists `1OPL`/`MYR` as a related complex, so our mandated apo is itself in ASD.
  - **KRAS — not blind, through its homologue.** ASBench curates HRAS (`AS001013301`, `4DLR`)
    with site residues R68, D92, Q95, Y96, Q99; **4 of those 5 are in our frozen KRAS label
    set** (all 5 at the 5.0 Å cutoff, and ASD prints the list truncated with `,etc.`, so this
    is a lower bound), and no predictor's 30–40 % identity dedup separates KRAS from HRAS.
    Separately, Eren 2021 ran GNM + ANM (no MD) on **`4OBE` itself**, treating the α3-L7 site
    as **known** and computing paths to it — not predicting it. That is worse for blindness,
    not better: our exact apo input is a published worked example.
  - **Myosin Site 2 — not blind.** Challenge reference [1] (Zheng 2023) tests this pocket via
    `1MMA`→`1YV3`, the blebbistatin site. That makes it a calibration point.
  - **Myosin Site 1 — not blind either, and this is the correction that matters most.**
    Zheng 2023 reports **two** myosin sites, and the earlier reading stopped one sentence
    short of the second: _"we also found another site at the **N-terminal/converter subdomain
    interface**, which may provide targets for other allosteric agents"_, with **ESSA**
    supplying residues **120, 121, 688, 693, 694** in _Dictyostelium_ numbering. Auguin 2024
    places the mavacamten pocket _"between the **N-terminal** (N-term) and the **Converter**
    subdomains"_ — the same interface. Settled by alignment rather than by wording: `1MMA`↔MYH7
    pairs **673 residues at 52 % identity**, carrying those five onto MYH7 **119, 120, 705,
    710, 711**, of which **3 of 5 are frozen labels** on the `8QYP` arm (120, 710, 711;
    hypergeometric E = 0.11, **P(≥3) = 0.0001**) and 2 of 5 on the `9GZ3` arm (E = 0.08,
    P = 0.0022). Zheng did not name it as the mavacamten site, which makes it a genuine blind
    prediction of this pocket **published in the challenge's own bibliography**.
    What survives is narrower and still worth saying: **no method has been reported on MYH7
    itself** — Zheng and ESSA ran on _Dictyostelium_ myosin II. Site 1 is the arm with the
    _weakest_ prior art, not a blind one, and Zheng's result is now a **bar to clear** rather
    than an absence to exploit.
  - **Two absence claims remain unverified and must not be asserted.** Only **ASBench**
    returns a checkable zero for myosin (live query, "No Complex to display"). **ASD proper**
    renders client-side and its bulk mirrors truncate; **CASBench** offers no enumerable
    listing. Neither absence is established. Worse, ASD2023 reports running **AlloSitePro over
    all 20,386 human proteins**, yielding 66,589 predicted allosteric sites across 17,767 of
    them — MYH7 among them — so ASD's *predicted* pocketome is an unexamined route to prior
    art for every human target here. Check it before any claim of novelty is published.
- **The field's headline numbers are not our bar.** They are mostly computed on
  ligand-stripped holo structures. After UniRef50 dedup, AlloBench finds "none of these
  programs could achieve an accuracy of more than 60 %"; at Jaccard > 0.5 the best are PASSer
  18 % and APOP 15 %. Quote APOP's 88.5 % top-3 alongside AlloBench's 15 %, or quote neither.
  **APOP is the classical bar** — GNM, 10 Å, unsupervised, no MD, no training data, satisfying
  C1/C2/C6 exactly. Neither challenge ENM reference supplies a number: Zheng 2023 is four
  qualitative case studies and Chennubhotla & Bahar 2007 has no ranking task.
- **Decoy surface pockets** need a geometric detector; none is installed. Blocks the second
  negative set the challenge requires.
- **Modified residues** in the chain (trimethyl-lysine `M3L` at 129 and 549 in `8QYP`) are
  kept as polymer nodes and mapped to their parent amino acid, because `label_seq_id` — not
  the ATOM/HETATM flag — decides chain membership. Settled in ADR 0006; whether they carry
  _modified properties_ as network nodes is explicitly out of scope there.
- **Alternate conformations are ignored, not handled — but no longer on trust.**
  `parse_mmcif` keeps every altloc atom and no code filters by `label_alt_id` or occupancy,
  so a residue could enter a label set through a 0.25-occupancy conformer. Four holo entries
  carry altlocs (`5MO4`, `8QYR`, `8QYU`, `9F6C`). Re-deriving every pocket from the primary
  conformer alone returns **the identical label set on all ten arms**, so the defect is
  latent rather than live — and that is now `test_label_sets_do_not_depend_on_a_minor_conformer`
  under `make verify`, not a one-off check recorded in prose. It will still bite on the ASD
  selection set, where the parser needs a real occupancy policy.
- **`9YRH` is not a specificity control.** An earlier draft here claimed it bound
  **omecamtiv mecarbil** (`2OW`) at a _different_ site from mavacamten, and proposed it as a
  negative. That is wrong. Measured ligand-centroid separation is **2.1 Å** from mavacamten
  in `8QYR` and 0.3–0.4 Å from omecamtiv in `5N69`/`8QYU` — it is the _same_ pocket, which is
  the finding in the title of **Auguin et al., _Nat Commun_ 2024,
  doi:10.1038/s41467-024-47587-9: "Omecamtiv mecarbil and Mavacamten target the same myosin
  pocket despite opposite effects in heart contraction"**. (An earlier draft attributed that
  title to Planelles-Herrero et al. 2017, doi:10.1038/s41467-017-00176-5 — impossible on its
  face, since mavacamten had no deposited structure in 2017. The 2017 paper establishes the
  separate and still-needed point that omecamtiv "binds to an allosteric site that stabilizes
  the lever arm in a primed position".) Confirmed independently in
  `evidence/myosin-structural-landscape.md` §3. Two drugs with **opposite** functional
  effects sharing one pocket is evidence the site is allosteric, not evidence of a second
  site. The genuine second site is aficamten's, 34.2 Å away.
- **The IHM arm is frozen as chain A of a hexamer.** `9YRG`/`9YR7` are the folded-back off
  state, and the inter-head interface is the mechanism — label residue 721 is in a 3.34 Å
  inter-chain contact. Whether the network should be one head or the whole IHM is the
  coarse-graining question (Phase 4), and the frozen input takes one head until that is
  settled. Recorded so the choice is visible rather than inherited.
- **The `srx` heavy chain is a Myosin-7/GCN4/EGFP chimera — and there is nothing to trim.**
  An earlier draft listed trimming the residue set to MYH7 as unimplemented work. Measured:
  chain A of `9YRG` models **912 residues spanning 4–943** with gaps at 203–214 and 627–642
  (940 − 28 = 912), and `9YR7` chain A models 4–943 complete. The GCN4 and EGFP portions are
  not modelled in the heavy chain at all; chains C–F are the light chains. So the frozen
  residue set is already native MYH7 numbering end to end, and the frozen `n_residues` = 912
  contains no chimeric residue. Recorded because the concern was real and the answer is not
  obvious from the construct name.
- **Insertion codes are refused, not handled.** No frozen entry has any; `parse_mmcif` raises
  rather than silently merging two residues into one node. This will need extending for the
  ASD generalisability set.
- **The patch null** needs the contact graph, so it lands with network construction.
- **`Ala767` — resolved; it was our misreading, not the paper's error.** An earlier draft
  recorded that "Auguin et al. name Leu120 and Ala767 as mavacamten contacts" and that
  `Ala767` appears in no structure at any cutoff up to 6.0 Å. Re-reading the paper: **A767 is
  an _omecamtiv_ residue, and Auguin explicitly contrasts it with mavacamten** — "the methyl
  ester piperazine ring of **OM** uniquely reaches ... ᶜᵒⁿᵛ⁻ᴴ³**A767**", and "OM stabilizes the
  first turn of this helix but not Mava". We had been looking for it in the XB2 structures,
  where the paper says it should not be. It is also a helix-register claim rather than a
  contact claim: even against `2OW` our 4.5 Å rule returns Phe765 and Gly771 but not Ala767,
  and PDBe's independent interaction analysis of `2OW` in `8QYU` likewise does not list it.
  Excluding it from every label set is correct. **Leu120 is genuinely Auguin's mavacamten
  contact** ("The isopropyl group of Mava uniquely interacts with ⁿ⁻ᵗᵉʳᵐLeu120") and is
  genuinely borderline — 4.5 Å in the 1.80 Å X-ray (`8QYR`) and in `9YP9`, 4.93 Å in `9GZ1`
  chain B, 5.0006 Å in `9GZ2` chain A — which is why it is a label in the X-ray arm and not
  in the cryo-EM arms. That is a cutoff artefact, correctly handled.
- **ASD (`mdl.shsmu.edu.cn/ASD`) serves over HTTP only.** Its wildcard certificate for
  `*.shsmu.edu.cn` expired 2025-12-28, so HTTPS fails certificate validation; plain HTTP
  returns 200. The secondary benchmark (challenge reference [25]) is therefore _not_
  blocked, but any fetch of it must be over HTTP and its integrity checked another way —
  record checksums of whatever we download, since the transport is unauthenticated.
- c-Myc (`1NKP`) is out of scope for this phase. Hazard already recorded: its two Myc copies
  carry different arbitrary numbering offsets (`docs/targets.md`).
- **Two questions for the organisers, and `6C1H` is only the first.** (a) `6C1H` carries
  mavacamten on actin, not myosin — the mandated Site 1 pair has no ground truth. (b) **How
  C5 is to be read.** "Catalytic domains only" taken strictly would trim `1OPL` from 451
  residues to the kinase domain alone, and we have declined that (ADR 0010, accepted) because
  it deletes the SH3–SH2 clamp the myristoyl pocket acts through. That is a defensible
  reading, not a ruling. Until one exists, the whole-chain node set is the primary and **a
  trimmed-domain arm is run as a declared sensitivity analysis on ABL1**, so the answer is
  reported either way rather than depending on which reading a judge holds.
- **The second negative set blocks scoring, not just reporting.** §5 class 2 needs a geometric
  pocket detector; none is installed. Choosing one after seeing method results would make the
  detector a hyperparameter — which detector, what surface definition, how pockets merge, what
  is excluded — so the choice, its version and its full configuration go into `manifest.yaml`
  and are frozen before any method is scored. Same for the patch null: §5 now requires a
  distance-only and a degree-only score to fail against it before any p-value from it counts.
