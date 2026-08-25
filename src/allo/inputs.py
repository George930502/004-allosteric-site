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

import gzip
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from allo.structure.pdb import Structure, contacts, parse_mmcif_text, sha256

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "benchmark" / "manifest.yaml"
SECONDARY_MANIFEST = ROOT / "docs" / "benchmark" / "secondary" / "manifest.yaml"

# Two files rather than one. The primary set is the three disease areas the challenge
# names; the secondary set is drawn from a candidate pool to demonstrate generalisability
# and scalability. They freeze on different dates and are admitted under different rules --
# a pool gets a resolution ceiling and a redundancy bound, hand-specified targets cannot
# (ADR 0009, ADR 0021). Keeping them in one file would mean re-freezing a closed artifact
# every time the secondary set moves.
BENCHMARK_MANIFESTS = (MANIFEST, SECONDARY_MANIFEST)

# Written as one path rather than as `STRUCTURES / "apo"` on purpose: a `STRUCTURES` root
# exported here would put the tracked holo mirror one `/ "holo"` away from prediction code.
APO_STRUCTURES = ROOT / "structures" / "apo"

# The only cache prediction code writes to, and the only one it can reach.
#
# Both used to be one directory. `data/raw/` was the default for `apo_input` *and* for
# `benchmark.derive`, so `make check` -- offline, no network marker -- restored all seven
# holo entries into the cache a method reads from, on every clone. The former shared parser
# accepted a `Path`, so a constructed legacy-cache path returned asciminib's coordinates
# from a module importing nothing but `allo.inputs` and `allo.structure.pdb`. No guard saw
# it: the import trace watches `allo.groundtruth`, and the file-read tests grep for the
# names of the freeze artifact and the manifest -- that route contains neither string.
# (This comment may not spell either filename either; the grep does not read comments.)
#
# Partitioning the cache and removing filesystem access from the shared parser close it.
# Evaluation writes to
# `allo.groundtruth.structures.EVAL_CACHE`; nothing reachable from the prediction path
# names that directory. `test_the_prediction_cache_never_holds_a_holo_structure` holds the
# invariant after a full `make check`.
APO_CACHE = ROOT / "data" / "raw" / "apo"

# Conserved catalytic motifs, for the targets whose apo entry holds no cofactor (ADR 0005).
# Patterns are matched against the modelled chain sequence, so the residue numbers come out
# in whatever numbering convention that entry uses — which is the point: ABL1 is deposited
# under two, 19 apart, and a hand-written list is only ever right for one of them.
#
# Every entry carries provenance and must match EXACTLY ONCE on the chain that uses it;
# `active_site` raises otherwise. That check is the real guarantee, and it earns its keep:
# it rejected SHP2 apo `6CMP` during secondary screening, which is the catalytically dead
# C459E mutant. Where PROSITE publishes a `PA` pattern the regex is converted from it
# mechanically and carries the accession. Where PROSITE covers the family by profile only,
# a profile is not a regular expression, so the motif carries a primary-literature
# citation instead (ADR 0021 section 4, amended).
CATALYTIC_MOTIFS = {
    # Protein kinase, from the primary set. ABL1 and CHK1.
    "VAIK": r"[VLIA]A[VLIA]K",
    "HRD": r"H[RG][DN][LIVM]",
    "DFG": r"D[FWY]G",
    # RNA/DNA polymerase motifs A and C (Poch 1989, doi 10.1002/j.1460-2075.1989.tb08565.x).
    # HIV-1 RT needs both: motif C alone gives D185/D186 and misses catalytic D110, which
    # would make the propagation source two thirds of the triad.
    "POLA": r"[LIVM]{2}D[TV]G",
    "YXDD": r"Y[MIVL]DD",
    # Motif C again, in a positive-strand RdRp. HCV NS5B: G317-D318-D319.
    "GDD": r"GDD",
    # PROSITE PS00383 TYR_PHOSPHATASE_1, converted from its PA line
    # `[LIVMF]-H-C-x(2)-G-x(2)-R-[STC]-[STAGP].`
    "PTP": r"[LIVMF]HC.{2}G.{2}R[STC][STAGP]",
}

_THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
    "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
    "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    # modified residues seen in the benchmark targets, mapped to their parent
    "MSE": "M", "M3L": "K", "SEP": "S", "TPO": "T", "PTR": "Y",
}  # fmt: skip


_LEAF = object()
_PREDICTION_SCHEMA = {
    "defaults": {"contact_cutoff_angstrom": _LEAF},
    "targets": [
        {
            "id": _LEAF,
            "protein": _LEAF,
            "apo": {"pdb": _LEAF, "chain": _LEAF, "sha256": _LEAF},
            "active_site": {"from_ligands": _LEAF, "from_motifs": _LEAF},
        }
    ],
}


def _project(value, schema):
    """Copy only exact schema paths; a newly nested key is absent by default."""
    if schema is _LEAF:
        return value
    if isinstance(schema, list):
        return [_project(item, schema[0]) for item in value]
    return {key: _project(value[key], child) for key, child in schema.items() if key in value}


def load(path: Path = MANIFEST) -> dict:
    """The manifest as **prediction code** may see it: the apo half, and nothing else.

    C1 says holo data may not reach the prediction path. `allo.inputs` is the one
    prediction-path module that has to open the manifest at all — it needs the chain and
    the active-site rule — so it is also the place the answer key has to be stripped. It
    rebuilds the manifest from two allow-lists rather than filtering a deny-list, so a field
    added later is redacted by default rather than leaked by default. The verbatim read is
    `allo.groundtruth.manifest.read_manifest`, behind the import guard; this module never
    exposes one (`tests/test_no_leakage.py`).

    `site` used to survive redaction, justified as a human label the challenge already
    gives every participant. That was true for `Switch-II pocket`, `myristoyl pocket` and
    `mavacamten site` -- and false for `blebbistatin/aficamten pocket (Site 2)` and
    `mavacamten/omecamtiv pocket (Site 1)`, which name effectors that appear nowhere in
    `CHALLENGE.md` because those arms are ours. Naming the effector is naming where the
    pocket is, to anyone with a search engine. Nothing on the prediction path ever read the
    key, so it is gone rather than repaired: a benchmark whose purpose is that no method can
    take an advantage another cannot does not ship an unused channel to the answer.
    """
    manifest = yaml.safe_load(path.read_text())
    # Evaluation status cannot admit or delete a prediction input. `prediction_status` is a
    # separate apo-side decision: ADR 0016 records why 5TBY is blocked without fabricating a
    # propagation source, independently of the defective 6C1H evaluation arm.
    manifest = {
        **manifest,
        "targets": [
            target
            for target in manifest["targets"]
            if target.get("prediction_status", "admitted") == "admitted"
        ],
    }
    return _project(manifest, _PREDICTION_SCHEMA)


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


def admitted_residue_numbers(apo: Structure, chain: str) -> tuple[int, ...]:
    """The node set: every modelled protein residue of the frozen chain (ADR 0010).

    There is no trim, on either benchmark set. The deposited construct is what defines
    the scope, so scope is chosen when a structure is admitted rather than by a rule
    applied afterwards -- which keeps it an apo-only decision and keeps it out of code.
    """
    return tuple(number for c, number, _ in apo.residues() if c == chain)


