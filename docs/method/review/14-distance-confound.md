# The distance confound: how the field measures it, how to condition on it, and what is left over

**Scope:** the single question of whether a residue score contains anything beyond Euclidean
distance to the active site — how that confound is documented across structural bioinformatics
and adjacent fields, the statistical machinery for removing or conditioning on it, the
descriptors that are genuinely not a function of it, the normalisations that cancel it by
construction, what the allosteric-site field itself does about it, and how to report a result
that is partly explained by it. It deliberately excludes the choice of propagator, the quantum
observable space, and the hardware account.
**Sibling files:** `09-data-analysis.md` (our own measured confound sizes — this file is the
literature that surrounds those numbers), `01-classical-baselines.md` (the baseline battery),
`../exploration/lit/24-residue-descriptors.md` (per-residue descriptors and the burial axis, the
file this one extends), `../exploration/lit/22-transport-formalisms.md` (why most propagation
scores are one measurement), `../exploration/results/41-selection-and-power.md` (multiplicity).
**Retrieved:** 2026-08-26.

**Databases searched:** Crossref REST API (`api.crossref.org/works`, bibliographic query and
DOI-direct), PubMed E-utilities (`esearch`, `efetch` with `rettype=abstract`), Semantic Scholar
Graph API (`api.semanticscholar.org/graph/v1`), arXiv, bioRxiv, and publisher article pages
(PLOS, Springer, Nature) plus two software documentation sites. Approximately 60 distinct
queries; the full list is in §Method. **Europe PMC, which `00-conventions.md` §3 lists as a
working route, returned `{"version":"6.9"}` with an empty result list on every one of ten
attempts through this session's fetch route, in JSON and XML, with `+` separators and with
`%20`, at `resultType` `core`, `lite` and `idlist`. Record it as down for this route.**

---

## 0. The one-paragraph answer

The confound is real, it is measured, and it is measured almost everywhere except in the
allosteric-site literature. Adjacent structural-ML fields have repeatedly shown that a trivial
baseline recovers most or all of a published number — the sharpest case being a
convolutional network on protein–ligand complexes that scores mean AUC 0.98 across 102 DUD-E
targets whether or not the receptor is shown to it, with the two models' per-target AUCs
correlated at R² = 0.98 (doi:10.1371/journal.pone.0220113) [VERIFIED-FULLTEXT]. The
statistical machinery for conditioning on a spatially structured confound is mature but lives
in neuroimaging and ecology, not in structural biology: variogram-matched surrogate maps and
Moran spectral randomisation both transfer to a residue graph unchanged, because their only
geometric input is a pairwise distance matrix or a weights matrix. The spin test does not
transfer. Of the distance-orthogonal descriptors, the one the brief nominates as most promising
— SCA sectors — is the one the retrieved evidence undercuts hardest: on the proteins where SCA
has actually been tested experimentally, plain conservation reproduces the sector's functional
predictions with no statistical difference (doi:10.1371/journal.pcbi.1004091)
[VERIFIED-FULLTEXT], and conservation is itself a weak allosteric discriminator. The strongest
distance-orthogonal candidates that survive are local energetic frustration, cavity geometry,
and the ENM spectral readouts we have already measured at ρ ≈ −0.05 against distance. And no
published allosteric-site predictor was retrieved that runs a distance-only control. That last
sentence is the differentiator.

---

## Q1 — Is this confound documented in the field?

### Synthesis

**It is documented as a class, and the class has a name in every field except ours.** The
general finding is that a predictor's headline number can be reproduced by an input the
predictor was not supposed to be using. The measurements are cleanest in structure-based
virtual screening, where the ablation is easy to run.

Chen and colleagues trained the same convolutional architecture twice on 102 DUD-E targets:
once on the receptor–ligand complex, once on the ligand alone with the receptor deleted. Both
reached **mean AUC 0.98**, and the per-target AUCs of the two models correlated at **R² = 0.98
with slope 0.99** (doi:10.1371/journal.pone.0220113) [VERIFIED-FULLTEXT]. The structural input
contributed nothing measurable. Volkov and colleagues reached the same conclusion from a
different direction with graph neural networks on protein–ligand complexes: "an explicit
description of protein–ligand noncovalent interactions does not provide any advantage with
respect to ligand or protein descriptors", and simple models "inferring binding affinities of
test samples from that of the closest ligands or proteins in the training set, already exhibit
good performances, suggesting that memorization largely dominates true learning"
(doi:10.1021/acs.jmedchem.2c00487, PMID 35608179) [VERIFIED-ABSTRACT]. Wallach and Heifets
quantified the mechanism across seven benchmarks with the AVE bias statistic and found "the
amount of AVE bias strongly correlates with the performance of ligand-based predictive methods
irrespective of the predicted property, chemical fingerprint, similarity measure, or previously
applied unbiasing techniques" (doi:10.1021/acs.jcim.7b00403, PMID 29698607)
[VERIFIED-ABSTRACT]. Sieg, Flachsenberg and Rarey put it plainly: "bias is learned implicitly
and unnoticed from standard benchmarks" (doi:10.1021/acs.jcim.8b00712, PMID 30835112)
[VERIFIED-ABSTRACT].

**The methodological fix that transfers is stratification, and protein contact prediction has
been doing it for twenty years.** CASP does not report a single contact-prediction accuracy; it
reports short-, medium- and long-range accuracy separately, where long-range means "those
involving residues separated by at least 24 residues along the sequence"
(doi:10.1002/prot.24340, PMID 23760879) [VERIFIED-ABSTRACT]. The reason is exactly ours: a
predictor that says "residues near each other in sequence are near each other in space" is
correct and uninformative, so the trivial baseline is removed by conditioning the metric rather
than by arguing about it. Sequence separation is to contact prediction what distance to the
active site is to us, and the field's answer was to make the stratified number the headline
number. Our repository already made the same choice; the literature says it is the right one.

**The "biggest pocket" baseline is strong for orthosteric sites and unmeasured for allosteric
ones.** fpocket reports detecting "94% and 92% of the pockets within the best three ranked
pockets from the holo and apo proteins respectively" (doi:10.1186/1471-2105-10-168)
[VERIFIED-ABSTRACT]. That is a pure geometry detector at ceiling for the ligand pocket. No
equivalent measurement of a geometric-only baseline against _allosteric_ sites was retrieved.

**Inside the allosteric field the critiques exist but they are leakage critiques, not
confound critiques.** AlloBench benchmarked seven tools — APOP, PASSer, Ohm, ALLO, Allosite,
STRESS and AlloPred — on a common 100-protein subset and found "the accuracy for all programs
is well below 60%, with PASSer (Ensemble) outperforming the rest", noting that "such a
large-scale benchmarking of these programs has not been undertaken on a common test set"
(doi:10.1021/acsomega.5c01263, PMID 40352555) [VERIFIED-ABSTRACT]. Ai and colleagues built two
independent sets, CAPASP-General (holo) and CAPASP-Unbound (apo), and found that PASSer and
APOP "performed better with the CAPASP-General subset than with the CAPASP-Unbound subset"
(doi:10.1007/s10822-026-00831-4, PMID 42126486) [VERIFIED-ABSTRACT] — degradation on exactly the
axis the challenge scores on. Pryakhin, Smaïl-Tabbone and Karami identified a mechanism:
"applying fpocket to holo structures without removing bound allosteric modulators introduces
data leakage and leads to artificially inflated performance estimates"
(doi:10.64898/2026.05.22.727284) [VERIFIED-ABSTRACT]. None of these three runs a distance-only
control.

**Our own numbers are the sharpest measurement of the specific confound anywhere in this
project.** From `09-data-analysis.md` §2.2 and §6, computed in-session on 72–73 curated
targets of the teammate benchmark: the best non-control method reaches plain AUC 0.6176 against
`ctrl_closeness = −distance` at 0.6166, a margin of +0.0010 with a paired bootstrap CI of
[−0.017, +0.019] and p = 0.909; and the share of each method's margin over 0.5 that disappears
under 2 Å distance stratification is **91.5 % for `btb_raw`, 84.3 % for `ctqw_only` and 97.3 %
for `qasc_baseline`**. Those are the numbers the literature does not supply for our task, and
they were derived from files on disk rather than quoted.

### Table

| Citation                                                         | Year | Method or finding                                 | Domain                            | What it measured                                                                                                      | Relevance to us                                                                                        |
| ---------------------------------------------------------------- | ---- | ------------------------------------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Chen et al., doi:10.1371/journal.pone.0220113                    | 2019 | Same CNN with and without the receptor            | Structure-based virtual screening | Mean AUC 0.98 both ways over 102 DUD-E targets; per-target R² = 0.98, slope 0.99                                      | The cleanest published case of a trivial baseline recovering **100 %** of a structural method's number |
| Volkov et al., doi:10.1021/acs.jmedchem.2c00487                  | 2022 | Modular GNN ablation; nearest-neighbour baselines | Binding-affinity prediction       | Noncovalent interaction description gives "no advantage"; memorisation dominates                                      | The ablation design — hide the channel the method claims to use — is the one to copy                   |
| Wallach & Heifets, doi:10.1021/acs.jcim.7b00403                  | 2018 | AVE bias statistic                                | Ligand-based classification       | Bias magnitude correlates with measured performance across seven benchmarks                                           | Formalises "performance is a property of the benchmark, not the method"                                |
| Sieg, Flachsenberg & Rarey, doi:10.1021/acs.jcim.8b00712         | 2019 | Re-evaluation of three benchmark sets             | Structure-based virtual screening | "Bias is learned implicitly and unnoticed from standard benchmarks"                                                   | Argues for designed validation experiments, not post-hoc excuses                                       |
| Monastyrskyy et al., doi:10.1002/prot.24340                      | 2013 | CASP10 contact assessment                         | Protein contact prediction        | Accuracy reported separately for short/medium/long range; long range = \|i−j\| ≥ 24                                   | The direct precedent for making the **stratified** number the headline number                          |
| Le Guilloux, Schmidtke & Tuffery, doi:10.1186/1471-2105-10-168   | 2009 | fpocket                                           | Pocket detection                  | 94 % (holo) and 92 % (apo) of ligand pockets in the top-3 ranked                                                      | A pure-geometry baseline at ceiling for orthosteric pockets; no allosteric equivalent retrieved        |
| Maity et al., doi:10.1021/acsomega.5c01263                       | 2025 | AlloBench pipeline; 7 tools on one test set       | Allosteric-site prediction        | Accuracy "well below 60%" for all seven                                                                               | Establishes that published allosteric numbers are not comparable across papers                         |
| Ai et al., doi:10.1007/s10822-026-00831-4                        | 2026 | CAPASP-General vs CAPASP-Unbound                  | Allosteric-site prediction        | PASSer and APOP better on holo than on apo                                                                            | The apo penalty is the axis the challenge scores on                                                    |
| Pryakhin, Smaïl-Tabbone & Karami, doi:10.64898/2026.05.22.727284 | 2026 | AlloDyn; benchmark-bias audit                     | Allosteric-site prediction        | fpocket on unstripped holo = leakage, "artificially inflated performance estimates"                                   | Names a concrete mechanism inflating the field's baseline numbers                                      |
| This repository, `09-data-analysis.md` §2.2, §6                  | 2026 | Plain vs 2 Å-stratified AUC, 72 targets           | Our task exactly                  | 84–97 % of the margin over 0.5 lost for the coherent-walk family; best method beats `−distance` by +0.0010, p = 0.909 | The confound size for **our** method family, measured rather than assumed                              |

**Not retrieved:** no paper was found that reports a _distance-to-a-named-source-only_ control
for a structural residue-ranking method. Recorded as not retrieved by the recorded search per
ADR 0019, not as absent.

---

## Q2 — Statistical methods for removing or conditioning on a confound

### Synthesis

Six families, in the order of increasing trustworthiness for our setting.

**(a) Regress the score on distance, keep the residual.** This is what `ALPS` and the
distance-corrected `btb` do, and on our data it works: `ALPS` has Spearman ρ = −0.045 against
distance (R² = 0.003) and `btb` has ρ = −0.016 (R² = 0.002), against ρ = −0.927 for `btb_raw`
(`09-data-analysis.md` §2.1). Three failure modes, each with a source.

_Functional-form misspecification._ A parametric decay fit that under-fits leaves a residual
trend that the metric then reads as signal. Binned medians and kernel smoothers are safer
because they are non-parametric, at the cost of variance in sparse bins.

_The residual is not a substitute variable._ García-Berthou showed that "the regression
coefficient used by the residual index differs from the one used in ANCOVA" and that the linear
model assumptions fail when applied to residuals rather than to the original variables
(doi:10.1046/j.1365-2656.2001.00524.x) [VERIFIED-ABSTRACT]; Freckleton's companion paper argues
the same case against residual regression and for multiple regression
(doi:10.1046/j.1365-2656.2002.00618.x) [VERIFIED-ABSTRACT]. The correct partialling residualises
**both** variables, not only the score. If we residualise the score against distance and then
correlate the residual with a raw label indicator, the estimand is not the partial association.

_Heteroscedasticity._ Mean regression removes a trend in the mean, not in the spread. If the
score's variance shrinks with distance — which it does for any propagation score, because the
amplitude decays — a residual near the source is a different animal from a residual far away.
Quantile normalisation (Q4) is the fix.

**(b) Rank-based partial and semi-partial correlation.** Spearman partial correlation is the
Pearson partial correlation of the ranks; `ppcor::pcor.test(..., method = "spearman")` and
`spcor.test` implement both (doi:10.5351/csam.2015.22.6.665) [VERIFIED-ABSTRACT]. Assumption:
the confound enters linearly _in the ranks_. This is much weaker than linearity in the raw
variable and is usually adequate for a monotone radial decay. It fails when the confound
interacts with the label — when, say, distance helps at one arm and hurts at another. Our
own data says that happens: on curated expert labels `ctrl_closeness` wins at AUC 0.6166; on
proxy tier-B labels the opposite control `ctrl_dist` wins at 0.6136 (`09-data-analysis.md`
§2.4). A single pooled partial correlation across arms would average those to nothing.

**(c) Stratified or conditional evaluation.** Bin residues by distance and score within bins;
or match each positive to negatives at similar distance and compute a matched-pair AUC. The
formal machinery is the covariate-adjusted ROC curve of Janes and Pepe
(doi:10.1093/biomet/asp002) [VERIFIED-ABSTRACT], which is the right citation if we ever need to
defend the estimator in the report. Assumptions: within a stratum the confound is exchangeable,
and enough matched pairs survive to estimate anything. Both are checkable, and our repository
has already checked them — the tolerance sweep in `09-data-analysis.md` §2.3 shows
`ctrl_closeness` sitting at 0.489–0.494 for τ ≤ 2 Å and rising monotonically to 0.573 at τ = ∞,
with matched pairs falling from 2448 to 104 as τ tightens from ∞ to 0.5 Å. That is the
bias–variance trade-off made visible, and 2 Å is where it is resolved.

