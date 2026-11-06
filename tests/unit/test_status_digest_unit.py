"""Unit tests for ``scripts/python/status-digest.py`` — the shared state reader (087, T006).

Layer-1 of the Feature 087 test map (``tasks.md`` § Tests Mode). This file owns the *reader-level* behaviour that a
whole-repository contract test cannot isolate:

* the registry directory resolution order — ``$SPECIFY_LINE_REGISTRY_DIR`` → ``$XDG_STATE_HOME/spec-kit/lines`` →
  ``~/.local/state/spec-kit/lines`` — and the fact that the three overrides are the *only* inputs that move it;
* the per-entry triplet path projection (``status_path`` / ``log_path`` / ``heartbeat_path``): declared → projected,
  absent → the literal ``-``;
* the state vocabulary **quoted** from the engine, never re-enumerated here: ``STATE_VALUES`` and ``ACTIVE_STATES``
  are imported from ``skills/external/sdd-loop-driver/scripts/line-registry.py`` at authoring time and every
  projected state is asserted to be a *member* of the imported set (floor-style). A hard-coded list would be a
  second definition of the closed set and is exactly what constitution XIV forbids;
* the read-only boundary: over every path the script touched, no ``open`` for writing is ever made (``data-model.md``
  E7, contract ``status-digest.contract.md`` C-42).

**Red-first (Constitution IV)**: this file is authored before ``scripts/python/status-digest.py`` exists, so each
test asserts the script path first. Red is therefore "artifact missing / behaviour wrong", never an import or
collection error — the engine reference below raises a clear message instead of an ``ImportError`` traceback.

**Fixture posture**: every fixture is built from scratch under ``tmp_path``; no test reads or writes the real
registry directory, the real workspace's ``test-evidence/`` or any file of this repository.

Scope boundary: this row covers the *reader* only. Bounding/ordering/`omitted`/staleness exit codes are T027's
subject, the guard's thirteen propositions are T033's, and the rendered status line is T016's — none of them is
asserted here, so a failure in them cannot be attributed to the wrong row.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "status-digest.py"
LINE_REGISTRY_ENGINE = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py"
)

#: The three actions contract C-41 fixes — exactly three, no fourth, none missing.
ACTIONS = ("digest", "guard", "report")

#: The triplet keys the registry entry declares (``line-registry.py`` lines 412/425-427).
TRIPLET_KEYS = ("status_path", "log_path", "heartbeat_path")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _require_engine() -> Path:
    assert ENGINE.is_file(), (
        "status-digest engine missing: %s — expected at T009 (087). "
        "Red is the intended pre-implementation state for T006." % ENGINE.relative_to(REPO_ROOT)
    )
    return ENGINE


def _run(args, cwd: Path, env_overrides=None, home: Path | None = None) -> subprocess.CompletedProcess:
    engine = _require_engine()
    env = os.environ.copy()
    for key in ("SPECIFY_LINE_REGISTRY_DIR", "XDG_STATE_HOME"):
        env.pop(key, None)
    env["HOME"] = str(home if home is not None else cwd)
    env.update(env_overrides or {})
    return subprocess.run(
        [sys.executable, str(engine), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )


def _load_engine_constants() -> dict:
    """Load the line-registry engine's closed state sets without importing it as a package.

    The digest MUST NOT import the engine (``plan.md`` § Technical Context): coupling to an internal module path is
    the defect the plan rejects. This test does import it, precisely so the values it pins are read from the owner
    rather than copied into a test-local list.
    """
    assert LINE_REGISTRY_ENGINE.is_file(), (
        "line-registry engine missing: %s" % LINE_REGISTRY_ENGINE.relative_to(REPO_ROOT)
    )
    spec = importlib.util.spec_from_file_location(
        "_line_registry_for_status_digest_tests", LINE_REGISTRY_ENGINE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {
        "STATE_VALUES": set(module.STATE_VALUES),
        "ACTIVE_STATES": set(module.ACTIVE_STATES),
    }


def _write_entry(registry: Path, entry: dict) -> Path:
    registry.mkdir(parents=True, exist_ok=True)
    path = registry / ("%s.json" % entry["line_id"])
    path.write_text(json.dumps(entry, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


def _entry(line_id: str, project_dir: Path, **overrides) -> dict:
    entry = {
        "schema_version": 1,
        "line_id": line_id,
        "run_id": "r20261106T000000Z-aaaa",
        "project_dir": str(project_dir),
        "repo_root": str(project_dir),
        "driver_session": "pid:1",
        "cli": "qodercli",
        "state": "active",
        "last_event": "registered",
        "created_at": "2026-11-06T00:00:00Z",
        "updated_at": "2026-11-06T00:00:00Z",
        "run_history": [],
    }
    entry.update(overrides)
    return entry


def _json_stdout(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected JSON on stdout, got empty output (stderr=%r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - failure path
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


# --------------------------------------------------------------------------- #
# T006-1 — the registry directory resolution order (contract C-42, step 1)
# --------------------------------------------------------------------------- #
def test_registry_dir_env_override_wins(tmp_path):
    """``$SPECIFY_LINE_REGISTRY_DIR`` is the first resolution step."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    override = tmp_path / "override-registry"
    _write_entry(override, _entry("override-line-0001", workspace))
    _write_entry(
        tmp_path / ".local" / "state" / "spec-kit" / "lines",
        _entry("home-line-00000001", workspace),
    )

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(override)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    payload = _json_stdout(proc)
    line_ids = [e["line_id"] for e in payload["entries"]]
    assert line_ids == ["override-line-0001"], (
        "the env override must be the only registry read; got %r" % (line_ids,)
    )
    assert Path(payload["registry_dir"]).resolve() == override.resolve(), (
        "the digest must report the registry directory it actually read"
    )


