# The organisers' reply, and what each answer forces

**Received:** relayed to the repository on 2026-09-02.
**Status of this page:** the verbatim record. It states what was asked, what was answered,
and what the answer changes. It decides nothing on its own — each consequence is argued in
the numbered file beside it.

The reply is the highest authority available on the four questions below. It outranks
`CHALLENGE.md` where the two disagree, because it is the organisers correcting their own
document. It does **not** outrank a measurement: where the reply is a suggestion
("I would suggest", "you may"), the repository still has to show its choice is defensible.

---

## Q1 — Cardiac myosin validation structure

**Asked.** `6C1H` is an actin-bound unconventional myosin-Ib complex from rabbit/rat, not
human beta-cardiac myosin (MYH7). It contains neither MYH7 nor mavacamten. The mavacamten
site cannot be derived from this entry as specified. `9GZ2` is a 2.9 A human MYH7-mavacamten
complex. `8QYR` and `9GZ1` are alternatives. May teams substitute? Will one replacement be
designated for all teams, to preserve scoring parity?

**Answered.**

> To better represent the human MYH7-mavacamten complex for this challenge, you may
> substitute 9GZ2 for 6C1H. Please always document the substitution you make and explain
> rational of why you did it.

**What it forces.**

1. The challenge's factual error at `6C1H` is confirmed by the organisers.
2. `9GZ2` is the sanctioned holo. The repository already froze `9GZ2` as the holo of
   `cardiac_myosin_corrected`, so no label set moves.
3. No replacement is designated for all teams. Scoring parity is not guaranteed. Each team
   documents its own substitution.
4. The final sentence is general, not myosin-only: **document every substitution and give the
   reason.** The repository's apo substitutions (`4LDJ`, `2G2H`, `9GZ3`) fall under it and are
   now sanctioned procedure rather than unilateral repair, provided each is documented.
5. The reply supplies a holo. It supplies **no apo**. `5TBY` is unchanged, so the input-side
   blocker in ADR 0016 is untouched by this answer. See `02-cardiac-myosin.md`.

---

## Q2 — BCR-ABL1 apo input

**Asked.** `1OPL` chain A already contains myristate in the myristoyl pocket and the ATP-site
inhibitor PD180970. Chain B lacks myristate but still contains the ATP-site inhibitor. This
creates unequal starting conditions unless ligand stripping and chain selection are
standardised. Should ligands be stripped uniformly, and should chain A or chain B be the
designated input?

**Answered.**

> The challenge guidelines specify that the "unbound (apo) PDB structure serves as the input".
> Additionally, the challenge scope explicitly excludes "co-factors, and complex
> post-translational modifications (unless modeled as simple nodes)". To ensure equal starting
> conditions, all non-protein residues and ligands must be uniformly stripped. I would suggest
> teams use Chain B as the input, as its native lack of myristate best fulfills the requirement
> to use the unbound apo structure.

**What it forces.**

1. **Chain B, not chain A.** The frozen `bcr_abl1_mandated` arm uses `1OPL:A`. That is now
   contrary to the organisers' guidance and must change or be argued against in writing.
2. Ligand stripping is required and uniform. The repository already strips: `apo_input`
   returns a ligand-free single-chain view.
3. The reply confirms the repository's own audit finding — chain A is holo at the site it is
   asked to predict — from the organisers' side.
4. **An unresolved tension.** "All non-protein residues and ligands must be uniformly
   stripped" is a statement about the *input*. Two frozen arms derive their propagation source
   from the apo entry's own cofactor (`{from_ligands: [GDP, MG]}`,
   `{from_ligands: [ADP, MG, PO4]}`). Stripping the ligand from the node set is not the same
   as refusing to use its position to locate the active site, but the two readings differ and
   the reply does not separate them. See `01-bcr-abl1-chain.md` section 5.

---

## Q3 — KRAS switch-II label

**Asked.** The switch-II label overlaps the nucleotide-site source set at five residues
(A11, C12, G13, K16, P34). Those residues are at graph distance zero from the source, which
makes a distal-connectivity score ambiguous and may give trivial credit. Should they be
included? Should source-set residues be excluded from scoring? Should KRAS be reported
separately from the genuinely distal targets?

**Answered.**

> The primary objective of the challenge requires participants to evaluate "distal regulatory
> residues" based on their dynamic connectivity to an active site. Residues that overlap with
> the source set (A11, C12, G13, K16, and P34) are not distal and would result in trivial
> zero-distance credit. Thus, they must be excluded from the switch-II target label during
> scoring. KRAS G12C remains a required target, but these overlapping residues will be masked.

**What it forces.**

1. **The exclusion is mandatory, not optional.** "They must be excluded ... will be masked."
2. The five residues named are exactly the five the frozen benchmark already removes.
   `scoreable_label_residues` is 16 of 21 on both KRAS arms, and the removed five are
   11, 12, 13, 16 and 34. Clause (vii) is ratified by the organisers.
3. KRAS stays a required target. The third sub-question — report KRAS separately — was **not
   answered**. The repository's own reporting already separates arms by proximity axis, so
   nothing is blocked.
4. The organisers' reason ("not distal ... trivial zero-distance credit") is a **distance**
   argument. Clause (vii) is a **membership** argument. The two agree on this label set and do
   not agree in general. See `03-kras-mask.md`.

---

## Q4 — Enrichment over non-functional surface pockets

**Asked.** Is a specific pocket-detection method or decoy set expected, so that negative
examples are comparable across teams?

**Answered.**

> The challenge objective requires algorithms to distinguish allosteric sites from "random
> background residues and non-functional surface pockets". Teams are responsible for
> generating their own negative examples and defining their decoy sets. And of course, their
> approach to this must be clearly documented in their submission.

**What it forces.**

1. No prescribed detector. The repository's pyKVFinder 0.9.3 choice is admissible and its
   full configuration is already frozen and documented (ADR 0024).
2. Cross-team comparability of negative class (b) is **not** guaranteed by the organisers. A
   number quoted against our decoys is not comparable to another team's.
3. **The decoy set is ours to design.** The frozen set floors the attainable p at 0.25 on two
   of three confirmatory arms, so negative class (b) cannot reject there at any effect size.
   The organisers' answer removes the reason to treat that floor as fixed. See
   `04-decoys-and-power.md`.
