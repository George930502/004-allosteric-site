# 0006 — Cofactors, and modified residues, as network nodes

**Status:** accepted · 2026-08-20

## Context

`docs/targets.md` says of the KRAS nucleotide "kept as a simple node or dropped — see the
ADR", and the KRAS audit dossier recorded "Action required: decide and record
whether GDP and Mg2+ become simple nodes". No ADR covered it. This one does, because the
question is part of the input layer — it decides which nodes exist — and an input-layer
question has to be settled before any method runs or it becomes a knob.

Constraint C5 excludes "solvents, co-factors, and complex post-translational modifications
— _unless modelled as simple nodes_". So the challenge permits either treatment and
requires neither. The frozen apo entries are not cofactor-free: KRAS holds GDP·Mg, the
myosin entries hold ADP·Mg·Pi or ADP·Mg·vanadate, `2G1T` holds Mg, `1OPL` and `2G2H` hold
an ATP-site inhibitor (`docs/benchmark/primary/frozen.json`, `apo_site_occupancy`). The `8QYP` apo
additionally carries trimethyl-lysine (`M3L`) at 129 and 549 where its holo `8QYR` does not
— the pair members disagree about the chemistry at two positions, neither of them a label.

The physics cuts both ways. A bound nucleotide is a real mechanical bridge: it contacts the
P-loop, both switch regions and the metal, and deleting it removes coupling that exists in
the crystal we are reading coordinates from. Against that, the elastic network hypothesis
(C6) is a statement about the _protein_ contact topology, GNM/ANM as normally practised is
protein-only, and every classical baseline we must compare against is defined that way.

## Decision

1. **Default: cofactors, metals, ions and small-molecule ligands are not nodes.** The
   network is the protein chain only. This keeps the quantum method and every classical
   baseline on _the same graph_, which is the entire purpose of freezing the input layer —
   a comparison where one method sees an extra node is not a comparison of methods.
2. **The cofactor-as-node treatment is pre-registered here as a declared ablation**, not
   left available as a knob. If it is run, it is run on all targets, reported alongside the
   default, and the default remains the headline. Selecting between them by which enriches
   better is test-set fitting (`docs/playbooks/constraint-audit.md`).
