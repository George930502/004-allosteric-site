# The frozen benchmark

**Status: frozen 2026-08-20.** The input layer is fixed. Every method is scored on
identical structures, identical residue sets, identical labels and identical negatives, so
that a difference between two methods is a difference between the methods.

```bash
uv run allo benchmark show      # what is frozen, derived live from the deposited files
uv run allo benchmark verify    # exit 0 iff nothing has moved since the freeze
```

| File | What it is |
|---|---|
| `manifest.yaml` | the choices — entries, chains, ligands, cutoffs, active sites. Hand-edited. |
| `frozen.json` | the consequences — residue counts, label sets, distal label sets, geometry. Generated; never hand-edited. |
| `audit/` | forensic dossier per target pair, every fact carrying its provenance |
| `evidence/` | literature basis: the apo/holo definition, prior art, evaluation practice |

---

## 1. What an apo/holo pair is, operationally

"Apo" is used loosely in this literature, and the looseness is exactly what lets a broken
benchmark through. Three readings circulate: ligand-free of *anything*; ligand-free *at the
site of interest*; ligand-free *with respect to the drug under study*. They give different
answers for every target here — `4OBE` holds GDP·Mg, `9GZ3` holds ADP·Mg·Pi, and both are
routinely called apo.

**We adopt the site-apo reading, made operational:**

> An **apo/holo pair** for allosteric-site prediction is two experimentally determined
> structures of the same protein, in which (i) the *holo* member contains the effector of
> interest, identified by its PDB chemical component ID, bound at the site to be predicted;
> (ii) the *apo* member contains **no ligand of any kind within the site**, where the site
> is the residue set defined by the holo complex; (iii) the two members are the same gene
> product and the same domain content, with sequence differences enumerated; and (iv)
> physiological cofactors at *other* sites (nucleotide, catalytic metal) may be present in
> either member, and are recorded, because they define the active site.

**Selecting the apo entry is not blind to the answer, and that is fine.** Clause (ii) uses
the holo-defined pocket to decide whether an apo candidate is ligand-free there. That is
holo used to *validate the benchmark*, not to predict — and the bias runs against us, since
the filter discards apo structures that would have leaked conformational information. Stating
the direction of the bias is what makes it admissible; leaving it implicit is what would not.

Two consequences we apply without exception:

- **A pair fails clause (ii) even if the occupying ligand is deleted during cleaning.** A
  structure crystallised with something in the pocket is in the pocket-bound conformation.
  Removing the atoms does not remove the information. This is what disqualifies `1OPL`.
- **Clause (i) is checked by reading the chemical component ID out of the file**, never by
  trusting a table. This is what disqualifies `6C1H`.

**Where this sits in the literature.** The site-relative reading is published, not invented
here: AHoJ annotates chains "as holo or apo respective to the presence or absence of ligands
in the defined binding site(s)" ([10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701)),
PocketMiner scopes its ligand exclusion to 5 A of the site
([10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)), and CryptoBench
inherits that annotation ([10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)).
It is also contested. Wankowicz et al. define apo *globally* -- any heteroatom group of >=10
heavy atoms disqualifies a structure
([10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114)) -- and classical IUPAC/NC-IUBMB
enzymology inverts the label outright, making a cofactor-bound form holo unconditionally. No
shared term for the site-relative concept exists in the sources reviewed, so "site-apo" is
this repo's coinage and the report states the sense in use at first use. Because the readings
disagree, we record what each structure *contains* rather than relying on the word. Full
review, including the tolerated-ligand whitelists that disagree between benchmarks:
[`evidence/apo-holo-definition.md`](evidence/apo-holo-definition.md).

**What the apo structures actually contain.** Measured, not assumed -- heavy atoms, 4.5 A,
via `allo.structure.pdb`. None of the eight nominated apo structures is globally ligand-free,
so under the Wankowicz reading this benchmark would have no apo members at all. Under clause
(ii) exactly one fails:

