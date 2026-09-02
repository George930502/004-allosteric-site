# Conventions for the Phase 2 method-layer literature review

Every file in this directory obeys these rules. Read this before you write or quote one.

---

## 1. What this review is for

Phase 1 closed. The input layer and the evaluation layer are both frozen. Phase 2 must
choose a **method**: a quantum, quantum-inspired or hybrid algorithm that takes an apo
structure, builds a residue network, propagates a signal, and ranks residues by dynamic
connectivity to the active site (`CHALLENGE.md` §4.1, §5).

This review supplies the evidence for that choice. It is **not** a summary of the field for
its own sake. Every section must end by saying what the finding changes for our pipeline.

## 2. Evidence rules (project rule R3)

- **A recalled number is not evidence.** Every number carries a DOI, an arXiv ID, or a URL
  retrieved in this session.
- **Tag every claim.** Use exactly these three tags:
  - `[VERIFIED-FULLTEXT]` — the quote came back from the paper's full text this session.
  - `[VERIFIED-ABSTRACT]` — the quote came back from an abstract or metadata record.
  - `[UNVERIFIED]` — inference, or a claim that could not be sourced this session.
- **A negative result is a result.** Write "not retrieved by the recorded search", never
  "does not exist". ADR 0019 forbids an absence-of-prior-art claim from a scoped search.
- **Record the search.** Each file ends with a Method section: queries run, databases hit,
  counts retrieved, counts screened in, and the stopping rule.
- **Numbers must be comparable before they are compared.** State the dataset, the positive
  class, the negative class and the criterion beside every metric. Different papers use
  different hit criteria, and the differences are large.

## 3. Retrieval routes that work

Reachable and tested on 2026-08-25:

| Route | Endpoint |
| --- | --- |
| arXiv | `https://export.arxiv.org/api/query?search_query=...` |
| Europe PMC search | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json` |
| Europe PMC full text | `https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML` |
| PubMed E-utilities | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=...` |
| PMC article page | `https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/` |

Semantic Scholar returned HTTP 429 and is rate limited. If Europe PMC `fullTextXML` returns
404, try the PMC article page before you record the source as closed.

## 4. Hard constraints the method must satisfy

These come from the challenge, not from us. A method that breaks one is unusable, however
good its published numbers are. Say so explicitly when you review such a method.

| # | Rule |
| --- | --- |
| C1 | Apo input only. Holo information may not enter the prediction path. |
| C2 | No classical MD trajectories as input, and no MD-trained weights in the prediction path. |
| C3 | Circuit depth, qubit count and connectivity reported for every quantum method. |
| C4 | A credible path to near-term or fault-tolerant hardware. Quantum-inspired is allowed, but it must state how it maps to hardware. |
| C5 | Catalytic domains. Waters, cofactors and PTMs excluded unless modelled as simple nodes. |
| C6 | Elastic network hypothesis: contact topology drives propagation. |

C2 is the one that eliminates most published AI methods. PocketMiner trains on MD.
CrypToth runs mixed-solvent MD. Note the violation, then say whether any part of the
method survives without the trajectory.

## 5. What is already known — read with ADR 0026 beside it

> **Amended 2026-08-26. The heading of this section used to read "do not re-derive it", and
> that instruction no longer binds.** The benchmark that closed these eleven items contains
> all three of our primary targets in its own evaluation sets — KRAS, the ABL1 myristoyl
> pocket and myosin — so it fails ADR 0012's disjointness clauses. **ADR 0026** records the
> check and the rule that follows: a negative result there is *prior*, not verdict, and a
> method is closed for this project only when an experiment on this frozen benchmark, run
> through `allo.scoring.score_arm`, produces a number.
>
> Three of the eleven survive re-opening on mathematics rather than on measurement, and stay
> closed: items **9, 10 and 11**. The OTOC and Krylov collapse to `C(r,t) = 4 g²(r,t)`, the
> Lieb-Robinson bound collapses to the same transfer amplitude, and a real symmetric contact
> graph has neither non-reciprocal hopping nor gain and loss. Those are identities.
>
> The other eight were re-measured on the `development` tier in
> `experiments/2026-08-26-method-sweep`. Six constructions this list never tested are named
> in ADR 0026 and are implemented in `allo.quantum.walk` and `allo.classical`. The
> re-derivation that separates genuinely new observables from transforms of the
> single-particle amplitude is `../exploration/lit/23-quantum-node-ranking.md`.
>
> The eleven items below are still informative. They are a well-argued prior over what is
> likely to fail, and the mechanism they diagnose is a real argument. They are no longer a
> reason not to measure.

A teammate's repository (`allosteric-benchmark/`) has already measured eleven quantum
insertion points on 73–101 targets, and all eleven lost to a classical spectral readout.
The mechanism was diagnosed, not assumed:

> A single-particle Hermitian walk on a graph is classically simulable and carries no
> information beyond its transfer amplitudes. Every genuinely quantum observable found
> needs many-body interactions or non-Hermitian structure, and a residue contact graph
> supplies neither.

Closed by measurement, with the numbers in `allosteric-benchmark/README.md` §6, §7, §9 and
`allosteric-benchmark/docs/quantum-observable-search.md`:

1. Absolute CTQW transfer amplitude — correlates −0.60 to −0.71 with distance; it is a
   proximity ranker.
