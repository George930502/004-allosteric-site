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
import sys
from pathlib import Path, PurePath

import pytest

ROOT = Path(__file__).resolve().parents[1]
# Everything importable from the installed package root. The scans below rglob SRC_ROOT,
# not the `allo` package: `NON_RUNNER_TREES` exempts the whole of `src/` from the runner scan
# on the stated ground that "package import-graph tests cover it", and until 2026-09-03 those
# tests globbed `src/allo` only. A probe package at `src/predict/` was therefore scanned by
# neither -- it imported `allo.groundtruth.labels`, read the evaluation freeze by literal
# path, and recovered the positive count for all fifteen arms with the whole suite green. The
# editable install puts `src/` on `sys.path`, so a second package there is importable the day
# it is written. `module_name` already names modules relative to `src/`, so widening the glob
# is all that was missing.
SRC_ROOT = ROOT / "src"
SRC = SRC_ROOT / "allo"
GROUND_TRUTH = "allo.groundtruth"
PROTECTED_PATHS = {
    (ROOT / "structures" / "holo").resolve(),
    (ROOT / "data" / "raw").resolve(),
    (ROOT / "data" / "raw" / "eval").resolve(),
    # Routes one and two, widened to the whole tree on 2026-09-02. `frozen.json` was
    # protected on the first day and its own siblings were not: `primary/README.md:243` and
    # `secondary/README.md:178` tabulate a `Scoreable` column that IS the positive count,
    # beside the holo accession, the holo chain and the effector component ID -- for all
    # five sealed `generalisation` arms as well. That is the payload `selection.json` is
    # protected for (route three) and the payload `data/patches` is protected for (route
    # six), sitting unguarded next to the file protected first. Protected whole, on the
    # argument `evaluation/` and `review/` already use: a file added here later is protected
    # by default rather than leaked by default. The three entries below that now sit inside
    # these trees -- `selection.json`, `extension-candidates.md` and `primary/audit/` -- are
    # redundant against them and are kept, because each records the route it closed and the
    # date it was found.
    #
    # `allo.inputs` is the one prediction-path module that must spell the two manifests, and
    # `MANIFEST_READS` below is the exemption. It names the manifests and the directories
    # leading to them, so every OTHER file in these trees stays guarded for that module too.
    (ROOT / "docs" / "benchmark" / "primary").resolve(),
    (ROOT / "docs" / "benchmark" / "secondary").resolve(),
    # The candidate ledger is the third data route. It is not prose: for every admitted arm
    # it carries `holo`, `holo_chain` and `effector` as structured fields, which is a label
    # set three lines of code away, and its `detail` strings name real label residues
    # (ns5b P495, ecoli_cps S948). Found by an adversarial audit after the first two routes
    # were closed.
    (ROOT / "docs" / "benchmark" / "secondary" / "selection.json").resolve(),
    # The fourth route, added 2026-08-24. A screening record for candidate arms that were
    # measured and NOT admitted. It names real label residues in apo numbering, plus holo
    # accessions and effector component IDs, so it is an answer key for arms that do not
    # exist yet. Guarded on the same argument as `selection.json`.
    (ROOT / "docs" / "benchmark" / "secondary" / "evidence" / "extension-candidates.md").resolve(),
    # The fifth route, added 2026-08-25 with the evaluation layer. Everything under
    # `evaluation/` is derived from the label sets: `frozen.json` carries each arm's decoy
    # pocket linings, and a decoy is defined as a pocket that does NOT touch the site, so
    # the decoy list is the label set's complement among detected pockets. The directory is
    # protected whole rather than file by file, so a file added there later is protected by
    # default rather than leaked by default.
    (ROOT / "docs" / "benchmark" / "evaluation").resolve(),
    # The sixth route, added 2026-08-27 by a design-stage constraint audit. The matched-patch
    # cache is derived from the label set and it says so in its own array shapes: `members`
    # has width equal to the arm's positive count for all fifteen arms, the five sealed
    # `generalisation` arms included. Redacted 2026-09-03: this comment used to print three of
    # those counts and the range of the sealed five, which is the payload it warns about.
    # C1 forbids holo-derived information reaching prediction code and names this
    # exact case: "not even the residue count". Its `diagnostics` string carries more --
    # `observed_median_distance_to_source`, `observed_radius_of_gyration` and
    # `observed_mean_degree` are geometric properties of the true site. `allo.scoring` writes
    # and reads it; nothing on the prediction path may.
    (ROOT / "data" / "patches").resolve(),
    # The seventh route, added 2026-09-02 by ADR 0034. The multi-axis review carries
    # per-arm positive counts (`01`, `02`, `10`, `12`), five real KRAS label residues
    # (`03-kras-mask.md`), and a candidate ledger with holo accessions and effector
    # component IDs -- the same shape as `selection.json` above. C1 names the residue
    # count directly, and `extension-candidates.md` is already a protected Markdown
    # answer key on the identical argument. Protected whole, like `evaluation/`, so a
    # file added later is protected by default rather than leaked by default.
    (ROOT / "docs" / "benchmark" / "review").resolve(),
    # Routes eight to ten, added 2026-09-02 after a sweep of every tracked `.md`, `.yaml`,
    # `.json` and `.txt` outside the seven trees above for a run of label residues inside
    # one 400-character window. Three files cleared the coincidence floor, and all three
    # are answer keys in prose.
    #
    # Eight: the per-target input audits. `kras-g12c.md` tabulates the `MOV` contact shell
    # and reproduces 21 of 21 label residues for both KRAS arms; `bcr-abl1.md` reproduces
    # 18 of 18 and 17 of 17. These are the label sets, written out, one directory above
    # the `frozen.json` that was protected on the first day. Protected whole.
    (ROOT / "docs" / "benchmark" / "primary" / "audit").resolve(),
    # Nine: the shared literature evidence. `allosteric-prediction-prior-art.md` prints
    # "our frozen KRAS distal label set ... is `9, 59, 60, ...`" as running prose, to make
    # a point about ASD coverage. Protected whole, on the `evaluation/` argument: a file
    # added here later is protected by default rather than leaked by default.
    (ROOT / "docs" / "benchmark" / "evidence").resolve(),
    # Ten: the experiment record. Every `metrics.json` a calibration run writes carries the
    # matched-patch sampler diagnostics, and `observed_radius_of_gyration` is the true
    # site's own geometry -- 65 such fields in the 2026-09-02 recalibration alone, for the
    # six primary arms and for all five sealed `generalisation` arms by name. `data/patches`
    # was protected for exactly this content in August; the copy the runner persists beside
    # it was not. A runner that derives its output directory from `__file__` does not name
    # this path, so protecting the tree costs the runners nothing.
    (ROOT / "experiments").resolve(),
    # The eleventh route, found 2026-09-02 by re-running the label sweep with three-letter
    # residue codes normalised. `docs/targets.md:170` prints the cardiac myosin site in
    # three-letter codes -- 12 of 12 `label_residues` for BOTH myosin arms, and line 172 adds
    # the minimum label-to-source distance per arm, which is a scored quantity.
    #
    # The residues themselves used to be quoted here, and this file is neither protected nor
    # scanned, so the comment explaining the route WAS the route. Found 2026-09-03. Describe
    # an answer key by its shape and its location; never by its contents.
    #
    # The earlier sweep matched bare integers on a word boundary, so a three-letter code did
    # not match its own number and the whole set was invisible to it. That sweep cleared the
    # file and the
    # clearance was written down as a refutation. A detector's false negative is the one
    # kind of finding that closes a question instead of opening it, which is why the sweep
    # that replaced it normalises the codes.
    (ROOT / "docs" / "targets.md").resolve(),
    # The twelfth route, found 2026-09-03 by the same sweep run over the trees the eleventh
    # cleared. `docs/adr/0031-cardiac-myosin-holo-substitution.md:22` prints the `9GZ2`
    # contact shell in three-letter codes -- 12 of 12 `label_residues` for both myosin arms,
    # the same set `docs/targets.md` was protected for one day earlier. An ADR argues from
    # the evidence, so the evidence lands in it, and the tree holds 37 of them. Protected
    # whole rather than file by file, for the reason `evaluation/` and `review/` are: an ADR
    # written next week is protected by default rather than leaked by default.
    (ROOT / "docs" / "adr").resolve(),
    # The fourteenth route, found 2026-09-03 by an adversarial pass, and it is a class the
    # label sweep could not see. `09a-power-verification.md` tabulates "m (scoreable labels)"
    # per arm and `17-generalisation-variance.md` does the same for four secondary arms. Those
    # are POSITIVE COUNTS, not residue numbers, and C1 names the count in as many words: "not
    # even the residue count". Every sweep before this one matched residue identities, so a
    # table of counts passed every one of them. The gap is now closed in two places -- this
    # entry, and `test_no_unprotected_tracked_file_reproduces_a_positive_count`, which is what
    # catches the next file rather than this one. Protected whole, on the `evaluation/`
    # argument: the tree holds 23 documents and a survey written next week joins them.
    (ROOT / "docs" / "evidence" / "method-landscape").resolve(),
}