**(d) Matched-control and propensity-style designs.** The matched-patch null is a matched
design at the patch level; its ancestry is Rosenbaum and Rubin's propensity score
(doi:10.1093/biomet/70.1.41) [VERIFIED-ABSTRACT]. The assumption is strong ignorability: no
unmeasured confounder distinguishes a true patch from a matched decoy patch. The specific
danger here is **over-matching**. Real allosteric sites _are_ somewhat distal, so distance is on
the causal path, not merely alongside it; matching it away discards genuine signal along with
the artefact. The correct posture is to report both the matched and the unmatched number and to
name the discarded quantity, not to pretend the matched number is the only true one.

**(e) Permutation nulls that preserve spatial autocorrelation.** This is the part of the
machinery that structural biology does not have and neuroimaging does.

_Why the naive version fails._ Legendre's classic statement is that spatial autocorrelation is
"a very general statistical property of ecological variables observed across geographic space"
whose "most common forms are patches and gradients", and that it breaks the independence
assumption behind ordinary tests (doi:10.2307/1939924) [VERIFIED-ABSTRACT]. Clifford, Richardson
and Hémon derived the effective-sample-size correction for the correlation of two spatial
processes (doi:10.2307/2532039) [VERIFIED-ABSTRACT]; Dutilleul extended it to a modified _t_
test (doi:10.2307/2532625) [VERIFIED-ABSTRACT]. Markello and Misic measured the consequence
directly for brain maps across ten null frameworks: "naive null models that do not preserve
spatial autocorrelation consistently yield elevated false positive rates"
(doi:10.1016/j.neuroimage.2021.118052; quote from the preprint record,
doi:10.1101/2020.08.13.249797) [VERIFIED-ABSTRACT]. Our own null-calibration experiment found
the same thing on our own arms: the unmatched background permutation has a measured type-I rate
of 0.096–0.323 at a nominal 0.05 (`09-data-analysis.md` §8).

_The spin test (Alexander-Bloch et al. 2018)._ Algorithm: represent each region by a coordinate
on a spherical representation of the cortical surface; draw a uniform random rotation from
SO(3); apply it to every coordinate; reassign each original region the value of its nearest
rotated neighbour; recompute the test statistic; repeat. The paper describes it as generating
"null models of overlap by applying random rotations to spherical representations of the
cortical surface", with "a theoretical statistical foundation" and reference code at
github.com/spin-test (doi:10.1016/j.neuroimage.2018.05.070, PMID 29860082) [VERIFIED-ABSTRACT].
The rotation is rigid, so the surrogate field has the target's autocorrelation exactly.
**This one does not transfer to a protein.** It requires a spherical parameterisation of the
domain, and a protein has none. Projecting residues radially onto an enclosing sphere and
rotating would scramble radial depth, which is precisely the burial axis our null already
controls. Do not use it, and say why in the report rather than leaving the omission unexplained.

_Variogram-matched surrogates (BrainSMASH; Burt et al. 2020)._ This one **does** transfer,
because its only geometric input is a pairwise distance matrix. Algorithm, verified from the
package documentation: (1) compute the variogram of the target map from the distance matrix;
(2) randomly permute the map values, which "breaks its spatial structure and randomizes its
topography"; (3) reintroduce autocorrelation by smoothing the permuted map with a
distance-dependent, typically exponentially decaying kernel over the _k_ nearest neighbours;
(4) compute the smoothed map's variogram and regress it onto the empirical map's variogram;
(5) score the fit by the sum of squared error; (6) sweep _k_ and take the minimiser; (7) emit
surrogates at that _k_. Inputs required: the map and a distance matrix — geodesic on a surface,
Euclidean in a volume (brainsmash.readthedocs.io/en/latest/approach.html)
[VERIFIED-FULLTEXT]; paper doi:10.1016/j.neuroimage.2020.117038 [VERIFIED-ABSTRACT]. For us the
distance matrix is Cα–Cα or Cβ–Cβ, which we already build. Implementations:
`brainsmash.mapgen.base.Base` and `brainsmash.mapgen.sampled.Sampled`, and
`neuromaps.nulls.burt2020` (doi:10.1038/s41592-022-01625-w) [VERIFIED-ABSTRACT].

**A caveat that decides how to use it, and that the neuroimaging literature does not have to
worry about.** The variogram is a function of the distance _between pairs of points_, not of the
distance _from a fixed source_. Variogram matching therefore reproduces the field's smoothness,
not its radial trend about the active site, and it assumes stationarity — which a field with a
monotone decay from a named source violates. A variogram-matched null is **not** a
distance-confound control. It is a smoothness control. The two must be composed: remove the
radial trend first (Q4), then generate variogram-matched surrogates of the _residual_ field.

_Moran spectral randomisation (Wagner & Dray 2015)._ Also transfers, and needs only a spatial
weights matrix — for us, the contact-graph adjacency or a distance kernel. The paper motivates
it by noting that "spatial autocorrelation jeopardizes the validity of statistical inference"
and offers restricted randomisation with "technically unlimited numbers of randomizations"
(doi:10.1111/2041-210x.12407) [VERIFIED-ABSTRACT]. Algorithm: build the weights matrix W;
doubly centre it; take its eigenvectors, the Moran eigenvector maps; project the observed
variable onto that basis; randomise the projection coefficients while preserving their squared
amplitude spectrum — by random sign flips (`singleton`), by random rotations within pairs
(`pair`), or by triplets; reconstruct. The Moran coefficient is preserved exactly or in
expectation depending on the procedure. Implementations: `adespatial::msr` in R,
`brainspace.null_models.MoranRandomization` in Python, `neuromaps.nulls.moran`.

**(f) Does residualising before or after a nonlinear ranking step change the residual?** Yes,
and the direction matters for us.

Rank transformation is monotone, so a Spearman correlation is invariant to it. Residualisation
is not monotone, so _rank-then-residualise_ and _residualise-then-rank_ produce different
residuals. The conditioned metric we report is a rank statistic, so the residual that should
feed it is the rank-space one: convert to within-arm rank percentile first, then remove the
distance trend from the percentile. That way the residual does not inherit the raw score's
scale, skew or heteroscedasticity.

The order that matters more, and that is easy to get wrong, is **residualisation versus spatial
smoothing**. Pocket-smoothing — averaging a residue's score over its geometric neighbours — is a
spatial low-pass filter. Applied _after_ residualisation it re-imports a distance trend, because
each residue's neighbours sit at a similar distance from the source and their shared trend
survives the average. **Residualise after smoothing, never before.** The benchmark's own
post-processing pipeline is raw score → rank percentile → pocket smoothing, and
`09-data-analysis.md` §2.1 correlates against distance at the end of that chain, which is the
right place; any confound removal must be inserted at the same point and not earlier.

### Table

| Citation                                                                    | Year | Method or finding                                      | Domain                | What it measured                                                                                                          | Relevance to us                                                                                  |
| --------------------------------------------------------------------------- | ---- | ------------------------------------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| García-Berthou, doi:10.1046/j.1365-2656.2001.00524.x                        | 2001 | Residual index vs ANCOVA                               | Ecology               | The residual index's coefficient differs from ANCOVA's; model assumptions fail on residuals                               | Our detrend-then-score pipeline is a residual index; the estimand is not the partial association |
| Freckleton, doi:10.1046/j.1365-2656.2002.00618.x                            | 2002 | Regression of residuals vs multiple regression         | Ecology               | Companion critique                                                                                                        | Same; argues for putting the confound in the model instead                                       |
| Kim, doi:10.5351/csam.2015.22.6.665                                         | 2015 | `ppcor`                                                | Statistics software   | Partial and semi-partial correlations, Pearson/Spearman/Kendall                                                           | Names the function for the rank-based partial correlation                                        |
| Janes & Pepe, doi:10.1093/biomet/asp002                                     | 2009 | Covariate-adjusted ROC (AROC)                          | Biostatistics         | Classification accuracy conditional on a covariate                                                                        | The formal name and theory for our distance-stratified AUC                                       |
| Rosenbaum & Rubin, doi:10.1093/biomet/70.1.41                               | 1983 | Propensity score                                       | Causal inference      | Balancing on a scalar summary of covariates                                                                               | The ancestry of the matched-patch null; supplies the ignorability assumption to state            |
| Legendre, doi:10.2307/1939924                                               | 1993 | Spatial autocorrelation                                | Ecology               | Patches and gradients break independence                                                                                  | Why residue-level permutation is invalid                                                         |
| Clifford, Richardson & Hémon, doi:10.2307/2532039                           | 1989 | Effective sample size for correlated spatial processes | Biometrics            | Corrected variance of a spatial correlation                                                                               | The analytic alternative to permutation                                                          |
| Dutilleul, doi:10.2307/2532625                                              | 1993 | Modified _t_ test                                      | Biometrics            | Correlation between two spatial processes                                                                                 | Same family                                                                                      |
| Alexander-Bloch et al., doi:10.1016/j.neuroimage.2018.05.070, PMID 29860082 | 2018 | Spin test                                              | Neuroimaging          | SO(3) rotations of a spherical surface representation                                                                     | Canonical, exact autocorrelation preservation — but **needs a sphere, so it does not transfer**  |
| Burt et al., doi:10.1016/j.neuroimage.2020.117038                           | 2020 | BrainSMASH variogram-matched surrogates                | Neuroimaging          | Permute, smooth, match variogram, sweep bandwidth                                                                         | **Transfers unchanged** — only needs a distance matrix. Controls smoothness, not a radial trend  |
| Burt et al., doi:10.1038/s41593-018-0195-0                                  | 2018 | Spatial-lag surrogate maps                             | Neuroimaging          | Autoregressive surrogates matched on an autocorrelation parameter                                                         | The parametric sibling; `neuromaps.nulls.burt2018`                                               |
| Wagner & Dray, doi:10.1111/2041-210x.12407                                  | 2015 | Moran spectral randomisation                           | Ecology               | Restricted randomisation preserving the Moran coefficient                                                                 | **Transfers unchanged** — needs only a weights matrix, which is our contact graph                |
| Markello & Misic, doi:10.1016/j.neuroimage.2021.118052                      | 2021 | Ten null frameworks compared                           | Neuroimaging          | Naive nulls "consistently yield elevated false positive rates"                                                            | The measured case for spending the effort                                                        |
| Váša & Mišić, doi:10.1038/s41583-022-00601-9                                | 2022 | Review of null models                                  | Network neuroscience  | Catalogue of rewiring, geometric and spatial nulls                                                                        | The single best orientation document for choosing a null                                         |
| Markello et al., doi:10.1038/s41592-022-01625-w                             | 2022 | `neuromaps`                                            | Neuroimaging software | Bundles `alexander_bloch`, `burt2018`, `burt2020`, `moran`, `vasa`, `cornblath`, `hungarian`, `baum`, `vazquez_rodriguez` | One package, several nulls, readable source to port                                              |

---

## Q3 — Structural descriptors that are genuinely not a function of distance to a source

### Synthesis

The test to apply is narrow: **is the descriptor a monotone function of Euclidean distance to
the active site?** A descriptor can pass that test and still be useless to us, because there is
a second confound — burial — which `../exploration/lit/24-residue-descriptors.md` shows absorbs
almost every packing descriptor in the literature, and which our null already controls. So each
candidate needs two verdicts: distance-orthogonal, and burial-orthogonal.

**Evolutionary conservation.** Distance-orthogonal by construction: it is computed from a
sequence alignment with no coordinates. Burial-orthogonal: partly — conservation correlates with
burial. The evidence on allostery is asymmetric and unflattering. AR-Pred, which trained on both
site classes with a conservation feature, found the conservation score to be the most important
feature overall but "significantly more important for active site than for allosteric site
detection", with median AUC 91 % for active sites against 80 % for allosteric
(doi:10.1002/prot.25749) [VERIFIED-ABSTRACT]. Riedlová and colleagues, on 453 human kinases,
place allosteric pockets in "predominantly neutrally frustrated zones associated with
conformational plasticity and reduced evolutionary constraint" and call them "often transient,
weakly conserved" (doi:10.1021/acs.jctc.6c00427; quoted from
`../exploration/lit/24-residue-descriptors.md` §4.4, verified full-text there)
[VERIFIED-ABSTRACT for the record, full text verified in the sibling file]. Verdict: legal,
distance-orthogonal, weak prior. Keep it as a confounder column, not a predictor.

**Coevolution and direct coupling analysis.** This is the most distance-orthogonal object
available — a residue–residue coupling matrix computed from sequence alone with no geometry
whatsoever. Morcos and colleagues established that DCA "is shown to yield a large number of
correctly predicted contacts" across many families (doi:10.1073/pnas.1111471108)
[VERIFIED-ABSTRACT]; plmDCA improved the inference by pseudolikelihood
(doi:10.1103/physreve.87.012707) [VERIFIED-ABSTRACT]; GREMLIN combined it with structural
information (doi:10.1073/pnas.1314045110) [VERIFIED-ABSTRACT].

**And that is precisely the problem.** DCA's demonstrated skill is _contact prediction_. Its
top-ranked couplings are, by its own validation, the 3D contact map — which we already have and
which is the substrate of the graph. Feeding DCA's top couplings into our pipeline would be
re-deriving the input. The distance-orthogonal information is the **residual**: strong couplings
between residues that are _not_ in spatial contact. In the contact-prediction literature those
are the false positives; in the allostery literature they are the candidate long-range
functional couplings. That reframing is the only construction here that is not circular, and it
is our construction — **no published measurement of non-contacting DCA couplings as an
allosteric-site score was retrieved.** Cost: a deep MSA. `24-residue-descriptors.md` §4.3 records
the depth requirement — tens of thousands of effective sequences for L ≥ 100 — and notes that
nearly all real inference operates in the undersampled regime.

**SCA sectors — investigated hard, as the brief asked, and the answer is negative.** The
positive claims are real and are the reason SCA is the natural first guess. Lockless and
Ranganathan developed "a technique … that uses evolutionary data for a protein family to
measure statistical interactions between amino acid positions" (doi:10.1126/science.286.5438.295)
[VERIFIED-ABSTRACT]. Süel and colleagues generalised it to "evolutionarily conserved networks of
residues mediate allosteric communication in proteins" (doi:10.1038/nsb881) [VERIFIED-ABSTRACT].
Halabi and colleagues decomposed the S1A proteases into sectors
(doi:10.1016/j.cell.2009.07.038) [VERIFIED-ABSTRACT]. And Reynolds, McLaughlin and Ranganathan
made the claim that matters to us exactly: on DHFR, "sector-connected surface sites are
statistically preferred locations for the emergence of allosteric control in vivo"
(doi:10.1016/j.cell.2011.10.049, PMID 22196731) [VERIFIED-ABSTRACT].

The evidence against is specific, quantitative, and it targets the load-bearing link.

