"""C1: holo-derived data must not reach the prediction path.

Module names prove nothing, so this walks the import graph transitively. Allowed
importers of `allo.groundtruth` are the stages that *score* or *report* — never the
stages that predict.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "allo"
GROUND_TRUTH = "allo.groundtruth"

# Allow-list, not deny-list. Naming the four prediction stages we happen to have
# thought of protects only those four: a module called `allo.rank` would have been
# outside the rule and free to read the answer key. Everything not named here is
# treated as prediction code and must not reach `groundtruth` by any route.
MAY_IMPORT_GROUND_TRUTH = {
    "allo.groundtruth",
    "allo.scoring",
    "allo.viz",
    "allo.cli",
    "allo.benchmark",
}


def is_prediction_path(module: str) -> bool:
    return not any(module == a or module.startswith(a + ".") for a in MAY_IMPORT_GROUND_TRUTH)


def module_name(path: Path) -> str:
    parts = path.relative_to(SRC.parent).with_suffix("").parts
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def direct_imports(path: Path, package: str | None = None) -> set[str]:
    """Every `allo.*` module this file pulls in, by any route an author might use.

    Absolute imports, relative imports resolved against the file's own package, and
    `importlib.import_module("allo...")` — a guard that only understands the first
    form is a guard someone routes around without meaning to.
    """
    tree = ast.parse(path.read_text())
    if package is None:
        package = (
            module_name(path) if path.name == "__init__.py" else module_name(path).rsplit(".", 1)[0]
        )
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if node.module:
                    found.add(node.module)
                    # `from allo import groundtruth` binds the subpackage under a name
                    # the plain module string does not contain. It is a working route
                    # and it is this repo's own house style (see cli.py).
                    found.update(f"{node.module}.{alias.name}" for alias in node.names)
            else:
                base = package.split(".")
                base = base[: len(base) - node.level + 1]
                found.add(".".join([*base, node.module] if node.module else base))
                found.update(".".join([*base, a.name]) for a in node.names)
        elif isinstance(node, ast.Call):
            target = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
            if target in {"import_module", "__import__"}:
                found.update(
                    a.value
                    for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                )
    return {name for name in found if name.startswith("allo")}


@pytest.fixture(scope="module")
def graph() -> dict[str, set[str]]:
    return {module_name(p): direct_imports(p) for p in sorted(SRC.rglob("*.py"))}


def reaches(graph: dict[str, set[str]], start: str, target: str) -> list[str] | None:
    """Any import chain from `start` to a module under `target`, or None."""
    stack = [(start, [start])]
    seen = {start}
    while stack:
        node, trail = stack.pop()
        for dep in graph.get(node, ()):
            if dep == target or dep.startswith(target + "."):
                return [*trail, dep]
            if dep not in seen:
                seen.add(dep)
                stack.append((dep, [*trail, dep]))
    return None


def test_prediction_path_never_reaches_ground_truth(graph):
    offenders = []
    for module in graph:
        if not is_prediction_path(module):
            continue
        chain = reaches(graph, module, GROUND_TRUTH)
        if chain:
            offenders.append(" -> ".join(chain))
    assert not offenders, "holo data reaches the prediction path:\n" + "\n".join(offenders)


def test_only_scoring_and_reporting_import_ground_truth(graph):
    unexpected = {
        module
        for module, deps in graph.items()
        if any(d == GROUND_TRUTH or d.startswith(GROUND_TRUTH + ".") for d in deps)
        and is_prediction_path(module)
    }
    assert not unexpected, f"unexpected importers of {GROUND_TRUTH}: {sorted(unexpected)}"


def test_prediction_path_never_reads_the_frozen_label_sets():
    """C1 also has a data route: `frozen.json` contains the answers as plain JSON.

    An import trace cannot see a module that simply opens the file, so check for it
    directly. This is the cheapest way for a prediction stage to cheat.
    """
    offenders = [
        p.relative_to(SRC.parent)
        for p in sorted(SRC.rglob("*.py"))
        if is_prediction_path(module_name(p))
        and ("frozen.json" in (text := p.read_text()) or "FROZEN" in text)
    ]
    assert not offenders, f"prediction-path modules referencing the frozen labels: {offenders}"


def test_the_manifest_reaches_prediction_code_with_the_answer_key_stripped():
    """C1's second data route, and the one an import trace is blindest to.

    `manifest.yaml` is not just an index of apo entries. It names every holo accession and
    effector component ID, and three of its prose fields spell out label residues outright:
    `blind.why` names KRAS 68/95/96/99, `defect` says myristate contacts "16 of the 20"
    labels, and Site 2's `note` gives the whole label-to-active-site distribution. Any
    prediction module may `from allo.inputs import load` without touching `allo.groundtruth`
    and without opening `frozen.json`, so neither existing guard sees it.

    `allo.inputs.load` therefore redacts, and this is the test that says so.
    """
    from allo.groundtruth.manifest import read_manifest
    from allo.inputs import load

    redacted, full = load(), read_manifest()
    forbidden = {"holo", "defect", "note", "blind", "allosteric_evidence", "state"}
    for target in redacted["targets"]:
        leaked = forbidden & set(target)
        assert not leaked, f"{target['id']}: prediction path can see {sorted(leaked)}"
    # Allow-list, not deny-list: a field added to the manifest tomorrow must be redacted by
    # default. If this fires, decide whether the new field is apo-side and add it explicitly.
    known_apo_side = {"id", "tier", "protein", "site", "apo", "active_site", "status"}
    for target in redacted["targets"]:
        assert set(target) <= known_apo_side, (
            f"{target['id']}: unreviewed field(s) {sorted(set(target) - known_apo_side)} "
            "reaching prediction code -- redact in allo.inputs._HOLO_SIDE or allow here"
        )
    # And the redaction has to be doing real work, or it is decoration.
    assert any(forbidden & set(target) for target in full["targets"])


def test_only_the_boundary_module_reads_the_manifest():
    """`allo.inputs` is the one prediction-path module allowed to open the manifest.

    It has to — it needs the chain and the active-site rule. Everything else on the
    prediction path must take the redacted result from it rather than re-reading the file
    and getting the unredacted one.
    """
    offenders = [
        p.relative_to(SRC.parent)
        for p in sorted(SRC.rglob("*.py"))
        if is_prediction_path(module_name(p))
        and module_name(p) != "allo.inputs"
        and ("manifest.yaml" in (text := p.read_text()) or "MANIFEST" in text)
    ]
    assert not offenders, f"prediction-path modules reading the manifest directly: {offenders}"


def test_no_prediction_module_can_reach_an_unredacted_manifest():
    """The hole the two tests above left open, found by an adversarial review.

    `allo.inputs` used to expose `read_manifest` beside `load`. Every guard stayed green
    for a prediction module that imported it: the import trace only watches
    `allo.groundtruth`, and the file-read test greps for `manifest.yaml`/`MANIFEST` --
    neither string appears in `from allo.inputs import read_manifest`. One import returned
    holo accessions, effector IDs and the prose naming label residues.

    The repair is structural rather than another special case: the verbatim read moved to
    `allo.groundtruth.manifest`, so the import guard already covers it. This test holds the
    boundary module clean, because putting it back is a one-line change nothing else sees.
    """
    import allo.inputs

    exported = {
        name
        for name in dir(allo.inputs)
        if not name.startswith("_") and callable(getattr(allo.inputs, name))
    }
    assert "read_manifest" not in exported, (
        "allo.inputs exposes an unredacted manifest reader again -- prediction code can "
        "import it without tripping the import guard or the file-read guard"
    )
    # And what it does export must not carry the holo half through by another name.
    holo_side = {"holo", "defect", "note", "blind", "allosteric_evidence", "state"}
    for target in allo.inputs.load()["targets"]:
        assert not holo_side & set(target), f"{target['id']}: holo fields on the prediction path"


def test_the_manifest_guard_would_catch_the_route_it_missed(graph):
    """A planted prediction module reaching the unredacted manifest must fail the guard."""
    planted = {"allo.rank": {"allo.groundtruth.manifest"}}
    assert is_prediction_path("allo.rank")
    assert reaches(planted, "allo.rank", GROUND_TRUTH) is not None
    # and the real graph is clean on that same route
    for module in graph:
        if is_prediction_path(module):
            assert reaches(graph, module, GROUND_TRUTH) is None, module


def test_experiment_scripts_never_read_the_frozen_label_sets():
    """The same data route, one directory over. `experiments/` is where a run lives,
    and nothing there imports through `src/allo`, so the import graph cannot see it."""
    offenders = [
        p.relative_to(ROOT)
        for p in sorted((ROOT / "experiments").rglob("*.py"))
        if "frozen.json" in (text := p.read_text()) or "groundtruth" in text
    ]
    assert not offenders, f"experiment scripts reaching holo-derived data: {offenders}"


def test_the_detector_sees_every_import_form(tmp_path):
    """A guard that cannot fail is not a guard. Try to route around it, three ways."""
    probe = tmp_path / "_leak_probe.py"
    for source in (
        "from allo.groundtruth.labels import pocket_residues",
        "from ..groundtruth.labels import pocket_residues",
        "from . import x\nfrom ..groundtruth import labels",
        "import importlib\nlabels = importlib.import_module('allo.groundtruth.labels')",
        "from allo import groundtruth",
        "from allo import groundtruth, structure",
    ):
        probe.write_text(source)
        found = direct_imports(probe, package="allo.network")
        assert any(name == GROUND_TRUTH or name.startswith(GROUND_TRUTH + ".") for name in found), (
            f"detector missed: {source!r} -> {found}"
        )


def test_the_detector_would_catch_a_violation(graph):
    """A guard that fails loudly is worth having; one that cannot fail is not."""
    planted = {
        "allo.network.contacts": {"allo.structure.pdb"},
        "allo.structure.pdb": {GROUND_TRUTH},
    }
    assert reaches(planted, "allo.network.contacts", GROUND_TRUTH) is not None
    # and the case the old prefix rule waved through: a prediction module under a
    # name nobody predicted, reaching the labels through the allow-listed benchmark.
    assert is_prediction_path("allo.rank")
    planted = {"allo.rank": {"allo.benchmark"}, "allo.benchmark": {GROUND_TRUTH}}
    assert reaches(planted, "allo.rank", GROUND_TRUTH) is not None
