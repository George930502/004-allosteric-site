# The frozen benchmark — input layer

**Status: frozen 2026-08-24. Six scoreable arms across the three challenge disease areas.**
`uv run allo benchmark verify` re-derives every pinned value from the deposited files and
exits 0 only if nothing moved.

> **Read [`../review/README.md`](../review/README.md) before quoting a number from this page.**
> An audit closed on 2026-09-02, after the organisers answered four questions about the
> benchmark. It ratifies most of this document, corrects seven stated facts in it, and lists the
> decisions it forces. Corrections are recorded there rather than edited in here, so that this
> freeze stays a freeze.

This document covers **what** a method receives and **what** it is scored against. It does
not cover **how** a score is computed. That is a separate layer with its own lifecycle, and
it is frozen in [`evaluation/README.md`](../evaluation/README.md). The two were in one
document until 2026-08-24, and the coupling meant an unfinished null model blocked a
finished input layer.

**What this is for.** The frozen benchmark makes no novelty claim. It is not a contribution.
It is the instrument the contribution will be measured with. Its only job is to let methods
be compared fairly, honestly and neutrally, so that no method class gains a bonus or a
handicap from how the inputs were built. Where a choice would have been more interesting but
less neutral, the neutral one wins. Where a defect is disclosed rather than repaired, the
disclosure lets a reader price it.

**There is a second set.** This document is the PRIMARY benchmark: the three disease areas
`CHALLENGE.md` Table 1 names. Three targets cannot support a claim about the method in
general — a sign test over N target-level effects has a minimum attainable one-sided p of
2^-N, which at N = 3 is 0.125 whatever the result. (That floor binds tests invariant to sign
flips; two constructions escape it and license less — `evaluation/README.md` §8.) The
generalisability and
scalability claims therefore come from the **secondary** set,
[`secondary/README.md`](../secondary/README.md): nine further targets, frozen the same day,
through this same code, under these same clauses plus four selection clauses (ADR 0021).
Both sets verify together.

```bash
uv run allo benchmark show      # what is frozen, derived live from the deposited files
uv run allo benchmark verify    # exit 0 iff nothing has moved since the freeze, BOTH sets
uv run allo benchmark verify --set secondary   # one set only
```

| File            | What it is                                                                      |
| --------------- | ------------------------------------------------------------------------------- |
| `manifest.yaml` | the choices — entries, chains, ligands, cutoff, active-site rules. Hand-edited. |
| `frozen.json`   | the consequences — residue sets, label sets, geometry. Generated, never edited. |
| `audit/`        | forensic dossier per target pair, every fact carrying its provenance            |
| `evidence/`     | the literature basis, indexed in [`evidence/README.md`](../evidence/README.md)  |

---

## 1. What an apo/holo pair is, operationally

"Apo" is used loosely in this literature, and the looseness is what lets a broken benchmark
through. Three readings circulate: ligand-free of anything, ligand-free at the site of
interest, and ligand-free with respect to the drug under study. They give different answers
for every target here. `4OBE` holds GDP·Mg and `9GZ3` holds ADP·Mg·Pi, and both are routinely
called apo.

**We adopt the site-apo reading as repository policy.** That reading is the majority one in
the field, but it is not unanimous: AHoJ, AHoJ-DB, CryptoBench, PocketMiner and ASD v3.0 all
apply it, while Wankowicz 2022 requires global ligand-freedom. The clauses below are one
normative repository definition. Each clause is tagged **[IN-DOMAIN]**, **[BORROWED]** or
**[REPOSITORY POLICY]** according to its actual authority. Full clause-by-clause traces with
quotes: [`evidence/allosteric-pair-definition.md`](../evidence/allosteric-pair-definition.md).

> An **apo/holo pair for allosteric-site prediction** is an ordered pair of experimentally
> determined structures of the same gene product satisfying:
>
> **(i) Effector [IN-DOMAIN + REPOSITORY POLICY].** The _holo_ member contains the allosteric
> effector, identified by its PDB chemical component ID, at the site to be predicted. Site
> residues are those within a **declared** radius of its heavy atoms.
> **(ii) Provenance of label [IN-DOMAIN].** The site is allosteric because _functional_
> evidence says so. Distance from the active site is neither necessary nor sufficient.
> **(iii) Site-apo [BORROWED + REPOSITORY POLICY].** The _apo_ member contains **no ligand of
> any kind within the _scoreable_ portion of that site** — the labels a method is actually
> asked to find. Contacts to the full label set are recorded beside it and do not disqualify:
> where the allosteric and orthosteric sites share a border, the catalytic cofactor touches
> labels that are themselves active-site residues. That is two sites adjoining, not a
> modulator in the pocket.
> **(iv) Identity [IN-DOMAIN].** Same protein at **≥ 90 % sequence identity**, differences
> enumerated.
> **(v) Assembly [IN-DOMAIN].** Same oligomeric state, and the modelled state should be the
> biological assembly.
> **(vi) Second site [REPOSITORY POLICY].** Orthosteric occupancy recorded for **both**
> members, and the active-site rule stated.
> **(vii) Non-circularity [BORROWED + REPOSITORY POLICY] — a rule about the _procedure_, not
> about the biology.** No residue of the propagation source may be scored as a candidate for
> the site being predicted. The allosteric site is free to act _on_ the source; that is what
> allostery to a catalytic site **is**. Each arm declares which function the site is
> allosteric for, and whether that function is measured at the source.
> **(viii) State disclosure [REPOSITORY POLICY].** The functional state of each member is
> **stated**, and the pocket-lining change reported. State difference is _disclosed, not
> required_.