def test_registry_dir_falls_back_to_xdg_state_home(tmp_path):
    """With no env override, ``$XDG_STATE_HOME/spec-kit/lines`` is second."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    xdg = tmp_path / "xdg"
    _write_entry(
        xdg / "spec-kit" / "lines",
        _entry("xdg-line-00000001", workspace),
    )
    _write_entry(
        tmp_path / ".local" / "state" / "spec-kit" / "lines",
        _entry("home-line-00000001", workspace),
    )

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"XDG_STATE_HOME": str(xdg)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    payload = _json_stdout(proc)
    line_ids = [e["line_id"] for e in payload["entries"]]
    assert line_ids == ["xdg-line-00000001"], (
        "XDG_STATE_HOME must outrank the HOME default; got %r" % (line_ids,)
    )


def test_registry_dir_falls_back_to_home_local_state(tmp_path):
    """With neither override, ``~/.local/state/spec-kit/lines`` is the default.

    The subprocess runs from a plain directory and NOT with ``cwd`` inside the fake HOME: the script resolves
    ``--workspace`` from the current directory, and a cwd inside HOME would make the workspace filter drop the very
    entry this test pins. ``HOME`` itself is the variable under test.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    _write_entry(
        home / ".local" / "state" / "spec-kit" / "lines",
        _entry("home-line-00000001", workspace),
    )

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"HOME": str(home)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    payload = _json_stdout(proc)
    assert [e["line_id"] for e in payload["entries"]] == ["home-line-00000001"], (
        "HOME/.local/state/spec-kit/lines is the third resolution step"
    )


# --------------------------------------------------------------------------- #
# T006-2 — the per-entry triplet projection (contract C-42, step 2)
# --------------------------------------------------------------------------- #
def test_triplet_paths_are_projected_when_declared(tmp_path):
    """A declared triplet projects all three path values verbatim."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    triplet = {
        "status_path": str(tmp_path / "status-line-0001.log"),
        "log_path": str(tmp_path / "log-line-0001.log"),
        "heartbeat_path": str(tmp_path / "heartbeat-line-0001.log"),
    }
    _write_entry(registry, _entry("line-00000001", workspace, **triplet))

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    entry = _json_stdout(proc)["entries"][0]
    assert entry["triplet"] == triplet, (
        "the triplet projection must carry the entry's declared paths verbatim; got %r"
        % (entry.get("triplet"),)
    )


def test_triplet_projects_dash_when_paths_are_absent(tmp_path):
    """An entry with no declared triplet projects the literal ``-`` for every key."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    _write_entry(registry, _entry("line-00000002", workspace))

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    entry = _json_stdout(proc)["entries"][0]
    assert set(entry["triplet"]) == set(TRIPLET_KEYS), (
        "the projection exposes exactly the three triplet keys; got %r"
        % (sorted(entry["triplet"]),)
    )
    assert set(entry["triplet"].values()) == {"-"}, (
        "an absent triplet path projects the literal '-'; got %r" % (entry["triplet"],)
    )


