# 0008 — One benchmark target per allosteric site

**Status:** accepted · 2026-08-20

## Context

Cardiac myosin forced the question. Three clinically relevant modulators bind it, but
they occupy **two** pockets, not three: mavacamten and omecamtiv mecarbil share one site
(centroids 2.0–2.4 Å apart), while aficamten and blebbistatin occupy a second site
34.2 Å away. Both are validated allosteric sites of the same protein.

A benchmark keyed on the _protein_ has three bad options: pick one site and silently
discard a validated answer; merge both label sets into one ground truth; or exclude the
protein. Merging is the tempting one and the worst one. The scored artifact is a **top-5
ranked residue list per target** (`CHALLENGE.md` line 97) evaluated by precision@5. With
a merged label set, a method that finds Site 1 perfectly and never sees Site 2 scores
identically to one that half-finds both — and the hypergeometric baseline is computed
against a prevalence that describes neither site.

The same situation is latent elsewhere. Any protein with two characterised allosteric
pockets hits it, and the ASD secondary benchmark will supply more of them.

## Decision

**One benchmark target = one protein plus one allosteric site.** A protein with two
validated allosteric sites contributes two targets.

- The two targets **share the apo input** — same structure, same chain, same residue set,
  same active site. They differ only in the holo member and therefore the label set.
- The target `id` names the site, not just the protein, so a results table cannot
  ambiguously reference "the myosin target".
- Whether to _include_ a second site is a separate decision per protein, taken on the
  evidence for that site. This ADR fixes only the granularity.

## Consequences

- The myosin question becomes an **addition** question rather than a choice question:
  adding Site 2 does not displace Site 1, so the two can be judged on their own merits.
- **Targets sharing an apo are not independent replicates.** Aggregate statistics must
  not treat them as such — no pooling across arms that share an input structure as if
  they were separate draws. The Holm correction remains valid (it holds under arbitrary
  dependence), but any variance estimate that assumes independence does not.
- Per-target prevalence, `n_residues` and the hypergeometric baseline stay meaningful,
  because each is computed against one site's label set.
- A method is scored twice on the same input structure. That is correct — it is being
  asked two different questions about it — but the report must say so, or a reader will
  read two myosin rows as two proteins' worth of evidence.
- Cost: the arm count grows with the number of sites rather than the number of proteins,
  and the smallest benchmark that covers the challenge's three diseases is no longer
  three arms. Accepted; the alternative is a ground truth that cannot be scored honestly.
