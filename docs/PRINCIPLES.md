# Research principles — full statements

Standing instructions from the principal investigator, recorded 2026-08-19. `AGENTS.md`
carries R1–R4 as one-line imperatives because they bind every task; this file holds the
full statement of each, and is the authority if the two ever disagree.

Enforcement points are marked **[R1]**–**[R4]** in `docs/playbooks/phase-work.md` and
`docs/playbooks/experiment.md`. The field these principles are practised in is defined
in `docs/FIELD.md`.

---

Standing instructions from the principal investigator. They govern *how* the research
is conducted, in the same way the hard constraints govern what the result is allowed to be. They apply
to every task, not only to the ones that look scientific.

### R1 — First-principles thinking

Reason from the physics and the biology, not from what a similar repo did. Before
adopting any method, be able to state: what physical quantity it computes, what
assumption makes that quantity meaningful here, and what would make it break. If a
step exists only because it is conventional, it is not yet justified.

Practically: derive before you cite; when a paper's result is used, state the mechanism
in one sentence in your own terms. If you cannot, you do not yet understand it well
enough to build on it. "This is standard practice" is not a reason.

### R2 — Decompose into executable phases

Every unit of work reduces to phases with an **exit criterion that a command can
check**. Never start a task whose success condition is a feeling. If a task cannot be
decomposed that way, that is the finding — say so and reduce scope until it can be.

The project-level decomposition lives in `docs/ROADMAP.md`; the task-level version is
step 5 of `docs/playbooks/phase-work.md`. Both are load-bearing, not paperwork.

### R3 — Ground every claim in evidence

Four admissible kinds, in the order we prefer them when they conflict:

1. **Quantitative experimental results** produced in this repo, reproducible from a
   committed config (`experiments/`).
2. **Statistical analysis** of those results: effect size against a stated null model,
   with the test named. A ranking without a null is not evidence.
3. **Literature** with a DOI, read rather than recalled. Its claim is reported with its
   conditions — the protein class, the system size, the regime it was shown in.
4. **Observational / empirical** notes on structures and data — what the PDB file
   actually contains, what the network actually looks like. Recorded as observations,
   with the code path that produced them.

Not admissible as evidence: an LLM's recollection of a residue number, a plausible
mechanism nobody measured, or a number whose provenance cannot be named. When there is
no evidence yet, write "unknown" — an honest gap is cheaper than a confident guess that
someone later builds on.

### R4 — Work like a frontier researcher in this field

The field is defined explicitly in [`docs/FIELD.md`](docs/FIELD.md): protein allostery
and ensemble dynamics, elastic-network biophysics, and quantum transport on graphs,
applied to early-stage target validation. Read it before non-trivial work — it also
lists the known intellectual traps in this specific challenge, including the ones that
produce an impressive-looking but hollow submission.

Expert behaviour that is expected here: build the null model before the method; treat
the classical baselines as serious opponents rather than strawmen; distinguish pocket
from allosteric site from communication pathway; report in the units a medicinal
chemist uses; state the limits of a claim in the same breath as the claim.

Searching for best practice is encouraged — and it means finding what expert groups in
*these* fields actually do and why, then judging it, not copying the first tutorial
that runs. An adopted practice that cannot be justified under R1 is not adopted.
