"""Structure contract for sdd-project-setup (bootstrap + handoff).

The skill was split: bootstrap stays here, periodic maintenance moved to
sdd-house-keeping. These pins protect that boundary rather than the old
S0–S5 all-in-one loop.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "external" / "sdd-project-setup"
SKILL_MD = SKILL_DIR / "SKILL.md"
RECIPES = SKILL_DIR / "references" / "setup-recipes.md"
DOCS = ROOT / "docs" / "reference" / "skills" / "sdd-project-setup.md"

pytestmark = pytest.mark.contract

PINNED_H2 = [
    "What This Skill Does",
    "When to Load",
    "The Loop (S0–S2 + HANDOFF)",
    "Hard Requirements",
    "Discipline Defaults",
    "References",
    "Subagent Delegation（子代理委派说明——2026-10-16 裁定）",
    "Boundary",
    "Wrap-up",
]

STAGE_CHAIN = ["S0 ENTRY", "S1 ASSESS", "S2 INSTALL", "S2.5 BOOTSTRAP",
               "HANDOFF      "]


def _skill() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _recipes() -> str:
    return RECIPES.read_text(encoding="utf-8")


def _frontmatter(text: str):
    assert text.startswith("---")
    end = text.find("\n---", 3)
    assert end != -1
    fields = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def _h2(text: str):
    return [line[3:].strip() for line in text.splitlines()
            if line.startswith("## ")]


# ---------------------------------------------------------------- C-1/C-2


def test_frontmatter_four_fields():
    fields = _frontmatter(_skill())
    assert set(fields) == {"name", "description", "skill_id", "classification"}
    assert fields["name"] == "sdd-project-setup"
    assert fields["skill_id"] == (
        "<SKILL:.specify/skills/sdd-project-setup/SKILL.md>")
    assert fields["classification"] == "external"
    assert "bootstrap" in fields["description"]
    assert "sdd-house-keeping" in fields["description"]


def test_classification_annotation_declares_three_skill_split():
    body = _skill().split("---", 2)[2]
    head = body[:1000]
    assert "依赖轴" in head and "external" in head
    assert "语义耦合" in head
    assert "sdd-house-keeping" in head and "sdd-loop-driver" in head
    assert "bootstrap" in head


# ---------------------------------------------------------------- C-3/C-4


def test_routing_skeleton():
    assert _h2(_skill()) == PINNED_H2


def test_loop_stage_chain_in_order():
    text = _skill()
    positions = [text.find(stage) for stage in STAGE_CHAIN]
    assert all(pos != -1 for pos in positions), (
        f"missing bootstrap stages: {positions}")
    assert positions == sorted(positions)
    recipes = _recipes()
    assert "S2.5 BOOTSTRAP CONTENT" in recipes
    assert "## HANDOFF" in recipes


def test_bootstrap_commands_and_handoff_owner():
    text = _skill() + _recipes()
    for command in ("/speckit.constitution", "/speckit.feature",
                    "/speckit.docs", "/speckit.goal"):
        assert command in text, f"bootstrap command missing: {command}"
    assert "sdd-house-keeping" in text
    assert "H0–H4" in text or "H1–H4" in text
    # sanitize is house-keeping's job, not setup's
    assert "MUST NOT 执行 `/speckit.sanitize`" in _skill()
    assert "retention apply" in _skill()


# ---------------------------------------------------------------- C-5


def test_mechanism_matrix_dimensions_pinned():
    text = _recipes()
    for key in ["const", "feat", "gloss", "fb", "reg", "kb", "session",
                "tools", "skills", "tmpl", "specs", "src", "compat"]:
        assert re.search(rf"\|\s*{key}\s*\|", text), (
            f"mechanism matrix dimension missing: {key}")


def test_grading_literature_pinned():
    text = _recipes()
    for grade in ["absent", "degraded", "partial", "complete"]:
        assert f"`{grade}`" in text
    assert "缺≠错" in text
    assert "未处理清单" in text


# ---------------------------------------------------------------- C-6/C-7


def test_hard_requirements_numbered_and_state_oracle():
    text = _skill()
    for n in range(1, 6):
        assert re.search(rf"^{n}\. \*\*", text, re.MULTILINE)
    assert "盘点先于处置" in text
    assert "就绪是三态判定" in text
    assert "bootstrap + 首次维护" in text


def test_suggestion_not_mandate_redline():
    text = _skill() + _recipes()
    assert "建议而非强制" in text
    assert "不携带任何「必须调用 sdd-loop-driver」的语义" in text


def test_no_sdd_stage_advancement_and_bootstrap_command_set():
    text = _skill()
    assert "不做任何 SDD 阶段推进" in text
    assert "constitution/feature/docs/goal/agents/team" in text


def test_setup_creates_specify_and_does_not_require_it():
    text = _skill() + _recipes()
    assert "不依赖 `.specify/`" in text
    assert "不向上搜索 `.specify/`" in text
    assert "由本 skill 创建/刷新" in text


def test_handoff_and_completion_contract():
    text = _skill()
    assert "bootstrap-complete / maintenance-pending" in text
    assert "ready" in text and "H4" in text
    assert "不得冒充 ready" in text or "不冒充 ready" in text


# ---------------------------------------------------------------- C-8/C-9


def test_handoff_twin_in_loop_driver():
    ld = (ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
          ).read_text(encoding="utf-8")
    assert "sdd-project-setup" in ld
    assert "sdd-house-keeping" in ld


def test_inventory_script_contract():
    text = (SKILL_DIR / "scripts" / "mechanism-inventory.py").read_text(
        encoding="utf-8")
    assert "--project" in text and "required=True" in text
    assert "--json" in text
    assert "return 2" in text
    assert not re.search(r"open\([^)]*['\"][wax]", text)
    assert not re.search(r"mkdir|makedirs|shutil|rmtree|unlink|remove\(", text)


# ---------------------------------------------------------------- C-10..C-15


def test_docs_page_bootstrap_and_handoff():
    text = DOCS.read_text(encoding="utf-8")
    assert "sdd-project-setup" in text
    assert "bootstrap" in text
    assert "S0–S2" in text
    assert "sdd-house-keeping" in text
    assert "软协同" in text
    assert "可移植" in text
    assert "边界" in text


def test_wrapup_compiled_block_present():
    text = _skill()
    assert "## Wrap-up" in text
    assert "AUTO-GENERATED by probe-utils.py" in text
    assert 'unit-id "skill:sdd-project-setup"' in text


def test_instruction_budget_and_hook_health_are_pointers():
    text = _skill() + _recipes()
    for literal in ("S3.4", "R3", "BUDGET", "placeholder=yes", "pending",
                    "S4-H", "hook-health.py", "vendor-managed"):
        assert literal in text, f"pointer literal missing: {literal}"
    docs = DOCS.read_text(encoding="utf-8")
    assert "预算" in docs and "R3" in docs
    assert "hook-health" in docs


def test_local_default_and_native_subagent():
    text = _skill()
    assert "S0 入口缺省解析" in text
    assert "当前项目" in text
    assert "原生子代理" in text
    assert "MUST NOT 启动 `qodercli`" in text
    recipes = _recipes()
    assert "本地拓扑" in recipes and "n/a" in recipes
    docs = DOCS.read_text(encoding="utf-8")
    assert "当前项目" in docs and "原生子代理" in docs
