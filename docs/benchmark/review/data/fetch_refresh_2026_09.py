#!/usr/bin/env python3
"""Live RCSB + wwPDB pull for the nine accessions of the SIX frozen primary arms.

Companion to `fetch_structure_evidence.py`, which covered 33 accessions before the
organisers' 2026-09-02 reply moved two arms. This one is narrower and deeper: it adds
the deposited mmCIF for every entry, every assembly, every entity instance and every
chemical component, so per-chain B-factors, occupancies, `_struct_ref_seq` ranges and
`_struct_conn` records can be read from the primary file rather than from a summary.

Raw bytes land in `rcsb-2026-09-refresh/<ID>/`; nothing is interpreted here.
Re-running is cheap — anything already on disk is reused.

Imports nothing from `allo` and names no path outside this directory.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "rcsb-2026-09-refresh"
REST = "https://data.rcsb.org/rest/v1/core"
VAL = "https://files.rcsb.org/pub/pdb/validation_reports"
CIF = "https://files.rcsb.org/download"

# The union of apo and holo accessions over the six primary arms. Written out here
# rather than read, so that this tool names no path outside its own directory.
IDS = ["1OPL", "2G2H", "4LDJ", "4OBE", "5MO4", "5TBY", "6OIM", "9GZ2", "9GZ3"]


def get(url: str, dest: Path, binary: bool = False) -> bytes | None:
    if dest.exists() and dest.stat().st_size:
        return dest.read_bytes()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                body = fh.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            return body
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                print(f"  404 {url}", file=sys.stderr)
                return None
            time.sleep(2 * (attempt + 1))
        except Exception:  # noqa: BLE001 - transient network, retried
            time.sleep(2 * (attempt + 1))
    print(f"  FAILED {url}", file=sys.stderr)
    return None


def get_json(url: str, dest: Path) -> dict | None:
    body = get(url, dest)
    return json.loads(body) if body else None


def main() -> int:
    comps: set[str] = set()
    for pdb in IDS:
        out = CACHE / pdb
        print(pdb)
        entry = get_json(f"{REST}/entry/{pdb}", out / "entry.json")
        if entry is None:
            return 1
        ids = entry.get("rcsb_entry_container_identifiers", {})

        for eid in ids.get("polymer_entity_ids", []):
            ent = get_json(f"{REST}/polymer_entity/{pdb}/{eid}", out / f"polymer_entity_{eid}.json")
            for asym in (
                (ent or {}).get("rcsb_polymer_entity_container_identifiers", {}).get("asym_ids", [])
            ):
                get_json(
                    f"{REST}/polymer_entity_instance/{pdb}/{asym}",
                    out / f"polymer_instance_{asym}.json",
                )

        for eid in ids.get("non_polymer_entity_ids", []):
            ent = get_json(
                f"{REST}/nonpolymer_entity/{pdb}/{eid}",
                out / f"nonpolymer_entity_{eid}.json",
            )
            cid = (ent or {}).get("pdbx_entity_nonpoly", {}).get("comp_id")
            if cid:
                comps.add(cid)
            for asym in (
                (ent or {})
                .get("rcsb_nonpolymer_entity_container_identifiers", {})
                .get("asym_ids", [])
            ):
                get_json(
                    f"{REST}/nonpolymer_entity_instance/{pdb}/{asym}",
                    out / f"nonpolymer_instance_{asym}.json",
                )

        for aid in ids.get("assembly_ids", []):
            get_json(f"{REST}/assembly/{pdb}/{aid}", out / f"assembly_{aid}.json")

        low = pdb.lower()
        get(
            f"{VAL}/{low[1:3]}/{low}/{low}_validation.xml.gz",
            out / "validation.xml.gz",
            binary=True,
        )
        get(f"{CIF}/{pdb}.cif.gz", out / f"{pdb}.cif.gz", binary=True)

    for cid in sorted(comps):
        get_json(f"{REST}/chemcomp/{cid}", CACHE / "_chemcomp" / f"{cid}.json")

    print(f"cached under {CACHE.name}/: {len(IDS)} entries, {len(comps)} components")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
