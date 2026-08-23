# Allosteric site discovery

The domain language of this repo. One entry per term whose meaning has been argued
about and settled. Definitions only — no procedures, no file paths, no numbers that
belong in `docs/benchmark/frozen.json`.

Terms enter here when a decision fixes them, not when they are first used. Where two
words circulate for one concept, the preferred one is the heading and the rest sit
under `_Avoid_`.

## Language

### The thing we predict

**Allosteric site**:
A site on a protein, distinct from the active site, where an effector binds and thereby
changes activity at the active site. Allostery is a **functional coupling between two
sites**, so a site is allosteric _for a given function_ — never in isolation. This is
the ground-truth concept of the benchmark (ADR 0007).
_Avoid_: cryptic site, hidden pocket, hotspot — none is a synonym.

**Cryptic site**:
A pocket that is absent in the unbound structure and forms on binding. A purely
**structural** property of an apo/holo pair, orthogonal to allostery: fewer than half of
validated **high-affinity** cryptic sites are allosteric (Vajda 2018, 8 of 19), and
allosteric sites are frequently pre-formed — the second half resting on ESSA's 7/14 and
APOP's 11/14 top-3 successes on true apo structures, **not** on Vajda, whose next sentence
says allosteric modulators "frequently bind at flexible regions without pre-formed pockets".
Reported here as a difficulty axis — never as a validity test for a pair.
_Avoid_: using interchangeably with "allosteric site".

**Drug-binding site**:
The residues lining a ligand observed in a deposited structure. This is what geometry
alone yields. It is an **observation**, not a claim about function: a drug-binding site
becomes an allosteric site only by cited functional experiment.
_Avoid_: pocket (ambiguous), binding pocket.

**Active site**:
The catalytic site whose activity the allosteric site modulates, and the source term of
signal propagation. Defined per target by a _rule_ over the apo structure, never a
written-down residue list (ADR 0005).
_Avoid_: orthosteric site (correct in the literature, but we reserve "active site" for
the propagation source so the two never drift apart), catalytic pocket.

**Effector**:
The molecule that binds the allosteric site and changes activity. May inhibit or
activate — one pocket can do both, which is itself evidence the site is allosteric.
_Avoid_: drug, ligand, inhibitor (each presumes a direction or an origin).

### The benchmark

**Apo/holo pair**:
Two experimentally determined structures of the same gene product where the _holo_
member contains the effector at the site to be predicted and the _apo_ member contains
nothing at that site. Site-relative, not structure-global: cofactors elsewhere are
permitted and recorded.
_Avoid_: bound/unbound pair, complex/free pair.

**Site-apo**:
Apo _with respect to a named site_, as opposed to globally ligand-free. This repo's
coinage; the field has no agreed term for it, so it is glossed at first use in any
external writing.

**Label set**:
The residues constituting a target's ground truth. Derived from the holo structure by a
fixed geometric rule, then carried onto the apo numbering by sequence alignment.
_Avoid_: ground truth (use for the concept, not the residue list), positives, true site.

**Scoreable label set**:
A label set minus the labels that are themselves propagation-source residues. A
**circularity guard for the metric**, not a claim that the excluded residues are
non-allosteric: a label inside the source set scores maximally by construction and so
measures nothing. The rule is **set membership, not distance** — no minimum separation
convention exists in the allostery literature (AlloPred, doi:10.1186/s12859-015-0771-1).
This is the **positive class** of the primary endpoint, and the frozen key is
`scoreable_label_residues`. The negative class is the *candidate set*, below — not the rest
of the chain.
_Avoid_: **distal label set** (this repo's earlier name for it, withdrawn — it invited a
distance reading of what is a membership rule), "the real allosteric residues", "distal
regulatory residues" as a derived set.

**Candidate set**:
The **scoring universe**: every node minus the residues that score by construction rather
than by evidence — the propagation source. The same argument that removes a source residue
from the positives removes it from the negatives; leaving it in the negatives penalises
connectivity methods and no other class (ADR 0011). Frozen as `n_candidates` /
`excluded_from_scoring`. **Not** the node set: a method still receives the whole chain, so `N`
(what it sees) and `n_candidates` (what it is scored against) are two numbers and must not be
swapped.
_Avoid_: "background", "the negatives" for the whole chain, using `n_residues` as a
denominator for prevalence or a chance line.

**Target**:
One benchmark instance = one protein **plus one allosteric site**. The scored artifact is a
ranked residue list per target, so a protein with two validated allosteric sites would
contribute two. Every protein in the current benchmark carries one (ADR 0008, withdrawn).
_Avoid_: protein, system, case.

**Tier**:
Which claim an arm supports. `mandated` is the pair the challenge specifies, defects and all,
reported because the challenge requires it. `corrected` is the defensible pair for the same
protein and the same site, and is where methods are compared. There is no third tier: a
robustness arm varies one thing to test whether a conclusion survives, and a conclusion has to
exist first, so those belong to the method phase (ADR 0003, amended).

**Frozen input layer**:
The fixed set of structures, chains, residues and active sites every method receives.
Fixed before any method exists, so that a difference between two methods is a difference
between the methods.
_Avoid_: dataset, test set (the evaluation layer is separate and frozen separately).

**Primary benchmark**:
The three challenge-specified disease targets. **Secondary benchmark**: additional
targets with known allosteric sites, drawn from the Allosteric Database, used for
hyperparameter selection and for generalisability. **Stretch target**: c-Myc, which has
no characterised allosteric site and therefore no ground truth.