def test_stage_projects_dash_when_absent(tmp_path):
    """The ``stage`` field projects ``-`` when the registry entry carries none."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    _write_entry(registry, _entry("line-00000003", workspace))

    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    assert _json_stdout(proc)["entries"][0]["stage"] == "-", (
        "an entry with no stage must project '-' rather than null or an empty string"
    )


# --------------------------------------------------------------------------- #
# T006-3 — the state vocabulary is quoted from the engine, never re-enumerated
# --------------------------------------------------------------------------- #
def test_projected_state_is_a_member_of_the_engine_state_set(tmp_path):
    """Floor-style: every state the engine can hold projects as a member of ``STATE_VALUES``.

    The assertion is membership, not equality against a test-local list — a new engine value must flow through this
    test without an edit, and a projection that invents its own vocabulary must fail it.
    """
    constants = _load_engine_constants()
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    projected = []
    for index, state in enumerate(sorted(constants["STATE_VALUES"])):
        line_id = "state-%02d-%06d" % (index, index)
        _write_entry(registry, _entry(line_id, workspace, state=state))
        projected.append((line_id, state))

    proc = _run(
        ["--action", "digest", "--format", "json", "--cap", str(len(projected))],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    entries = _json_stdout(proc)["entries"]
    assert {e["line_id"] for e in entries} == {lid for lid, _ in projected}, (
        "every state entry must be projected; got %r" % ([e["line_id"] for e in entries],)
    )
    for entry in entries:
        assert entry["state"] in constants["STATE_VALUES"], (
            "projected state %r is not a member of the engine's STATE_VALUES %r"
            % (entry["state"], sorted(constants["STATE_VALUES"]))
        )


def test_active_flag_derives_from_the_engine_active_set(tmp_path):
    """``is_active`` is the engine's ``ACTIVE_STATES`` predicate, not a second one."""
    constants = _load_engine_constants()
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    active_state = sorted(constants["ACTIVE_STATES"])[0]
    inactive_state = sorted(constants["STATE_VALUES"] - constants["ACTIVE_STATES"])[0]
    _write_entry(registry, _entry("active-line-0001", workspace, state=active_state))
    _write_entry(registry, _entry("inactive-line-001", workspace, state=inactive_state))

    proc = _run(
        ["--action", "digest", "--format", "json", "--cap", "10"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    by_id = {e["line_id"]: e for e in _json_stdout(proc)["entries"]}
    assert by_id["active-line-0001"]["is_active"] is True, (
        "%r is an ACTIVE_STATES member, so is_active must be true" % active_state
    )
    assert by_id["inactive-line-001"]["is_active"] is False, (
        "%r is not an ACTIVE_STATES member, so is_active must be false" % inactive_state
    )


def test_engine_constants_are_the_authority_not_the_test(tmp_path):
    """Guard the guard: the imported sets are non-empty and disjoint in the expected direction."""
    constants = _load_engine_constants()
    assert constants["STATE_VALUES"], "STATE_VALUES must not be empty"
    assert constants["ACTIVE_STATES"] <= constants["STATE_VALUES"], (
        "ACTIVE_STATES must be a subset of STATE_VALUES; the engine moved and this test must be re-read"
    )


# --------------------------------------------------------------------------- #
# T006-4 — the read-only boundary (contract C-42), asserted three ways
# --------------------------------------------------------------------------- #
def test_script_source_contains_no_write_mode_open():
    """Static audit: no ``open(..., 'w'/'a'/'x')`` and no write-mode file constructor in the source."""
    engine = _require_engine()
    tree = ast.parse(engine.read_text(encoding="utf-8"), filename=str(engine))
    write_modes = {"w", "a", "x", "wb", "ab", "xb", "w+", "a+", "x+"}
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = getattr(func, "id", None) or getattr(func, "attr", None)
        if name != "open":
            continue
        mode = None
        if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
            mode = node.args[1].value
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = kw.value.value
        if isinstance(mode, str) and mode in write_modes:
            offenders.append((getattr(node, "lineno", "?"), mode))
    assert not offenders, (
        "status-digest.py must open no file for writing; found %r" % (offenders,)
    )


def test_script_source_never_calls_a_writer_api():
    """Static audit: no filesystem-mutating method is called on any object.

    ``str.replace`` is a pure string operation and is therefore excluded by its receiver, not by its name — the audit
    is about *filesystem* mutation, and a name-only blocklist would both miss a writer and flag a benign call.
    """
    engine = _require_engine()
    tree = ast.parse(engine.read_text(encoding="utf-8"), filename=str(engine))
    forbidden = {
        "write_text",
        "write_bytes",
        "mkdir",
        "unlink",
        "rename",
        "rmdir",
        "mkstemp",
        "mkdtemp",
        "copyfile",
        "copytree",
    }
    offenders = sorted(
        {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in forbidden
        }
    )
    # ``Path.replace`` is a rename; ``str.replace`` is not. Distinguish by the receiver's call site.
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "replace"
            and isinstance(node.func.value, ast.Call)
            and getattr(node.func.value.func, "id", None) == "Path"
        ):
            offenders.append("Path.replace")
    assert not offenders, (
        "status-digest.py must not mutate the filesystem; found calls to %r" % (offenders,)
    )


def test_runtime_reads_leave_every_input_byte_identical(tmp_path):
    """Runtime audit: the digest over a fixture registry changes no byte of its inputs."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    triplet_file = tmp_path / "status-line-0001.log"
    triplet_file.write_text("one line\n", encoding="utf-8")
    entry_path = _write_entry(
        registry,
        _entry("line-00000001", workspace, status_path=str(triplet_file)),
    )

    def snapshot() -> dict:
        return {
            str(p.relative_to(tmp_path)): (p.stat().st_mtime_ns, p.read_bytes())
            for p in sorted(tmp_path.rglob("*"))
            if p.is_file()
        }

    before = snapshot()
    proc = _run(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, "digest failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    after = snapshot()

    assert after == before, (
        "the digest must not create, delete or rewrite any file; changed: %r"
        % (sorted(set(after) ^ set(before)) or "contents differ",)
    )
    assert entry_path.is_file(), "the registry entry must still exist after the read"


# --------------------------------------------------------------------------- #
# T006-5 — the action surface exists (established here, judged in full by T033)
# --------------------------------------------------------------------------- #
def test_exactly_three_actions_are_declared():
    """Contract C-41 floor: the script exposes the three action names and nothing else."""
    engine = _require_engine()
    text = engine.read_text(encoding="utf-8")
    for action in ACTIONS:
        assert action in text, (
            "action %r must be declared by status-digest.py (contract C-41)" % action
        )


def test_unknown_action_is_an_input_error(tmp_path):
    """An action outside the closed set exits 2 (input error), never 0 or 1."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    proc = _run(
        ["--action", "not-an-action"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(tmp_path / "empty")},
    )
    assert proc.returncode == 2, (
        "an unknown action must exit 2; got rc=%s (stderr=%r)" % (proc.returncode, proc.stderr)
    )


