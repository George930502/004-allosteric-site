# What every quantum observable in this repository costs on hardware

**Scope:** the C3 and C4 resource account for the eleven observables in
`allo.quantum.walk.SCORERS`. Each row gives the operator, the qubit count under two encodings,
the circuit depth, the two-qubit gate count, the connectivity requirement, and a build verdict.
It excludes which observable ranks residues well. That question belongs to
[`40-method-sweep.md`](40-method-sweep.md) and [`41-selection-and-power.md`](41-selection-and-power.md).
It also excludes the theory of coarse-graining, which belongs to
`../../review/07-coarse-graining-scalability.md`.
**Sibling files:** `../../review/08-hardware-viability.md` supplies every device number, encoding
cost and coherence ceiling used below. `../lit/23-quantum-node-ranking.md` supplies the flop
costs of the open branch and the quantum PageRank circuit cost.
`../data/30-frozen-graph-profile.md` supplies the graphs.
**Produced:** 2026-08-26. Every graph number was measured this session through
`allo.inputs.apo_input` and `allo.network.build`. No holo structure, freeze, manifest,
selection ledger or evaluation artifact was opened.

---

## 0. The honest statement

**Nothing in `allo.quantum` has run on a quantum device. Every observable in the module is
evaluated by classical dense linear algebra on the statevector.** The encoding is one qubit per
residue in the single-excitation sector. An N-residue graph is therefore an N-dimensional
Hilbert space. `exp(-iHt)` is an N x N matrix that `scipy` builds from one `eigh` call. The eleven
observables cost between `N^2` and `(N - |S|) N^3` multiply-adds. The most expensive of them,
`quantum_perturbation_response`, needs 1.5e12 flops on the largest primary arm. The cheapest,
`ctqw_infinite_time_average`, needs 5.8e5 flops on the same arm. The whole set runs in under
two seconds per arm on a laptop. **This is Phase 2, whose exit criterion is a method, not a
circuit.** `docs/ROADMAP.md` assigns circuits, the depth budget and the noise-resilience study
to **Phase 3**, and coarse-graining to **Phase 4**. This file is the C3 and C4 account that
Phase 3 must build against. It is not a report of a hardware run.

Measured flop counts, by the convention of `../lit/23-quantum-node-ranking.md` §3.5. One `eigh`
or one Schur-based Sylvester solve counts as `N^3`. One dense complex `(N,N) x (N,T)` product
counts as `N^2 T`. `T` is the time grid, 512 points for the CTQW observables and 128 for the
perturbation scan. `|S|` is the active-site source size. `[derived here from the code in
`src/allo/quantum/walk.py`]`

| Observable                      | Flop formula                      |  mkp5 | ptp1b | hiv_rt |  ns5b | myosin |
| ------------------------------- | --------------------------------- | ----: | ----: | -----: | ----: | -----: |
| shared eigendecomposition       | `N^3`                             | 3.2e6 | 2.6e7 |  1.6e8 | 1.7e8 |  4.5e8 |
| `ctqw_average_transfer`         | `+ \|S\| N^2 T`, T = 512          | 1.2e8 | 5.0e8 |  1.4e9 | 4.7e8 |  6.3e9 |
| `ctqw_infinite_time_average`    | `+ N^2`                           | 2.2e4 | 8.9e4 |  2.9e5 | 3.1e5 |  5.8e5 |
| `ctqw_peak_transfer`            | `+ \|S\| N^2 T`                   | 1.2e8 | 5.0e8 |  1.4e9 | 4.7e8 |  6.3e9 |
| `ctqw_temporal_variance`        | `+ \|S\| N^2 T`                   | 1.2e8 | 5.0e8 |  1.4e9 | 4.7e8 |  6.3e9 |
| `ctqw_coherent_source_contrast` | `+ (\|S\|+1) N^2 T`               | 1.3e8 | 5.5e8 |  1.5e9 | 6.3e8 |  6.6e9 |
| `quantum_survival_time`         | `N^3` (one Sylvester solve)       | 3.2e6 | 2.6e7 |  1.6e8 | 1.7e8 |  4.5e8 |
| `quantum_perturbation_response` | `(N-\|S\|)(N^3 + \|S\| N^2 128)`  | 4.6e9 | 4.3e10 | 2.7e11 | 1.6e11 | 1.5e12 |
| `dephased_transport`            | `2 k N^3`, k Krylov matrix-vector | 2.8e9 | 3.6e10 | ceiling | ceiling | refused |
| `szegedy_quantum_pagerank`      | `4 R N^2`, R = 200 steps          | 1.7e7 | 7.1e7 |  2.4e8 | 2.4e8 |  4.7e8 |
| `quantum_best_case_transfer`    | `12 N^3` (12 Sylvester solves)    | 3.8e7 | 3.2e8 |  1.9e9 | 2.0e9 |  5.4e9 |
| `quantum_opening_gain`          | free once the sweep is cached     |     0 |     0 |      0 |     0 |      0 |

Three notes on that table. The eigendecomposition is shared through `graph.memo`. Rows 2 to 6
and row 8 pay it once per graph, not once per scorer. `dephased_transport` refuses above
`DEPHASING_MAX_NODES = 620`, which is a declared limit in the module and not a crash. Its Krylov
iteration count was measured this session at **435 matrix-vector products at N = 147** and
**683 at N = 298**. The cost therefore grows faster than `N^3`. `[measured this session, not a
registered experiment]`

---

