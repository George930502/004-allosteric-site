# Conservation as the fourth apo-only confounder column

**Compiled 2026-09-02.** Evidence base for audit item 3.1 of
[`../review/11-synthesis.md`](../review/11-synthesis.md), which names this "the single
highest-value addition". `../evaluation/README.md` §11 already reserves the column and it
reads `null`.

**Headline recommendation.** Add one column, `jsd_conservation`, computed as the per-column
Jensen–Shannon divergence of Capra & Singh (doi:10.1093/bioinformatics/btm270) over a Pfam
full alignment pinned to release 38.2 and mirrored in this repository as gzipped Stockholm;
do **not** add a coevolution column, because coupling-to-the-source is a rival method rather
than a residue property and belongs beside `cavity_volume` in the baseline list if it is ever
added at all.

---

## 0. Evidence rules, and one honest weakening of the tags

The three-level convention of [`README.md`](README.md) is used: `[VERIFIED-FULLTEXT]`,
`[VERIFIED-ABSTRACT]`, `[UNVERIFIED]`.

**Every retrieval in this file passed through a summarising fetch tool, not a human reading a
PDF.** `[VERIFIED-FULLTEXT]` here therefore means "the fetch returned this string presented as
a quotation from the full text". That is one notch weaker than the tag means elsewhere in this
directory. Where the fetch returned a paraphrase rather than a quotation, the row is
`[UNVERIFIED]` even when the underlying fact is probably right. Two sources could not be
retrieved at all and are recorded in §5 rather than reconstructed.

Reachability statements in §3 were measured on **2026-09-02** from this machine. A single
network vantage point cannot distinguish a dead host from a blocked egress path, and §5 says
so.

---

## 1. Is conservation actually a confounder here?

### 1.1 The claim everyone repeats, and what stands behind it

"Allosteric sites are less conserved than orthosteric sites" is stated as settled in most of
this literature. Traced back, the usual citation is a **review**, not a measurement:
Nussinov & Tsai, doi:10.2174/138161212799436377, cited for exactly this sentence by Eccleston
& Furnham (doi:10.1101/2025.06.27.662060), whose own wording is "Allosteric sites, however,
are less conserved across protein families and so allosteric drugs can be more selective"
`[VERIFIED-FULLTEXT]`. The same paper adds "Allosteric sites tend to be less evolutionarily
conserved, involve fewer residues and exhibit more ambiguous, non-pocket-like geometries" with
**no citation attached** `[VERIFIED-FULLTEXT]`.

Martí-Aranda & Lehner say the quiet part directly:

> "It is often stated that allosteric sites are less conserved than active sites ... the
> functional conservation of allostery in proteins is, to our knowledge, largely unknown."
> (doi:10.1101/2025.06.20.660748) `[VERIFIED-FULLTEXT]`, preprint

So the field's stock sentence is an assertion with a review behind it. Distinguish it from the
four measurements below.

### 1.2 What has actually been measured

| Source                                            | Population measured                                               | Comparator                     | Finding                                                                                                                                                                                                            | Tag                             |
| ------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| Cimermancic et al., doi:10.1016/j.jmb.2016.01.029 | **cryptic** site residues, 93 apo/holo pairs                      | rest of the protein            | **more** conserved, P = 3.4 × 10⁻⁶⁷                                                                                                                                                                                | `[VERIFIED-FULLTEXT]`           |
| same                                              | cryptic site residues                                             | traditional binding pockets    | "tend to be as conserved in evolution as traditional binding pockets but are less hydrophobic and more flexible"                                                                                                   | `[VERIFIED-ABSTRACT]`           |
| Chen et al., doi:10.1101/2025.03.28.645953        | allosteric **pocket** residues, ASD-derived                       | orthosteric sites              | **less** conserved, 0.63 against 0.83, P = 1.26 × 10⁻²³                                                                                                                                                            | `[VERIFIED-FULLTEXT]`, preprint |
| Leander et al., doi:10.1073/pnas.2002613117       | allosteric **signalling** residues, deep mutational scanning      | structurally critical residues | "Residues critical for allosteric signaling are surprisingly poorly conserved while those required for structural integrity are highly conserved, suggesting evolutionary pressure to preserve fold over function" | `[VERIFIED-ABSTRACT]`           |
| Leander et al., doi:10.7554/eLife.79932           | allosteric hotspots, DMS, homologous pairs                        | non-hotspots                   | "We compared hotspots to close sequence homologs (>50% sequence identity) and did not find statistically higher sequence conservation in hotspots over non-hotspots"                                               | `[VERIFIED-FULLTEXT]`           |
| Sharir-Ivry & Xia, doi:10.1016/j.jmb.2019.07.019  | dN/dS gradient away from allosteric binding sites, proteome scale | gradient from catalytic sites  | allosteric and other non-catalytic sites induce **significantly weaker** long-range rate gradients                                                                                                                 | `[VERIFIED-ABSTRACT]`           |

