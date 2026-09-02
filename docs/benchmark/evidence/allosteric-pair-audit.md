# Structural audit of the frozen pairs against the ALLOSTERIC criterion

**Question.** The frozen arms were first validated against *cryptic-pocket* criteria: is the
pocket absent in the apo, does the ligand clash if transplanted. That lens is silent on the
two things allostery actually is — **coupling between two sites** and **transition between
functional states**. This document re-audits every frozen arm on the axes crypticity does not
measure.

**Re-run:** 2026-09-02, over the **six** arms of the re-frozen benchmark. The 2026-08-24 run
covered five. Two arms changed after the organisers answered on 2026-09-02: `bcr_abl1_mandated`
moved to `1OPL` chain B (ADR 0029) and `cardiac_myosin_mandated` was frozen for the first time
(ADR 0031). Every number for the other four arms reproduced exactly.
**Sources:** the deposited mmCIF files in `data/raw/`, plus `manifest.yaml` and
`frozen.json`. Nothing is restated from memory.

**Tags.** `[DERIVED]` — computed from coordinates by the script in §5. `[RETRIEVED]` — read
from an RCSB entry record. Nothing else is asserted.

This is evaluation-side evidence and is never imported by prediction code.

---

## 0. Headline

**No arm supplies an isolated structural comparison from which an active-site response can be
attributed to the allosteric ligand.** That is the finding. It survived the reduction from
eleven arms to five, and it survives the return to six.

Concretely, across the six arms the two things that would have to co-occur never do:

- On KRAS and on myosin the **label site moves and the active site does not** (active-site
  median displacement 0.23–0.43 Å, one-sided p = 1 against the rest of the chain).
- On `bcr_abl1_corrected` the **active site does move** (median 0.90–0.93 Å, p = 0.025 on the
  core fit) — but both ABL1 arms also swap their ATP-site occupant, `P16` in the apo for
  nilotinib in the holo. A displacement at the active site cannot be attributed to asciminib
  when a second ligand changed at that exact site.
- **On the two arms added or changed on 2026-09-02 the axis does not apply at all**, and
  saying so is the honest reading. `bcr_abl1_mandated` on chain B displaces by 22.89 Å over
  345 common Cα, because chain B's regulatory module sits somewhere else entirely; that is a
  domain placement, not a response to a ligand. `cardiac_myosin_mandated` displaces by 6.77 Å,
  because the apo member is a 20 Å homology model. Neither number measures coupling and
  neither is quoted as if it did.

The consequence is not "the pairs are bad". It is that **the benchmark's ground truth is a
binding-site label set, not a coupling label set** (ADR 0007). Allostery is inherited from the
cited functional experiments in `allosteric_evidence`, never from these coordinates. No arm
can by itself establish that a propagation method recovered *coupling* rather than *a pocket*.

---

## 1. Coupling geometry `[DERIVED]`

Distance and contact-graph separation between the scoreable label set and the derived active
site. This is the geometry a propagation method has to traverse.

| Arm | min | mean over pairs | mean nearest | shortest path | median path | shared residues |
| --- | --: | --: | --: | --: | --: | --- |
| `kras_g12c_mandated` | 1.32 Å | 16.08 Å | 7.79 Å | 1 hop | 2.0 hops | 11, 12, 13, 16, 34 |
| `kras_g12c_corrected` | 1.31 Å | 15.93 Å | 7.81 Å | 1 hop | 2.0 hops | 11, 12, 13, 16, 34 |
| `bcr_abl1_mandated` | 7.66 Å | 23.18 Å | 14.28 Å | 2 hops | 3.0 hops | none |
| `bcr_abl1_corrected` | 7.85 Å | 23.64 Å | 14.87 Å | 2 hops | 3.0 hops | none |
| `cardiac_myosin_mandated` | 13.98 Å | 32.06 Å | 25.22 Å | 4 hops | 6.0 hops | none |
| `cardiac_myosin_corrected` | 13.70 Å | 30.08 Å | 23.81 Å | 4 hops | 6.0 hops | none |

