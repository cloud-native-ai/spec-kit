"""Contract tests for the sdd-loop-driver deterministic gates (§5–§7).

Pins the three gate scripts, their ceiling/exit-code interface, the owner doc
sections, and the stage-prompt wiring. Behaviour is covered by the unit tests;
this file stops the interface and the wiring from drifting silently.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SCRIPTS = SKILL_DIR / "scripts"
EFFICIENCY = SKILL_DIR / "references" / "efficiency-model.md"
STAGE_PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
SKILL = SKILL_DIR / "SKILL.md"

GATES = {
    "decomposition-check.py": ("--mode", "--requirements", "--tasks"),
    "pre-analyze-check.py": ("--spec-dir", "--stage", "--repo", "--strict", "--waive"),
    "overlap-check.py": ("--spec-dir", "--specs-root", "--repo"),
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _constant(source: str, name: str) -> int:
    match = re.search(r"^%s = ([0-9]+)$" % name, source, re.MULTILINE)
    assert match, "constant %s not found" % name
    return int(match.group(1))


@pytest.mark.contract
def test_gate_scripts_exist_and_expose_interface():
    for name, flags in GATES.items():
        path = SCRIPTS / name
        assert path.is_file(), "missing gate script: %s" % name
        source = _text(path)
        for flag in flags:
            assert flag in source, "%s lacks %s" % (name, flag)
        completed = subprocess.run([sys.executable, str(path), "--help"],
                                   capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr
        for flag in flags:
            assert flag in completed.stdout


@pytest.mark.contract
def test_exit_codes_are_documented():
    for name in GATES:
        source = _text(SCRIPTS / name)
        for code in ("0 =", "1 =", "2 ="):
            assert code in source, "%s does not document exit %s" % (name, code)


@pytest.mark.contract
def test_decomposition_ceilings_match_fast_lane_limits():
    admission = _text(SCRIPTS / "admission-check.py")
    decomposition = _text(SCRIPTS / "decomposition-check.py")
    assert _constant(decomposition, "FR_CEILING") == _constant(admission, "FR_MAX") == 30
    assert _constant(decomposition, "TASK_CEILING") == _constant(admission, "TASK_MAX") == 40


@pytest.mark.contract
def test_owner_document_has_the_three_sections():
    efficiency = _text(EFFICIENCY)
    for marker in ("大特性拆分门", "确定性预检", "跨特性重叠预检"):
        assert marker in efficiency, "owner doc lacks %s" % marker
    for script in GATES:
        assert script in efficiency, "owner doc does not name %s" % script
    for heading in ("## 5.", "## 6.", "## 7."):
        assert heading in efficiency, "owner doc lacks section %s" % heading


@pytest.mark.contract
def test_skill_lists_the_three_gates():
    skill = _text(SKILL)
    for marker in ("大特性拆分门", "确定性预检", "跨特性重叠预检"):
        assert marker in skill, "SKILL.md does not list %s" % marker
    for script in GATES:
        assert script in skill, "SKILL.md does not name %s" % script


@pytest.mark.contract
def test_stage_prompts_wire_every_decision_point():
    prompts = _text(STAGE_PROMPTS)
    assert "Deterministic Gates" in prompts
    for script in GATES:
        assert script in prompts, "stage prompts do not run %s" % script
    for decision in ("clarify U4", "requirements U4", "plan U4", "tasks U4"):
        assert decision in prompts, "stage prompts lack %s" % decision
    assert "不得派发 analyze" in prompts
    assert "不得派发 plan" in prompts


@pytest.mark.contract
def test_gate_scripts_are_stdlib_only():
    stdlib = {
        "argparse", "json", "os", "re", "sys", "time", "pathlib",
        "subprocess", "shutil", "collections", "datetime", "glob",
    }
    for name in GATES:
        source = _text(SCRIPTS / name)
        for module in re.findall(r"^(?:import|from)\s+([A-Za-z_][\w.]*)",
                                 source, re.MULTILINE):
            assert module.split(".", 1)[0] in stdlib, (
                "%s imports non-stdlib module %s" % (name, module))
        assert "specify_cli" not in source
        assert ".specify/scripts" not in source