2. Coherent transfer as the perturbation readout — 9.1 % significant against 90.9 %.
3. ENAQT / dephasing-assisted transport — no optimum over γ from 0 to 3·J_max.
4. Level-spacing degeneracy structure — 54.5 % against 90.9 %.
5. Eigenvector content and mode IPR — 63.6 % and 36.4 %.
6. Cooperative selection as a QUBO — classical annealing hits the exhaustive optimum at
   every size up to C(34,7).
7. Degeneracy readouts on symmetric multimers — symmetry enriches degeneracy, the readout
   still loses.
8. Chiral quantum walks — the precondition held (7.7–8.3 cycles per residue) and the
   observable was still uninformative, AUC 0.318–0.565 against 0.757.
9. OTOCs, operator growth, Krylov complexity — algebraically `C(r,t) = 4 g²(r,t)`, four
   times the squared transfer amplitude already rejected.
10. Lieb-Robinson light cones — collapses to the same transfer amplitude.
11. Non-Hermitian sensing and exceptional points — a real symmetric contact graph has
    neither non-reciprocal hopping nor gain and loss.

Also settled there, and load-bearing for anything new:

- **The bar is one line of geometry.** `ctrl_closeness = −distance` reaches AUC 0.617 on 73
  curated targets. The best method tested leads it by 0.001. Real allosteric sites are
  **closer** to the active site than the distal background.
- **Plain AUC is confounded.** Under distance stratification at 2 Å, only ALPS separates
  from a 25-draw random floor of 0.496 ± 0.016, at +0.082, p = 0.03 uncorrected — and
  nothing survives Bonferroni over 13 comparisons.
- **A published quantum result already exists.** Mohtashim, Sajjan & Kais, _JACS_ 2026,
  doi:10.1021/jacs.6c08053: CTQW centrality on residue interaction networks over 150
  proteins shows "consistently strong agreement with classical eigenvector centrality".
- **Quantum kernels are pre-refuted at our feature dimension.** A bandwidth-tuned quantum
  kernel becomes numerically indistinguishable from an RBF kernel.
- **Protein language models collapse on allosteric sites.** AUPR 0.64–0.76 on orthosteric
  against **0.06** on allosteric in the same proteins, with AUROC still 0.70.

**Quantum reservoir computing is the one candidate that appeared in the corpus and was
never characterised.** No full text was landed and no cards were extracted.

Your job is to find what is **not** on this list, or to bring evidence that changes an item
on it. Re-reporting one of these eleven as a new idea is a wasted file.

## 6. What our method must clear

Not "beat the best published number". Published numbers are inflated: AlloBench dropped
every test protein sharing a UniRef50 cluster with a training protein and found that no
tool exceeded 60 % accuracy even at a very low Jaccard cutoff. The real bar is four
numbers, and a method must clear them together:

1. `−distance` from the active site, at AUC ≈ 0.617.
2. `cavity_volume`, a zero-parameter geometric detector, which rejects the null on all
   three confirmatory arms of our own frozen benchmark.
3. Eigenvector centrality, which is one line and which a CTQW reproduces.
4. APOP and ESSA, the unsupervised ENM bar that satisfies C1, C2 and C6 exactly. On
   matched apo structures APOP reports top-3 of 11/15 = 73 %, against ESSA's 7/14 = 50 %
   on essentially the same set (doi:10.1093/bioinformatics/btad275). Neither number
   survives the field's own leakage-controlled reappraisal: AlloBench retests APOP at
   **15 %** at Jaccard > 0.5, and no tool of eight clears 60 % even at a very low cutoff
   (doi:10.1021/acsomega.5c01263). CAPASP finds APOP and PASSer degrade specifically on
   apo input against holo input (doi:10.1007/s10822-026-00831-4) — which is the exact axis
   the challenge scores on.

   *Corrected 2026-08-25 by file 01. The earlier text called ESSA's 50 % the only clean
   apo-versus-holo comparison. APOP reports a higher number on the same kind of set.*

## 7. Leakage guard — do not open these

Five paths hold answer keys. Nothing in this review needs them, and quoting a real label
residue into a method-design document defeats C1.

1. `docs/benchmark/primary/frozen.json`
2. `docs/benchmark/secondary/frozen.json` and `docs/benchmark/secondary/selection.json`
3. `docs/benchmark/primary/manifest.yaml` and `docs/benchmark/secondary/manifest.yaml`
4. `docs/benchmark/secondary/evidence/extension-candidates.md`
5. Everything under `docs/benchmark/evaluation/`

`tests/test_no_leakage.py` enforces this for code. For documents it is on you.

## 8. File format

Each file opens with:

```
# <Title>

**Scope:** one sentence saying what this file covers and what it deliberately excludes.
**Sibling files:** the neighbours that cover the excluded parts.
**Retrieved:** YYYY-MM-DD.
```

Then the body. Then two closing sections, both mandatory:

- **What this changes for our pipeline** — a short list of decisions this evidence
  supports or blocks, each naming the pipeline stage it touches.
- **Method** — queries, databases, counts, stopping rule, and what could not be reached.

Write in the project's documentation register: short sentences, active voice, one topic per
paragraph, no marketing adjectives. State a limitation where one exists.