**KRAS shares five residues between its label set and its propagation source.** Those five
are removed from both classes before scoring (21 labels → 16 scoreable), which is why the
positives and the negatives are both defined on the candidate set (ADR 0011). One hop of
separation is why a distance-only baseline is close to unbeatable on this target, and why the
KRAS result must never be quoted without that baseline beside it.

**Myosin is the genuine long-range case**: 13.7 Å and four hops at the closest approach, six
hops at the median. It is also the arm with the lowest prevalence (1.6 %, and 1.3 % on the
mandated arm). Those two facts together make it the hardest arm and the most informative one.
The two myosin arms agree on this axis to within 2 Å and to the hop, which is the one place the
homology model and the measured structure do agree.

---

## 2. Orthosteric-site state `[DERIVED]`

What sits in the catalytic site of each member, and how close it gets.

| Arm | Apo occupant | Holo occupant | Matched? |
| --- | --- | --- | --- |
| `kras_g12c_mandated` | GDP 2.78 Å, MG 2.09 Å | GDP 2.72 Å, MG 2.16 Å (+ MOV 1.81 Å, the effector) | yes |
| `kras_g12c_corrected` | GDP 2.70 Å, MG 2.11 Å | GDP 2.72 Å, MG 2.16 Å (+ MOV 1.81 Å) | yes |
| `bcr_abl1_mandated` | P16 3.38 Å | NIL 3.01 Å | **no** |
| `bcr_abl1_corrected` | P16 3.27 Å | NIL 3.01 Å | **no** |
| `cardiac_myosin_mandated` | **nothing — the entry has zero heteroatoms** | ADP 2.34 Å, MG 2.07 Å, PO4 2.61 Å | **no** |
| `cardiac_myosin_corrected` | ADP 2.29 Å, MG 2.09 Å, PO4 2.43 Å | ADP 2.34 Å, MG 2.07 Å, PO4 2.61 Å | yes |

The effector is classified separately from the catalytic state, so MOV does not make the KRAS
pair look mismatched. The ABL1 mismatch is real and is the confound named in §0.

`cardiac_myosin_mandated` is a third kind of mismatch. `5TBY` is a homology model with no
heteroatoms at all, so its catalytic site is empty of nucleotide while the holo carries
ADP·Mg·Pi. Nothing was stripped: the entry never had any. This is also why the arm's
propagation source comes from a family motif triple and not from a ligand (ADR 0031).

---

## 3. Local versus global response `[DERIVED]`

Per-residue Cα displacement after superposition, reported twice: fitted globally, and fitted
on the core (non-label, non-active-site) residues only. `p_vs_rest` is a one-sided
Mann-Whitney test of that group against the rest of the chain.

| Arm | fit | n | RMSD | scoreable labels | p | active site | p | rest |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| `kras_g12c_mandated` | global | 166 | 1.36 Å | 1.19 Å | 0.0046 | 0.43 Å | 1 | 0.66 Å |
| `kras_g12c_mandated` | core | 166 | 1.53 Å | 1.53 Å | 0.010 | 0.23 Å | 1 | 0.48 Å |
| `kras_g12c_corrected` | global | 167 | 1.34 Å | 1.03 Å | **8.4e-05** | 0.29 Å | 1 | 0.48 Å |
| `kras_g12c_corrected` | core | 167 | 1.38 Å | 1.21 Å | **0.00019** | 0.26 Å | 1 | 0.43 Å |
| `bcr_abl1_mandated` † | global | 345 | 22.89 Å | 23.96 Å | 0.27 | 10.67 Å | 0.99 | 21.02 Å |
| `bcr_abl1_mandated` † | core | 345 | 22.91 Å | 25.26 Å | 0.089 | 10.93 Å | 0.99 | 20.73 Å |
| `bcr_abl1_corrected` | global | 252 | 1.78 Å | 0.64 Å | 0.86 | 0.93 Å | 0.11 | 0.87 Å |
| `bcr_abl1_corrected` | core | 252 | 2.01 Å | 0.48 Å | 0.61 | 0.90 Å | 0.025 | 0.50 Å |
| `cardiac_myosin_mandated` † | global | 761 | 6.77 Å | 1.83 Å | 0.88 | 1.45 Å | 1 | 2.60 Å |
| `cardiac_myosin_mandated` † | core | 761 | 6.80 Å | 1.70 Å | 0.93 | 1.70 Å | 1 | 2.46 Å |
| `cardiac_myosin_corrected` | global | 764 | 1.18 Å | 0.79 Å | **0.0019** | 0.29 Å | 1 | 0.59 Å |
| `cardiac_myosin_corrected` | core | 764 | 1.26 Å | 0.74 Å | 0.036 | 0.29 Å | 1 | 0.43 Å |

