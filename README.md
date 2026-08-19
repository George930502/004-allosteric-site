# Allosteric Site Discovery via Quantum Signal Propagation

Research codebase for the **Global Quantum + AI Challenge 2026 — Cleveland Clinic
Enterprise Challenge**: *Unlocking undruggable targets: quantum simulation of
allosteric signal propagation.*

> Over 85% of disease-causing proteins lack a druggable active site. For those
> targets the only viable strategy is allostery — finding a hidden distal pocket
> whose occupancy shuts the active site down from a distance. Finding those
> channels classically takes months of MD and relies on approximations that are
> often too linear to capture the real, non-linear signal propagation.

**What this repo builds:** an *allosteric scanner*. Input an apo PDB structure,
output a ranked map of residues by their **dynamic connectivity to the active
site**, computed from quantum information propagation over the residue contact
network — no MD trajectories anywhere in the pipeline.

The full challenge statement is restated verbatim in [`CHALLENGE.md`](CHALLENGE.md).
Agent operating rules are in [`AGENTS.md`](AGENTS.md).

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
[`docs/decisions/0002-quantum-metric-hypothesis.md`](docs/decisions/0002-quantum-metric-hypothesis.md).

## Validation targets

| Target | Apo (input) | Holo (ground truth) | Pocket to find |
|---|---|---|---|
| KRAS G12C | `4OBE` | `6OIM` | cryptic Switch-II pocket (sotorasib) |
| BCR-ABL1 | `1OPL` | `5MO4` | distal myristoyl pocket (asciminib) |
| Cardiac myosin | `5TBY` | `6C1H` | mavacamten site (super-relaxed state) |
| c-Myc (stretch) | `1NKP` | — | no ground truth; consensus-judged |

Details and the ground-truth derivation policy: [`docs/targets.md`](docs/targets.md).

## Quickstart

```bash
make setup     # uv sync --extra dev  (Python >= 3.11, creates .venv)
make check     # format + lint + fast tests — the gate for every change
```

Optional backends: `uv sync --extra hw` (AWS Braket, Classiq),
`uv sync --extra viz` (3D structure rendering).

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 0 | Repo, harness, agent infrastructure | done |
| 1 | Classical foundation: structures, networks, ground truth, baselines, scoring harness | next |
| 2 | Quantum propagation metric (statevector) | |
| 3 | Circuit implementation, depth budget, noise resilience | |
| 4 | Coarse-graining and scalability | |
| 5 | Interpretability, 3D visualisation, report, c-Myc + extra targets | |

Phase detail and exit criteria: [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Repository layout

```
CHALLENGE.md         the spec
AGENTS.md            agent operating contract (CLAUDE.md -> symlink)
docs/                roadmap, ADRs, targets, methodological report
src/allo/            package, organised by pipeline stage
experiments/         one directory per run: config, metrics, notes
results/<target>/    connectivity matrix + top-5 hit list per target
data/                raw PDB downloads and derived artifacts (gitignored)
```

## License

MIT — see [`LICENSE`](LICENSE).