## 1. The graphs these numbers are derived from

Measured this session with `allo.network.build` at the input layer's frozen contact rule.
The rule is heavy-atom minimum distance at 4.5 A over every modeled residue of the frozen
chain. `[derived here]`

| Arm                        | Tier          |    N |  \|E\| | max degree | \|S\| | greedy edge colors | `ceil(log2 N)` |
| -------------------------- | ------------- | ---: | -----: | ---------: | ----: | -----------------: | -------------: |
| `mkp5`                     | `development` |  147 |    718 |         16 |    11 |                 16 |              8 |
| `ptp1b`                    | `development` |  298 |  1,481 |         20 |    11 |                 20 |              9 |
| `hiv_rt`                   | `development` |  543 |  2,403 |         16 |     9 |                 16 |             10 |
| `ns5b`                     | `development` |  553 |  2,720 |         18 |     3 |                 18 |             10 |
| `cardiac_myosin_corrected` | primary       |  764 |  3,641 |         18 |    21 |                 18 |             10 |

`cardiac_myosin_corrected` is the largest primary arm. The other primary arms measure N = 170
(`kras_g12c_corrected`), N = 272 (`bcr_abl1_corrected`) and N = 451 (`bcr_abl1_mandated`).
`kras_g12c_mandated` measures N = 169 in `../data/30-frozen-graph-profile.md`.

Two columns do work later. The **greedy edge coloring is 16 to 20 classes at every size**. That
is the depth of one Trotter step over the whole contact graph, given all-to-all connectivity. `../../review/08-hardware-viability.md` §1.1 measured 16 to 17 classes on the
C-alpha graph at 8 A. Our frozen graph is denser locally, so the count is slightly higher, and
it is still independent of N. And **\|S\| ranges from 3 to 21**, a 7x range, which multiplies
the circuit count of every source-conditioned observable.

---

## 2. The two encodings, and why only one of them is a route

Both numbers come from `../../review/08-hardware-viability.md` §2. They are restated here so
the main table's two qubit columns are readable without opening that file.

**One-hot, single-excitation sector.** N qubits. The XY hopping Hamiltonian conserves
excitation number, so the state never leaves the N-dimensional subspace. Restricted to that
subspace, `exp(-iHt)` is an N x N unitary. An exact Givens-rotation network implements it in
`N(N-1)/2` two-qubit gates at depth N on a line. Kivlichan, McClean, Wiebe, Gidney,
Aspuru-Guzik, Chan, Babbush, _PRL_ 120, 110501 (2018), arXiv:1711.04789, state it verbatim:
_"we can simulate a Trotter step of the electronic structure Hamiltonian in exactly N depth and
with N^2/2 two-qubit entangling gates ... all assuming only a minimal, linearly connected
architecture."_ `[VERIFIED-FULLTEXT in `08-hardware-viability.md` §2.1]` The mesh construction
is Clements, Humphreys, Metcalf, Kolthammer, Walmsley, _Optica_ 3, 1460 (2016),
doi:10.1364/OPTICA.3.001460. `[VERIFIED-ABSTRACT in the same file]`