# The tracked ledger of former names. It is the source rather than the cross-check, so the
# guard is the same strength in a shallow clone and in a `git archive` export as it is here.
FORMER_PATH_LEDGER = ROOT / "tests" / "former_protected_paths.json"


def renamed_into_protected() -> set[Path]:
    """Every path a protected file has lived at before.

    A protected path is protected by its name, and a rename gives the same bytes a second
    name that no entry above covers. `docs/benchmark/audit/kras-g12c.md` became
    `docs/benchmark/primary/audit/kras-g12c.md` on 2026-08-31, and
    `git show <sha>:docs/benchmark/audit/kras-g12c.md` still returns the 21-of-21 KRAS
    contact shell -- from `main`, with no network, under a path the guard reads as ordinary
    documentation. The segment-cover backstop does not reach it either: the old name is
    missing the `primary` component, so it covers no protected root.

    Two of the five renames were backstopped by a `FROZEN_TOKEN` (`frozen.json`,
    `manifest.yaml`) and the three audit files were not, which is the same asymmetry that
    made `data/patches` the hole in September. Deriving the list from git closes the class
    instead of the instance: a rename next week is protected the day it is made.
    """
    return {
        (ROOT / name).resolve()
        for name in json.loads(FORMER_PATH_LEDGER.read_text())["former_paths"]
    }


def renamed_into_protected_from_git() -> set[Path] | None:
    """The same list, derived from history, or None when there is no history to read.

    This is the cross-check and not the source. Deriving it at import time made the guard
    depend on clone depth: a `--depth=1` fetch and a `git archive` export both produce an
    empty set, and a machine with no `git` binary raises during collection. Found 2026-09-03
    by an adversarial pass, which ran the shallow clone. A guard that is weaker in an export
    than in a working clone is weakest exactly where a release is verified.

    **Deletions count, not only renames -- widened 2026-09-03 by a second adversarial pass.**
    Reading `--diff-filter=R` alone missed three files. `docs/benchmark/audit/*.json` were
    converted to Markdown, which git recorded as a delete plus an add rather than a rename
    because the bytes changed too much. They reproduce every primary label set and
    `git show <sha>^:docs/benchmark/audit/kras-g12c.json` still returns them. A rename and a
    delete leave the same artefact -- content that was protected, under a name that is not --
    so the filter is `RD` and the deleted path is kept when it sat inside a protected tree.
    """
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "log",
                "--all",
                "-M",
                "--diff-filter=RD",
                "--name-status",
                "--format=",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None

    def guarded_now(path: Path) -> bool:
        return any(path == root or root in path.parents for root in PROTECTED_PATHS)

    former: set[Path] = set()
    deleted: set[Path] = set()
    emptied: set[Path] = set()
    for line in result.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) == 3 and fields[0].startswith("R"):
            was, now = (ROOT / fields[1]).resolve(), (ROOT / fields[2]).resolve()
            if guarded_now(now):
                former.add(was)
                emptied.add(was.parent)
        elif len(fields) == 2 and fields[0].startswith("D"):
            deleted.add((ROOT / fields[1]).resolve())

    # A deletion qualifies on either of two grounds. The direct one is that the file sat
    # inside a tree that is protected today, which is how the four `structures/holo` entries
    # arrive. The second is the one the `.json` audit files needed: they were CONVERTED to
    # Markdown, so git saw a delete plus an add and not a rename, and their own directory
    # `docs/benchmark/audit/` was never protected -- only the `docs/benchmark/primary/audit/`
    # it became. So a directory that lost any file to a protected tree is treated as a former
    # protected tree itself, and everything ever deleted from it comes with.
    for gone in deleted:
        if guarded_now(gone) or gone.parent in emptied:
            former.add(gone)
    return former


# Kept apart from `PROTECTED_PATHS` on purpose. The resolver compares a concrete path and
# must know the former names; the segment cover asks whether a file holds every component of
# a path, and a former name shares most of its components with the current one -- so folding
# these in would fire on `allo.inputs` for `docs/benchmark/manifest.yaml` the moment it
# spells `docs/benchmark/primary/manifest.yaml`, which is its one exemption.
FORMER_PROTECTED_PATHS = renamed_into_protected()
ALLOWED_PREDICTION_PATHS = {(ROOT / "data" / "raw" / "apo").resolve()}

# `allo.inputs` needs the chain and the active-site rule, so it is the one prediction-path
# module that spells a path inside the two protected input trees. It reads them through the
# `_PREDICTION_SCHEMA` allow-list, so the answer key never survives the read. Only these
# paths are exempt: `primary/README.md` and `secondary/README.md` publish the positive count
# and stay guarded for this module like every other.
MANIFEST_READS = {
    (ROOT / "docs" / "benchmark" / "primary").resolve(),
    (ROOT / "docs" / "benchmark" / "secondary").resolve(),
    (ROOT / "docs" / "benchmark" / "primary" / "manifest.yaml").resolve(),
    (ROOT / "docs" / "benchmark" / "secondary" / "manifest.yaml").resolve(),
}

# The review directory's own tools write into it, so protecting the tree makes every
# such script name five protected paths -- all of them its own output. The guard
# resolves `Path(__file__).resolve().parent`, so deriving the output directory from the
# script's location does not escape it, and `data/` commits nothing while `experiments/`
# is scanned, so there is nowhere to move them to (ADR 0034).
#
# The exemption is a rule, not a list of names. A prediction runner must import `allo` to
# run a method, so a tracked review-side file that imports no `allo` module cannot be one.
# `test_every_exempt_review_tool_imports_no_package_module` holds the second half.
REVIEW_TOOLS = (ROOT / "docs" / "benchmark" / "review").resolve()

# The tenth route is a tree the runners themselves write into, so it cannot be protected
# the way the other nine are. What leaks is the record, not the directory: `metrics.json`
# and `records.jsonl` carry the matched-patch sampler diagnostics, and
# `observed_radius_of_gyration` is the true site's own geometry. A `config.yaml` carries
# graph settings an experimenter wrote and no holo-derived value, which is why one runner
# legitimately reads another run's config.
#
# The rule is therefore narrower than a tree: **no file may name a record it did not
# write.** A run script may name the two records beside it; every other file, runner or
# module, may name neither. Anything else under `experiments/` is not a violation.
EXPERIMENTS = (ROOT / "experiments").resolve()
RUN_RECORDS = {"metrics.json", "records.jsonl"}


def allowed_experiment_path(hit: Path, source_file: Path) -> bool:
    """A hit under `experiments/` that `source_file` is entitled to name.

    Naming the tree, a run directory or a `config.yaml` is how `allo.experiment` scaffolds
    a run and how the runners write their outputs. Naming a `metrics.json` or a
    `records.jsonl` that some other run wrote is the leak, and no file is entitled to it.
    """
    if hit != EXPERIMENTS and EXPERIMENTS not in hit.parents:
        return False
    if hit.name not in RUN_RECORDS:
        return True
    owner = source_file.resolve().parent
    return EXPERIMENTS in owner.parents and owner == hit.parent


