"""C1: holo-derived data must not reach the prediction path.

Module names prove nothing, so this walks the import graph transitively. Allowed
importers of `allo.groundtruth` are the stages that *score* or *report* — never the
stages that predict.
"""

from __future__ import annotations

import ast
import json
import os
import re
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


def imports_from_source(source: str, package: str) -> set[str]:
    """Every `allo.*` module this file pulls in, by any route an author might use.

    Absolute imports, relative imports resolved against the file's own package, and
    `importlib.import_module("allo...")` — a guard that only understands the first
    form is a guard someone routes around without meaning to.
    """
    tree = ast.parse(source)
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


def direct_imports(path: Path, package: str | None = None) -> set[str]:
    """Python imports in `path`, with relative imports resolved against its package."""
    if package is None:
        package = (
            module_name(path) if path.name == "__init__.py" else module_name(path).rsplit(".", 1)[0]
        )
    return imports_from_source(path.read_text(), package)


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
    known_apo_side = {"id", "protein", "site", "apo", "active_site"}
    for target in redacted["targets"]:
        assert set(target) <= known_apo_side, (
            f"{target['id']}: unreviewed field(s) {sorted(set(target) - known_apo_side)} "
            "reaching prediction code -- it is absent from allo.inputs._PREDICTION_TARGET"
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


# Every directory outside `src/allo` that can execute a prediction. The import graph does
# not reach them -- nothing in `src/allo` imports an experiment -- so they get walked
# directly, with the same AST, against the same rule.
OUTSIDE_THE_PACKAGE = ("experiments", "scripts")

# Naming these is the whole point: `allo.benchmark` is allow-listed *inside* the package
# because it is the evaluation entry point, and it re-exports `load` (the unredacted
# manifest) and `FROZEN` (the label sets). A run script that imports it has the answer key,
# by a route with no `groundtruth` and no `frozen.json` anywhere in its text.
FORBIDDEN_OUTSIDE = (GROUND_TRUTH, "allo.benchmark")
RUNNER_SUFFIXES = {".py", ".sh", ".ipynb"}
FROZEN_TOKENS = ("frozen.json", "FROZEN", "manifest.yaml", "MANIFEST", "groundtruth")


def is_runner(path: Path) -> bool:
    if path.name == "Makefile" or path.suffix in RUNNER_SUFFIXES:
        return True
    if path.suffix:
        return False
    return os.access(path, os.X_OK) or path.read_text(errors="ignore").startswith("#!")


def outside_runner_files(root: Path = ROOT) -> list[Path]:
    candidates = [root / "Makefile"]
    for directory in OUTSIDE_THE_PACKAGE:
        base = root / directory
        if base.exists():
            candidates.extend(path for path in base.rglob("*") if path.is_file())
    return sorted(path for path in candidates if path.exists() and is_runner(path))


def joined_continuations(text: str) -> str:
    """Collapse backslash and parenthesised line continuations onto one line.

    Without this the single-line regex below cannot see a wrapped import: a heredoc holding
    `from allo import (\n    benchmark,\n)` scored zero violations while the module it
    pulls in exposes `benchmark.FROZEN`. `[^\n;]*` cannot cross a newline, so the fix is to
    remove the newline rather than to widen the pattern across the whole file.
    """
    text = re.sub(r"\\\s*\n", "", text)
    text = re.sub(r"\.\s+(?=[A-Za-z_])", ".", text)
    return re.sub(r"\(([^()]*)\)", lambda m: "(" + " ".join(m.group(1).split()) + ")", text)


def embedded_python(text: str) -> list[str]:
    """Python heredocs in shell/Make runners, when their boundaries are explicit."""
    pattern = re.compile(
        r"(?ms)^[^\n]*\bpython(?:\d+(?:\.\d+)?)?\b[^\n]*<<-?\s*(['\"]?)([A-Za-z_]\w*)\1\s*\n"
        r"(.*?)^\s*\2\s*$"
    )
    sources = []
    for match in pattern.finditer(text):
        source = match.group(3)
        try:
            ast.parse(source)
        except SyntaxError:
            continue
        sources.append(source)
    return sources


def runner_violations(path: Path) -> set[str]:
    """Evaluation-side routes in Python, shell, Make recipes, notebooks or entrypoints."""
    text = path.read_text(errors="ignore")
    sources: list[str] = []
    if path.suffix == ".py":
        sources = [text]
    elif path.suffix == ".ipynb":
        notebook = json.loads(text)
        sources = [
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
            if cell.get("cell_type") == "code"
        ]
    else:
        sources = embedded_python(text)

    violations = {
        name
        for source in sources
        for name in imports_from_source(source, "")
        for bad in FORBIDDEN_OUTSIDE
        if name == bad or name.startswith(bad + ".")
    }
    if path.suffix not in {".py", ".ipynb"}:
        flat = joined_continuations(text)
        for bad in FORBIDDEN_OUTSIDE:
            if bad in flat:
                violations.add(bad)
        if re.search(r"\bfrom\s+allo\s+import\s+[^\n;]*\bbenchmark\b", flat):
            violations.add("allo.benchmark")
        if re.search(r"\ballo\s+benchmark\s+(?:freeze|show|stats)\b", flat):
            violations.add("allo benchmark evaluation command")
    violations.update(token for token in FROZEN_TOKENS if token in text)
    return violations


def test_run_scripts_never_import_the_evaluation_side():
    """The hole a string search left open, found by an adversarial review.

    The old guard grepped `experiments/*.py` for `frozen.json` or `groundtruth`. Neither
    string appears in `from allo import benchmark`, and `benchmark.load()` returns the
    unredacted manifest while `benchmark.FROZEN` points at the labels. A run script could
    read both with every leakage test green.
    """
    runners = outside_runner_files()
    assert runners, "runner leakage gate inspected no files"
    assert ROOT / "Makefile" in runners
    assert ROOT / "scripts" / "check.sh" in runners
    offenders = [
        f"{path.relative_to(ROOT)} -> {sorted(hit)}"
        for path in runners
        if (hit := runner_violations(path))
    ]
    assert not offenders, "run scripts reaching the evaluation side:\n" + "\n".join(offenders)


def test_run_scripts_never_name_the_frozen_files_either():
    """Belt to the import guard's braces: a bare `open()` needs no import at all."""
    offenders = [
        path.relative_to(ROOT)
        for path in outside_runner_files()
        if any(token in path.read_text(errors="ignore") for token in FROZEN_TOKENS)
    ]
    assert not offenders, f"run scripts naming a frozen file directly: {offenders}"


def test_the_run_script_guard_would_catch_a_violation(tmp_path):
    """A guard that cannot fail is not a guard."""
    for source in (
        "from allo import benchmark",
        "from allo.benchmark import FROZEN",
        "import allo.benchmark as b",
        "from allo.groundtruth.manifest import read_manifest",
    ):
        probe = tmp_path / "run.py"
        probe.write_text(source)
        found = direct_imports(probe, package="")
        assert any(
            name == bad or name.startswith(bad + ".") for name in found for bad in FORBIDDEN_OUTSIDE
        ), f"detector missed: {source!r} -> {found}"


def test_a_wrapped_import_inside_a_runner_is_still_a_violation(tmp_path):
    """`[^\\n;]*` cannot cross a newline, so the guard read a wrapped import as clean.

    A review wrote `from allo import (\\n    benchmark,\\n)` into a heredoc and the runner
    gate stayed green while the module it pulls in exposes `benchmark.FROZEN`. Both
    continuation forms Python accepts are probed, because fixing only the one that was
    reported leaves the sibling open.
    """
    wrapped = {
        "parens.sh": "#!/bin/sh\npython - <<'PY'\nfrom allo import (\n    benchmark,\n)\nPY\n",
        "backslash.sh": "#!/bin/sh\npython - <<'PY'\nfrom allo import \\\n    benchmark\nPY\n",
    }
    for name, source in wrapped.items():
        probe = tmp_path / name
        probe.write_text(source)
        assert runner_violations(probe), f"wrapped import read as clean: {name}"


def test_a_backslash_split_import_is_caught_at_every_token_boundary(tmp_path):
    """Python removes a backslash-newline before tokenising, including after a dot."""
    wrapped = {
        "before_dot": "import allo\\\n    .benchmark",
        "after_dot": "import allo.\\\n    benchmark",
        "before_import": "from allo \\\n    import benchmark",
        "after_import": "from allo import \\\n    benchmark",
    }
    for name, statement in wrapped.items():
        probe = tmp_path / f"{name}.sh"
        probe.write_text(f"#!/bin/sh\npython - <<'PY'\n{statement}\nPY\n")
        assert runner_violations(probe), f"split import read as clean: {name}"


def test_the_prediction_manifest_is_built_from_an_allow_list(tmp_path):
    """`load()` claimed allow-list redaction and was a per-target deny-list with no top-level
    filter at all, so `orthosteric_vocabulary` and the whole `null` model reached prediction
    code. The property that matters is not which names leak today but that an unknown one
    cannot: this plants fields at both levels and requires their absence.
    """
    import yaml

    from allo.groundtruth.manifest import read_manifest
    from allo.inputs import load

    planted = read_manifest()

    # Plant at every mapping level the prediction schema admits. The old implementation
    # copied `defaults` and `apo` wholesale, so testing only the top level and target level
    # gave a green guard while nested answer fields crossed C1.
    def plant_every_mapping(value):
        if isinstance(value, dict):
            value["nested_answer"] = [68, 95, 96, 99]
            for child in list(value.values()):
                plant_every_mapping(child)
        elif isinstance(value, list):
            for child in value:
                plant_every_mapping(child)

    plant_every_mapping(planted)
    probe = tmp_path / "manifest.yaml"
    probe.write_text(yaml.safe_dump(planted))

    redacted = load(probe)

    def assert_rejected(value):
        if isinstance(value, dict):
            assert "nested_answer" not in value
            for child in value.values():
                assert_rejected(child)
        elif isinstance(value, list):
            for child in value:
                assert_rejected(child)

    assert_rejected(redacted)
    assert set(redacted) == {"defaults", "targets"}
    assert set(redacted["defaults"]) == {"contact_cutoff_angstrom"}
    assert all("tier" not in target and "status" not in target for target in redacted["targets"])
    assert "cutoff_sensitivity" not in redacted["defaults"]
    for evaluation_only in ("null", "orthosteric_vocabulary"):
        assert evaluation_only not in redacted, f"{evaluation_only} still reaches prediction code"
    for holo_side in ("holo", "defect", "note", "blind"):
        assert not any(holo_side in target for target in redacted["targets"])


def test_the_runner_guard_covers_every_executable_format(tmp_path):
    probes = {
        "run.py": "from allo import benchmark",
        "run.sh": "#!/bin/sh\nuv run python -c 'from allo import benchmark'\n",
        "Makefile": "run:\n\tuv run allo benchmark stats\n",
        "analysis.ipynb": json.dumps(
            {"cells": [{"cell_type": "code", "source": ["import allo.groundtruth\n"]}]}
        ),
        "run": "#!/bin/sh\nuv run allo benchmark show\n",
    }
    for name, source in probes.items():
        path = tmp_path / name
        path.write_text(source)
        if name == "run":
            path.chmod(0o755)
        assert is_runner(path), f"runner discovery missed {name}"
        assert runner_violations(path), f"runner leakage detector missed {name}"


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