| apo | non-water components | nearest distal label | distal labels contacted | clause (ii) |
|---|---|---:|---:|---|
| `4OBE` | GDP, MG | 5.35 A | 0 | passes |
| `4LDJ` | GDP, MG | 5.14 A | 0 | passes |
| `1OPL` | **MYR**, P16 | **3.29 A** | **16 of 20** | **FAILS** |
| `2G2H` | P16 | 16.27 A | 0 | passes |
| `2G1T` | 112 (chain E), MG | 13.15 A | 0 | passes |
| `9GZ3` | ADP, MG, PO4 | 20.52 A | 0 | passes |
| `8QYP` | ADP, MG, VO4 | 18.83 A | 0 | passes |
| `9YRG` | ADP, PO4 | 20.03 A | 0 | passes |

`1OPL` does not merely resemble a holo structure, it *is* one with respect to the site being
predicted: myristate contacts 16 of the 20 distal label residues. It is retained only
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
metal and HEME count as *part of the protein*
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

| Pair | Verdict | Deciding evidence |
|---|---|---|
| KRAS `4OBE`→`6OIM` | usable, wrong genotype | `4OBE` `_struct_ref_seq_dif` lists no mutation; residue 12 is **GLY** in both chains. `6OIM` is G12C + C51S/C80L/C118S. The apo input lacks the cysteine the holo drug is covalently bonded to. |
| BCR-ABL1 `1OPL`→`5MO4` | not a blind prediction | `1OPL` contains `MYR` **in the myristoyl pocket** (chain A) and `P16` in the ATP site. Its 16 myristate-contact residues are a strict subset of asciminib's 20. Apo↔holo Cα RMSD **1.00 Å** over 409 paired residues and **0.50 Å** across the pocket lining, fitted on the non-label residues. |
| Cardiac myosin `5TBY`→`6C1H` | **unscoreable** | `6C1H` is rat unconventional **myosin-Ib** + rabbit actin + calmodulin (Mentes 2018, doi:10.1073/pnas.1718316115). Ligands: ADP and Mg, both in the *actin* clefts. No mavacamten; mavacamten is component `XB2` and appears in six entries, none of them this one. `5TBY` is a SWISS-MODEL homology model on a **tarantula** template (`3JBH`), rigid-body fitted; the entry records 20 Å (`_em_3d_reconstruction.resolution`) and its source map `EMD-2240` is 28 Å. |

The myosin failure is a factual error in the challenge statement rather than a judgement
call, and is worth reporting upstream. The other two are defensible-but-suboptimal choices.

### 2b. Dimensions checked beyond ligand identity

An audit that only reads the ligand list misses the ways a pair fails quietly. Re-audit
2026-08-20 swept the following, all from RCSB records and the deposited coordinates. Six of
eight came back clean; the two that did not are recorded rather than smoothed over.