- Fodor and Aldrich compared four correlated-mutation methods and found "a surprising lack of
  agreement between the four correlated mutation methods", attributing the disagreement to
  differing sensitivity to background conservation (doi:10.1002/prot.20098) [VERIFIED-ABSTRACT].
- Teşileanu, Colwell and Leibler re-examined the experimental data behind sectors and observed
  that "it involves almost exclusively proteins with a single sector", in which case "sequence
  conservation is the dominating factor in SCA". Their numbers: for the PDZ domain the SCA
  sector was 67 % functionally significant against a 25 % background, but **the top 21 most
  conserved residues identified the same functional positions, Mann-Whitney p = 0.9**; for DHFR
  the sector touched all 14 functionally significant sites and conservation touched 12,
  **p = 0.2** (doi:10.1371/journal.pcbi.1004091) [VERIFIED-FULLTEXT].

So the chain "SCA sectors → allosteric sites" breaks at both links. At the first link, sectors
are not distinguishable from conservation on the systems where they were tested. At the second,
conservation is a weak allosteric discriminator and a strong catalytic one — and our benchmark
_hands the method the active site_, so a descriptor whose demonstrated skill is finding the
active site cannot score on our endpoint. There is a third problem, of validation design: sector
membership is validated by mutating sector residues and observing a functional effect, which
tests "these residues matter", not "these residues form a druggable allosteric pocket". That is
a different proposition and it is the one the challenge scores.

**The brief's prior that SCA sectors are the single most promising distance-orthogonal signal is
not supported by the retrieved evidence.** Reynolds 2011 remains the strongest single claim in
the literature for a sequence-derived allosteric-site detector, and it is one enzyme with no
extractable effect size — the abstract gives no count of surface sites tested and no fraction
showing an effect.

**Protein language models.** Distance-orthogonal in their _input_ — sequence only — but not in
their _representation_: Rao and colleagues showed that "Transformer attention maps learn
contacts from the unsupervised language modeling objective" (doi:10.1101/2020.12.15.422761)
[VERIFIED-ABSTRACT], so a pLM's internals encode the geometry we are trying to be independent
of. On our class specifically the evidence is bad: Riedlová reports AUROC 0.968 for Type I
kinase sites falling to **0.676 for Type IV distal allosteric sites**, described as a
"near-random ranking regime" (doi:10.1021/acs.jctc.6c00427; via
`../exploration/lit/24-residue-descriptors.md` §5, full-text verified there), converging with
the AUPR 0.06-on-allosteric figure already in `00-conventions.md` §5. The field's own response
is instructive: Eccleston and Furnham found the plain pLM classifier insufficient and added "a
structure-aware conditioning mechanism, whereby orthosteric binding sites are encoded and
integrated directly into the input embeddings", which "improves upon the performance of the
first two methods and achieves results comparable to the leading structure-based allosteric site
predictors" (doi:10.1101/2025.06.27.662060) [VERIFIED-ABSTRACT]. **That is our setting** — we are
given the active site — and it is the strongest published signal that source-conditioning is the
right framing. DeepAllo reports "89.66% F1 score and 90.5% of allosteric pockets in the top 3
positions" from a fine-tuned pLM plus fpocket features (doi:10.1093/bioinformatics/btaf294)
[VERIFIED-ABSTRACT], but the number is a top-3-pocket rate on ASD-supervised labels and is not
comparable to our endpoint.

**Cavity and pocket geometry.** Local shape descriptors, computed without reference to where the
active site is, so distance-orthogonal by construction. Tools: fpocket
(doi:10.1186/1471-2105-10-168), its druggability score (doi:10.1021/jm100574m)
[VERIFIED-ABSTRACT], CASTp 3.0 (doi:10.1093/nar/gky473) [VERIFIED-ABSTRACT], pyKVFinder, which
reports "volume, area, depth and hydropathy, storing these cavity properties in NumPy arrays"
and is designed to be called from Python rather than a server
(doi:10.1186/s12859-021-04519-4) [VERIFIED-ABSTRACT]. Strong, cheap, real — `00-conventions.md`
§6 already records that `cavity_volume` rejects the null on all three confirmatory arms. Two
cautions: it is the field's universal first stage, so it is not a differentiator; and Pryakhin
2026 shows that running it on an unstripped holo structure is leakage.

**Local flexibility and rigidity.** FIRST counts degrees of freedom in a covalent-plus-hydrogen-
bond constraint network, identifies rigid and flexible substructures from "a single, static
three-dimensional structure", and is "approximately a million times faster than molecular
dynamics simulations" (doi:10.1002/prot.1081) [VERIFIED-ABSTRACT]. Sljoka's rigidity-transmission
allostery is the direct application (doi:10.1007/978-1-0716-1154-8_5) [VERIFIED-ABSTRACT].
Distance-orthogonal: yes, rigid-cluster membership is topological. Cost: hydrogens must be
placed and an H-bond energy cut-off chosen, which is the same C6 argument
`24-residue-descriptors.md` §7 item 8 already deferred on. **No dataset-level allosteric ROC was
retrieved — case studies only.**

**Packing density, contact order, residue depth, protrusion.** Settled by
`24-residue-descriptors.md` §1: residue depth, DPX, CX, occluded surface, Voronoi volume and
weighted contact number are one axis, the burial axis, already in the null. The single exception
is per-residue local contact order — mean \|i − j\| over a residue's contacts — which is
orthogonal to burial by construction and is already implemented in `allo.classical.baselines`.
Do not re-open the rest.

**Secondary structure, hinges, domain boundaries.** PACKMAN predicts hinges from a single static
structure using alpha shapes (doi:10.1016/j.jmb.2019.11.018) [VERIFIED-ABSTRACT], with hdANM as
the dynamics follow-on (doi:10.1016/j.bpj.2021.10.017) [VERIFIED-ABSTRACT] and a Python toolbox
(doi:10.1093/bioadv/vbac007) [VERIFIED-ABSTRACT]. Distance-orthogonal: yes. The warning is in
`../exploration/lit/25-md-free-fluctuation.md`: catalytic sites sit at global-hinge _minima_ in
over 70 % of 98 enzymes, so a naive hinge or fluctuation ranking returns the negative class.

**Spectral and modal descriptors that are local rather than radial.** This is where our own
measurements already place the best candidates, and it is the most decision-relevant paragraph
in this section. From `09-data-analysis.md` §2.1, Spearman against distance inside the candidate
pool: `ALPS` −0.045 (R² 0.003), `apop` −0.112 (R² 0.026), `mode_ipr_dipr` −0.122 (R² 0.038),
`eigvec_dpart` −0.306 (R² 0.093), against `qfi` at −0.956 (R² 0.915) and `ctqw_only` at −0.651
(R² 0.423). The ENM spectral readouts are the only descriptors we have measured that are
simultaneously distance-orthogonal and above chance. Their literature: ESSA
(doi:10.1016/j.csbj.2020.06.020, PMID 32637054) [VERIFIED-ABSTRACT] and APOP, which "perturbs
the pockets formed in the structure by stiffening pairwise interactions" and reports the known
allosteric site among the top three in **92 of 104 cases** (doi:10.1093/bioinformatics/btad275)
[VERIFIED-ABSTRACT] — a number AlloBench's leakage-controlled retest cuts to 15 % at Jaccard

> 0.5 (`00-conventions.md` §6). The _ratio_ of a residue's mode participation to its degree,
> which the brief proposes, was **not retrieved anywhere** and is our construction; it costs one
> line given the eigenvectors we already compute.

**Thermodynamic and stability descriptors — local frustration is the strongest new candidate in
this file.** Frustration asks whether a residue's native interactions are energetically better
than the same interactions with decoy residues or decoy geometries, and it is explicitly not a
geometric quantity. Ferreiro and colleagues established that "natural proteins are multiply
connected by a web of local interactions that are individually minimally frustrated" while
"highly frustrated interactions are found clustered on the surface, often near binding sites"
(doi:10.1073/pnas.0709915104) [VERIFIED-ABSTRACT]. The allostery-specific paper is the one to
lean on: "regions that reconfigure are often enriched in patches of highly frustrated
interactions", functioning as mechanical hinges in allosteric proteins
(doi:10.1073/pnas.1018980108) [VERIFIED-ABSTRACT]. Freiberger and colleagues quantified the
complementary statement for the class we are _given_: energetic conflicts around enzyme active
sites, conserved beyond primary-structure variation (doi:10.1073/pnas.1819859116)
[VERIFIED-ABSTRACT]. FrustratometeR's own summary ties frustration to "protein–protein
interactions, small ligand recognition, catalytic sites and allostery"
(doi:10.1093/bioinformatics/btab176) [VERIFIED-ABSTRACT]. And Riedlová's differential claim —
orthosteric pockets in minimally frustrated basins, allosteric pockets in neutrally frustrated
zones — is a _contrast between the two classes_, which is exactly our endpoint.

Three honest caveats. (i) The frustration index is computed against an energy function — AWSEM
in the Frustratometer family — which raises the same C6 question as Poisson-Boltzmann in
`24-residue-descriptors.md` §7 item 7. It needs an ADR before implementation. (ii) It is
burial-correlated: frustration is elevated at surfaces, so it must be reported against RSA.
(iii) No dataset-level ROC for allosteric-site localisation from frustration alone was
retrieved; the only quantitative allosteric result is embedded inside Riedlová's supervised pLM
pipeline. Tools: Protein Frustratometer 2 (doi:10.1093/nar/gkw304) [VERIFIED-ABSTRACT],
FrustratometeR (doi:10.1093/bioinformatics/btab176) [VERIFIED-ABSTRACT].

**Predicted ΔΔG of mutation.** Distance-orthogonal, but two strikes: it needs a force field
(C6), and `24-residue-descriptors.md` §1.2 records that residue depth is already a good ΔΔG
predictor, which makes ΔΔG partly a burial proxy. Low priority.

### Table

| Citation                                                                          | Year | Method or finding                                   | Domain                      | What it measured                                                                                                                             | Relevance to us                                                                                   |
| --------------------------------------------------------------------------------- | ---- | --------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Lockless & Ranganathan, doi:10.1126/science.286.5438.295                          | 1999 | SCA                                                 | Sequence coevolution        | Statistical coupling between alignment positions                                                                                             | The origin of the sector idea                                                                     |
| Süel et al., doi:10.1038/nsb881                                                   | 2003 | Conserved networks mediate allosteric communication | Sequence coevolution        | Sparse connected networks across GPCRs, proteases, haemoglobins                                                                              | The strongest conceptual claim for sequence-derived allostery                                     |
| Halabi et al., doi:10.1016/j.cell.2009.07.038                                     | 2009 | Protein sectors                                     | Sequence coevolution        | Three quasi-independent sectors in S1A proteases                                                                                             | Multi-sector case; the case Teşileanu says was never tested                                       |
| Reynolds, McLaughlin & Ranganathan, doi:10.1016/j.cell.2011.10.049, PMID 22196731 | 2011 | Sector-connected surface sites                      | DHFR                        | "Statistically preferred locations for the emergence of allosteric control in vivo"                                                          | The single best published claim — **one enzyme, no extractable effect size**                      |
| **Teşileanu, Colwell & Leibler, doi:10.1371/journal.pcbi.1004091**                | 2015 | SCA versus conservation                             | Sequence coevolution        | PDZ: sector 67 % vs 25 % background, but top-21 conserved gives the same positions, p = 0.9. DHFR: sector 14/14, conservation 12/14, p = 0.2 | **Removes SCA's advantage over conservation on every system where SCA was experimentally tested** |
| Fodor & Aldrich, doi:10.1002/prot.20098                                           | 2004 | Four covariance methods compared                    | Sequence coevolution        | "A surprising lack of agreement", driven by conservation sensitivity                                                                         | Independent, earlier version of the same critique                                                 |
| Mishra, Kandoi & Jernigan (AR-Pred), doi:10.1002/prot.25749                       | 2019 | Random forest on geometry + evolution + dynamics    | Allosteric and active sites | Median AUC 91 % active vs 80 % allosteric; conservation "significantly more important for active site"                                       | Direct measurement that conservation is the weaker signal for our class                           |
| Morcos et al., doi:10.1073/pnas.1111471108                                        | 2011 | DCA                                                 | Sequence coevolution        | Native contacts recovered across many families                                                                                               | Zero-geometry couplings — but validated _as_ geometry                                             |
| Ekeberg et al., doi:10.1103/physreve.87.012707                                    | 2013 | plmDCA                                              | Sequence coevolution        | Pseudolikelihood inference of Potts models                                                                                                   | The implementation to use if DCA is attempted                                                     |
| Kamisetty, Ovchinnikov & Baker, doi:10.1073/pnas.1314045110                       | 2013 | GREMLIN                                             | Sequence coevolution        | Coevolution plus structure over 400+ families                                                                                                | Same                                                                                              |
| Rao et al., doi:10.1101/2020.12.15.422761                                         | 2020 | Attention maps learn contacts                       | Protein language models     | Unsupervised contact recovery from attention                                                                                                 | **pLM internals encode geometry** — attention is not distance-orthogonal                          |
| Lin et al., doi:10.1126/science.ade2574                                           | 2023 | ESM-2                                               | Protein language models     | Atomic-level structure from sequence                                                                                                         | The model whose entropies `24` proposes as the conservation substitute                            |
| Eccleston & Furnham, doi:10.1101/2025.06.27.662060                                | 2025 | pLM with orthosteric conditioning                   | Allosteric-site prediction  | Conditioning on the orthosteric pocket beats unconditioned pLM heads                                                                         | **Independent support that source-conditioning is the right framing**                             |
| Khokhar, Keskin & Gursoy (DeepAllo), doi:10.1093/bioinformatics/btaf294           | 2025 | pLM + fpocket, multitask                            | Allosteric-site prediction  | 89.66 % F1, 90.5 % top-3 pockets                                                                                                             | Not comparable to our endpoint; supervised on ASD labels                                          |
| Le Guilloux, Schmidtke & Tuffery, doi:10.1186/1471-2105-10-168                    | 2009 | fpocket                                             | Pocket geometry             | 94 %/92 % top-3 ligand pockets                                                                                                               | Local shape, distance-orthogonal, near-ceiling for orthosteric                                    |
| Schmidtke & Barril, doi:10.1021/jm100574m                                         | 2010 | Druggability score                                  | Pocket geometry             | Drug-binding-site detection                                                                                                                  | Adds a chemistry axis to volume                                                                   |
| Tian et al., doi:10.1093/nar/gky473                                               | 2018 | CASTp 3.0                                           | Pocket geometry             | Alpha-shape pockets and mouths                                                                                                               | Alternative pocket detector for a robustness check                                                |
| Guerra et al., doi:10.1186/s12859-021-04519-4                                     | 2021 | pyKVFinder                                          | Pocket geometry             | Volume, area, depth, hydropathy as NumPy arrays                                                                                              | Callable offline from Python — fits our gate                                                      |
| Jacobs et al. (FIRST), doi:10.1002/prot.1081                                      | 2001 | Pebble-game rigidity                                | Constraint theory           | Rigid clusters from one static structure, ~10⁶× faster than MD                                                                               | Best conceptual fit; C6 argument and no benchmark number                                          |
| Sljoka, doi:10.1007/978-1-0716-1154-8_5                                           | 2020 | Rigidity transmission allostery                     | Allostery                   | Long-range rigidity propagation                                                                                                              | The allosteric application of the pebble game                                                     |
| Khade, Savol & Jernigan, doi:10.1016/j.jmb.2019.11.018                            | 2020 | PACKMAN hinge prediction                            | Single-structure dynamics   | Hinges from alpha shapes                                                                                                                     | Distance-orthogonal topology descriptor; no allosteric ROC retrieved                              |
| Kaynak, Bahar & Doruker (ESSA), doi:10.1016/j.csbj.2020.06.020, PMID 32637054     | 2020 | Essential site scanning                             | Elastic network models      | Sites that modulate global-mode dispersion                                                                                                   | Our own data: near-zero distance correlation                                                      |
| Kumar et al. (APOP), doi:10.1093/bioinformatics/btad275                           | 2023 | Pocket stiffening + global-mode shift               | Elastic network models      | 92/104 known sites in the top 3                                                                                                              | Best published unsupervised ENM number; cut to 15 % under AlloBench's leakage control             |
| Ferreiro et al., doi:10.1073/pnas.0709915104                                      | 2007 | Localizing frustration                              | Energy landscapes           | Highly frustrated interactions cluster on the surface near binding sites                                                                     | The founding measurement                                                                          |
| **Ferreiro et al., doi:10.1073/pnas.1018980108**                                  | 2011 | Frustration in allosteric proteins                  | Energy landscapes           | "Regions that reconfigure are often enriched in patches of highly frustrated interactions"                                                   | **The allostery-specific claim; a non-geometric energetic quantity on a static structure**        |
| Freiberger et al., doi:10.1073/pnas.1819859116                                    | 2019 | Frustration around active sites                     | Energy landscapes           | Energetic conflicts at catalytic sites, conserved beyond sequence                                                                            | The complementary class — useful as a positive control since we are given the active site         |
| Parra et al., doi:10.1093/nar/gkw304                                              | 2016 | Protein Frustratometer 2                            | Software                    | Local frustration with electrostatics                                                                                                        | The tool                                                                                          |
| Rausch et al., doi:10.1093/bioinformatics/btab176                                 | 2021 | FrustratometeR                                      | Software                    | Frustration for structures, point mutants, MD                                                                                                | The scriptable tool; its own text names allostery                                                 |
| Riedlová et al., doi:10.1021/acs.jctc.6c00427                                     | 2026 | pLM + structure + frustration, explainable          | Kinase binding sites        | Type IV distal allosteric AUROC 0.676 vs Type I 0.968; allosteric pockets in neutrally frustrated zones                                      | Both the negative pLM result and the positive frustration contrast                                |