_KNOWN_INPUT_PATHS = {
    "ROOT": ROOT,
    "MANIFEST": ROOT / "docs" / "benchmark" / "primary" / "manifest.yaml",
    "SECONDARY_MANIFEST": ROOT / "docs" / "benchmark" / "secondary" / "manifest.yaml",
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
    parts = path.relative_to(SRC_ROOT).with_suffix("").parts
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
    # `from src.allo.groundtruth import ...` runs whenever the repository root is on the
    # path, which is how a scratch script and a notebook usually import it. Without this
    # line the detector reads that as a third-party module and returns nothing.
    found = {n.removeprefix("src.") for n in found}
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


# What the interpreter accepts as a path component. `Path` belongs here because
# `Path("data") / Path("patches")` and `d.joinpath(Path("patches"))` both resolve at runtime.
# The guard modelled `str` and `int` only, so a `Path` on the right of `/` made the whole
# expression evaluate to None and the composed protected path vanished from the scan --
# `data/patches` is protected as a path and is NOT a frozen token, so nothing backstopped it.
# Fourth instance of one failure mode: the guard reads the text correctly and the interpreter
# accepts a form the text does not model. Found 2026-09-03 by an adversarial pass. One
# constant is used by every composition branch below, so a fifth spelling has one place to fix.
_PATH_PART = (str, int, Path, PurePath)
# A base is what a path can start from. `int` is excluded because `Path(1)` raises, and an
# integer on the left of `/` is arithmetic rather than a path.
_PATH_BASE = (str, Path, PurePath)


def constant_paths_from_source(source: str, filename: Path) -> set[Path]:
    """Paths that can be resolved from constants without executing the source."""
    tree = ast.parse(source)
    values: dict[str, object] = {"__file__": filename.resolve()}
    call_names = {"Path", "pathlib.Path", "PurePath", "pathlib.PurePath"}
    join_names = {"os.path.join"}
    dirname_names = {"os.path.dirname"}

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
                if alias.name == "dirname":
                    dirname_names.add(alias.asname or alias.name)

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
                and isinstance(left, _PATH_BASE)
                and isinstance(right, _PATH_PART)
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
            if name in call_names and all(isinstance(arg, _PATH_PART) for arg in args):
                return Path(*args)
            if name in join_names and args and all(isinstance(arg, _PATH_PART) for arg in args):
                return Path(os.path.join(*(str(arg) for arg in args)))
            if isinstance(node.func, ast.Attribute) and node.func.attr == "resolve":
                base = evaluate(node.func.value)
                if isinstance(base, Path):
                    return base.resolve()
            # `d.joinpath("frozen.json")` is `d / "frozen.json"`, and the `/` operator was
            # modelled while the method was not. A prediction module reaching `data/patches`
            # this way produced zero violations and no frozen token, because `patches` is not
            # a token: the whole matched-patch cache was readable with all 34 tests green.
            # Third instance of one failure mode -- the guard reads the text correctly and
            # the interpreter accepts a form the text does not model. Found 2026-09-02.
            if isinstance(node.func, ast.Attribute) and node.func.attr == "joinpath":
                base = evaluate(node.func.value)
                args = [evaluate(arg) for arg in node.args]
                if isinstance(base, Path) and args and all(isinstance(a, _PATH_PART) for a in args):
                    return base.joinpath(*(str(a) for a in args))
            # `os.path.dirname` walks up the way `.parent` does. Without it a prefix built
            # from `dirname(__file__)` evaluates to None and every path concatenated onto
            # that prefix disappears from the scan.
            # `Path("experiments").glob("*/metrics.json")` names a record without spelling a
            # resolvable path, so the record rule saw only `experiments/` and allowed it.
            # Modelling the pattern as a path component gives the rule a name to reject.
            # `iterdir()` stays open by construction -- its result is a loop variable and no
            # static evaluator can follow it. That residual is stated in AGENTS.md.
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"glob", "rglob"}:
                base = evaluate(node.func.value)
                pattern = evaluate(node.args[0]) if node.args else None
                if isinstance(base, Path) and isinstance(pattern, str):
                    return base / pattern
            if _dotted_name(node.func) in dirname_names and len(node.args) == 1:
                base = evaluate(node.args[0])
                if isinstance(base, _PATH_BASE):
                    # A str, as the real function returns, so that `dirname(...) + "/x"`
                    # composes through the string-addition branch below.
                    return os.path.dirname(str(base))
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


def literal_segments(source: str) -> set[str]:
    """Every path component that appears as a literal anywhere in the source.

    Split on the separators and on whitespace, so a component survives being glued to a
    command word. `os.system("cat docs/benchmark/primary/audit/kras-g12c.md")` yields
    `docs` as well as `cat`, and a one-word prefix no longer hides the route.

    A `bytes` literal is decoded first. `open`, `os.open` and `os.stat` all accept one, and
    both `evaluate` and the fallback scan test `isinstance(value, str)`, so `b"data/patches"`
    was invisible to the resolver at two places at once.
    """
    segments: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return segments
    docstrings = {
        node.body[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
        and node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
    }
    for node in ast.walk(tree):
        # A path component built from code points leaves no string and no bytes literal:
        # `Path(*(bytes(x).decode() for x in [[100, 111, 99, 115], ...]))` reads
        # `docs/benchmark/primary/frozen.json` and was invisible to the resolver and to the
        # harvest at once. Found 2026-09-03 by an adversarial pass. Any run of printable code
        # points is decoded and offered as text.
        if isinstance(node, ast.List | ast.Tuple):
            points = [
                e.value
                for e in node.elts
                if isinstance(e, ast.Constant) and isinstance(e.value, int) and 32 <= e.value < 127
            ]
            if points and len(points) == len(node.elts):
                segments.update(_components("".join(map(chr, points))))
            continue
        if not isinstance(node, ast.Constant) or node in docstrings:
            continue
        value = node.value
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="ignore")
        if not isinstance(value, str):
            continue
        segments.update(_components(value))
    return segments


def _components(value: str) -> set[str]:
    """The path components a string offers, or the whole string when it is one bare word.

    A string carrying a separator is split on it, and on whitespace and colon too, so neither
    a command word nor a revision prefix hides a component: `cat docs/...` and
    `HEAD~9:docs/...` both yield `docs`. A string with no separator counts only when it is a
    single word, which keeps prose out: a docstring is skipped entirely and a phrase offers
    nothing.
    """
    if "/" in value or "\\" in value:
        return {part for part in re.split(r"[/\\\s:]+", value) if part}
    stripped = value.strip()
    return {stripped} if stripped and not stripped.split()[1:] else set()


def segment_cover_violations(source: str) -> set[Path]:
    """Protected roots whose every component appears as a literal in this file.

    The resolver above is a whitelist of spellings, and a whitelist loses this race. An
    adversarial pass on 2026-09-03 listed 26 spellings that assemble a protected path out of
    separator-free components and vanish from it: `"/".join(["data", "patches"])`,
    `"{}/{}".format(...)`, `os.sep.join`, `chr(47)`, a tuple assignment, a walrus, an
    augmented assignment, a for-loop accumulation, a dict lookup, `Path.cwd() / ...`,
    `Path.home() / ...`, a starred `Path(*parts)`, `.with_name`, and a shell string with a
    command word in front. Three of them ran together in one tracked probe runner and read
    the matched-patch cache, the per-target input audits and the sealed tier's positive
    counts with all 37 tests green.

    Every one of them leaves the components behind as literals in the same file, because the
    interpreter has to get the characters from somewhere. So this asks the question the other
    way round: not "which path does this expression build", which needs the whole language,
    but "does this file hold every piece of a protected path", which needs no evaluation at
    all. It is the backstop, not the primary: the resolver still reports the concrete path,
    which is the message a reader can act on.

    Two rules keep it honest. Only roots of two or more components are covered, because a
    one-word root such as `experiments` is a word before it is a path, and the resolver plus
    `allowed_experiment_path` already handle that tree. And a root is excused when the file
    also covers a deeper path that is explicitly allowed, which is what lets
    `allo.structure.pdb` spell `data/raw/apo` without `data/raw` firing underneath it.
    """
    segments = literal_segments(source)

    def covered(path: Path) -> bool:
        parts = path.relative_to(ROOT).parts
        return len(parts) >= 2 and all(part in segments for part in parts)

    # A former name enters the cover only when no `FROZEN_TOKEN` already backstops it. Two of
    # the five renames carry their token in the file name (`frozen.json`, `manifest.yaml`) and
    # are caught in a runner by the token scan and in a module by
    # `test_prediction_path_never_reads_the_frozen_label_sets`; covering them here would fire
    # on `allo.inputs`, whose one exemption is to spell the manifest. The three audit files
    # carry no token, which is the asymmetry that left them readable.
    former = {
        path
        for path in FORMER_PROTECTED_PATHS
        if not any(token in path.name for token in FROZEN_TOKENS)
    }
    allowed = {path for path in ALLOWED_PREDICTION_PATHS if covered(path)}
    return {
        protected
        for protected in PROTECTED_PATHS | former
        if covered(protected) and not any(protected in path.parents for path in allowed)
    }


def protected_path_violations(source: str, filename: Path) -> set[Path]:
    violations = set()
    for path in constant_paths_from_source(source, filename):
        if any(path == allowed or allowed in path.parents for allowed in ALLOWED_PREDICTION_PATHS):
            continue
        for protected in PROTECTED_PATHS | FORMER_PROTECTED_PATHS:
            if path == protected or protected in path.parents:
                violations.add(path)
    return violations | segment_cover_violations(source)


