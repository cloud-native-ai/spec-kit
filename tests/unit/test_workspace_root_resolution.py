"""Regression tests for workspace-root resolution in the store engines.

Bug: when the agent's CWD sat inside a skill directory (e.g.
``.specify/skills/<name>/``), the engines fell back to bare CWD and created a
nested ``.specify/memory/`` store inside the skill dir, splitting project
state. The fix resolves the root by priority: explicit CLI arg > script
self-location (an engine installed under ``*/.specify/scripts/`` anchors its
parent project) > nearest CWD ancestor containing ``.specify/`` > CWD.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.script_api import feedback_utils, history_utils, memory_utils

ENGINES = [
    pytest.param(memory_utils, "resolve_workspace_root", id="memory-utils"),
    pytest.param(feedback_utils, "resolve_workspace_root", id="feedback-utils"),
    pytest.param(history_utils, "_project_root", id="history-utils"),
]


def _resolve(module, func_name: str, explicit):
    return getattr(module, func_name)(explicit)


@pytest.mark.parametrize("module,func_name", ENGINES)
def test_explicit_argument_always_wins(module, func_name, tmp_path: Path):
    target = tmp_path / "somewhere"
    target.mkdir()
    assert _resolve(module, func_name, str(target)) == target.resolve()


@pytest.mark.parametrize("module,func_name", ENGINES)
def test_self_location_anchors_parent_project(module, func_name, tmp_path: Path, monkeypatch):
    project = tmp_path / "proj"
    fake_engine = project / ".specify" / "scripts" / "python" / "eng.py"
    fake_engine.parent.mkdir(parents=True)
    fake_engine.write_text("# engine copy", encoding="utf-8")
    monkeypatch.setattr(module, "__file__", str(fake_engine))
    monkeypatch.chdir(tmp_path)  # CWD has no .specify anywhere
    assert _resolve(module, func_name, None) == project.resolve()


@pytest.mark.parametrize("module,func_name", ENGINES)
def test_self_location_outranks_stray_nested_specify(module, func_name, tmp_path: Path, monkeypatch):
    """The original bug: CWD inside a skill dir holding a stray nested
    ``.specify/`` must still resolve to the real project root."""
    project = tmp_path / "proj"
    fake_engine = project / ".specify" / "scripts" / "python" / "eng.py"
    fake_engine.parent.mkdir(parents=True)
    fake_engine.write_text("# engine copy", encoding="utf-8")
    stray = project / ".specify" / "skills" / "start-kind" / ".specify"
    stray.mkdir(parents=True)
    monkeypatch.setattr(module, "__file__", str(fake_engine))
    monkeypatch.chdir(project / ".specify" / "skills" / "start-kind")
    assert _resolve(module, func_name, None) == project.resolve()


@pytest.mark.parametrize("module,func_name", ENGINES)
def test_walk_up_finds_nearest_specify_ancestor(module, func_name, tmp_path: Path, monkeypatch):
    """Repo-root script copies (``scripts/python/``, no ``.specify`` in path)
    fall through to the CWD walk-up."""
    project = tmp_path / "proj"
    (project / ".specify").mkdir(parents=True)
    nested = project / "a" / "b"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    assert _resolve(module, func_name, None) == project.resolve()


@pytest.mark.parametrize("module,func_name", ENGINES)
def test_bare_cwd_is_last_resort(module, func_name, tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert _resolve(module, func_name, None) == tmp_path.resolve()