**Binary or Gray code.** `ceil(log2 N)` qubits, which is 8 to 10 on our arms. The compression is
real in space and catastrophic in gates. `exp(-iHt)` becomes a generic element of `SU(2^n)`, and
Shende, Bullock, Markov, _IEEE TCAD_ 25(6), 1000-1010 (2006), arXiv:quant-ph/0406176, bound
generic synthesis: _"An arbitrary n-qubit operator can be implemented in a circuit containing no
more than (23/48) x 4^n - (3/2) x 2^n + 4/3 CNOT gates"_, and _"n-qubit operators generically
require ceil[(1/4)(4^n - 3n - 1)] CNOTs"_. `[VERIFIED-FULLTEXT in `08-hardware-viability.md`
§2.3]` Instantiated on our arms, the binary encoding loses at every size. `[derived here from
the two published formulas]`

| Arm      |    N | one-hot qubits | one-hot 2q gates | binary qubits | binary upper bound | binary lower bound |
| -------- | ---: | -------------: | ---------------: | ------------: | -----------------: | -----------------: |
| `mkp5`   |  147 |            147 |           10,731 |             8 |             31,020 |             16,378 |
| `ptp1b`  |  298 |            298 |           44,253 |             9 |            124,844 |             65,529 |
| `hiv_rt` |  543 |            543 |          147,153 |            10 |            500,908 |            262,137 |
| `ns5b`   |  553 |            553 |          152,628 |            10 |            500,908 |            262,137 |
| myosin   |  764 |            764 |          291,466 |            10 |            500,908 |            262,137 |

The binary column is therefore a **qubit count and not a route**. The generic lower bound is
1.5x to 1.8x the one-hot gate count on every arm, and no compiler beats a lower bound. The
binary qubit column appears in the main table because C3 asks for it, not because any row
recommends it.

---

## 3. The main table

One row per entry of `allo.quantum.walk.SCORERS`. Costs are formulas in the arm's own `N`,
`|E|`, `|S|` and edge-color count `C`. Section 3.2 instantiates them.

The verdict column uses three values, defined here.

- **`circuit-realisable now`** — the full-N circuit fits a Braket device today, in qubits and
  in coherent two-qubit gate budget.
- **`circuit-realisable after coarse-graining`** — the circuit exists and is correct, and it
  becomes runnable at the ~20-node size §6 derives.
- **`do not build as a circuit`** — the gate cost exceeds the whole exact CTQW even after
  coarse-graining, or the operator has no useful unitary realization.

### 3.1 The rows

| # | Observable | Operator it needs | Qubits, one-hot | Qubits, binary | Trotter depth per step x steps | Two-qubit gates | Connectivity | Verdict |
| --: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ctqw_average_transfer` | `exp(-iHt)`, H real symmetric | N | `ceil(log2 N)` | C per step, r = 64 to 256 | `\|E\| r`, or `N(N-1)/2` exact | line (Givens), all-to-all (Trotter) | circuit-realisable after coarse-graining |
| 2 | `ctqw_infinite_time_average` | spectral overlap `sum_k \|<i\|k>\|^2 \|<k\|s>\|^2` | N | `ceil(log2 N)` | not applicable, t -> infinity | phase estimation, unknown | any | **do not build as a circuit** |
| 3 | `ctqw_peak_transfer` | `exp(-iHt)` on the same grid | N | `ceil(log2 N)` | C per step, r = 64 to 256 | as row 1 | line | circuit-realisable after coarse-graining |
| 4 | `ctqw_temporal_variance` | `exp(-iHt)` on the same grid | N | `ceil(log2 N)` | C per step, r = 64 to 256 | as row 1 | line | circuit-realisable after coarse-graining, **rank not noise-safe** (§3.3) |
| 5 | `ctqw_coherent_source_contrast` | `exp(-iHt)` plus a source superposition | N | `ceil(log2 N)` | C per step, r = 64 to 256 | as row 1, `+ (\|S\|-1)` for the W state | line | circuit-realisable after coarse-graining |
| 6 | `quantum_survival_time` | `H - i(kappa/2) P_S`, non-unitary | `N + \|S\|` | `ceil(log2 N) + 1` | C per step, r absorption steps | as row 1, `+ r \|S\|` | line, plus mid-circuit reset | circuit-realisable after coarse-graining (§4) |
| 7 | `quantum_perturbation_response` | N detuned copies of `exp(-iHt)` | N | `ceil(log2 N)` | C per step, r = 64 to 256 | as row 1, `x (N - \|S\|)` circuit families | line | circuit-realisable after coarse-graining, N times the shot bill |
| 8 | `dephased_transport` | Lindblad dephasing on every site, plus a sink | `N + N + \|S\|` dilated | `ceil(log2 N) + 2` | C per step, r Trotter steps | `\|E\| r + N r` dephasing gates `+ r \|S\|` | line, plus reset on N ancillas | **do not build as a circuit** (§4.3) |
| 9 | `szegedy_quantum_pagerank` | Szegedy walk on the dense Google matrix | 2N | `2 ceil(log2 N)` | O(N) per reflection block, R = 200 | `~2 N_pad^2` per step, R steps | all-to-all | **do not build as a circuit** (§3.4) |
| 10 | `quantum_best_case_transfer` | 12 values of `H - i(Gamma/2) P_S` | `N + \|S\|` | `ceil(log2 N) + 1` | C per step, r per rate | as row 6, `x 12` rates | line, plus mid-circuit reset | circuit-realisable after coarse-graining (§4) |
| 11 | `quantum_opening_gain` | 2 of the same 12 rates | `N + \|S\|` | `ceil(log2 N) + 1` | C per step, r per rate | as row 6, `x 2` rates | line, plus mid-circuit reset | circuit-realisable after coarse-graining, **rank not noise-safe** (§3.3) |

**Zero rows read `circuit-realisable now`.** That is the finding. It agrees with
`../../review/08-hardware-viability.md` §5.3, which puts the coherent budget at about 200
two-qubit gates. That budget puts the exact Givens network at **N ~ 20**. Our smallest arm is
N = 147.

**Two hidden costs are not in the gate column, and both are larger than it.** First, every CTQW
observable samples a **time grid of 512 points**, and one point is one circuit. Second, the
incoherent source sum is `|S|` separate injections, and one injection is one circuit. So row 1
costs `512 |S|` circuits per arm, which is 5,632 circuits at `mkp5` and 10,752 at myosin.
`[derived here: 512 time points x \|S\| source residues]` The gate count per circuit is
identical across all of them, because only the rotation angles and one X gate change. Braket's
parametric compilation under Hybrid Jobs compiles such a family once
(`../../review/08-hardware-viability.md` §7.1). `[VERIFIED-FULLTEXT there]`

### 3.2 The circuit families, instantiated

Eight of the eleven observables share **one** circuit family, the exact Givens network for
`exp(-iHt)`. Rows 6, 10 and 11 add a sink to that same network. So instantiating three families
covers the table. `[derived here]`

| Arm      |    N | Exact Givens: gates / depth | Trotter r = 64: gates / depth | Trotter r = 256: gates / depth | Szegedy binary: gates per step |
| -------- | ---: | --------------------------: | ----------------------------: | -----------------------------: | -----------------------------: |
| `mkp5`   |  147 |                10,731 / 147 |                45,952 / 1,024 |                183,808 / 4,096 |                        131,072 |
| `ptp1b`  |  298 |                44,253 / 298 |                94,784 / 1,280 |                379,136 / 5,120 |                        524,288 |
| `hiv_rt` |  543 |               147,153 / 543 |               153,792 / 1,024 |                615,168 / 4,096 |                      2,097,152 |
| `ns5b`   |  553 |               152,628 / 553 |               174,080 / 1,152 |                696,320 / 4,608 |                      2,097,152 |
| myosin   |  764 |               291,466 / 764 |               233,024 / 1,152 |                932,096 / 4,608 |                      2,097,152 |