**Two rows carry a caveat that the numbers themselves hide.** Allo-PED's 0.63 and 0.83 are on
an unstated scale: the fetch reported that the paper does not identify which conservation tool
or database produced them, so the two values are comparable to each other and to nothing else.
And CryptoSite's P = 3.4 × 10⁻⁶⁷ is computed over a very large residue count, so it establishes
the direction of the effect and says nothing about its size. Neither row licenses a magnitude.

### 1.3 The evidence is mixed, and the split is not random — it is a definitional split

The two directions do not contradict each other. They are measuring two different residue
populations that this repository already keeps apart (`CONTEXT.md`).

- **Pocket-lining residues** — a ligandable concave surface — are _more_ conserved than
  background (CryptoSite, P = 3.4 × 10⁻⁶⁷) and _less_ conserved than the orthosteric site
  (Allo-PED, 0.63 against 0.83).
- **Signalling hotspot residues** — positions whose mutation destroys coupling, found by
  saturation mutagenesis — are _not_ more conserved than non-hotspots (Leander 2022) and are
  "surprisingly poorly conserved" (Leander 2020).

**The frozen label sets are the first population, not the second.** They are the lining of an
effector-bound pocket, derived from holo contacts (`../primary/README.md`). So the direction
that applies to this benchmark is CryptoSite's: our positives are expected to sit above
background on conservation before any method runs.

**That is the definition of a confounder, and it is why the column is worth the work.** A
score that ranks conserved residues highly will score above chance on these arms for a reason
that has nothing to do with propagation.

### 1.4 Conservation as a published baseline — a gap, not an answer

The task asks for a paper that measures conservation as a **baseline** against which
allosteric-site predictors are compared. Searching the allosteric-prediction literature, I did
not find one.

- Wu, Strömich & Yaliraki (doi:10.1016/j.patter.2021.100408) benchmark bond-to-bond propensity
  against AllositePro (51.7 %), AlloPred (59 %) and PARS (65 %) on ASBench, and the fetch
  returned "The document does not discuss conservation as a predictor or feature"
  `[UNVERIFIED]`, a negative from a summariser.
- Eccleston & Furnham (doi:10.1101/2025.06.27.662060) compare against PASSer, Allosite and
  AlloPred; "No conservation-only baseline was reported" `[UNVERIFIED]`.
- Khokhar, Keskin & Gursoy (DeepAllo, doi:10.1093/bioinformatics/btaf294) — the fetch returned
  that the paper reports **no** formal conservation analysis, only the conjecture "Like the
  main binding sites, it can be conjectured that allosteric sites are also conserved to some
  extent" `[VERIFIED-FULLTEXT]` for the quotation, `[UNVERIFIED]` for the absence.
- Maity & Qiao (AlloBench, doi:10.1021/acsomega.5c01263) provide no conservation field
  `[UNVERIFIED]`.

The closest published number is CryptoSite's, and it needs a correction that matters. The
retrieved sentence is:

> "The second feature added to the subset of the 3 features by the greedy-forward approach was
> sequence conservation (AUC = 0.74)." `[VERIFIED-FULLTEXT]`

Read literally, **0.74 is the AUC of the growing feature subset at the step where conservation
was added, not conservation's standalone AUC.** Do not quote it as "conservation alone reaches
AUC 0.74". CryptoSite's standalone conservation AUC is **unknown** from what was retrieved.

**Consequence for this repository.** Nobody has published the number this benchmark needs, on
any dataset. Computing the column here produces it for the fourteen frozen arms, which is a
contribution rather than a formality — and it is the only way to answer "your hits are just
the conserved residues" with a number instead of an argument.

### 1.5 C1 and C2, stated rather than assumed

**C1 — apo input only. Cleared, on content; guarded, on plumbing.** The column's inputs are
(i) the apo chain's amino-acid sequence and (ii) an alignment of homologous sequences from an
external database. Neither is a function of the holo entry. The apo and holo entries of one
arm describe the same construct and therefore the same sequence, so no conformation, no
ligand, no pocket definition and no residue count can cross. The residual risk is procedural,
not informational: a fetcher that keys the alignment by PDB accession could be handed the holo
accession from `manifest.yaml`. Mitigation is to key the mirrored artifact by **Pfam
accession** and to derive the query sequence from the apo `ApoInput` alone, never from the
manifest's holo fields, which `allo.inputs` already redacts.

