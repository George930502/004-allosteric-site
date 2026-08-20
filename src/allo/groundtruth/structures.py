"""Evaluation-side structure resolution, including holo coordinates (C1)."""

from __future__ import annotations

import gzip
import urllib.request
from pathlib import Path

from allo.groundtruth.manifest import read_manifest

STRUCTURES = Path(__file__).resolve().parents[3] / "structures"
RCSB_FILE = "https://files.rcsb.org/download/{pdb_id}.cif"
_UA = {"User-Agent": "allo-benchmark/0.1 (+https://github.com/George930502/004-allosteric-site)"}


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