**Comparator disclosure, outside pair validity.** A comparator trained on ASD, ASBench or
CASBench and evaluated on a target those databases curate **is not blind**, and must be
labelled. Blindness is a property of an evaluation procedure, not of an apo/holo pair, so it
is deliberately not a ninth admission clause (ADR 0017).

### Where the clauses come from

| Clause     | Authority                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (i) radius | ASD v2.0 **6 Å**; CASBench **5 Å**; CryptoSite and PocketMiner **5 Å**; AHoJ and CryptoBench **4.5 Å**; ASBench and AlloBench **4 Å**; Amor **3.5 Å** (a caspase-1 result, not a set-wide convention). Four incompatible conventions coexist. **Our 4.5 Å matches AHoJ and CryptoBench and is declared at first use.** A number reported against one cutoff is not comparable to a number reported against another                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| (ii)       | **Two statements, two scopes — and the one we rely on is the protein-general one.** IUPHAR XC §III recommends the _term_ (doi:10.1124/pr.114.008862, full text read at PMC11060431): "reserved for instances where the properties of one ligand **(small molecule or protein)** are altered upon binding of a second ligand at a nonoverlapping, topographically distinct site and where, **ideally**, reciprocity in this interaction can be demonstrated". The parenthetical is what makes this sentence protein-general, and it is the sentence clause (ii) rests on. Reciprocity is IUPHAR's ideal case, **not** its threshold. Table 1 of the same article defines the _site_ — "A binding site on a **receptor macromolecule** that is nonoverlapping and spatially distinct from, but **conformationally linked to**, the orthosteric binding site" — but its caption reads "Terms used to describe **receptor** allosterism", and no target in this repo is a receptor in that sense. So Table 1 is quoted for the "conformationally linked" qualifier only, and the threshold comes from §III. ASD v1 sets the evidence bar at "at least three cases of experimental evidence". A crystal structure alone is on nobody's list |
| (iii)      | **Borrowed, then RELAXED by us — corrected 2026-08-24, this row said "narrowed" and that reads backwards.** ASD's "apo" is _modulator_-relative; no allostery source states the site-relative reading. The **scoreable-portion** qualifier is ours, and it narrows the _region checked_, which **lowers** the admission bar. Two published site-apo rules reject on contact to **any** label residue: PocketMiner removes apo candidates "with ligands ... within 5 Å of all MOAD-assigned biologically relevant residues", and Clark 2020 removes "any structures containing HET material apart from water (HOH) within 4.5 Å of any unified binding site residue". GDP·Mg contacts **5 of the 21** KRAS labels, so **both KRAS arms would fail both published tests and pass ours**. The reasoning behind the relaxation stands — an adjoining catalytic cofactor is not a modulator in the pocket — but it is a weakening, and these are the arms that depend on it                                                                                                                                                                                                                                                                 |
| (iv)       | ESSA — "at least 90% sequence identity". The allostery field's only published apo↔holo pairing threshold. Cryptic-site benchmarks are stricter and disagree with each other: PocketMiner 100 %, Clark 95 %, CryptoBench a UniProt group                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| (v)        | Amor et al. exclude on "a mismatch between the oligomeric state of the active and inactive structures". AlloBench downloads "the **biological assembly** structures" (doi:10.1021/acsomega.5c01263), so both halves are the field's, not ours                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| (vii)      | AlloPred — "Active site residues were not counted as being in any pocket … in order to avoid direct perturbation of the site at which the effect was measured". Note what that source is a rule about: **pocket membership inside AlloPred's own procedure**, not a biological requirement on the modulator. Read as biology it would disqualify KRAS by construction, because Ostrem 2013's evidence for the S-IIP being allosteric _is_ that it subverts nucleotide preference at the site we use as the source                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

### No minimum distance, and that is not an oversight

No formal definition of an allosteric site in any source we have **read** contains a minimum
separation from the active site. Checked and read: ASD v1/v2/v3/2019/2023, CASBench, ASBench,
AlloBench, and IUPHAR XC — whose criteria are topological throughout ("nonoverlapping",
"spatially distinct", "topographically distinct") and never metric. The same article allows a
**bitopic** ligand to occupy both sites at once, so even competitive kinetics do not by
themselves refute an allosteric site.

