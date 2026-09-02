"""Self-check: the vectorised JSD must reproduce Capra & Singh's scalar reference.

The reference file is Python 2, so its two scoring functions are transcribed here
line for line from the fetched source and compared on a random alignment.
"""

import math
import random

import jsd as V
import numpy as np

AAS = list(V.AA) + ["-"]
IDX = {a: i for i, a in enumerate(AAS)}
PC = 1e-7
BG = list(V.BG)


def ref_weights(msa):
    w = [0.0] * len(msa)
    for i in range(len(msa[0])):
        fc = [0] * len(AAS)
        for j in range(len(msa)):
            if msa[j][i] != "-":
                fc[IDX[msa[j][i]]] += 1
        types = sum(1 for x in fc if x > 0)
        for j in range(len(msa)):
            d = fc[IDX[msa[j][i]]] * types
            if d > 0:
                w[j] += 1.0 / d
    return [x / len(msa[0]) for x in w]


def ref_jsd(col, w):
    fc = [PC] * len(AAS)
    for k, aa in enumerate(AAS):
        for j in range(len(col)):
            if col[j] == aa:
                fc[k] += w[j]
    fc = [x / (sum(w) + len(AAS) * PC) for x in fc]
    fc = fc[:-1]
    s = sum(fc)
    fc = [x / s for x in fc]
    r = [0.5 * fc[i] + 0.5 * BG[i] for i in range(20)]
    d = 0.0
    for i in range(20):
        if r[i] != 0.0:
            if fc[i] == 0.0:
                d += BG[i] * math.log(BG[i] / r[i], 2)
            elif BG[i] == 0.0:
                d += fc[i] * math.log(fc[i] / r[i], 2)
            else:
                d += fc[i] * math.log(fc[i] / r[i], 2) + BG[i] * math.log(BG[i] / r[i], 2)
    d /= 2
    gap = sum(w[i] for i in range(len(col)) if col[i] == "-")
    return d * (1 - gap / sum(w))


random.seed(0)
msa = ["".join(random.choice(AAS) for _ in range(37)) for _ in range(45)]
M = V.encode(msa)
wv, wr = V.henikoff(M), np.array(ref_weights(msa))
assert np.allclose(wv, wr, atol=1e-12), f"weights differ: {np.abs(wv - wr).max()}"
sv = V.jsd(M, wv)
sr = np.array([ref_jsd([m[i] for m in msa], list(wr)) for i in range(len(msa[0]))])
assert np.allclose(sv, sr, atol=1e-10), f"jsd differs: {np.abs(sv - sr).max()}"
print(
    f"OK  weights max|diff|={np.abs(wv - wr).max():.2e}  jsd max|diff|={np.abs(sv - sr).max():.2e}"
)
