"""Contract guard — the read-only containment claim (C-041, FR-006, SC-002).

A declared regression guard over behavior already delivered (the per-run engine landed in
US1; this file is authored after it, per the migration/regression exception recorded on T023).
The claim — a reading changes nothing under the managed store roots — is decided exactly as
its contract states it:

- **Baseline referent**: a hash manifest captured by THIS test immediately before each
  reading invocation in the same working tree (path, SHA-256 of bytes, size per file).
- **Comparison unit**: every file under the roots derived from
  ``shared/declarations/facts/runtime-store-layout.yaml#/statement`` — read through
  ``declaration_reader`` and projected as ``.specify/<store-name>/`` (the fact carries no
  per-store ``root`` key) — byte-level, plus the root path sets themselves. The test holds no
  second root table.
- **Allowed diff set**: none — the set is empty by construction (the engine carries zero write
  points, pinned statically below).
- **Declared exclusion**: interpreter bytecode caches (``__pycache__/``, ``*.pyc``/``*.pyo``)
  are excluded by name; the exclusion is named here, not left implicit.
- **Complement assertions**: after a per-run reading, every root is byte-identical to the
  baseline and no new file appears. The longitudinal complement (T027) runs the same comparison
  around a window reading over the multi-run fixture.
- **Determinism is a separate claim** (C-023): it is judged by run-A/run-B equality in its own
  leg and is never cited here as containment evidence.

The guard proves its own comparator would go red on a store write, so a green here is a
decided claim, not an empty one.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "prompt-adherence.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "prompt-adherence"

#: The declared exclusion (C-041) — bytecode caches, excluded by name.
CACHE_DIR_NAME = "__pycache__"
CACHE_SUFFIXES = (".pyc", ".pyo")

#: Declared store names the seeded fixture must populate, so the comparison unit is not empty.
SEEDED_STORES = ("session", "exec-quant", "feedback", "evidence")

#: Source-level write points the engine MUST NOT carry (T025's static half).
#: ``rename``/``replace`` are deliberately absent: ``str.replace`` is string manipulation,
#: and a filesystem rename or replace still changes the manifest's path set empirically.
WRITE_METHODS = {
    "write",
    "writelines",
    "write_text",
    "write_bytes",
    "mkdir",
    "makedirs",
    "unlink",
    "rmdir",
    "touch",
    "symlink_to",
    "hardlink_to",
    "chmod",
    "lchmod",
    "truncate",
    "dump",
}
FORBIDDEN_IMPORTS = {
    "tempfile",
    "sqlite3",
    "shelve",
    "dbm",
    "pickle",
    "shutil",
    "fcntl",
    "filelock",
    "mmap",
}


# --------------------------------------------------------------------------- #
# the declared comparison unit (C-041), read through its one owner
# --------------------------------------------------------------------------- #
def _require_engine():
    assert ENGINE.is_file(), (
        "red-first: scripts/python/prompt-adherence.py is absent (built in US1 / T011…T015); "
        "this guard may go green only once the engine exists"
    )
    return ENGINE


def _store_roots():
    """The declared roots, projected from the runtime store layout fact (FR-030/C-041)."""
    assert READER.is_file(), "declaration reader absent: %s" % READER
    spec = importlib.util.spec_from_file_location("pa_readonly_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    body = module.load_fact(str(REPO_ROOT), "runtime-store-layout")["body"]
    stores = (body.get("statement") or {}).get("stores")
    assert isinstance(stores, dict) and stores, (
        "runtime-store-layout carries no store roster; the comparison unit cannot be derived"
    )
    roots = {".specify/" + str(name) for name in stores}
    assert all(root.startswith(".specify/") for root in roots), (
        "a derived root leaves the documented .specify/<store-name>/ projection"
    )
    return roots


def _manifest(workspace, roots):
    """``{"files": {relpath: (sha256, size)}, "roots": {root: exists}}`` — the baseline referent."""
    files = {}
    root_state = {}
    for root in sorted(roots):
        base = Path(workspace) / root
        root_state[root] = base.is_dir()
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(Path(workspace))
            if CACHE_DIR_NAME in rel.parts or path.suffix in CACHE_SUFFIXES:
                continue
            payload = path.read_bytes()
            files[rel.as_posix()] = (hashlib.sha256(payload).hexdigest(), len(payload))
    return {"files": files, "roots": root_state}


def _copy_fixture(tmp_path, name="seeded"):
    workspace = tmp_path / "ws"
    shutil.copytree(FIXTURES / name, workspace)
    return workspace


def _run(workspace, *args):
    engine = _require_engine()
    return subprocess.run(
        [sys.executable, str(engine), "--workspace-root", str(workspace)]
        + [str(arg) for arg in args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _contained_run(workspace, *args):
    """Capture the baseline immediately before the invocation and compare immediately after."""
    roots = _store_roots()
    before = _manifest(workspace, roots)
    proc = _run(workspace, *args)
    after = _manifest(workspace, roots)
    assert after["roots"] == before["roots"], (
        "a managed store root appeared or vanished around the invocation %r: before=%r "
        "after=%r (allowed delta: none, C-041)" % (args, before["roots"], after["roots"])
    )
    paths = sorted(set(before["files"]) | set(after["files"]))
    diffs = [rel for rel in paths if before["files"].get(rel) != after["files"].get(rel)]
    assert not diffs, (
        "the invocation %r changed files under the managed store roots (allowed delta: none; "
        "C-041): %r"
        % (args, [(rel, before["files"].get(rel), after["files"].get(rel)) for rel in diffs])
    )
    return proc


# --------------------------------------------------------------------------- #
# the comparison unit is real: roots and files exist to be compared
# --------------------------------------------------------------------------- #
def test_manifest_baseline_covers_the_populated_fixtures_store_files(tmp_path):
    workspace = _copy_fixture(tmp_path)
    manifest = _manifest(workspace, _store_roots())
    for store in SEEDED_STORES:
        root = ".specify/" + store
        assert manifest["roots"].get(root) is True, (
            "the seeded fixture lacks the store root %r, so the containment claim would have "
            "nothing to compare there" % root
        )
    assert len(manifest["files"]) >= 4, (
        "the baseline manifest carries %d store files; the populated fixture must seed every "
        "catalog row's store" % len(manifest["files"])
    )
    for rel, (digest, size) in manifest["files"].items():
        assert len(digest) == 64 and size > 0, (
            "the manifest entry for %r is not a (path, SHA-256, size) reading" % rel
        )


# --------------------------------------------------------------------------- #
# C-041 — the complement assertions after a per-run reading
# --------------------------------------------------------------------------- #
def test_per_run_reading_leaves_the_store_roots_byte_identical(tmp_path):
    workspace = _copy_fixture(tmp_path)
    for args in ((), ("--json",), ("--run", "r20261126T000000Z-fixture")):
        proc = _contained_run(workspace, *args)
        assert proc.returncode == 0, (
            "the per-run reading %r exited %d before containment could be read; stderr=%r"
            % (args, proc.returncode, proc.stderr)
        )
        assert proc.stdout.strip(), "the per-run reading %r emitted nothing" % (args,)


# --------------------------------------------------------------------------- #
# C-041 — the complement assertions after a longitudinal reading (T027)
# --------------------------------------------------------------------------- #
LONGITUDINAL_ARGS = (
    ("--since", "2026-11-25T00:00:00Z", "--until", "2026-11-26T00:00:00Z"),
    ("--since", "2026-11-24", "--json"),
    ("--until", "2026-11-26T00:00:00Z"),
)


def test_longitudinal_reading_leaves_the_store_roots_byte_identical(tmp_path):
    workspace = tmp_path / "ws"
    shutil.copytree(FIXTURES / "multi-run", workspace)
    manifest = _manifest(workspace, _store_roots())
    assert len(manifest["files"]) >= 8, (
        "the multi-run fixture seeds %d store files; the containment claim needs a populated "
        "comparison unit" % len(manifest["files"])
    )
    for args in LONGITUDINAL_ARGS:
        proc = _contained_run(workspace, *args)
        assert proc.returncode == 0, (
            "the longitudinal reading %r exited %d before containment could be read; stderr=%r"
            % (args, proc.returncode, proc.stderr)
        )
        assert proc.stdout.strip(), "the longitudinal reading %r emitted nothing" % (args,)


# --------------------------------------------------------------------------- #
# T025's static half — the engine source carries zero write points
# --------------------------------------------------------------------------- #
def test_engine_source_has_zero_write_points():
    tree = ast.parse(_require_engine().read_text(encoding="utf-8"))
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".", 1)[0] in FORBIDDEN_IMPORTS:
                    violations.append("imports %s (line %d)" % (alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".", 1)[0] in FORBIDDEN_IMPORTS:
                violations.append("imports from %s (line %d)" % (node.module, node.lineno))
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in WRITE_METHODS:
                violations.append("calls .%s() (line %d)" % (func.attr, node.lineno))
            if isinstance(func, ast.Name) and func.id == "open":
                mode = None
                if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                    mode = node.args[1].value
                for keyword in node.keywords:
                    if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                        mode = keyword.value.value
                if isinstance(mode, str) and any(flag in mode for flag in "wax+"):
                    violations.append("opens for writing mode=%r (line %d)" % (mode, node.lineno))
    assert not violations, (
        "the engine carries write points, so the containment claim is not empty by "
        "construction (FR-006/C-041): %r" % violations
    )


def test_manifest_comparison_would_detect_a_store_write(tmp_path):
    """The guard's own discrimination: a write, a new file and a new root each go red."""
    workspace = _copy_fixture(tmp_path)
    roots = _store_roots()
    baseline = _manifest(workspace, roots)

    mutated = workspace / ".specify" / "feedback" / "20261126T000300Z-fixture-plan.md"
    mutated.write_bytes(mutated.read_bytes() + b"\n")
    (workspace / ".specify" / "session" / "injected-note.md").write_text("x", encoding="utf-8")
    (workspace / ".specify" / "knowledge").mkdir()

    after = _manifest(workspace, roots)
    assert after["files"] != baseline["files"], (
        "the manifest did not notice a byte change or a new file under a store root"
    )
    assert after["roots"] != baseline["roots"], (
        "the manifest did not notice a managed root appearing"
    )
    assert ".specify/session/injected-note.md" in set(after["files"]) - set(baseline["files"]), (
        "the injected file is not the reported difference"
    )


