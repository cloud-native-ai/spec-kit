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


# ================================================================ US1 (C-9..C-14)

EXECUTOR = REPO_ROOT / "agents" / "sdd-executor.agent.md"
EXECUTOR_MIRROR = REPO_ROOT / ".specify" / "agents" / "templates" / "sdd-executor.agent.md"
CREATE_AGENT_SKILL = REPO_ROOT / "skills" / "internal" / "create-agent" / "SKILL.md"

EXPECTED_EXECUTOR_FRONTMATTER = [
    "name", "description", "user-invocable", "model-tier",
    "capability-tools", "skills", "run-turn-budget",
]


def _executor_text() -> str:
    return _read(EXECUTOR)


def _create_agent_skill() -> str:
    return _read(CREATE_AGENT_SKILL)


# ---------------------------------------------------------------- C-9


def test_c9_sdd_executor_template_valid():
    """sdd-executor 模板合法：词表字段齐 + 三要素能力面 + 职责字样零命中。"""
    assert EXECUTOR.exists(), "agents/sdd-executor.agent.md missing"
    text = _executor_text()
    fm = text.split("---")[1]
    for field in EXPECTED_EXECUTOR_FRONTMATTER:
        assert re.search(rf"^{field}:", fm, re.MULTILINE), f"frontmatter field missing: {field}"
    assert "user-invocable: false" in fm, "executor is dispatch-delegated, not user-invocable"
    # capability face: project dir / project context / SDD stage commands
    assert "项目目录" in text or "project directory" in text
    assert "上下文" in text or "context" in text.lower()
    assert "/speckit." in text
    # duty-agnostic: no per-duty binding words in the whole template
    assert not re.search(r"\b(setup|requirements)\b", text, re.IGNORECASE), (
        "duty words (setup/requirements) leaked into the capability template"
    )


# ---------------------------------------------------------------- C-10


def test_c10_content_criterion_mechanical():
    """内容判据机械面：无用户名/IP/家目录/内网段字面量。"""
    text = _executor_text()
    patterns = [
        r"([0-9]{1,3}\.){3}[0-9]{1,3}",  # IPv4
        r"/Users/[a-z]",                  # macOS home
        r"/home/[a-z]",                   # linux home
    ]
    for pat in patterns:
        assert not re.search(pat, text), f"special-info literal matched: {pat}"


# ---------------------------------------------------------------- C-11


def test_c11_distribution_criterion_in_create_agent():
    """create-agent 载入分发层内容判据 + sdd-executor 首次应用结论。"""
    text = _create_agent_skill()
    assert "分发层" in text, "distribution-layer criterion missing"
    assert "专用信息" in text, "the special-info condition must be stated"
    assert "框架分发角色集" in text or "框架分发" in text
    assert "项目侧" in text
    assert "sdd-executor" in text, "first-application conclusion missing"


# ---------------------------------------------------------------- C-12


def test_c12_multi_duty_instantiation():
    """多职责实例化：capacity-scope 引用 + 一实例一职责 + team-scope 互斥。"""
    text = _create_agent_skill()
    assert "capacity-scope" in text
    assert "一实例一职责" in text or "single duty" in text
    assert "team-scope" in text, "mutual exclusion with team-scope must be stated"


# ---------------------------------------------------------------- C-13


def test_c13_retire_lifecycle_in_create_agent():
    """Agent Lifecycle 节退役规则：retired 标记保留 + 先解引用。"""
    text = _create_agent_skill()
    assert "retired" in text, "retire lifecycle missing from Agent Lifecycle"
    assert "解引用" in text or "dereference" in text.lower()
    assert re.search(r"retire", text, re.IGNORECASE)


# ---------------------------------------------------------------- C-14


def test_c14_mirror_pair_byte_identical():
    """agents/ ↔ .specify/agents/templates/ 镜像对字节一致。"""
    assert EXECUTOR_MIRROR.exists(), "runtime mirror missing — sync-mirrors not run"
    assert EXECUTOR.read_bytes() == EXECUTOR_MIRROR.read_bytes(), (
        "agents/sdd-executor.agent.md mirror drift"
    )
