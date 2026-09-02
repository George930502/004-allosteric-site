# 0037 — The method layer leaves `main`, and the nine required baselines stay behind

**Status:** accepted · 2026-09-02 · withdraws [`0002`](0002-working-hypothesis-for-the-quantum-metric.md)
and [`0028`](0028-per-protein-adaptation-is-not-testable-at-four-arms.md)

## Context

`main` carried two layers that were never separated in git. The frozen layer is the
benchmark and the evaluation protocol. The method layer is the code and the runs that
propose a prediction. Only the frozen layer had ever been committed. The method layer, the
nine experiment runs behind it and the third-pass audit all existed as uncommitted working
files, on one machine, with no branch and no stash.

That is two problems in one. A clean clone could not reproduce what these documents call
frozen. And the frozen layer's status was unreadable, because method work in progress sat
beside it with no boundary a reader could see.

**The two layers are not symmetric, and one measurement shows why.** The frozen evaluation
manifest freezes nine `required_baselines` and states that no method result is reportable
until it is compared against all nine. Eight of the nine had exactly one implementation, in
`src/allo/classical/baselines.py`, and every one of them needs `src/allo/network/graph.py`
to build the graph it scores. Deleting the method layer wholesale would have left the frozen
protocol demanding numbers that no code in the repository could produce.

## Decision

**1. Remove the method layer from `main`, and preserve it whole on `method-layer-archive`.**
Removed: `src/allo/{network,classical,quantum}`, `tests/test_method.py`,
`docs/method/exploration/`, and the nine experiment directories dated 2026-08-26 and
2026-08-27. The branch is the only copy and is never deleted.

**2. A required baseline is a control, not a candidate method, and it stays.** A candidate
method is something this project proposes and wants scored. A required baseline is what the
frozen protocol mandates as the reference a candidate has to beat. The distinction decides
where code lives, and `classical/baselines.py` held both.

- `allo.network.graph` moves to **`allo.structure.graph`**, unchanged. It derives a graph
  from deposited coordinates and nothing else. It cannot move into `allo.scoring`, because a
  future prediction package needs the same builder and may not import the evaluation layer.
- Eight required scorers and their four transitive helpers move to
  **`allo.scoring.baselines`**, unchanged, with `REQUIRED_BASELINES` keyed by the name the
  manifest uses. The other twenty-two scorers in that module were candidate methods and go
  to the archive.

**The extraction is verified numerically, not by reading.** Every required baseline was
scored on all four `development` arms through `score_arm` and compared to the archived
sweep record: **32 scorer-arm pairs, 0 mismatches**, on `mean_rank`, `auc_roc`, `auc_pr`,
`precision_at_5`, `hits_at_5` and `recall_at_5`, to a tolerance of 1e-9.

**3. The literature review is evidence and stays.** `docs/method/review/` moves to
`docs/evidence/method-landscape/`. It holds twenty-three documents, every claim carrying a
DOI, no code and no scored number. ADRs 0026 and 0027 cite it and both bind the frozen
layer, so deleting it would strip the source from two accepted decisions.

**4. Withdraw ADR 0002 and ADR 0028 rather than delete them.** `docs/adr/README.md` states
twice that no ADR file is ever deleted. ADR 0028 draws every numbered claim from
`docs/method/exploration/`, so its numbers are inlined before withdrawal and stay checkable
against the archive. ADR 0002 is the recorded source of two entries in the frozen manifest's
baseline list, and that provenance is written into the withdrawal.

**5. The C1 contract stops naming packages that do not exist.** The rule "nothing in
`network/`, `classical/` or `quantum/` imports `allo.scoring`" passed after those packages
were deleted, because an empty set satisfies it. The rule now names the prediction path
itself, and `test_the_prediction_path_is_the_set_this_contract_names` pins that set, so
restoring a prediction package has to be argued for rather than merely committed.

## Consequences

- `main` holds the frozen benchmark, the frozen evaluation protocol, the evidence behind
  both, and the nine controls the protocol requires. It holds no candidate method.
- Challenge deliverable 1, the N x N connectivity matrix, returns to **not built**.
  `allo.quantum.connectivity.connectivity_matrix` was the only implementation.
  `docs/report/conformance.md` records the regression rather than hiding it.
- The prediction path is now `allo.structure` and `allo.inputs`. It was six packages.
- Roughly sixteen findings in `docs/benchmark/review/` have a deleted file as their subject.
  Each affected document carries a banner naming the branch the subject survives on. An
  audit that cannot be re-run is still a record. An audit that silently cites missing files
  is not.
- Phase 2 restarts from an empty method package against a frozen substrate, which is the
  order ADR 0020 and ADR 0021 both require.

## Alternatives rejected

**Delete the baselines too, and amend the manifest.** Rejected. It reopens the frozen
evaluation protocol to solve a filing problem. The protocol has been reopened twice already,
once by its own audit and once by the organisers' answers, and each reopening costs a
version and a re-derivation. Nothing about the baselines themselves was found wrong.

**Delete the baselines and leave the manifest as it is.** Rejected. That is the state this
ADR exists to escape: a frozen document mandating something no code can produce.

**Delete the method layer without archiving it.** Rejected. It had never been committed
anywhere. The cost of a branch is one commit, against the permanent loss of nine experiment
runs, roughly 6,700 scored records and twenty-three cited reviews.

**Keep everything and separate by directory only.** Rejected on the stated reason for the
work: the boundary was already a directory boundary, and it did not stop method work in
progress from making the frozen layer's status unreadable.
