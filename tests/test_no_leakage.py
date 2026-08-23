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
import shlex
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "allo"
GROUND_TRUTH = "allo.groundtruth"
PROTECTED_PATHS = {
    (ROOT / "structures" / "holo").resolve(),
    (ROOT / "data" / "raw").resolve(),
    (ROOT / "data" / "raw" / "eval").resolve(),
    (ROOT / "docs" / "benchmark" / "frozen.json").resolve(),
}
ALLOWED_PREDICTION_PATHS = {(ROOT / "data" / "raw" / "apo").resolve()}
_KNOWN_INPUT_PATHS = {
    "ROOT": ROOT,
    "MANIFEST": ROOT / "docs" / "benchmark" / "manifest.yaml",
    "APO_STRUCTURES": ROOT / "structures" / "apo",
    "APO_CACHE": ROOT / "data" / "raw" / "apo",
}

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


def _dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute) and (base := _dotted_name(node.value)):
        return f"{base}.{node.attr}"
    return None


def constant_paths_from_source(source: str, filename: Path) -> set[Path]:
    """Paths that can be resolved from constants without executing the source."""
    tree = ast.parse(source)
    values: dict[str, object] = {"__file__": filename.resolve()}
    call_names = {"Path", "pathlib.Path", "PurePath", "pathlib.PurePath"}
    join_names = {"os.path.join"}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "allo.inputs":
            for alias in node.names:
                if alias.name in _KNOWN_INPUT_PATHS:
                    values[alias.asname or alias.name] = _KNOWN_INPUT_PATHS[alias.name]
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "allo.inputs":
                    values[alias.asname or "allo"] = "module:allo.inputs"
        elif isinstance(node, ast.ImportFrom) and node.module == "pathlib":
            for alias in node.names:
                if alias.name in {"Path", "PurePath"}:
                    call_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "os.path":
            for alias in node.names:
                if alias.name == "join":
                    join_names.add(alias.asname or alias.name)

    def evaluate(node: ast.AST) -> object | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, (str, int)):
            return node.value
        if isinstance(node, ast.Name):
            return values.get(node.id)
        if isinstance(node, ast.JoinedStr):
            parts = [
                evaluate(part.value) if isinstance(part, ast.FormattedValue) else part.value
                for part in node.values
            ]
            return (
                "".join(str(part) for part in parts)
                if all(part is not None for part in parts)
                else None
            )
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add) and isinstance(left, str) and isinstance(right, str):
                return left + right
            if (
                isinstance(node.op, ast.Div)
                and isinstance(left, (str, Path))
                and isinstance(right, (str, int))
            ):
                return Path(left) / str(right)
        if isinstance(node, ast.Attribute):
            base = evaluate(node.value)
            if isinstance(base, Path) and node.attr == "parent":
                return base.parent
            if base == "module:allo.inputs" and node.attr in _KNOWN_INPUT_PATHS:
                return _KNOWN_INPUT_PATHS[node.attr]
            if base == "module:allo.inputs" and node.attr == "inputs":
                return base
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute):
            base = evaluate(node.value.value)
            index = evaluate(node.slice)
            if isinstance(base, Path) and node.value.attr == "parents" and isinstance(index, int):
                return base.parents[index]
        if isinstance(node, ast.Call):
            name = _dotted_name(node.func)
            args = [evaluate(arg) for arg in node.args]
            if name in call_names and all(isinstance(arg, (str, Path)) for arg in args):
                return Path(*args)
            if name in join_names and args and all(isinstance(arg, (str, Path)) for arg in args):
                return Path(os.path.join(*(str(arg) for arg in args)))
            if isinstance(node.func, ast.Attribute) and node.func.attr == "resolve":
                base = evaluate(node.func.value)
                if isinstance(base, Path):
                    return base.resolve()
        return None

    assignments = [node for node in ast.walk(tree) if isinstance(node, (ast.Assign, ast.AnnAssign))]
    for _ in range(len(assignments) + 1):
        changed = False
        for node in assignments:
            result = evaluate(node.value)
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if (
                    isinstance(target, ast.Name)
                    and result is not None
                    and values.get(target.id) != result
                ):
                    values[target.id] = result
                    changed = True
        if not changed:
            break

    found: set[Path] = set()
    for node in ast.walk(tree):
        value = evaluate(node)
        if isinstance(value, Path):
            found.add((ROOT / value).resolve() if not value.is_absolute() else value.resolve())
        elif isinstance(value, str) and ("/" in value or "\\" in value):
            path = Path(value)
            found.add((ROOT / path).resolve() if not path.is_absolute() else path.resolve())
    return found


