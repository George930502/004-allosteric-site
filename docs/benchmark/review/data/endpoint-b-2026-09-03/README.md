# Endpoint (b) and the decision rule — measured 2026-09-03

Raw output from the fourth pass. Every number ADR 0038, ADR 0039 and ADR 0040 quote is in
these files, with the seed and the sample size that produced it.

| File | What it holds |
| --- | --- |
| `s34_sim.json` | Size and power of the **shipped** negative-class-(b) statistic, which ranks the detector's site-pocket lining. Four correlation lengths, 50 000 fields per size cell, 20 000 per power cell |
| `s4b.json` | Size and power of the **label-set** form, same instrument, same linings. 20 000 fields per size cell, 10 000 per power cell |
| `s1_fwer.json`, `s1_lfc.json` | Familywise error of the disjunction and of the conjunction, at the global null and at the least-favourable configuration |
| `s5_t005_n999_cap10000.json`, `s5_t010_n999_cap4000.json` | The matched-patch sampler re-drawn at two rejection budgets |

## Why the scripts are not here

They import `allo.inputs` and `allo.scoring`, and a tracked file inside this tree may import
no `allo` module (ADR 0034). That rule is what makes the exemption for this directory's own
tools a rule rather than a list of names: a prediction runner must import the package, so a
file that does not cannot be one.

The rule is right and these scripts are the case it does not cover. They are audit-side
simulations that need the evaluation layer, and `experiments/` cannot hold them either,
because a runner there may not name `_positives` or the frozen label sets. An audit tool that
reads the answer key belongs on the evaluation side, and the evaluation side is package code.

So the JSON is the record. Each file carries the seed, the sample size, the arm, the
correlation length and the Clopper-Pearson interval, which is what a reader needs to check the
arithmetic or to re-run it. `27-fourth-pass-synthesis.md` states the instrument in full.