def _prediction_structure(apo: Structure, chain: str, residues: tuple[int, ...]) -> Structure:
    """Copy only admitted protein atoms into an immutable prediction-side structure."""
    keep = apo.protein & (apo.chain == chain) & np.isin(apo.seq_id, residues)

    # ADR 0006 chooses the parent amino acid representation. M3L's three methyl carbons are
    # PTM-specific topology, not lysine topology, so remove them before any contact graph can
    # see them and rename the remaining residue to its parent.
    m3l = apo.resname == "M3L"
    keep &= ~(m3l & np.isin(apo.atom, ["CM1", "CM2", "CM3"]))

    def immutable(array: np.ndarray) -> np.ndarray:
        """Read-only *and* un-unfreezable. Clearing the flag on an owning copy was not:
        a review called `setflags(write=True)` on it and wrote to `coord` in place. Backing
        the array with a `bytes` buffer makes NumPy refuse that, on the view and on its base.
        """
        selected = array[keep]
        if array is apo.resname:
            selected = selected.copy()
            selected[selected == "M3L"] = "LYS"
        frozen = np.frombuffer(selected.tobytes(), dtype=selected.dtype)
        return frozen.reshape(selected.shape)

    structure = Structure(
        pdb_id=apo.pdb_id,
        chain=immutable(apo.chain),
        seq_id=immutable(apo.seq_id),
        resname=immutable(apo.resname),
        atom=immutable(apo.atom),
        element=immutable(apo.element),
        altloc=immutable(apo.altloc),
        coord=immutable(apo.coord),
        bfactor=immutable(apo.bfactor),
        hetatm=immutable(apo.hetatm),
        in_polymer=immutable(apo.in_polymer),
    )
    atom_residues = {number for _, number, _ in structure.residues()}
    if set(structure.chain.tolist()) != {chain}:
        raise ValueError(f"{apo.pdb_id}: prediction structure is not restricted to chain {chain}")
    if atom_residues != set(residues):
        raise ValueError(
            f"{apo.pdb_id}:{chain} atom residues {sorted(atom_residues)} do not equal nodes "
            f"{list(residues)}"
        )
    if structure.ligand.any() or np.any(structure.resname == "HOH"):
        raise ValueError(f"{apo.pdb_id}:{chain} prediction structure contains non-protein atoms")
    return structure


@dataclass(frozen=True)
class ApoInput:
    """What a method receives. Identical for every method, by construction."""

    target: str
    pdb_id: str
    chain: str
    structure: Structure
    residues: tuple[int, ...]
    active_site: tuple[int, ...]
    cutoff: float


def apo_input(target: str, raw: Path = APO_CACHE) -> ApoInput:
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

    Its default is `APO_CACHE`, not the shared `data/raw/`, and that distinction is the C1
    boundary rather than a tidiness preference -- see the comment on `APO_CACHE`.
    """
    specs = {}
    for path in BENCHMARK_MANIFESTS:
        # A set that has not been frozen yet has no manifest. A clone holding only the
        # primary set must still be able to load a primary target.
        if not path.exists():
            continue
        for spec in load(path)["targets"]:
            if spec["id"] in specs:
                raise ValueError(f"{spec['id']!r} is declared in more than one benchmark set")
            specs[spec["id"]] = (spec, path)
    if target not in specs:
        raise KeyError(f"{target!r} is not a frozen target; have {sorted(specs)}")
    spec, manifest_path = specs[target]
    cutoff = load(manifest_path)["defaults"]["contact_cutoff_angstrom"]
    chain = spec["apo"]["chain"]
    raw.mkdir(parents=True, exist_ok=True)
    path = raw / f"{spec['apo']['pdb'].upper()}.cif"
    if not path.exists():
        archived = APO_STRUCTURES / f"{spec['apo']['pdb'].upper()}.cif.gz"
        if not archived.exists():
            raise FileNotFoundError(
                f"{target}: frozen apo {spec['apo']['pdb']} is absent from the apo store"
            )
        path.write_bytes(gzip.decompress(archived.read_bytes()))
    # Fail closed on the bytes, not just on the accession. The cache is gitignored, writable,
    # and may be stale or replaced, so the store path alone is not the boundary. The hash
    # below binds the restored bytes to the target's manifest record.
    expected = spec["apo"].get("sha256")
    if not expected:
        raise ValueError(f"{target}: manifest pins no apo sha256; refusing to run unpinned")
    if (actual := sha256(path)) != expected:
        raise ValueError(
            f"{target}: {spec['apo']['pdb']} is not the frozen file -- expected {expected}, "
            f"got {actual}. RCSB may have re-versioned it; re-freeze deliberately or delete "
            f"{path} and refetch."
        )
    apo = parse_mmcif_text(path.read_text(), spec["apo"]["pdb"])
    residues = admitted_residue_numbers(apo, chain)
    source = tuple(active_site(apo, chain, spec["active_site"], cutoff))
    if not set(source) <= set(residues):
        raise ValueError(
            f"{target}: active-site residues {sorted(set(source) - set(residues))} fall outside "
            "the admitted node set"
        )
    return ApoInput(
        target=target,
        pdb_id=spec["apo"]["pdb"],
        chain=chain,
        structure=_prediction_structure(apo, chain, residues),
        residues=residues,
        active_site=source,
        cutoff=cutoff,
    )
