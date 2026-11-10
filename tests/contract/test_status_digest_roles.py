"""Contract test: the digest's role-edge view (095, T034).

Owner of the design contract: ``.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md``
(C-1…C-8). This module owns the digest-side half of the role view:

* C-1 — one reader, one renderer: the role model is one ``read_carrier_inputs`` + one
  ``evaluate_role_model`` call per digest run (asserted structurally over the script source), the
  digest carries no second parser for the role carriers, and the existing table renderer is the
  only renderer;
* C-2 — every entry carries ``parent`` / ``roles`` / ``role_set_marker`` / ``depth`` beside its
  existing fields, with the two source families kept unmixed (line rows keep ``line_id`` /
  ``last_activity_at``; executor rows outside the registry use ``id`` / ``last_activity``);
* C-3 — the merged entry set keeps the existing cap/``omitted`` declaration and the
  ``nothing-running`` rendering (exit 3) unchanged;
* C-4 — one digest read renders a parent row plus one row per child for a ten-child fan-out;
* C-5 — the role fields are passed through from the model unchanged (the digest never re-derives
  the both-roles marker, never reads process state for them);
* C-7 — seeded mutations prove the guarding checks are not blind (a dropped field and a second
  renderer both turn them red);
* the mirror copy renders the same role view (plan § Mirror Obligations pins the pair here).

**Red-first (Constitution IV)**: authored before ``status-digest.py`` grows the role view, so the
field/schema/fan-out legs fail on their own missing-key assertions — never on an import error.

**Degrade decision (analyze W2-15)**: the engine requires its three carrier roots, while a project
that never ran a team or driver may not have them. The digest therefore renders the four role
fields with empty values (``None`` / ``[]`` / ``None`` / ``None``) when the materialization is
unavailable, and keeps its own reading otherwise untouched; the last test pins that face.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "python" / "status-digest.py"
MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "status-digest.py"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "superagent-role"

#: The four role-view fields C-2 adds to every rendered entry, in contract order.
ROLE_FIELDS = ("parent", "roles", "role_set_marker", "depth")

#: The closed violation of the renderer clause: a role-specific render function.
SECOND_RENDERER = re.compile(r"def\s+\w*render\w*role|def\s+\w*role\w*render")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _engine_source() -> str:
    assert SCRIPT.is_file(), "digest engine missing: scripts/python/status-digest.py"
    return SCRIPT.read_text(encoding="utf-8")


def _workspace_from_fixture(tmp_path: Path, name: str):
    """Copy one feature fixture into a digest-shaped workspace and return it with its registry.

    The digest resolves its carrier roots from ``--workspace`` (``<ws>/.specify/{state,teams,
    agents/execution/logs}``); the fixture keeps the engine-shaped layout, so the copy is the
    bridge. ``@WORKSPACE@`` inside a fixture registry entry is replaced with the copy's path so
    the workspace rule lists the entry (the raw fixture stays path-free).
    """
    fixture = FIXTURE_ROOT / name
    assert fixture.is_dir(), f"fixture missing: tests/fixtures/superagent-role/{name}"
    for part in ("state", "teams", "logs", "registry"):
        assert (fixture / part).is_dir(), f"fixture root missing: {name}/{part}"
    workspace = tmp_path / "workspace"
    targets = {
        "state": workspace / ".specify" / "state",
        "teams": workspace / ".specify" / "teams",
        "logs": workspace / ".specify" / "agents" / "execution" / "logs",
    }
    for part, target in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(fixture / part, target)
    registry = tmp_path / "registry"
    shutil.copytree(fixture / "registry", registry)
    for path in sorted(registry.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        if "@WORKSPACE@" in text:
            path.write_text(text.replace("@WORKSPACE@", str(workspace)), encoding="utf-8")
    return workspace, registry


def _workspace_without_carrier_roots(tmp_path: Path):
    """A bare workspace plus one registry entry — the pre-095 digest posture (no teams/logs roots)."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    registry.mkdir()
    entry = {
        "schema_version": 1,
        "line_id": "bare-line",
        "run_id": "r20261110T000000Z-bare",
        "project_dir": str(workspace),
        "repo_root": str(workspace),
        "state": "active",
        "created_at": "2026-11-10T00:00:00Z",
        "updated_at": "2026-11-10T00:00:00Z",
        "run_history": [],
    }
    (registry / "bare-line.json").write_text(
        json.dumps(entry, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return workspace, registry


def _digest(workspace: Path, registry: Path, *extra, script: Path | None = None):
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(workspace),
        "SPECIFY_LINE_REGISTRY_DIR": str(registry),
    }
    return subprocess.run(
        [sys.executable, str(script or SCRIPT), "--action", "digest", "--workspace", str(workspace), *extra],
        cwd=str(workspace),
        capture_output=True,
        text=True,
        env=env,
    )


def _payload(proc) -> dict:
    assert proc.stdout.strip(), "expected JSON on stdout (stderr=%r)" % proc.stderr
    return json.loads(proc.stdout)


def _age_tree(root: Path, seconds: int) -> None:
    stamp = time.time() - seconds
    for path in root.rglob("*"):
        if path.is_file():
            os.utime(path, (stamp, stamp))


def _entry_rows(rendered: str) -> list:
    """The aligned table body rows (the existing contract test uses the same shape)."""
    lines = rendered.splitlines()
    sep = next((i for i, line in enumerate(lines) if line and set(line.replace(" ", "")) == {"-"}), None)
    assert sep is not None, "the table carries a separator row:\n%s" % rendered
    rows = []
    for line in lines[sep + 1:]:
        if not line.strip():
            break
        if line.startswith(("last_completion=", "omitted=", "store=", "最近完成：", "另有 ", "未找到运行记录存储")):
            break
        rows.append(line)
    return rows


def _declared_role_fields(source: str) -> tuple:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            getattr(target, "id", None) == "ROLE_VIEW_FIELDS" for target in node.targets
        ):
            return tuple(ast.literal_eval(node.value))
    return ()


