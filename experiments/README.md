# Experiments

One directory per run: `YYYY-MM-DD-slug/` containing

- `config.yaml` — every knob, including the seed. Complete enough to rerun.
- `metrics.json` — the numbers.
- `notes.md` — question, setup, result, interpretation.

Create one with:

```bash
uv run allo new-experiment "ctqw time-averaged transfer"
```

Then add a line to `REGISTRY.md`. The registry is how an agent starting cold learns
what has already been tried — keep it one line per run, newest last.