3. **Modified residues stay polymer nodes and are mapped to their parent amino acid.**
   `M3L` → Lys, `MSE` → Met, and so on. Membership is decided by `label_seq_id`, never by
   the ATOM/HETATM flag (`src/allo/structure/pdb.py`). A trimethyl-lysine is a lysine in
   the chain; dropping it would renumber the chain and break the alignment that carries
   labels across (ADR 0004). Parent mapping applies to topology as well as the one-letter
   sequence: before prediction, `M3L` is renamed `LYS` and PTM-only atoms `CM1`, `CM2` and
   `CM3` are removed. Heavy-atom contact edges therefore come from the parent lysine atom set,
   not the trimethyl group. Modified node properties are not modelled.

   **"and so on" overstates the implementation, and an adversarial review was right to say so
   (2026-08-21).** `_THREE_TO_ONE` maps `MSE`, `SEP`, `TPO` and `PTR` for *sequence* purposes,
   but `allo.inputs._prediction_structure` performs the *topology* mapping for `M3L` alone.
   Selenomethionine would keep its `SE` atom and a phosphoresidue its phosphate, so their
   contact edges would not be the parent's.

   **CORRECTED 2026-09-03 by the round-6 audit. The claim that followed here was wrong on
   both halves, and it stood for thirteen days.** It said `M3L` is the only modified residue
   in any frozen node set, and it named a test that fails the moment that stops being true.
   The test it named does not exist. The test that did exist,
   `test_modified_residues_are_parent_normalized_before_prediction`, asserted two `M3L`
   residues on one arm **by number**, so it could never have seen a different modification on
   a different arm, and it left the suite with that arm in `0f1fe3f`. Meanwhile `hiv_rt`
   entered the secondary set carrying `CSD`, oxidised cysteine, at 280 — on exactly the
   untested path this clause promised was closed. It kept its two sulfinyl oxygens, and in
   `allo.structure.properties` it took the hydropathy fallback (0.0, where cysteine is 2.5)
   and the RSA denominator fallback (200.0, where cysteine is 167.0), both silently.

   **Three things changed, and the order matters.** The topology mapping is now a table,
   `allo.inputs._PARENT_TOPOLOGY`, with `M3L` and `CSD` — two entries, because two modified
   residues occur across the fifteen frozen arms and the arm set is frozen. Both property
   tables now **raise** instead of substituting, because a fallback that is neither the
   measured value nor an error is the failure mode here: 0.0 sits between glycine and alanine
   and 200.0 between cysteine and arginine, so both print as plausible numbers.
   `tests/test_benchmark.py::test_no_modified_residue_reaches_a_prediction_structure` sweeps
   **every** arm and asks the general question, which is what this clause always described.

   **The graph does not move. One frozen decoy volume does, and the first version of this
   paragraph missed it.** Measured on `hiv_rt`: removing the two oxygens changes **zero** graph
   edges, so no null, no endpoint and no scored value moves. What moves is three reported
   confounder columns — RSA on four residues, by at most 0.045; hydropathy on one; and the
   chain's B-factor z-scores in the fourth decimal, because residue 280's mean B is now taken
   over six atoms rather than eight.

   **CORRECTED the same day.** This said "no frozen value moves, and all three verifiers
   re-derive their freezes unchanged". Those runs were `allo evaluate verify` **offline**,
   which skips the pocket detector by design, and the detector reads the atoms. Under
   `--detect` one decoy's cavity volume on `hiv_rt` moved, from 1727.57 to 1718.28 cubic
   angstrom, a drop of 0.54 %. **A verifier that skips a stage cannot certify that stage**,
   and the claim should have named the mode it ran in.

   The extent was then measured in full, and it is that one number. The detector finds 72
   pockets before and after, with the same identifiers; `n_scoreable`, the three halo
   exclusions and `minimum_attainable_p` are unchanged; and the site pocket keeps its
   identifier, its lining and its volume. The evaluation layer is re-frozen on that one value
   and **`protocol_version` stays at 4**, which is ADR 0044's precedent exactly: an
   input-layer correction that moves a derived value while changing no endpoint, null, decoy
   rule or decision does not open a protocol version. Nothing is invalidated by the re-freeze,
   because no method has been scored on `main` since ADR 0037 removed the method layer, and
   `hiv_rt` is a sealed `generalisation` arm in any case.
4. **The residue set the network is built on is `allo.inputs.apo_input(...).residues`**, and
   nothing else. It is the frozen `n_residues` count in `frozen.json`.

## Consequences

- **The approximation is stated, not hidden.** The nucleotide's conformational imprint stays
  in the coordinates while the nucleotide is absent from the graph. On KRAS this matters
  most: GDP·Mg contacts residues 11–18 and 28–36, which include the switch-II pocket rim.
  The report says so rather than letting "apo" imply "unliganded".
- The active site is still _derived_ from those cofactors where the apo entry holds them
  (ADR 0005). Using a ligand to locate the source is independent of putting it in the graph,
  and only the first is needed.
- `bcr_abl1_*` no longer depends on this: since the ABL1 arms moved to the catalytic-motif
  rule, no ABL1 source term is defined by a bound drug at all.
- Risk accepted: if propagation through the nucleotide turns out to be mechanistically
  important on KRAS, the default understates the signal. That is why the ablation is
  declared now — so running it later is a pre-registered check, not a rescue.
- **Accepted.** It was left proposed on the reasoning that reversing it before Phase 1.2
  costs nothing — but this ADR's own opening says an input-layer question "has to be settled
  before any method runs or it becomes a knob", and `docs/ROADMAP.md` declares the input
  layer closed. A reversible node-set decision is not a frozen input layer, and an
  adversarial review found the two statements contradicting each other. Accepting it is what
  makes the freeze true; the declared ablation is how the alternative still gets measured,
  as a pre-registered check rather than a rescue.