@pytest.fixture(scope="module")
def graph() -> dict[str, set[str]]:
    """The import graph, with the edges Python adds that the source text does not show.

    `import a.b.c` executes `a/__init__.py` and `a/b/__init__.py` before `c`, so a module
    that names only the submodule still runs everything the parent packages import. The
    graph built from import statements alone does not carry those edges, and the gap is not
    theoretical: `from allo.scoring.properties import residue_properties` reaches
    `allo.groundtruth` at runtime through `allo/scoring/__init__.py`, while
    `allo.scoring.properties` itself imports nothing but `allo.inputs`. Every guard was
    green on that route -- no protected path, no frozen token, no `groundtruth` in the text.
    Found by the 2026-08-27 design-stage constraint audit.

    Adding parent edges is exact rather than conservative. It encodes what the interpreter
    does, so it introduces no false positive: if the parent package is clean, the edge leads
    nowhere.
    """
    direct = {module_name(p): direct_imports(p) for p in sorted(SRC_ROOT.rglob("*.py"))}
    for module, deps in direct.items():
        for dep in list(deps):
            parts = dep.split(".")
            deps.update(".".join(parts[:i]) for i in range(1, len(parts)))
        deps.discard(module)
    return direct


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


def test_a_submodule_import_cannot_smuggle_the_parent_package_in(graph, tmp_path):
    """A guard that cannot fail is not a guard, and this one could not until 2026-08-27.

    `from allo.scoring.properties import residue_properties` names a module whose own imports
    are `numpy`, `scipy` and `allo.inputs`. Reading the source, it is clean. Running it, the
    interpreter executes `allo/scoring/__init__.py` first and `allo.groundtruth` is in the
    process. The first assertion pins the runtime fact, the second pins the fix.
    """
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import allo.scoring.nulls; "
            "print(any(m.startswith('allo.groundtruth') for m in sys.modules))",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert probe.stdout.strip() == "True", "the route this test exists for is gone; delete it"

    synthetic = {
        "allo.network.sneak": {"allo.scoring.nulls"},
        "allo.scoring": {GROUND_TRUTH},
        "allo.scoring.nulls": {"allo.inputs"},
    }
    for module, deps in synthetic.items():
        for dep in list(deps):
            parts = dep.split(".")
            deps.update(".".join(parts[:i]) for i in range(1, len(parts)))
        deps.discard(module)
    assert reaches(synthetic, "allo.network.sneak", GROUND_TRUTH), (
        "parent-package edges are missing from the import graph"
    )


def test_no_prediction_package_imports_the_evaluation_layer(graph):
    """`AGENTS.md`: no prediction-path module imports `allo.scoring`.

    Stated in the contract since Phase 2 and unchecked until 2026-08-27. It is a stronger
    rule than the ground-truth reachability test above and it is the one a reader is
    promised: a scorer that reaches into the harness can read the frozen graph, the null and
    the patch pool, none of which a method is entitled to see before it is scored.

    **Reworded 2026-09-02.** It used to name `network/`, `classical/` and `quantum/`. Those
    packages were removed from `main` with the method layer, and a rule that names a package
    which does not exist reads as satisfied when it is merely empty. The rule now names the
    prediction path itself, which `test_the_prediction_path_is_the_set_this_contract_names`
    pins. `allo.structure.graph` is inside it and is the graph builder the required
    baselines run on, so the rule still binds real code.
    """
    offenders = []
    for module, deps in graph.items():
        if not is_prediction_path(module):
            continue
        for dep in sorted(deps):
            if dep == "allo.scoring" or dep.startswith("allo.scoring."):
                offenders.append(f"{module} -> {dep}")
    assert not offenders, "prediction code imports the evaluation layer:\n" + "\n".join(offenders)