**IUPAC Gold Book 14107 is checked but NOT read, and an earlier version of this paragraph
claimed more than that.** It said the entry "is protein-general rather than receptor-scoped".
That is not established. Crossref confirms the entry exists and gives its title and its single
parent reference; it carries no definition text. Every route to the text failed: the IUPAC
host returns 403 to automated fetches, the legacy host fails its TLS handshake, three
proxies returned 522, and `web.archive.org` is blocked for the tool although a snapshot exists.
Two web searches rendered the entry's opening differently from each other, which proves at
least one is confabulating, so none of it is quotable. **Correction to the parent citation as
well:** doi:10.1351/PAC-REC-09-05-03 is "Glossary of terms used in biomolecular screening",
Proudfoot et al., _Pure Appl Chem_ 2011;83(5):1129–1158 — a screening-assay glossary, not a
pharmacology nomenclature recommendation. On provenance alone IUPHAR XC is the stronger
authority, and nothing here depends on 14107.

CASBench measures the opposite — "in **30%** of cases, the catalytic and
allosteric sites either overlap or share a common border"
(doi:10.32607/20758251-2019-11-1-74-80). A distance filter on a label set would discard about
a third of curated allosteric sites. Clause (vii) is therefore a **membership** rule, not a
distance rule.

### What each site is allosteric _for_

Clause (vii) declares this rather than forbidding it, and it is not uniform:

| Arm                        | The site is allosteric for                                                                                                 | Measured at the propagation source?                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `kras_g12c_*`              | nucleotide preference (GTP→GDP, mant-dGDP competition) **and** Raf effector binding — Ostrem 2013, doi:10.1038/nature12796 | **Yes, in part.** The nucleotide half is measured at the GDP·Mg site, which is this arm's source. The Raf half is not |
| `bcr_abl1_*`               | kinase catalytic activity, via the SH3–SH2 clamp — Zhang 2010, doi:10.1038/nature08675                                     | **Yes** — activity is measured at the catalytic site, the source under `{from_motifs: [VAIK, HRD, DFG]}`              |
| `cardiac_myosin_corrected` | the SRX/DRX equilibrium and lever-arm priming — Rohde 2018, doi:10.1073/pnas.1720342115                                    | **No.** Mavacamten's reported effect is on the population of the super-relaxed state, not on the ATP site directly    |

### A two-structure pair cannot establish allostery

Fenton states the requirement plainly: allostery "is more strictly defined in functional terms
as a comparison of how one ligand binds in the absence, versus the presence, of a second
ligand … a study of allostery must consider **four complexes and not just two**"
(doi:10.1016/j.tibs.2008.05.009). An apo/holo pair supplies one corner of that cycle. Every
arm therefore carries an `allosteric_evidence` field naming the functional experiment, and
the allostery is inherited from that citation and never from the geometry (ADR 0007).

### Cryptic is not a synonym

A cryptic site is a **structural** property of one apo/holo pair. An allosteric site is a
**functional** property. Vajda 2018 classified the CryptoSite validated high-affinity set:
**8 of 19** cryptic sites are allosteric (doi:10.1016/j.cbpa.2018.05.003). The converse
fraction — how many allosteric sites are cryptic — is **not reported anywhere in the
literature**, checked again against CryptoBank 2025. Crypticity is reported here as a
difficulty axis (§4) and is never a validity test for a pair.

---

### The secondary set's four extra clauses, applied here as a diagnostic

Clauses (ix) to (xii) bind the **secondary** set and not this one, because they are selection
rules and a selection only exists where there is a pool (ADR 0009). `CHALLENGE.md` Table 1 is
not a pool. Applying them here anyway is cheap, and it closes the "different rules for
different sets" objection before a reader raises it. Added 2026-09-02. **Diagnostic only: no
arm is admitted or rejected on these rows.**

| Clause                                                         | Verdict on this set                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **(ix)** single-chain effector lining                          | **passes on every arm.** Both arms changed on 2026-09-02 share their holo member with an arm already measured — `5MO4` and `9GZ2` — so the verdict did not move                                                                                                                                                                                     |
| **(x)** apo occupant classification                            | **passes by construction**, because it is clause (iii) restricted to the scoreable set, which this set already enforces                                                                                                                                                                                                                             |
| **(xi)** structure admission, X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å | **fails on two entries.** `1OPL` is X-ray at **3.42 Å** and `5TBY` is deposited as electron microscopy at **20.00 Å**. Every other pinned entry passes: `4LDJ` 1.15, `4OBE` 1.24, `6OIM` 1.65, `2G2H` 2.00, `5MO4` 2.17, `9GZ2` 2.9, `9GZ3` 3.4. Measured from `_refine.ls_d_res_high` and `_em_3d_reconstruction.resolution` in the tracked mmCIFs |
| **(xii)** within-set redundancy                                | **fails by design.** Each disease area contributes a mandated arm and a corrected arm on the same protein and the same site. That is the point of the tier split, not a defect                                                                                                                                                                      |

**The (xi) failures are the two arms this set already declares defective**, and both are
non-confirmatory for reasons that subsume the resolution. `1OPL` is at the 0.4th absolute
percentile of the PDB for RSRZ outliers; `5TBY` is a homology model whose contact graph
disagrees with the measured structure at long-range Jaccard 0.471. Neither carries a
statistical decision.

---