def _second_renderer_offenders(source: str) -> list:
    return SECOND_RENDERER.findall(source)


def _role_attachment_fn(source: str, name: str = "merge_role_entries"):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(source, node) or ""
    return None


# --------------------------------------------------------------------------- #
# C-1 — one materialization per run, decided on observable reads
#
# The clause is behavioural ("the legacy line entries and the role view both derive from it, and no carrier
# root may be read twice"), so the guard observes actual reads: an audit hook records every directory scan
# and file open an in-process digest run performs. Counting AST call sites cannot see a second read.
# --------------------------------------------------------------------------- #
_AUDIT = {"active": False, "events": [], "installed": False}


def _install_audit_hook():
    if _AUDIT["installed"]:
        return

    def hook(event, args):
        if not _AUDIT["active"]:
            return
        if event in ("os.scandir", "os.listdir", "open"):
            try:
                _AUDIT["events"].append((event, str(args[0])))
            except Exception:
                pass

    sys.addaudithook(hook)
    _AUDIT["installed"] = True


def _run_digest_in_process(args, workspace: Path, registry: Path):
    """Run the digest in this process under an audit hook; returns ``(exit_code, stdout, events)``."""
    import contextlib
    import io
    import runpy

    _install_audit_hook()
    env_keys = ("SPECIFY_LINE_REGISTRY_DIR", "XDG_STATE_HOME", "HOME", "SPECIFY_STATUS_WORKSPACE")
    saved_env = {key: os.environ.get(key) for key in env_keys}
    saved_cwd, saved_argv = os.getcwd(), sys.argv
    os.environ["SPECIFY_LINE_REGISTRY_DIR"] = str(registry)
    os.environ["HOME"] = str(workspace)
    os.environ.pop("XDG_STATE_HOME", None)
    os.environ.pop("SPECIFY_STATUS_WORKSPACE", None)
    os.chdir(workspace)
    sys.argv = [str(SCRIPT), *args]
    _AUDIT["events"] = []
    buffer = io.StringIO()
    code = 0
    try:
        _AUDIT["active"] = True
        with contextlib.redirect_stdout(buffer):
            runpy.run_path(str(SCRIPT), run_name="__main__")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
    finally:
        _AUDIT["active"] = False
        for key, value in saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        os.chdir(saved_cwd)
        sys.argv = saved_argv
    return code, buffer.getvalue(), list(_AUDIT["events"])


