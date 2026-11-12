"""G-2 (T063) — the Goal command surface refuses the four Anchor-only modes.

The executable subject is the engine's read-only action
`goal-utils.py command-mode --command goal --mode <mode>`, driven here as a real subprocess
(that is what a consumer sees). Red conditions: an Anchor-only mode is accepted by the Goal
surface, the refusal loses the `anchor-only-mode` literal or the `/speckit.anchor` pointer, or
the engine no longer publishes the action at all.

The store digest comparison wraps every call: a refusal that wrote anything would show up here
even if its exit code were right.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
ENGINE = ROOT / "scripts/python/goal-utils.py"
TEMPLATE = ROOT / "templates/commands/goal.md"

GOAL_MODES = ("create", "view", "modify", "status")
ANCHOR_ONLY_MODES = ("targets", "migrate", "migrate-archive", "coordinate")
REFUSAL_LITERAL = "anchor-only-mode"
REFUSAL_POINTER = "/speckit.anchor"
STORE_DIRS = (".specify/anchoring", ".specify/goals", ".specify/teams")


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        capture_output=True, text=True, cwd=str(ROOT), check=False)


def _store_manifest() -> dict[str, str]:
    manifest: dict[str, str] = {}
    for rel in STORE_DIRS:
        base = ROOT / rel
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in {"runs", "__pycache__"} for part in path.relative_to(ROOT).parts):
                continue
            manifest[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


def _help_lists(engine: Path, action: str) -> bool:
    result = subprocess.run([sys.executable, str(engine), "--help"],
                            capture_output=True, text=True, check=False)
    return action in (result.stdout or "") + (result.stderr or "")


def refusal_problems(template_text: str) -> list[str]:
    """Ways the template stops naming the refusal contract for a mode."""
    problems = []
    for mode in ANCHOR_ONLY_MODES:
        if f"`{mode}`" not in template_text:
            problems.append(f"template does not name {mode} as refused")
    for token in (REFUSAL_LITERAL, REFUSAL_POINTER, "exit 2"):
        if token not in template_text:
            problems.append(f"template lost the refusal token {token!r}")
    return problems


def test_goal_hint_declares_the_four_goal_modes() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    hint = next(line for line in text.splitlines() if line.startswith("argument-hint:"))
    modes = [part.strip() for part in hint.split("[", 1)[1].split("]", 1)[0].split("|")]
    assert sorted(modes) == sorted(GOAL_MODES), modes


def test_anchor_only_modes_are_refused_by_the_subprocess_action() -> None:
    for mode in ANCHOR_ONLY_MODES:
        result = _run("command-mode", "--command", "goal", "--mode", mode, "--json")
        assert result.returncode == 2, f"{mode}: expected exit 2, got {result.returncode}"
        assert REFUSAL_LITERAL in result.stderr, f"{mode}: stderr lost {REFUSAL_LITERAL}: {result.stderr}"
        assert REFUSAL_POINTER in result.stderr, f"{mode}: stderr lost {REFUSAL_POINTER}: {result.stderr}"
        payload = json.loads(result.stdout)
        assert payload["verdict"] == REFUSAL_LITERAL, payload
        assert payload["mode"] == mode


def test_goal_modes_exit_zero_and_the_anchor_side_covers_seven() -> None:
    for mode in GOAL_MODES:
        result = _run("command-mode", "--command", "goal", "--mode", mode, "--json")
        assert result.returncode == 0, f"{mode}: {result.stderr}"
        assert json.loads(result.stdout)["verdict"] == "ok"
    for mode in (*GOAL_MODES[:3], *ANCHOR_ONLY_MODES):
        result = _run("command-mode", "--command", "anchor", "--mode", mode, "--json")
        assert result.returncode == 0, f"anchor/{mode}: {result.stderr}"
        assert json.loads(result.stdout)["verdict"] == "ok"


def test_every_call_leaves_the_definition_stores_byte_identical() -> None:
    before = _store_manifest()
    for mode in (*GOAL_MODES, *ANCHOR_ONLY_MODES):
        _run("command-mode", "--command", "goal", "--mode", mode, "--json")
    after = _store_manifest()
    changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    assert not changed, f"a read-only refusal changed the stores: {changed}"


def test_engine_publishes_the_command_mode_action() -> None:
    assert _help_lists(ENGINE, "command-mode"), "the engine no longer publishes command-mode"


def test_template_names_each_refused_mode() -> None:
    problems = refusal_problems(TEMPLATE.read_text(encoding="utf-8"))
    assert not problems, problems


def test_injection_template_accepting_a_mode_is_red() -> None:
    text = TEMPLATE.read_text(encoding="utf-8").replace("`coordinate`", "")
    problems = refusal_problems(text)
    assert problems == ["template does not name coordinate as refused"]


def test_injection_missing_engine_action_is_red(tmp_path: Path) -> None:
    stub = tmp_path / "stub-engine.py"
    stub.write_text("print('usage: stub-engine.py {list,validate}')\n", encoding="utf-8")
    assert not _help_lists(stub, "command-mode")
    assert _help_lists(ENGINE, "command-mode")