Trotter gate count is `|E| r` and Trotter depth is `C r`, following the convention
`../../review/08-hardware-viability.md` §3.2 measured. The step counts `r = 64` and `r = 256`
are that file's measurement of what a stable top-5 needs. They are not a guess. At N = 272 the
top-5 matched the exact propagator at `r = 64`. At N = 169 it needed `r = 256`.
`[measured in `08-hardware-viability.md` §3.2, not a registered experiment]`

**The exact network beats Trotter on four of the five arms and is 3 to 8 times shallower on all
five.** File 08 §3.6 records the same comparison at N = 272 and draws the same conclusion.
Trotterization is the standard move when the exact unitary is not efficiently synthesizable. In
the single-excitation sector it is. **Any Phase-3 circuit that Trotterizes must state why it is
not using the Givens network.**

### 3.3 Two observables lose their noise guarantee, and it is a property of the estimator

`../../review/08-hardware-viability.md` §5.1 establishes that a global depolarizing channel maps
measured probabilities as `p_i -> lambda p_i + (1 - lambda)/D`. That map is affine and strictly
increasing, so it **cannot reorder a ranking**. The rank deliverable degrades through the shot
budget, which grows as `1/lambda^2`, and not through rank inversion. The published form of the
statement is Micklitz, arXiv:2510.13026. `[VERIFIED-FULLTEXT there]`

That guarantee transfers to an observable only if the observable is an affine function of the
measured probabilities. Checking each row against that condition gives a real split.
`[derived here]`

| Observable                      | Score as a function of `p_i(t)`    | Affine in `p_i`?          | Rank safe under depolarizing noise |
| ------------------------------- | ---------------------------------- | ------------------------- | ---------------------------------- |
| `ctqw_average_transfer`         | `mean_t p_i(t)`                    | yes                       | **yes**                            |
| `ctqw_infinite_time_average`    | `mean_t p_i(t)` at `t -> infinity` | yes                       | **yes**                            |
| `ctqw_peak_transfer`            | `max_t p_i(t)`                     | yes, `max` is monotone    | **yes**                            |
| `ctqw_coherent_source_contrast` | difference of two means            | yes, the offsets cancel   | **yes**                            |
| `ctqw_temporal_variance`        | `var_t p_i / mean_t p_i`           | **no**, a ratio           | **no**                             |
| `quantum_opening_gain`          | `log10` of a ratio of two survivals | **no**, a ratio          | **no**                             |

The mechanism is the offset. Under `p -> lambda p + c`, a mean becomes `lambda mean + c`. A maximum
becomes `lambda max + c`. Both therefore keep their order. A ratio becomes
`lambda^2 var / (lambda mean + c)`, and the constant `c` in the denominator does not divide out.
So the noisy score is not a common monotone image of the noiseless one. Residues whose true
scores differ by less than the distortion can invert. **Rows 4 and 11 must therefore carry a
per-`lambda` calibration in Phase 3, or they must be reported with the caveat.** This is the
same precondition file 08 §5.4 states for per-residue readout schemes, applied to the estimator
rather than to the circuit.

### 3.4 Why quantum PageRank is `do not build as a circuit`

`../lit/23-quantum-node-ranking.md` §2.4 prices it and the number is not close. At N = 272 the
Szegedy walk needs **~524,288 two-qubit gates per step** on `2 ceil(log2 N) = 18` qubits. The
entire exact CTQW at the same N needs **36,856 two-qubit gates** on 272 qubits. The time average needs
hundreds of steps. `[derived in `23-quantum-node-ranking.md` §2.4]` Our arms are worse. `ptp1b` at
N = 298 pays the same 524,288 per step. The three arms above N = 512 pay 2,097,152 per step. `[derived here: `2 N_pad^2` with `N_pad = 2^ceil(log2 N)`]`