def test_c1_the_role_model_is_one_materialization_per_run(tmp_path):
    """C-1 (behaviour): the registry carrier root is read exactly once, and each entry opened once.

    The fixture provides the engine's three required carrier roots, so the materialization is the path taken and
    the legacy line rows derive from its registry read. A second read anywhere — the defect this clause names —
    makes either count exceed one.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    for part in ("state", "teams", "agents/execution/logs"):
        (workspace / ".specify" / part).mkdir(parents=True, exist_ok=True)
    registry = tmp_path / "registry"
    registry.mkdir()
    entry_paths = []
    for index in range(2):
        entry = {
            "schema_version": 1,
            "line_id": "c1-line-%d" % index,
            "run_id": "r20261110T000000Z-c1-%d" % index,
            "project_dir": str(workspace),
            "repo_root": str(workspace),
            "state": "active",
            "created_at": "2026-11-10T00:00:00Z",
            "updated_at": "2026-11-10T00:%02d:00Z" % index,
            "run_history": [],
        }
        path = registry / ("c1-line-%d.json" % index)
        path.write_text(json.dumps(entry), encoding="utf-8")
        entry_paths.append(path)

    code, stdout, events = _run_digest_in_process(
        ["--action", "digest", "--workspace", str(workspace), "--format", "json"],
        workspace,
        registry,
    )
    assert code == 0, "the fixture digest must render; stdout=%r stderr-events=%r" % (stdout, events)

    registry_root = registry.resolve()
    scans = [
        event
        for event in events
        if event[0] in ("os.scandir", "os.listdir") and Path(event[1]).resolve() == registry_root
    ]
    assert len(scans) == 1, (
        "the registry carrier root must be read exactly once per run (contract C-1); observed %d reads: %r"
        % (len(scans), events)
    )
    for path in entry_paths:
        opens = [
            event
            for event in events
            if event[0] == "open" and Path(event[1]).resolve() == path.resolve()
        ]
        assert len(opens) == 1, (
            "registry entry %s must be opened exactly once by the one materialization; observed %d"
            % (path.name, len(opens))
        )
    # Both views are present from that one read: the legacy line rows and the role fields.
    payload = json.loads(stdout)
    assert {entry.get("line_id") for entry in payload["entries"]} == {"c1-line-0", "c1-line-1"}
    for entry in payload["entries"]:
        for field in ROLE_FIELDS:
            assert field in entry, "the role view derives from the same read; missing %r" % field


def test_c1_the_digest_adds_no_second_carrier_parser_or_root_scan():
    """C-1: the role carriers' parsing stays in the engine; the digest scans no new carrier root."""
    source = _engine_source()
    for token in ("Execution Detail", ".meta.json", "role_edge", "role-transition"):
        assert token not in source, (
            "the digest must not carry a second parser for the role carriers (found %r)" % token
        )
    assert source.count(".glob(") == 2, (
        "the digest scans exactly two roots of its own (the legacy registry and the pid state scan); "
        "the role carriers are scanned only by the materialization"
    )
    assert source.count('glob("*.json")') == 1, (
        "the legacy registry scan is the digest's only registry read"
    )
    assert source.count('glob("pid-*")') == 1, (
        "the legacy executor scan is the digest's only state-root scan"
    )
    assert source.count("teams_dir") == 1, (
        "the teams root is named only by the single materialization call"
    )


