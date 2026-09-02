# Allosteric Site Discovery via Quantum Signal Propagation

Research codebase for the **Global Quantum + AI Challenge 2026 — Cleveland Clinic
Enterprise Challenge**: *Unlocking undruggable targets: quantum simulation of
allosteric signal propagation.*

> Over 85% of disease-causing proteins lack a druggable active site. For those
> targets the only viable strategy is allostery — finding a hidden distal pocket
> whose occupancy shuts the active site down from a distance. Finding those
> channels classically takes months of MD and relies on approximations that are
> often too linear to capture the real, non-linear signal propagation.

**Status, 2026-09-02.** Phase 1 is closed, and both frozen layers moved once more on
2026-09-02 — **before any method was scored**, which is the only condition under which they
may move at all.

The organisers answered four questions about the benchmark, and a multi-axis audit of all
three frozen sets ran against those answers
([`docs/benchmark/review/`](docs/benchmark/review/)). Eight decisions came out of it, ADRs
0029 to 0036. The **primary input layer is re-frozen at six arms**: `bcr_abl1_mandated` moved
to the chain the organisers designated, and `cardiac_myosin_mandated` is frozen for the first
time. Both are **non-confirmatory** and print their measured defects. All four minimum targets
now have a contract. The **evaluation layer** is re-frozen at **protocol version 3** over fifteen arms. The
recalibration reproduced thirteen of the fifteen arms' thresholds to six decimal places and
moved only the two the input re-freeze changed, which is the check that says they moved for a
reason.

Every departure from `CHALLENGE.md` Table 1 is on one page:
[`docs/report/substitutions.md`](docs/report/substitutions.md).