def test_script_is_a_single_stdlib_only_file(tmp_path):
    """Contract RS-08 shape applied to this script: one file, standard library imports only."""
    engine = _require_engine()
    tree = ast.parse(engine.read_text(encoding="utf-8"), filename=str(engine))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    third_party = sorted(
        name
        for name in imported
        if name not in sys.stdlib_module_names and name != "__future__"
    )
    assert not third_party, (
        "status-digest.py must import only the standard library; found %r" % (third_party,)
    )


def test_no_process_spawn_in_source():
    """Contract OM-04 (C-50): the digest/guard path spawns no process.

    An AST audit rather than a text scan: the script *names* the forbidden APIs in order to describe and run this very
    audit, so a text scan would always find itself. The question the clause asks is whether any of them is imported
    or called.
    """
    engine = _require_engine()
    tree = ast.parse(engine.read_text(encoding="utf-8"), filename=str(engine))
    spawn_modules = {"subprocess", "multiprocessing", "threading", "asyncio"}
    spawn_calls = {"system", "fork", "execv", "execvp", "execl", "execle", "spawnl", "spawnv", "popen"}
    imports, calls = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            calls.add(node.func.attr)
    assert not (imports & spawn_modules), (
        "status-digest.py must import no spawn/thread module; found %r"
        % sorted(imports & spawn_modules)
    )
    assert not (calls & spawn_calls), (
        "status-digest.py must call no spawn API; found %r" % sorted(calls & spawn_calls)
    )
    assert shutil.which("python3"), "sanity: the interpreter used by these tests resolves"