There is no sparsity escape and the reason is structural. The damping term `(1-alpha)/N` makes
**every entry of the Google matrix strictly positive**, so the matrix is dense whatever the
contact graph looks like. Loke and Wang, _Ann. Phys._ 382, 64 (2017),
doi:10.1016/j.aop.2017.04.006, give efficient Szegedy circuits only for chains _"possessing
transformational symmetry in the columns of the transition matrix"_. `[VERIFIED-ABSTRACT in
`23-quantum-node-ranking.md` §2.4]` A residue contact graph has no such symmetry.

**The classical simulation is cheap and must still be run.** `szegedy_quantum_pagerank` costs
1.7e7 to 4.7e8 flops on our arms, which is under a second. Its C4 path is fault-tolerant, and
the report must say so rather than citing the 2012 headline of Paparo and Martin-Delgado,
doi:10.1038/srep00444.

### 3.5 Why the infinite-time average is `do not build as a circuit`

The reason is physics and not cost. The `T -> infinity` average has the closed form
`sum_k |<i|k>|^2 |<k|s>|^2`, in which every phase has cancelled. The module's own docstring
records this: the limit is **interference-free by construction**. A circuit that reproduces a
quantity with no interference in it buys nothing that `eigh` does not already give for `N^2`
flops. Two further facts close it. There is no finite time at which the circuit stops, and
Childs and Kothari, arXiv:0908.4398, prove a no-fast-forwarding theorem _"ruling out generic
simulations taking time o(\|\|Ht\|\|)"_. `[VERIFIED-ABSTRACT in `08-hardware-viability.md` §3.5]`
The row is kept in the module because it measures how much of the finite-window score is
interference. That is a diagnostic, not a hardware candidate.

---

## 4. The non-unitary observables, where C4 bites hardest

Four observables are **not** unitary evolution: `quantum_survival_time`,
`quantum_best_case_transfer`, `quantum_opening_gain` and `dephased_transport`. A plain Trotter
circuit does not realize any of them. They are also the observables that carry genuinely
non-classical structure. `../../review/00-conventions.md` §5 and ADR 0026 record why: a
single-excitation Hermitian walk on a real symmetric graph carries no information beyond its
transfer amplitudes. **The two facts point in opposite directions, and this section is where C4
must be paid rather than asserted.**

### 4.1 What each one actually needs

| Observable                   | The generator                             | What hardware must supply                                             |
| ---------------------------- | ----------------------------------------- | --------------------------------------------------------------------- |
| `quantum_survival_time`      | `H_eff = H - i(kappa/2) P_S`              | an absorbing channel on the `\|S\|` source qubits                     |
| `quantum_best_case_transfer` | the same `H_eff` at 12 values of `Gamma`  | the same channel, at 12 calibrated strengths                          |
| `quantum_opening_gain`       | the same sweep, read as a ratio           | the same channel, plus a per-`lambda` calibration (§3.3)              |
| `dephased_transport`         | Lindblad dephasing on every site, plus a sink | N independent dephasing channels **and** an absorbing channel      |

### 4.2 The ancilla and reset route, which is the cheap one

An absorbing sink is a partial SWAP into a fresh ancilla followed by a reset of that ancilla.
`../lit/23-quantum-node-ranking.md` §3.5 gives the construction for a single drain: **one extra
qubit**, and per absorption step **one two-qubit partial SWAP plus one mid-circuit reset**. Our
sink sits on the whole active site, so it needs `|S|` ancillas rather than one. Placing each
ancilla next to its own source qubit keeps the register a line, so the connectivity requirement
does not change. `[derived here from the construction in `23-quantum-node-ranking.md` §3.5]`

Cost of the sink, over `r = 32` absorption steps. `[derived here: `r x \|S\|` extra two-qubit
gates against `N(N-1)/2` in the base network]`

| Arm      |    N | \|S\| | base Givens gates | extra 2q gates | extra as % of base | qubits    | depth      |
| -------- | ---: | ----: | ----------------: | -------------: | -----------------: | --------- | ---------- |
| `mkp5`   |  147 |    11 |            10,731 |            352 |             3.28 % | 147 + 11  | 147 + 32   |
| `ptp1b`  |  298 |    11 |            44,253 |            352 |             0.80 % | 298 + 11  | 298 + 32   |
| `hiv_rt` |  543 |     9 |           147,153 |            288 |             0.20 % | 543 + 9   | 543 + 32   |
| `ns5b`   |  553 |     3 |           152,628 |             96 |             0.06 % | 553 + 3   | 553 + 32   |
| myosin   |  764 |    21 |           291,466 |            672 |             0.23 % | 764 + 21  | 764 + 32   |

**The sink costs under 3.3 % of the gate budget on every arm.** The non-Hermitian branch is
therefore the cheapest genuinely non-classical structure available here. That is why it is worth
Phase 3 effort.

**Mid-circuit reset availability, which `23-quantum-node-ranking.md` §3.5 flagged as unchecked.**
It is available on exactly one Braket device. AWS announced dynamic circuits on **IQM Garnet** on
**26 June 2025**, providing _"mid-circuit measurements (MCM) and feed-forward operations"_ and
_"active qubit reset to reuse qubits within a single circuit execution"_, in the Europe
(Stockholm) region, with the announcement calling it an _"experimental capability"_.
`[VERIFIED-FULLTEXT — aws.amazon.com/about-aws/whats-new/2025/06/amazon-braket-dynamic-circuit-capabilities-iqm-garnet/,
retrieved 2026-08-26]` No equivalent announcement for IonQ, Rigetti, AQT or QuEra was retrieved
by this session's search. **This closes file 23's open item, and it makes IQM Garnet the only
device on which the sink observables can run at all.**

### 4.3 The Sz.-Nagy dilation route, and what it costs

If mid-circuit reset is unavailable, a contraction is realized instead by unitary dilation. A
contraction `T` on an N-dimensional space dilates to a unitary on `2N` dimensions through the
block `U = [[T, D], [D', -T*]]` with `D = sqrt(I - T* T)`. Hu, Xia and Kais, _Sci. Rep._ 10, 3301
(2020), doi:10.1038/s41598-020-60321-x, arXiv:1904.00910, state the principle verbatim:
_"The Kraus operators governing the time evolution can be converted into unitary matrices with
minimal dilation guaranteed by the Sz.-Nagy theorem. This allows the evolution of the initial
state through unitary quantum gates, while using significantly less resource than required by
the conventional Stinespring dilation."_ `[VERIFIED-ABSTRACT — retrieved 2026-08-26]`

The overhead on our encoding is exact arithmetic and is stated here rather than cited.
`[derived here: `2N(2N-1)/2 = N(2N-1)` against `N(N-1)/2`]`

| Arm      |    N | one-hot qubits | dilated qubits | Givens gates | dilated gates | gate ratio | depth       |
| -------- | ---: | -------------: | -------------: | -----------: | ------------: | ---------: | ----------- |
| `mkp5`   |  147 |            147 |            294 |       10,731 |        43,071 |      4.01x | 147 -> 294  |
| `ptp1b`  |  298 |            298 |            596 |       44,253 |       177,310 |      4.01x | 298 -> 596  |
| `hiv_rt` |  543 |            543 |          1,086 |      147,153 |       589,155 |      4.00x | 543 -> 1086 |
| `ns5b`   |  553 |            553 |          1,106 |      152,628 |       611,065 |      4.00x | 553 -> 1106 |
| myosin   |  764 |            764 |          1,528 |      291,466 |     1,166,628 |      4.00x | 764 -> 1528 |

**Under one-hot, the dilation doubles the qubit count and quadruples the gate count.** Under the
binary encoding it costs **one extra qubit**, because `ceil(log2 2N) = ceil(log2 N) + 1`. The
dilated operator is still a generic unitary, so §2's lower bound still applies. Three further
costs must be stated, and none of them is in the table. The dilated block is not a graph-local
operator. Its Givens decomposition must be synthesized from a dense `2N x 2N` matrix, which is
computed classically at `O(N^3)`. The dilation is exact for one fixed `t`, so a survival integral over `r`
steps needs `r` dilated blocks. And the result is heralded by the ancilla flag, so the useful
shots are a post-selected fraction that shrinks with `r`. `[UNVERIFIED — our arithmetic and our
analysis. A published gate count for a Sz.-Nagy dilation of a graph-Laplacian contraction at
N > 100 was not retrieved by this session's search.]`

**Verdict on the two routes.** The ancilla and reset route costs under 3.3 % of the gate budget.
The dilation route costs 4x. **Use reset, and use IQM Garnet.** Report the dilation route as the
fallback that a device without reset would force. Report its 4x as a resource line rather than
as an obstacle.

### 4.4 Why `dephased_transport` stays `do not build as a circuit`

Dephasing is not one channel. It is **one channel per site per step**, because pure dephasing in
the site basis damps every off-diagonal entry. Realizing it needs `N` ancillas with `N` resets
per Trotter step, on top of the `|E|` hopping gates and the `|S|` sink gates. At `mkp5` with
`r = 32` that is 1,024 dephasing resets on 147 ancillas, on a device whose reset capability is
labeled experimental. The gate count exceeds the exact CTQW before the sink is added.

**There is an honest and interesting qualification, and it must be in the report.** A NISQ device
already dephases, for free and without asking. The device's own decoherence realizes the
dephasing term. What it does not realize is a **calibrated** dephasing rate. The whole point of
`dephased_transport` is the optimum in the transfer efficiency as a function of that rate. An
uncontrolled rate cannot find an optimum. So the honest C4 statement is: **the dephasing is free
and the calibration is not**, and the calibration is the part that carries the science.

---

## 5. What we would actually run on hardware

**One observable, one device, one resource line.**

### 5.1 The recommendation

Run **`ctqw_average_transfer`** on a **20-node coarse-grained graph**, in the one-hot
single-excitation encoding, through the exact Givens network, on **IQM Garnet**.

The exact resource line, at the coarse-grained size §6 derives. `[derived here except where
marked]`

| Item                              | Value                                                                    |
| --------------------------------- | ------------------------------------------------------------------------ |
| Encoding                          | one-hot, single-excitation sector                                        |
| Qubits                            | **20**                                                                   |
| Circuit                           | exact Givens network for `exp(-iHt)`, no Trotter error                   |
| Two-qubit gates                   | **190** = `20 x 19 / 2`                                                  |
| Two-qubit depth                   | **20**                                                                   |
| Connectivity required             | **line** (a Hamiltonian path through the 20 qubits)                      |
| Circuits per time point           | `\|S\|`, one X gate apart                                                |
| Time points                       | 512 in the module, reducible to a logarithmic grid in Phase 3            |
| Shots per column                  | ~1e4 measured at N = 169 to 272 (`08-hardware-viability.md` §6.1). Unmeasured at N = 20 |
| `lambda` at p = 5e-3              | **0.386** = `(1 - 0.005)^190`                                            |
| Error detection                   | free, by post-selecting Hamming weight 1                                 |
| Device                            | IQM Garnet, 20 qubits, 99.5 % two-qubit fidelity, square lattice         |
| Price, 12 time points x 1 column  | **$178** = `12 x $0.30 + 1.2e5 x $0.00145`                               |
| Price, 512 time points x 1 column | **$7,578** = `512 x $0.30 + 5.12e6 x $0.00145`                           |

Device qubit count, fidelity and the $0.00145 per-shot price are from
`../../review/08-hardware-viability.md` §5.3 and §7.1. `[VERIFIED-FULLTEXT there, from
docs.aws.amazon.com/braket and aws.amazon.com/braket/pricing]`

### 5.2 Why this observable and not another

Four reasons, each of which this file can decide.

1. **It is the cheapest circuit in the module.** It needs no ancilla, no dilation, no
   mid-circuit reset and no second register. Rows 6, 10 and 11 add a sink. Rows 8 and 9 are
   `do not build`. Row 7 multiplies the circuit count by `N - |S|`.
2. **Its readout is one computational-basis sample.** Every residue score comes from the same
   noisy state with the same `lambda`. That is the precondition
   `../../review/08-hardware-viability.md` §5.4 states, and a per-residue observable scheme fails
   it.
3. **Its score is affine in the measured probabilities**, so global depolarizing noise cannot
   reorder its ranking (§3.3). `ctqw_temporal_variance` and `quantum_opening_gain` fail that
   test.
4. **It delivers the mandated matrix as well as the ranking.** `08-hardware-viability.md` §6.2
   shows the N x N connectivity matrix costs **N circuits and not N^2**, because one shot returns
   a whole column. The same circuit family produces both deliverables.

### 5.3 What this recommendation does not claim

**It does not claim that `ctqw_average_transfer` carries signal.** That is not a resource
question and this file must not answer it. `../../review/00-conventions.md` §5 item 1 records the
prior that the absolute CTQW transfer amplitude is a proximity ranker. ADR 0026 makes that
result prior rather than verdict. The measurement is
[`40-method-sweep.md`](40-method-sweep.md), read against the label-blind ceiling in
[`41-selection-and-power.md`](41-selection-and-power.md). That ceiling is
**best-of-3000 mean AUC 0.771 median and 0.810 at p95** at the raw variant count, falling to a p95 of 0.707 at the measured effective V of ≈10, on the `development` tier
(`experiments/REGISTRY.md`, `2026-08-26-selection-power`).

**So the recommendation is conditional, and the condition is stated as a rule.** Run the arm the
screen selects. If the screen selects a sink observable instead, the resource line moves to §4.2.
It grows by under 3.3 % in gates, plus `|S|` ancillas. The device must also support mid-circuit
reset. If the screen selects `dephased_transport` or
`szegedy_quantum_pagerank`, then **the hardware demonstration and the scored method are
different objects**. The report must say so plainly. Do not run one observable on the device and
report another in the results table.

---

## 6. Coarse-graining: the ceiling, and the compression factor per arm

### 6.1 The ceiling is set by fidelity and not by qubit count

Two ceilings exist and the tighter one wins.

- **Qubit count.** The largest gate-based device on Braket is Rigetti Cepheus-1-108Q at 108
  qubits. `[VERIFIED-FULLTEXT in `08-hardware-viability.md` §7.1]`
- **Coherent gate budget.** At two-qubit error `p`, the useful budget is `G* = 1/p` gates, and
  `N(N-1)/2 <= G*` fixes N.

The second ceiling is 5x tighter. `../../review/08-hardware-viability.md` §5.3 instantiates it
per device, and the numbers are reproduced here because they set every factor in §6.2.

| Device                    | Qubits | 2q error | `G* = 1/p` | largest N |
| ------------------------- | -----: | -------: | ---------: | --------: |
| IonQ Forte-1              |     36 |   4.0e-3 |        250 |    **22** |
| IQM Garnet                |     20 |   5.0e-3 |        200 |    **20** |
| IQM Emerald               |     54 |   5.0e-3 |        200 |    **20** |
| Rigetti Ankaa-3, fSim     |     84 |   5.0e-3 |        200 |    **20** |
| Rigetti Cepheus-1-108Q    |    108 |   9.0e-3 |        111 |    **15** |

`[VERIFIED-FULLTEXT for the error rates in `08-hardware-viability.md` §5.3. The `G*` and N
columns are that file's arithmetic]`

**Take N = 20 as the Phase-4 target.** IQM Garnet's 20 qubits and its 20-node fidelity ceiling
coincide exactly.
It is also the only Braket device with mid-circuit reset (§4.2).

### 6.2 The compression factor Phase 4 must achieve, per arm

`[derived here: `N / 20`]`

| Arm                        |    N | Compression to 20 nodes | Compression to 22 (IonQ Forte-1) | Qubits removed |
| -------------------------- | ---: | ----------------------: | -------------------------------: | -------------: |
| `mkp5`                     |  147 |               **7.3x**  |                            6.7x  |            127 |
| `ptp1b`                    |  298 |              **14.9x**  |                           13.5x  |            278 |
| `hiv_rt`                   |  543 |              **27.1x**  |                           24.7x  |            523 |
| `ns5b`                     |  553 |              **27.6x**  |                           25.1x  |            533 |
| `cardiac_myosin_corrected` |  764 |              **38.2x**  |                           34.7x  |            744 |

For the other primary arms the factors are 8.5x (`kras_g12c_corrected`, N = 170), 13.6x
(`bcr_abl1_corrected`, N = 272) and 22.6x (`bcr_abl1_mandated`, N = 451). `[derived here]`

### 6.3 What the factor does to the label set, which is the real risk

**A 38x compression on myosin puts about 20 residues in a super-node.** The mandated deliverable
is a **top-5 ranked residue hit list** in author numbering. A ranking over 20 super-nodes is not
that list, and expanding a super-node back to 20 residues does not order them. So Phase 4 must
show two separate things, and the second is the harder one.

1. The coarse propagator preserves the topological signal. `docs/ROADMAP.md` Phase 4 already
   names the tests: spectral distance, rank correlation and pocket recovery per ratio.
2. **The coarse ranking maps back to a residue-level top-5.** No file in this repository yet
   states how. It is not a reporting detail. It decides whether a hardware run produces a
   deliverable or a demonstration.

**And a warning about the numbers above.** N = 20 is a *hardware* constraint that
`08-hardware-viability.md` §5.3 derives, not a *methodological* choice. It is possible that
signal survives 7.3x on `mkp5` and does not survive 38.2x on myosin. If so, the honest report
states the ratio at which each arm breaks, and does not average them.

---

## 7. What this changes for our pipeline

1. **Phase 3 builds the exact Givens network, not a Trotterizer.** It is 3 to 8 times shallower on
   every arm and cheaper in gates on four of five. It has no Trotter error (§3.2).
   `docs/ROADMAP.md` Phase 3 currently reads "Trotterised `exp(-iHt)`". That wording must be
   amended, or the phase must state why the exact network was rejected.
2. **Do not implement a binary or Gray-code encoding.** The generic lower bound is 1.5x to 1.8x
   the one-hot gate count on every arm (§2). The qubit column exists to satisfy C3, not to
   propose a route.
3. **Do not build a circuit for `szegedy_quantum_pagerank`, `dephased_transport` or
   `ctqw_infinite_time_average`.** Three separate reasons: a dense Google matrix at 2,097,152
   gates per step, N dephasing channels per step, and an interference-free closed form. Simulate
   all three classically and report the resource line as the reason (§3.4, §3.5, §4.4).
4. **`ctqw_temporal_variance` and `quantum_opening_gain` need a per-`lambda` calibration.** Their
   scores are ratios, so the depolarizing order-preservation guarantee does not reach them
   (§3.3). This was not previously written down anywhere.
5. **Mid-circuit reset exists on IQM Garnet and nowhere else on Braket.** That closes the open
   item in `../lit/23-quantum-node-ranking.md` §3.5, and it makes Garnet the only device that can
   run the sink observables (§4.2).
6. **The circuit count, not the gate count, is the shot bill.** Row 1 needs `512 x |S|` circuits,
   which is 5,632 to 10,752 on our arms. Phase 3 must either reduce the time grid to a
   logarithmic one or price the full grid honestly (§3.1).
7. **Phase 4's compression target is 7.3x to 38.2x, and hardware fixes it.** Per-arm factors are
   in §6.2. The unresolved question is not the compression, it is how a super-node ranking
   becomes a residue-level top-5 (§6.3).
8. **Every quantum arm fills §3.1's row before it is accepted.** That is the operational form of
   C3 in this repository, and it is `../../review/08-hardware-viability.md` §9.2's procedure
   applied to code that now exists.

---

## 8. What is unknown, and what would fill each gap

Recorded as absences rather than as claims, per ADR 0019 and
`../../review/00-conventions.md` §2.

- **Shots at N = 20.** `08-hardware-viability.md` §6.1 measured the shot budget at N = 169 to
  764. The coarse-grained size has fewer residues to separate, so the budget must fall. Measure
  it once Phase 4 fixes the size.
- **The Krylov iteration count of `dephased_transport` above N = 298.** Measured at 435 and 683
  matrix-vector products at N = 147 and N = 298. The trend is faster than `N^3` and it is
  unmeasured on `hiv_rt` and `ns5b`.
- **A synthesized depth for the binary encoding.** Section 2 gives gate counts from published
  bounds. A transpiled depth needs one Qiskit or Classiq synthesis run on a real contact graph
  at 8 to 10 qubits. It is cheap and it is not done here.
- **A published Sz.-Nagy gate count for a graph-Laplacian contraction at N > 100** was not
  retrieved by this session's search. Section 4.3's arithmetic is ours.
- **Mid-circuit reset fidelity on IQM Garnet.** The capability is announced. No error rate for
  the reset operation was retrieved. The sink construction's `r` resets are a fidelity cost that
  is currently unpriced.
- **Whether any observable in `SCORERS` carries signal.** Not a resource question. See §5.3.

---

## Method

**Measurement.** Every graph number in §1, §2, §3.2, §4.2, §4.3 and §6.2 was computed this
session. Each arm was built through `allo.inputs.apo_input` and `allo.network.build` at the
input layer's frozen contact rule. Edges, degrees, greedy edge colors and source size were then
counted from that graph. The Krylov iteration counts in §0 were measured by instrumenting the `matvec` callback of
the `lgmres` solve that `allo.quantum.walk.dephased_transport` performs. Scripts ran in the
session scratchpad. **None of these is a registered experiment.** Any number here that becomes
load-bearing must be re-run under `docs/playbooks/experiment.md` and recorded in
`experiments/REGISTRY.md`.

**Arithmetic.** Gate counts, depths, dilation overheads, compression factors, `lambda` values and
prices are elementary arithmetic on published formulas. Each is marked `[derived here]` with the
formula beside it. The formulas themselves are cited to their sources in
`../../review/08-hardware-viability.md` and `../lit/23-quantum-node-ranking.md`. Those files
verified them on 2026-08-25 and 2026-08-26.

**Retrieval this session.** Two questions were open in the sibling files and both were closed by
direct fetch on 2026-08-26. Mid-circuit measurement and reset on Braket, from
`aws.amazon.com/about-aws/whats-new/2025/06/amazon-braket-dynamic-circuit-capabilities-iqm-garnet/`.
The Sz.-Nagy dilation principle, from `arxiv.org/abs/1904.00910`, which carries
doi:10.1038/s41598-020-60321-x. One WebSearch query for each. No other retrieval was performed,
because every other number in this file already exists with a verified citation in a sibling
file.

**Leakage.** Nothing here opened `docs/benchmark/primary/frozen.json`,
`docs/benchmark/secondary/frozen.json`, either `manifest.yaml`,
`docs/benchmark/secondary/selection.json`,
`docs/benchmark/secondary/evidence/extension-candidates.md`, or anything under
`docs/benchmark/evaluation/`. `allo.inputs.apo_input` and `allo.network.build` are
prediction-path code and were the only route to a structure.
