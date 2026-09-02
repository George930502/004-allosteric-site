"""Per-column Jensen-Shannon divergence, Capra & Singh (doi:10.1093/bioinformatics/btm270).

Vectorised reimplementation of `score_conservation.py`, fetched 2026-09-02 from the
authors' own site at https://compbio.cs.princeton.edu/conservation/score_conservation.py.
Every constant below is read from that file, not recalled:
  amino_acids            line 66   ARNDCQEGHILKMFPSTWYV plus '-'
  PSEUDOCOUNT = 1e-7     line 64
  blosum_background_distr line 585
  window_size = 0        line 597  (ADR 0035 keeps the window off; the reference default is off too)
Sequence cleaning follows lines 524/555: uppercase, B->D, Z->Q, X->'-'.
"""

from __future__ import annotations

import gzip

import numpy as np

AA = "ARNDCQEGHILKMFPSTWYV"  # reference order, line 66
GAP = len(AA)  # index 20 == '-'
NSYM = GAP + 1
PSEUDOCOUNT = 1e-7  # line 64
BG = np.array(
    [
        0.078,
        0.051,
        0.041,
        0.052,
        0.024,
        0.034,
        0.059,
        0.083,
        0.025,
        0.062,
        0.092,
        0.056,
        0.024,
        0.044,
        0.043,
        0.059,
        0.055,
        0.014,
        0.034,
        0.072,
    ]
)  # line 585

_LUT = np.full(256, GAP, dtype=np.uint8)
for i, a in enumerate(AA):
    _LUT[ord(a)] = i
_LUT[ord("B")] = AA.index("D")
_LUT[ord("Z")] = AA.index("Q")
# X, U, O, *, '-' and anything else fall through to GAP, as the reference does for X.


def encode(rows: list[str]) -> np.ndarray:
    """(n_seq, n_col) uint8 of indices into AA, gap/unknown == GAP."""
    buf = np.frombuffer("".join(rows).encode("ascii", "replace"), dtype=np.uint8)
    return _LUT[buf].reshape(len(rows), -1)


def henikoff(M: np.ndarray) -> np.ndarray:
    """Henikoff & Henikoff 1994 weights, as `calculate_sequence_weights` computes them."""
    n_seq, n_col = M.shape
    w = np.zeros(n_seq, dtype=np.float64)
    for start in range(0, n_col, 256):  # blocked, to bound memory
        blk = M[:, start : start + 256]
        counts = np.zeros((blk.shape[1], NSYM), dtype=np.int64)
        for s in range(NSYM):
            counts[:, s] = (blk == s).sum(axis=0)
        counts[:, GAP] = 0  # "ignore gaps"
        types = (counts > 0).sum(axis=1)  # num_observed_types
        c = counts[np.arange(blk.shape[1])[None, :], blk]
        d = c * types[None, :]
        w += np.where(d > 0, 1.0 / np.maximum(d, 1), 0.0).sum(axis=1)
    return w / n_col


def jsd(M: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Per-column JSD against the BLOSUM62 background, with the reference gap penalty."""
    n_seq, n_col = M.shape
    out = np.empty(n_col, dtype=np.float64)
    wsum = w.sum()
    for start in range(0, n_col, 512):
        blk = M[:, start : start + 512]
        fc = np.zeros((blk.shape[1], NSYM), dtype=np.float64)
        for s in range(NSYM):
            fc[:, s] = ((blk == s) * w[:, None]).sum(axis=0)
        fc += PSEUDOCOUNT
        fc /= wsum + NSYM * PSEUDOCOUNT
        p = fc[:, :GAP]  # drop the gap slot
        p = p / p.sum(axis=1, keepdims=True)  # renormalise, as the reference does
        r = 0.5 * p + 0.5 * BG[None, :]
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = np.where(
                p > 0, p * np.log2(np.divide(p, r, out=np.ones_like(p), where=r > 0)), 0.0
            )
            t2 = np.where(BG[None, :] > 0, BG[None, :] * np.log2(BG[None, :] / r), 0.0)
        d = (t1 + t2).sum(axis=1) / 2.0
        gap_w = ((blk == GAP) * w[:, None]).sum(axis=0) / wsum
        out[start : start + blk.shape[1]] = d * (1.0 - gap_w)
    return out


def read_stockholm(path: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return (rows: name -> aligned string, gs_ac: name -> UniProt accession)."""
    rows: dict[str, list[str]] = {}
    order: list[str] = []
    gs: dict[str, str] = {}
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("//"):
                continue
            if line.startswith("#=GS "):
                parts = line.split(None, 3)
                if len(parts) >= 4 and parts[2] == "AC":
                    gs[parts[1]] = parts[3].strip().split(".")[0]
                continue
            if line.startswith("#"):
                continue
            name, _, seq = line.partition(" ")
            seq = seq.strip()
            if not seq:
                continue
            if name not in rows:
                rows[name] = []
                order.append(name)
            rows[name].append(seq)
    return {n: "".join(rows[n]) for n in order}, gs


def match_columns(rows: dict[str, str]) -> np.ndarray:
    """Pfam Stockholm: match columns are uppercase or '-'; inserts are lowercase or '.'."""
    sample = next(iter(rows.values()))
    arr = np.frombuffer(sample.encode("ascii", "replace"), dtype=np.uint8)
    return ~((arr >= ord("a")) & (arr <= ord("z")) | (arr == ord(".")))