---

## Q4 — Normalisations that cancel a radial trend by construction

### Synthesis

Four constructions, of which one is already standard practice inside the allosteric field and
three are imports.

**1. Conditional-quantile normalisation against distance. This is the field's own answer and we
should adopt its exact form.** Bond-to-bond propensity analysis does not report a raw
propensity; it reports a quantile score, and the reference distribution is conditioned on
distance from the active site. From the paper's own text: "the quantile score of a bond p_b is a
measure of how high the propensity Π_b is relative to other bonds in the sample which are at a
similar distance from the active site", obtained by quantile regression on log-transformed
propensities (doi:10.1101/056275, published as doi:10.1038/ncomms12477, PMID 27561351)
[VERIFIED-FULLTEXT]. Two properties make this better than a mean residual: it conditions on
distance non-parametrically at each quantile level rather than only in the mean, and it is
therefore immune to the heteroscedasticity that any decaying propagation score has. Our own data
confirms it works on a real score: `btb_raw` has ρ = −0.927 against distance (R² = 0.859) and
the quantile-corrected `btb` has ρ = −0.016 (R² = 0.002), with the collinearity with distance
falling from VIF 7.3 to 1.1 (`09-data-analysis.md` §2.1, §3).

**2. Observed-over-expected against a distance-dependent background, with per-element
p-values. This is the mature version and it comes from Hi-C.** A Hi-C contact matrix has exactly
our pathology: contact frequency decays steeply and monotonically with genomic distance, so any
raw ranking of contacts returns "close in sequence". The field's fix, from the original paper,
is the observed/expected normalisation (doi:10.1126/science.1181369) [VERIFIED-ABSTRACT]; the
statistically complete version is Fit-Hi-C, which assigns confidence estimates by "jointly
modeling the random polymer looping effect and previously observed technical biases", i.e. by
fitting the distance-dependent expectation with a spline and testing each pair against it with
multiplicity control (doi:10.1101/gr.160374.113) [VERIFIED-ABSTRACT]; FitHiC2 is the current
implementation (doi:10.1038/s41596-019-0273-0) [VERIFIED-ABSTRACT]. Transferred to us: fit
E[score | d] over the candidate pool with a monotone spline or isotonic regression, model the
residual dispersion as a function of d, assign each residue a one-sided p-value against its own
distance-matched expectation, and apply Benjamini-Hochberg within the arm. This gives a
per-residue significance rather than only a corrected ranking, which is what a top-5 hit list
should be built from.

**3. Surrogate-graph z-scores, but geometry-preserving ones.** The reflex is a degree-preserving
rewiring: Maslov and Sneppen's switching algorithm (doi:10.1126/science.1065103)
[VERIFIED-ABSTRACT] and Milo's network-motif z-score against randomised networks
(doi:10.1126/science.298.5594.824) [VERIFIED-ABSTRACT]. **For a spatially embedded graph that
null is wrong and it over-rejects**, because it destroys geometry entirely and any real graph
looks extraordinary against it. The correct family preserves the distance dependence. Roberts
and colleagues built exactly this for the connectome — "by applying a novel resampling method to
tractography data, we show that the brain's spatial embedding makes a major, but not definitive,
contribution to the topology of the human connectome", and they quantify "the extent to which
the segregation, integration, and modularity of the human brain are passively inherited from its
geometry" (doi:10.1016/j.neuroimage.2015.09.009, PMID 26364864) [VERIFIED-ABSTRACT]. Betzel and
Bassett studied the same dependence in weighted interareal connectomes
(doi:10.1073/pnas.1720186115) [VERIFIED-ABSTRACT], and Váša and Mišić's review is the catalogue
(doi:10.1038/s41583-022-00601-9) [VERIFIED-ABSTRACT]. Transferred to us: build surrogate contact
graphs that preserve degree _and_ the empirical edge-length distribution, rerun the propagator
on each, and report the observed score's z-score. That tests "is propagation on the real
topology different from propagation on a graph with the same geometry", which is the question
C6 actually poses.

**4. Contrasting two sources.** Propagate from the active site and from a decoy source, take the
difference. **No published instance for allosteric-site prediction was retrieved.** The
construction is cheap, but the algebra bounds what it can buy, and the bound is worth stating
before anyone runs it: a difference of scores from sources A and B cancels any additive term
that is a function of the residue's own position alone — global burial, distance to the chain
centroid, degree — but it does **not** cancel a term that is a function of ‖x_i − x_A‖, because
that term is not shared. So a source contrast is a good _globularity_ control and a poor
_distance_ control. Use it for the second confound, not the first. The nearest published
normalisations of this shape are communicability (doi:10.1103/physreve.77.036111)
[VERIFIED-ABSTRACT] and the search-information and path-transitivity measures of Goñi and
colleagues, which normalise a propagation quantity against a shortest-path reference
(doi:10.1073/pnas.1315529111) [VERIFIED-ABSTRACT].

### Table

| Citation                                                                      | Year | Method or finding                                                       | Domain                     | What it measured                                                                                                                                | Relevance to us                                                                               |
| ----------------------------------------------------------------------------- | ---- | ----------------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Amor, Schaub, Yaliraki & Barahona, doi:10.1038/ncomms12477, PMID 27561351** | 2016 | Quantile score by quantile regression on distance from the active site  | Allosteric-site prediction | Propensity "relative to other bonds … at a similar distance from the active site"; site detected in 19/20 test proteins by at least one measure | **The one allosteric method that conditions on distance by construction. Copy its estimator** |
| Lieberman-Aiden et al., doi:10.1126/science.1181369                           | 2009 | Observed/expected normalisation                                         | Hi-C genomics              | Contact frequency against a distance-dependent expectation                                                                                      | The simplest form of the same idea, in a field with an identical pathology                    |
| Ay, Bailey & Noble (Fit-Hi-C), doi:10.1101/gr.160374.113                      | 2014 | Spline fit of the distance-dependent background, per-pair p-values, FDR | Hi-C genomics              | Statistical confidence for each contact against its distance-matched expectation                                                                | **The mature version: per-element significance, not just a corrected ranking**                |
| Kaul, Bhattacharyya & Ay (FitHiC2), doi:10.1038/s41596-019-0273-0             | 2020 | Protocol and implementation                                             | Hi-C genomics              | Same, as a documented protocol                                                                                                                  | The code to read when implementing step 3 of the protocol below                               |
| Maslov & Sneppen, doi:10.1126/science.1065103                                 | 2002 | Degree-preserving edge switching                                        | Network biology            | Link suppression between hubs relative to the rewired null                                                                                      | The standard null — and the **wrong** one for a spatially embedded graph                      |
| Milo et al., doi:10.1126/science.298.5594.824                                 | 2002 | Motif z-score against randomised networks                               | Network science            | Subgraph counts vs a degree-preserving null                                                                                                     | Same caution                                                                                  |
| Roberts et al., doi:10.1016/j.neuroimage.2015.09.009, PMID 26364864           | 2016 | Geometry-preserving resampling of a spatially embedded network          | Network neuroscience       | How much of connectome topology is "passively inherited from its geometry"                                                                      | **The template for a geometry-preserving surrogate graph**                                    |
| Betzel & Bassett, doi:10.1073/pnas.1720186115                                 | 2018 | Distance-dependent weights in interareal connectomes                    | Network neuroscience       | Weight–distance coupling and its topological consequences                                                                                       | Establishes that distance-dependence is a first-class nuisance, not an afterthought           |
| Váša & Mišić, doi:10.1038/s41583-022-00601-9                                  | 2022 | Review of null models                                                   | Network neuroscience       | Rewiring, geometric and spatial nulls side by side                                                                                              | The orientation document for choosing between them                                            |
| Estrada & Hatano, doi:10.1103/physreve.77.036111                              | 2008 | Communicability                                                         | Network science            | Weighted walk sums between node pairs                                                                                                           | A ratio-style propagation measure with a defined normalisation                                |
| Goñi et al., doi:10.1073/pnas.1315529111                                      | 2013 | Search information, path transitivity                                   | Network neuroscience       | Propagation normalised against a shortest-path reference                                                                                        | The published example of "divide by a reference with the same geometry"                       |

---

## Q5 — What the allosteric field itself does about it

### Synthesis

**Plainly: it does almost nothing, and that is a finding.**

Across the predictors the brief names, plus three the search surfaced, **no evaluation protocol
was retrieved that runs a distance-to-active-site-only control.** The dominant endpoint is a
top-_N_ pocket hit rate — "is the true allosteric pocket among the top 3 pockets my method
ranks?" — with the negative class being the _other pockets of the same protein_. That endpoint
has three properties that make the confound invisible. It is pocket-level, so it never sees the
per-residue distance gradient. It has no null model at all, only a hit rate. And because the
candidate set is the same protein's own pockets, the distance spread within the candidate set is
narrow, which suppresses the confound without controlling it.

The concrete evidence, predictor by predictor:

- **PARS** (Panjkovich & Daura, doi:10.1186/1471-2105-13-273, doi:10.1093/bioinformatics/btu002)
  [VERIFIED-ABSTRACT] ranks pockets by flexibility change and structural conservation. No
  distance control in the retrieved abstracts.
- **Allosite** (Huang et al., doi:10.1093/bioinformatics/btt399) [VERIFIED-ABSTRACT] is an SVM on
  pocket features. No distance control retrieved.
- **PASSer** reports "84.9% of allosteric pockets in the testing proteins appeared in the top 3
  positions" (doi:10.1088/2632-2153/abe6d6) and PASSer2.0 "89.2% of allosteric pockets appeared
  among the top 3 positions" (doi:10.26434/chemrxiv-2021-q4319), with the server paper at
  doi:10.1093/nar/gkad303 [VERIFIED-ABSTRACT]. Top-3 pocket rate; no null; no distance control.
- **Ohm** (Wang et al., doi:10.1038/s41467-020-17618-2) [VERIFIED-ABSTRACT] validates against NMR
  studies. No distance control retrieved.
- **STRESS** (Clarke et al., doi:10.1016/j.str.2016.03.008) [VERIFIED-ABSTRACT] validates by
  inter- and intra-species conservation — i.e. by a second correlated descriptor, not by a
  geometric null.
- **AlloReverse** (Zha et al., doi:10.1093/nar/gkad279) [VERIFIED-ABSTRACT] "integrates protein
  dynamics and machine learning". No distance control retrieved.
- **ASBench** (Huang et al., doi:10.1093/bioinformatics/btv169) [VERIFIED-ABSTRACT] supplies "a
  'Core set' with 235 unique allosteric sites and a 'Core-Diversity set' with 147 structurally
  diverse allosteric sites". It is a dataset. It prescribes no null model and no control.
- **ASD** (Huang et al., doi:10.1093/nar/gkq1022) [VERIFIED-ABSTRACT] is the underlying database.

**The single exception, and it is a partial one.** Bond-to-bond propensity conditions on distance
inside the _score_ (Q4). But its _evaluation_ does not: Wu, Strömich and Yaliraki extended it to
432 structures of 146 proteins from ASBench and CASBench and report "the allosteric site is
recovered for 95/113 proteins (99/118 structures) from ASBench and 32/33 proteins (304/314
structures) from CASBench, with the only _a priori_ knowledge being the orthosteric site
residues" (doi:10.1101/2021.08.16.456251) [VERIFIED-ABSTRACT]. No distance-matched null, no
random-site control, no decoy comparison appears in the abstract. The conditioning lives in the
estimator and not in the test — which means the reported hit rates still carry whatever residual
geometry the quantile regression did not remove.

**Where the field's self-criticism has gone instead.** Three recent reappraisals all attack
_leakage_, not _confounding_: AlloBench found all seven benchmarked tools below 60 % accuracy on
a common set (doi:10.1021/acsomega.5c01263); Ai and colleagues found PASSer and APOP degrading
from holo to apo input (doi:10.1007/s10822-026-00831-4); Pryakhin and colleagues found fpocket-
on-unstripped-holo inflating estimates (doi:10.64898/2026.05.22.727284). All three are correct
and none of them measures a geometric baseline.