def protected_path_violations(source: str, filename: Path) -> set[Path]:
    violations = set()
    for path in constant_paths_from_source(source, filename):
        if any(path == allowed or allowed in path.parents for allowed in ALLOWED_PREDICTION_PATHS):
            continue
        for protected in PROTECTED_PATHS:
            if path == protected or protected in path.parents:
                violations.add(path)
    return violations


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


def test_the_prediction_path_cannot_build_either_route_out_of_pieces():
    """Both guards above match literal tokens, and a literal is not the only way to write one.

    Adversarial review 2026-08-21 walked past every detector in this file with
    `importlib.import_module("allo." + "ground" + "truth")` and
    `Path("docs") / "benchmark" / ("frozen" + ".json")`: the AST holds a `BinOp`, not a string,
    so `imports_from_source` returned an empty set and no forbidden token appeared anywhere.
    No module was actually doing this -- what failed was the claim that the suite *enforces*
    the boundary.

    Static analysis cannot decide what an arbitrary expression evaluates to, so this does not
    try. It removes the two ingredients instead. Prediction code has no reason to import
    dynamically, and no reason to name `docs/` at all except the one module allowed to read the
    manifest. Neither costs anything today: `importlib` appears nowhere in `src/`, and `"docs"`
    appears twice, in `allo.inputs` (permitted) and `allo.benchmark` (evaluation side).

    What this still cannot catch: a path assembled from `os.environ`, a config file, or a
    parent directory walked at runtime. The guarantee is "no route is spelled here", not "no
    route can exist" -- which is why the cache partition and the redacted `load()` exist as
    independent layers rather than as belt to this brace.
    """
    dynamic = []
    capability_importers = []
    protected_path_names = []
    for path in sorted(SRC.rglob("*.py")):
        module = module_name(path)
        text = path.read_text()
        if "importlib" in text or "__import__" in text:
            dynamic.append(module)
        if (
            is_prediction_path(module)
            and module != "allo.structure.pdb"
            and "_EVALUATION_ACCESS" in text
        ):
            capability_importers.append(module)
        if (
            is_prediction_path(module)
            and module != "allo.structure.pdb"  # owns the runtime denial for these roots
            and (hits := protected_path_violations(text, path))
        ):
            if module == "allo.inputs":
                # This intermediate node is required to spell `data/raw/apo`; the parser
                # runtime guard still denies files directly under the legacy root.
                hits.discard((ROOT / "data" / "raw").resolve())
            if not hits:
                continue
            protected_path_names.append(f"{module}: {sorted(map(str, hits))}")
    assert not dynamic, f"dynamic import defeats the import trace; found in {dynamic}"
    assert not capability_importers, (
        f"prediction modules importing the evaluation parser capability: {capability_importers}"
    )
    assert not protected_path_names, (
        "prediction modules constructing evaluation-only paths: " + "; ".join(protected_path_names)
    )

    for path in outside_runner_files():
        text = path.read_text(errors="ignore")
        assert "importlib" not in text and "__import__" not in text, (
            f"{path.relative_to(ROOT)} imports dynamically, which the runner AST guard "
            "cannot resolve"
        )


def test_constant_path_guard_catches_composition_and_quote_variants(tmp_path):
    probes = {
        "pathlib_single_quotes.py": (
            "from pathlib import Path\np = Path('structures') / 'holo' / 'x.cif'\n"
        ),
        "exported_parent.py": (
            "from allo.inputs import APO_STRUCTURES\np = APO_STRUCTURES.parent / 'holo'\n"
        ),
        "joined_cache.py": (
            "import os\nfrom allo.inputs import APO_CACHE\n"
            "p = os.path.join(APO_CACHE.parent, 'eval')\n"
        ),
        "legacy_cache.py": (
            "from pathlib import Path\np = Path('data') / 'raw' / 'old-holo.cif'\n"
        ),
        "split_literal.py": (
            "from pathlib import Path\np = Path('docs') / 'benchmark' / ('frozen' + '.json')\n"
        ),
    }
    for name, source in probes.items():
        assert protected_path_violations(source, tmp_path / name), f"detector missed {name}"


def test_prediction_parser_has_no_filesystem_or_evaluation_capability():
    """The shared parser accepts content only; privileged path opening stays ground-truth-side."""
    import allo.structure.pdb as prediction_parser

    assert not hasattr(prediction_parser, "parse_mmcif")
    assert not hasattr(prediction_parser, "_EVALUATION_ACCESS")
    assert not hasattr(prediction_parser, "_EVALUATION_ONLY_ROOTS")
    assert callable(prediction_parser.parse_mmcif_text)


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


