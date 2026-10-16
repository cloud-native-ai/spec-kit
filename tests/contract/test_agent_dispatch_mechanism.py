"""Structure contract tests for the agent dispatch mechanism (Feature 060).

One test per contract clause, following the per-clause test convention of
test_sdd_loop_driver_skill.py (flat top-level functions, direct file reads).

Contract sources (clause ids are the machine-decidable C-N forms):
- contracts/concept-and-sources.md          (C-1..C-8)   — this file's tests
- contracts/skill-enhancements.md           (C-9..C-25)  — appended in US1/US2/US4/Polish phases
- contracts/delegation-parity.md            (C-26..C-35) — appended in US3 phase
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_DEFS = REPO_ROOT / "shared" / "definitions" / "agent-definitions.md"
SUBAGENT_DEFS = REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md"
RECIPES = REPO_ROOT / "shared" / "workflow" / "external-dispatch-recipes.md"

CLAUDE_FILES = ["AGENTS.md", "CLAUDE.md", "QODER.md", ".github/copilot-instructions.md"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _agent_defs() -> str:
    return _read(AGENT_DEFS)


def _subagent_defs() -> str:
    return _read(SUBAGENT_DEFS)


# ---------------------------------------------------------------- C-1


def test_c1_delegation_section_in_agent_definitions():
    """驱动子代理接线段：创建/派发/修正三技能接线 + 引用真源不复制。"""
    text = _agent_defs()
    assert "驱动子代理" in text, "delegation section missing from agent-definitions.md"
    # the three skill wirings are named
    assert "create-agent" in text and "run-agent" in text and "improve-agent" in text
    # references the truth sources instead of copying: both paths appear as references
    assert "subagent-definitions.md" in text
    assert "external-dispatch-recipes.md" in text
    # no recipe-body copy: the concrete dispatch command shape must not leak here
    assert "nohup" not in text, "recipe body copied into agent-definitions.md (C-1 violation)"


# ---------------------------------------------------------------- C-2


def test_c2_responsibility_divide_declared():
    """职责切分线：编排 = 驱动技能本体；创建/派发/修正 = 三技能承接面。"""
    text = _agent_defs()
    assert "职责切分线" in text
    assert "编排" in text and "承接" in text


# ---------------------------------------------------------------- C-3


def test_c3_no_third_owner_of_three_layers():
    """三层词条恰两处 owner：shared/definitions/ 下其他文件不得新增三层定义正文。"""
    owners = {"agent-definitions.md", "subagent-definitions.md"}
    defs_dir = REPO_ROOT / "shared" / "definitions"
    marker = "Agent Template → Agent Instance → Agent Execution"
    offenders = []
    for f in sorted(defs_dir.glob("*.md")):
        if f.name in owners:
            continue
        if marker in _read(f):
            offenders.append(f.name)
    assert not offenders, f"third owner of the three-layer taxonomy: {offenders}"


# ---------------------------------------------------------------- C-4


def test_c4_topology_declaration_section():
    """Execution 拓扑声明段：双拓扑要素表 + 双形态 + 冲突拒收。"""
    text = _subagent_defs()
    assert "拓扑声明" in text, "topology declaration section missing"
    # both topologies named
    assert "本地" in text and "远端" in text
    # dual input forms
    assert "内联" in text and "配置" in text
    # conflict rejection rule
    assert "拒收" in text and "冲突字段" in text


# ---------------------------------------------------------------- C-5


def test_c5_declaration_vs_recipe_division():
    """本段拥有"声明什么"，配方文档拥有"怎么执行"；分歧契约赢。"""
    text = _subagent_defs()
    assert "external-dispatch-recipes.md" in text, "recipes division-of-labor reference missing"
    assert "契约" in text


# ---------------------------------------------------------------- C-6


def test_c6_anti_nesting_referenced_in_governance():
    """派发时治理义务节含反嵌套引用（指向 run-agent），原文语义不被改写。"""
    text = _subagent_defs()
    gov = text[text.find("Dispatch-Time Governance Obligation"):]
    assert "反嵌套" in gov or "嵌套" in gov, "anti-nesting reference missing in governance section"
    assert "run-agent" in gov


# ---------------------------------------------------------------- C-7


def test_c7_layer_boundary_rules_present():
    """层界三行判定：Template=能力面 / Instance=职责绑定 / Execution=运行拓扑。"""
    text = _agent_defs()
    assert re.search(r"Template[^\n]*能力", text), "Template layer rule missing"
    assert re.search(r"Instance[^\n]*职责", text), "Instance layer rule missing"
    assert re.search(r"Execution[^\n]*拓扑", text), "Execution layer rule missing"


# ---------------------------------------------------------------- C-8


def test_c8_cross_layer_change_ban():
    """越层禁令：改能力不改拓扑、改拓扑不改能力。"""
    text = _agent_defs()
    assert "改能力" in text and "拓扑" in text, "cross-layer change ban missing"
