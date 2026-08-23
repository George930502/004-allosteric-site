"""Evaluation-side structure resolution, including holo coordinates (C1)."""

from __future__ import annotations

import gzip
import re
import urllib.request
from pathlib import Path

from Bio.PDB.MMCIF2Dict import MMCIF2Dict

from allo.groundtruth.manifest import read_manifest
from allo.structure.pdb import Structure, parse_mmcif_text

ROOT = Path(__file__).resolve().parents[3]
STRUCTURES = ROOT / "structures"

# Where evaluation caches the structures it restores -- both halves of every pair, so it is
# holo-bearing by design and must not be the directory a method reads from. `allo.inputs`
# caches apo separately under `APO_CACHE`; nothing on the prediction path names this one.
EVAL_CACHE = ROOT / "data" / "raw" / "eval"

RCSB_FILE = "https://files.rcsb.org/download/{pdb_id}.cif"
_UA = {"User-Agent": "allo-benchmark/0.1 (+https://github.com/George930502/004-allosteric-site)"}


def parse_mmcif(path: Path, pdb_id: str | None = None) -> Structure:
    """Open and parse an evaluation-side structure, including holo coordinates."""
    return parse_mmcif_text(path.read_text(), pdb_id or path.stem)


def biological_assembly(path: Path, chain: str, assembly_id: str = "1") -> dict[str, object]:
    """Derive a selected chain's biological assembly from pinned mmCIF metadata."""
    data = MMCIF2Dict(str(path))

    def values(key: str) -> list[str]:
        value = data.get(key, [])
        return value if isinstance(value, list) else [value]

    def operation_count(expression: str) -> int:
        groups = re.findall(r"\(([^()]*)\)", expression) or [expression]
        count = 1
        for group in groups:
            members = 0
            for part in group.split(","):
                part = part.strip()
                if re.fullmatch(r"\d+-\d+", part):
                    start, end = map(int, part.split("-"))
                    members += end - start + 1
                elif part:
                    members += 1
            count *= members
        return count

    polymer_asym: dict[str, str] = {}
    selected_asym: set[str] = set()
    for auth, asym, entity, seq in zip(
        values("_atom_site.auth_asym_id"),
        values("_atom_site.label_asym_id"),
        values("_atom_site.label_entity_id"),
        values("_atom_site.label_seq_id"),
        strict=True,
    ):
        if seq in {".", "?"}:
            continue
        polymer_asym[asym] = entity
        if auth == chain:
            selected_asym.add(asym)
    if not selected_asym:
        raise ValueError(f"{path.stem}:{chain} is absent from polymer atom_site records")

    composition: dict[str, int] = {}
    selected_entities = {polymer_asym[asym] for asym in selected_asym}
    found = False
    for row_id, expression, asym_list in zip(
        values("_pdbx_struct_assembly_gen.assembly_id"),
        values("_pdbx_struct_assembly_gen.oper_expression"),
        values("_pdbx_struct_assembly_gen.asym_id_list"),
        strict=True,
    ):
        if row_id != assembly_id:
            continue
        found = True
        multiplier = operation_count(expression)
        included = set(asym_list.replace(" ", "").split(","))
        for asym in included & set(polymer_asym):
            entity = polymer_asym[asym]
            composition[entity] = composition.get(entity, 0) + multiplier
    selected_copies = sum(composition.get(entity, 0) for entity in selected_entities)
    if not found or not selected_copies:
        raise ValueError(f"{path.stem}:{chain} is absent from biological assembly {assembly_id}")
    return {
        "id": assembly_id,
        "polymer_entity_copies": dict(sorted(composition.items())),
        "selected_chain_entity_copies": selected_copies,
    }


def fetch_mmcif(pdb_id: str, dest_dir: Path) -> Path:
    """Restore one evaluation structure from cache, partitioned store, or pinned archive."""
    pdb_id = pdb_id.upper()
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{pdb_id}.cif"
    if path.exists():
        return path
    for partition in ("apo", "holo"):
        archived = STRUCTURES / partition / f"{pdb_id}.cif.gz"
        if archived.exists():
            path.write_bytes(gzip.decompress(archived.read_bytes()))
            return path

    provenance = read_manifest().get("structure_provenance", {}).get(pdb_id)
    url = provenance["url"] if provenance else RCSB_FILE.format(pdb_id=pdb_id)
    request = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310
        payload = response.read()
    path.write_bytes(gzip.decompress(payload) if url.endswith(".gz") else payload)
    return path