| Dimension | Method | Result |
|---|---|---|
| **Ligand fit to density** | RCSB `nonpolymer_entity_instance` validation | `6OIM` MOV **RSCC 0.908**, `5MO4` AY7 **0.946**, `8QYR` XB2 **0.915** — all strong. **Cryo-EM entries carry no deposited ligand-fit score at all**, so `9GZ2`/`9GZ1` (the `corrected` and `srx` myosin holos) rest on an unscored placement; `9GZ1` chain B additionally reports 9 intermolecular clashes. |
| **Crystal packing at the pocket** | `REMARK 290` symmetry expansion, ±1 unit cell, Fisher test vs. the rest of the chain | Not enriched anywhere (`4OBE` 48 % of labels vs 40 % background, OR 1.37, **p = 0.33**) — so no crypticity verdict is a lattice artefact. But `4OBE`'s switch-II *is* lattice-engaged (10 of 21 labels, closest 2.58 Å) where `4LDJ`'s is not (2 of 21) — and `4LDJ`, the *less* packed structure, clashes *more* on transplant (18/41 vs 14/41). The confound was tested and the cryptic verdict survives it. |
| **Sequence identity, apo↔holo** | pairwise alignment of modelled chains | 97.6–100 % on every frozen arm; pinned as `sequence_agreement.identity`. ADR 0004's exclusion rule is now a number rather than a promise. |
| **Mutations inside the label set** | per-residue comparison across the alignment | Exactly one, and it is the KRAS defect: `kras_g12c_mandated` has **`GLY12->CYS`** — the residue sotorasib is covalently bonded to does not exist in the input. Every other arm: zero. `kras_g12c_corrected` is clean, which is the sharpest single argument for `4LDJ`. |
| **Alternate conformations / partial occupancy** | `label_alt_id`, `occupancy` | Present in `5MO4` and `8QYR`; **no label residue in any arm has one**. The parser ignores altloc, so this is currently true by luck, not by design — see open items. |
| **Chain breaks near the site** | gaps in modelled author numbering | None abuts a label in any arm. Myosin has gaps at 202–214 and 624–645; both are far from the site. |
| **Order at the site** | median B-factor, labels vs chain | Label residues are as ordered as the chain or better (ratio 0.78–1.10). The sites are not modelled into noise. |
| **Biological assembly vs. the frozen input** | RCSB `assembly` records | Every `corrected` arm is a **monomeric** assembly, so chain A *is* the biological unit. Two exceptions: `2G1T` is dimeric, and the IHM entries (`9YRG`/`9YR7`) are **hexameric**. Freezing chain A of the IHM discards the inter-head interface the arm exists to study — label residue 721 sits in a 3.34 Å inter-chain contact — which is the open question the coarse-graining phase has to answer, not a defect in the pair. |


---

## 3. The frozen input layer

Three tiers, all reported (ADR 0003). `mandated` is exactly what `CHALLENGE.md` Table 1
specifies; `corrected` is the defensible pair for the same biology; `sensitivity` tests
whether a conclusion survives a different structure. Everything was fixed **before any
method was run**.

| Target | Tier | Apo | Holo | Ligand | N | \|GT\| | prevalence | ligand clash in apo |
|---|---|---|---|---|---|---|---|---|
| kras_g12c_mandated | mandated | `4OBE`:A | `6OIM`:A | MOV | 169 | 21 | 12.4 % | **0.75 Å, 14/41** |
| kras_g12c_corrected | corrected | `4LDJ`:A | `6OIM`:A | MOV | 170 | 21 | 12.3 % | **0.69 Å, 18/41** |
| bcr_abl1_mandated | mandated | `1OPL`:A | `5MO4`:A | AY7 | 451 | 20 | 4.4 % | 2.60 Å, 0/31 |
| bcr_abl1_corrected | corrected | `2G2H`:A | `5MO4`:A | AY7 | 272 | 18 | 6.6 % | 1.95 Å, 2/31 |
| bcr_abl1_sensitivity | sensitivity | `2G1T`:A | `5MO4`:A | AY7 | 271 | 18 | 6.6 % | 2.12 Å, 2/31 |
| cardiac_myosin_mandated | mandated | `5TBY` | `6C1H` | — | — | — | — | **excluded: no ground truth exists** |
| cardiac_myosin_corrected | corrected | `9GZ3`:A | `9GZ2`:A | XB2 | 764 | 12 | 1.6 % | 2.63 Å, 0/20 |
| cardiac_myosin_sensitivity_xray | sensitivity | `8QYP`:A | `8QYR`:B | XB2 | 706 | 15 | 2.1 % | 2.93 Å, 0/20 |
| cardiac_myosin_sensitivity_srx | sensitivity | `9YRG`:A | `9YR7`:A | XB2 | 912 | 12 | 1.3 % | 2.77 Å, 0/20 |

Two `bcr_abl1_corrected` labels (Val525, Leu529) fall outside the kinase-domain-only apo
model and are reported as unmapped rather than silently dropped. N counts every polymer
residue including modified ones — the `8QYP` total includes two trimethyl-lysines, which
the ATOM/HETATM flag would have dropped.

The N, |GT| and prevalence columns are read back from `frozen.json` by
`tests/test_benchmark.py`, so they cannot drift from the freeze. The remaining columns are
in `frozen.json` but are not yet compared against this prose.

---

## 4. What this benchmark actually tests

