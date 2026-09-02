"""Monte-Carlo power of the decoy-pocket test. No closed form exists for it.

Model. Each detected pocket gets one number: the mean midrank of its lining. Under the
alternative the site pocket's number is shifted by delta standard deviations relative to
the decoy pockets' distribution. The frozen test is

    p = (1 + #{decoy >= site}) / (1 + n_decoys)

which is exact and one-sided. Power is P(p <= threshold). The ceiling is structural: at
delta = infinity the site is always largest and p = 1/(1 + n_decoys).
"""

from math import ceil

import numpy as np

rng = np.random.default_rng(0)
B = 20000


def power(n, delta, alpha):
    if 1.0 / (1 + n) > alpha:  # structural ceiling: cannot reject at any effect size
        return 0.0
    site = rng.normal(delta, 1.0, B)
    dec = rng.normal(0.0, 1.0, (B, n))
    p = (1 + (dec >= site[:, None]).sum(1)) / (1 + n)
    return float((p <= alpha + 1e-12).mean())


print("Minimum decoys needed for the test to be able to reject at all")
for a, nm in ((0.05, "alpha"), (0.025, "alpha/2"), (0.05 / 3, "alpha/3")):
    print(f"  {nm:8s} threshold {a:.5f}  ->  n_decoys >= {ceil(1 / a) - 1}")

MEASURED = {
    "kras_g12c_corrected      frozen": 3,
    "kras_g12c_corrected      rd1.2": 7,
    "kras_g12c_corrected      loosest": 18,
    "bcr_abl1_corrected       frozen": 9,
    "bcr_abl1_corrected       rd1.2": 22,
    "bcr_abl1_corrected       loosest": 31,
    "cardiac_myosin_corrected frozen": 41,
    "cardiac_myosin_corrected rd1.2": 71,
    "cardiac_myosin_corrected loosest": 84,
}
print("\nPower at the measured decoy counts (threshold alpha = 0.05)")
print(
    f"{'arm / setting':36s} {'n':>4s}"
    + "".join(f"{f'd={d}':>9s}" for d in (0.5, 1.0, 1.5, 2.0, 3.0))
    + f"{'ceiling':>9s}"
)
for k, n in MEASURED.items():
    row = "".join(f"{power(n, d, 0.05):>9.3f}" for d in (0.5, 1.0, 1.5, 2.0, 3.0))
    print(f"{k:36s} {n:>4d}{row}{1 / (1 + n):>9.4f}")

print("\nPower at Holm's tightest step (threshold alpha/3 = 0.01667)")
print(
    f"{'arm / setting':36s} {'n':>4s}"
    + "".join(f"{f'd={d}':>9s}" for d in (0.5, 1.0, 1.5, 2.0, 3.0))
)
for k, n in MEASURED.items():
    row = "".join(f"{power(n, d, 0.05 / 3):>9.3f}" for d in (0.5, 1.0, 1.5, 2.0, 3.0))
    print(f"{k:36s} {n:>4d}{row}")

print("\nDecoys required for 80 % power, by effect size, at alpha = 0.05")
print(f"{'delta':>6s} {'n_decoys':>9s}")
for d in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
    need = None
    for n in list(range(19, 400, 1)):
        if power(n, d, 0.05) >= 0.80:
            need = n
            break
    print(f"{d:>6.1f} {str(need) if need else '>400':>9s}")
