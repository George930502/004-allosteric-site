# Playbook: running an experiment

Use whenever a run produces a number worth comparing to another number.

1. **Question first.** Write the one sentence this run should settle before creating
   anything. If it does not have one, it is exploration — do it in `scratch/`, which is
   gitignored, and do not add it to the registry.

2. **Scaffold.**
   ```bash
   uv run allo new-experiment "short description"
   ```

3. **Fill `config.yaml` completely.** Every knob that affects the result, including
   the seed. The test: someone else's rerun of this config on this machine reproduces
   `metrics.json` exactly. If it does not, the config is incomplete — fix the config,
   not the expectation.

4. **Run it, write `metrics.json`.** Metrics come out of the shared scoring harness
   (`src/allo/scoring/`), never hand-computed per experiment, so numbers across runs
   are actually comparable.

5. **Write `notes.md`** while the reasoning is fresh: question, setup, result,
   interpretation. Include what would have to be true for you to stop believing the
   result.

6. **One line in `experiments/REGISTRY.md`.** Including for failures. A method that
   underperformed is a result the next agent needs; deleting it guarantees someone
   re-runs it in three weeks.

## Comparison hygiene

- Every method — classical baseline or quantum — is scored by the same harness on the
  same targets, splits and negative sets. A quantum number that beats a classical
  number computed differently is not evidence.
- Report the negative sets separately: random background residues *and* non-functional
  surface pockets. The challenge scores against both (`CHALLENGE.md` §4.1).
- State the statistical test and the null. "Higher" is not a result; effect size with
  a null model is (principle R3).
- Build the null model *before* the method, not after seeing the scores. In this field
  the null is the real opponent: burial and degree alone will "predict" functional
  sites (`docs/FIELD.md` §3).
