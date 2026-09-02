"""Non-functional surface pockets: the second negative class `CHALLENGE.md` requires.

Section 4.1 asks for enrichment against **random background residues and non-functional
surface pockets**. The first is `nulls.py`. This is the second, and it needs a geometric
pocket detector.

**Why a detector at all, when the matched-patch null already samples compact contiguous
residue sets.** Two reasons, and neither is presentation. First, the challenge names
pockets, not synthetic patches. Second, the field's near-universal convention for site
prediction is a *pocket* rank cutoff -- APOP states it as "If this pocket is among the
top-ranked three predicted pockets, we count it as a success" (APOP,
doi:10.1093/bioinformatics/btad275) -- so without a detector
there is no number in our report that a reader can put beside PASSer, APOP or DeepAllo.
One detection run supplies both.

**Which detector, and the argument for it.** pyKVFinder (doi:10.1186/s12859-021-04519-4),
at the package's documented defaults for the pinned version -- the paper states none of
the five values, so the version is the citation for them. The deciding argument is that it is purely
geometric, so it raises no C2 question, and that it is installable and versioned, so the
configuration below is reproducible. Version discipline in this literature is close to
absent -- of the allosteric papers surveyed, one states a detector version -- so stating
ours in full is a low bar that is nonetheless above the field's.

**Its limits, stated rather than found later.** SiteFerret's published objection
(doi:10.1021/acs.jctc.2c01306) to any
detector-derived negative set applies here: it is "conceptually unsatisfactory since: i) it
is method-specific ...; ii) false negatives cannot be ruled out". A pocket labelled
non-functional here is a pocket with no *known* function. The halo below is the mitigation,
not a refutation.

Everything in this module runs on the apo input alone. The label set enters only to
classify a detected pocket as the site or as a decoy, which happens at freeze time on the
evaluation side.
"""

from __future__ import annotations

import numpy as np

from allo.inputs import ApoInput

__all__ = [
    "DETECTOR_DEFAULTS",
    "DETECTOR_VERSION",
    "cavity_volume_score",
    "classify",
    "detect_pockets",
]

# Asserted at detection time, not merely written down. `manifest.yaml` carries the same
# string; `tests/test_scoring.py` checks the two agree.
DETECTOR_VERSION = "0.9.3"

# The package's documented defaults for DETECTOR_VERSION, written out rather than omitted.
# The cited paper states none of them, which is why the version is asserted above.
# Choosing the defaults is the choice not to tune a detector on the benchmark it will score.
DETECTOR_DEFAULTS = {
    "step": 0.6,
    "probe_in": 1.4,
    "probe_out": 4.0,
    "removal_distance": 2.4,
    "volume_cutoff": 5.0,
}


def detect_pockets(apo: ApoInput, **parameters) -> dict[str, dict]:
    """Detect surface pockets on the frozen apo node set. Returns id -> lining and volume.

    Runs on exactly what a method receives: one chain, ligand-free, modified residues
    normalised. A pocket found here is therefore a pocket a method could have found.
    """
    import pyKVFinder  # optional `eval` extra; only re-deriving the freeze needs it

    # The manifest pins the version, and pinning it in prose is not pinning it. pyproject
    # permits any 0.9.x, so a lock refresh would silently re-derive different linings and
    # `verify --detect` would report the diff as drift with no hint that the detector moved.
    # Version discipline is the only mitigation available for a detector-derived negative
    # set (SiteFerret, doi:10.1021/acs.jctc.2c01306), so it has to be enforced.
    if pyKVFinder.__version__ != DETECTOR_VERSION:
        raise RuntimeError(
            f"pyKVFinder {pyKVFinder.__version__} is installed, the freeze pins "
            f"{DETECTOR_VERSION}. Re-deriving the decoys under another version changes them."
        )

    # NOT `DETECTOR_DEFAULTS`. ADR 0030 re-froze the detector on 2026-09-02 and three of
    # the five values moved off the package defaults, so a caller who forgot to pass the
    # frozen settings silently got version-2 pockets. Round 6 found the trap. The base is
    # now what the manifest froze, and `DETECTOR_DEFAULTS` is kept only to record what was
    # withdrawn.
    from allo.scoring.harness import protocol

    settings = protocol()["decoys"]["detector_settings"] | parameters
    structure = apo.structure
    mask = structure.protein
    vdw = pyKVFinder.read_vdw()
    generic = vdw["GEN"]

    def radius(resname: str, atom: str, element: str) -> float:
        return vdw.get(resname, generic).get(atom, generic.get(element, 1.7))

    atomic = np.array(
        [
            [str(seq), chain, resname, atom, x, y, z, radius(resname, atom, element)]
            for seq, chain, resname, atom, element, (x, y, z) in zip(
                structure.seq_id[mask],
                structure.chain[mask],
                structure.resname[mask],
                structure.atom[mask],
                structure.element[mask],
                structure.coord[mask],
                strict=True,
            )
        ],
        dtype=object,
    )
    vertices = pyKVFinder.get_vertices(atomic)
    _, cavities = pyKVFinder.detect(atomic, vertices, **settings)
    _, volume, _ = pyKVFinder.spatial(cavities)
    lining = pyKVFinder.constitutional(cavities, atomic, vertices)
    return {
        name: {
            "lining": sorted({int(entry[0]) for entry in residues}),
            "volume": round(float(volume[name]), 2),
        }
        for name, residues in sorted(lining.items())
    }