def test_the_prediction_path_is_the_set_this_contract_names():
    """Adding a module to the prediction path must be a decision, not a side effect.

    The two rules above filter on `is_prediction_path` and assert over what survives. That
    is safe while the set is what the contract describes and silently weaker when it is not:
    on 2026-09-02 the method layer was removed from `main`, and the packages those rules
    named — `network/`, `classical/`, `quantum/` — stopped existing. Both rules kept
    passing. They pass over `structure/` now, which is real code, but nothing checked that.

    Pinning the set makes the next change visible. Restoring a prediction package, or moving
    one into `MAY_IMPORT_GROUND_TRUTH`, fails here first and has to be argued for.
    """
    declared = {
        "allo",
        "allo.experiment",
        "allo.inputs",
        "allo.structure",
        "allo.structure.graph",
        "allo.structure.pdb",
        "allo.structure.properties",
    }
    found = {module_name(p) for p in SRC_ROOT.rglob("*.py") if is_prediction_path(module_name(p))}
    assert found == declared, (
        "the prediction path changed. Update this list and say why in `AGENTS.md`:\n"
        f"  added:   {sorted(found - declared)}\n"
        f"  removed: {sorted(declared - found)}"
    )


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

    **What this still cannot catch, stated plainly.** A path assembled from `os.environ`, from
    a config file, or from a parent directory walked at runtime. A component computed by
    arithmetic rather than written down: code points in a list are harvested, and
    `chr(100 + 0)` is not. Anything read through a subprocess whose command is itself
    computed. A static check over Python source is a syntax denylist, and a syntax denylist
    cannot enforce an information-flow boundary against a Turing-complete language -- an
    adversarial pass demonstrated a working read on 2026-09-03 and would demonstrate another
    against any fixed rule set.

    So the guarantee is "no route is spelled here", not "no route can exist", and it is worth
    exactly what that says: it catches the accident, the copied idiom and the shortcut taken
    under time pressure, which is what has actually happened all four times. It does not catch
    a deliberate exfiltration and does not claim to. What would is an environment in which the
    answer keys are unreadable to prediction code, and that is infrastructure this repository
    does not have. The cache partition and the redacted `load()` are the independent layers,
    not belt to this brace.
    """
    dynamic = []
    capability_importers = []
    protected_path_names = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
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
                hits -= MANIFEST_READS
            hits = {hit for hit in hits if not allowed_experiment_path(hit, path)}
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

    # A composed attribute name is the `getattr` analogue of the composed import and the
    # composed path, both already closed. `_positives` is a FROZEN_TOKEN and returns the
    # whole label set, so `getattr(harness, "_" + "positives")` reaches the answer key with
    # no forbidden token in the text. A runner has to import `allo.scoring` -- it is the
    # scoring path -- so the import cannot be banned and the ingredient is removed instead.
    # Found 2026-09-02 by an adversarial pass; the route it demonstrated used `importlib`
    # and was already caught by the assertion above, this variant was not.
    composed = []
    for path in [*sorted(SRC_ROOT.rglob("*.py")), *outside_runner_files()]:
        if path.suffix != ".py":
            continue
        for node in ast.walk(ast.parse(path.read_text(errors="ignore"))):
            if (
                isinstance(node, ast.Call)
                and _dotted_name(node.func) in {"getattr", "setattr", "hasattr"}
                and len(node.args) >= 2
                and not (
                    isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str)
                )
            ):
                composed.append(f"{path.relative_to(ROOT)}:{node.lineno}")
    assert not composed, (
        "attribute name built at runtime defeats the token guard; found in " + "; ".join(composed)
    )

    def _composed(source: str) -> list[int]:
        return [
            node.lineno
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Call)
            and _dotted_name(node.func) in {"getattr", "setattr", "hasattr"}
            and len(node.args) >= 2
            and not (isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str))
        ]

    # A guard that cannot fail is not a guard.
    assert _composed('from allo.scoring import harness\ngetattr(harness, "_" + "positives")\n')
    assert _composed("import x\nname = 'a'\ngetattr(x, name)\n")
    assert not _composed('import x\ngetattr(x, "plain", None)\n')


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
            "from pathlib import Path\n"
            "p = Path('docs') / 'benchmark' / 'primary' / ('frozen' + '.json')\n"
        ),
        # The `/` operator was modelled and its method spelling was not. This probe is the
        # one that mattered: `data/patches` is protected but is not a frozen token, so the
        # matched-patch cache -- every arm's positive count, the sealed tier included -- was
        # readable from `allo.network` with all 34 tests green. Found 2026-09-02.
        "joinpath_cache.py": (
            "from pathlib import Path\nd = Path('data')\np = d.joinpath('patches')\n"
        ),
        "joinpath_frozen.py": (
            "from pathlib import Path\n"
            "d = Path('docs') / 'benchmark'\n"
            "p = d.joinpath('evaluation').joinpath('frozen.json')\n"
        ),
        # A prefix built with `os.path.dirname` evaluated to None, which deleted every path
        # concatenated onto it from the scan.
        "dirname_prefix.py": (
            "import os\nb = os.path.dirname('data/patches/x.npz')\nopen(b + '/y.npz').read()\n"
        ),
        # Fourth instance of the same failure mode, found 2026-09-03. The `/` operator was
        # modelled with a `str` or `int` on the right, and `Path("data") / Path("patches")`
        # resolves at runtime with a `Path` there. Neither operand is protected on its own,
        # so the composed path evaluated to None and left no violation and no frozen token.
        # Every composition branch now shares one operand rule, `_PATH_PART`.
        "path_div_path.py": ("from pathlib import Path\np = Path('data') / Path('patches')\n"),
        "joinpath_path.py": (
            "from pathlib import Path\np = Path('data').joinpath(Path('patches'))\n"
        ),
        "purepath_div.py": ("from pathlib import PurePath\np = PurePath('data') / 'patches'\n"),
        "path_of_purepath.py": (
            "from pathlib import Path, PurePath\np = Path(PurePath('data'), 'patches')\n"
        ),
        "osjoin_of_paths.py": (
            "import os\nfrom pathlib import Path\np = os.path.join(Path('data'), Path('patches'))\n"
        ),
    }
    for name, source in probes.items():
        assert protected_path_violations(source, tmp_path / name), f"detector missed {name}"


def test_the_segment_cover_backstop_catches_assembled_paths(tmp_path):
    """Twenty-one spellings that build a protected path without ever writing one.

    The resolver above models path expressions, and an adversarial pass on 2026-09-03
    listed twenty-six spellings it does not model. Three of them ran together in one tracked
    probe runner and read the matched-patch cache, the per-target input audits and the sealed
    tier's positive counts with all thirty-seven tests green. A whitelist of spellings loses
    this race, so `segment_cover_violations` asks the other question: does this file hold
    every component of a protected path. It needs no evaluation, so no new spelling defeats
    it -- the interpreter must still get the characters from somewhere.

    The two `process` entries are the sharpest of the twenty-six. The resolver catches
    `subprocess.run(["cat", "docs/..."])` because the path is its own argument, and a one-word
    prefix glued to the front defeated it. The `bytes` entry was invisible at two places at
    once: `evaluate` and the fallback scan both test `isinstance(value, str)`, while `open`,
    `os.open` and `os.stat` all accept a `bytes` path.
    """
    probes = {
        # pathlib bases and chains the resolver does not walk
        "cwd_div.py": "from pathlib import Path\np = Path.cwd() / 'data' / 'patches'\n",
        "cwd_joinpath.py": (
            "from pathlib import Path\np = Path.cwd().joinpath('data').joinpath('patches')\n"
        ),
        "file_absolute.py": (
            "from pathlib import Path\np = Path(__file__).absolute().parent / 'data' / 'patches'\n"
        ),
        "home_div.py": "from pathlib import Path\np = Path.home() / 'data' / 'patches'\n",
        "starred_parts.py": (
            "from pathlib import Path\nparts = ('data', 'patches')\np = Path(*parts)\n"
        ),
        "with_name.py": (
            "from pathlib import Path\np = Path('data').joinpath('x').with_name('patches')\n"
        ),
        # string assembly, where no component carries a separator
        "format.py": "p = '{}/{}'.format('data', 'patches')\n",
        "percent.py": "p = '%s/%s' % ('data', 'patches')\n",
        "str_join.py": "p = '/'.join(['data', 'patches', 'x.npz'])\n",
        "os_sep_join.py": "import os\np = os.sep.join(['data', 'patches'])\n",
        "chr_separator.py": "p = 'data' + chr(47) + 'patches'\n",
        "bytes_literal.py": "f = open(b'data/patches/x.npz')\n",
        "fstring_dynamic.py": "n = 'patches'\np = f'data/{n}'\n",
        # bindings the resolver does not track
        "tuple_assign.py": (
            "from pathlib import Path\na, b = 'data', 'patches'\np = Path(a) / b\n"
        ),
        "walrus.py": "from pathlib import Path\np = (d := Path('data')) / 'patches'\n",
        "aug_assign.py": "from pathlib import Path\np = Path('data')\np /= 'patches'\n",
        "for_loop.py": (
            "from pathlib import Path\np = Path('.')\n"
            "for s in ['data', 'patches']:\n    p = p / s\n"
        ),
        "dict_lookup.py": (
            "from pathlib import Path\nD = {'a': 'data', 'b': 'patches'}\n"
            "p = Path(D['a']) / D['b']\n"
        ),
        # a shell, where the path never becomes a Python path at all
        "os_system.py": ("import os\nos.system('cat docs/benchmark/primary/audit/kras-g12c.md')\n"),
        "subprocess_shell.py": (
            "import subprocess\n"
            "subprocess.run('cat docs/benchmark/primary/audit/x.md', shell=True)\n"
        ),
        # Code points, which leave no string and no bytes literal at all. Demonstrated
        # working against both defences by an adversarial pass on 2026-09-03.
        "code_points.py": (
            "from pathlib import Path\n"
            "parts = [[100, 97, 116, 97], [112, 97, 116, 99, 104, 101, 115]]\n"
            "p = Path(*(bytes(x).decode() for x in parts))\n"
        ),
        "chdir_then_open.py": (
            "import os\nos.chdir('docs')\nopen('benchmark/primary/audit/kras-g12c.md')\n"
        ),
    }
    missed = [
        name for name, src in probes.items() if not protected_path_violations(src, tmp_path / name)
    ]
    assert not missed, f"segment cover missed {missed}"

    # A guard that fires on everything is not a guard. Prose is where the false positive
    # would come from, so a docstring contributes no component and neither does a phrase.
    clean = (
        '"""Score residues against the data in the raw patches under docs/benchmark."""\n'
        "import numpy as np\n\n\n"
        "def score(graph):\n"
        '    """Return one array in the graph\'s own residue order."""\n'
        "    label = 'data patches are not a path here'\n"
        "    return np.zeros(len(graph.residues)), label\n"
    )
    assert not segment_cover_violations(clean), "prose must not read as a path"


def test_a_rename_leaves_no_second_unprotected_name(tmp_path):
    """`git show <sha>:<old path>` returns the same bytes under a name no entry covers.

    Five tracked files were renamed into a protected tree, and three of them are the
    per-target input audits: `docs/benchmark/audit/kras-g12c.md` became
    `docs/benchmark/primary/audit/kras-g12c.md` on 2026-08-31 and still reproduces the whole
    KRAS contact shell at its former name, from `main`, with no network. The other two carry
    a `FROZEN_TOKEN` in the file name and were backstopped by the token scan, which is the
    same asymmetry that left `data/patches` readable in September.

    **A delete leaves the same artefact as a rename, and the first version read only renames.**
    Three more files sat in that same directory as `.json` before the Markdown conversion.
    Git recorded a delete plus an add, not a rename, because the bytes changed too much, so
    `--diff-filter=R` never saw them and the ledger stood stale while every test passed --
    found 2026-09-03 by a second adversarial pass. The filter is now `RD`, and a directory
    that lost any file to a protected tree is treated as a former protected tree itself, so
    the conversion is covered by a rule rather than by three names.

    The list is derived from git rather than typed, so a rename or a deletion made next week
    is protected the day it is made.
    """
    assert FORMER_PROTECTED_PATHS, "the former-path ledger is empty"
    # The ledger is the source, because a shallow clone and a `git archive` export have no
    # rename history and a guard must not be weaker there. Git cross-checks it when it can.
    derived = renamed_into_protected_from_git()
    if derived is not None:
        missing = {p.relative_to(ROOT).as_posix() for p in derived - FORMER_PROTECTED_PATHS}
        assert not missing, f"rename history holds paths the ledger does not: {sorted(missing)}"
    audits = {p for p in FORMER_PROTECTED_PATHS if p.parent.name == "audit"}
    # Six: three Markdown audits renamed into `primary/audit/`, and the three `.json` they
    # were converted from. Both spellings still resolve through `git show`.
    assert len(audits) == 6, f"expected the six former input audits, got {sorted(audits)}"
    assert {p.suffix for p in audits} == {".md", ".json"}, sorted(audits)
    for former in sorted(audits):
        relative = former.relative_to(ROOT)
        assert protected_path_violations(f"open({str(relative)!r})\n", tmp_path / "p.py")
        revision = f"import subprocess\nsubprocess.run(['git', 'show', 'HEAD~9:{relative}'])\n"
        assert protected_path_violations(revision, tmp_path / "p.py"), (
            f"a revision prefix hides {relative}"
        )


def test_the_decision_record_is_guarded_like_the_dossier(tmp_path):
    """ADR 0031 argues the myosin substitution from the `9GZ2` contact shell, so it prints it.

    `docs/adr/0031-cardiac-myosin-holo-substitution.md:22` names 12 of 12 `label_residues`
    for both myosin arms -- the same set `docs/targets.md` was protected for one day earlier,
    in the same three-letter spelling that made the first sweep miss it.
    """
    adr = (ROOT / "docs" / "adr").resolve()
    assert adr in PROTECTED_PATHS
    source = "from pathlib import Path\np = Path('docs') / 'adr' / '0031-x.md'\n"
    assert protected_path_violations(source, tmp_path / "p.py")


