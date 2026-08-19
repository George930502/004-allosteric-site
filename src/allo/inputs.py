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

from allo.structure.pdb import Structure, contacts, fetch_mmcif, parse_mmcif

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


def load(path: Path = MANIFEST) -> dict:
    return yaml.safe_load(path.read_text())


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


def apo_input(target: str, manifest: dict | None = None, raw: Path = RAW) -> ApoInput:
    """Load one frozen target's apo input. The only supported way for a method to start.

    Re-deriving the residue list per method is how two methods end up silently scored
    on different node sets; this returns the same list to all of them.
    """
    manifest = manifest or load()
    specs = {s["id"]: s for s in manifest["targets"]}
    if target not in specs:
        raise KeyError(f"{target!r} is not a frozen target; have {sorted(specs)}")
    spec = specs[target]
    if spec.get("status") == "excluded":
        raise ValueError(f"{target} is excluded from the freeze: {spec.get('defect', '')}")
    cutoff = manifest["defaults"]["contact_cutoff_angstrom"]
    chain = spec["apo"]["chain"]
    apo = parse_mmcif(fetch_mmcif(spec["apo"]["pdb"], raw), spec["apo"]["pdb"])
    return ApoInput(
        target=target,
        pdb_id=spec["apo"]["pdb"],
        chain=chain,
        structure=apo,
        residues=sorted(number for c, number, _ in apo.residues() if c == chain),
        active_site=active_site(apo, chain, spec["active_site"], cutoff),
        cutoff=cutoff,
    )