## 2. Audit of the challenge's assignments

All three assigned pairs are defective. Every fact below was re-derived from the deposited
coordinate files and cross-checked against live RCSB records. Full dossiers in `audit/`.

| Pair                         | Verdict                | Deciding evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KRAS `4OBE`→`6OIM`           | usable, wrong genotype | `4OBE` residue 12 is **GLY** in both chains, `_struct_ref_seq_dif` lists no mutation, and RCSB reports `rcsb_mutation_count = 0`. `6OIM` is G12C plus C51S/C80L/C118S, and its `_struct_conn` records a `covale` from `A/CYS12.SG` to `A/MOV303.C25` at **1.805 Å**. The apo input lacks the cysteine the holo drug is bonded to. Repaired by `4LDJ`.                                                                                                                                                                                                      |
| BCR-ABL1 `1OPL`→`5MO4`       | **fails clause (iii)** | `1OPL` chain A contains `MYR` **in the myristoyl pocket** and `P16` in the ATP site of both chains. Measured: MYR contacts **16 of the 20** label residues, nearest approach **3.29 Å**, and those 16 are a strict subset of asciminib's 20 (Jaccard 0.80). The mandated apo already is holo at the site to be predicted. Repaired by `2G2H`.                                                                                                                                                                                                              |
| Cardiac myosin `5TBY`→`6C1H` | **unusable both ways** | `6C1H` is rat unconventional **myosin-Ib** (Q05096) with rabbit actin (P68135) and calmodulin (P0DP23), 3.9 Å cryo-EM, titled "…Actin-bound Myosin States…". Its only heteroatoms are ADP and Mg. Mavacamten is component `XB2` and appears in exactly six entries — `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7` — none of them this one. `5TBY` is a SWISS-MODEL homology model on a **tarantula** template (`3JBH`), rigid-body fitted, deposited at 20 Å, with 954 modelled residues in chain A and **zero heteroatoms**. Repaired by `9GZ3`/`9GZ2`. |

**The myosin failure is a factual error in the challenge statement, not a judgement call.**
It is question (a) for the organisers (§6). `5TBY` has clean provenance — the challenge's own
reference [23] cites it by accession. `6C1H` has none: the other two holo IDs are the
depositions of their cited references, and `6C1H` is the only ID in Table 1 with no basis
anywhere in the document's bibliography. How it got there is unverifiable from public
sources. We report what `6C1H` is and do not speculate.

Two precision notes, because both are easy to overstate. RCSB classifies `5TBY` as
`structure_determination_methodology: experimental`, so do not call it "not an experimental
structure". Say instead what is measurable: 20 Å, a `refine` category carrying **three**
non-null fields and no refinement statistic at all — `entry_id`, `pdbx_refine_id` =
`ELECTRON MICROSCOPY` and `ls_d_res_high` = 20.00, with the other 119 fields null — the
**only MODEL FITTING
software named in `em_software` being "UCSF Chimera"**, and 41 `covale` records at physically
impossible
distances such as 1.083 Å. And the KRAS genotype mismatch touches one residue of 21 labels;
it is a recorded caveat, not a disqualification.

### Dimensions checked beyond ligand identity

An audit that only reads the ligand list misses the ways a pair fails quietly.

| Dimension                          | Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ligand fit to density**          | `6OIM` MOV **RSCC 0.908**, `5MO4` AY7 **0.946** — both strong. Cryo-EM entries carry no deposited ligand-fit score at all, so `9GZ2` rests on an unscored placement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Crystal packing at the pocket**  | Not enriched anywhere (`4OBE` 48 % of labels vs 40 % background, OR 1.37, **p = 0.33**), so no crypticity verdict is a lattice artefact. `4OBE`'s switch-II is lattice-engaged where `4LDJ`'s is not, yet `4LDJ` — the less packed structure — clashes **more** on transplant.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Sequence identity, apo↔holo**    | 97.6–100 % on every arm, pinned as `sequence_agreement.identity`. Clause (iv)'s >= 90 % is a floor, not the operative number: every arm clears PocketMiner's and Clark's stricter published bars in fact.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Resolution difference**          | Reported in section 4a. Four of five scoreable primary arms exceed the 0.3 A community guidance, `bcr_abl1_mandated` by 1.25 A. **Added 2026-08-24** — this dimension was not checked before.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Mutations inside the label set** | Exactly one across all six arms: `kras_g12c_mandated` has **`GLY12->CYS`**. `kras_g12c_corrected` is clean, which is the sharpest single argument for `4LDJ`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Alternate conformations**        | Present in `5MO4`. Re-deriving every pocket from the primary conformer alone returns the **identical** label set on every arm, and that is `test_label_sets_do_not_depend_on_a_minor_conformer` under `make verify`, not a promise.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Chain breaks near the site**     | None abuts a label in any arm. Myosin has gaps at 203–213 and 625–643; both are far from the site.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Order at the site**              | Label residues are as ordered as the chain or better (median B-factor ratio 0.78–1.10). The sites are not modelled into noise. **Qualified 2026-09-02, and the qualification matters for myosin.** The ratio is a within-entry comparison, so it is only as meaningful as the column it is computed from, and on the two myosin entries that column is not a refined B-factor. `5TBY`'s runs **0.00 to 7.30, mean 2.45** over 20 357 atoms, against `9GZ3`'s 16.82 to 108.47, and it has no refinement statistic behind it. `9GZ2`'s mavacamten — the ligand that defines **both** myosin label sets — carries **B = 0.00 on all 20 atoms**. Read the myosin row as "no evidence of disorder at the site", never as "measured order". |
| **Biological assembly**            | Assembly 1 is derived and frozen for both members of every arm. Target copies match on every pair.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

