# Evidence base for the frozen benchmark

Every claim in `docs/benchmark/README.md` that is not a number derived by
`allo benchmark verify` traces to one of these reviews. They exist because R3 says a
recalled number is not evidence — so each one records its retrieval route, tags each claim
`[VERIFIED-FULLTEXT]` / `[VERIFIED-ABSTRACT]` / `[UNVERIFIED]`, and names what it could
**not** establish.

All eleven were compiled **2026-08-20**. None is generated; none regenerates. Where one
disagrees with `frozen.json`, the freeze wins.

## Open one when its question is yours

| Open this                            | When                                                                                                                                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allosteric-pair-definition.md`      | You need the nine clauses' provenance. The allostery field's own standards, clause by clause, with the quote behind each. **The definitional backbone of §1**                                                       |
| `cryptic-vs-allosteric.md`           | Anyone argues cryptic and allosteric are the same thing. Carries Vajda's 8-of-19 and CASBench's 30 %, the two numbers **ADR 0007** rests on — including the sentence that limits the second                         |
| `apo-holo-definition.md`             | The word "apo" is doing work in an argument. The three competing readings, the tolerated-ligand whitelists that disagree between benchmarks, and why "site-apo" is this repo's coinage                              |
| `curation-standard.md`               | Adding a pair, or defending how one was chosen. What other groups check when curating a benchmark pair, and the dimensions on which the field is silent                                                             |
| `evaluation-protocol-lit.md`         | Touching §5. Whether the field uses AUC-ROC or AUC-PR, whether anyone runs a permutation null (largely not), and what the matched-patch precedent actually is                                                       |
| `allosteric-prediction-prior-art.md` | Judging what a result is worth. Which methods have seen which target, the ENM bar (APOP, ESSA), and AlloBench's post-dedup collapse. **Carries the Zheng 2023 correction that voided the last blind claim**         |
| `prior-prediction-attempts.md`       | The same question from the cryptic-pocket side — deliberately not repeated in the file above. Includes Grant 2011, who predicted the S-IIP two years before Ostrem                                                  |
| `target-prior-art.md`                | Working on one target's biology. What the literature says about each of the three pockets                                                                                                                           |
| `myosin-structural-landscape.md`     | Anything myosin. The exhaustive RCSB sweep that found the replacement pairs after `6C1H` failed, and the ligand-centroid geometry separating Site 1 from Site 2                                                     |
| `allosteric-pair-audit.md`           | Asking what a high benchmark score actually demonstrates. Re-run over all **11 scoreable arms** from `sorted(frozen)`: five show a scoreable-site structural response; three ABL1 arms pass the active-site rule but have unmatched catalytic occupants and correlated differences, so none isolates an effector-attributable active-site response |
| `claim-verification.md`              | Checking the challenge statement itself. Seven claims from `CHALLENGE.md` §6 Table 1 against independent records                                                                                                    |

## How to read them

- **Tags are load-bearing.** `[VERIFIED-FULLTEXT]` means the quote came back from the
  paper's full text in that session. `[UNVERIFIED]` means it did not, and the claim must not
  be promoted to the README without retrieving it first.
- **A "could not retrieve" note may be stale.** Europe PMC's `fullTextXML` 404s on records it
  marks `isOpenAccess: N`, but `pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` often serves the same
  paper — three sources listed as unreachable in `cryptic-vs-allosteric.md` were later read
  that way, and one of them resolved the `Ala767` open item. Try the second route before
  recording a source as closed.
- **An "X did not test our site" claim is provisional until the whole results section is
  read.** The Site 1 blind claim survived for a day because a paper was read to the sentence
  that confirmed the expected answer and no further. That correction is written up in
  `allosteric-prediction-prior-art.md`.