**C2 — no classical MD trajectories. Cleared outright.** A conservation score is a statistic
of an alignment. No trajectory, no force field, no covariance matrix, no simulated ensemble
enters at any point. This is a stronger clearance than the existing `normalised_b_factor`
column, which at least touches a measured physical quantity.

**Three hidden dependencies to avoid, each of which would break one of the two rules.**

1. **PARS's "structural conservation"** (doi:10.1093/bioinformatics/btu002) is conservation of
   _pockets across multiple structures of the family_, not of sequence. It needs a structure
   set, and if the target's own holo entry is in that set it is a direct C1 breach. Do not
   adopt structural conservation under the word "conservation".
2. **CryptoSite's feature vector cannot be imported wholesale.** Its conservation feature is
   clean; its pocket-formation features come from AllosMod molecular dynamics, which C2
   forbids. Take the one column, not the set.
3. **ConSurf's server pipeline keys results to a PDB chain and uses the structure for
   rendering.** rate4site itself needs only an MSA and a tree. If ConSurf is ever used, use the
   grades, not the pipeline, and never key them by a holo accession.

A protein language model route (§2.5) clears both C1 and C2 — ESM-2 is trained on UniRef
sequences, not on structures or trajectories — but its weights are ML-trained, so **ADR 0027's
disclosed, never-load-bearing tier applies to it** and not to an MSA statistic.

---

## 2. Which conservation statistic

### 2.1 The comparison, on the four properties that decide it

| Statistic                                     | Input needed                                       | Offline after a one-time fetch                  | Deterministic                                                                          | Published precedent                                                         |
| --------------------------------------------- | -------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Jensen–Shannon divergence** (Capra & Singh) | one MSA                                            | yes                                             | **bit-exact** — closed-form arithmetic on a fixed alignment                            | doi:10.1093/bioinformatics/btm270; benchmarked on 645 + 828 + 64 alignments |
| Shannon entropy on an MSA column              | one MSA                                            | yes                                             | bit-exact                                                                              | the baseline JSD was measured against, doi:10.1093/bioinformatics/btm270    |
| rate4site evolutionary rate                   | MSA **plus a phylogenetic tree**                   | yes, with an extra binary                       | deterministic in principle; depends on tree inference and on an ML/empirical-Bayes fit | doi:10.1093/bioinformatics/18.suppl_1.s71                                   |
| ConSurf grades 1–9                            | a server call, or rate4site plus ConSurf's binning | **no** — grades come from a live homolog search | no; the grade depends on the homolog set sampled that day                              | doi:10.1093/nar/gkw408, doi:10.1002/pro.4582, doi:10.1002/pro.3779          |
| PLM masked-token entropy                      | sequence plus a ~2.5 GB weight file                | yes                                             | float arithmetic; stable on CPU, version- and hardware-sensitive                       | doi:10.1007/s00439-021-02411-y                                              |

### 2.2 The measurement that decides between JSD, entropy and rate4site

Capra & Singh compared seven measures — Shannon entropy, property entropy, von Neumann
entropy, relative entropy, sum-of-pairs, rate4site and their own JSD — on three datasets: 645
alignments with about 1,900 catalytic sites, 828 alignments scored by ligand distance, and 64
protein–protein interfaces `[VERIFIED-FULLTEXT]`.

> JSD and rate4site "perform similarly, and are not significantly outperformed by any other
> method." `[VERIFIED-FULLTEXT]`

On the catalytic-site set, JSD reached **AUC₁ = 0.9440** against Shannon entropy's **0.9235**
`[VERIFIED-FULLTEXT]`.

Read that the way it should be read. **JSD is not much better than entropy and is statistically
indistinguishable from rate4site.** The reason to prefer JSD is not accuracy. It is that JSD
needs an alignment and nothing else, while rate4site needs a tree, and a tree is a second
inference step with its own parameters that would have to be frozen, reproduced and defended.
For a confounder column, one fewer moving part is worth more than 0.02 of AUC on somebody
else's benchmark.

### 2.3 The parameterisation to freeze

Capra & Singh's published settings, which are what the AUC above was measured at:

- background distribution: the overall amino-acid distribution in the BLOSUM62 alignments
- sequence weighting: Henikoff & Henikoff position-based weights
- mixture parameter λ = 1/2

**With one departure: the window heuristic is off.** Capra & Singh add a term averaging the
estimated conservation of sequentially neighbouring sites over a window of three residues each
side. It improves _prediction_ of functional sites. It is wrong here, for a first-principles
reason: this column is a covariate, and the window injects sequence-local autocorrelation into
the very quantity whose correlation with a spatially autocorrelated score is being measured.
The plain per-column divergence is a property of the alignment column alone, which is what a
confounder column has to be. Turning it off also removes a second free parameter from a frozen
artifact.

