"""Contract tests — git workflow observation hook + init-seeded policy template.

Three surfaces:
1. **Init seeding** (``specify init``): ``templates/workflow/git.md`` lands at
   ``.specify/workflow/git.md`` only when absent; an existing policy file is never
   overwritten.
2. **The observe action** (``scripts/python/git-workflow-observe.py``): a fixture git
   repository proves the update is idempotent, ``--check`` writes nothing, and the
   ``GIT_WORKFLOW`` declaration block stays byte-identical.
3. **The registry hook** (probe + handler): the ``h-git-workflow-observe`` row and its
   ``@point:situation`` binding exist, the action is a real engine action, and the
   phase-2 rows leave the wrap-up compiled face zero-drift with an unchanged
   fingerprint. The end-to-end case runs the situation engine's assess and asserts
   the observe handler actually fired.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from specify_cli import copy_local_templates
from tests.script_api import probe_utils

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "git-workflow-observe.py"
TRIGGER = REPO_ROOT / "scripts" / "python" / "trigger-utils.py"
REGISTRY = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
TEMPLATE = REPO_ROOT / "templates" / "workflow" / "git.md"
PROBE_UTILS = REPO_ROOT / "scripts" / "python" / "probe-utils.py"

WF_START = "<!-- GIT_WORKFLOW_START -->"
WF_END = "<!-- GIT_WORKFLOW_END -->"
OBS_START = "<!-- GIT_OBSERVED_START -->"
OBS_END = "<!-- GIT_OBSERVED_END -->"
STATE_REL = Path(".specify") / "workflow" / "git.md"

STATE_TEXT = """# Git Workflow (Spec Kit framework)