---

## 3. The frozen input layer

One disease area from `CHALLENGE.md` Table 1 gives two arms: the **mandated** pair exactly as
specified, and a **corrected** pair for the same protein and the same site. Both are pinned
before any method exists, so neither choice can be tuned to a result (ADR 0003).

| Arm                        | Tier      | Apo      | Holo     | Effector |   N | Labels | Scoreable | Candidates | Prevalence |
| -------------------------- | --------- | -------- | -------- | -------- | --: | -----: | --------: | ---------: | ---------: |
| `kras_g12c_mandated`       | mandated  | `4OBE`:A | `6OIM`:A | `MOV`    | 169 |     21 |        16 |        146 |     11.0 % |
| `kras_g12c_corrected`      | corrected | `4LDJ`:A | `6OIM`:A | `MOV`    | 170 |     21 |        16 |        148 |     10.8 % |
| `bcr_abl1_mandated`        | mandated  | `1OPL`:B | `5MO4`:A | `AY7`    | 365 |     17 |        17 |        354 |      4.8 % |
| `bcr_abl1_corrected`       | corrected | `2G2H`:A | `5MO4`:A | `AY7`    | 272 |     18 |        18 |        261 |      6.9 % |
| `cardiac_myosin_mandated`  | mandated  | `5TBY`:A | `9GZ2`:A | `XB2`    | 954 |     12 |        12 |        932 |      1.3 % |
| `cardiac_myosin_corrected` | corrected | `9GZ3`:A | `9GZ2`:A | `XB2`    | 764 |     12 |        12 |        743 |      1.6 % |

**Two mandated arms changed on 2026-09-02, after the organisers answered four questions**
([`../review/00-official-reply.md`](../review/00-official-reply.md)). Their answers outrank
`CHALLENGE.md` where the two disagree.

- `bcr_abl1_mandated` moved from chain A to **chain B**, which the organisers designated.
  Chain A holds `MYR` in the myristoyl pocket and is therefore holo at the site it is asked
  to predict. Chain B is empty there. The cost is that chain B was rigid-body placed with
  three group B-factors, so its contact graph is largely a domain placement. The arm is
  **non-confirmatory** and prints four measured defects beside every number (ADR 0029).
- `cardiac_myosin_mandated` is **frozen for the first time**, against `9GZ2` in place of the
  `6C1H` of Table 1, which the organisers sanctioned. `6C1H` is bovine myosin-Ib and supplies
  no label set. `transfer_labels(9GZ2:A, 5TBY:A, XB2, 4.5 A)` returns all twelve
  mavacamten-contact residues with none unmapped, so the ADR 0016 label blocker is gone. Both
  input defects stand and are measured, not argued: the source comes from a family motif
  triple at Jaccard 0.48-0.52 against the ligand-derived source, and the 20 A homology model
  agrees with the measured `9GZ3` structure at long-range contact Jaccard **0.471**. The arm
  is **non-confirmatory** and prints both numbers beside every result (ADR 0031).

The confirmatory family is unchanged: the three `corrected` arms, and nothing else.

**N is what a method receives; `n_candidates` is what it is scored against.** They are two
different numbers and must never be swapped. `N` is every modelled residue of the frozen
chain (ADR 0010). The candidate set removes the residues that would score by construction
rather than by evidence — the propagation source. The same argument that removes a source
residue from the positives removes it from the negatives; leaving it in the negatives
penalises connectivity methods and no other class, by 44–62 % of AUC-PR (ADR 0011).

**The scoreable label set is the positive class.** It is the label set minus any label that
is itself a propagation-source residue. This is a circularity guard on the metric, not a
claim that the excluded residue is non-allosteric: a label inside the source scores maximally
by construction and therefore measures nothing. The rule is **set membership, not distance**.
Only KRAS loses labels this way (21 → 16), because its pocket borders the nucleotide site.

**A method never receives the deposited mmCIF object.** `allo.inputs.apo_input(target)`
returns an immutable, ligand-free, single-chain view holding exactly the frozen node set. It
fails closed on the apo file's sha256, has no free-form accession resolver, and cannot reach
`data/raw/eval` or `structures/holo`. Modified residues are normalised to their parent amino
acid before prediction, so a PTM cannot create a contact edge (ADR 0006).

### The active site is a rule, not a list

`active_site` is derived from the apo entry alone, so `verify` actually checks it. A pinned
list would only be compared against itself, and would break the moment an entry used another
numbering convention — which the ABL1 entries do (ADR 0005).