### 2.4 Column convention

Name it `jsd_conservation`, higher meaning more conserved, so that the objection
"your hits are just the conserved residues" corresponds to a **positive** Spearman ρ in
`score_arm`'s output. The existing three columns have mixed signs and a reader should not have
to work the direction out.

Residues with no alignment column are **absent from the mapping, never imputed** — R3's
"unknown". `score_arm` must therefore compute the Spearman on the covered subset and print the
coverage fraction beside it. A partial-coverage ρ is not comparable across arms with different
coverage, and the report has to say so.

### 2.5 The PLM route, and why it is second

Marquet et al. measured the obvious thing: the entropy of a masked-language-model's per-residue
distribution against ConSurf grades, over ConSurf10k (10,507 proteins; 9,392 train / 555
validation / 519 test).

> "The entropy of these probability distributions correlated slightly with conservation
> (Spearman's R = −0.374)." (doi:10.1007/s00439-021-02411-y) `[VERIFIED-FULLTEXT]`

A supervised model on the same embeddings reached MCC 0.596 ± 0.006 on the binary
conserved/not split, against MSA-based ConSeq at 0.608 ± 0.006 `[UNVERIFIED]` — so _learned_
embeddings match an MSA method, while _raw entropy_ does not.

**ρ = −0.374 is too weak to stand in for conservation in a column whose whole purpose is to
answer a conservation objection.** A reviewer would simply restate the objection about the
proxy. The route is recorded because it needs no alignment at all and covers every residue of
the chain, which is exactly the weakness of §3's recommendation; it is the fallback if Pfam
coverage turns out to be unacceptable on some arm.

Citations for the models themselves: ESM-2 / ESMFold, doi:10.1126/science.ade2574; zero-shot
masked-marginal scoring, doi:10.1101/2021.07.09.450648.

---

## 3. Which alignment source, measured today

### 3.1 What was reachable on 2026-09-02

| Source                                        | Reachable                                                                                                                  | Versioned and archived                                                                                                | Deterministic output                                                                                                       | Size                                                                                                                    |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Pfam**, `ftp.ebi.ac.uk/pub/databases/Pfam/` | **yes**                                                                                                                    | **yes** — `releases/` holds every release back to Pfam1.0; current is **38.2, June 2026, 30,134 families**            | **yes** — the alignment is a static file, so there is no aligner to reproduce                                              | `Pfam-A.full.gz` **22 G**, `Pfam-A.seed.gz` 185 M, `Pfam-A.hmm.gz` 399 M. Per family via the InterPro API, in Stockholm |
| **UniProt / UniRef**, `ftp.uniprot.org`       | **yes**, current release dated 2026-06-10                                                                                  | **yes** — `previous_releases/` back to 2005; `release-2026_02/` was checked and **contains a `uniref/` subdirectory** | needs a search program; jackhmmer is deterministic, MMseqs2 sensitivity settings are not free parameters to leave unfrozen | `uniref90.fasta.gz` **30 G** (`uniref90.xml.gz` 43 G)                                                                   |
| **UniClust / UniRef30 for HHblits**           | **yes** — `wwwuser.gwdg.de/~compbiol/uniclust/` lists 2016 through 2023 plus `current_release`; ColabFold mirror reachable | dated snapshots, so pinnable                                                                                          | HHblits is deterministic for fixed database and parameters                                                                 | `uniref30_2302` **≈103 G**, `2202` ≈83 G, `2103` ≈75 G                                                                  |
| **jackhmmer against a versioned database**    | yes — this is the UniRef row plus HMMER                                                                                    | as above                                                                                                              | yes                                                                                                                        | as above                                                                                                                |
| **ConSurf-DB**, `consurfdb.tau.ac.il`         | **no.** `ECONNREFUSED 132.66.243.136:443` on three attempts to three paths (`/`, `/overview.php`, `/index.php`)            | no — updated monthly and rebuilt annually, with no archived releases                                                  | no — a grade depends on the homolog set at fetch time                                                                      | n/a                                                                                                                     |

The live ConSurf **server** at `consurf.tau.ac.il` responded and is a different host from
ConSurf-DB. It is a web service, not a pinnable artifact, so it does not change the verdict.

One retrieval worth recording because it establishes the delivery mechanism: the InterPro API
at `https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00071/?annotation=alignment:seed` returned
Stockholm 1.0 beginning `#=GF ID Ras`, `#=GF AC PF00071.29`, `#=GF SQ 60` `[VERIFIED-FULLTEXT]`.
The same endpoint with `alignment:full` returned more than 10 MB and exceeded the fetch limit,
which establishes that full alignments are served and bounds their size from below only.

### 3.2 Recommendation: Pfam full alignments, pinned to release 38.2, mirrored per family

Four reasons, in order of weight.

1. **The pinned artifact is the alignment itself, so determinism is exact by construction.**
   Every other route pins a _database_ and then asks a search program to return the same
   alignment years later, from a different machine, at a different version. Pfam lets the
   repository commit the answer rather than the recipe. This is the same argument that made
   the decoy sets committed rather than re-derived (`../evaluation/README.md` §5.1).
2. **Archived and nameable.** Releases go back to Pfam1.0 at a stable EBI path, and the family
   accession carries its own version suffix — `PF00071.29` — so the manifest can name the
   exact alignment rather than a release plus a hope.
3. **The download is per family, not per planet.** Megabytes to hundreds of megabytes against
   22 G for all of Pfam, 30 G for UniRef90 and 75–103 G for UniRef30. It matches the pattern
   the repository already uses for deposited structures: fetch once by accession, mirror,
   checksum, work offline.
4. **Precedent inside the target literature.** KeyAlloSite built its MSAs with "HMMER to search
   the Pfam database" (doi:10.7554/eLife.81850) `[VERIFIED-FULLTEXT]`, which is the closest
   published work to what §4 discusses.

### 3.3 The four costs, stated rather than discovered later

1. **Coverage is the domain envelope, not the chain.** Residues outside every matched Pfam
   family get no score. On a single-domain arm this is a small tail; on the 764-residue cardiac
   myosin chain it may not be. Report per-arm coverage; do not impute.
2. **Depth is bounded by reference proteomes.** `userman.txt` for release 38.2 states: "As of
   release 29.0 Pfam is based on UniProtKB reference proteomes, as are the flat-files
   Pfam-A.full and Pfam-A.seed" `[VERIFIED-FULLTEXT]`. A Pfam full alignment is therefore
   shallower than a jackhmmer search of all of UniProtKB. For a confounder column this is
   acceptable; for a DCA fit (§4) it may not be.
3. **The column becomes a family property.** Two arms in the same Pfam family would share it.
   Between **distinct targets** this does not arise: clause (xii) of the secondary freeze
   forbids two targets sharing a Pfam family, and the secondary set is disjoint from every
   primary target on family (`../evaluation/README.md` §3.3). It does arise **within** a
   protein: `kras_g12c_mandated` and `kras_g12c_corrected` are the same protein, as are the two
   BCR-ABL1 arms, so each pair would draw the identical alignment and the identical column.
   That is correct rather than a defect — the two arms differ in structure, not in sequence
   family — but it means the column cannot separate a mandated arm from its corrected twin, and
   any per-arm table has to say so. The fourteen arms cover twelve distinct proteins.
4. **The residue-to-column mapping is the one real implementation risk.** Author numbering plus
   chain ID has to reach an alignment column. Either the target's own UniProt entry appears in
   the family's full alignment, in which case its row gives the mapping directly, or the apo
   chain's observed sequence is aligned to the family HMM. Both routes are sequence-only and
   C1-clean. Neither is free, and a silent off-by-one here would produce a plausible-looking
   column that is wrong — so the mapping needs its own test, not just the statistic.

If a family's full alignment is impractically large, subsample it by a rule recorded in the
manifest and commit the subsample. Deterministic subsampling of a static file is still exactly
reproducible, which is the property the whole recommendation rests on.

---

## 4. Coevolution: recommend against, and the reason is not that the evidence is absent

### 4.1 There is real published evidence, and it is one paper

Xie, Zhang, Zhu, Deng & Lai, **KeyAlloSite**, eLife 2023, doi:10.7554/eLife.81850, peer
reviewed. It computes pairwise evolutionary couplings by direct coupling analysis, fitted by
pseudo-maximum likelihood with L-BFGS, then for each pocket residue compares its coupling
values to orthosteric-site residues against a null and Z-scores the count of significant
differences `[VERIFIED-FULLTEXT]`.

Measured on 23 allosteric proteins with 25 known sites from ASBench's core set:

> "Among the 25 allosteric pockets in the data set, 23 have Z-scores greater than 0.5"
> `[VERIFIED-FULLTEXT]`
> "The probabilities that the known allosteric pockets were ranked in the top 1, top 2, and top
> 3 of Z-scores were 56.0, 76.0, and 96.0%, respectively" `[VERIFIED-FULLTEXT]`

Its stated depth requirement is "7 L (± 4L) number of effective homologous sequences"
`[VERIFIED-FULLTEXT]`, and its MSAs come from HMMER against Pfam. It compares itself against
statistical coupling analysis, **not** against a conservation baseline `[VERIFIED-FULLTEXT]`.
It is sequence-only, so it clears C1 and C2 on the same argument as §1.5.

**If it were added, the column would be:** per residue, the Z-score of the number of couplings
to the frozen source set that differ significantly from the residue's own coupling
distribution — a per-residue version of KeyAlloSite's pocket statistic, computed without a
pocket detector.

### 4.2 Why it should not go in the confounder table

**It is a category error, and that is the primary reason.** A confounder column answers "is
your score secretly re-measuring a property of the residue?" Relative solvent accessibility,
hydrophobicity, B-factor and conservation are all properties of a residue that exist before any
method runs. **Coupling-to-the-source is not.** It is a source-conditioned transport score
computed from sequence instead of from a contact graph — structurally the same kind of object
as the methods in `allo/classical/coupling` and `allo/quantum/walk`. Putting a rival method in
the control column would let it masquerade as a null. If it is added, it belongs in
`../evaluation/manifest.yaml`'s required baselines beside `cavity_volume`, under §10's
`compare_methods` rule.

**And as a baseline, the evidence is currently thin.** One group, one paper, N = 25 sites,
pocket-level rather than residue-level, no independent replication found, and no comparison
against the cheaper thing this document recommends. Against it sit two results from the
adjacent literature:

> "the top eigenvector of the SCA matrix does not contain information beyond that provided by
> single-site statistics" — Teşileanu, Colwell & Leibler, doi:10.1371/journal.pcbi.1004091
> `[VERIFIED-FULLTEXT]`
> "for the top sector, SCA is not significantly better than conservation at predicting
> functionally-important sites" — same `[VERIFIED-FULLTEXT]`

> "We have reassessed the energetic coupling of these residues by double mutant cycles together
> with ligand binding and stability experiments and found that coupling is not a special
> property of the coevolved network of residues in PDZ domains. The observed coupling for
> ligand binding is better explained by a distance relationship ... Our study demonstrates that
> statistical coupling from sequence analysis is not necessarily a reporter of energetic
> coupling and allostery." — Chi et al., doi:10.1073/pnas.0711732105 `[VERIFIED-FULLTEXT]`

Teşileanu is the sharper of the two for this decision. It says that where MSA covariance has
been claimed to find functional residues, plain conservation does the same job. That is an
argument for computing conservation **first** and treating coevolution as an increment to be
justified afterwards, not an argument that coevolution is worthless.

**Verdict: not in this submission.** Record KeyAlloSite as the strongest candidate for a
future sequence-only baseline, with its cost — a deep MSA plus a pseudolikelihood fit, against
a Pfam-bounded depth that §3.3 already flags as possibly insufficient at 7L effective
sequences. Nothing blocks it on C1 or C2. It is blocked on evidence weight and on category.

---

## 5. What this cannot settle

- **Whether conservation is a confounder on these fourteen arms.** Every number in §1 is from
  somebody else's dataset. The column is the measurement; until it runs, the direction is an
  expectation and not a result.
- **Whether the new column is redundant with `relative_solvent_accessibility`.** Buried
  residues are more conserved, and if `jsd_conservation` tracks RSA closely it adds a column and
  no information. Unmeasured, and it is the first thing to check once the column exists.
- **Conservation's standalone AUC for site prediction, on any dataset.** §1.4 shows the number
  usually quoted from CryptoSite does not say what it is quoted as saying. Unknown.
- **Whether allosteric pocket linings are more conserved than _surface_ background**, as opposed
  to than the whole protein. CryptoSite's comparator is the rest of the protein, which includes
  the buried core; Allo-PED's is the orthosteric site. Neither is the comparison a reviewer
  means. Unknown.
- **Whether ConSurf-DB's outage is permanent.** Measured from one network on one day. Three
  refusals at the same IP is suggestive and not conclusive.
- **Per-family Pfam full alignment sizes.** Only bounded from below, at >10 MB for PF00071.
  The aggregate is 22 G over 30,134 families; the distribution across the fourteen arms'
  families is unmeasured.
- **Whether all fourteen apo chains map into a Pfam family with adequate depth and coverage.**
  Unmeasured. It is a one-command check and it should run before this recommendation is
  adopted, because §3.3 item 1 could sink the cardiac myosin arm specifically.
- **Two sources could not be retrieved.** Panjkovich & Daura 2010, doi:10.1186/1472-6807-10-9,
  redirected to a Springer identity endpoint; its treatment of pocket conservation is
  unexamined here. Cimermancic et al.'s Methods section was not reached, so **which alignment
  database and conservation measure CryptoSite used is unknown** — a gap that matters, because
  it is the one paper whose vs-background result this recommendation leans on.
- **Negative findings in §1.4 came from a summarising fetch tool.** "The paper reports no
  conservation baseline" is weaker evidence than "I read the paper and there is none".

---

## 6. Bibliography

Every entry was retrieved in this session. Preprints are marked.

**Conservation and allosteric or cryptic sites**

- Cimermancic P, Weinkam P, Rettenmaier TJ, Bichmann L, Keedy DA, Woldeyes RA,
  Schneidman-Duhovny D, Demerdash ON, Mitchell JC, Wells JA, Fraser JS, Sali A. CryptoSite:
  expanding the druggable proteome by characterization and prediction of cryptic binding sites.
  _J Mol Biol_ 2016;428(4):709–719. doi:10.1016/j.jmb.2016.01.029
- Leander M, Yuan Y, Meger A, Cui Q, Raman S. Functional plasticity and evolutionary adaptation
  of allosteric regulation. _Proc Natl Acad Sci USA_ 2020;117(41):25445–25454.
  doi:10.1073/pnas.2002613117
- Leander M, Liu Z, Cui Q, Raman S. Deep mutational scanning and machine learning reveal
  structural and molecular rules governing allosteric hotspots in homologous proteins. _eLife_
  2022;11:e79932. doi:10.7554/eLife.79932
- Sharir-Ivry A, Xia Y. Non-catalytic binding sites induce weaker long-range evolutionary rate
  gradients than catalytic sites in enzymes. _J Mol Biol_ 2019;431(19):3860–3870.
  doi:10.1016/j.jmb.2019.07.019
- Nussinov R, Tsai CJ. The different ways through which specificity works in orthosteric and
  allosteric drugs. _Curr Pharm Des_ 2012;18(9):1311–1316. doi:10.2174/138161212799436377
  _(review; the origin of the "less conserved" claim)_
- Chen X, Zheng J, Huang Z, Xu Z, Huang J, Wei Y, Zhang H. Allo-PED: leveraging protein language
  models and structure features for allosteric site prediction. Posted 2025-04-02.
  doi:10.1101/2025.03.28.645953 _(preprint; conference version
  doi:10.1007/978-981-95-0695-8_31)_
- Martí-Aranda A, Lehner B. The evolution of allostery in a protein family.
  doi:10.1101/2025.06.20.660748 _(preprint)_
- Eccleston RC, Furnham N. Allosteric site prediction using protein language models and
  orthosteric conditioning. doi:10.1101/2025.06.27.662060 _(preprint)_

**Allosteric-site prediction, for the baseline question**

- Wu N, Strömich L, Yaliraki SN. Prediction of allosteric sites and signaling: insights from
  benchmarking datasets. _Patterns_ 2021;3(1):100408. doi:10.1016/j.patter.2021.100408
- Khokhar M, Keskin O, Gursoy A. DeepAllo: allosteric site prediction using protein language
  model (pLM) with multitask learning. _Bioinformatics_ 2025;41(6):btaf294.
  doi:10.1093/bioinformatics/btaf294
- Panjkovich A, Daura X. PARS: a web server for the prediction of protein allosteric and
  regulatory sites. _Bioinformatics_ 2014;30(9):1314–1315. doi:10.1093/bioinformatics/btu002
  _(structural conservation, not sequence — see §1.5)_
- Maity D, Qiao B. AlloBench: a data set pipeline for the development and benchmarking of
  allosteric site prediction tools. _ACS Omega_ 2025;10(17):17973–17982.
  doi:10.1021/acsomega.5c01263
- Meller A, Ward M, Borowsky J, Kshirsagar M, Lotthammer JM, Oviedo F, Ferres JL, Bowman GR.
  Predicting locations of cryptic pockets from single protein structures using the PocketMiner
  graph neural network. _Nat Commun_ 2023;14:1177. doi:10.1038/s41467-023-36699-3

**Conservation statistics**

- Capra JA, Singh M. Predicting functionally important residues from sequence conservation.
  _Bioinformatics_ 2007;23(15):1875–1882. doi:10.1093/bioinformatics/btm270
- Pupko T, Bell RE, Mayrose I, Glaser F, Ben-Tal N. Rate4Site: an algorithmic tool for the
  identification of functional regions in proteins by surface mapping of evolutionary
  determinants within their homologues. _Bioinformatics_ 2002;18(Suppl 1):S71–S77.
  doi:10.1093/bioinformatics/18.suppl_1.s71
- Ashkenazy H, Abadi S, Martz E, Chay O, Mayrose I, Pupko T, Ben-Tal N. ConSurf 2016: an
  improved methodology to estimate and visualize evolutionary conservation in macromolecules.
  _Nucleic Acids Res_ 2016;44:W344–W350. doi:10.1093/nar/gkw408
- Yariv B, Yariv E, Kessel A, Masrati G, Ben Chorin A, Martz E, Mayrose I, Pupko T, Ben-Tal N.
  Using evolutionary data to make sense of macromolecules with a "face-lifted" ConSurf.
  _Protein Sci_ 2023;32(3):e4582. doi:10.1002/pro.4582
- Ben Chorin A, Masrati G, Kessel A, Narunsky A, Sprinzak J, Lahav S, Ashkenazy H, Ben-Tal N.
  ConSurf-DB: an accessible repository for the evolutionary conservation patterns of the
  majority of PDB proteins. _Protein Sci_ 2020;29:258–267. doi:10.1002/pro.3779
- Marquet C, Heinzinger M, Olenyi T, Dallago C, Erckert K, Bernhofer M, Nechaev D, Rost B.
  Embeddings from protein language models predict conservation and variant effects. _Hum Genet_
  2022;141:1629–1647. doi:10.1007/s00439-021-02411-y
- Lin Z, Akin H, Rao R, Hie B, Zhu Z, Lu W, et al. Evolutionary-scale prediction of atomic-level
  protein structure with a language model. _Science_ 2023;379:1123–1130.
  doi:10.1126/science.ade2574
- Meier J, Rao R, Verkuil R, Liu J, Sercu T, Rives A. Language models enable zero-shot
  prediction of the effects of mutations on protein function.
  doi:10.1101/2021.07.09.450648 _(preprint)_

**Alignment sources and search tools**

- Mistry J, Chuguransky S, Williams L, Qureshi M, Salazar GA, Sonnhammer ELL, Tosatto SCE,
  Paladin L, Raj S, Richardson LJ, Finn RD, Bateman A. Pfam: the protein families database in 2021. _Nucleic Acids Res_ 2021;49:D412–D419. doi:10.1093/nar/gkaa913
- Blum M, Andreeva A, Florentino LC, et al. InterPro: the protein sequence classification
  resource in 2025. _Nucleic Acids Res_ 2025;53(D1):D444–D456. doi:10.1093/nar/gkae1082
- UniProt Consortium. UniProt: the Universal Protein Knowledgebase in 2025. _Nucleic Acids Res_
  2025;53(D1):D609–D617. doi:10.1093/nar/gkae1010
- Suzek BE, Wang Y, Huang H, McGarvey PB, Wu CH, UniProt Consortium. UniRef clusters: a
  comprehensive and scalable alternative for improving sequence similarity searches.
  _Bioinformatics_ 2015;31:926–932. doi:10.1093/bioinformatics/btu739
- Eddy SR. Accelerated profile HMM searches. _PLoS Comput Biol_ 2011;7:e1002195.
  doi:10.1371/journal.pcbi.1002195
- Johnson LS, Eddy SR, Portugaly E. Hidden Markov model speed heuristic and iterative HMM search
  procedure. _BMC Bioinformatics_ 2010;11:431. doi:10.1186/1471-2105-11-431 _(jackhmmer)_
- Remmert M, Biegert A, Hauser A, Söding J. HHblits: lightning-fast iterative protein sequence
  searching by HMM-HMM alignment. _Nat Methods_ 2011;9:173–175. doi:10.1038/nmeth.1818
- Steinegger M, Söding J. MMseqs2 enables sensitive protein sequence searching for the analysis
  of massive data sets. _Nat Biotechnol_ 2017;35:1026–1028. doi:10.1038/nbt.3988

**Coevolution**

- Xie J, Zhang W, Zhu X, Deng M, Lai L. Coevolution-based prediction of key allosteric residues
  for protein function regulation. _eLife_ 2023;12:e81850. doi:10.7554/eLife.81850
- Teşileanu T, Colwell LJ, Leibler S. Protein sectors: statistical coupling analysis versus
  conservation. _PLoS Comput Biol_ 2015;11(2):e1004091. doi:10.1371/journal.pcbi.1004091
- Chi CN, Elfström L, Shi Y, Snäll T, Engström Å, Jemth P. Reassessing a sparse energetic
  network within a single protein domain. _Proc Natl Acad Sci USA_ 2008;105(12):4679–4684.
  doi:10.1073/pnas.0711732105

**Retrieved but not read in full** — recorded so the gap is visible

- Panjkovich A, Daura X. Assessing the structural conservation of protein pockets to study
  functional and allosteric sites: implications for drug discovery. _BMC Struct Biol_ 2010;10:9.
  doi:10.1186/1472-6807-10-9 _(redirected to an authentication endpoint)_

---

**Literature last searched: 2026-09-02.** Recorded here because audit item 3.8 asks for it, and
because a negative finding without a date cannot be told apart from a stale one.