Freezing the inputs let us measure the benchmark's own difficulty before measuring any
method on it — which is the difference between crediting a method and crediting an easy
instance.

**The crypticity measure.** Superpose the holo entry onto the apo entry locally (the shell
within 20 Å of the pocket centroid, pocket residues excluded from the fit, residues paired
through the sequence alignment), carry the ligand across, and ask how hard it collides with
the apo structure. A cryptic pocket does not exist in the apo input, so the ligand cannot be
placed. A pre-formed pocket accepts it.

- **KRAS is the only genuinely cryptic case.** Closest approach 0.69–0.75 Å with 14–18 of
  41 ligand atoms clashing below 2.5 Å. The switch-II segment swings out to create the
  pocket: fitting on the 145 residues paired between the two entries and *not* in the label
  set gives a 1.07 Å core, against **2.61 Å across the pocket lining, 8.9 Å at its worst**.
  The change is local, large, and exactly where the pocket appears. Compare the mandated
  BCR-ABL1 pair on the same measure: 1.00 Å core, **0.50 Å lining** — nothing to predict.
  All of these are in `frozen.json` under `apo_holo_rmsd`, so they regenerate rather than
  living in a lost scratch script.
- **The myristoyl pocket is not cryptic**, and the literature agrees. Asciminib transplants
  into *every* myristate-free ABL1 apo candidate we tested — `1M52`, `2G1T`, `2G2H`, `4WA9` —
  with at most 2 of 31 atoms clashing (`1M52` 2/31 at 2.35 Å, `2G1T` 2/31 at 2.12 Å,
  `2G2H` 2/31 at 1.95 Å, `4WA9` 1/31 at 2.01 Å). Paladini et al. (*eLife* 2024) describe the αI helix
  as adopting "a straight conformation in crystal structures of the isolated Abl kinase
  domain with an **empty myristoyl binding pocket** (PDB 1M52)"; Wylie et al. (*Nature* 2017)
  call it a "vacant pocket". It is a constitutive cavity gated by helix conformation, and in
  `1OPL` it is filled with its native ligand. **We must not claim to discover a cryptic
  pocket in ABL1.**
- **The mavacamten site is not cryptic.** Zero clashing atoms in all three myosin pairs,
  and all three fail CryptoBench's 2 Å floor (1.10, 1.79, 0.46 Å).

**Measured against the field's own published threshold.** CryptoBench requires "at least 2 Å
RMSD between the binding residues in the apo and holo forms" to call a site cryptic
([10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)). Applying
it to the frozen pocket-lining RMSDs, which regenerate from `frozen.json`:

| Target | core RMSD | pocket lining | worst | CryptoBench 2 Å floor |
|---|---:|---:|---:|---|
| `kras_g12c_mandated` | 1.07 | **2.61** | 8.9 | passes |
| `kras_g12c_corrected` | 1.05 | **2.62** | 8.9 | passes |
| `bcr_abl1_mandated` | 1.00 | **0.50** | 1.0 | **fails, by 4x** |
| `bcr_abl1_corrected` | 1.72 | **2.38** | 9.6 | passes |
| `bcr_abl1_sensitivity` | 2.56 | **2.28** | 9.0 | passes |
| `cardiac_myosin_corrected` | 1.18 | **1.10** | 1.9 | fails |
| `cardiac_myosin_sensitivity_xray` | 1.22 | **1.79** | 3.4 | fails |
| `cardiac_myosin_sensitivity_srx` | 0.88 | **0.46** | 0.8 | fails |

Three things fall out that were not obvious before this was computed. The mandated BCR-ABL1
pair fails a published cryptic-site criterion by a factor of four, so "this pair is not a
blind prediction" is now the field's verdict rather than ours. **The corrected pair passes**
— swapping `1OPL` for `2G2H` does not merely remove the myristate, it restores a real 2.38 Å
pocket rearrangement, which is a stronger argument for the corrected tier than the audit
made. And the `srx` arm is the control on the whole measure: its replacement pair (`9YRG`→`9YR7`,
same study, same construct) gives **0.88 Å core over 900 paired residues at 100 % sequence
identity** — what a genuinely matched pair looks like. Its 0.46 Å lining says the mavacamten
site is pre-formed, agreeing with the other two myosin arms rather than contradicting them.
The arm it replaced (`8ACT`→`9GZ1`) gave an 11.78 Å core, which is how it was caught.