| Arm                                 | Rule                              | Derived source residues |
| ----------------------------------- | --------------------------------- | ----------------------: |
| `kras_g12c_mandated` / `_corrected` | `{from_ligands: [GDP, MG]}`       |                 23 / 22 |
| `bcr_abl1_mandated` / `_corrected`  | `{from_motifs: [VAIK, HRD, DFG]}` |                 11 / 11 |
| `cardiac_myosin_corrected`          | `{from_ligands: [ADP, MG, PO4]}`  |                      21 |

---

## 4. The benchmark's difficulty axes

**The benchmark poses one cryptic-pocket problem, one proximal-site problem, and one
pre-formed distal-pocket problem.** Freezing the inputs let us measure that before measuring
any method on it, which is the difference between crediting a method and crediting an easy
instance. Nothing in this section is a validity test.

**Axis 1 — crypticity.** Superpose the holo onto the apo locally (the shell within 20 Å of
the pocket centroid, pocket residues excluded from the fit), then transplant the effector and
count clashes below 2.5 Å.

| Arm                        | Nearest apo atom to the transplanted effector | Clashes | Reading                                                   |
| -------------------------- | --------------------------------------------: | ------- | --------------------------------------------------------- |
| `kras_g12c_mandated`       |                                        0.75 Å | 14/41   | genuinely cryptic                                         |
| `kras_g12c_corrected`      |                                        0.69 Å | 18/41   | genuinely cryptic                                         |
| `bcr_abl1_mandated`        |                                        2.63 Å | 0/31    | pre-formed — and unsurprising, the pocket holds myristate |
| `bcr_abl1_corrected`       |                                        1.95 Å | 2/31    | pre-formed even with the pocket empty                     |
| `cardiac_myosin_mandated`  |                                        1.70 Å | 8/20    | between the two readings; see below                       |
| `cardiac_myosin_corrected` |                                        2.63 Å | 0/20    | pre-formed                                                |

**Re-derived from `frozen.json` on 2026-09-03, and the note that stood here for a day was
wrong.** That note said `bcr_abl1_mandated`'s 2.60 Å was stale after ADR 0029's move to `1OPL`
chain **B**, that `cardiac_myosin_mandated` had no row although ADR 0031 froze it, and then
that **neither quantity is in `frozen.json`**. Both are: `transplant_min_distance` and
`transplant_clashes`, per arm, for all six arms. The two rows are now derived from the freeze
like every other table on this page, and
`test_the_primary_readme_quotes_the_transplant_the_freeze_derives` re-derives them. The
lesson is the round's own: a claim that a number cannot be derived is itself a claim, and it
needs the same check as the number.

`cardiac_myosin_mandated` gets no verdict word, because the two words in that column were
assigned by judgement and it sits between them: the nearest apo atom is closer than either
pre-formed arm and further than either cryptic one, and 8 of 20 effector atoms clash. It is a
homology model on the apo side (ADR 0031), so the geometry behind both numbers is partly
invented and a crispier reading would be reading the model. The arm is non-confirmatory and
prints its measured defects, so nothing rests on this.

Pocket-lining RMSD does **not** tell the same story, and the sentence that said it did was
wrong by a factor of 52 on one arm. Re-derived from `frozen.json` on 2026-09-03:

| arm | core RMSD | pocket-lining RMSD | pocket max |
| --- | ---: | ---: | ---: |
| `kras_g12c_mandated` | 1.07 Å | 2.61 Å | 8.9 Å |
| `kras_g12c_corrected` | 1.05 Å | 2.62 Å | 8.9 Å |
| `bcr_abl1_mandated` | **22.79 Å** | **26.31 Å** | 36.8 Å |
| `bcr_abl1_corrected` | 1.72 Å | 2.38 Å | 9.6 Å |
| `cardiac_myosin_mandated` | 6.82 Å | 2.94 Å | 5.3 Å |
| `cardiac_myosin_corrected` | 1.18 Å | 1.10 Å | 1.9 Å |

This page previously read "ABL1 0.50 Å mandated", a pre-chain-B value, immediately before
CryptoBench's 2 Å cryptic-site criterion — so a reader used it to classify the arm as
maximally pre-formed. At 26.31 Å the two halves are not the same fold in the same place, which
is the measured defect ADR 0029 records and the reason that arm is non-confirmatory.
CryptoBench's 2 Å entry criterion is quoted as a yardstick and not as a pass mark.

### 4a. What the difference numbers are measured against

**Added 2026-08-24. Every number in this section is a difference between two crystals, and a
resolution difference confounds all of them.** The field's most recent community-standards
paper says so directly: "Some general guidelines include using datasets with resolutions
within **0.3 Å**, identical space groups, and unit cell dimensions that differ by no more than
10 %" — Wankowicz & Fraser, _Ten rules for a structural bioinformatic analysis_, _PLoS Comput
Biol_ 2025, doi:10.1371/journal.pcbi.1013094, Recommendation 8. Wankowicz 2022
(doi:10.7554/eLife.74114) is stricter still at 0.1 Å. Neither is an allostery source, and
neither is an admission clause here. Both describe exactly the comparison Axis 1 and the
pocket-lining RMSD make.

