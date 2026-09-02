# 0045 — The alternate-conformer policy is stated rather than chosen, and the two paths that disagree are pinned

**Status:** accepted · 2026-09-03 · closes the round-6 contract audit's altloc finding · no
re-freeze, no protocol version change

## Context

Four apo entries in the frozen sets model alternate conformations. Nothing in the repository
says what to do with them, and three code paths answered the question three different ways by
accident.

| arm           | altloc atoms | residues | CA has an altloc |
| ------------- | -----------: | -------: | ---------------: |
| `smyd3`       |          168 |       15 |               15 |
| `ecoli_cps`   |           66 |        7 |                0 |
| `glucokinase` |           40 |        3 |                3 |
| `ptp1b`       |            6 |        1 |                0 |

At least one holo entry carries them too: `mkp5`'s transplant distance moves when the apo-side
rule changes, and the transplant reads both members.

The three answers, none of them written down:

1. **`allo.scoring.nulls.evaluation_graph`** builds `ca_by_residue` with a dict comprehension,
   so the **last** conformer in file order wins.
2. **`allo.benchmark._chain_ca`** builds its map with `setdefault`, so the **first** wins.
3. **The contact graph and the solvent-accessibility integration** consult no altloc field at
   all, so **every** conformer contributes atoms. A residue with two conformers therefore
   occludes itself, and an edge can exist through a minor conformer alone.

The repository had already asked this question once, on the other side of the boundary. The
label sets were checked against a primary-conformer mask — `[".", "?", "", "A"]` — and no
frozen label was found to depend on a minor conformer. **The graph was never checked, and
neither was the CA.**

## What the evidence says

Measured on 2026-09-03, on the frozen inputs, with `allo` at `db752ff`.

**The two CA maps disagree.** Not on whether a residue has a CA, but on which one:

| arm           | residues where the two disagree | largest disagreement |
| ------------- | ------------------------------: | -------------------: |
| `smyd3`       |                              15 |             0.1003 A |
| `glucokinase` |                               3 |             0.0496 A |
| `ptp1b`       |                               0 |                    — |
| `ecoli_cps`   |                               0 |                    — |

**Counting every conformer only adds edges, never removes them.** Against a primary-conformer
build, on the same node set and with the node order unchanged on all four arms:

| arm           | directed edges present only when alternates count | of total | share      |
| ------------- | ------------------------------------------------: | -------: | ---------- |
| `smyd3`       |                                                14 |     4178 | **0.335 %** |
| `glucokinase` |                                                 2 |        — | —          |
| `ecoli_cps`   |                                                 2 |        — | —          |
| `ptp1b`       |                                                 0 |        — | —          |

Zero edges go the other way on any arm, which is what the geometry predicts: a union of
conformers can only bring atom pairs closer.

**Solvent accessibility moves further than either.** A residue modelled twice is occluded by
its own second copy, so its RSA is deflated:

| arm           | residues whose RSA moves | largest move |
| ------------- | -----------------------: | -----------: |
| `smyd3`       |                       56 |       0.1921 |
| `ecoli_cps`   |                       22 |       0.1572 |
| `glucokinase` |                       12 |       0.2130 |
| `ptp1b`       |                        2 |       0.0933 |

**Making the two CA maps agree moves three frozen values, all at the rounding digit.** Flipping
`_chain_ca` to the `evaluation_graph` rule and re-deriving:

```
targets.glucokinase.transplant_min_distance: frozen 2.65 != current 2.66
targets.mkp5.transplant_min_distance:        frozen 0.65 != current 0.64
targets.smyd3.apo_holo_rmsd.pocket_lining:   frozen 0.31 != current 0.3
```

The primary set does not move at all. No verdict moves: the clash count that carries the 2.5
angstrom threshold is unchanged on every arm, and no admission clause reads any of the three.

## Decision

**1. The policy in force is stated, not changed.** Every modelled conformer contributes atoms
to the contact graph and to the solvent-accessibility integration, and the CA that reaches the
evaluation graph is the last one in file order. That is what the frozen numbers were computed
under, and it is now written where a reader will find it.

**2. It is not the policy this repository would choose today, and that is recorded here rather
than acted on.** The better rule is the primary conformer, on two arguments. Occupancy is
ignored, so a conformer refined at 0.2 occupancy contributes exactly as much as one at 0.8.
And "last in file order" is a property of the deposition, not of the protein. The
repository's own label-side check already used a primary-conformer mask, so the two sides of
the boundary do not currently agree on what a conformer is.

**3. The change is not made now, and the reason is arithmetic rather than schedule.** Adopting
the primary-conformer rule moves the evaluation graph, so it is a protocol version 5 and a
re-freeze of both input layers and the evaluation layer. Against that: the effect is 0.335 %
of edges on the worst of fifteen arms, at most 0.1 angstrom of CA, and — the part that decides
it — **identical for every method**, because the graph is frozen and every method receives the
same one. A frozen input that is uniformly slightly wrong biases no comparison. A re-freeze
performed at the end of an audit round, to move three diagnostics by 0.01 angstrom, carries
more risk of moving something that matters.

**4. Both CA paths are pinned by a test, at the values they have.** The defect worth closing
today is not the policy; it is that two functions computed "the CA of residue r" and got
different answers with nothing to notice. `test_the_altloc_policy_is_the_one_this_adr_states`
re-derives every number in the tables above and fails if any drifts, so the disagreement cannot
widen, and cannot silently disappear either.

## Consequences

- **No number moves, and no freeze is rebuilt.** All three verifiers re-derive their freezes
  unchanged at this commit.
- **Any figure that quotes an RSA on `smyd3`, `ecoli_cps`, `glucokinase` or `ptp1b` carries
  this caveat.** RSA is the confounder column most affected, by up to 0.213, and it is
  reported beside every result (ADR 0025).
- **What would reopen this.** A method whose score depends on a single edge, or a result whose
  margin is inside 0.335 % of the edge set. Either makes the primary-conformer rule worth a
  protocol version 5. Neither is true of any result on `main` today, because no method has been
  scored on `main` since ADR 0037 removed the method layer.
- **The `_chain_ca` map is also used on holo structures**, in the transplant and the apo/holo
  RMSD. The policy stated here therefore applies to the ground-truth side as well, which is
  where `mkp5` enters the table above despite having no apo altloc.