def test_the_prediction_cache_never_holds_a_holo_structure():
    """C1's third data route, and the one the other two are structurally blind to.

    `frozen.json` and `manifest.yaml` are *files a module names*. Coordinates on disk are
    not: the former prediction-side parser accepted a `Path`, so a constructed cache path
    was readable without importing ground truth and without typing a guarded string. The
    cache used to be shared -- `benchmark.RAW` *was* `allo.inputs.RAW` -- and
    three unmarked assertions in `tests/test_benchmark.py` restored all seven holo entries
    into it, so a clean clone running the offline gate ended up with asciminib's coordinates
    sitting in the directory `apo_input` reads from.

    The fix is a partition, so this is the test that the partition holds. It asserts the
    invariant over whatever the suite has already cached, which is why it must run *after*
    the freeze tests rather than in isolation.
    """
    import yaml

    from allo.groundtruth.structures import EVAL_CACHE
    from allo.inputs import APO_CACHE, APO_STRUCTURES, MANIFEST

    manifest = yaml.safe_load(MANIFEST.read_text())
    apo = {s["apo"]["pdb"].upper() for s in manifest["targets"]}
    holo = {(s.get("holo") or {}).get("pdb", "").upper() for s in manifest["targets"]} - {""}
    assert holo, "manifest declares no holo entries; this test would pass vacuously"
    assert EVAL_CACHE != APO_CACHE, "evaluation and prediction must not share a cache root"

    # An accession may legitimately be both (`1OPL` is apo for one arm), so only entries that
    # are holo and *never* apo are unambiguous evidence of a breach.
    forbidden = holo - apo
    for store in (APO_CACHE, APO_STRUCTURES):
        present = (
            {p.name.split(".")[0].upper() for p in store.glob("*.cif*")}
            if store.exists()
            else set()
        )
        assert not (present & forbidden), (
            f"{store} holds holo-only structures {sorted(present & forbidden)}; prediction "
            "code can read them with parse_mmcif and no guarded string"
        )
    legacy = {p.name for p in APO_CACHE.parent.glob("*.cif*")}
    assert not legacy, (
        f"{APO_CACHE.parent} still holds pre-partition structure files {sorted(legacy)}; "
        "delete them because prediction code must not read the legacy shared cache"
    )


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
    from allo.inputs import _PREDICTION_SCHEMA, load

    assert "site" not in _PREDICTION_SCHEMA["targets"][0], (
        "site display strings name effectors and must remain outside the prediction schema"
    )

    redacted, full = load(), read_manifest()
    forbidden = {"site", "holo", "defect", "note", "blind", "allosteric_evidence", "state"}
    for target in redacted["targets"]:
        leaked = forbidden & set(target)
        assert not leaked, f"{target['id']}: prediction path can see {sorted(leaked)}"
    # Allow-list, not deny-list: a field added to the manifest tomorrow must be redacted by
    # default. If this fires, decide whether the new field is apo-side and add it explicitly.
    known_apo_side = {"id", "protein", "apo", "active_site"}
    for target in redacted["targets"]:
        assert set(target) <= known_apo_side, (
            f"{target['id']}: unreviewed field(s) {sorted(set(target) - known_apo_side)} "
            "reaching prediction code -- it is absent from allo.inputs._PREDICTION_SCHEMA"
        )
    # And the redaction has to be doing real work, or it is decoration.
    assert any(forbidden & set(target) for target in full["targets"])


def test_evaluation_status_cannot_delete_prediction_inputs(tmp_path):
    """A defective holo arm is not an apo-admission decision (ADR 0016)."""
    import yaml

    from allo.groundtruth.manifest import read_manifest
    from allo.inputs import load

    manifest = read_manifest()
    baseline = {target["id"] for target in load()["targets"]}
    for target in manifest["targets"]:
        target["status"] = "excluded" if target.get("status") != "excluded" else "corrected"
    probe = tmp_path / "manifest.yaml"
    probe.write_text(yaml.safe_dump(manifest))
    assert {target["id"] for target in load(probe)["targets"]} == baseline
    mandated = next(
        target for target in manifest["targets"] if target["id"] == "cardiac_myosin_mandated"
    )
    assert mandated["prediction_status"] == "blocked"


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


# Executable prediction entry points outside `src/allo` are walked directly because the
# package import graph cannot reach them. Discovery comes from git rather than filesystem
# directory names, so virtualenvs and dependency trees are excluded without maintaining an
# incomplete list of names such as `.venv`, `venv`, `.tox`, and `node_modules`.

