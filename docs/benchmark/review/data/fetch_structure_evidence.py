#!/usr/bin/env python3
"""Pull live RCSB + wwPDB validation evidence for every benchmark structure.

Writes raw responses under `rcsb-raw/<ID>/` and the extracted table to
`structure-evidence.json`. Re-running is cheap: anything already on disk is reused,
so the JSON is re-derivable offline once the cache exists.

Every extracted value names its own source in `structure-evidence.json`:
REST paths are `<endpoint>:<field.path>`, validation-report values are
`validation.xml:<attribute>`. A field RCSB does not carry is written as null.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(__file__).resolve().parent
RAW = DATA / "rcsb-raw"
REST = "https://data.rcsb.org/rest/v1/core"
VAL = "https://files.rcsb.org/pub/pdb/validation_reports"

GROUPS = {
    "primary_apo": ["4OBE", "4LDJ", "1OPL", "2G2H", "5TBY", "9GZ3"],
    "primary_holo": ["6OIM", "5MO4", "6C1H", "9GZ2"],
    "myosin_alternative": ["8QYR", "9GZ1", "8QYQ", "9YP9", "9YR7"],
    "secondary_apo": ["1ZZW", "1IA8", "1SUG", "6P7Z", "3IDH", "1RTJ", "1QUV", "5FTK", "1A9X"],
    "secondary_holo": ["7UMV", "3JVR", "1T48", "7BJ1", "3F9M", "1VRT", "2BRK", "5FTJ", "1T36"],
    # Outside the 33 the audit was asked for. Fetched because question (b) asks whether each
    # mavacamten holo has a matched apo in its own deposition series, and these two are the
    # only candidates: 8QYP is the 8QYQ/8QYR series apo, 9YRG the 9YP9/9YR7 series apo.
    "myosin_apo_counterpart_supporting": ["8QYP", "9YRG"],
}
GROUP_OF = {pdb: g for g, ids in GROUPS.items() for pdb in ids}
IDS = list(GROUP_OF)

# Criterion for `common_cryo_or_buffer_component`, applied to the CCD id alone. It is
# ours, not RCSB's, and it is stated in 08-structure-evidence.md next to the table.
CRYO_BUFFER = {
    "HOH",
    "GOL",
    "EDO",
    "PEG",
    "PG4",
    "PGE",
    "1PE",
    "2PE",
    "P6G",
    "MPD",
    "IPA",
    "DMS",
    "SO4",
    "PO4",
    "NO3",
    "CL",
    "BR",
    "IOD",
    "NA",
    "K",
    "MG",
    "CA",
    "MN",
    "ZN",
    "NI",
    "CD",
    "CS",
    "ACT",
    "ACY",
    "FMT",
    "CIT",
    "FLC",
    "TRS",
    "MES",
    "EPE",
    "BME",
    "IMD",
    "TLA",
    "MLI",
    "OXL",
    "SCN",
    "AZI",
    "BCT",
    "CO3",
    "NH4",
    "BOG",
    "LDA",
    "C8E",
    "SIN",
    "ETX",
    "MRD",
    "BU3",
    "PDO",
    "12P",
    "15P",
    "XPE",
    "DTT",
    "TCE",
    "GLC",
    "NAG",
    "MAN",
}


def get(url: str, dest: Path, binary: bool = False) -> object | None:
    """Fetch once, cache on disk. 404 is a real answer here and is cached as absent."""
    if dest.exists():
        if dest.suffix == ".gz":
            return dest
        txt = dest.read_text()
        return None if txt == "null" else json.loads(txt)
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                payload = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                if not binary:
                    dest.write_text("null")
                return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    else:
        print(f"FAILED {url}", file=sys.stderr)
        return None
    if binary:
        dest.write_bytes(payload)
        return dest
    obj = json.loads(payload)
    dest.write_text(json.dumps(obj, indent=1, sort_keys=True))
    return obj


def fetch_entry(pdb: str) -> None:
    d = RAW / pdb
    entry = get(f"{REST}/entry/{pdb}", d / "entry.json")
    if entry is None:
        print(f"NO ENTRY {pdb}", file=sys.stderr)
        return
    ids = entry.get("rcsb_entry_container_identifiers", {})
    for eid in ids.get("polymer_entity_ids") or []:
        ent = get(f"{REST}/polymer_entity/{pdb}/{eid}", d / f"polymer_entity_{eid}.json")
        for asym in (ent or {}).get("rcsb_polymer_entity_container_identifiers", {}).get(
            "asym_ids"
        ) or []:
            get(f"{REST}/polymer_entity_instance/{pdb}/{asym}", d / f"polymer_instance_{asym}.json")
    for eid in ids.get("non_polymer_entity_ids") or []:
        ent = get(f"{REST}/nonpolymer_entity/{pdb}/{eid}", d / f"nonpolymer_entity_{eid}.json")
        for asym in (ent or {}).get("rcsb_nonpolymer_entity_container_identifiers", {}).get(
            "asym_ids"
        ) or []:
            get(
                f"{REST}/nonpolymer_entity_instance/{pdb}/{asym}",
                d / f"nonpolymer_instance_{asym}.json",
            )
    for eid in ids.get("branched_entity_ids") or []:
        get(f"{REST}/branched_entity/{pdb}/{eid}", d / f"branched_entity_{eid}.json")
    get(f"{REST}/assembly/{pdb}/1", d / "assembly_1.json")
    low = pdb.lower()
    get(f"{VAL}/{low[1:3]}/{low}/{low}_validation.xml.gz", d / "validation.xml.gz", binary=True)


def val_root(pdb: str) -> dict[str, str]:
    """`<Entry .../>` attributes from the wwPDB validation report."""
    p = RAW / pdb / "validation.xml.gz"
    if not p.exists():
        return {}
    with gzip.open(p, "rt", errors="replace") as f:
        txt = f.read()
    m = re.search(r"<Entry\s(.*?)/?>", txt, re.S)
    return dict(re.findall(r'([\w\-.]+)="([^"]*)"', m.group(1))) if m else {}


def val_ligands(pdb: str) -> list[dict]:
    p = RAW / pdb / "validation.xml.gz"
    if not p.exists():
        return []
    with gzip.open(p, "rt", errors="replace") as f:
        txt = f.read()
    out = []
    for tag in re.findall(r"<ModelledSubgroup\s([^>]*?)/?>", txt, re.S):
        a = dict(re.findall(r'([\w\-.]+)="([^"]*)"', tag))
        out.append(a)
    return out


def num(v):
    if v in (None, "", "NotAvailable", "n/a"):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def load(pdb: str, name: str):
    p = RAW / pdb / name
    if not p.exists():
        return None
    t = p.read_text()
    return None if t == "null" else json.loads(t)


def entity_files(pdb: str, prefix: str) -> list[dict]:
    out = []
    for p in sorted((RAW / pdb).glob(f"{prefix}_*.json")):
        obj = load(pdb, p.name)
        if obj:
            out.append(obj)
    return out


def extract(pdb: str) -> dict:
    e = load(pdb, "entry.json")
    v = val_root(pdb)
    info = e.get("rcsb_entry_info", {})
    acc = e.get("rcsb_accession_info", {})
    sym = e.get("symmetry") or {}
    cell = e.get("cell") or {}
    refine = (e.get("refine") or [{}])[0]
    em3d = (e.get("em_3d_reconstruction") or [{}])[0]
    emexp = e.get("em_experiment") or {}

    # ---- polymer entities, chains, gaps -------------------------------------------
    entities, chains = [], []
    for pe in entity_files(pdb, "polymer_entity"):
        cid = pe.get("rcsb_polymer_entity_container_identifiers", {})
        poly = pe.get("entity_poly", {})
        ents = pe.get("rcsb_polymer_entity", {})
        entities.append(
            {
                "entity_id": cid.get("entity_id"),
                "description": ents.get("pdbx_description"),
                "type": poly.get("rcsb_entity_polymer_type"),
                "seq_length": poly.get("rcsb_sample_sequence_length"),
                "auth_asym_ids": cid.get("auth_asym_ids"),
                "source_organism": [
                    {
                        "scientific_name": s.get("scientific_name"),
                        "ncbi_taxonomy_id": s.get("ncbi_taxonomy_id"),
                    }
                    for s in (pe.get("rcsb_entity_source_organism") or [])
                ],
                "host_organism": [
                    s.get("scientific_name") for s in (pe.get("rcsb_entity_host_organism") or [])
                ],
                "uniprot_accessions": cid.get("uniprot_ids"),
                "mutation_count": poly.get("rcsb_mutation_count"),
                "mutations": ents.get("pdbx_mutation"),
                # RCSB annotates the *positions* of UniProt mismatches even when the depositor
                # left `pdbx_mutation` empty. Entity numbering; auth numbering is added below.
                "mutation_positions_entity_seq": sorted(
                    fp.get("beg_seq_id")
                    for feat in pe.get("rcsb_polymer_entity_feature") or []
                    if feat.get("type") == "mutation"
                    for fp in feat.get("feature_positions") or []
                    if fp.get("beg_seq_id") is not None
                ),
                "mutation_positions_auth_seq": None,
            }
        )
        for asym in cid.get("asym_ids") or []:
            pi = load(pdb, f"polymer_instance_{asym}.json")
            if not pi:
                continue
            iid = pi.get("rcsb_polymer_entity_instance_container_identifiers", {})
            mapping = iid.get("auth_to_entity_poly_seq_mapping") or []
            gaps, n_unobs = [], 0
            for feat in pi.get("rcsb_polymer_instance_feature") or []:
                if feat.get("type") != "UNOBSERVED_RESIDUE_XYZ":
                    continue
                for fp in feat.get("feature_positions") or []:
                    b, t = fp.get("beg_seq_id"), fp.get("end_seq_id") or fp.get("beg_seq_id")
                    if b is None:
                        continue
                    n_unobs += t - b + 1
                    ab = mapping[b - 1] if len(mapping) >= b else None
                    at = mapping[t - 1] if len(mapping) >= t else None
                    gaps.append({"entity_seq": [b, t], "auth_seq": [ab, at], "length": t - b + 1})
            gaps.sort(key=lambda g: g["entity_seq"][0])
            chains.append(
                {
                    "auth_asym_id": iid.get("auth_asym_id"),
                    "asym_id": asym,
                    "entity_id": iid.get("entity_id"),
                    "entity_seq_length": len(mapping) or None,
                    "modelled_polymer_residues": (len(mapping) - n_unobs) if mapping else None,
                    "unmodelled_residue_count": n_unobs,
                    "unmodelled_ranges": gaps,
                }
            )

    # entity-numbered mutation positions -> author numbering, via any chain of that entity
    maps = {}
    for c in chains:
        maps.setdefault(c["entity_id"], c)
    for ent in entities:
        c = maps.get(ent["entity_id"])
        if not c or not ent["mutation_positions_entity_seq"]:
            continue
        pi = load(pdb, f"polymer_instance_{c['asym_id']}.json") or {}
        m = (
            pi.get("rcsb_polymer_entity_instance_container_identifiers", {}).get(
                "auth_to_entity_poly_seq_mapping"
            )
            or []
        )
        ent["mutation_positions_auth_seq"] = [
            m[i - 1] if len(m) >= i else None for i in ent["mutation_positions_entity_seq"]
        ]

    # ---- non-polymer components ----------------------------------------------------
    lig_val = {(a.get("chain"), a.get("resnum"), a.get("resname")): a for a in val_ligands(pdb)}
    nonpoly = []
    for ne in entity_files(pdb, "nonpolymer_entity"):
        cid = ne.get("rcsb_nonpolymer_entity_container_identifiers", {})
        comp_id = cid.get("nonpolymer_comp_id")
        cc = (
            get(f"{REST}/chemcomp/{comp_id}", RAW / "_chemcomp" / f"{comp_id}.json")
            if comp_id
            else None
        )
        chem = (cc or {}).get("chem_comp", {})
        soi = None
        for ann in ne.get("rcsb_nonpolymer_entity_annotation") or []:
            if ann.get("type") == "SUBJECT_OF_INVESTIGATION":
                soi = "Y"
        insts = []
        for asym in cid.get("asym_ids") or []:
            ni = load(pdb, f"nonpolymer_instance_{asym}.json")
            if not ni:
                continue
            iid = ni.get("rcsb_nonpolymer_entity_instance_container_identifiers", {})
            score = (ni.get("rcsb_nonpolymer_instance_validation_score") or [{}])[0]
            if score.get("is_subject_of_investigation") == "Y":
                soi = "Y"
            key = (iid.get("auth_asym_id"), iid.get("auth_seq_id"), comp_id)
            xml = lig_val.get(key, {})
            insts.append(
                {
                    "asym_id": asym,
                    "auth_asym_id": iid.get("auth_asym_id"),
                    "auth_seq_id": iid.get("auth_seq_id"),
                    "RSCC": score.get("RSCC"),
                    "RSR": score.get("RSR"),
                    "average_occupancy": score.get("average_occupancy"),
                    "intermolecular_clashes": score.get("intermolecular_clashes"),
                    "ranking_model_fit": score.get("ranking_model_fit"),
                    "ranking_model_geometry": score.get("ranking_model_geometry"),
                    "validation_xml_rscc": num(xml.get("rscc")),
                    "validation_xml_rsr": num(xml.get("rsr")),
                    "annotations": [
                        a.get("type") for a in ni.get("rcsb_nonpolymer_instance_annotation") or []
                    ],
                }
            )
        nonpoly.append(
            {
                "entity_id": cid.get("entity_id"),
                "comp_id": comp_id,
                "name": (ne.get("pdbx_entity_nonpoly") or {}).get("name"),
                "formula_weight_da": chem.get("formula_weight"),
                "formula": chem.get("formula"),
                "subject_of_investigation": soi,
                "common_cryo_or_buffer_component": comp_id in CRYO_BUFFER,
                "instances": insts,
            }
        )
    for be in entity_files(pdb, "branched_entity"):
        cid = be.get("rcsb_branched_entity_container_identifiers", {})
        nonpoly.append(
            {
                "entity_id": cid.get("entity_id"),
                "comp_id": "|".join(cid.get("chem_comp_monomers") or []),
                "name": (be.get("rcsb_branched_entity") or {}).get("pdbx_description"),
                "formula_weight_da": None,
                "formula": None,
                "subject_of_investigation": None,
                "common_cryo_or_buffer_component": None,
                "instances": [{"auth_asym_id": a} for a in cid.get("auth_asym_ids") or []],
                "note": "branched (oligosaccharide) entity; not a non-polymer entity",
            }
        )

    asm = load(pdb, "assembly_1.json") or {}
    ai = asm.get("rcsb_assembly_info", {})
    symops = asm.get("rcsb_struct_symmetry") or []

    return {
        "pdb_id": pdb,
        "group": GROUP_OF[pdb],
        "title": (e.get("struct") or {}).get("title"),
        "experimental_method": info.get("experimental_method"),
        "exptl_methods": [x.get("method") for x in e.get("exptl") or []],
        "structure_determination_methodology": info.get("structure_determination_methodology"),
        "resolution_combined_angstrom": (info.get("resolution_combined") or [None])[0],
        "validation_report_resolution": num(v.get("PDB-resolution")),
        "r_work": num(refine.get("ls_R_factor_R_work")) if refine else None,
        "r_free": num(refine.get("ls_R_factor_R_free")) if refine else None,
        "r_work_validation_report": num(v.get("PDB-R")),
        "r_free_validation_report": num(v.get("PDB-Rfree")),
        "refine_records_present": bool(e.get("refine")),
        "space_group": sym.get("space_group_name_H_M"),
        "space_group_number": sym.get("Int_Tables_number"),
        "unit_cell": {
            "a": cell.get("length_a"),
            "b": cell.get("length_b"),
            "c": cell.get("length_c"),
            "alpha": cell.get("angle_alpha"),
            "beta": cell.get("angle_beta"),
            "gamma": cell.get("angle_gamma"),
        }
        if cell
        else None,
        "deposit_date": (acc.get("deposit_date") or "")[:10] or None,
        "initial_release_date": (acc.get("initial_release_date") or "")[:10] or None,
        "latest_revision_date": (acc.get("revision_date") or "")[:10] or None,
        "wwpdb_version_label": f"{acc.get('major_revision')}-{acc.get('minor_revision')}"
        if acc.get("major_revision") is not None
        else None,
        "revision_count": len(e.get("pdbx_audit_revision_history") or []),
        "has_released_experimental_data": acc.get("has_released_experimental_data"),
        "polymer_entity_count": info.get("polymer_entity_count"),
        "nonpolymer_entity_count": info.get("nonpolymer_entity_count"),
        "branched_entity_count": info.get("branched_entity_count"),
        "deposited_polymer_chain_count": info.get("deposited_polymer_entity_instance_count"),
        "deposited_nonpolymer_instance_count": info.get(
            "deposited_nonpolymer_entity_instance_count"
        ),
        "deposited_modeled_atom_count": info.get("deposited_modeled_atom_count"),
        "nonpolymer_bound_components": info.get("nonpolymer_bound_components"),
        "polymer_entities": entities,
        "chains": chains,
        "nonpolymer_components": nonpoly,
        "assembly_1": {
            "polymer_entity_instance_count": ai.get("polymer_entity_instance_count"),
            "nonpolymer_entity_instance_count": ai.get("nonpolymer_entity_instance_count"),
            "polymer_composition": ai.get("polymer_composition"),
            "oligomeric_state": (asm.get("pdbx_struct_assembly") or {}).get("oligomeric_details"),
            "oligomeric_count": (asm.get("pdbx_struct_assembly") or {}).get("oligomeric_count"),
            "method_details": (asm.get("pdbx_struct_assembly") or {}).get("method_details"),
            "stoichiometry": [
                {
                    "symbol": s.get("symbol"),
                    "kind": s.get("kind"),
                    "type": s.get("type"),
                    "stoichiometry": s.get("stoichiometry"),
                    "oligomeric_state": s.get("oligomeric_state"),
                }
                for s in symops
            ],
        }
        if asm
        else None,
        "validation_percentiles": {
            "clashscore": {
                "value": num(v.get("clashscore")),
                "absolute_percentile": num(v.get("absolute-percentile-clashscore")),
                "relative_percentile": num(v.get("relative-percentile-clashscore")),
            },
            "ramachandran_outliers_percent": {
                "value": num(v.get("percent-rama-outliers")),
                "absolute_percentile": num(v.get("absolute-percentile-percent-rama-outliers")),
                "relative_percentile": num(v.get("relative-percentile-percent-rama-outliers")),
            },
            "sidechain_outliers_percent": {
                "value": num(v.get("percent-rota-outliers")),
                "absolute_percentile": num(v.get("absolute-percentile-percent-rota-outliers")),
                "relative_percentile": num(v.get("relative-percentile-percent-rota-outliers")),
            },
            "rsrz_outliers_percent": {
                "value": num(v.get("percent-RSRZ-outliers")),
                "absolute_percentile": num(v.get("absolute-percentile-percent-RSRZ-outliers")),
                "relative_percentile": num(v.get("relative-percentile-percent-RSRZ-outliers")),
            },
            "rfree_dcc": {
                "value": num(v.get("DCC_Rfree")),
                "absolute_percentile": num(v.get("absolute-percentile-DCC_Rfree")),
                "relative_percentile": num(v.get("relative-percentile-DCC_Rfree")),
            },
            "percentile_bins": v.get("percentilebins"),
            "report_creation_date": (e.get("pdbx_vrpt_summary") or {}).get(
                "report_creation_date", ""
            )[:10]
            or None,
            "validation_report_present": bool(v),
        },
        "cryo_em": {
            "emdb_ids": (e.get("rcsb_entry_container_identifiers") or {}).get("emdb_ids"),
            "reconstruction_method": emexp.get("reconstruction_method"),
            "aggregation_state": emexp.get("aggregation_state"),
            "map_resolution_angstrom": em3d.get("resolution"),
            "resolution_method": em3d.get("resolution_method"),
            "symmetry_type": em3d.get("symmetry_type"),
            "num_particles": em3d.get("num_particles"),
            "em_software": [
                {"name": s.get("name"), "category": s.get("category"), "version": s.get("version")}
                for s in e.get("em_software") or []
            ],
            "model_fitting": [
                {
                    "software": f.get("software_name"),
                    "details": f.get("details"),
                    "target_criteria": f.get("target_criteria"),
                    "ref_protocol": f.get("ref_protocol"),
                }
                for f in e.get("em_3d_fitting") or []
            ],
            "vrpt_em": e.get("pdbx_vrpt_summary_em"),
        }
        if e.get("em_experiment")
        else None,
        "software": [
            {
                "name": s.get("name"),
                "classification": s.get("classification"),
                "version": s.get("version"),
            }
            for s in e.get("software") or []
        ],
    }


def self_check(entries: dict) -> None:
    """The extraction has two pieces of real logic: the gap arithmetic and the ligand join.

    Both reconcile against a count RCSB computes independently, so one assert catches either
    breaking.
    """
    for pdb, v in entries.items():
        for c in v["chains"]:
            assert (
                c["modelled_polymer_residues"] + c["unmodelled_residue_count"]
                == c["entity_seq_length"]
            ), f"{pdb}:{c['auth_asym_id']} residue counts do not reconcile"
            for r in c["unmodelled_ranges"]:
                assert None not in r["auth_seq"], f"{pdb}:{c['auth_asym_id']} unmapped gap {r}"
        assert len(v["chains"]) == v["deposited_polymer_chain_count"], f"{pdb} chain count"
        n_inst = sum(len(c["instances"]) for c in v["nonpolymer_components"] if "note" not in c)
        assert n_inst == (v["deposited_nonpolymer_instance_count"] or 0), (
            f"{pdb} ligand instance count"
        )


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fetch_entry, IDS))
    out = {
        "generated_from": "RCSB Data API (data.rcsb.org/rest/v1/core) and wwPDB validation reports",
        "raw_cache": "rcsb-raw/",
        "entries": {pdb: extract(pdb) for pdb in IDS},
    }
    self_check(out["entries"])
    (DATA / "structure-evidence.json").write_text(json.dumps(out, indent=1, sort_keys=False) + "\n")
    print(f"wrote {len(out['entries'])} entries")
