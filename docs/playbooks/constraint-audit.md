# Playbook: constraint audit

Run against a diff before merging anything that touches the prediction path, ground
truth, or a quantum method. These constraints come from the challenge statement;
breaking one invalidates the submission regardless of how good the numbers look.

## C1 — Apo input only, holo for scoring only

- Does any module outside `src/allo/groundtruth/` load, import, or receive a holo
  structure, holo-derived residue set, or anything computed from one?
- Does a prediction function take a parameter whose value came from ground truth —
  including a residue count, a pocket size, a threshold tuned on holo labels, or a
  "top-k" chosen because it happened to work?
- Was any hyperparameter selected by looking at the final enrichment score? That is
  test-set leakage even without a holo import. If so, say so explicitly in the report.

## C2 — No classical MD trajectories as input

- No trajectory files, no MD-derived covariance or contact-frequency inputs, no
  weights from a model trained on MD data anywhere in the prediction path.
- Elastic-network normal modes are analytical, not MD — those are allowed (C6).

## C3 — Near-term hardware viability

- Does every quantum method report qubit count, circuit depth, gate counts and
  required connectivity for each target?
- Is depth growth with system size stated, not just the single-instance number?

## C4 — Credible execution path

- If the method is quantum-inspired or classically simulated, is the mapping to
  hardware described concretely?

## C5 — Scope

- Catalytic domains only; waters, co-factors and PTMs excluded unless modelled as
  simple nodes — and if modelled, is that documented per target?

## C6 — Elastic network hypothesis

- Are we still deriving dynamics from contact topology rather than smuggling in an
  atomic force field?

## Reporting

Findings go back as a list, most severe first, each naming the file and line and the
concrete way it breaks the constraint. "Looks fine" without having checked the
prediction path's imports is not an audit.