def test_the_runner_scan_reaches_the_two_files_that_run_on_every_push():
    """`.github/workflows/ci.yml` and `pyproject.toml` had no suffix here and no exempt tree.

    Both execute: one runs commands on every push, the other declares the console scripts.
    Neither was scanned by the runner guard nor by the package import-graph tests, so a step
    that imported `allo.benchmark` -- which re-exports the unredacted manifest and the label
    sets -- would have been invisible to all thirty-eight tests.

    The frozen manifests come with the widening and must NOT be scanned: a file that IS the
    evaluation side answers a different question, and `PROTECTED_PATHS` is what guards it.
    """
    scanned = set(outside_runner_files())
    for name in (".github/workflows/ci.yml", "pyproject.toml"):
        path = ROOT / name
        if path.exists():
            assert path in scanned, f"{name} is executable configuration and is scanned by nothing"
    for name in ("primary", "secondary", "evaluation"):
        manifest = ROOT / "docs" / "benchmark" / name / "manifest.yaml"
        if manifest.exists():
            assert manifest not in scanned, f"{name} manifest is frozen data, not a runner"
            assert frozen_data(manifest)


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
        p.relative_to(SRC_ROOT)
        for p in sorted(SRC_ROOT.rglob("*.py"))
        if is_prediction_path(module_name(p))
        and ("frozen.json" in (text := p.read_text()) or "FROZEN" in text)
    ]
    assert not offenders, f"prediction-path modules referencing the frozen labels: {offenders}"


def test_prediction_path_never_names_the_answer_key_ledgers():
    """The gap the two literal-token guards above left open, found by an audit 2026-08-24.

    `frozen.json`/`FROZEN` and `manifest.yaml`/`MANIFEST` each get a literal-string scan over
    the prediction path. `selection.json` did not, so a prediction module doing
    `open(base / "selection.json")` with a constructed base tripped nothing: the path analysis
    cannot resolve a dynamic path, and no token guard covered the name. The same hole applied
    to `extension-candidates.md` the moment it was added. Both are answer keys -- they carry
    holo accessions, effector component IDs and real label residues in prose -- so they get
    the same belt as the other two routes.
    """
    tokens = ("selection.json", "extension-candidates")
    offenders = [
        f"{p.relative_to(SRC_ROOT)} -> {token}"
        for p in sorted(SRC_ROOT.rglob("*.py"))
        if is_prediction_path(module_name(p))
        for token in tokens
        if token in p.read_text()
    ]
    assert not offenders, f"prediction-path modules naming an answer-key ledger: {offenders}"


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
    from allo.inputs import APO_CACHE, APO_STRUCTURES, BENCHMARK_MANIFESTS

    # Computed PER MANIFEST and then unioned, not over the pooled targets. An accession
    # that is holo in one set and apo in the other would otherwise cancel out of
    # `forbidden` and disarm the check for both -- the same-set case is legitimate
    # (`1OPL` is apo for one primary arm), the cross-set case is not.
    holo, forbidden = set(), set()
    for path in BENCHMARK_MANIFESTS:
        if not path.exists():
            continue
        specs = yaml.safe_load(path.read_text())["targets"]
        set_apo = {s["apo"]["pdb"].upper() for s in specs}
        set_holo = {(s.get("holo") or {}).get("pdb", "").upper() for s in specs} - {""}
        holo |= set_holo
        forbidden |= set_holo - set_apo
    assert holo, "manifest declares no holo entries; this test would pass vacuously"
    assert EVAL_CACHE != APO_CACHE, "evaluation and prediction must not share a cache root"

    # Only entries that are holo and *never* apo within their own set are unambiguous
    # evidence of a breach.
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
    from allo.inputs import _PREDICTION_SCHEMA, BENCHMARK_MANIFESTS, load

    assert "site" not in _PREDICTION_SCHEMA["targets"][0], (
        "site display strings name effectors and must remain outside the prediction schema"
    )

    forbidden = {"site", "holo", "defect", "note", "blind", "allosteric_evidence", "state"}
    # Allow-list, not deny-list: a field added to the manifest tomorrow must be redacted by
    # default. If this fires, decide whether the new field is apo-side and add it explicitly.
    known_apo_side = {"id", "protein", "apo", "active_site"}
    for path in BENCHMARK_MANIFESTS:
        # A set that has not been frozen yet has no manifest, and a clone may hold only one.
        if not path.exists():
            continue
        redacted, full = load(path), read_manifest(path)
        for target in redacted["targets"]:
            leaked = forbidden & set(target)
            assert not leaked, (
                f"{path.name}/{target['id']}: prediction path can see {sorted(leaked)}"
            )
            assert set(target) <= known_apo_side, (
                f"{path.name}/{target['id']}: unreviewed field(s) "
                f"{sorted(set(target) - known_apo_side)} reaching prediction code -- it is "
                "absent from allo.inputs._PREDICTION_SCHEMA"
            )
        # And the redaction has to be doing real work, or it is decoration.
        assert any(forbidden & set(target) for target in full["targets"]), (
            f"{path.name} carries no redactable field; this test would pass vacuously"
        )


def test_evaluation_status_cannot_delete_prediction_inputs(tmp_path):
    """A defective holo arm is not an apo-admission decision (ADR 0016, ADR 0031).

    `status` and `prediction_status` are evaluation-side judgements about the ground truth.
    They must not change what a method receives, because a method that sees fewer inputs when
    an arm is judged defective has been told something about the answer key.

    The two fields are not interchangeable, and that is the point. `prediction_status` is an
    input-side decision and it **may** block an arm: `allo.inputs.load` filters on it.
    `status` is an evaluation-side judgement about the ground truth and it **may not**.

    ADR 0031 removed `prediction_status: blocked` from `cardiac_myosin_mandated` when the
    organisers sanctioned `9GZ2`, so no arm carries the field today and pinning one arm's value
    would now pin nothing. This pins the rule instead, in both directions.
    """
    import yaml

    from allo.groundtruth.manifest import read_manifest
    from allo.inputs import load

    manifest = read_manifest()
    baseline = {target["id"] for target in load()["targets"]}
    assert baseline, "the manifest admits no prediction input; this test would pass vacuously"
    for target in manifest["targets"]:
        target["status"] = "excluded" if target.get("status") != "excluded" else "corrected"
    probe = tmp_path / "manifest.yaml"
    probe.write_text(yaml.safe_dump(manifest))
    assert {target["id"] for target in load(probe)["targets"]} == baseline, (
        "an evaluation-side `status` changed the set of prediction inputs"
    )
    assert not any(
        {"status", "prediction_status"} & set(target) for target in load(probe)["targets"]
    ), "a status judgement reached the prediction path as a field"

    # The other direction: `prediction_status` is input-side and must still be able to block.
    blocked = yaml.safe_load(probe.read_text())
    blocked["targets"][0]["prediction_status"] = "blocked"
    probe.write_text(yaml.safe_dump(blocked))
    assert {target["id"] for target in load(probe)["targets"]} == baseline - {
        blocked["targets"][0]["id"]
    }, "`prediction_status: blocked` no longer removes an arm from the prediction path"