**Consequence for us.** Reporting a distance-conditioned number, with the `−distance` control's
own value beside it in the same table, is a methodological contribution independent of whether
our method wins. It is also, per `00-conventions.md` §2, a claim that must be phrased as "not
retrieved by the recorded search" rather than "nobody has done this" (ADR 0019).

### Table

| Citation                                                            | Year | Method or finding                                        | Domain                     | What it measured                                                                               | Relevance to us                                                                                     |
| ------------------------------------------------------------------- | ---- | -------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Panjkovich & Daura (PARS), doi:10.1186/1471-2105-13-273             | 2012 | Flexibility change on pocket binding                     | Allosteric-site prediction | 65 % PPV; flexibility change in 70 % of cases                                                  | No distance control retrieved; the 70 % is an apo-vs-holo statistic, inadmissible as input under C1 |
| Panjkovich & Daura (PARS server), doi:10.1093/bioinformatics/btu002 | 2014 | Web server                                               | Allosteric-site prediction | Pockets ranked by dynamics + conservation                                                      | Same                                                                                                |
| Huang et al. (Allosite), doi:10.1093/bioinformatics/btt399          | 2013 | SVM on pocket descriptors                                | Allosteric-site prediction | Pocket classification                                                                          | No distance control retrieved                                                                       |
| Tian et al. (PASSer), doi:10.1088/2632-2153/abe6d6                  | 2021 | XGBoost + GCN ensemble                                   | Allosteric-site prediction | 84.9 % top-3 pockets                                                                           | Endpoint is pocket-level; negatives are the same protein's other pockets; no null                   |
| Xiao et al. (PASSer2.0), doi:10.26434/chemrxiv-2021-q4319           | 2021 | AutoML                                                   | Allosteric-site prediction | 89.2 % top-3 pockets                                                                           | Same                                                                                                |
| Tian et al. (PASSer server), doi:10.1093/nar/gkad303                | 2023 | Three trained models, web server                         | Allosteric-site prediction | Deployment statistics                                                                          | Same                                                                                                |
| Wang et al. (Ohm), doi:10.1038/s41467-020-17618-2                   | 2020 | Network allosteric-coupling mapping from structure alone | Allosteric pathways        | Validated against NMR                                                                          | Structure-only and C1/C2-compatible in shape; no geometric null                                     |
| Clarke et al. (STRESS), doi:10.1016/j.str.2016.03.008               | 2016 | Dynamics-based hotspot identification                    | Allosteric hotspots        | Inter/intra-species conservation                                                               | Validation by a correlated descriptor, not by a null                                                |
| Zha et al. (AlloReverse), doi:10.1093/nar/gkad279                   | 2023 | Dynamics + ML, hierarchical regulation                   | Allosteric regulation      | Residues, sites, pathways                                                                      | No distance control retrieved                                                                       |
| Huang et al. (ASBench), doi:10.1093/bioinformatics/btv169           | 2015 | Benchmark sets                                           | Allosteric discovery       | Core set 235 sites; Core-Diversity 147 sites                                                   | A dataset; prescribes no null                                                                       |
| Huang et al. (ASD), doi:10.1093/nar/gkq1022                         | 2010 | Allosteric database                                      | Allostery                  | Proteins and modulators                                                                        | The label source everything else inherits                                                           |
| Wu, Strömich & Yaliraki, doi:10.1101/2021.08.16.456251              | 2021 | Bond-to-bond propensity at scale                         | Allosteric-site prediction | 95/113 (ASBench) and 32/33 (CASBench) proteins recovered from orthosteric-site knowledge alone | **The closest match to our task setting anywhere — and still no distance-matched null**             |
| Maity et al. (AlloBench), doi:10.1021/acsomega.5c01263              | 2025 | Seven tools, one test set                                | Allosteric-site prediction | All below 60 % accuracy                                                                        | Leakage-aware, not confound-aware                                                                   |
| Ai et al. (CAPASP), doi:10.1007/s10822-026-00831-4                  | 2026 | Five tools, holo vs apo subsets                          | Allosteric-site prediction | PASSer and APOP better on holo than apo                                                        | Leakage-aware, not confound-aware                                                                   |
| Pryakhin et al., doi:10.64898/2026.05.22.727284                     | 2026 | Benchmark-bias audit + AlloDyn                           | Allosteric-site prediction | fpocket-on-holo leakage inflates estimates                                                     | Leakage-aware, not confound-aware                                                                   |

---

## Q6 — How to report honestly

### Synthesis

**Report both numbers and the control's number, always, in the same table.** The conditioned
metric is only trustworthy if the control collapses under it. That is the negative-control logic
of Lipsitch, Tchetgen Tchetgen and Cohen (doi:10.1097/ede.0b013e3181d61eeb) [VERIFIED-ABSTRACT]:
a control that _must_ be null under a correct analysis, run through the identical pipeline. Our
repository already produces the worked example — `ctrl_closeness` sits at 0.494 under 2 Å
stratification and climbs monotonically to 0.573 as the window opens
(`09-data-analysis.md` §2.3). Print that row beside every method row.

**Do not test the difference in AUC between nested models. This is the single most common error
in this area and it has four independent sources saying so.**

- Demler, Pencina and D'Agostino, "Misuse of DeLong test to compare AUCs for nested models"
  (doi:10.1002/sim.5328) [VERIFIED-ABSTRACT].
- Seshan, Gönen and Begg: the "test of the two ROC areas often produces a non-significant result
  when a corresponding Wald test from the underlying regression model is significant"
  (doi:10.1002/sim.5648) [VERIFIED-ABSTRACT].
- Begg, Cronin and Vickers: "use of risk predictors from nested models as data in subsequent
  tests comparing areas under the ROC curves of the models leads to grossly invalid inferences"
  (doi:10.1177/1740774513496490) [VERIFIED-ABSTRACT].
- Pepe, Kerr, Longton and Wang: "null hypotheses concerning no improvement in performance are
  equivalent to the simple null hypothesis that Y is not a risk factor when controlling for X",
  and they recommend estimating performance rather than testing for improvement
  (doi:10.1002/sim.5727) [VERIFIED-ABSTRACT].

The constructive version is Vickers, Cronin and Begg's: **one statistical test is sufficient**
(doi:10.1186/1471-2288-11-13) [VERIFIED-ABSTRACT]. Fit the baseline model with distance in it,
add the method's score, and test the added coefficient. That is the incremental-value test and
it is the answer to "does our method beat the distance baseline on the same arms".

**DeLong's test remains correct for the non-nested comparison** — our score against the
`−distance` control as two separate rankers of the same residues (doi:10.2307/2531595)
[VERIFIED-ABSTRACT], with Hanley and McNeil's correlated-ROC treatment as background
(doi:10.1148/radiology.148.3.6878708) [VERIFIED-ABSTRACT] and `pROC::roc.test(method = "delong")`
as the reference implementation (doi:10.1186/1471-2105-12-77) [VERIFIED-ABSTRACT]. But there is a
second problem DeLong does not solve: DeLong's variance assumes independent observations, and
residues within a protein are spatially autocorrelated. Its p-value will be anti-conservative
here. The repository's existing choice — a paired bootstrap that resamples **arms**, not residues
— is the right variance estimator, and `09-data-analysis.md` §6 already runs it at 20 000
resamples.

**Effect sizes to report, in this order.** (i) The conditioned AUC, with a paired-bootstrap CI
over arms. (ii) Δ = method − control, with the same CI. (iii) The share of the control's
remaining headroom the method closes, `(best − control) / (1 − control)`, which is the quantity
a reader can interpret without knowing our baseline; `09-data-analysis.md` §6 already reports it
(0.3 % on the confounded metric, 19.0 % on the stratified one). (iv) The added coefficient β and
its LRT p-value from the nested-model test. (v) The top-5 hit rate, because that is the
deliverable, alongside the AUC.

**State the sensitivity band before stating the number.** Our frozen protocol needs an achieved
AUC of 0.76 to 0.96 for 80 % power, median 0.879 across 60 arm × λ × Holm-level cells
(`09-data-analysis.md` §8). A non-rejection at that sensitivity is not evidence of no effect, and
the report must say so before it reports a p-value, not after. TRIPOD is the reporting skeleton
for a prediction model if one is needed (doi:10.1186/s12916-014-0241-z) [VERIFIED-ABSTRACT].

### Table

| Citation                                                              | Year | Method or finding                                | Domain               | What it measured                                                       | Relevance to us                                                             |
| --------------------------------------------------------------------- | ---- | ------------------------------------------------ | -------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| DeLong, DeLong & Clarke-Pearson, doi:10.2307/2531595                  | 1988 | Nonparametric comparison of correlated ROC areas | Biostatistics        | Covariance of AUCs on the same cases                                   | Correct for the **non-nested** score-vs-control comparison                  |
| Hanley & McNeil, doi:10.1148/radiology.148.3.6878708                  | 1983 | Comparing ROC areas from the same cases          | Radiology            | Correlated-ROC variance                                                | Background for the same comparison                                          |
| **Demler, Pencina & D'Agostino, doi:10.1002/sim.5328**                | 2012 | DeLong invalid for nested models                 | Biostatistics        | Type-I behaviour under nesting                                         | **Forbids the obvious test**                                                |
| Seshan, Gönen & Begg, doi:10.1002/sim.5648                            | 2013 | ROC comparison from regression models            | Biostatistics        | ΔAUC non-significant while the Wald test is significant                | Explains why ΔAUC under-detects real incremental value                      |
| Begg, Cronin & Vickers, doi:10.1177/1740774513496490                  | 2013 | Incremental predictive accuracy                  | Clinical trials      | "Grossly invalid inferences" from nested ROC comparisons               | Same, stated at full strength                                               |
| **Vickers, Cronin & Begg, doi:10.1186/1471-2288-11-13**               | 2011 | One test is sufficient                           | Biostatistics        | Test the new marker's coefficient in the model containing the baseline | **The test we should run**                                                  |
| Pepe, Kerr, Longton & Wang, doi:10.1002/sim.5727                      | 2013 | Testing for improvement                          | Biostatistics        | Improvement nulls reduce to "Y is not a risk factor given X"           | The theory behind the previous row; also argues for estimation over testing |
| Robin et al. (pROC), doi:10.1186/1471-2105-12-77                      | 2011 | ROC software                                     | Software             | `roc.test`, DeLong and bootstrap variants                              | Names the function                                                          |
| Lipsitch, Tchetgen Tchetgen & Cohen, doi:10.1097/ede.0b013e3181d61eeb | 2010 | Negative controls                                | Epidemiology         | Controls that must be null under a correct analysis                    | The formal justification for "`−distance` must collapse to 0.5"             |
| Collins et al. (TRIPOD), doi:10.1186/s12916-014-0241-z                | 2015 | Reporting standard                               | Prediction modelling | Checklist for model development and validation                         | The report skeleton if a fitted model reaches `docs/report/`                |
| Kapoor & Narayanan, doi:10.1016/j.patter.2023.100804                  | 2023 | Leakage taxonomy                                 | ML-based science     | Leakage types across fields and their effect on reported performance   | Adjacent to but distinct from confounding — cite both, do not conflate them |

---

## Ranked candidate signals

Ranked by expected value to this project: measured distance-orthogonality first, then published
allosteric evidence, then cost. "Expected ρ with distance" is a measurement where one exists in
`09-data-analysis.md` §2.1 and an expectation flagged `[UNVERIFIED]` where it does not.

| Descriptor                                                                 | Computable from apo alone?                                           | Tool / package                                                                                                          | Published evidence for allostery                                                                                                                                                              | Expected correlation with distance                                               | Implementation cost                                                           |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **1. ENM spectral readouts (ALPS-family eigenvalue shift, ESSA, APOP)**    | Yes — coordinates only                                               | ProDy (ESSA); APOP web server and code (doi:10.1093/bioinformatics/btad275); already in `allo.classical`                | APOP 92/104 top-3 (doi:10.1093/bioinformatics/btad275), cut to 15 % under AlloBench's leakage control                                                                                         | **Measured: ρ = −0.045 (ALPS), −0.112 (apop)**                                   | **Zero — already implemented**                                                |
| **2. Local energetic frustration**                                         | Yes — coordinates + sequence                                         | Frustratometer 2 (doi:10.1093/nar/gkw304); FrustratometeR (doi:10.1093/bioinformatics/btab176)                          | Ferreiro 2011: frustrated patches at reconfiguring regions/hinges (doi:10.1073/pnas.1018980108); Riedlová: allosteric pockets in neutrally frustrated zones                                   | Low `[UNVERIFIED]`; **burial-correlated — must be reported against RSA**         | Medium. **Blocked on a C6 ADR** — it uses an energy function                  |
| **3. Cavity geometry: volume, buriedness, enclosure, druggability**        | Yes — coordinates only                                               | pyKVFinder (doi:10.1186/s12859-021-04519-4); fpocket (doi:10.1186/1471-2105-10-168); CASTp 3.0 (doi:10.1093/nar/gky473) | `cavity_volume` already rejects the null on all three confirmatory arms (`00-conventions.md` §6)                                                                                              | Low by construction — the pocket detector never sees the active site             | Low. pyKVFinder is offline-callable                                           |
| **4. Conditional-quantile normalisation of an existing propagation score** | Yes                                                                  | `statsmodels.regression.quantile_regression.QuantReg`; the estimator of doi:10.1038/ncomms12477                         | The one distance-conditioned allosteric method in the literature                                                                                                                              | **Measured: reduces ρ from −0.927 to −0.016 on `btb`**                           | **Low — it is a post-processing step, not a new descriptor**                  |
| **5. Per-residue local contact order**                                     | Yes — from the graph we build                                        | `allo.classical.baselines` (already added by `24`)                                                                      | None retrieved; Plaxco's result is chain-level (doi:10.1006/jmbi.1998.1645)                                                                                                                   | Orthogonal to burial by construction `[UNVERIFIED]` for distance                 | **Zero — already implemented**                                                |
| **6. Mode participation ÷ degree (and other local-over-global ratios)**    | Yes — from eigenvectors we already compute                           | Ours; no package                                                                                                        | **None retrieved — our construction**                                                                                                                                                         | Designed to be low; unmeasured `[UNVERIFIED]`                                    | **Very low — one line given the eigendecomposition**                          |
| **7. Conservation, via pLM entropy or an MSA**                             | Sequence only; pLM route is offline after a one-time weight download | ESM-2 (doi:10.1126/science.ade2574); ConSurf for the MSA route                                                          | **Negative**: conservation "significantly more important for active site than for allosteric site" (doi:10.1002/prot.25749); allosteric sites weakly conserved (doi:10.1021/acs.jctc.6c00427) | Zero by construction; **burial-correlated**                                      | Medium. Already scoped as item 2 of `24` §7                                   |
| **8. Hinge and domain-boundary descriptors**                               | Yes — coordinates only                                               | PACKMAN (doi:10.1016/j.jmb.2019.11.018), toolbox doi:10.1093/bioadv/vbac007                                             | Mechanistic only; **no benchmark effect size retrieved**. Counter-evidence: catalytic sites at hinge minima in > 70 % of 98 enzymes (`25`)                                                    | Low `[UNVERIFIED]`                                                               | Low–medium                                                                    |
| **9. Non-contacting DCA couplings**                                        | Sequence only, but needs a deep MSA                                  | plmDCA (doi:10.1103/physreve.87.012707); GREMLIN (doi:10.1073/pnas.1314045110)                                          | **None retrieved for the non-contacting residual** — the published skill is contact recovery                                                                                                  | Zero by construction, but the _top_ couplings **are** the contact map            | **High** — MSA construction, depth check per target, and a network dependency |
| **10. Rigid-cluster membership (pebble game)**                             | **No** — needs hydrogens and an H-bond cut-off                       | FIRST (doi:10.1002/prot.1081); rigidity-transmission allostery (doi:10.1007/978-1-0716-1154-8_5)                        | Case studies only; no dataset-level effect size retrieved                                                                                                                                     | Topological, so low `[UNVERIFIED]`                                               | High. Same C6 ADR as frustration; `24` §7 already deferred it                 |
| **11. SCA sector membership**                                              | Sequence only; needs a curated family MSA of 10⁴–10⁵ sequences       | pySCA                                                                                                                   | **Undercut**: conservation reproduces sector predictions, PDZ p = 0.9, DHFR p = 0.2 (doi:10.1371/journal.pcbi.1004091)                                                                        | Zero by construction                                                             | High, for a signal the evidence says is conservation in disguise              |
| **12. pLM attention maps / embeddings as a site predictor**                | Sequence only                                                        | ESM-2, ProtT5, Ankh                                                                                                     | **Negative**: Type IV distal allosteric AUROC 0.676 vs Type I 0.968; AUPR 0.06 on allosteric                                                                                                  | **Not orthogonal** — attention recovers contacts (doi:10.1101/2020.12.15.422761) | Medium, for a signal measured near-random on our class                        |
| **13. Predicted ΔΔG of mutation**                                          | Needs a force field                                                  | FoldX, Rosetta, ThermoMPNN                                                                                              | None retrieved for allosteric-site localisation                                                                                                                                               | **Partly a burial proxy** — depth predicts ΔΔG well (`24` §1.2)                  | High cost, C6 problem, low prior                                              |
| **14. Packing descriptors: depth, DPX, CX, OSP, Voronoi volume, WCN**      | Yes                                                                  | Several                                                                                                                 | **Closed by `24` §7 item 1: one axis, already in the null**                                                                                                                                   | High collinearity with burial, not with distance                                 | **Do not implement**                                                          |

