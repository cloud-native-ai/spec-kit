"""Carrier contract for the three SDD-driving external skills.

Rule 1: no remote information -> local execution in the current project,
        via the orchestrator / host native subagent (never qodercli).
Rule 2: complete remote triple -> ssh (su) + cd + subagent CLI
        (default qodercli from the execution-config defaults layer).
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY = ROOT / "shared" / "workflow" / "execution-topology.md"
DISPATCH = ROOT / "shared" / "workflow" / "external-dispatch-recipes.md"
DEFAULTS = ROOT / "templates" / "execution-config-defaults.yaml"
SETUP = ROOT / "skills" / "external" / "sdd-project-setup" / "SKILL.md"
SETUP_RECIPES = ROOT / "skills" / "external" / "sdd-project-setup" / "references" / "setup-recipes.md"
HOUSE = ROOT / "skills" / "external" / "sdd-house-keeping" / "SKILL.md"
HOUSE_RECIPES = ROOT / "skills" / "external" / "sdd-house-keeping" / "references" / "maintenance-recipes.md"
LOOP = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
LOOP_RECIPES = ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
PREFLIGHT = ROOT / "skills" / "internal" / "run-agent" / "references" / "dispatch-preflight.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def test_shared_carrier_owner_has_both_rules():
    text = _read(TOPOLOGY)
    assert "## Carrier decision (local vs remote)" in text
    assert "No remote information" in text and "local" in text
    assert "current project" in text or "current working directory" in text
    assert "native subagent" in text
    assert "MUST NOT launch `qodercli`" in text
    assert "Complete remote triple" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    assert "cli: qodercli" in text


def test_execution_config_default_is_qodercli():
    text = _read(DEFAULTS)
    assert "cli: qodercli" in text


def test_sdd_skills_reference_the_carrier_owner():
    for path in (SETUP, HOUSE, LOOP):
        assert "execution-topology.md" in _read(path), (
            f"{path.name} must reference the carrier owner")


def test_setup_local_and_remote_shapes():
    text = _read(SETUP) + _read(SETUP_RECIPES)
    assert "当前项目" in text
    assert "原生子代理" in text
    assert "MUST NOT 启动 `qodercli`" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    assert "qodercli" in text


def test_house_keeping_local_and_remote_shapes():
    text = _read(HOUSE) + _read(HOUSE_RECIPES)
    assert "当前项目" in text
    assert "原生子代理" in text
    assert "MUST NOT 启动 `qodercli`" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    assert "qodercli" in text
    # H4 hook-health must be run on the target side, not against a remote path locally
    assert "hook-health.py" in text
    assert "ssh <alias>" in text


def test_loop_driver_local_native_and_remote_cli():
    text = _read(LOOP) + _read(LOOP_RECIPES)
    assert "会话 cwd" in text
    assert "向上搜索" in text
    assert "原生子代理" in text
    assert "MUST NOT 启动 qodercli" in text
    assert "SDD local default" in text
    assert "MUST NOT 以 `qodercli` 作为 SDD 缺省子代理" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "qodercli" in text
    preflight = _read(PREFLIGHT)
    assert "su - <run-user>" in preflight and "cd <project-dir>" in preflight


def test_shared_dispatch_doc_marks_local_variant_non_default():
    text = _read(DISPATCH)
    assert "SDD-driving skills boundary" in text
    assert "MUST NOT launch `qodercli` locally" in text
    assert "not the SDD local default" in text