# Naming these is the whole point: `allo.benchmark` is allow-listed *inside* the package
# because it is the evaluation entry point, and it re-exports `load` (the unredacted
# manifest) and `FROZEN` (the label sets). A run script that imports it has the answer key,
# by a route with no `groundtruth` and no `frozen.json` anywhere in its text.
FORBIDDEN_OUTSIDE = (GROUND_TRUTH, "allo.benchmark")
RUNNER_SUFFIXES = {".py", ".sh", ".ipynb"}
FROZEN_TOKENS = ("frozen.json", "FROZEN", "manifest.yaml", "MANIFEST", "groundtruth")
NON_RUNNER_TREES = {
    "src",  # package import-graph tests cover it
    "tests",  # the guards necessarily name forbidden routes
    "docs",  # non-executable evidence and freeze artifacts
    "data",
    "structures",
    "graphify-out",
    ".claude",  # tracked third-party skill helpers, not project prediction runners
}


def is_runner(path: Path) -> bool:
    if path.name == "Makefile" or path.suffix in RUNNER_SUFFIXES:
        return True
    if path.suffix:
        return False
    return os.access(path, os.X_OK) or path.read_text(errors="ignore").startswith("#!")


def outside_runner_files(root: Path = ROOT) -> list[Path]:
    tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    relative = [Path(name.decode()) for name in tracked if name]
    candidates = [root / path for path in relative if path.parts[0] not in NON_RUNNER_TREES]
    return sorted(path for path in candidates if path.is_file() and is_runner(path))


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


def inline_python(text: str) -> list[str]:
    """Constant Python passed with ``python -c`` in shell-like runners."""
    sources = []
    for line in text.splitlines():
        try:
            words = shlex.split(line.lstrip("\t"))
        except ValueError:
            continue
        for index, word in enumerate(words):
            if (
                re.fullmatch(r"python(?:\d+(?:\.\d+)?)?", Path(word).name)
                and index + 2 < len(words)
                and words[index + 1] == "-c"
            ):
                try:
                    ast.parse(words[index + 2])
                except SyntaxError:
                    continue
                sources.append(words[index + 2])
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
        sources = [*embedded_python(text), *inline_python(text)]

    violations = {
        name
        for source in sources
        for name in imports_from_source(source, "")
        for bad in FORBIDDEN_OUTSIDE
        if name == bad or name.startswith(bad + ".")
    }
    violations.update(
        f"evaluation path {hit}"
        for source in sources
        for hit in protected_path_violations(source, path)
    )
    if "_EVALUATION_ACCESS" in text:
        violations.add("evaluation parser capability")
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


def test_the_runner_gate_inspects_trees_nobody_listed(tmp_path):
    """The inclusion list this replaced would have skipped this file entirely."""
    (tmp_path / "tools" / "deep").mkdir(parents=True)
    runner = tmp_path / "tools" / "deep" / "run.py"
    runner.write_text("from allo import benchmark\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "tools/deep/run.py"], check=True)
    assert runner in outside_runner_files(tmp_path)
    assert runner_violations(runner)


def test_runner_discovery_ignores_untracked_dependency_trees(tmp_path):
    tracked = tmp_path / "run.py"
    tracked.write_text("print('prediction runner')\n")
    dependency = tmp_path / "venv" / "site-packages" / "third_party.py"
    dependency.parent.mkdir(parents=True)
    dependency.write_text("FROZEN = object()\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "run.py"], check=True)

    runners = outside_runner_files(tmp_path)
    assert tracked in runners
    assert dependency not in runners


def test_runner_discovery_ignores_tracked_third_party_skill_helpers():
    assert not any(".claude" in path.relative_to(ROOT).parts for path in outside_runner_files())


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


def test_constant_path_guard_covers_every_runner_format(tmp_path):
    python = "from pathlib import Path; p = Path('structures') / 'holo'"
    probes = {
        "run.py": python,
        "run.sh": f'#!/bin/sh\npython -c "{python}"\n',
        "Makefile": f'run:\n\tpython -c "{python}"\n',
        "analysis.ipynb": json.dumps({"cells": [{"cell_type": "code", "source": [python]}]}),
        "run": f'#!/bin/sh\npython -c "{python}"\n',
    }
    for name, source in probes.items():
        path = tmp_path / name
        path.write_text(source)
        if name == "run":
            path.chmod(0o755)
        assert runner_violations(path), f"constant path detector missed {name}"


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