---

## Recommended protocol

A nine-step procedure for demonstrating that a method adds signal beyond distance. It is a
**diagnostic layer reported beside** the frozen endpoint, not a replacement for it: the
evaluation protocol is frozen and every headline number still goes through
`allo.scoring.score_arm`.

**Step 0 — define the confound once, in code.** `d_i` = minimum Euclidean distance from residue
_i_ to any active-site residue, using the same coordinate convention the graph uses. Compute it
in one place and reuse it, so the stratified metric, the detrend and the null all condition on
the identical vector.

**Step 1 — measure the confound per arm; never assume its size or its sign.**
Report three estimators, because they can disagree and the disagreement is informative:
(i) per-residue Spearman ρ(score, −d) inside the candidate pool, and ρ²;
(ii) between-arm R² from regressing the method's per-arm AUC on the `−d` control's per-arm AUC;
(iii) the plain-minus-stratified drop, expressed as the fraction of the margin over 0.5 that is
lost. `09-data-analysis.md` §2 is the worked template for all three.
The sign must be measured per arm: it inverts between label conventions (§2.4 there).

**Step 2 — run the negative control through the identical pipeline.** Score `−d` itself. Under
the conditioned metric it must sit at 0.5 within its own CI. If it does not, stop: nothing
downstream is interpretable (Lipsitch 2010). Choose the stratification tolerance by the sweep
that makes this true with the largest surviving matched-pair count, exactly as
`09-data-analysis.md` §2.3 chose 2 Å.

**Step 3 — condition three ways and require agreement.**
(a) _Distance-matched stratified AUC_ at the tolerance from Step 2; report the matched-pair
count beside the estimate.
(b) _Conditional-quantile normalisation_, following doi:10.1038/ncomms12477: quantile-regress
`log(score)` on `d` at a grid of quantile levels, map each residue to its conditional quantile
given `d`, and rank on that. Robust to the heteroscedasticity a decaying score always has.
(c) _Observed-over-expected with per-residue p-values_, following Fit-Hi-C
(doi:10.1101/gr.160374.113): fit `E[score | d]` with a monotone spline or isotonic regression,
model the residual dispersion as a function of `d`, assign each residue a one-sided p-value
against its distance-matched expectation, then Benjamini-Hochberg within the arm. This is what
turns a corrected ranking into a hit list with stated confidence.
A candidate must survive all three. Divergence between (a) and (b)/(c) indicates
misspecification of the trend, not signal.

**Step 4 — the incremental-value test. This is the direct answer to "does our method beat the
distance baseline on the same arms?"**
Per arm, over the candidate pool, fit two nested logistic models:

- `M0: logit P(y_i = 1) = β₀ + s(d_i)`
- `M1: logit P(y_i = 1) = β₀ + s(d_i) + β₂ · z_i`

where `s(·)` is a natural cubic spline with 4 degrees of freedom, knots at the pool's `d`
quantiles, and `z_i` is the method's within-arm rank percentile. Test `H₀: β₂ = 0` by a
**likelihood-ratio test on 1 df**. Report `β₂`, its confidence interval, and the LRT p-value.
Two implementation details are load-bearing.
_The spline is not optional._ A linear-in-`d` baseline under-fits, and the test then credits the
method for the baseline's misspecification.
_The standard errors are wrong by default._ Residues within an arm are spatially autocorrelated,
so use a cluster-robust sandwich by arm for a pooled fit, or take the p-value for `β₂` from the
Step-5 permutation null instead of from the asymptotic distribution.
Do **not** report a DeLong test of AUC(M1) − AUC(M0): the models are nested and the test is
invalid (doi:10.1002/sim.5328; doi:10.1177/1740774513496490). DeLong is appropriate only for the
non-nested comparison of the method's score against the `−d` control as two separate rankers.

**Step 5 — the null must preserve spatial autocorrelation, and it must be applied to the
detrended field.**
Naive residue permutation is anti-conservative (doi:10.1016/j.neuroimage.2021.118052; our own
type-I rates of 0.096–0.323 at nominal 0.05). Use, in this order:
(a) _Variogram-matched surrogates_ of the **Step-3 residual** field (doi:10.1016/j.neuroimage.2020.117038;
`brainsmash.mapgen.sampled.Sampled` or `neuromaps.nulls.burt2020`), with the Cα–Cα distance
matrix as the only geometric input. Applying this to the _raw_ field would be a mistake: the
variogram controls smoothness, not a radial trend about a fixed source, and the observed field
is non-stationary in exactly the way the variogram does not see.
(b) _Moran spectral randomisation_ (doi:10.1111/2041-210x.12407; `adespatial::msr`,
`brainspace.null_models.MoranRandomization`, `neuromaps.nulls.moran`) with the contact-graph
adjacency as the weights matrix, as an independent check with a different preservation guarantee.
(c) _Geometry-preserving surrogate graphs_ for the graph-side question: rewire preserving degree
**and** the empirical edge-length distribution, rerun the propagator, z-score the observed score
(doi:10.1016/j.neuroimage.2015.09.009; doi:10.1038/s41583-022-00601-9). A plain configuration
model (doi:10.1126/science.1065103) destroys geometry and will over-reject.
(d) _Do not use the spin test._ It requires a spherical parameterisation of the domain
(doi:10.1016/j.neuroimage.2018.05.070) and a protein has none.

**Step 6 — fix the order of operations.**
Rank-percentile first, then any spatial smoothing, then the detrend. Never detrend before
smoothing: pocket-smoothing averages over a geometric neighbourhood whose members share the
residue's distance from the source, so it re-imports the trend the detrend removed. And because
residualisation is not monotone, `rank → residualise` and `residualise → rank` give different
residuals; the conditioned metric is a rank statistic, so report the first.

**Step 7 — one table, five columns, every method row and the control row.**
`raw AUC | conditioned AUC | β₂ with LRT p | Δ(method − control) with 95 % paired-bootstrap CI |
share of the control's headroom closed`. The bootstrap resamples **arms**, not residues.

**Step 8 — fix the multiplicity family before slicing.** Declare the family, then Holm or BH
across it, and print the uncorrected p beside the corrected one.
`../exploration/results/41-selection-and-power.md` is the reference for what a screen of our size
produces by chance.

**Step 9 — state the sensitivity band before the number.** Our protocol needs an achieved AUC of
0.76–0.96 for 80 % power. Write that sentence first, then the result. A non-rejection at that
sensitivity is a bound on our resolution, not evidence of no effect, and the report must not let
a reader confuse the two.

---

## What the literature does NOT support

Each item is something a reader might reasonably assume, and each is contradicted or unsupported
by what was retrieved.

1. **That SCA sectors are a demonstrated allosteric-site locator beyond plain conservation.** On
   the systems where SCA has been experimentally tested — almost all single-sector — conservation
   reproduces the sector's functional predictions with no statistical difference: PDZ p = 0.9,
   DHFR p = 0.2 (doi:10.1371/journal.pcbi.1004091). The strongest surviving claim, Reynolds 2011,
   is one enzyme with no extractable effect size.
2. **That conservation is a strong allosteric-site signal.** It is a strong _catalytic_-site
   signal. AR-Pred measures the asymmetry directly (doi:10.1002/prot.25749). Since our benchmark
   hands the method the active site, a conservation column that lights up there is a working
   column, not a useful one.
3. **That protein language models locate distal allosteric sites.** Type IV distal allosteric
   AUROC 0.676 against Type I 0.968 (doi:10.1021/acs.jctc.6c00427); AUPR 0.06 on allosteric
   against 0.64–0.76 on orthosteric in the same proteins (`00-conventions.md` §5). And pLM
   attention maps recover contacts (doi:10.1101/2020.12.15.422761), so they are not
   distance-orthogonal even in principle.
4. **That any published allosteric-site predictor has been shown to beat a distance-only
   control.** No such control was retrieved for PARS, Allosite, PASSer, PASSer2.0, Ohm, STRESS,
   AlloReverse, ASBench, ASD, DeepAllo, or bond-to-bond propensity's evaluation. Recorded as not
   retrieved by the recorded search (ADR 0019), not as absent.
5. **That a variogram-matched surrogate controls for a radial trend.** It controls for
   smoothness. The variogram is a function of pairwise distance, not of distance from a source,
   and it assumes stationarity that a source-decaying field violates. Composing it with a detrend
   is required; substituting it for one is an error.
6. **That naive residue permutation gives valid p-values on a protein.** Measured type-I rates of
   0.096–0.323 at nominal 0.05 on our own arms; the same failure is measured across ten null
   frameworks for brain maps (doi:10.1016/j.neuroimage.2021.118052).
7. **That DeLong's test can compare a method against a nested baseline.** Four independent
   sources say it cannot (doi:10.1002/sim.5328, doi:10.1002/sim.5648,
   doi:10.1177/1740774513496490, doi:10.1002/sim.5727).
8. **That the spin test transfers to proteins.** It needs a spherical parameterisation. Radially
   projecting residues onto an enclosing sphere destroys burial, which is our second confound.
9. **That more packing descriptors would help.** `24-residue-descriptors.md` §7 item 1 closed
   this: residue depth, DPX, CX, occluded surface, Voronoi volume and weighted contact number are
   one axis, already controlled, and adding them worsens multiplicity for no new information.
10. **That rigidity theory or frustration has a dataset-level allosteric ROC.** For rigidity,
    case studies only. For frustration, the only quantitative allosteric result retrieved is
    embedded inside a supervised pLM pipeline (doi:10.1021/acs.jctc.6c00427) and is not a
    frustration-alone effect size.
11. **That top-3-pocket hit rates are comparable to our endpoint.** PASSer's 84.9 %, PASSer2.0's
    89.2 %, DeepAllo's 90.5 % and APOP's 92/104 all use a pocket-level positive class with the
    same protein's other pockets as negatives. Our endpoint is per-residue against a matched-patch
    null. The numbers are not on the same scale and must never be quoted side by side
    (`00-conventions.md` §2, last bullet).
12. **That a "biggest pocket" baseline has been measured against allosteric sites.** fpocket's
    94 %/92 % top-3 is for the _ligand_ (orthosteric) pocket (doi:10.1186/1471-2105-10-168). No
    allosteric equivalent was retrieved.
13. **That contrasting two propagation sources removes the distance confound.** The algebra says
    a source difference cancels terms that depend on the residue's own position — burial,
    globularity, degree — but not a term in ‖x_i − x_A‖. It is a globularity control, not a
    distance control. No published instance for allostery was retrieved either way.

---

## What this changes for our pipeline

1. **Adopt the conditional-quantile detrend as the primary confound-removal form.**
   [`allo.classical.postprocess`, stage S6.] It is the allosteric field's own estimator
   (doi:10.1038/ncomms12477), it is robust to heteroscedasticity where a mean residual is not,
   and our own data shows it working on `btb` (ρ from −0.927 to −0.016). Keep the mean-residual
   form as a comparator, not as the headline.
2. **Add the Fit-Hi-C-style per-residue p-value against a distance-matched expectation.**
   [`allo.classical.postprocess`, feeding S7 site assembly.] This is what turns a ranking into a
   top-5 hit list with a stated confidence, which is the deliverable
   (`AGENTS.md`, deliverable 2).
3. **Add two spatial-autocorrelation-preserving nulls, applied to the detrended field.**
   [Diagnostic layer beside `allo.scoring`, never inside it — the evaluation protocol is frozen.]
   Variogram-matched surrogates and Moran spectral randomisation both need only objects we
   already have. Do not implement the spin test.
4. **Replace any ΔAUC-based "our method beats the baseline" claim with the nested LRT of
   Step 4.** [Report layer.] Four sources forbid the ΔAUC version for nested models. The spline
   baseline is mandatory or the test credits us for the baseline's misspecification.
5. **Frustration is the one genuinely new descriptor worth an ADR.** [`scoring/properties.py`
   or a new `allo.classical` scorer.] It is non-geometric, single-structure, MD-free, and it has
   an allostery-specific published claim (doi:10.1073/pnas.1018980108). It also needs an energy
   function, which is the same C6 question `24` §7 item 7 raised for Poisson-Boltzmann. Write the
   ADR once and it settles both.
