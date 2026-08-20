"""The frozen input layer: everything a method is allowed to see, and nothing else.

Separate from `allo.benchmark` for one reason. `benchmark` holds both halves of the
pair — the apo inputs *and* the holo-derived labels — so it must import
`allo.groundtruth`, so it must sit on the evaluation side of the C1 firewall. A method
that needed the manifest or the propagation source would have had to import it, and
would have dragged the answer key across with it (`tests/test_no_leakage.py`).

So the apo-only half lives here. This module never imports `allo.groundtruth`, which
is what makes it safe for `network/`, `quantum/` and `classical/` to depend on, and
what makes "every method saw identical inputs" a checkable statement rather than a
promise.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from allo.structure.pdb import Structure, contacts, fetch_mmcif, parse_mmcif, sha256

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "benchmark" / "manifest.yaml"
RAW = ROOT / "data" / "raw"

# Conserved catalytic motifs, for the targets whose apo entry holds no cofactor (ADR 0005).
# Patterns are matched against the modelled chain sequence, so the residue numbers come out
# in whatever numbering convention that entry uses — which is the point: ABL1 is deposited
# under two, 19 apart, and a hand-written list is only ever right for one of them.
CATALYTIC_MOTIFS = {"VAIK": r"[VLIA]A[VLIA]K", "HRD": r"H[RG][DN][LIVM]", "DFG": r"D[FWY]G"}

_THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
    "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
    "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    # modified residues seen in the benchmark targets, mapped to their parent
    "MSE": "M", "M3L": "K", "SEP": "S", "TPO": "T", "PTR": "Y",
}  # fmt: skip


# Fields of a manifest target that describe the *answer* rather than the input. Every one
# of them is holo-derived, and three of them spell out label residue numbers in prose --
# `blind.why` names KRAS 68/95/96/99, `defect` names "16 of the 20 distal labels", `note`
# gives Site 2's full label-to-active-site distribution. An import trace cannot see a module
# that simply calls `load()`, so the redaction is what stops it, not the allow-list.
_HOLO_SIDE = frozenset({"holo", "defect", "note", "blind", "allosteric_evidence", "state"})


def load(path: Path = MANIFEST) -> dict:
    """The manifest as **prediction code** may see it: the apo half, and nothing else.

    C1 says holo data may not reach the prediction path. `allo.inputs` is the one
    prediction-path module that has to open the manifest at all — it needs the chain and
    the active-site rule — so it is also the place the answer key has to be stripped, and
    it strips by allow-list so a field added later is redacted by default rather than
    leaked by default. The verbatim read is `allo.groundtruth.manifest.read_manifest`,
    behind the import guard; this module never exposes one (`tests/test_no_leakage.py`).

    `site` survives redaction deliberately: it is a human label ("Switch-II pocket"), and
    `CHALLENGE.md` Table 1 gives it to every participant, so it is not ours to withhold.
    """
    manifest = yaml.safe_load(path.read_text())
    manifest["targets"] = [
        {k: v for k, v in target.items() if k not in _HOLO_SIDE} for target in manifest["targets"]
    ]
    return manifest


def one_letter(residues: list[tuple[str, int, str]]) -> str:
    return "".join(_THREE_TO_ONE.get(name, "X") for _, _, name in residues)


def active_site(apo: Structure, chain: str, rule: dict, cutoff: float) -> list[int]:
    """The propagation source, derived from the apo entry alone (C1, ADR 0005)."""
    if "from_ligands" in rule:
        source = apo.ligand & np.isin(apo.resname, rule["from_ligands"]) & (apo.chain == chain)
        if not source.any():
            raise ValueError(f"{apo.pdb_id}:{chain} holds none of {rule['from_ligands']}")
        target = apo.protein & (apo.chain == chain)
        return sorted(number for _, number, _ in contacts(apo, source, target, cutoff))

    residues = [r for r in apo.residues() if r[0] == chain]
    sequence = one_letter(residues)
    found: list[int] = []
    for name in rule["from_motifs"]:
        matches = list(re.finditer(CATALYTIC_MOTIFS[name], sequence))
        if len(matches) != 1:
            raise ValueError(
                f"{apo.pdb_id}:{chain} motif {name} matched {len(matches)} times, expected 1"
            )
        span = matches[0]
        found += [residues[i][1] for i in range(span.start(), span.end())]
    return sorted(found)


@dataclass(frozen=True)
class ApoInput:
    """What a method receives. Identical for every method, by construction."""

    target: str
    pdb_id: str
    chain: str
    structure: Structure
    residues: list[int]
    active_site: list[int]
    cutoff: float


def apo_input(target: str, raw: Path = RAW) -> ApoInput:
    """Load one frozen target's apo input. The only supported way for a method to start.

    Re-deriving the residue list per method is how two methods end up silently scored
    on different node sets; this returns the same list to all of them.

    **There is no `manifest` parameter, deliberately.** It used to take one, and an
    adversarial review pointed out that the hash check below was then verifying
    caller-supplied bytes against caller-supplied metadata: hand it a manifest mapping
    `kras_g12c_mandated` to `4LDJ` with `4LDJ`'s real hash and it returned `4LDJ` as the
    mandated input, every guard green. "Every method saw identical inputs" has to be true by
    construction, so the accession, chain, active-site rule, cutoff and hash all come from
    the repository-pinned manifest and a caller cannot substitute any of them. `raw` stays
    open because it only says *where to cache*, and the hash check covers the bytes.
    """
    manifest = load()
    specs = {s["id"]: s for s in manifest["targets"]}
    if target not in specs:
        raise KeyError(f"{target!r} is not a frozen target; have {sorted(specs)}")
    spec = specs[target]
    if spec.get("status") == "excluded":
        raise ValueError(f"{target} is excluded from the freeze: {spec.get('defect', '')}")
    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    chain = spec["apo"]["chain"]
    path = fetch_mmcif(spec["apo"]["pdb"], raw)
    # Fail closed on the bytes, not just on the accession. `data/raw/` is gitignored and
    # `fetch_mmcif` returns whatever is already cached, so a clean clone after an RCSB
    # revision -- or a stale cache -- would silently run a method on different coordinates
    # and only `allo benchmark verify`, a command a method run never invokes, would notice.
    # A frozen input layer that re-downloads its input is not frozen.
    expected = spec["apo"].get("sha256")
    if not expected:
        raise ValueError(f"{target}: manifest pins no apo sha256; refusing to run unpinned")
    if (actual := sha256(path)) != expected:
        raise ValueError(
            f"{target}: {spec['apo']['pdb']} is not the frozen file -- expected {expected}, "
            f"got {actual}. RCSB may have re-versioned it; re-freeze deliberately or delete "
            f"{path} and refetch."
        )
    apo = parse_mmcif(path, spec["apo"]["pdb"])
    return ApoInput(
        target=target,
        pdb_id=spec["apo"]["pdb"],
        chain=chain,
        structure=apo,
        residues=sorted(number for c, number, _ in apo.residues() if c == chain),
        active_site=active_site(apo, chain, spec["active_site"], cutoff),
        cutoff=cutoff,
    )