# --------------------------------------------------------------------------- #
# C-2 — entry fields, both families, unmixed
# --------------------------------------------------------------------------- #
def test_c2_line_rows_gain_the_role_fields_and_keep_their_family(tmp_path):
    """C-2: a line-registry row keeps ``line_id`` / ``last_activity_at`` and gains the four fields."""
    workspace, registry = _workspace_from_fixture(tmp_path, "interrupted")
    proc = _digest(workspace, registry, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    line = next(e for e in payload["entries"] if e.get("line_id") == "demo-line")
    for field in ROLE_FIELDS:
        assert field in line, "line row misses the role field %r; got %r" % (field, sorted(line))
    assert "last_activity_at" in line and "line_id" in line
    assert "id" not in line and "last_activity" not in line, (
        "the two field families must never mix inside one entry; got %r" % sorted(line)
    )
    assert line["parent"] is None and line["depth"] == 0
    assert line["roles"] == ["superagent"] and line["role_set_marker"] is None


def test_c2_executor_rows_outside_the_registry_use_the_role_names(tmp_path):
    """C-2: an executor row outside the registry uses ``id`` / ``last_activity`` and null source fields."""
    workspace, registry = _workspace_from_fixture(tmp_path, "interrupted")
    proc = _digest(workspace, registry, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    child = next(e for e in payload["entries"] if e.get("id") == "child-1")
    for field in ROLE_FIELDS + ("state", "last_activity", "age", "stale"):
        assert field in child, "executor row misses %r; got %r" % (field, sorted(child))
    assert child["parent"] == "r-fixture-root"
    assert child["roles"] == ["subagent"]
    assert child["role_set_marker"] is None
    assert child["depth"] == 1
    for key in ("project_dir", "branch", "stage"):
        assert key in child and child[key] is None, (
            "an executor row states %r as null where the source type does not carry it" % key
        )
    assert "line_id" not in child and "last_activity_at" not in child, (
        "the two field families must never mix inside one entry; got %r" % sorted(child)
    )


def test_c2_the_four_role_fields_are_declared_once(tmp_path):
    """C-2: the field set lives in one constant, so dropping a field is a single visible edit."""
    declared = _declared_role_fields(_engine_source())
    assert declared == ROLE_FIELDS, (
        "the digest must declare the four role-view fields once; got %r" % (declared,)
    )


# --------------------------------------------------------------------------- #
# C-3 — bounded output unchanged
# --------------------------------------------------------------------------- #
def test_c3_omitted_declares_the_truncated_merged_set(tmp_path):
    """C-3: the cap applies to the merged set and truncation declares ``omitted=<n>``."""
    workspace, registry = _workspace_from_fixture(tmp_path, "interrupted")
    proc = _digest(workspace, registry, "--format", "json", "--cap", "1")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    assert len(payload["entries"]) == 1
    assert payload["omitted"] == 1, (
        "one of the two visible executors is not shown, so omitted must say 1; got %r"
        % payload["omitted"]
    )
    table = _digest(workspace, registry, "--cap", "1")
    assert "另有 1 条未显示" in table.stdout, table.stdout


def test_c3_nothing_running_is_unchanged(tmp_path):
    """C-3: the empty merged set renders the literal and exit 3 — not an empty summary."""
    workspace, registry = _workspace_without_carrier_roots(tmp_path)
    empty = tmp_path / "empty-registry"
    empty.mkdir()
    proc = _digest(workspace, empty)
    assert proc.returncode == 3, "an empty set is the nothing-running answer; got %r" % (proc,)
    assert proc.stdout.strip() == "nothing-running", proc.stdout


# --------------------------------------------------------------------------- #
# C-4 — fan-out shape
# --------------------------------------------------------------------------- #
def test_c4_one_read_renders_the_parent_and_ten_children(tmp_path):
    """C-4: a ten-child fan-out renders one parent row plus one row per child in the same read."""
    workspace, registry = _workspace_from_fixture(tmp_path, "fanout-10")
    proc = _digest(workspace, registry, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    entries = payload["entries"]
    parent = next(e for e in entries if e.get("id") == "A")
    assert parent["parent"] == "root"
    assert parent["roles"] == ["subagent", "superagent"]
    assert parent["role_set_marker"] == "dual-role", (
        "the both-roles marker is passed through from the model; got %r"
        % parent.get("role_set_marker")
    )
    assert parent["depth"] == 1
    children = [e for e in entries if e.get("parent") == "A" and "id" in e]
    assert len(children) == 10, "one row per child in one read; got %d" % len(children)
    assert {child["depth"] for child in children} == {2}
    assert {child["roles"][0] for child in children} == {"subagent"}
    root = next(e for e in entries if e.get("id") == "root")
    assert root["parent"] is None and root["depth"] == 0 and root["roles"] == ["superagent"]


def test_c4_the_table_carries_the_role_columns(tmp_path):
    """C-2/C-4: the single human renderer carries the same fields (localized labels allowed)."""
    workspace, registry = _workspace_from_fixture(tmp_path, "fanout-10")
    proc = _digest(workspace, registry)
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    for column in ("父边", "角色", "深度"):
        assert column in out, "the table must carry the %r column; got:\n%s" % (column, out)
    assert "subagent,superagent" in out and "dual-role" in out, (
        "the dual-role executor's row carries its role set and the both-roles marker; got:\n%s" % out
    )
    rows = _entry_rows(out)
    assert len(rows) == 12, "root + A + ten children render as one row each; got %r" % rows


# --------------------------------------------------------------------------- #
# C-5 — provenance: pass-through, never re-derived, never a scan
# --------------------------------------------------------------------------- #
def test_c5_the_both_roles_marker_is_passed_through_never_re_derived():
    """C-5: the marker literal never appears in the digest — it can only come from the model."""
    source = _engine_source()
    assert "dual-role" not in source, (
        "re-deriving the marker in the digest is a second source; it must be passed through"
    )


def test_c5_role_fields_are_attached_without_process_state():
    """C-5: the role attachment reads the model's keys only — no pid/proc scan, no store read."""
    source = _engine_source()
    segment = _role_attachment_fn(source)
    assert segment is not None, "the digest must attach the role fields in one named helper"
    assert "role_set_marker" in segment and "roles" in segment and "depth" in segment
    for forbidden in ("_pid_alive", "read_executors", "/proc", "os.kill", "load_store_engine"):
        assert forbidden not in segment, (
            "the role fields must never derive from %r — they are model pass-through" % forbidden
        )


# --------------------------------------------------------------------------- #
# C-6 — the existing JSON vocabulary is untouched
# --------------------------------------------------------------------------- #
def test_c6_the_existing_json_keys_keep_their_names(tmp_path):
    workspace, registry = _workspace_from_fixture(tmp_path, "fanout-10")
    payload = _payload(_digest(workspace, registry, "--format", "json"))
    for key in (
        "registry_dir",
        "generated_at",
        "cap",
        "stale_bound_seconds",
        "entries",
        "all_entries",
        "omitted",
        "profile",
        "state_summary",
        "efficiency",
    ):
        assert key in payload, "the existing JSON key %r must keep its name" % key
    assert payload["state_summary"] == "active"


# --------------------------------------------------------------------------- #
# C-5/C-3 — the interrupted fixture: stale/interrupted, never silently completed
# --------------------------------------------------------------------------- #
def test_the_interrupted_child_renders_stale_interrupted_and_never_completed(tmp_path):
    """SC-005's digest face: no exit record + stale activity under a stopped parent → interrupted."""
    workspace, registry = _workspace_from_fixture(tmp_path, "interrupted")
    spine = (workspace / ".specify" / "state" / "demo-line.md").read_text(encoding="utf-8")
    assert "spine_state: stalled" in spine, (
        "the fixture carries the parent's stopping verdict in its status spine"
    )
    status = (workspace / ".specify" / "agents" / "execution" / "logs" / "child-1.status").read_text(
        encoding="utf-8"
    )
    assert "exit=" not in status, "the child never recorded an exit — it only appears running"
    _age_tree(workspace / ".specify" / "agents" / "execution" / "logs", 3600)

    proc = _digest(workspace, registry, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    child = next(e for e in payload["entries"] if e.get("id") == "child-1")
    assert child["state"] == "interrupted", (
        "a child still appearing running under a stopped parent is marked interrupted; got %r"
        % child["state"]
    )
    assert child["state"] != "completed", "the interrupted child must never read as completed"
    assert child["stale"] is True and child["age_seconds"] >= 900
    line = next(e for e in payload["entries"] if e.get("line_id") == "demo-line")
    assert line["state"] == "stalled"

    table = _digest(workspace, registry)
    assert table.returncode == 0, table.stderr
    assert "已中断" in table.stdout and "静默" in table.stdout, table.stdout
    assert "已完成" not in table.stdout, (
        "the interrupted child is never rendered as completed; got:\n%s" % table.stdout
    )


# --------------------------------------------------------------------------- #
# C-7 — seeded mutations: the checks are not blind
# --------------------------------------------------------------------------- #
def test_c7_dropping_a_role_field_turns_the_declaration_check_red():
    """Dragging one field out of the declared set must be caught by the presence check."""
    source = _engine_source()
    assert _declared_role_fields(source) == ROLE_FIELDS
    mutated = source.replace('"role_set_marker", "depth"', '"depth"', 1)
    assert mutated != source, "the seeded drop must change the source"
    assert _declared_role_fields(mutated) == ("parent", "roles", "depth"), (
        "the check must read the mutated declaration, not a cached good value"
    )
    assert _declared_role_fields(mutated) != ROLE_FIELDS


def test_c7_adding_a_second_renderer_turns_the_single_renderer_check_red():
    source = _engine_source()
    assert _second_renderer_offenders(source) == []
    mutated = source + "\n\ndef render_role_view(state):\n    return ''\n"
    assert _second_renderer_offenders(mutated), (
        "a role-specific renderer is the defect C-1 names and must be detected"
    )


def test_c7_the_action_still_delegates_to_the_one_table_renderer():
    source = _engine_source()
    tree = ast.parse(source)
    action = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "action_digest"
    )
    calls = [
        node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
        for node in ast.walk(action)
        if isinstance(node, ast.Call)
    ]
    assert calls.count("render_digest_table") == 1, (
        "the role view renders through the existing table renderer, never a second one; calls=%r" % calls
    )


# --------------------------------------------------------------------------- #
# Mirror parity — the runtime copy renders the same role view
# --------------------------------------------------------------------------- #
def test_the_mirror_renders_the_same_role_view(tmp_path):
    """plan § Mirror Obligations: the pair is pinned here, not only by byte equality."""
    assert MIRROR.is_file(), "the runtime mirror must exist"
    workspace, registry = _workspace_from_fixture(tmp_path, "fanout-10")
    source_payload = _payload(_digest(workspace, registry, "--format", "json"))
    mirror_payload = _payload(_digest(workspace, registry, "--format", "json", script=MIRROR))
    source_payload.pop("generated_at", None)
    mirror_payload.pop("generated_at", None)
    assert source_payload == mirror_payload, (
        "the runtime mirror must render the same role view as its source"
    )


# --------------------------------------------------------------------------- #
# W2-15 — the degrade face: no carrier roots still renders the four fields
# --------------------------------------------------------------------------- #
def test_without_carrier_roots_the_role_fields_render_as_empty_not_missing(tmp_path):
    """The engine's required roots may not exist in a young project; the fields still render."""
    workspace, registry = _workspace_without_carrier_roots(tmp_path)
    proc = _digest(workspace, registry, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    line = payload["entries"][0]
    assert line["parent"] is None
    assert line["roles"] == []
    assert line["role_set_marker"] is None
    assert line["depth"] is None