6. **Do not spend effort on SCA sectors or on DCA's top couplings.** [No stage.] Sectors are
   conservation in disguise on every system where they were tested; DCA's top couplings are the
   contact map we already have. The only non-circular DCA construction is the non-contacting
   residual, and that is a high-cost, zero-prior experiment.
7. **Report the `−distance` control row in every results table, under both metrics.** [Report
   layer.] It is the negative control that certifies the conditioning, and printing it is also
   the methodological contribution: the search found no allosteric-site predictor that does.
8. **Order of operations is a correctness requirement, not a style choice.** [Stage S6.]
   Rank-percentile → spatial smoothing → detrend. A detrend before smoothing re-imports the
   trend.

---

## Method

**Databases and routes.** Crossref REST API `api.crossref.org/works` (bibliographic query with
`select=DOI,title,author,issued,container-title,abstract`, and DOI-direct lookups); PubMed
E-utilities `esearch.fcgi` (including multi-DOI `[doi]` OR queries) and `efetch.fcgi` with
`rettype=abstract&retmode=text`; Semantic Scholar Graph API
`api.semanticscholar.org/graph/v1/paper/{DOI|PMID}?fields=title,abstract,year,venue,externalIds`;
arXiv abstract pages; bioRxiv article and full-text pages; publisher article pages for PLOS ONE
and PLOS Computational Biology; and two software documentation sites
(`brainsmash.readthedocs.io`, `netneurolab.github.io/neuromaps`).

**Route failure to record.** Europe PMC, listed as a working route in `00-conventions.md` §3,
returned `{"version":"6.9"}` with an empty result list on **all ten** attempts in this session:
`format=json` and XML, `+` and `%20` separators, `resultType` `core`, `lite` and `idlist`, with
and without field prefixes. The `+`-separator fix recorded by
`../exploration/lit/24-residue-descriptors.md` did not resolve it. Crossref and PubMed
E-utilities were used instead and both worked. Semantic Scholar returned HTTP 429 on two of five
calls, consistent with the rate limit already recorded.

**Queries run (approximately 60).**
_Q1:_ hidden bias DUD-E deep learning virtual screening; in need of bias control evaluating
chemical data machine learning; frustration to predict binding affinities protein-ligand deep
neural networks; most ligand-based classification benchmarks reward memorization; evaluation of
residue-residue contact prediction CASP10; assessment of ligand binding site predictions CASP10;
PoseBusters AI docking physically valid poses; CryptoSite expanding the druggable proteome;
PocketMiner cryptic pockets graph neural network; allosteric site prediction benchmark sequence
similarity leakage ACS Omega 2025; binding site prediction largest pocket trivial baseline
(web search); protein-protein interaction site prediction solvent accessibility baseline critical
assessment; leakage and the reproducibility crisis in machine-learning-based science; CAFA
challenge improved protein function prediction.
_Q2:_ on testing for spatial correspondence between maps of human brain structure and function;
generative modeling of brain maps with spatial autocorrelation; comparing spatial null models for
brain maps; null models in network neuroscience; generating spatially constrained null models
Moran spectral randomization; assessing the significance of the correlation between two spatially
autocorrelated processes; on the misuse of residuals in ecology; adjusting for covariate effects
on classification accuracy covariate-adjusted ROC; the central role of the propensity score;
spatial autocorrelation trouble or new paradigm; ppcor semi-partial correlation; neuromaps
structural and functional interpretation of brain maps; BrainSMASH approach documentation;
neuromaps API documentation.
_Q3:_ evolutionarily conserved pathways of energetic connectivity; protein sectors evolutionary
units of three-dimensional structure; hot spots for allosteric regulation on protein surfaces;
the spatial architecture of protein function and adaptation; protein sectors statistical coupling
analysis versus conservation; influence of conservation on calculations of amino acid covariance;
direct-coupling analysis of residue coevolution; improved contact prediction pseudolikelihoods
Potts; assessing the utility of coevolution-based contact predictions; evolutionary-scale
prediction of atomic-level protein structure; transformer protein language models are
unsupervised structure learners; fpocket open source platform ligand pocket detection;
understanding and predicting druggability; CASTp 3.0; pyKVFinder; protein flexibility predictions
using graph theory; rigidity transmission allostery Sljoka; PACKMAN hinge prediction alpha shape;
essential site scanning analysis; APOP allosteric pocket prediction (DOI-direct); localizing
frustration in native proteins; role of frustration in the energy landscapes of allosteric
proteins; local frustration around enzyme active sites; Protein Frustratometer 2; FrustratometeR;
AR-Pred (DOI-direct); Riedlová 2026 (DOI-direct); allosteric site prediction protein language
models orthosteric conditioning; DeepAllo (DOI-direct).
_Q4:_ prediction of allosteric sites and mediating interactions through bond-to-bond propensities
(Crossref, PubMed and bioRxiv full text); comprehensive mapping of long-range interactions
folding principles human genome (DOI-direct); statistical confidence estimation for Hi-C data;
the contribution of geometry to the human connectome; specificity and robustness of long-distance
connections; specificity and stability in topology of protein networks; network motifs simple
building blocks; communicability in complex networks; resting-brain functional connectivity
predicted by analytic measures of network communication; AlloSigMA; structure-based statistical
mechanical model allosteric communication.
_Q5:_ exploiting protein flexibility to predict the location of allosteric sites; Allosite;
PASSer; mapping allosteric communications within individual proteins; identifying allosteric
hotspots with dynamics; AlloReverse; ASBench; ASD; prediction of allosteric sites and signalling
insights from benchmarking datasets; allosteric site prediction evaluation distance to the active
site control baseline (web search).
_Q6:_ comparing the areas under two or more correlated ROC curves; misuse of DeLong test to
compare AUCs for nested models; one statistical test is sufficient for assessing new predictive
markers; comparing ROC curves derived from regression models; testing for improvement in
prediction model performance; a method of comparing areas under ROC curves derived from the same
cases; negative controls a tool for detecting confounding; pROC; TRIPOD statement.

**Counts.** Approximately 150 bibliographic records returned with usable metadata across the
queries; **62 screened in** and cited below with a DOI, PMID or preprint identifier. Screening
criterion: the record either (i) measures the size of a trivial or geometric baseline against a
published method, (ii) defines or evaluates a statistical procedure for conditioning on a
confound, (iii) defines a descriptor with a stated relationship to distance or burial, or (iv)
states an evaluation protocol for an allosteric-site predictor. Records reporting a single
protein's mechanism with no transferable estimator or descriptor were screened out.

**Verification depth.** 4 claims `[VERIFIED-FULLTEXT]`: Chen 2019 via the PLOS ONE article page
(the 0.98/0.98/R² = 0.98 figures); Teşileanu 2015 via the PLOS Computational Biology article page
(the PDZ and DHFR p-values); Amor 2016 via the bioRxiv full text (the quantile-score definition
and the 19/20 figure); the BrainSMASH algorithm via the package documentation. All remaining
literature claims are `[VERIFIED-ABSTRACT]` from an abstract or metadata record retrieved this
session. Claims sourced from sibling files in this repository are attributed to the file and
carry that file's own verification tag; they are not re-verified here. Repository-derived numbers
carry the file and section that computed them, per R3.

**Stopping rule.** Per question: stop when a new query returns only records already screened, or
returns records with no numeric effect size and no new estimator. Q1 stopped after the eleventh
query, Q2 after the fourteenth, Q3 after the twenty-ninth, Q4 after the eleventh, Q5 after the
tenth, Q6 after the ninth.

**What could not be reached.**

- **Europe PMC**, on every attempt. See the route-failure note above. This is a real limit: the
  full-text XML route that gave `24-residue-descriptors.md` eight full-text verifications was
  unavailable, so this file has four rather than a dozen.
- **A distance-only control in any published allosteric-site evaluation.** Ten queries across
  Q1 and Q5. Nothing. This is the largest gap in the file and it is also the finding.
- **A per-residue allosteric ROC for local frustration alone.** Four queries. The only
  quantitative allosteric result is inside a supervised pLM pipeline.
- **Roberts 2016's abstract text on distance-preserving surrogates** was retrieved (Semantic
  Scholar) but the paper's _method section_ was not, so the exact resampling procedure is
  described here at the level the abstract supports and would need one full-text pass before it
  is implemented.
- **The Burt 2020 abstract** could not be retrieved: Crossref carries no abstract for it, and
  Semantic Scholar returned 404 then 429. The algorithm is cited from the package documentation
  instead, which is a stronger source for implementation and a weaker one for the paper's claims.
- **ACS full texts** (`pubs.acs.org`) returned HTTP 403; **Nature** and **Springer** article pages
  returned 303 redirects to identity providers. PubMed `efetch` supplied those abstracts instead.
- **Riedlová 2026's numbers** are quoted at second hand from
  `../exploration/lit/24-residue-descriptors.md`, which verified them full-text on 2026-08-26.
  They are not independently re-verified here.

**Leakage guard.** No file under `docs/benchmark/` was opened. No real label residue, holo
accession, effector component ID or active-site definition appears in this document. Repository
files read: `CLAUDE.md`, `docs/FIELD.md`, `docs/method/README.md`,
`docs/method/review/00-conventions.md`, `docs/method/review/09-data-analysis.md`,
`docs/method/exploration/README.md`, `docs/method/exploration/lit/README.md`,
`docs/method/exploration/lit/24-residue-descriptors.md`.

---

## References

**How to read these entries.** Every DOI, PMID and preprint identifier below was resolved in
this session and is the authority for the entry. Journal names and years come from the resolved
record. **Volume, issue and page fields are bibliographic completion and were not separately
verified**; where one disagrees with the publisher's own record, the publisher wins and the DOI
still resolves to the right paper. Do not quote a page number from this list into
`docs/report/` without re-resolving it.

