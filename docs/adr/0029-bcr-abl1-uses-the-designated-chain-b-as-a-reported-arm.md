# 0029 — BCR-ABL1 uses the organisers' chain B as a reported arm, and 2G2H stays the comparison arm

**Status:** accepted · 2026-09-02 · changes the `bcr_abl1_mandated` arm frozen on 2026-08-24

## Context

The organisers answered a question about `1OPL` on 2026-09-02
([`../benchmark/review/00-official-reply.md`](../benchmark/review/00-official-reply.md) Q2):

> "To ensure equal starting conditions, all non-protein residues and ligands must be
> uniformly stripped. I would suggest teams use Chain B as the input, as its native lack of
> myristate best fulfills the requirement to use the unbound apo structure."

The frozen `bcr_abl1_mandated` arm uses `1OPL:A`. That is contrary to the guidance.

The reply is a suggestion, not a rule. The repository still has to show that its choice is
defensible. Both chains were therefore measured from the deposited file
([`../benchmark/review/01-bcr-abl1-chain.md`](../benchmark/review/01-bcr-abl1-chain.md)).

| Property                 | `1OPL:A` (frozen)                            | `1OPL:B` (organisers)                    | `2G2H:A` (comparison) |
| ------------------------ | -------------------------------------------- | ---------------------------------------- | --------------------- |
| myristoyl pocket empty   | **no** — 16 of 20 labels contacted at 3.29 Å | yes — nearest 16.0 Å                     | yes                   |
| SH3–SH2 clamp            | docked on the C-lobe                         | **absent** — no SH3, SH2 on the N-lobe   | absent                |
| Cα RMSD to holo `5MO4:A` | 0.98 Å                                       | **22.89 Å**                              | 1.78 Å                |
| coordinates              | individual B-factors, 3041 distinct values   | **rigid-body placed, 3 group B-factors** | individual, 2.00 Å    |
| labels modelled          | 20 of 20                                     | 17 of 20                                 | 18 of 20              |

The coordinate row is the depositors' own statement, in `_refine.details` of the deposited
file: "only overall domain B-factors were applied to molecule B, whereas individual B-factors
were refined for molecule A". Under C6 the contact topology is the object the method rests
on. Chain B's residue contacts are therefore properties of `1OPK`'s geometry plus a domain
placement, not of a refinement against chain B's own density.

**One row must be read with its decomposition, and an independent re-derivation supplied it**
([`../benchmark/review/15-blocking-measurement-recheck.md`](../benchmark/review/15-blocking-measurement-recheck.md)).
The 22.89 Å is **entirely the regulatory module**. Over the same 239 Cα of the kinase domain
alone, chain B fits the holo kinase domain at **1.08 Å** against chain A's **1.00 Å**. Quoting
22.89 Å without that sentence overstates the case against chain B, and the real case — three
group B-factors, no SH3, SH2 on the N-lobe — reproduces exactly and does not need it.

**One number in the audit does not reproduce and is not used here.** `01-bcr-abl1-chain.md`
§3.2 gives four SH2-to-lobe centroid distances without stating where it split the N-lobe from
the C-lobe, and no canonical kinase lobe boundary reproduces them. The **conclusion** is robust:
under every boundary from residue 320 to 355 the inversion holds and is large — chain A nearer
the C-lobe by 5–9 Å, chain B nearer the N-lobe by 20–23 Å — and the convention-free interface
residue counts reproduce exactly, 11 of 11. This ADR therefore rests on the interface counts
and not on the centroid distances.

Neither chain is clean, and the trade is not symmetric. Chain A fails clause (iii) of the
pair definition: it is holo at the site it is asked to predict. Chain B passes clause (iii)
and loses the mechanism instead.

**One finding outranks the trade.** An exhaustive RCSB survey of every entry that models more
than the ABL kinase domain returns six entries. Every entry with the SH3–SH2 clamp docked on
the C-lobe has the myristoyl pocket filled, five for five. Every entry with the pocket empty
has the SH2 domain on the N-lobe, two for two. **The clamp docks only when the pocket is
filled.** No myristate-free assembled ABL1 exists, and none is likely to, because the
assembled state is what myristate binding causes.

## Decision

**Report `1OPL:B` as the `bcr_abl1_mandated` arm, and mark it non-confirmatory.** The
organisers designated it. Print all four measured defects beside every number it produces:
no SH3 modelled, SH2 on the N-lobe, 22.89 Å from the holo over all common residues — with the
kinase domain's own 1.08 Å beside it, so the number is not read as a bad kinase fit — and
three group B-factors.

**Keep `2G2H:A` as `bcr_abl1_corrected`, and keep it in the confirmatory family.** It is
where methods are compared. Nothing about it changes.

**Do not substitute `4XEY:B`.** It is better coordinates — 2.891 Å, individual B-factors,
wild-type sequence, 18 of 20 labels — for the same arrangement, which is 1.44 Å from
`1OPL:B` over 352 Cα. It is better coordinates for a state that is wrong either way.
Swapping an accession the organisers named for one they did not is the move that needs the
strongest reason, and better B-factors for the wrong conformation is not it.

**Do not argue against the organisers by keeping chain A.** Chain A fails the repository's
own clause (iii). Keeping it would mean defending, against the organisers' explicit
guidance, an apo structure that is holo at the target site.

## Consequences

- `bcr_abl1_mandated` moves from chain A to chain B in `primary/manifest.yaml`. The freeze is
  re-derived, so its node set, label set and candidate set all move. Three of the twenty
  labels are not modelled in chain B and are reported as unmapped, against zero in chain A.
- The confirmatory family is unchanged. `bcr_abl1_mandated` was already `supportive_only`.
- The arm now satisfies clause (iii), which no BCR-ABL1 mandated arm did before. The
  benchmark gains one arm whose apo member is genuinely empty at the site.
- **The cost is that the arm's contact graph is largely a domain placement.** A method scored
  on it is measured partly against the depositors' rigid-body fit. That is disclosed, not
  repaired, and it is why the arm is non-confirmatory.
- **A scope statement enters the report.** For an allosteric site that works by a
  conformational switch, no apo structure carries the coupled conformation, because carrying
  it is what binding causes. Any apo-input benchmark on a switch-type site inherits this. It
  belongs in `docs/report/` as a scope statement, not as a caveat on one arm.
- `docs/targets.md` and `primary/audit/bcr-abl1.md` gain the chain B dossier.

## Alternatives rejected

**Keep chain A and argue against the organisers.** Rejected: the measurement that would
support the argument — chain B's coordinate quality — does not repair chain A's clause (iii)
failure. The repository would be defending a structure its own definition rejects.

**Report both chains as two arms.** Rejected: one disease area would then contribute three
arms, and the two mandated arms would share every property except the defect under test. The
comparison that adds information is chain B against `2G2H:A`, and that comparison already
exists.