No method exists yet, and that order is deliberate: every scoring choice is fixed before any
method can be tuned against it. Phase 2 designs the quantum propagation metric. See
[Roadmap](#roadmap).

**What this repo builds:** an *allosteric scanner*. Input an apo PDB structure,
output a ranked map of residues by their **dynamic connectivity to the active
site**, computed from quantum information propagation over the residue contact
network — no MD trajectories anywhere in the pipeline.

The full challenge statement is restated verbatim in [`CHALLENGE.md`](CHALLENGE.md).
Agent operating rules and the research principles are in [`AGENTS.md`](AGENTS.md);
the field itself — protein allostery, elastic-network biophysics, quantum transport on
graphs — is defined in [`docs/FIELD.md`](docs/FIELD.md), together with the known
intellectual traps in this challenge.

---

## Quickstart

```bash
make setup     # uv sync --extra dev  (Python >= 3.11, creates .venv)
make check     # format + lint + tests — the offline gate for every change
make verify    # re-derive both frozen layers from RCSB and fail on drift (needs network)
```

`make check` is offline and takes seconds. Run it before every commit. `make verify`
re-downloads the pinned structures, re-derives both freezes and re-runs the pocket detector.
Run it before a merge.

Optional extras:

- `uv sync --extra eval` — pyKVFinder, needed only to re-derive the decoy pockets.
- `uv sync --extra hw` — AWS Braket and Classiq backends.
- `uv sync --extra viz` — 3D structure rendering.

The command line entry point is `allo`:

```bash
uv run allo benchmark show --set all      # what each target holds
uv run allo benchmark verify --set all    # re-derive the input layer, exit 1 on drift
uv run allo evaluate verify --detect      # re-derive the evaluation layer and the pockets
uv run allo new-experiment "ctqw time-averaged transfer"
```

---

## The hypothesis

Under the elastic network hypothesis, a protein's contact topology is the primary
driver of signal propagation. That topology is a graph — and graph dynamics is
exactly where quantum and classical transport diverge.

1. **Structure → network.** Apo structure → residues as nodes, contacts within a
   cutoff as edges, weighted by an elastic-network spring model.
2. **Network → Hamiltonian.** The contact graph becomes a Hamiltonian `H` (adjacency
   / Laplacian / ENM Hessian variants). In the single-excitation sector of an XY spin
   model this is realised with **one qubit per network node**.
3. **Propagation.** Inject an excitation at the active site and evolve under
   `exp(-iHt)` — a continuous-time quantum walk. Unlike classical diffusion
   (`exp(-Lt)`), the walk spreads ballistically and **interferes**: amplitude arriving
   at a residue by different structural paths can add or cancel. Our working claim is
   that this interference structure is a sharper discriminator of genuine allosteric
   channels than diffusive smearing, which washes out path specificity.
4. **Metric.** Time-averaged transfer amplitude between residue pairs gives the
   **N x N connectivity matrix**; connectivity to the active site gives the residue
   ranking and the **top-5 hit list**.
5. **Validation.** Blind prediction from the apo structure, scored against the pocket
   observed in the drug-bound holo structure, tested for statistically significant
   enrichment over random background residues and non-functional surface pockets.

The exact metric is a research question, not a settled choice — the challenge
explicitly leaves it to participants. Candidates and their status are tracked in
[`docs/adr/0002-quantum-metric-hypothesis.md`](docs/adr/0002-quantum-metric-hypothesis.md).

## Validation targets

These are the pairs `CHALLENGE.md` Table 1 assigns. A forensic audit of the deposited
files found **all three defective**, one fatally. Each disease area therefore carries two
arms: the mandated pair exactly as given, and a defensible `corrected` pair for the same
protein and the same site. Both are frozen before any method exists.

| Target | Mandated pair | Status of the mandated pair | Corrected pair |
|---|---|---|---|
| KRAS G12C | `4OBE` → `6OIM` | usable; apo is **wild-type** Gly12, not G12C | `4LDJ` → `6OIM` |
| BCR-ABL1 | `1OPL` **chain B** → `5MO4` | 17 labels; the nearest myristate atom is **16.0 Å** from the site (ADR 0029) | `2G2H` → `5MO4` |
| Cardiac myosin | `5TBY` → **`9GZ2`** | the organisers permit the substitution; 954 residues, 12 labels, scored non-confirmatory (ADR 0031) | `9GZ3` → `9GZ2` |
| c-Myc (stretch) | `1NKP` | scored against NMR segments, declared non-blind (ADR 0036) | — |

The frozen benchmark, the corrected pairs and the evidence:
[`docs/benchmark/primary/README.md`](docs/benchmark/primary/README.md). Ground-truth derivation policy:
[`docs/targets.md`](docs/targets.md).

## What is frozen, and why that matters

A prediction method can be tuned until it looks good. The defence against that is to fix
every input and every scoring rule **before** the method exists, and to make a command
re-derive them. This repo does that in two separate layers.

### The input layer — what a method receives

Frozen 2026-08-24 in [`docs/benchmark/primary/`](docs/benchmark/primary/README.md). It pins the structure
bytes, the chain, the node set, the active-site rule and the candidate set for **6 primary
arms** (five at the freeze, a sixth added by ADR 0031), and a second set of **9 secondary targets** in
[`docs/benchmark/secondary/`](docs/benchmark/secondary/README.md).

The secondary set is two disjoint tiers (ADR 0021). Every hyperparameter is chosen on the
`development` tier. The `generalisation` tier stays closed until the method is frozen. Without
that split, an ablation on the primary benchmark is test-set fitting.

### The evaluation layer — how a score is computed

Frozen 2026-09-02 in [`docs/benchmark/evaluation/`](docs/benchmark/evaluation/README.md), at
**protocol version 3**. It pins the endpoint, the estimator, the null, the decoy pockets, the
multiplicity correction and the required baselines for all 15 arms. Every method calls
`allo.scoring.score_arm` and no other path.

Version 3 opened because the **input** layer moved, not because a defect was found in version
2. See [`README.md`](docs/benchmark/evaluation/README.md) §0 for the six changes and why each
is not a hyperparameter.

Version 1 was frozen and reopened the same day by its own audit. Two blockers were found:
the procedure did not control the family-wise error rate, and a trivial geometric baseline
cleared the whole confirmatory family. Both are repaired.
[`docs/benchmark/evaluation/AUDIT.md`](docs/benchmark/evaluation/AUDIT.md) is the record of
everything the audit found.

**One consequence a reader must see before any result.** Rank each residue by the volume of
the largest cavity that lines it — label-blind, apo-only, zero parameters — and that score
rejected the null on all three confirmatory arms under protocol version 2. **Under version 3
it rejects on one of three** (`p_calibrated` 0.0046 / 0.0715 / 0.3236), because ADR 0030
re-froze the detector this baseline is computed from. Rejecting the null is still a low bar,
and the report's claim threshold is **beating that baseline**, not clearing the null.

### The separation is enforced, not promised

Holo structures build the labels and never enter the prediction path (constraint C1). The
import graph enforces it, `src/allo/groundtruth/` is a sink, and fourteen file-read routes that no
import trace can see are named and guarded in
[`tests/test_no_leakage.py`](tests/test_no_leakage.py).

## How to score a method

Phase 2 onward, every number goes through one function.

```python
from allo.inputs import apo_input
from allo.scoring import compare_methods, score_arm

apo = apo_input("kras_g12c_corrected")  # apo only. No label is reachable from here
scores = my_method(apo)  # dict: author residue number -> score

result = score_arm("kras_g12c_corrected", scores, method="ctqw_transfer")
result["p_calibrated"]  # the confirmatory p-value, size-corrected at every Holm level
result["auc_roc"]  # reported endpoints, each against its own chance line
result["recall_at_5"]  # the top-5 deliverable, against its hypergeometric baseline
result["dcc_angstrom"]  # distance from the predicted centre to the site centre

# The claim threshold is beating a baseline, so the paired test is part of the protocol.
compare_methods(
    "kras_g12c_corrected", scores, baseline_scores, names=("ctqw_transfer", "cavity_volume")
)["p_calibrated"]
```

The harness chooses the estimator, the tie rule, the null and the replicate count. A method
chooses none of them. That is the point.

Read [`docs/benchmark/evaluation/README.md`](docs/benchmark/evaluation/README.md) before you
read any number this repo produces.

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 0 | Repo, harness, agent infrastructure | ✅ done |
| 1 | Classical foundation: structures, ground truth, frozen benchmark, scoring harness | ✅ **closed** — input layer frozen 2026-08-24, re-frozen 2026-09-02 at six primary arms; evaluation layer frozen 2026-08-25 at protocol version 2, re-frozen 2026-09-02 at version 3 over fifteen arms |
| 2 | Quantum propagation metric (statevector) | **open — current phase** |
| 3 | Circuit implementation, depth budget, noise resilience | |
| 4 | Coarse-graining and scalability | |
| 5 | Interpretability, 3D visualisation, report, c-Myc + extra targets | |

Phase detail and exit criteria: [`docs/ROADMAP.md`](docs/ROADMAP.md).

**Both per-target blockers are cleared.** ADR 0031 supersedes ADR 0016 and exposes the
mandated 5TBY arm; ADR 0036 supersedes ADR 0020 and freezes the c-Myc contract. One gate
condition replaces them: protocol version 3 must be frozen before any method is scored.

## Repository layout

```
CHALLENGE.md            the spec, restated verbatim from the official PDF
CONTEXT.md              the settled vocabulary — "cryptic" and "allosteric" are not synonyms
AGENTS.md               operating contract: constraints C1-C6, principles R1-R4, routing
                        (CLAUDE.md is a symlink to it)
CONTRIBUTING.md         how to set up, work and open a pull request

src/allo/               the package, organised by pipeline stage
  structure/            PDB fetch and parse -> coordinates, residue indexing
  scoring/              the frozen harness: ranking, nulls, decoys, statistics
  groundtruth/          holo-derived labels ONLY. Never imported by prediction code
  inputs.py             the one prediction-path module that opens the input manifest
  benchmark.py          the freeze and its verification
  experiment.py         the run-directory scaffold behind `allo new-experiment`
  cli.py                the `allo` entry point
  --- reserved, created when the phase needs it (AGENTS.md fixes the name) ---
  viz/                  2D plots and 3D structure rendering            (Phase 5)
  --- built in Phase 2, then removed from main on 2026-09-02 (ADR 0037) ---
  network/ classical/ quantum/   whole on the branch method-layer-archive

docs/
  Cleveland-Clinic-Challenge-Statement-vF.pdf   the official source document
  ROADMAP.md            phases and their exit criteria. Start here
  PRINCIPLES.md         R1-R4 in full
  FIELD.md              the field, expert practice, and the traps in this challenge
  targets.md            per-protein chains and ground-truth derivation
  adr/                  40 decision records, indexed by topic in adr/README.md
  benchmark/            three frozen sets as siblings, indexed by benchmark/README.md
    primary/            the 3 assigned disease areas: manifest, frozen.json, audit
    secondary/          9 further targets in two disjoint tiers
    evaluation/         how a score is computed. Protocol version 4
    evidence/           the literature all three rest on
  playbooks/            phase-work, experiment and constraint-audit procedures
  agents/               issue tracker, triage labels, domain-doc layout
  report/               the methodological report, assembled across phases

experiments/            one directory per run: config.yaml, metrics.json, notes.md
  REGISTRY.md           one line per comparable number. Read it before you re-run anything
structures/             the offline mirror of every pinned structure (ADR 0014)
results/<target>/       connectivity matrix and top-5 hit list per target
tests/                  including test_no_leakage.py, which enforces constraint C1
data/                   downloads and derived artifacts (gitignored)
.claude/                agent skills, subagents and slash commands
```

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version:

1. `make setup`, then `make check` before every commit.
2. Read [`AGENTS.md`](AGENTS.md). Constraints C1–C6 are not negotiable, and C1 is the one
   that breaks silently.
3. Never edit a frozen artifact. If a freeze is wrong, open an ADR that supersedes it.
4. A new comparable number goes in `experiments/REGISTRY.md`. A negative result goes there too.

## Citing and reuse

MIT licensed. If you use the frozen benchmark or the evaluation protocol, cite this
repository and state the protocol version. The freezes are versioned artifacts, and a number
produced under protocol version 1 is not comparable to one produced under version 2.

## License

MIT — see [`LICENSE`](LICENSE).
