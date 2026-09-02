# The benchmark

Everything a method receives, and everything it is scored against. All of it was frozen
before any method existed. That order is the whole point: a scoring rule chosen after the
results are in is not a scoring rule.

Three frozen sets sit here as siblings. Shared material sits at this level.

```
docs/benchmark/
  README.md      this page
  primary/       the three disease areas CHALLENGE.md Table 1 assigns. 6 arms
  secondary/     9 further targets, in two disjoint tiers
  evaluation/    how a score is computed. Protocol version 3
  evidence/      the literature the three sets rest on
  review/        the 2026-09-02 audit of all three, and what the organisers' answers force
```

---

## Which one do you want?

| Question                                                                           | Open                                           |
| ---------------------------------------------------------------------------------- | ---------------------------------------------- |
| What structure, chain and node set does a method get for KRAS, BCR-ABL1 or myosin? | [`primary/README.md`](primary/README.md)       |
| Where do I tune a hyperparameter, and what proves generalisation?                  | [`secondary/README.md`](secondary/README.md)   |
| What endpoint, null, decoys and multiplicity correction does a score go through?   | [`evaluation/README.md`](evaluation/README.md) |
| Why is that pair defensible, and who says so?                                      | [`evidence/README.md`](evidence/README.md)     |
| Is any of it wrong, and what did the organisers rule?                              | [`review/README.md`](review/README.md)         |

---

## `primary/` — the three assigned disease areas

Frozen **2026-08-24**, and a sixth arm added by ADR 0031 on 2026-09-02. Six scoreable arms:
for KRAS G12C, BCR-ABL1 and cardiac myosin, the
**mandated** pair exactly as `CHALLENGE.md` gives it, and a **corrected** pair for the same
protein and the same site.

All three mandated pairs are defective. All three are now scoreable: ADR 0031 replaced the
cardiac-myosin holo with `9GZ2`, which the organisers permit. `primary/audit/` holds the
forensic audit per target, re-derived from the deposited coordinate files.

```
primary/manifest.yaml   every pinned choice, with its reason
primary/frozen.json     the consequences. The authority for every count and label set
primary/README.md       the argument
primary/audit/          why each mandated pair is defective
```

## `secondary/` — generalisation and scale

Frozen **2026-08-24**. Nine targets from 97 candidates, in two tiers that never mix
(ADR 0021).

- `development` carries **every** hyperparameter. Metric, Hamiltonian, cutoff, coarse-graining
  ratio. Tune here and nowhere else.
- `generalisation` carries the Phase 5 claim. It stays closed until the method is frozen.

Without the first tier, an ablation runs on the primary benchmark, which is test-set fitting.
Without the second, no set can demonstrate generalisation, because the tuning set is burned by
construction.

`secondary/selection.json` is an answer key. Nothing on the prediction path opens it.

## `evaluation/` — how a score is computed

Frozen **2026-09-02** at **protocol version 3**. Endpoint, estimator, null, decoy pockets,
multiplicity correction and required baselines, for all 15 arms. Every method calls
`allo.scoring.score_arm` and no other path.

Version 1 was frozen and reopened the same day by its own audit.
[`evaluation/AUDIT.md`](evaluation/AUDIT.md) is the record. Read it before you trust a number
that a pre-audit document quotes.

Nothing in this directory changes once a method has been scored.

## `evidence/` — the literature

Shared across all three sets, which is why it sits at this level rather than inside one of
them. Definitions, prior art, curation standard, per-target evidence, and the evaluation
metric review. [`evidence/README.md`](evidence/README.md) indexes the fourteen files and says
which are superseded.

---

## Three things that are true of the whole benchmark, not of one set

Read these before quoting any result from any set.

1. **All fifteen arms use a synthetic small molecule as the effector.** No arm tests classical
   allosteric enzymology — cooperativity, metabolite feedback, a physiological effector such as
   AMP, GTP or acetyl-CoA. The cause is measured: of 32 physiological-effector holo entries
   screened for the secondary set, 23 were killed by the single-chain lining clause, because
   those phenomena are quaternary. Any claim from this benchmark is a claim about **drug-like
   allosteric pockets in a single chain**.
2. **The negative class has an unknown false-negative rate.** Each arm labels one site positive
   and everything else negative. Beltran 2026 (doi:10.1126/sciadv.aea2726) reports dozens of
   functionally allosteric surfaces on Src alone. A scored false positive may be a real site
   nobody annotated, so precision-style endpoints are more trustworthy here than recall-style
   ones.
3. **Ground truth is a binding-site label set, not a coupling label set.** No structure pair
   can establish that a method recovered *coupling* rather than *a pocket*. Allostery is
   inherited from the cited functional experiments in each arm's `allosteric_evidence`, never
   from the coordinates. The honest claim is "ranks the experimentally validated allosteric
   pocket highly on apo input" (ADR 0007).

## Two rules for everything under this directory

**`frozen.json` is the authority.** Never quote a residue count, a label set or an active
site from prose. Prose drifts and a freeze does not.

**`n_residues` is not `n_candidates`.** The first is what a method **receives**. The second is
what it is **scored against**. Residues that score by construction leave both classes
(ADR 0011), so the two numbers differ on every arm.

## Verify it

```bash
uv run allo benchmark verify --set all    # re-derive both input layers from the deposited files
uv run allo evaluate verify --detect      # re-derive the evaluation layer and the pockets
```

Both exit 0 only if nothing moved. `make verify` runs them together with the network tests
that byte-check every pinned structure.