def classify(
    pockets: dict[str, dict],
    *,
    labels,
    candidates,
    ca_coord: dict[int, np.ndarray],
    halo_angstrom: float,
) -> dict:
    """Split detected pockets into the site pocket and the decoys.

    * Every lining is first restricted to the **candidate set**: a residue that scores by
      construction leaves both classes, and a pocket lining is no exception (ADR 0011). A
      pocket with nothing left is dropped.
    * The **site pocket** is the one covering the most label residues. It is a description
      of what the detector found, not a prediction, and it is what makes the field's
      pocket-rank convention computable here.
    * A pocket is a **decoy** only if its lining holds no label and no residue within
      `halo_angstrom` of one. Without the halo, a pocket bordering the true site counts as
      a negative and a method is penalised for being nearly right.

    A pocket that is neither -- inside the halo but not the site pocket -- is **excluded**
    from both classes and counted, because silently folding it into either would move the
    number.
    """
    labels = set(labels)
    inside = set(candidates)
    label_coords = np.array([ca_coord[r] for r in sorted(labels)])

    site, best_cover, decoys, excluded = None, -1, {}, {}
    trimmed = {}
    for name, pocket in pockets.items():
        lining = sorted(set(pocket["lining"]) & inside)
        if not lining:
            continue
        trimmed[name] = dict(pocket, lining=lining)
        cover = len(set(lining) & labels)
        if cover > best_cover:
            site, best_cover = name, cover

    for name, pocket in trimmed.items():
        if name == site:
            continue
        coords = np.array([ca_coord[r] for r in pocket["lining"]])
        near = np.linalg.norm(coords[:, None, :] - label_coords[None, :, :], axis=-1).min()
        if set(pocket["lining"]) & labels or near <= halo_angstrom:
            excluded[name] = dict(pocket, nearest_label_angstrom=round(float(near), 3))
        else:
            decoys[name] = dict(pocket, nearest_label_angstrom=round(float(near), 3))

    site_pocket = trimmed.get(site, {"lining": [], "volume": 0.0})
    return {
        "n_detected": len(pockets),
        "n_scoreable": len(trimmed),
        "site_pocket": {
            "id": site,
            "lining": site_pocket["lining"],
            "volume": site_pocket["volume"],
            "labels_covered": best_cover if site else 0,
            "label_coverage": round(best_cover / len(labels), 4) if site and labels else 0.0,
        },
        "decoys": decoys,
        "excluded_by_halo": excluded,
        "minimum_attainable_p": round(1 / (1 + len(decoys)), 6) if decoys else None,
    }


def cavity_volume_score(pockets: dict[str, dict], candidates) -> dict[int, float]:
    """Score each candidate by the volume of the largest detected cavity that lines it.

    Label-blind, apo-only, zero-parameter, and it uses the detector the freeze already pins.
    A required baseline. Under protocol **version 2** it cleared the confirmatory family
    outright, rejecting on all three arms, and that is why the claim threshold is beating
    this score rather than clearing the matched-patch null (ADR 0025). **Under version 3 it
    rejects on ONE arm of three** — `p_calibrated` 0.0046, 0.0715, 0.3236, Holm over three.
    The cause is mechanical: ADR 0030 re-froze the detector, and this score is computed from
    that detector's cavities, so re-freezing the decoys moved the baseline the claim is
    measured against. The rule is unchanged and the numbers behind it are not; do not write
    that this baseline sweeps the family (`../../../docs/benchmark/evaluation/manifest.yaml`).

    It is the field's own control too. "Rank by detector score alone" is the reference both
    PASSer2.0 (doi:10.1093/nar/gkad303) and DeepAllo (doi:10.1093/bioinformatics/btaf294)
    report against.

    Lives here because the detector does, and because it is the ninth of the nine baselines
    the frozen protocol requires. The other eight are in `allo.scoring.baselines` (ADR 0037).
    """
    score = dict.fromkeys(candidates, 0.0)
    for pocket in pockets.values():
        for residue in pocket["lining"]:
            if residue in score:
                score[residue] = max(score[residue], float(pocket["volume"]))
    return score