<!-- GIT_WORKFLOW_START -->
- **Workflow model**: temp-branch
- **Trunk**: `master`
- **Closeout**: `ask`
- **Closeout remotes**: `origin`
- **Last updated**: 2026-11-10
<!-- GIT_WORKFLOW_END -->
"""


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, check=True, env=env)


def _repo(path: Path, branches=("050-alpha", "051-beta")) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "symbolic-ref", "HEAD", "refs/heads/master")
    _git(path, "commit", "-q", "--allow-empty", "-m", "init")
    for branch in branches:
        _git(path, "branch", branch)
    _git(path, "remote", "add", "origin", "https://example.invalid/fork.git")
    return path


def _state_file(ws: Path, text: str = STATE_TEXT) -> Path:
    target = ws / STATE_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def _run(ws: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ENGINE), "--action", "observe", *args,
                           "--workspace", str(ws)],
                          capture_output=True, text=True, check=False)


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), proc.stderr
    return json.loads(proc.stdout)


def _block(text: str) -> str:
    start = text.index(WF_START)
    end = text.index(WF_END) + len(WF_END)
    return text[start:end]


# ---------------------------------------------------------------------------
# 1. Init seeding
# ---------------------------------------------------------------------------

def _resource(root: Path, with_workflow_template: bool = True) -> Path:
    resource = root / "resource"
    (resource / "templates" / "commands").mkdir(parents=True)
    (resource / "templates" / "commands" / "requirements.md").write_text(
        "# requirements\n", encoding="utf-8")
    (resource / "memory").mkdir(parents=True)
    (resource / "memory" / "constitution.md").write_text("# C\n", encoding="utf-8")
    (resource / "scripts").mkdir()
    if with_workflow_template:
        (resource / "templates" / "workflow").mkdir(parents=True)
        shutil.copy2(TEMPLATE, resource / "templates" / "workflow" / "git.md")
    return resource


def test_init_seeds_the_policy_template_when_absent(monkeypatch, tmp_path):
    resource = _resource(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)
    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")

    seeded = project / STATE_REL
    assert seeded.is_file(), "init must seed .specify/workflow/git.md when absent"
    assert seeded.read_text(encoding="utf-8") == TEMPLATE.read_text(encoding="utf-8")
    assert "None yet." in seeded.read_text(encoding="utf-8"), \
        "the seeded skeleton must carry the Bootstrap placeholder state"
    # The template face also lands under .specify/templates/ (generic template copy).
    assert (project / ".specify" / "templates" / "workflow" / "git.md").is_file()


def test_init_never_overwrites_an_existing_policy(monkeypatch, tmp_path):
    resource = _resource(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)
    project = tmp_path / "proj"
    _state_file(project, "# user policy\n")
    copy_local_templates(project, "claude", "sh")
    assert (project / STATE_REL).read_text(encoding="utf-8") == "# user policy\n"


def test_init_without_the_template_creates_nothing(monkeypatch, tmp_path):
    resource = _resource(tmp_path, with_workflow_template=False)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)
    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")
    assert not (project / STATE_REL).exists()


# ---------------------------------------------------------------------------
# 2. The observe action on a fixture repository
# ---------------------------------------------------------------------------

def test_observe_creates_the_section_and_leaves_declarations_byte_identical(tmp_path):
    ws = _repo(tmp_path / "ws")
    state = _state_file(ws)
    proc = _run(ws, "--json")
    assert proc.returncode == 0, proc.stderr
    payload = _payload(proc)
    assert payload["ok"] is True and payload["changed"] is True

    text = state.read_text(encoding="utf-8")
    assert text.count(OBS_START) == 1 and text.count(OBS_END) == 1
    assert _block(text) == _block(STATE_TEXT), \
        "the GIT_WORKFLOW declaration block must stay byte-identical"
    assert "**Trunk**: `master` (declared; present locally)" in text
    assert "`origin`" in text
    # The section sits outside (after) the managed block.
    assert text.index(WF_END) < text.index(OBS_START)


def test_observe_is_idempotent(tmp_path):
    ws = _repo(tmp_path / "ws")
    state = _state_file(ws)
    assert _run(ws, "--json").returncode == 0
    first = state.read_text(encoding="utf-8")
    proc = _run(ws, "--json")
    assert proc.returncode == 0
    assert _payload(proc)["changed"] is False
    assert state.read_text(encoding="utf-8") == first, \
        "an unchanged observation set must not rewrite the file"
    assert _run(ws, "--check", "--json").returncode == 0


def test_check_reports_pending_without_writing(tmp_path):
    ws = _repo(tmp_path / "ws")
    state = _state_file(ws)
    before = state.read_text(encoding="utf-8")
    proc = _run(ws, "--check", "--json")
    assert proc.returncode == 10, "a pending observation update must exit 10"
    assert _payload(proc)["wouldChange"] is True
    assert state.read_text(encoding="utf-8") == before, "--check must write nothing"


def test_observe_updates_when_a_fact_changes_but_never_declarations(tmp_path):
    ws = _repo(tmp_path / "ws")
    state = _state_file(ws)
    assert _run(ws, "--json").returncode == 0
    first = state.read_text(encoding="utf-8")

    _git(ws, "branch", "052-gamma")
    assert _run(ws, "--check", "--json").returncode == 10
    proc = _run(ws, "--json")
    assert proc.returncode == 0 and _payload(proc)["changed"] is True

    second = state.read_text(encoding="utf-8")
    assert second != first
    assert _block(second) == _block(STATE_TEXT)
    assert "3/3" in second, "the observation must count the new non-declared branch"


def test_observe_skips_without_a_state_file(tmp_path):
    ws = _repo(tmp_path / "ws")
    proc = _run(ws, "--json")
    assert proc.returncode == 0
    payload = _payload(proc)
    assert payload["skipped"] == "workflow-state-file-absent"
    assert not (ws / STATE_REL).exists()


def test_observe_treats_a_non_repository_workspace_honestly(tmp_path):
    ws = tmp_path / "plain"
    (ws / ".specify").mkdir(parents=True)
    state = _state_file(ws)
    proc = _run(ws, "--json")
    assert proc.returncode == 0
    text = state.read_text(encoding="utf-8")
    assert "not a git repository" in text
    assert _block(text) == _block(STATE_TEXT)


# ---------------------------------------------------------------------------
# 3. The registry hook
# ---------------------------------------------------------------------------

def _handler_rows() -> dict:
    text = REGISTRY.read_text(encoding="utf-8")
    return {row["handler_id"]: row for row in probe_utils._table_rows(text, "Handler")}


def _binding_rows() -> list:
    text = REGISTRY.read_text(encoding="utf-8")
    return probe_utils._table_rows(text, "HandlerBinding")


def test_registry_registers_exactly_one_observe_handler_and_binding():
    handlers = _handler_rows()
    assert "h-git-workflow-observe" in handlers
    row = handlers["h-git-workflow-observe"]
    assert row["kind"] == "engine"
    assert row["action"].strip("`") == "observe"
    assert row["mode"] == "non-blocking"
    assert row["behavior_owner"] == "scripts/python/git-workflow-observe.py"
    assert "observe" in probe_utils._engine_action_union(), \
        "the observe action must be a real engine action of a scanned sibling"

    rows = [b for b in _binding_rows()
            if b["handler_id"] == "h-git-workflow-observe"]
    assert len(rows) == 1, \
        f"exactly one observe binding must exist, got {rows}"
    assert rows[0]["selector"] == "@point:situation"
    assert rows[0]["scope"] == "all"


def test_registry_validation_and_wrap_up_face_stay_green():
    for args in (["--action", "handlers", "--validate"],
                 ["--action", "compile-embeds", "--check"],
                 ["--action", "probes", "--validate", "--reconcile"]):
        proc = subprocess.run([sys.executable, str(PROBE_UTILS), *args],
                              capture_output=True, text=True, check=False)
        assert proc.returncode == 0, f"{args}: {proc.stdout}{proc.stderr}"


def test_phase2_rows_do_not_change_the_wrap_up_registry_fingerprint():
    """The banner fingerprint covers the wrap-up projection only; the new
    situation rows must leave it unchanged (compile-embeds --check stays clean)."""
    text = REGISTRY.read_text(encoding="utf-8")
    handlers = probe_utils._table_rows(text, "Handler")
    bindings = probe_utils._table_rows(text, "HandlerBinding")
    wrap_bindings = [b for b in bindings if b["selector"] == "@point:wrap-up"]
    wrap_ids = {b["handler_id"] for b in wrap_bindings}
    fingerprint = probe_utils._fingerprint(
        [h for h in handlers if h["handler_id"] in wrap_ids], wrap_bindings)
    banner = (REPO_ROOT / "skills" / "external" / "git-utils" / "SKILL.md").read_text(
        encoding="utf-8")
    assert f"fingerprint: {fingerprint}" in banner, (
        "the compiled banner no longer matches the wrap-up registry projection — "
        "the new rows must not alter it")


def test_assess_dispatches_the_registered_situation_handler(tmp_path):
    """End-to-end: the situation engine's assess invokes the registered engine
    handler (runtime dispatch for the @point:situation subscription)."""
    ws = _repo(tmp_path / "ws")
    state = _state_file(ws)
    registry = ws / ".specify" / "shared" / "definitions" / "probe-definitions.md"
    registry.parent.mkdir(parents=True)
    shutil.copy2(REGISTRY, registry)
    owner = ws / ".specify" / "scripts" / "python" / "git-workflow-observe.py"
    owner.parent.mkdir(parents=True)
    shutil.copy2(ENGINE, owner)

    proc = subprocess.run(
        [sys.executable, str(TRIGGER), "--action", "assess",
         "--session", "shook", "--turn-id", "shook-01", "--compliance-done",
         "--stage", "non-feature", "--workspace", str(ws), "--format", "json"],
        capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert any("h-git-workflow-observe" in note and "ok" in note
               for note in env["notes"]), \
        f"assess did not dispatch the observe handler: {env['notes']}"
    assert OBS_START in state.read_text(encoding="utf-8"), \
        "the dispatched handler must have refreshed the observed section"