Read from the frozen bytes, not from RCSB prose:

| Arm                        | apo, method, Å     | holo, method, Å    |     Δres | Space groups                      |
| -------------------------- | ------------------ | ------------------ | -------: | --------------------------------- |
| `kras_g12c_mandated`       | `4OBE` X-ray 1.24  | `6OIM` X-ray 1.65  | **0.41** | `C 1 2 1` → `P 21 21 21` — differ |
| `kras_g12c_corrected`      | `4LDJ` X-ray 1.15  | `6OIM` X-ray 1.65  | **0.50** | `P 21 21 21` both                 |
| `bcr_abl1_mandated`        | `1OPL` X-ray 3.42  | `5MO4` X-ray 2.17  | **1.25** | `C 2 2 21` both                   |
| `bcr_abl1_corrected`       | `2G2H` X-ray 2.00  | `5MO4` X-ray 2.17  |     0.17 | `P 21 21 2` → `C 2 2 21` — differ |
| `cardiac_myosin_corrected` | `9GZ3` cryo-EM 3.4 | `9GZ2` cryo-EM 2.9 | **0.50** | n/a — single-particle             |

**Four of the five exceed 0.3 Å, and three of the five sit in different space groups.** In the
secondary set, `smyd3` (0.42 Å), `glucokinase` (0.64 Å) and `ecoli_cps` (0.30 Å, exactly at the
limit) exceed or reach it; the other six are 0.06–0.25 Å and share a space group in five of six.

**This is a disclosure, not a repair, and no arm is removed for it.** Requiring 0.3 Å would
delete the KRAS arms, which the challenge mandates, and would delete both ABL1 arms with them.
The consequence is bounded and specific: read Axis 1's clash counts and the pocket-lining RMSDs
as **upper bounds on the conformational difference**, because part of each is a difference in
how well the two maps resolve side chains. `bcr_abl1_mandated` at 1.25 Å is the arm where that
caveat bites hardest, and it is already the arm that fails clause (iii).

**Axis 2 — proximity to the active site.** Minimum Cα distance to the nearest source residue.
The frozen `distance_to_active_site` is computed over the **full** label set, so it is quoted
here over the full set. The **scoreable** set is what a method is scored against, and on KRAS
the two differ, because clause (vii) removes the label that sits inside the source.

| Arm                        | full: min / median / max | scoreable: min / median / max | Reading                                         |
| -------------------------- | -----------------------: | ----------------------------: | ----------------------------------------------- |
| `kras_g12c_corrected`      |       0.0 / 9.2 / 18.2 Å |       **3.8** / 10.7 / 18.2 Å | proximal; the S-IIP borders the nucleotide site |
| `bcr_abl1_corrected`       |     10.8 / 17.5 / 30.1 Å |          10.8 / 17.5 / 30.1 Å | genuinely distal                                |
| `cardiac_myosin_corrected` |     16.5 / 27.6 / 35.6 Å |          16.5 / 27.6 / 35.6 Å | the most distal site in the set                 |

The two columns differ on the KRAS arms and nowhere else in this set. `kras_g12c_mandated`
reads 0.0 / 9.5 / 18.3 Å full and 3.8 / 10.6 / 18.3 Å scoreable. This caption said "scoreable"
against the full-set numbers until 2026-08-24, which overstated the KRAS case: the nearest
**scored** label is 3.8 Å from the source, not 0.0 Å.

A distance-only baseline must be reported beside every method. **It is weaker than this
section claimed until 2026-08-24.** Measured on the frozen 4.5 A contact graph, scoring each
candidate by minus its distance to the source gives AUC-ROC **0.589** on `kras_g12c_mandated`
(1 hit in the top 5, 2 of 16 in the top 16), **0.215** on `bcr_abl1_corrected` and **0.335** on
`cardiac_myosin_corrected` — and, re-measured at the 2026-09-02 re-freeze, **0.588** on
`kras_g12c_corrected`, **0.385** on `bcr_abl1_mandated` and **0.442** on
`cardiac_myosin_mandated`, so it is below chance on **four of six** arms. An _oracle_ distance band,
fitted to the answer, reaches only 0.664 on KRAS. "Close to unbeatable by construction" was an
inference from the proximity table and is contradicted by the measurement. The honest statement
is narrower: KRAS is the arm where proximity helps most, and it still does not carry the arm.

**Prior art, recorded now so it counts as prior art.** No arm in this benchmark is blind, and
the `blind:` field in `manifest.yaml` says so per arm with its reason. The sharpest case: the
KRAS S-IIP was predicted classically by Grant 2011 (120 ns MD plus FTMap), two years before
Ostrem — pocket p2 covers 6 of 16 scoreable labels, Jaccard 0.24. The bar to clear is
therefore not zero on any target.

---

## 5. Provenance of every structure used

