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

## Resuming a run across a protocol change

A long sweep writes `records.jsonl` incrementally and skips a key it already holds. Two rules
make that safe.

- **Put the protocol version in the resume key.** `score_arm` stamps `protocol_frozen_on` into
  every record. If the key is only `arm|graph|scorer|detrend`, a re-run after the evaluation
  layer is re-frozen keeps every old row and appends nothing. The 2026-08-26 sweeps did this,
  and their decoy columns stayed at protocol version 1 with no visible sign.
- **If a run's records predate the current freeze, say so in `notes.md` and measure the gap.**
  Do not assume that every column moved, and do not assume that none did. Re-score a sample
  through the current harness and print the per-field table. For the 2026-08-26 sweeps, the
  decoy columns all moved and the screening statistic moved on none of 216 records, so the
  selection stood and no re-run was needed.

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