# --------------------------------------------------------------------------- #
# C-029 — the advisory-only boundary: a deviation-bearing reading changes nothing
# --------------------------------------------------------------------------- #
def _tree_manifest(workspace):
    """Every file in the workspace (path, SHA-256, size) — so a new aggregate anywhere, not
    only under a declared store root, is caught; bytecode caches are excluded by name."""
    files = {}
    for path in sorted(Path(workspace).rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(Path(workspace))
        if CACHE_DIR_NAME in rel.parts or path.suffix in CACHE_SUFFIXES:
            continue
        payload = path.read_bytes()
        files[rel.as_posix()] = (hashlib.sha256(payload).hexdigest(), len(payload))
    return files


def test_advisory_reading_of_deviation_bearing_fixtures_changes_nothing(tmp_path):
    workspace = tmp_path / "ws"
    shutil.copytree(FIXTURES / "seeded", workspace)
    before = _tree_manifest(workspace)
    expected_class = {
        (): "classes=evidence-missing",
        ("--json",): '"evidence-missing"',
        ("--run", "r20261126T000030Z-deviant"): "classes=axis-regression,green-unproven",
        ("--run", "gate:fixture-gate:2026-11-26T00:04:00Z"): "state=Exercised",
    }
    for args, marker in expected_class.items():
        proc = _contained_run(workspace, *args)
        assert proc.returncode == 0, (
            "the advisory reading %r exited %d; stderr=%r" % (args, proc.returncode, proc.stderr)
        )
        assert marker in proc.stdout, (
            "the advisory fixture did not surface %r for %r; the negative observation this leg "
            "exists for is absent" % (marker, args)
        )
    after = _tree_manifest(workspace)
    assert after == before, (
        "a deviation-bearing reading changed the workspace tree (no aggregate, no new store "
        "root, no mutation may appear): %r"
        % (sorted(set(before) ^ set(after)),)
    )


# --------------------------------------------------------------------------- #
# C-023 — determinism is a separate claim, judged by run-A/run-B equality
# --------------------------------------------------------------------------- #
def test_determinism_is_judged_separately_by_run_a_run_b_equality(tmp_path):
    workspace = _copy_fixture(tmp_path)
    first = _run(workspace)
    second = _run(workspace)
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout, (
        "two consecutive readings of the same records differ (C-023); determinism is this "
        "leg's claim and is never cited as containment evidence"
    )
    json_first = _run(workspace, "--json")
    json_second = _run(workspace, "--json")
    assert json_first.stdout == json_second.stdout
    json.loads(json_first.stdout)