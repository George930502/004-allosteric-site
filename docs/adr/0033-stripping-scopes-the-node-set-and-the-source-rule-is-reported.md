# 0033 — "Uniformly stripped" scopes the node set, and the source rule is reported per arm

**Status:** accepted · 2026-09-02 · reading of the organisers' Q2 answer · adds one
sensitivity arm

## Context

The organisers wrote, answering a question about `1OPL`:

> "To ensure equal starting conditions, all non-protein residues and ligands must be uniformly
> stripped."

The repository already complies with the plain reading. `allo.inputs.apo_input` returns a
ligand-free, single-chain, immutable view holding exactly the frozen node set. No method ever
sees `MYR`, `P16`, `GDP` or `ADP`. No ligand is a node and no ligand is an edge.

**The sentence does not say whether a stripped ligand may still locate the active site.**
`CHALLENGE.md` §4.1 requires a ranking by "dynamic connectivity ... to an active site", so the
active site has to be locatable somehow. The repository locates it two ways, and the split is
almost exactly even
([`../benchmark/review/10-cross-set-consistency.md`](../benchmark/review/10-cross-set-consistency.md) §4):

| `{from_ligands: ...}` — 7 arms            | `{from_motifs: ...}` — 7 arms         |
| ----------------------------------------- | ------------------------------------- |
| `kras_g12c_mandated` (GDP, MG)            | `bcr_abl1_mandated` (VAIK, HRD, DFG)  |
| `kras_g12c_corrected` (GDP, MG)           | `bcr_abl1_corrected` (VAIK, HRD, DFG) |
| `cardiac_myosin_corrected` (ADP, MG, PO4) | `mkp5` (PTP)                          |
| `smyd3` (SAM)                             | `chk1` (VAIK, HRD, DFG)               |
| `glucokinase` (GLC)                       | `ptp1b` (PTP)                         |
| `p97_vcp` (ADP)                           | `hiv_rt` (POLA, YXDD)                 |
| `ecoli_cps` (ADP, MN, PO4)                | `ns5b` (GDD)                          |

Two readings are defensible.

- **Narrow.** "Stripped" scopes the node set. Locating the active site is a separate step and
  the challenge requires it. Nothing changes.
- **Wide.** "Stripped" scopes every use of the coordinates. Half the benchmark then needs a
  new source rule.

The split cuts across both sets and both tiers, so no partial fix exists.

**Note what a ligand-derived source is and is not.** It is not holo information. The cofactor
sits in the **apo** entry, which is the input the challenge names. C1 forbids holo-derived
information on the prediction path, and a cofactor present in the apo file is not that. The
question here is the organisers' wording, not C1.

## Decision

**Adopt the narrow reading.** "Stripped" scopes the node set, which is what "equal starting
conditions" is about: the myristate in `1OPL:A` changes the graph, and a GDP that is used once
to name a residue set does not.

**Report the source rule for every arm in the submission**, as a column beside every result,
so a reader can see which arms used a cofactor position and which used a sequence motif.

**Run a motif-only sensitivity comparison on KRAS, and report the difference.** KRAS's P-loop
is a single unique PROSITE PS00016 match at residues 10–17. Re-derived here on both KRAS apo
entries: one match, residues 10–17, on `4OBE:A` and on `4LDJ:A`. This converts the ambiguity
into a measurement instead of an argument.

**One measurement changes the design, and the audit did not have it.** The audit reported that
the motif span sits "inside the frozen ligand-derived source of 22–23 residues". It does not.
Seven of the eight are inside. **Residue 10 is not a source residue under the frozen rule — it
is a scoreable label.** `kras_g12c_corrected` has `scoreable_label_residues` beginning
`[9, 10, 58, ...]`.

So a motif-only source is not a drop-in substitution. Under clause (vii) it would move residue
10 out of the positive class, taking the scoreable label set from 16 to 15 and changing what is
being scored. The two source rules would then produce numbers on different positive classes.

**Therefore: no new frozen arm.** Run the comparison as a descriptive re-score that holds
everything except the source fixed, and score both on the **intersection** positive class of
15 residues, so the comparison is like-for-like:

| run       | source rule                 | positive class         | status                         |
| --------- | --------------------------- | ---------------------- | ------------------------------ |
| frozen    | `{from_ligands: [GDP, MG]}` | 16 scoreable labels    | the official number, unchanged |
| matched A | `{from_ligands: [GDP, MG]}` | 15, residue 10 removed | descriptive                    |
| matched B | `{from_motifs: [PLOOP]}`    | 15, residue 10 removed | descriptive                    |

Matched A against matched B is the answer to the question. The frozen number is reported as it
stands and nothing about it moves.

**Do not change any frozen source rule.** The sensitivity runs sit beside the frozen arms,
never in place of one.

## Consequences

- **No arm is added and no freeze moves.** `primary/frozen.json` and `evaluation/frozen.json`
  keep fourteen arms.
- `PS00016` enters `CATALYTIC_MOTIFS` as `PLOOP`, with its uniqueness on both KRAS apo entries
  pinned by a test. On MYH7 it matches **twice**, which is why ADR 0031 uses a family triple
  there and not this one.
- The confirmatory family is unchanged.
- The submission carries a source-rule column and one sentence saying which reading was taken
  and why.
- **The audit's statement that the motif span is inside the frozen source is corrected here.**
  It is off by one residue, and that residue is a label, which is the difference between a
  free sensitivity run and a change to the positive class.
- **If the organisers later state the wide reading, six of the seven ligand-derived arms still
  need work.** The KRAS measurement will already exist, so the cost of the answer is known
  rather than guessed. That is the point of running it now.
- The question can also simply be asked. It is listed as an open item, not as a settled fact
  about the organisers' intent.

## Alternatives rejected

**Adopt the wide reading now, and convert all seven arms.** Rejected: it re-derives half the
frozen benchmark on a reading of one sentence that the sentence does not carry, and it would
replace measured cofactor positions with motif approximations that agree at Jaccard 0.5 on the
one arm where both exist.

**Add `kras_g12c_corrected_motif_source` as a sixth primary arm.** Rejected on the measurement
above: the motif source moves one residue out of the positive class, so the new arm would not
be scoring the same thing. A fifteen-residue matched comparison answers the question without
touching a freeze. The repository also deleted a `sensitivity` tier on 2026-08-24 for adding
arms in answer to audit findings; this is the same instinct.

**Say nothing and keep the frozen rules.** Rejected: the divergence is real, a reviewer will
find it, and the cheap measurement that bounds it costs one run.