`manifest.yaml:structure_provenance` pins the exact wwPDB version label, versioned URL and
decompressed SHA-256 for all eight entries that contribute to this set's `frozen.json`, and the
secondary manifest does the same for its eighteen. The archive test downloads all twenty-six
URLs and rechecks byte identity. The tracked corpus under `structures/apo/` and
`structures/holo/` retains those twenty-six plus the two excluded mandated-pair structures —
28 files, 7.83 MiB — as an offline fallback (ADR 0014). Prediction code receives bytes only
through target-bound `allo.inputs.apo_input`.

| PDB            | What it is                                                    | Primary citation as deposited                              |
| -------------- | ------------------------------------------------------------- | ---------------------------------------------------------- |
| `4OBE`, `4LDJ` | KRAS WT and G12C, GDP·Mg                                      | Hunter et al., _PNAS_ 2014, doi:10.1073/pnas.1404639111    |
| `6OIM`         | KRAS G12C + sotorasib (`MOV`)                                 | Canon et al., _Nature_ 2019, doi:10.1038/s41586-019-1694-1 |
| `1OPL`         | autoinhibited c-Abl, `MYR` + `P16`                            | Nagar et al., _Cell_ 2003                                  |
| `2G2H`         | Abl kinase domain, Src-like inactive                          | Levinson et al., _PLoS Biol_ 2006                          |
| `5MO4`         | ABL1 **ternary**: asciminib (`AY7`) **and** nilotinib (`NIL`) | Wylie et al., _Nature_ 2017, doi:10.1038/nature21702       |
| `9GZ2`, `9GZ3` | human MYH7 motor domain ± mavacamten (`XB2`), primed state    | McMillan et al., _Sci Adv_ 2026                            |
| `5TBY`         | homology model of the human IHM — **excluded**, see §2        | Alamo et al., _eLife_ 2017                                 |
| `6C1H`         | rat myosin-Ib + actin + calmodulin — **excluded**, see §2     | Mentes et al., _PNAS_ 2018, doi:10.1073/pnas.1718316115    |

---

## 6. Open items

Three of these belong to later phases and are listed so they are not rediscovered.

- **Two questions for the organisers.** (a) `6C1H` is the wrong protein and contains no
  mavacamten, so the mandated cardiac-myosin pair has no ground truth. What was intended?
  (b) How is C5 ("catalytic domains only") to be read? Taken strictly it would trim `1OPL`
  from 451 residues to the kinase domain alone. We have declined that reading (ADR 0010,
  accepted) because it deletes the SH3–SH2 clamp the myristoyl pocket acts through. That is
  a defensible reading, not a ruling.
- **Decoy surface pockets — CLOSED 2026-08-25** (ADR 0024). pyKVFinder 0.9.3 at its published
  defaults, frozen in `evaluation/manifest.yaml` before any method ran. The per-arm power
  floor is disclosed. **Re-frozen at protocol version 3** on `n_detected` alone, after the
  organisers answered that no detector is prescribed (ADR 0030): the five primary arms went
  from 3 / 3 / 24 / 9 / 41 decoys to 13 / 18 / 45 / 31 / 84, and the sixth arm has 139. The
  per-arm floor still binds on `kras_g12c_mandated` (0.071) and `kras_g12c_corrected` (0.053),
  so the negative class (b) cannot reject at α = 0.05 on **two of six** arms. The family is
  tested by a Fisher combination instead.
- **The matched-patch null — CLOSED 2026-08-25** (ADR 0023, clearing ADR 0018). It does not
  hold its size everywhere: anti-conservative on both BCR-ABL1 arms, conservative on myosin.
  The threshold is calibrated per arm instead, capped so it can only tighten.
- **The ASD selection set does not exist** (ADR 0012). Every hyperparameter must be chosen on
  it and nowhere else, or Phase 2's ablations are selected on this frozen benchmark, which is
  test-set fitting even with no holo import. Phase 1.7. Note that ASD serves over HTTP only —
  its wildcard certificate for `*.shsmu.edu.cn` expired 2025-12-28 — so any fetch must record
  checksums, because the transport is unauthenticated.
- **c-Myc (`1NKP`) is out of scope for this phase** (ADR 0020). Hazard already recorded: its
  two Myc copies carry different arbitrary numbering offsets (`docs/targets.md`).
- **Insertion codes are refused, not handled.** No frozen entry has any; `parse_mmcif` raises
  rather than silently merging two residues into one node. This needs extending for the ASD
  set.
- **Alternate conformations are ignored, not handled.** Latent rather than live on these five
  arms, and guarded by a test. It will bite on the ASD set, where the parser needs a real
  occupancy policy.
- **The field's headline numbers are not our bar.** They are mostly computed on
  ligand-stripped holo structures. After UniRef50 dedup, AlloBench finds "none of these
  programs could achieve an accuracy of more than 60 %"; at Jaccard > 0.5 the best are PASSer
  18 % and APOP 15 %. Quote APOP's 88.5 % top-3 alongside AlloBench's 15 %, or quote neither.
  **APOP is the classical bar** — GNM, 10 Å, unsupervised, no MD, no training data, satisfying
  C1, C2 and C6 exactly.
