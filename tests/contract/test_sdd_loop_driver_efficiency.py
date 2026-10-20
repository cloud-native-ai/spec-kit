"""Contract tests for Feature 063 efficiency clauses.

One named test function per clause:
  FL-01…FL-10 (fast lane), TB-01…TB-10 (test budget),
  PC-01…PC-11 (plan constraint), PD-01…PD-10 (progress decoupling),
  DI-01…DI-09 (delivery and invariants).

The file is authored incrementally per user story; each story's tests go
red-first. The T046 coverage meta-test asserts that every clause id in
``contracts/*.md`` has its named function.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
EFFICIENCY = SKILL_DIR / "references" / "efficiency-model.md"
RECIPES = SKILL_DIR / "references" / "dispatch-recipes.md"
PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
WATCH = SKILL_DIR / "references" / "watch-model.md"
SKILL_MD = SKILL_DIR / "SKILL.md"
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "063-sdd-loop-efficiency"
REQUIREMENTS = SPEC_DIR / "requirements.md"
CONTRACTS = SPEC_DIR / "contracts"


def _text(path):
    assert path.exists(), "missing required file: %s" % path
    return path.read_text(encoding="utf-8")


def _run(args):
    return subprocess.run(
        [sys.executable] + [str(item) for item in args],
        capture_output=True, text=True,
    )


def _script_help(name):
    completed = _run([SKILL_DIR / "scripts" / name, "--help"])
    assert completed.returncode == 0, completed.stderr
    return completed.stdout + completed.stderr


# ------------------------------------------------------------------ FL-01


def test_fl_01_opt_in_literal_pinned():
    text = _text(EFFICIENCY)
    assert "fast-lane=opt-in" in text
    assert "唯一" in text and "启用" in text
    assert "无人值守" in text
    assert "自然语言" in text


# ------------------------------------------------------------------ FL-02


def test_fl_02_admission_point_and_sequence_policy():
    recipes = _text(RECIPES)
    assert "tasks" in recipes and "checklist" in recipes
    assert "admission-check.py" in recipes
    assert "快车道保留 analyze" in recipes or ("保留" in recipes and "analyze" in recipes)
    efficiency = _text(EFFICIENCY)
    assert "tasks.md" in efficiency and "checklist" in efficiency
    assert "analyze" in efficiency and "review" in efficiency


# ------------------------------------------------------------------ FL-03


def test_fl_03_criteria_table_pinned():
    efficiency = _text(EFFICIENCY)
    for criterion in "abcdefg":
        assert re.search(r"\|\s*\(%s\)" % criterion, efficiency), (
            "criterion (%s) missing from the owner table" % criterion)
    requirements = _text(REQUIREMENTS)
    assert "`^- **FR-[0-9]{3}**:`" in requirements
    assert "`^- \\[[ xX]\\] T[0-9]{3}`" in requirements
    assert "`^- \\[[ xX>~]\\] T[0-9]{3}`" in requirements
    source = _text(SKILL_DIR / "scripts" / "admission-check.py")
    assert "FR_MIN = 8" in source and "FR_MAX = 30" in source
    assert "TASK_MIN = 10" in source and "TASK_MAX = 40" in source
    assert "数据模型" in efficiency or "lines.manifest" in efficiency


# ------------------------------------------------------------------ FL-04


def test_fl_04_admission_record_fields():
    efficiency = _text(EFFICIENCY)
    for field in ("decision", "entry_evidence", "criteria", "measured",
                  "decided_at", "reversion"):
        assert field in efficiency, "admission record field missing: %s" % field
    assert "checklist=skipped(fast-lane)" in efficiency
    data_model = _text(SPEC_DIR / "data-model.md")
    assert "E1 — Fast-Lane Admission Record" in data_model


# ------------------------------------------------------------------ FL-05


def test_fl_05_downstream_publication():
    prompts = _text(PROMPTS)
    assert "checklist=skipped(fast-lane)" in prompts
    assert "admission" in prompts.lower() or "准入" in prompts
    assert "implement" in prompts and "review" in prompts
    efficiency = _text(EFFICIENCY)
    assert "下游" in efficiency and "发布" in efficiency


# ------------------------------------------------------------------ FL-06


def test_fl_06_reversion_procedure():
    efficiency = _text(EFFICIENCY)
    assert "回退" in efficiency
    assert "checklist" in efficiency
    assert "analyze" in efficiency
    assert "证据" in efficiency
    recipes = _text(RECIPES)
    assert "回退" in recipes


# ------------------------------------------------------------------ FL-07


def test_fl_07_analyze_review_unchanged():
    efficiency = _text(EFFICIENCY)
    assert "CRITICAL" in efficiency and "HIGH" in efficiency
    assert "有界回环" in efficiency or "一轮" in efficiency
    assert "review" in efficiency
    assert "不削弱" in efficiency or "不变" in efficiency


# ------------------------------------------------------------------ FL-08


def test_fl_08_admission_script_interface():
    help_text = _script_help("admission-check.py")
    for flag in ("--project", "--base-ref", "--requirements", "--tasks",
                 "--checklists", "--entry-evidence", "--lines-manifest",
                 "--expected-branch"):
        assert flag in help_text, "admission-check flag missing: %s" % flag
    source = _text(SKILL_DIR / "scripts" / "admission-check.py")
    assert "admissible" in source and "rejected" in source and "input" in source
    assert "standard library" in source.lower() or "stdlib" in source
    imports = re.findall(r"^import\s+([A-Za-z_][A-Za-z0-9_]*)", source, re.MULTILINE)
    allowed = {"argparse", "json", "os", "re", "subprocess", "sys", "time", "pathlib"}
    assert set(imports) <= allowed, "unexpected import: %s" % (set(imports) - allowed)
    assert ".specify/scripts" not in source


# ------------------------------------------------------------------ FL-09


def test_fl_09_definition_owned_and_pinned():
    efficiency = _text(EFFICIENCY)
    assert "唯一 owner" in efficiency or "唯一owner" in efficiency
    assert "快车道" in efficiency
    assert "tests/contract/test_sdd_loop_driver_efficiency.py" in efficiency
    assert (SKILL_DIR / "scripts" / "admission-check.py").exists()


# ------------------------------------------------------------------ FL-10


def test_fl_10_self_application_exclusion():
    requirements = _text(REQUIREMENTS)
    assert "**FR-010**" in requirements
    assert "完整阶段链" in requirements
    efficiency = _text(EFFICIENCY)
    assert "063" in efficiency and "完整阶段链" in efficiency
    assert "MUST NOT" in efficiency
    feature_ref = _text(SPEC_DIR / "feature-ref.md")
    assert "自应用" in feature_ref
