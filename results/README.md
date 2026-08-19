# Results

The scored deliverables, one directory per target (`CHALLENGE.md` §5):

```
results/<target>/connectivity.npz   N x N quantum connectivity matrix
results/<target>/hits.csv           top-5 ranked predicted allosteric residues
results/<target>/meta.json          config hash, code version, timestamp
```

Small artifacts (`hits.csv`, `meta.json`) are committed — they are the submission.
Large arrays are gitignored and regenerated from the recorded config.