def test_only_the_boundary_module_reads_the_manifest():
    """`allo.inputs` is the one prediction-path module allowed to open the manifest.

    It has to — it needs the chain and the active-site rule. Everything else on the
    prediction path must take the redacted result from it rather than re-reading the file
    and getting the unredacted one.
    """
    offenders = [
        p.relative_to(SRC_ROOT)
        for p in sorted(SRC_ROOT.rglob("*.py"))
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
# `.yml` and `.toml` joined on 2026-09-03. `.github/workflows/ci.yml` runs commands on every
# push and `pyproject.toml` declares the console scripts, and neither had a suffix here nor a
# first path part in `NON_RUNNER_TREES`, so both were scanned by nothing at all. `.yaml` comes
# with them rather than after them, because the difference between `ci.yml` and `ci.yaml` is
# a spelling and this guard has lost to a spelling four times.
RUNNER_SUFFIXES = {".py", ".sh", ".ipynb", ".yml", ".yaml", ".toml"}
FROZEN_TOKENS = (
    "frozen.json",
    "FROZEN",
    "manifest.yaml",
    "MANIFEST",
    "selection.json",
    "extension-candidates",
    # `allo.scoring` is not forbidden to a runner -- it takes scores in and gives numbers
    # out. That property is false at the submodule level: `harness._positives` reads
    # `frozen.json` and returns the label list, by a route with no `groundtruth`, no
    # `frozen.json` and no `FROZEN` in its text. A leading underscore is a convention, not
    # an access control. Found by the 2026-08-25 evaluation-layer audit.
    "_positives",
    "PATCH_CACHE",
    "groundtruth",
)
NON_RUNNER_TREES = {
    "src",  # package import-graph tests cover it
    "tests",  # the guards necessarily name forbidden routes
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
    return sorted(
        path for path in candidates if path.is_file() and is_runner(path) and not frozen_data(path)
    )


def frozen_data(path: Path) -> bool:
    """A config file inside a protected tree is the answer key, not a runner.

    Widening `RUNNER_SUFFIXES` to `.yml`, `.yaml` and `.toml` pulled the three frozen
    manifests into the runner scan, where each one names itself and fails. The scan asks
    whether a file reaches the evaluation side; a file that IS the evaluation side answers a
    different question, and `PROTECTED_PATHS` is what guards it. A `.py` or `.sh` inside such
    a tree still scans, because the review directory's own tools are executable and the rule
    that exempts them is stated separately.
    """
    resolved = path.resolve()
    return resolved.suffix in {".yml", ".yaml", ".toml"} and any(
        guarded in resolved.parents for guarded in PROTECTED_PATHS
    )


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


def is_review_tool(path: Path) -> bool:
    """A tracked file inside the review tree that imports no `allo` module (ADR 0034).

    Exempts such a file from the protected-path check **for paths inside that tree only**.
    Every other protected path stays live for it, as do the import and frozen-token
    checks, so the carve-out is "a review tool may name its own output" and nothing wider.
    """
    if REVIEW_TOOLS not in path.resolve().parents:
        return False
    if path.suffix != ".py":
        return False
    return not any(
        name == "allo" or name.startswith("allo.")
        for name in imports_from_source(path.read_text(errors="ignore"), "")
    )


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
    own_tree = REVIEW_TOOLS if is_review_tool(path) else None
    violations.update(
        f"evaluation path {hit}"
        for source in sources
        for hit in protected_path_violations(source, path)
        if (own_tree is None or (hit != own_tree and own_tree not in hit.parents))
        and not allowed_experiment_path(hit, path)
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


def test_every_review_tool_imports_no_package_module():
    """The condition ADR 0034's exemption rests on, as a test rather than an observation.

    A review-side tool is exempt from the protected-path check for paths inside the review
    tree. That is safe only while it cannot be a prediction runner, and what makes it
    unable to be one is that it imports nothing from `allo`. A future tool that reaches for
    the package fails here, with this message, rather than failing the main gate for naming
    its own output.
    """
    offenders = [
        str(path.relative_to(ROOT))
        for path in outside_runner_files()
        if REVIEW_TOOLS in path.resolve().parents and path.suffix == ".py"
        if not is_review_tool(path)
    ]
    assert not offenders, "review tools must import no `allo` module (ADR 0034):\n" + "\n".join(
        offenders
    )


def test_the_review_exemption_stops_at_the_review_tree(tmp_path):
    """A review tool may name its own output. It may not name any other protected path."""
    tool = ROOT / "docs" / "benchmark" / "review" / "data" / "fetch_structure_evidence.py"
    if not tool.exists():
        pytest.skip("review tooling not present")
    assert is_review_tool(tool)
    assert not runner_violations(tool), "a review tool naming only its own tree is clean"

    smuggler = tmp_path / "probe.py"
    smuggler.write_text(
        "from pathlib import Path\n"
        f"OUT = Path({str(ROOT / 'docs' / 'benchmark' / 'review' / 'data')!r})\n"
        f"ANSWERS = Path({str(ROOT / 'docs' / 'benchmark' / 'evaluation')!r})\n"
    )
    source = smuggler.read_text()
    hits = protected_path_violations(source, tool)
    outside = {hit for hit in hits if REVIEW_TOOLS not in hit.parents}
    assert outside, "the evaluation directory must still register as protected"


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
        # A scratch script run from the repository root imports through the source
        # directory, and the detector read that as a third-party package until 2026-09-02.
        "from src.allo.groundtruth.labels import pocket_residues",
        "import src.allo.groundtruth",
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


# ---------------------------------------------------------------------------------------
# The evaluation layer, added 2026-08-25.
#
# `allo.scoring` is allow-listed to import `allo.groundtruth`, and unlike `allo.benchmark`
# it is NOT forbidden to run scripts -- an experiment has to be able to score a method
# (`docs/playbooks/experiment.md`). What makes that safe is a property of its API rather
# than of the import graph: it takes scores in and gives numbers out, and never hands back
# the label set. These two tests are that property.
# ---------------------------------------------------------------------------------------


def test_scoring_public_api_never_returns_a_label_set():
    from allo import scoring

    # A whitelist, not a spot check. A new public name must be justified against this test
    # before it is exported, because the package reads the answer key.
    #
    # `confirmatory_verdict` was added 2026-09-02 and takes only p-values and the frozen
    # manifest -- no residue, no score vector, no label set -- and returns Holm thresholds
    # and booleans. It is exported because the alternative is every caller re-implementing
    # the frozen decision rule, which had already happened once with the wrong family.
    assert set(scoring.__all__) == {
        "compare_methods",
        "confirmatory_verdict",
        "holm",
        "protocol",
        "score_arm",
    }
    for name in scoring.__all__:
        assert not name.startswith("_")
    # The one function that reads the answer key is private and stays private.
    from allo.scoring import harness as harness_module

    assert not hasattr(scoring, "_positives")
    assert harness_module._positives.__name__.startswith("_")


def test_a_scored_record_names_no_label_residue():
    """The record a method gets back must not contain the answer, even as a by-product."""
    import copy

    import numpy as np

    from allo.inputs import apo_input
    from allo.scoring import harness as harness_module
    from allo.scoring.nulls import evaluation_graph

    target = "kras_g12c_mandated"
    labels = set(
        json.loads(harness_module.INPUT_FROZEN.read_text())["targets"][target][
            "scoreable_label_residues"
        ]
    )
    graph = evaluation_graph(apo_input(target))
    settings = copy.deepcopy(harness_module.protocol())
    settings["nulls"]["replicates"] = 49
    settings["nulls"]["matched_patch_distance"]["replicates"] = 49
    rng = np.random.default_rng(0)
    scores = {r: float(rng.random()) for r in graph.order}
    record = harness_module.score_arm(target, scores, method="random", config=settings)

    def integers(value):
        if isinstance(value, bool):
            return set()
        if isinstance(value, int):
            return {value}
        if isinstance(value, dict):
            return set().union(*(integers(v) for v in value.values()), set())
        if isinstance(value, list | tuple):
            return set().union(*(integers(v) for v in value), set())
        return set()

    # Every label happens to be a plausible small integer, so require that the record does
    # not reproduce the label SET -- a single collision with a count is not a leak.
    assert not labels <= integers(record)

    # `compare_methods` is the second public entry point and it reads the same answer key.
    other = {r: float(rng.random()) for r in graph.order}
    paired = harness_module.compare_methods(target, scores, other, config=settings)
    assert not labels <= integers(paired)


def test_no_file_may_name_a_record_it_did_not_write():
    """The tenth data route, added 2026-09-02.

    A scoring run persists the matched-patch sampler diagnostics beside itself, and
    `observed_radius_of_gyration` is the true site's own geometry. `data/patches` was
    protected for that content in August; the copy in `experiments/` was not. The tree
    cannot be protected outright, because the runners write into it, so the rule is
    narrower: a run script may name the two records beside it and no others.
    """
    mine = EXPERIMENTS / "2026-01-01-mine" / "run.py"
    ours = EXPERIMENTS / "2026-01-01-mine" / "metrics.json"
    theirs = EXPERIMENTS / "2026-01-01-theirs" / "metrics.json"
    config = EXPERIMENTS / "2026-01-01-theirs" / "config.yaml"

    assert allowed_experiment_path(ours, mine), "a runner must be able to write its own record"
    assert allowed_experiment_path(config, mine), "a config carries no holo-derived value"
    assert allowed_experiment_path(EXPERIMENTS, mine), "the scaffold names the tree"
    assert not allowed_experiment_path(theirs, mine), "a foreign record is the leak"
    assert not allowed_experiment_path(theirs, SRC / "network" / "contacts.py"), (
        "a prediction module owns no run directory, so every record is foreign to it"
    )


def test_the_three_new_answer_keys_are_protected():
    """Routes eight to ten name real label sets, and a sweep found them, not a hunch.

    `kras-g12c.md` reproduces 21 of 21 label residues for both KRAS arms and `bcr-abl1.md`
    18 of 18; `allosteric-prediction-prior-art.md` prints the KRAS distal label set as
    running prose. The assertion is on the file, not on the tree, so moving one out of a
    protected directory fails here rather than silently.
    """
    keys = [
        ROOT / "docs" / "benchmark" / "primary" / "audit" / "kras-g12c.md",
        ROOT / "docs" / "benchmark" / "primary" / "audit" / "bcr-abl1.md",
        ROOT / "docs" / "benchmark" / "evidence" / "allosteric-prediction-prior-art.md",
    ]
    for key in keys:
        assert key.exists(), f"{key.relative_to(ROOT)} moved; re-run the label sweep"
        assert any(root == key or root in key.parents for root in PROTECTED_PATHS), (
            f"{key.relative_to(ROOT)} names a full label set and is unprotected"
        )


def test_the_answer_keys_the_numeric_sweep_could_not_see_are_protected(tmp_path):
    """Routes eleven to thirteen, and the reason the sweep that cleared them was wrong.

    `docs/targets.md` prints the cardiac myosin site in three-letter codes, so a sweep
    matching bare integers on a word boundary scored it zero and
    a true finding was written down as refuted. Re-run with the codes normalised it is 12 of
    12 for both myosin arms. The two benchmark READMEs tabulate a `Scoreable` column that is
    the positive count, beside the holo entry and the effector, for the five sealed
    `generalisation` arms among others.

    The first loop pins the files. The second pins that the guard actually fires on a
    prediction module naming one, because protecting a path the detector cannot resolve
    protects nothing -- that was the `.joinpath` hole found the same day.
    """
    keys = [
        ROOT / "docs" / "targets.md",
        ROOT / "docs" / "benchmark" / "primary" / "README.md",
        ROOT / "docs" / "benchmark" / "secondary" / "README.md",
    ]
    for key in keys:
        assert key.exists(), f"{key.relative_to(ROOT)} moved; re-run the label sweep"
        assert any(root == key or root in key.parents for root in PROTECTED_PATHS), (
            f"{key.relative_to(ROOT)} reproduces a label set or a positive count, unprotected"
        )

    for key in keys:
        rel = key.relative_to(ROOT).as_posix()
        source = f"from pathlib import Path\np = Path({rel.split('/')[0]!r})\n"
        for part in rel.split("/")[1:]:
            source += f"p = p.joinpath({part!r})\n"
        assert protected_path_violations(source, tmp_path / "probe.py"), (
            f"the guard cannot resolve a joinpath route to {rel}"
        )


def test_the_boundary_module_is_exempt_for_the_manifests_and_nothing_else():
    """Widening the input trees must not hand `allo.inputs` the whole tree.

    It has to spell both manifests. It has no reason to spell `primary/README.md`, which
    publishes the positive count, so the exemption is four paths rather than two directories.
    """
    inputs = SRC / "inputs.py"
    assert not (
        protected_path_violations(inputs.read_text(), inputs)
        - MANIFEST_READS
        - {(ROOT / "data" / "raw").resolve()}
    ), "allo.inputs names a protected path outside its exemption"

    readme = "from pathlib import Path\np = Path('docs') / 'benchmark' / 'primary' / 'README.md'\n"
    assert protected_path_violations(readme, inputs) - MANIFEST_READS, (
        "the exemption must not cover the README that publishes the positive count"
    )


# Three-letter codes, so a sweep for `164` also sees `Tyr164`. The 2026-09-02 sweep matched
# bare integers on a word boundary and recorded a true finding as refuted for want of this.
THREE_LETTER = [
    # fmt: off
    "ALA",
    "ARG",
    "ASN",
    "ASP",
    "CYS",
    "GLN",
    "GLU",
    "GLY",
    "HIS",
    "ILE",
    "LEU",
    "LYS",
    "MET",
    "PHE",
    "PRO",
    "SER",
    "THR",
    "TRP",
    "TYR",
    "VAL",
    "MSE",
    # fmt: on
]


def tracked_files() -> set[str]:
    """Every path in the index, as a repo-relative POSIX string."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True, check=True
    ).stdout
    return {name.decode() for name in out.split(b"\0") if name}


def label_numbers_in(text: str) -> list[tuple[int, int]]:
    """Every residue number in `text`, with its offset, three-letter prefixes normalised."""
    pattern = "|".join(THREE_LETTER)
    found = []
    for match in re.finditer(rf"(?i)\b(?:(?:{pattern})[- ]?)?(\d{{1,5}})\b", text):
        found.append((match.start(), int(match.group(1))))
    return found


def test_no_unprotected_tracked_file_reproduces_a_label_set():
    """C1 says "not even the residue count"; a residue LIST is the count and the answer.

    The sweep that found `docs/targets.md` on 2026-09-02 ran once, by hand, and the note that
    recorded what it found quoted the residues it found -- in `AGENTS.md` and in this file,
    neither of which is protected and neither of which is scanned. **The comment explaining
    the route was the route**, and it stood for a day before an adversarial pass found it.

    So the sweep is a test now. Describe an answer key by its shape and its location, never by
    its contents, and this fails if anyone forgets.

    The window is 400 characters. Residue numbers scattered over a whole document are a
    coincidence; a run of them inside one paragraph is a list. Measured: at 400 characters the
    unwindowed version of this sweep produced 14 false positives and this one produces none.
    """
    from allo.scoring.harness import _arms_from_the_input_layer, _positives

    window = 400
    indexed = tracked_files()
    labels = {}
    for target in _arms_from_the_input_layer():
        residues, _ = _positives(target)
        if len(residues) >= 8:  # a short set collides with ordinary numbers too easily
            labels[target] = set(residues)

    offenders = []
    for path in sorted(ROOT.rglob("*")):
        if (
            path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt", ".py"}
            or not path.is_file()
        ):
            continue
        resolved = path.resolve()
        if any(resolved == p or p in resolved.parents for p in PROTECTED_PATHS):
            continue
        if path.relative_to(ROOT).as_posix() not in indexed:
            continue
        hits = label_numbers_in(path.read_text(errors="ignore"))
        for target, wanted in labels.items():
            inside = [(off, n) for off, n in hits if n in wanted]
            for i, (start, _) in enumerate(inside):
                near = {n for off, n in inside[i:] if off - start <= window}
                if near == wanted:
                    offenders.append(f"{path.relative_to(ROOT)}: complete {target} label set")
                    break
    assert not offenders, "unprotected tracked files reproducing a label set: " + "; ".join(
        sorted(set(offenders))
    )


def test_no_unprotected_tracked_file_reproduces_a_positive_count():
    """C1 names the count, not only the identities: "not even the residue count".

    Added 2026-09-03. Every label sweep before this one matched residue IDENTITIES, so a
    table of per-arm positive counts passed all of them. Two files in
    `docs/evidence/method-landscape/` held exactly that -- "m (scoreable labels)" per arm --
    and the tree was unprotected. Protecting it closes those two; this closes the class.

    A bare count is a small integer and small integers are everywhere, so the match needs two
    things in one 250-character window: the arm's own identifier, and its exact count in a
    context that reads as a count. The cue list is what makes it precise rather than noisy --
    without it the same sweep returns nine hits and every one is a chain ID or a year.
    """
    from allo.scoring.harness import _arms_from_the_input_layer, _positives

    counts = {arm: len(_positives(arm)[0]) for arm in _arms_from_the_input_layer()}
    assert len(counts) == 15, sorted(counts)

    cue = re.compile(
        r"scoreable|positive count|n_labels|label(?:s)? count|number of labels|positives|m \(",
        re.IGNORECASE,
    )
    offenders: list[str] = []
    for name in tracked_files():
        relative = Path(name)
        if relative.suffix not in {".md", ".py", ".yaml", ".yml", ".json", ".txt"}:
            continue
        absolute = (ROOT / relative).resolve()
        if any(absolute == root or root in absolute.parents for root in PROTECTED_PATHS):
            continue
        if not absolute.is_file():
            continue
        text = absolute.read_text(errors="ignore")
        for arm, count in counts.items():
            for found in re.finditer(re.escape(arm), text):
                window = text[max(0, found.start() - 250) : found.start() + 250]
                if re.search(rf"(?<![\d.]){count}(?![\d.])", window) and cue.search(window):
                    offenders.append(f"{relative}: {arm}")
                    break
    assert not offenders, (
        "an unprotected tracked file names an arm beside its exact positive count, in a "
        f"context that reads as a count: {sorted(offenders)}. C1 forbids the count reaching "
        "the prediction path as plainly as it forbids the residue identities"
    )