**† These two rows do not measure a conformational response, and must not be read as one.**
Both arms have an apo member that differs from the holo for a reason unrelated to the ligand.
`1OPL` chain B carries the same kinase domain in a different place — over the 239 Cα of the
kinase domain alone it fits the holo at **1.08 Å**, against chain A's 1.00 Å (ADR 0029), so
the 22.89 Å is the regulatory module and nothing else. `5TBY` is a 20 Å homology model whose
long-range contact Jaccard against the measured `9GZ3` is 0.471 (ADR 0031). The rows are
printed because omitting them would hide the size of the defect, not because the axis works.

Read the pattern, not the individual p-values. **KRAS and myosin show a local response at the
label site with a rigid active site.** That is consistent with a pocket forming or adjusting
around a ligand, and it is silent on coupling. **ABL1 shows the opposite** — a rigid label
site (the myristoyl pocket is pre-formed in both members) with a moving active site — which
would be the interesting signal if its ATP-site occupant had not changed too.

### Caveats on this axis

- Displacement is not dynamics. A crystal or cryo-EM pair gives two snapshots, and the elastic
  network hypothesis (C6) is about topology rather than about observed motion.
- Every arm has some construct difference. `1OPL` carries K29R, E30D and D382N; `2G2H` carries
  H415P; `5MO4` carries T334I and D382N.
- One-sided Mann-Whitney with n between 12 and 21 in the positive group is a weak test. p = 1
  means "the group is more rigid than the rest", not "no effect".

---

## 4. What follows

**For the freeze.** Nothing changes. These axes are difficulty and confound descriptors, not
admission criteria. ADR 0007 settled that crypticity and conformational response are reported,
never used as pass or fail. That settlement is what lets the two defective mandated arms be
carried at all: they are disclosed, not admitted on merit, and they are non-confirmatory.

**For the method, and this is the decision-relevant point.** A method that scores highly here
has recovered a **drug-binding site**. Claiming it recovered an **allosteric** site requires
the functional citation in `allosteric_evidence`, not this benchmark. Write the report that
way. The honest claim is "ranks the experimentally validated allosteric pocket highly on apo
input", and it is a strong claim. "Predicts allostery" is not supported by any structure pair
in this set, or by any two-structure comparison at all — see the Fenton four-complex
requirement in `README.md` §1.

---

## 5. Reproduction

Every `[DERIVED]` number above regenerates from the script below. Inputs are the frozen
manifest, `frozen.json` and the deposited mmCIFs. No holo information enters any apo-side
quantity, and this file is evidence, never imported by prediction code (C1).

The exact re-run command from the repo root:

```text
awk '/^```python/{flag=1;next}/^```$/{if(flag){exit}}flag' docs/benchmark/evidence/allosteric-pair-audit.md | UV_CACHE_DIR=/tmp/allo-uv-cache uv run python -
```

It imports one private helper (`allo.benchmark._chain_ca`). The arm list is derived as
`ARMS = sorted(frozen)`, so adding or removing a frozen arm changes both the run and the
coverage regression test.

