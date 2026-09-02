#!/usr/bin/env python3
"""Derive the 2026-09 structure-evidence table from the cached raw bytes.

Reads only `rcsb-2026-09-refresh/`, writes `structure-evidence-refresh.json`, and prints
a flat dump of everything 18-structure-evidence-refresh.md quotes. Every extracted value
names its source: a REST path, a validation-report attribute, or an mmCIF category.

Run with the project interpreter (biopython supplies the mmCIF tokenizer):
    uv run python docs/benchmark/review/data/extract_refresh_2026_09.py

Imports nothing from `allo` and names no path outside this directory.
"""

from __future__ import annotations

import gzip
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from Bio.PDB.MMCIF2Dict import MMCIF2Dict

CACHE = Path(__file__).resolve().parent / "rcsb-2026-09-refresh"
OUT = Path(__file__).resolve().parent / "structure-evidence-refresh.json"
IDS = ["1OPL", "2G2H", "4LDJ", "4OBE", "5MO4", "5TBY", "6OIM", "9GZ2", "9GZ3"]


def jload(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def cif(pdb: str) -> dict:
    with gzip.open(CACHE / pdb / f"{pdb}.cif.gz", "rt") as fh:
        return MMCIF2Dict(fh)


def val_entry(pdb: str) -> dict:
    """Attributes of the wwPDB validation report's single <Entry> element."""
    with gzip.open(CACHE / pdb / "validation.xml.gz", "rt", errors="replace") as fh:
        text = fh.read()
    m = re.search(r"<Entry\b(.*?)/?>", text, re.S)
    attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(1))) if m else {}
    attrs["_n_ModelledSubgroup"] = text.count("<ModelledSubgroup")
    return attrs


def ranges(nums: list[int]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for n in sorted(nums):
        if out and n == out[-1][1] + 1:
            out[-1] = (out[-1][0], n)
        else:
            out.append((n, n))
    return out


def fmt(rs) -> str:
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in rs) or "none"