So the benchmark poses **one cryptic-pocket problem and two "which pre-formed surface pocket
is the allosteric one" problems.** The prediction that follows — untested until a geometric
detector is wired in, and recorded here so it counts as a prediction rather than a
rationalisation — is that a pure pocket finder scores near zero on KRAS and respectably on
the other two. Any claim of advantage must be read against that, and the report must say so
rather than let a strong average hide it.

**The KRAS pocket has already been predicted classically, in 2011.** Grant et al. ran 120 ns
of MD from `2PMX` with FTMap/AutoLigand and reported a pocket "between helices α2 and α3" at
residues **61–65 and 90–99** ([10.1371/journal.pone.0025711](https://doi.org/10.1371/journal.pone.0025711))
— **two years before** Ostrem et al. characterised the switch-II pocket experimentally. Against
our frozen distal label set that prediction contains **6 of 14 residues (61, 62, 63, 95, 96,
99)**, Jaccard 0.26. A ranking that returned five residues drawn from their pocket would be
expected to score ~2 true hits, against a hypergeometric expectation of 0.41.

This is the single most important calibration fact in the benchmark and it must appear in the
report. It does not disqualify anything — Grant's input was an MD trajectory, which C2 forbids
us — but it means **the S-IIP is not an open prediction problem**, and any claim that a quantum
method "discovers" it is a claim about efficiency and about doing it without MD, never about
priority. Stating this ourselves is worth more than having a reviewer state it.

**Distality.** All three sites are distal in the sense the challenge means. Minimum Cα distance
from a label residue to the active site is 10.6 Å for `bcr_abl1_mandated`, 10.8 Å for
`bcr_abl1_corrected` and 16.5 Å for `cardiac_myosin_corrected`; medians run 17–28 Å.
(The ABL1 minima moved from 12.1/12.7 Å when all three ABL1 arms adopted the catalytic-motif
source rule ADR 0005 prescribes; the drug-footprint source they previously used was larger
and sat further from the myristoyl pocket.) KRAS is the
exception and needs care: **5 of its 21 label residues (11, 12, 13, 16, 34) are themselves
active-site residues**, at 0.0 Å, because the switch-II pocket abuts the nucleotide site and
sotorasib is anchored at Cys12. Scoring "connectivity to the active site" will rank those top trivially. See ADR
0005 and §5.

---

## 5. The evaluation protocol

Fixed here, before any method exists, so that no test can be chosen after seeing scores.

**Primary endpoint.** Within a target: **AUC-ROC *and* AUC-PR of the residue score for
ground-truth pocket residues against background residues**, each reported with the chance
line (0.5 for ROC; the label prevalence for PR). AUC is simultaneously the test statistic
and the effect size, which avoids reporting significance without magnitude.

**Both, because one is not enough at this prevalence.** Distal-label prevalence runs from
8.2 % (`kras_g12c_corrected`, 14/170) to 1.3 % (`cardiac_myosin_sensitivity_srx`, 12/912) --
a 6x span. Simulating a *fixed* real signal (d = 0.8, 2000 draws, seed 0; regenerate with
`uv run allo benchmark stats`) across that range gives AUC-ROC 0.711 / 0.712 / 0.713 --
flat -- while AUC-PR falls 0.243 -> 0.202 -> 0.066, a 3.7x span. AUC-ROC is
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

**For KRAS, the primary endpoint is computed on the distal label set** — the **14** label
residues more than 5 Å from any active-site residue (9, 59, 60, 61, 62, 63, 68, 69, 72, 95,
96, 99, 100, 103) — with the full-label figure reported alongside. The set is identical for
any threshold from 4 to 6 Å, so the choice is not delicate. The active-site-adjacent
residues answer a question nobody asked. Both sets are pinned in `frozen.json`.

**The null is the opponent, and it is not the rank-sum null.** Residue scores are spatially
autocorrelated and the label set is a single contiguous patch, so residues are nowhere near
independent draws. We use a **matched patch null**: sample B = 10,000 connected surface
patches of the same size as the label set by nearest-neighbour growth on the contact graph
from a uniformly drawn surface seed, recompute the statistic on each, and take the empirical
p-value. This preserves size, contiguity and surface exposure, and so controls the confound
`docs/FIELD.md` §3 names — that any residue score correlates with burial and degree, and
"buried and well connected" already predicts functional sites.

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
characterise what cryptic sites *are*; they do not calibrate what a ranking *scores*. And in
the other full texts reviewed -- PocketMiner, CryptoBench, DeepAllo
([10.1093/bioinformatics/btaf294](https://doi.org/10.1093/bioinformatics/btaf294)), Ohm
([10.1038/s41467-020-17618-2](https://doi.org/10.1038/s41467-020-17618-2)), P2Rank -- there
are no permutation tests, no p-values and no random baselines; MEF-AlloSite
([10.1186/s13321-024-00882-5](https://doi.org/10.1186/s13321-024-00882-5)) reports
uncorrected one-sided t-tests. None addresses spatial autocorrelation explicitly. Two adjacent
literatures supply the justification the field leaves implicit: on residue-contact graphs a
non-geometric null declares "almost all analyzed subgraphs" significant
([10.1371/journal.pone.0005967](https://doi.org/10.1371/journal.pone.0005967)), and
clustering alone lets labelled residues beat *size-matched* random subsets in 96.7 % and
87.7 % of interfaces
([10.1186/1471-2105-11-286](https://doi.org/10.1186/1471-2105-11-286)) -- a confound our
patch null is built to absorb and a uniform-residue null is not. Full review:
[`evidence/evaluation-protocol-lit.md`](evidence/evaluation-protocol-lit.md).

**Second negative set.** The challenge scores against non-functional surface pockets as well
as random background. Decoys are the pockets found by a geometric detector on the apo
structure, excluding any pocket overlapping the true site, ranked and reported separately.

**Secondary endpoints.** Precision@5 and P(≥1 true residue in the top 5) — the top-5 hit
list is the scored artifact. Exact hypergeometric baselines under a uniform random ranking,
computed on the **distal** label set that is the primary endpoint, per frozen target:

| Target | N | \|GT\| | \|distal\| | E[hits@5] | P(≥1 hit) | P(≥2 hits) |
|---|---|---|---|---|---|---|
| `kras_g12c_mandated` | 169 | 21 | 14 | 0.41 | **0.355** | 0.055 |
| `kras_g12c_corrected` | 170 | 21 | 14 | 0.41 | **0.353** | 0.055 |
| `bcr_abl1_mandated` | 451 | 20 | 20 | 0.22 | **0.204** | 0.017 |
| `bcr_abl1_corrected` | 272 | 18 | 18 | 0.33 | **0.292** | 0.037 |
| `bcr_abl1_sensitivity` | 271 | 18 | 18 | 0.33 | **0.293** | 0.037 |
| `cardiac_myosin_corrected` | 764 | 12 | 12 | 0.08 | **0.076** | 0.002 |
| `cardiac_myosin_sensitivity_xray` | 706 | 15 | 15 | 0.11 | **0.102** | 0.004 |
| `cardiac_myosin_sensitivity_srx` | 912 | 12 | 12 | 0.07 | **0.064** | 0.002 |

**One hit in the top five means very different things across targets** — better than a
1-in-3 coin flip on KRAS, roughly 13:1 on myosin. Reporting "we found the pocket in the top
5" without this table would be reporting a coin flip as a discovery. Two hits is the level
at which a single target carries evidence on its own.

**Power, honestly.** Treating residues as independent, a rank-sum test at α = 0.05
one-sided and 80 % power detects, on the distal label sets that are the primary endpoint,
AUC ≈ 0.70 (KRAS), 0.675 (ABL1 corrected), 0.709 (myosin corrected) -- all from
`uv run allo benchmark stats`. Under the patch null those numbers are optimistic by a wide
margin, and the honest figure is starker than a number: if the pocket contributes **one**
effectively independent observation rather than twelve, the Noether bound has **no solution
below AUC = 1.0** at any of these sizes. A single target cannot carry the claim on its own. **We report the patch-null p-value as primary and the rank-sum p-value only as
a labelled upper bound on the evidence.**

**Across targets we claim nothing quantitative.** Three proteins cannot support a pooled
p-value (`docs/FIELD.md` trap 5). Significance lives within a target; the cross-target
statement is qualitative and is reported as such.

**Multiplicity.** One primary metric per method per target, fixed in advance. When claiming
one method beats another, Holm correction across the methods compared.

**No tuning on this benchmark.** Any hyperparameter selected by looking at enrichment here
is test-set fitting even with no holo import (`docs/playbooks/constraint-audit.md`).
Selection happens on the ASD generalisability set and is frozen before the primary targets
are touched; anything not selected that way is fixed a priori and declared.

---

## 6. Provenance of every structure used

| PDB | What it is | Primary citation as deposited |
|---|---|---|
| `4OBE`, `4LDJ` | KRAS WT and G12C, GDP·Mg | Hunter et al., *PNAS* 2014, doi:10.1073/pnas.1404639111 |
| `6OIM` | KRAS G12C + sotorasib (`MOV`) | Canon et al., *Nature* 2019, doi:10.1038/s41586-019-1694-1 |
| `1OPL` | autoinhibited c-Abl, `MYR` + `P16` | Nagar et al., *Cell* 2003 |
| `2G1T`, `2G2H` | Abl kinase domain, Src-like inactive | Levinson et al., *PLoS Biol* 2006 |
| `5MO4` | ABL1 **ternary**: asciminib (`AY7`) **and** nilotinib (`NIL`), T334I/D382N | Wylie et al., *Nature* 2017, doi:10.1038/nature21702 |
| `5TBY` | homology model of the human IHM | Alamo et al., *eLife* 2017 |
| `6C1H` | rat myosin-Ib + actin + calmodulin | Mentes et al., *PNAS* 2018, doi:10.1073/pnas.1718316115 |
| `8QYP`, `8QYR` | bovine MYH7 motor domain ± mavacamten (`XB2`) | bioRxiv 2023 → Auguin et al., *Nat Commun* 2024, doi:10.1038/s41467-024-47587-9 |
| `9GZ1`–`9GZ3` | human MYH7 ± mavacamten | bioRxiv 2025 (deposited citation is a preprint) → McMillan et al., *Sci Adv* 2026 |
| `8ACT` | human β-cardiac myosin folded-back off state | Grinzato et al., *Nat Commun* 2023, doi:10.1038/s41467-023-38698-w — **considered and replaced**, see §7 |
| `9YRG`, `9YR7` | human β-cardiac myosin IHM (undocked S2-FH) ± mavacamten, Myosin-7/GCN4/EGFP chimera | Somavarapu et al., *Sci Adv* 2026, doi:10.1126/sciadv.aed6472 |

Two forensic notes. `5TBY` has clean provenance — Anderson et al. *PNAS* 2018, the
challenge's own reference [23], cites it by accession. `6C1H` has none: the other two rows'
holo IDs are the depositions of their cited references, and the myosin holo is the only ID
in Table 1 with no basis anywhere in the document's bibliography. How it got there is
**unverifiable** from public sources — we report what `6C1H` is and do not speculate.

---

## 7. Open items

- **No resolution ceiling is declared.** The field near-universally applies one — 2.0 Å
  (Wankowicz), 2.5 Å (PocketMiner, CryptoBench, Binding MOAD), 3.0 Å (PASSer/DeepAllo).
  Ours would exclude `1OPL` (3.42 Å, R-free 0.315, 22 % RSRZ outliers) and `5TBY` (20 Å) —
  both mandated, so a ceiling cannot be applied to the mandated tier without discarding what
  the challenge requires us to report. Every `corrected` and `sensitivity` entry is 1.15–3.7 Å
  and would clear a 4.0 Å cryo-EM-inclusive bar. The rule to declare before the ASD selection
  set is built: **X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å, with the mandated tier exempt by
  definition.** Not yet an ADR.
- **ML baselines are not blind on BCR-ABL1.** ASD curates the myristoyl site, and
  PASSer/PASSer2.0/PASSerRank are trained on ASD. Any comparison against them on this target
  is a comparison against a method that has seen the answer, and must be labelled as such.
- **Decoy surface pockets** need a geometric detector; none is installed. Blocks the second
  negative set the challenge requires.
- **Modified residues** in the chain (trimethyl-lysine `M3L` at 129 and 549 in `8QYP`) are
  kept as polymer nodes and mapped to their parent amino acid, because `label_seq_id` — not
  the ATOM/HETATM flag — decides chain membership. Settled in ADR 0006; whether they carry
  *modified properties* as network nodes is explicitly out of scope there.
- **Alternate conformations are ignored, not handled.** `parse_mmcif` keeps every altloc
  atom and no code filters by `label_alt_id` or occupancy, so a residue could enter a label
  set through a 0.25-occupancy conformer. No frozen arm is affected (checked), which makes
  this a latent defect rather than a live one — but it will bite on the ASD selection set.
- **A specificity control is available and not yet used.** `9YRH` is the same construct and
  state as the `srx` arm with **omecamtiv mecarbil** (`2OW`) bound at a different site
  (Somavarapu et al., *Sci Adv* 2026). It answers "does the method find *this* site, or any
  pocket?" directly, which no random or decoy negative can. Adding it is an evaluation-layer
  decision and is deliberately not taken here.
- **The IHM arm is frozen as chain A of a hexamer.** `9YRG`/`9YR7` are the folded-back off
  state, and the inter-head interface is the mechanism — label residue 721 is in a 3.34 Å
  inter-chain contact. Whether the network should be one head or the whole IHM is the
  coarse-graining question (Phase 4), and the frozen input takes one head until that is
  settled. Recorded so the choice is visible rather than inherited.
- **The `srx` heavy chain is a Myosin-7/GCN4/EGFP chimera.** Modelled span is 4–943 in native
  MYH7 numbering, so the site is 1:1 with the other arms, but the residue set must be trimmed
  to MYH7 before network construction. Not yet implemented.
- **Insertion codes are refused, not handled.** No frozen entry has any; `parse_mmcif` raises
  rather than silently merging two residues into one node. This will need extending for the
  ASD generalisability set.
- **The patch null** needs the contact graph, so it lands with network construction.
- **`Ala767` is unresolved.** Auguin et al. name Leu120 and Ala767 as mavacamten contacts.
  Leu120 is real but borderline — present at 4.5 Å in the 1.80 Å X-ray (`8QYR`) and in
  `9YP9`, 4.93 Å in `9GZ1` chain B and 5.0006 Å in `9GZ2` chain A -- which is why Leu120
  is a label in the X-ray arm and not in the cryo-EM arms. **`Ala767` appears in no structure at any
  cutoff up to 6.0 Å.** Either a different numbering, a second-shell/network claim rather
  than a contact, or an error. Not included; recorded rather than quietly dropped.
- **ASD (`mdl.shsmu.edu.cn/ASD`) serves over HTTP only.** Its wildcard certificate for
  `*.shsmu.edu.cn` expired 2025-12-28, so HTTPS fails certificate validation; plain HTTP
  returns 200. The secondary benchmark (challenge reference [25]) is therefore *not*
  blocked, but any fetch of it must be over HTTP and its integrity checked another way —
  record checksums of whatever we download, since the transport is unauthenticated.
- c-Myc (`1NKP`) is out of scope for this phase. Hazard already recorded: its two Myc copies
  carry different arbitrary numbering offsets (`docs/targets.md`).
- Whether to notify the organisers about `6C1H`, and in what form.