```python
"""Regenerates the derived numbers in docs/benchmark/evidence/allosteric-pair-audit.md."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

from allo.benchmark import FROZEN, _chain_ca
from allo.groundtruth.labels import align_numbering
from allo.groundtruth.manifest import read_manifest as load  # evaluation side: needs `holo`
from allo.groundtruth.structures import EVAL_CACHE, fetch_mmcif, parse_mmcif

CUT = 4.5
_seen: dict[str, object] = {}


def S(pdb):
    if pdb not in _seen:
        _seen[pdb] = parse_mmcif(fetch_mmcif(pdb, EVAL_CACHE), pdb)
    return _seen[pdb]


def res_atoms(st, chain, keep=None):
    """{author seq id: heavy-atom row indices} for polymer residues of `chain`."""
    idx = np.where(st.protein & (st.chain == chain))[0]
    out: dict[int, list[int]] = {}
    for i in idx:
        out.setdefault(int(st.seq_id[i]), []).append(i)
    return {n: np.array(v) for n, v in out.items() if keep is None or n in keep}


def site_distance(st, chain, setA, setB):
    """Heavy-atom distances between two residue sets of one chain."""
    ai, bi = res_atoms(st, chain, set(setA)), res_atoms(st, chain, set(setB))
    per_res = {}
    for ka, ia in ai.items():
        per_res[ka] = min(
            float(
                np.linalg.norm(st.coord[ia][:, None, :] - st.coord[ib][None, :, :], axis=-1).min()
            )
            for ib in bi.values()
        )
    allpairs = [
        float(np.linalg.norm(st.coord[ia][:, None, :] - st.coord[ib][None, :, :], axis=-1).min())
        for ia in ai.values()
        for ib in bi.values()
    ]
    return {
        "min": round(min(allpairs), 2),
        "mean_over_pairs": round(float(np.mean(allpairs)), 2),
        "mean_nearest": round(float(np.mean(list(per_res.values()))), 2),
        "max_nearest": round(max(per_res.values()), 2),
    }


def contact_graph(st, chain, keep=None, cutoff=CUT):
    """Residue graph: edge when any heavy-atom pair is within `cutoff`."""
    ri = res_atoms(st, chain, keep)
    keys = sorted(ri)
    cen = np.array([st.coord[ri[k]].mean(0) for k in keys])
    rad = np.array(
        [np.linalg.norm(st.coord[ri[k]] - cen[i], axis=1).max() for i, k in enumerate(keys)]
    )
    D = np.linalg.norm(cen[:, None, :] - cen[None, :, :], axis=-1)
    adj = {k: set() for k in keys}
    for i in range(len(keys)):
        for j in np.where(D[i] <= rad[i] + rad + cutoff)[0]:
            if j <= i:
                continue
            a, b = ri[keys[i]], ri[keys[j]]
            if (
                np.linalg.norm(st.coord[a][:, None, :] - st.coord[b][None, :, :], axis=-1).min()
                <= cutoff
            ):
                adj[keys[i]].add(keys[j])
                adj[keys[j]].add(keys[i])
    return adj


def hops(adj, src, dst):
    """BFS hop count from any residue in `src` to the nearest residue in `dst`."""
    dst = set(dst) & set(adj)
    seen = {s: 0 for s in set(src) & set(adj)}
    q = deque(seen)
    while q:
        u = q.popleft()
        if u in dst:
            return seen[u]
        for v in adj[u]:
            if v not in seen:
                seen[v] = seen[u] + 1
                q.append(v)
    return None


def deviation(apo_id, apo_ch, holo_id, holo_ch, keep):
    """Per-residue CA deviation, apo numbering, in a global and an outlier-rejected frame."""
    apo, holo = S(apo_id), S(holo_id)
    aca, hca = _chain_ca(apo, apo_ch), _chain_ca(holo, holo_ch)
    h2a = align_numbering(holo, apo, holo_ch, apo_ch)
    pairs = [(h, h2a[h]) for h in sorted(hca) if h in h2a and h2a[h] in aca and h2a[h] in keep]
    P = np.array([hca[h] for h, _ in pairs])
    Q = np.array([aca[a] for _, a in pairs])
    nums = np.array([a for _, a in pairs])

    def kabsch(mask):
        p, q = P[mask], Q[mask]
        pb, qb = p.mean(0), q.mean(0)
        V, _, W = np.linalg.svd((p - pb).T @ (q - qb))
        R = V @ np.diag([1, 1, np.sign(np.linalg.det(V @ W))]) @ W
        return np.linalg.norm((P - pb) @ R + qb - Q, axis=1)

    mask = np.ones(len(P), bool)
    for _ in range(10):  # iterative 2-sigma rejection -> rigid core
        d = kabsch(mask)
        new = d <= max(d[mask].mean() + 2 * d[mask].std(), 0.5)
        if new.sum() < 0.5 * len(P):
            new = d <= np.quantile(d, 0.5)
        if (new == mask).all():
            break
        mask = new
    return nums, kabsch(np.ones(len(P), bool)), kabsch(mask), int(mask.sum())


def main():
    frozen = json.loads(Path(FROZEN).read_text())["targets"]
    ARMS = sorted(frozen)
    specs = {s["id"]: s for s in load()["targets"]}
    for arm in ARMS:
        sp, fz = specs[arm], frozen[arm]
        ac, hc = sp["apo"]["chain"], sp["holo"]["chain"]
        apo, holo = S(sp["apo"]["pdb"]), S(sp["holo"]["pdb"])
        labels, scoreable, active, nodes = (
            fz["label_residues"],
            fz["scoreable_label_residues"],
            fz["active_site"],
            set(fz["residue_ids"]),
        )
        print("=" * 78)
        print(
            f"{arm}  {sp['apo']['pdb']}:{ac} -> {sp['holo']['pdb']}:{hc}  ({sp['holo']['ligand']})"
        )

        # --- axis 2: what occupies each member's orthosteric site
        h2a = align_numbering(holo, apo, hc, ac)
        holo_active = [h for h, a in h2a.items() if a in set(active)]
        for tag, st, ch, site in (("apo ", apo, ac, active), ("holo", holo, hc, holo_active)):
            tgt = st.protein & (st.chain == ch) & np.isin(st.seq_id, site)
            lig = st.ligand
            d = np.linalg.norm(st.coord[lig][:, None, :] - st.coord[tgt][None, :, :], axis=-1).min(
                1
            )
            near = {}
            for i in np.where(d <= CUT)[0]:
                near.setdefault(str(st.resname[lig][i]), []).append(float(d[i]))
            print(
                f"  orthosteric {tag}: "
                + ", ".join(f"{k} (min {min(v):.2f} A)" for k, v in sorted(near.items()))
            )

        # --- axis 3: coupling geometry, on the apo (the blind input)
        g = site_distance(apo, ac, scoreable, active)
        adj = contact_graph(apo, ac, nodes)
        per = [hops(adj, [r], active) for r in scoreable if r in adj]
        print(
            f"  coupling: min {g['min']} A | mean-over-pairs {g['mean_over_pairs']} A | "
            f"mean-nearest {g['mean_nearest']} A | shortest path {hops(adj, scoreable, active)} hops | "
            f"median {float(np.median(per))} hops | shared residues {sorted(set(labels) & set(active))}"
        )

        # --- axis 4: local vs global response
        nums, dev_g, dev_c, ncore = deviation(sp["apo"]["pdb"], ac, sp["holo"]["pdb"], hc, nodes)
        rest = sorted(set(nums.tolist()) - set(labels) - set(active))
        for frame, dev in (("global", dev_g), ("core  ", dev_c)):
            r = dev[np.isin(nums, rest)]
            line = [
                f"  {frame} (n={len(nums)}, core-fit={ncore}, RMSD {np.sqrt((dev**2).mean()):.2f} A)"
            ]
            for name, s in (("scoreable-labels", scoreable), ("active-site", active)):
                x = dev[np.isin(nums, s)]
                p = mannwhitneyu(x, r, alternative="greater").pvalue
                line.append(f"{name} median {np.median(x):.2f} (p_vs_rest {p:.2g})")
            line.append(f"rest median {np.median(r):.2f}")
            print(" | ".join(line))


if __name__ == "__main__":
    main()
```