1. Chen L, Cruz A, Ramsey S, Dickson CJ, Duca JS, Hornak V, et al. Hidden bias in the DUD-E dataset leads to misleading performance of deep learning in structure-based virtual screening. PLoS One. 2019;14(8):e0220113. doi:10.1371/journal.pone.0220113
2. Volkov M, Turk J-A, Drizard N, Martin N, Hoffmann B, Gaston-Mathé Y, et al. On the frustration to predict binding affinities from protein–ligand structures with deep neural networks. J Med Chem. 2022;65(11):7946-58. doi:10.1021/acs.jmedchem.2c00487. PMID 35608179
3. Wallach I, Heifets A. Most ligand-based classification benchmarks reward memorization rather than generalization. J Chem Inf Model. 2018;58(5):916-32. doi:10.1021/acs.jcim.7b00403. PMID 29698607
4. Sieg J, Flachsenberg F, Rarey M. In need of bias control: evaluating chemical data for machine learning in structure-based virtual screening. J Chem Inf Model. 2019;59(3):947-61. doi:10.1021/acs.jcim.8b00712. PMID 30835112
5. Monastyrskyy B, D'Andrea D, Fidelis K, Tramontano A, Kryshtafovych A. Evaluation of residue–residue contact prediction in CASP10. Proteins. 2013;82(S2):138-53. doi:10.1002/prot.24340. PMID 23760879
6. Le Guilloux V, Schmidtke P, Tuffery P. Fpocket: an open source platform for ligand pocket detection. BMC Bioinformatics. 2009;10:168. doi:10.1186/1471-2105-10-168
7. Maity D, et al. AlloBench: a data set pipeline for the development and benchmarking of allosteric site prediction tools. ACS Omega. 2025;10(17):17973-85. doi:10.1021/acsomega.5c01263. PMID 40352555
8. Ai Y, Li H, Huang X, Liu S. A systematic evaluation of protein allosteric site prediction tools with independent datasets. J Comput Aided Mol Des. 2026;40. doi:10.1007/s10822-026-00831-4. PMID 42126486
9. Pryakhin V, Smaïl-Tabbone M, Karami Y. Benchmark bias and conformational dynamics in allosteric site prediction. bioRxiv. 2026. doi:10.64898/2026.05.22.727284
10. García-Berthou E. On the misuse of residuals in ecology: testing regression residuals vs. the analysis of covariance. J Anim Ecol. 2001;70(4):708-11. doi:10.1046/j.1365-2656.2001.00524.x
11. Freckleton RP. On the misuse of residuals in ecology: regression of residuals vs. multiple regression. J Anim Ecol. 2002;71(3):542-5. doi:10.1046/j.1365-2656.2002.00618.x
12. Kim S. ppcor: an R package for a fast calculation to semi-partial correlation coefficients. Commun Stat Appl Methods. 2015;22(6):665-74. doi:10.5351/csam.2015.22.6.665
13. Janes H, Pepe MS. Adjusting for covariate effects on classification accuracy using the covariate-adjusted receiver operating characteristic curve. Biometrika. 2009;96(2):371-82. doi:10.1093/biomet/asp002
14. Rosenbaum PR, Rubin DB. The central role of the propensity score in observational studies for causal effects. Biometrika. 1983;70(1):41-55. doi:10.1093/biomet/70.1.41
15. Legendre P. Spatial autocorrelation: trouble or new paradigm? Ecology. 1993;74(6):1659-73. doi:10.2307/1939924
16. Clifford P, Richardson S, Hémon D. Assessing the significance of the correlation between two spatial processes. Biometrics. 1989;45(1):123-34. doi:10.2307/2532039
17. Dutilleul P. Modifying the t test for assessing the correlation between two spatial processes. Biometrics. 1993;49(1):305-14. doi:10.2307/2532625
18. Alexander-Bloch AF, Shou H, Liu S, Satterthwaite TD, Glahn DC, Shinohara RT, et al. On testing for spatial correspondence between maps of human brain structure and function. NeuroImage. 2018;178:540-51. doi:10.1016/j.neuroimage.2018.05.070. PMID 29860082
19. Burt JB, Helmer M, Shinn M, Anticevic A, Murray JD. Generative modeling of brain maps with spatial autocorrelation. NeuroImage. 2020;220:117038. doi:10.1016/j.neuroimage.2020.117038
20. Burt JB, Demirtaş M, Eckner WJ, Navejar NM, Ji JL, Martin WJ, et al. Hierarchy of transcriptomic specialization across human cortex captured by structural neuroimaging topography. Nat Neurosci. 2018;21(9):1251-9. doi:10.1038/s41593-018-0195-0
21. Wagner HH, Dray S. Generating spatially constrained null models for irregularly spaced data using Moran spectral randomization methods. Methods Ecol Evol. 2015;6(10):1169-78. doi:10.1111/2041-210x.12407
22. Markello RD, Misic B. Comparing spatial null models for brain maps. NeuroImage. 2021;236:118052. doi:10.1016/j.neuroimage.2021.118052. Preprint: bioRxiv. 2020. doi:10.1101/2020.08.13.249797
23. Váša F, Mišić B. Null models in network neuroscience. Nat Rev Neurosci. 2022;23(8):493-504. doi:10.1038/s41583-022-00601-9
24. Markello RD, Hansen JY, Liu Z-Q, Bazinet V, Shafiei G, Suárez LE, et al. neuromaps: structural and functional interpretation of brain maps. Nat Methods. 2022;19(11):1472-9. doi:10.1038/s41592-022-01625-w
25. Lockless SW, Ranganathan R. Evolutionarily conserved pathways of energetic connectivity in protein families. Science. 1999;286(5438):295-9. doi:10.1126/science.286.5438.295
26. Süel GM, Lockless SW, Wall MA, Ranganathan R. Evolutionarily conserved networks of residues mediate allosteric communication in proteins. Nat Struct Biol. 2003;10(1):59-69. doi:10.1038/nsb881
27. Halabi N, Rivoire O, Leibler S, Ranganathan R. Protein sectors: evolutionary units of three-dimensional structure. Cell. 2009;138(4):774-86. doi:10.1016/j.cell.2009.07.038
28. Reynolds KA, McLaughlin RN, Ranganathan R. Hot spots for allosteric regulation on protein surfaces. Cell. 2011;147(7):1564-75. doi:10.1016/j.cell.2011.10.049. PMID 22196731
29. Teşileanu T, Colwell LJ, Leibler S. Protein sectors: statistical coupling analysis versus conservation. PLoS Comput Biol. 2015;11(2):e1004091. doi:10.1371/journal.pcbi.1004091
30. Fodor AA, Aldrich RW. Influence of conservation on calculations of amino acid covariance in multiple sequence alignments. Proteins. 2004;56(2):211-21. doi:10.1002/prot.20098
31. McLaughlin RN, Poelwijk FJ, Raman A, Gosal WS, Ranganathan R. The spatial architecture of protein function and adaptation. Nature. 2012;491(7422):138-42. doi:10.1038/nature11500
32. Mishra SK, Kandoi G, Jernigan RL. Coupling dynamics and evolutionary information with structure to identify protein regulatory and functional binding sites. Proteins. 2019;87(10):850-68. doi:10.1002/prot.25749
33. Morcos F, Pagnani A, Lunt B, Bertolino A, Marks DS, Sander C, et al. Direct-coupling analysis of residue coevolution captures native contacts across many protein families. Proc Natl Acad Sci USA. 2011;108(49):E1293-301. doi:10.1073/pnas.1111471108
34. Ekeberg M, Lövkvist C, Lan Y, Weigt M, Aurell E. Improved contact prediction in proteins: using pseudolikelihoods to infer Potts models. Phys Rev E. 2013;87(1):012707. doi:10.1103/physreve.87.012707
35. Kamisetty H, Ovchinnikov S, Baker D. Assessing the utility of coevolution-based residue–residue contact predictions in a sequence- and structure-rich era. Proc Natl Acad Sci USA. 2013;110(39):15674-9. doi:10.1073/pnas.1314045110
36. Rao R, Meier J, Sercu T, Ovchinnikov S, Rives A. Transformer protein language models are unsupervised structure learners. bioRxiv. 2020. doi:10.1101/2020.12.15.422761
37. Lin Z, Akin H, Rao R, Hie B, Zhu Z, Lu W, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science. 2023;379(6637):1123-30. doi:10.1126/science.ade2574
38. Eccleston RC, Furnham N. Allosteric site prediction using protein language models and orthosteric conditioning. bioRxiv. 2025. doi:10.1101/2025.06.27.662060
39. Khokhar M, Keskin O, Gursoy A. DeepAllo: allosteric site prediction using protein language model (pLM) with multitask learning. Bioinformatics. 2025;41(6):btaf294. doi:10.1093/bioinformatics/btaf294
40. Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, et al. Predicting and decoding allosteric binding sites using protein language models and structure-based machine learning: an energy landscape-guided explainable AI framework. J Chem Theory Comput. 2026;22(10):5326-47. doi:10.1021/acs.jctc.6c00427
41. Schmidtke P, Barril X. Understanding and predicting druggability. A high-throughput method for detection of drug binding sites. J Med Chem. 2010;53(15):5858-67. doi:10.1021/jm100574m
42. Tian W, Chen C, Lei X, Zhao J, Liang J. CASTp 3.0: computed atlas of surface topography of proteins. Nucleic Acids Res. 2018;46(W1):W363-7. doi:10.1093/nar/gky473
43. Guerra JVDS, Ribeiro-Filho HV, Jara GE, Bortot LO, Pereira JGC, Lopes-de-Oliveira PS. pyKVFinder: an efficient and integrable Python package for biomolecular cavity detection and characterization in data science. BMC Bioinformatics. 2021;22(1):607. doi:10.1186/s12859-021-04519-4
44. Jacobs DJ, Rader AJ, Kuhn LA, Thorpe MF. Protein flexibility predictions using graph theory. Proteins. 2001;44(2):150-65. doi:10.1002/prot.1081
45. Sljoka A. Probing allosteric mechanism with long-range rigidity transmission across protein networks. Methods Mol Biol. 2020;2253:61-75. doi:10.1007/978-1-0716-1154-8_5
46. Khade PM, Savol A, Jernigan RL. Characterizing and predicting protein hinges for mechanistic insight. J Mol Biol. 2020;432(2):508-22. doi:10.1016/j.jmb.2019.11.018
47. Khade PM, Scaramozzino D, Kumar A, Lacidogna G, Carpinteri A, Jernigan RL. hdANM: a new comprehensive dynamics model for protein hinges. Biophys J. 2021;120(22):4955-65. doi:10.1016/j.bpj.2021.10.017
48. Khade PM, Kumar A, Jernigan RL. PACKMAN-molecule: Python toolbox for structural bioinformatics. Bioinform Adv. 2022;2(1):vbac007. doi:10.1093/bioadv/vbac007
49. Kaynak BT, Bahar I, Doruker P. Essential site scanning analysis: a new approach for detecting sites that modulate the dispersion of protein global motions. Comput Struct Biotechnol J. 2020;18:1577-86. doi:10.1016/j.csbj.2020.06.020. PMID 32637054
50. Kumar A, Kaynak BT, Dorman KS, Doruker P, Jernigan RL. Predicting allosteric pockets in protein biological assemblages. Bioinformatics. 2023;39(5):btad275. doi:10.1093/bioinformatics/btad275
51. Ferreiro DU, Hegler JA, Komives EA, Wolynes PG. Localizing frustration in native proteins and protein assemblies. Proc Natl Acad Sci USA. 2007;104(50):19819-24. doi:10.1073/pnas.0709915104
52. Ferreiro DU, Hegler JA, Komives EA, Wolynes PG. On the role of frustration in the energy landscapes of allosteric proteins. Proc Natl Acad Sci USA. 2011;108(9):3499-503. doi:10.1073/pnas.1018980108
53. Freiberger MI, Guzovsky AB, Wolynes PG, Parra RG, Ferreiro DU. Local frustration around enzyme active sites. Proc Natl Acad Sci USA. 2019;116(10):4037-43. doi:10.1073/pnas.1819859116
54. Parra RG, Schafer NP, Radusky LG, Tsai M-Y, Guzovsky AB, Wolynes PG, et al. Protein Frustratometer 2: a tool to localize energetic frustration in protein molecules, now with electrostatics. Nucleic Acids Res. 2016;44(W1):W356-60. doi:10.1093/nar/gkw304
55. Rausch AO, Freiberger MI, Leonetti CO, Luna DM, Radusky LG, Wolynes PG, et al. FrustratometeR: an R-package to compute local frustration in protein structures, point mutants and MD simulations. Bioinformatics. 2021;37(18):3038-40. doi:10.1093/bioinformatics/btab176
56. Amor BRC, Schaub MT, Yaliraki SN, Barahona M. Prediction of allosteric sites and mediating interactions through bond-to-bond propensities. Nat Commun. 2016;7:12477. doi:10.1038/ncomms12477. PMID 27561351. Preprint: bioRxiv. 2016. doi:10.1101/056275
57. Wu N, Strömich L, Yaliraki SN. Prediction of allosteric sites and signalling: insights from benchmarking datasets. bioRxiv. 2021. doi:10.1101/2021.08.16.456251
58. Lieberman-Aiden E, van Berkum NL, Williams L, Imakaev M, Ragoczy T, Telling A, et al. Comprehensive mapping of long-range interactions reveals folding principles of the human genome. Science. 2009;326(5950):289-93. doi:10.1126/science.1181369
59. Ay F, Bailey TL, Noble WS. Statistical confidence estimation for Hi-C data reveals regulatory chromatin contacts. Genome Res. 2014;24(6):999-1011. doi:10.1101/gr.160374.113
60. Kaul A, Bhattacharyya S, Ay F. Identifying statistically significant chromatin contacts from Hi-C data with FitHiC2. Nat Protoc. 2020;15(3):991-1012. doi:10.1038/s41596-019-0273-0
61. Maslov S, Sneppen K. Specificity and stability in topology of protein networks. Science. 2002;296(5569):910-3. doi:10.1126/science.1065103
62. Milo R, Shen-Orr S, Itzkovitz S, Kashtan N, Chklovskii D, Alon U. Network motifs: simple building blocks of complex networks. Science. 2002;298(5594):824-7. doi:10.1126/science.298.5594.824
63. Roberts JA, Perry A, Lord AR, Roberts G, Mitchell PB, Smith RE, et al. The contribution of geometry to the human connectome. NeuroImage. 2016;124(Pt A):379-93. doi:10.1016/j.neuroimage.2015.09.009. PMID 26364864
64. Betzel RF, Bassett DS. Specificity and robustness of long-distance connections in weighted, interareal connectomes. Proc Natl Acad Sci USA. 2018;115(21):E4880-9. doi:10.1073/pnas.1720186115
65. Estrada E, Hatano N. Communicability in complex networks. Phys Rev E. 2008;77(3):036111. doi:10.1103/physreve.77.036111
66. Goñi J, van den Heuvel MP, Avena-Koenigsberger A, Velez de Mendizabal N, Betzel RF, Griffa A, et al. Resting-brain functional connectivity predicted by analytic measures of network communication. Proc Natl Acad Sci USA. 2014;111(2):833-8. doi:10.1073/pnas.1315529111
67. Panjkovich A, Daura X. Exploiting protein flexibility to predict the location of allosteric sites. BMC Bioinformatics. 2012;13:273. doi:10.1186/1471-2105-13-273
68. Panjkovich A, Daura X. PARS: a web server for the prediction of protein allosteric and regulatory sites. Bioinformatics. 2014;30(9):1314-5. doi:10.1093/bioinformatics/btu002
69. Huang W, Lu S, Huang Z, Liu X, Mou L, Luo Y, et al. Allosite: a method for predicting allosteric sites. Bioinformatics. 2013;29(18):2357-9. doi:10.1093/bioinformatics/btt399
70. Tian H, Jiang X, Tao P. PASSer: prediction of allosteric sites server. Mach Learn Sci Technol. 2021;2(3):035015. doi:10.1088/2632-2153/abe6d6
71. Xiao S, Tian H, Tao P. PASSer2.0: accurate prediction of protein allosteric sites through automated machine learning. ChemRxiv. 2021. doi:10.26434/chemrxiv-2021-q4319
72. Tian H, Xiao S, Jiang X, Tao P. PASSer: fast and accurate prediction of protein allosteric sites. Nucleic Acids Res. 2023;51(W1):W427-31. doi:10.1093/nar/gkad303
73. Wang J, Jain A, McDonald LR, Gambogi C, Lee AL, Dokholyan NV. Mapping allosteric communications within individual proteins. Nat Commun. 2020;11(1):3862. doi:10.1038/s41467-020-17618-2
74. Clarke D, Sethi A, Li S, Kumar S, Chang RWF, Chen J, et al. Identifying allosteric hotspots with dynamics: application to inter- and intra-species conservation. Structure. 2016;24(5):826-37. doi:10.1016/j.str.2016.03.008
75. Zha J, Li M, Kong R, Lu S, Zhang J. AlloReverse: multiscale understanding among hierarchical allosteric regulations. Nucleic Acids Res. 2023;51(W1):W33-8. doi:10.1093/nar/gkad279
76. Huang W, Wang G, Shen Q, Liu X, Lu S, Geng L, et al. ASBench: benchmarking sets for allosteric discovery. Bioinformatics. 2015;31(15):2598-600. doi:10.1093/bioinformatics/btv169
77. Huang Z, Zhu L, Cao Y, Wu G, Liu X, Chen Y, et al. ASD: a comprehensive database of allosteric proteins and modulators. Nucleic Acids Res. 2011;39(Database issue):D663-9. doi:10.1093/nar/gkq1022
78. Guarnera E, Tan ZW, Zheng Z, Berezovsky IN. AlloSigMA: allosteric signaling and mutation analysis server. Bioinformatics. 2017;33(24):3996-8. doi:10.1093/bioinformatics/btx430
79. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics. 1988;44(3):837-45. doi:10.2307/2531595
80. Hanley JA, McNeil BJ. A method of comparing the areas under receiver operating characteristic curves derived from the same cases. Radiology. 1983;148(3):839-43. doi:10.1148/radiology.148.3.6878708
81. Demler OV, Pencina MJ, D'Agostino RB Sr. Misuse of DeLong test to compare AUCs for nested models. Stat Med. 2012;31(23):2577-87. doi:10.1002/sim.5328
82. Seshan VE, Gönen M, Begg CB. Comparing ROC curves derived from regression models. Stat Med. 2013;32(9):1483-93. doi:10.1002/sim.5648
83. Begg CB, Cronin AM, Vickers AJ. Testing the incremental predictive accuracy of new markers. Clin Trials. 2013;10(5):690-4. doi:10.1177/1740774513496490
84. Vickers AJ, Cronin AM, Begg CB. One statistical test is sufficient for assessing new predictive markers. BMC Med Res Methodol. 2011;11:13. doi:10.1186/1471-2288-11-13
85. Pepe MS, Kerr KF, Longton G, Wang Z. Testing for improvement in prediction model performance. Stat Med. 2013;32(9):1467-82. doi:10.1002/sim.5727
86. Robin X, Turck N, Hainard A, Tiberti N, Lisacek F, Sanchez J-C, et al. pROC: an open-source package for R and S+ to analyze and compare ROC curves. BMC Bioinformatics. 2011;12:77. doi:10.1186/1471-2105-12-77
87. Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative controls: a tool for detecting confounding and bias in observational studies. Epidemiology. 2010;21(3):383-8. doi:10.1097/ede.0b013e3181d61eeb
88. Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement. BMC Med. 2015;13:1. doi:10.1186/s12916-014-0241-z
89. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804. doi:10.1016/j.patter.2023.100804
90. Plaxco KW, Simons KT, Baker D. Contact order, transition state placement and the refolding rates of single domain proteins. J Mol Biol. 1998;277(4):985-94. doi:10.1006/jmbi.1998.1645
</content>

</invoke>