def main() -> int:
    table: dict[str, dict] = {}
    for pdb in IDS:
        d = CACHE / pdb
        entry = jload(d / "entry.json")
        ei = entry.get("rcsb_entry_info", {})
        ai = entry.get("rcsb_accession_info", {})
        ci = entry.get("rcsb_entry_container_identifiers", {})
        ref = (entry.get("refine") or [{}])[0]
        v = val_entry(pdb)
        c = cif(pdb)
        rec: dict = {"pdb": pdb}

        # ---------------- 1. provenance
        rec["provenance"] = {
            "title": entry.get("struct", {}).get("title"),
            "method": ei.get("experimental_method"),
            "methodology": ei.get("structure_determination_methodology"),
            "resolution": (ei.get("resolution_combined") or [None])[0],
            "R_work": ref.get("ls_R_factor_R_work"),
            "R_free": ref.get("ls_R_factor_R_free"),
            "refine_keys_present": sorted(k for k in ref if ref[k] is not None),
            "deposited": ai.get("deposit_date", "")[:10],
            "released": ai.get("initial_release_date", "")[:10],
            "revised": ai.get("revision_date", "")[:10],
            "version": f"{ai.get('major_revision')}-{ai.get('minor_revision')}",
            "n_revisions": len(entry.get("pdbx_audit_revision_history") or []),
            "exp_data_released": ai.get("has_released_experimental_data"),
            "emdb": ci.get("emdb_ids"),
            "space_group": entry.get("symmetry", {}).get("space_group_name_H_M"),
            "validation": {
                "report_created": v.get("XMLcreationDate"),
                "report_revision": v.get("PDB-revision-number"),
                "percentilebins": v.get("percentilebins"),
                "clashscore": v.get("clashscore"),
                "clash_abs": v.get("absolute-percentile-clashscore"),
                "clash_rel": v.get("relative-percentile-clashscore"),
                "rama": v.get("percent-rama-outliers"),
                "rama_abs": v.get("absolute-percentile-percent-rama-outliers"),
                "rota": v.get("percent-rota-outliers"),
                "rota_abs": v.get("absolute-percentile-percent-rota-outliers"),
                "rsrz": v.get("percent-RSRZ-outliers"),
                "rsrz_abs": v.get("absolute-percentile-percent-RSRZ-outliers"),
                "rsrz_rel": v.get("relative-percentile-percent-RSRZ-outliers"),
                "DCC_Rfree": v.get("DCC_Rfree"),
                "EDS_R": v.get("DCC_R"),
                "n_modelled_subgroups": v["_n_ModelledSubgroup"],
            },
        }
        em = (entry.get("em_3d_reconstruction") or [{}])[0]
        fit = (entry.get("em_3d_fitting") or [{}])[0]
        if em or fit:
            rec["provenance"]["em"] = {
                "map_resolution": em.get("resolution"),
                "resolution_method": em.get("resolution_method"),
                "num_particles": em.get("num_particles"),
                "ref_protocol": fit.get("ref_protocol"),
                "target_criteria": fit.get("target_criteria"),
                "fitted_from": c.get("_em_3d_fitting_list.pdb_entry_id"),
                "initial_model": c.get("_pdbx_initial_refinement_model.accession_code"),
                "software": [
                    (a, b)
                    for a, b in zip(
                        c.get("_em_software.category", []),
                        c.get("_em_software.name", []),
                        strict=False,
                    )
                ],
            }

        # ---------------- 2. chemical composition
        polymers = []
        for eid in ci.get("polymer_entity_ids", []):
            pe = jload(d / f"polymer_entity_{eid}.json")
            pid = pe.get("rcsb_polymer_entity_container_identifiers", {})
            polymers.append(
                {
                    "entity_id": eid,
                    "description": pe.get("rcsb_polymer_entity", {}).get("pdbx_description"),
                    "auth_chains": pid.get("auth_asym_ids"),
                    "asym_ids": pid.get("asym_ids"),
                    "organism": [
                        o.get("scientific_name")
                        for o in pe.get("rcsb_entity_source_organism") or []
                    ],
                    "taxid": [
                        o.get("ncbi_taxonomy_id")
                        for o in pe.get("rcsb_entity_source_organism") or []
                    ],
                    "uniprot": pid.get("uniprot_ids"),
                    "seq_length": pe.get("entity_poly", {}).get("rcsb_sample_sequence_length"),
                    "mutation_count": pe.get("entity_poly", {}).get("rcsb_mutation_count"),
                    "pdbx_mutation": pe.get("rcsb_polymer_entity", {}).get("pdbx_mutation"),
                    "formula_weight_kDa": pe.get("rcsb_polymer_entity", {}).get("formula_weight"),
                }
            )
        rec["polymer_entities"] = polymers

        # _struct_ref_seq / _struct_ref, straight out of the deposited file
        srs = []
        n = len(c.get("_struct_ref_seq.ref_id", []))
        refmap = {
            i: (db, code, acc)
            for i, db, code, acc in zip(
                c.get("_struct_ref.id", []),
                c.get("_struct_ref.db_name", []),
                c.get("_struct_ref.db_code", []),
                c.get("_struct_ref.pdbx_db_accession", []),
                strict=False,
            )
        }
        for i in range(n):
            rid = c["_struct_ref_seq.ref_id"][i]
            db, code, acc = refmap.get(rid, (None, None, None))
            srs.append(
                {
                    "ref_id": rid,
                    "db": db,
                    "db_code": code,
                    "accession": acc,
                    "entity_chain": c["_struct_ref_seq.pdbx_strand_id"][i],
                    "auth_beg": c["_struct_ref_seq.pdbx_auth_seq_align_beg"][i],
                    "auth_end": c["_struct_ref_seq.pdbx_auth_seq_align_end"][i],
                    "db_beg": c["_struct_ref_seq.db_align_beg"][i],
                    "db_end": c["_struct_ref_seq.db_align_end"][i],
                }
            )
        rec["struct_ref_seq"] = srs
        rec["struct_ref_seq_dif"] = [
            {
                "auth_seq": s,
                "pdb_mon": m,
                "db_mon": dm,
                "details": det,
                "chain": ch,
            }
            for s, m, dm, det, ch in zip(
                c.get("_struct_ref_seq_dif.pdbx_auth_seq_num", []),
                c.get("_struct_ref_seq_dif.mon_id", []),
                c.get("_struct_ref_seq_dif.db_mon_id", []),
                c.get("_struct_ref_seq_dif.details", []),
                c.get("_struct_ref_seq_dif.pdbx_pdb_strand_id", []),
                strict=False,
            )
        ]
        rec["modified_residues"] = [
            {"comp": comp, "chain": ch, "auth_seq": sq, "parent": par, "details": det}
            for comp, ch, sq, par, det in zip(
                c.get("_pdbx_struct_mod_residue.label_comp_id", []),
                c.get("_pdbx_struct_mod_residue.auth_asym_id", []),
                c.get("_pdbx_struct_mod_residue.auth_seq_id", []),
                c.get("_pdbx_struct_mod_residue.parent_comp_id", []),
                c.get("_pdbx_struct_mod_residue.details", []),
                strict=False,
            )
        ]

        # atom_site: per-chain B-factors, occupancies, HETATM inventory
        grp = c["_atom_site.group_PDB"]
        ch_a = c["_atom_site.auth_asym_id"]
        comp = (
            c["_atom_site.auth_comp_id"]
            if "_atom_site.auth_comp_id" in c
            else c["_atom_site.label_comp_id"]
        )
        seq = c["_atom_site.auth_seq_id"]
        occ = c["_atom_site.occupancy"]
        bfac = c["_atom_site.B_iso_or_equiv"]
        model = c.get("_atom_site.pdbx_PDB_model_num", ["1"] * len(grp))

        bvals: dict[str, set] = defaultdict(set)
        occs: dict[str, list] = defaultdict(list)
        het: dict[tuple, dict] = {}
        polyres: dict[str, set] = defaultdict(set)
        for i in range(len(grp)):
            if model[i] != "1":
                continue
            ch = ch_a[i]
            if grp[i] == "ATOM":
                bvals[ch].add(bfac[i])
                occs[ch].append(float(occ[i]))
                polyres[ch].add(int(seq[i]))
            else:
                key = (comp[i], ch, seq[i])
                h = het.setdefault(
                    key, {"comp": comp[i], "chain": ch, "auth_seq": seq[i], "occ": [], "b": []}
                )
                h["occ"].append(float(occ[i]))
                h["b"].append(float(bfac[i]))
        rec["per_chain_atom_site"] = {
            ch: {
                "distinct_B_values": len(bvals[ch]),
                "n_polymer_residues": len(polyres[ch]),
                "min_occupancy": min(occs[ch]),
                "polymer_span": (min(polyres[ch]), max(polyres[ch])),
            }
            for ch in sorted(bvals)
        }
        rec["heteroatom_groups"] = [
            {
                "comp": h["comp"],
                "chain": h["chain"],
                "auth_seq": h["auth_seq"],
                "n_atoms": len(h["occ"]),
                "occupancy": sorted({round(x, 3) for x in h["occ"]}),
                "mean_B": round(sum(h["b"]) / len(h["b"]), 2),
            }
            for h in het.values()
            if h["comp"] != "HOH"
        ]
        rec["n_water_groups"] = sum(1 for h in het.values() if h["comp"] == "HOH")
        rec["n_hetatm_records"] = sum(
            1 for i in range(len(grp)) if grp[i] == "HETATM" and model[i] == "1"
        )

        # non-polymer entities from REST, with per-instance density fit
        nonpoly = []
        for eid in ci.get("non_polymer_entity_ids", []):
            ne = jload(d / f"nonpolymer_entity_{eid}.json")
            nid = ne.get("rcsb_nonpolymer_entity_container_identifiers", {})
            cid = ne.get("pdbx_entity_nonpoly", {}).get("comp_id")
            cc = jload(CACHE / "_chemcomp" / f"{cid}.json") or {}
            insts = []
            for asym in nid.get("asym_ids", []):
                ni = jload(d / f"nonpolymer_instance_{asym}.json")
                if not ni:
                    continue
                nci = ni.get("rcsb_nonpolymer_entity_instance_container_identifiers", {})
                sc = (ni.get("rcsb_nonpolymer_instance_validation_score") or [{}])[0]
                insts.append(
                    {
                        "asym": asym,
                        "auth_chain": nci.get("auth_asym_id"),
                        "auth_seq": nci.get("auth_seq_id"),
                        "RSCC": sc.get("RSCC"),
                        "RSR": sc.get("RSR"),
                        "completeness": sc.get("completeness"),
                        "intermolecular_clashes": sc.get("intermolecular_clashes"),
                        "average_occupancy": sc.get("average_occupancy"),
                        "is_best_instance": sc.get("is_best_instance_in_entry"),
                        "score_model": sc.get("ranking_model_fit"),
                        "flags": sc.get("is_subject_of_investigation_provenance"),
                        "alt_conf": sc.get("alt_id"),
                        "validation_flags": ni.get("rcsb_nonpolymer_instance_annotation")
                        and sorted(
                            {a.get("type") for a in ni["rcsb_nonpolymer_instance_annotation"]}
                        ),
                    }
                )
            nonpoly.append(
                {
                    "entity_id": eid,
                    "comp_id": cid,
                    "name": ne.get("pdbx_entity_nonpoly", {}).get("name"),
                    "formula": cc.get("chem_comp", {}).get("formula"),
                    "formula_weight": cc.get("chem_comp", {}).get("formula_weight"),
                    "auth_chains": nid.get("auth_asym_ids"),
                    "subject_of_investigation": ne.get("rcsb_nonpolymer_entity", {}).get("details"),
                    "instances": insts,
                }
            )
        rec["nonpolymer_entities"] = nonpoly

        # ---------------- 3. what is modelled
        chains = {}
        for pe in polymers:
            for asym in pe["asym_ids"]:
                pi = jload(d / f"polymer_instance_{asym}.json")
                if not pi:
                    continue
                pid = pi.get("rcsb_polymer_entity_instance_container_identifiers", {})
                mapping = pid.get("auth_to_entity_poly_seq_mapping", [])
                unobs: list[int] = []
                domains = []
                for f in pi.get("rcsb_polymer_instance_feature") or []:
                    if f["type"] == "UNOBSERVED_RESIDUE_XYZ":
                        for p in f.get("feature_positions", []):
                            unobs += list(range(p["beg_seq_id"], p["end_seq_id"] + 1))
                    if f["type"] in ("CATH", "SCOP", "SCOP2", "ECOD"):
                        domains.append(
                            {
                                "source": f["type"],
                                "id": f.get("feature_id"),
                                "name": f.get("name"),
                                "auth_ranges": [
                                    (
                                        mapping[p["beg_seq_id"] - 1],
                                        mapping[p["end_seq_id"] - 1],
                                    )
                                    for p in f.get("feature_positions", [])
                                ],
                            }
                        )
                unobs_auth = sorted({int(mapping[i - 1]) for i in unobs})
                modelled = sorted({int(x) for x in mapping} - set(unobs_auth))
                chains[pid.get("auth_asym_id")] = {
                    "asym": asym,
                    "entity": pe["entity_id"],
                    "deposited_seq": len(mapping),
                    "modelled": len(modelled),
                    "unmodelled": len(unobs_auth),
                    "unmodelled_auth_ranges": fmt(ranges(unobs_auth)),
                    "modelled_auth_ranges": fmt(ranges(modelled)),
                    "domains": domains,
                }
        rec["chains"] = chains

        assemblies = []
        for aid in ci.get("assembly_ids", []):
            a = jload(d / f"assembly_{aid}.json")
            if not a:
                continue
            psa = a.get("pdbx_struct_assembly") or {}
            assemblies.append(
                {
                    "id": aid,
                    "oligomeric_details": psa.get("oligomeric_details"),
                    "oligomeric_count": psa.get("oligomeric_count"),
                    "method_details": psa.get("method_details"),
                    "details": psa.get("details"),
                    "polymer_instances": a.get("rcsb_assembly_info", {}).get(
                        "polymer_entity_instance_count"
                    ),
                    "nonpolymer_instances": a.get("rcsb_assembly_info", {}).get(
                        "nonpolymer_entity_instance_count"
                    ),
                    "symmetry": [
                        s.get("stoichiometry") for s in a.get("rcsb_struct_symmetry") or []
                    ],
                }
            )
        rec["assemblies"] = assemblies
        rec["deposited_counts"] = {
            "polymer_instances": ei.get("deposited_polymer_entity_instance_count"),
            "nonpolymer_instances": ei.get("deposited_nonpolymer_entity_instance_count"),
            "atom_count": ei.get("deposited_atom_count"),
            "modeled_polymer_monomers": ei.get("deposited_modeled_polymer_monomer_count"),
            "unmodeled_polymer_monomers": ei.get("deposited_unmodeled_polymer_monomer_count"),
            "assembly_count": ei.get("assembly_count"),
            "polymer_entity_count": ei.get("polymer_entity_count"),
            "nonpolymer_entity_count": ei.get("nonpolymer_entity_count"),
            "branched_entity_count": ei.get("branched_entity_count"),
        }

        # ---------------- struct_conn, refine details
        ct = c.get("_struct_conn.conn_type_id", [])
        rec["struct_conn"] = dict(Counter(ct))
        cov = [
            float(x)
            for t, x in zip(
                ct, c.get("_struct_conn.pdbx_dist_value", ["0"] * len(ct)), strict=False
            )
            if t == "covale" and x not in (".", "?")
        ]
        if cov:
            rec["covale_distance"] = {
                "n": len(cov),
                "min": round(min(cov), 3),
                "max": round(max(cov), 3),
                "mean": round(sum(cov) / len(cov), 3),
            }
        rd = c.get("_refine.details")
        rec["refine_details"] = rd[0] if rd else None
        rec["refine_cif_keys"] = {
            k.split(".")[1]: c[k][0]
            for k in c
            if k.startswith("_refine.") and c[k][0] not in ("?", ".")
        }
        table[pdb] = rec

    OUT.write_text(json.dumps(table, indent=1, sort_keys=False))

    # ---------------- flat dump
    for pdb, r in table.items():
        p = r["provenance"]
        print(f"\n===== {pdb} =====")
        print(" title:", (p["title"] or "")[:300])
        print(
            f" method={p['method']} methodology={p['methodology']} res={p['resolution']} "
            f"Rwork={p['R_work']} Rfree={p['R_free']} SG={p['space_group']}"
        )
        print(
            f" dep={p['deposited']} rel={p['released']} rev={p['revised']} v{p['version']} "
            f"nrev={p['n_revisions']} expdata={p['exp_data_released']} emdb={p['emdb']}"
        )
        print(" validation:", json.dumps(p["validation"]))
        if "em" in p:
            print(" em:", json.dumps(p["em"]))
        print(" refine_cif_keys:", json.dumps(r["refine_cif_keys"]))
        print(" refine.details:", (r["refine_details"] or "")[:400])
        print(" deposited:", json.dumps(r["deposited_counts"]))
        for a in r["assemblies"]:
            print("  assembly:", json.dumps(a))
        for pe in r["polymer_entities"]:
            print("  polymer:", json.dumps(pe))
        for s in r["struct_ref_seq"]:
            print("  struct_ref_seq:", json.dumps(s))
        if r["struct_ref_seq_dif"]:
            print("  seq_dif:", json.dumps(r["struct_ref_seq_dif"]))
        print("  modified_residues:", json.dumps(r["modified_residues"]))
        for ne in r["nonpolymer_entities"]:
            print("  nonpolymer:", json.dumps(ne))
        print("  hetatm_records:", r["n_hetatm_records"], " water_groups:", r["n_water_groups"])
        for h in r["heteroatom_groups"]:
            print("   het:", json.dumps(h))
        print("  per_chain_atom_site:", json.dumps(r["per_chain_atom_site"]))
        for ch, cd in r["chains"].items():
            print(
                f"  chain {ch} (asym {cd['asym']}, ent {cd['entity']}): "
                f"{cd['modelled']}/{cd['deposited_seq']} modelled; "
                f"unmodelled {cd['unmodelled_auth_ranges']}; modelled {cd['modelled_auth_ranges']}"
            )
            for dm in cd["domains"]:
                print(f"     domain {dm['source']} {dm['id']} {dm['name']} {dm['auth_ranges']}")
        print("  struct_conn:", json.dumps(r["struct_conn"]), r.get("covale_distance"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
