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


# ================================================================ US2 (C-15..C-21)

RUN_AGENT_SKILL = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
PREFLIGHT = REPO_ROOT / "skills" / "internal" / "run-agent" / "references" / "dispatch-preflight.md"


def _run_agent_skill() -> str:
    return _read(RUN_AGENT_SKILL)


# ---------------------------------------------------------------- C-15


def test_c15_topology_input_forms():
    """Run Mode 增拓扑声明输入：本地/远端参数集 + 双形态 + 模板缺失快速失败。"""
    text = _run_agent_skill()
    assert "拓扑" in text, "topology declaration input missing from run-agent"
    assert "本地" in text and "远端" in text
    assert "内联" in text and "配置" in text, "dual input forms missing"
    assert "快速失败" in text and ("模板缺失" in text or "缺失" in text), (
        "template-missing fast-fail rule missing"
    )


# ---------------------------------------------------------------- C-16


def test_c16_conflict_rejection():
    """双形态冲突 → 解析期拒收并列冲突字段。"""
    text = _run_agent_skill()
    assert "拒收" in text
    assert "冲突字段" in text


# ---------------------------------------------------------------- C-17


def test_c17_dispatch_preflight_reference_file():
    """dispatch-preflight.md 承载五族前置检查表 + 失败处置链。"""
    assert PREFLIGHT.exists(), "references/dispatch-preflight.md missing"
    text = _read(PREFLIGHT)
    # five families, each with its decisive literal
    assert "ConnectTimeout" in text and "本地拓扑" in text          # ① ssh
    assert "id <run-user>" in text and "uid" in text                # ② run user
    assert "--version" in text                                       # ③ CLI
    assert "effort" in text and "context" in text.lower()           # ④ LLM config
    assert "source.json" in text and "constitution" in text         # ⑤ framework
    # handling chain
    assert "待补" in text or "待用户补充" in text                    # ④ uncertain
    assert "handoff" in text and "sdd-project-setup" in text        # ⑤ fail handoff
    assert "停线" in text or "上送" in text                          # ①②③ fail


# ---------------------------------------------------------------- C-18


def test_c18_preflight_wired_by_reference():
    """SKILL.md 以引用接线 preflight，不复制检查表正文。"""
    text = _run_agent_skill()
    assert "dispatch-preflight.md" in text, "preflight reference missing from SKILL.md"
    assert "ConnectTimeout" not in text, "five-family table copied into SKILL.md (C-18 violation)"


# ---------------------------------------------------------------- C-19


def test_c19_recipes_referenced_not_copied():
    """拓扑配方引用 [[STR-006]]，配方正文不复制。"""
    text = _run_agent_skill()
    assert "external-dispatch-recipes.md" in text, "recipes reference missing"
    assert "nohup" not in text, "recipe body copied into run-agent (C-19 violation)"


# ---------------------------------------------------------------- C-20


def test_c20_anti_nesting_in_run_agent():
    """反嵌套义务上收为公用派发义务：派发前拦截。"""
    text = _run_agent_skill()
    assert "反嵌套" in text or "嵌套" in text, "anti-nesting obligation missing"
    assert "循环层级" in text or "层级" in text
    assert "派发前" in text, "pre-dispatch interception must be named"


# ---------------------------------------------------------------- C-21


def test_c21_existing_rules_unchanged():
    """既有规则零改写：模态选择/可见性契约/注入子句/单代理边界全部在位。"""
    text = _run_agent_skill()
    assert "native" in text and "virtual" in text and "external" in text
    assert "Visibility Contract" in text
    assert "fast-fail injection" in text or "子代理派发注入" in text or "注入" in text
    assert "/speckit.team" in text, "single-agent boundary must remain"


# ================================================================ US3 (C-26..C-35)

LOOP_DRIVER_SKILL = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
LOOP_DRIVER_RECIPES = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
LOOP_DRIVER_PROMPTS = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "stage-prompts.md"
SETUP_RECIPES = REPO_ROOT / "skills" / "external" / "sdd-project-setup" / "references" / "setup-recipes.md"
SETUP_SKILL = REPO_ROOT / "skills" / "external" / "sdd-project-setup" / "SKILL.md"


# ---------------------------------------------------------------- C-26


def test_c26_driver_topology_referenced():
    """Driver Topology 改引用+自检行：义务本体移交 run-agent，循环视角自检保留。"""
    text = _read(LOOP_DRIVER_SKILL)
    assert "run-agent" in text, "delegation reference missing from Driver Topology"
    assert "自检" in text, "loop-perspective self-check line must be retained"
    assert "MUST NOT 加载本手册" not in text, (
        "obligation owner literal still in loop-driver (should have moved to run-agent)"
    )


# ---------------------------------------------------------------- C-27


def test_c27_preflight_and_recipes_collapsed():
    """dispatch-recipes：Preflight 清零引用、同型配方段坍缩引用、差异面保留。"""
    text = _read(LOOP_DRIVER_RECIPES)
    assert "ConnectTimeout" not in text, "five-family table still self-held (C-27 violation)"
    assert "dispatch-preflight.md" in text, "preflight reference missing"
    assert ".specify/shared/workflow/external-dispatch-recipes.md" in text, "recipes reference missing"
    assert "心跳" in text or "heartbeat" in text, "loop-driver-specific delta (heartbeat) must be retained"
    assert "阶段链" in text or "收尾" in text, "Recipe 4 stage-chain (orchestration body) must be retained"


# ---------------------------------------------------------------- C-28


def test_c28_skeleton_kept_mechanics_referenced():
    """stage-prompts：三段骨架内容保留，机制红线改引用。"""
    text = _read(LOOP_DRIVER_PROMPTS)
    for marker in ["第①段", "第②段", "第③段"]:
        assert marker in text, f"skeleton segment missing: {marker}"
    assert "run-agent" in text, "mechanism redline must reference run-agent obligation"
    assert "禁止引用 sdd-loop-driver" not in text, "owner literal still self-held (C-28 violation)"


# ---------------------------------------------------------------- C-29


def test_c29_orchestration_body_retained():
    """编排本体保留 + 委派说明段落位。"""
    skill = _read(LOOP_DRIVER_SKILL)
    for marker in ["状态脊", "哨兵", "卡死", "U0", "U6"]:
        assert marker in skill, f"orchestration body marker missing: {marker}"
    assert "create-agent" in skill, "delegation section must name create-agent"


# ---------------------------------------------------------------- C-30


def test_c30_setup_preflight_collapsed():
    """setup-recipes S4 五族检查表清零引用。"""
    text = _read(SETUP_RECIPES)
    assert "ConnectTimeout" not in text, "five-family table still self-held in setup-recipes"
    assert "dispatch-preflight.md" in text, "preflight reference missing"


# ---------------------------------------------------------------- C-31


def test_c31_remote_forms_referenced():
    """远端命令形态坍缩引用配方真源。"""
    text = _read(SETUP_RECIPES)
    assert ".specify/shared/workflow/external-dispatch-recipes.md" in text, "recipes reference missing"
    assert "nohup su -" not in text, "remote command form still self-held (C-31 violation)"


# ---------------------------------------------------------------- C-32


def test_c32_setup_delegation_section():
    """sdd-project-setup SKILL.md 委派说明段落位。"""
    text = _read(SETUP_SKILL)
    assert "run-agent" in text, "delegation section must name run-agent"
    assert "create-agent" in text or "盘点" in text


# ---------------------------------------------------------------- C-33


def test_c33_external_behavior_unchanged():
    """入口/frontmatter/probe 认领零变更。"""
    for path, name in [(LOOP_DRIVER_SKILL, "sdd-loop-driver"), (SETUP_SKILL, "sdd-project-setup")]:
        fm = _read(path).split("---")[1]
        assert f"name: {name}" in fm or f'name: "{name}"' in fm or name in fm, f"{name}: frontmatter name changed"
        assert "classification: external" in fm, f"{name}: classification changed"
        assert f"skill:sdd-{name.split('sdd-')[1]}" in fm or "skill_id" in fm, f"{name}: skill_id changed"
    team_md = REPO_ROOT / "templates" / "commands" / "team.md"
    assert team_md.exists(), "team command template missing (must remain untouched)"


# ---------------------------------------------------------------- C-34


def test_c34_skills_still_self_contained():
    """委派化后两技能自足可加载：引用 + 内联最小事实。"""
    skill = _read(LOOP_DRIVER_SKILL)
    assert "状态脊" in skill and "哨兵" in skill
    setup = _read(SETUP_RECIPES)
    assert "机制矩阵" in setup and "候选" in setup


# ---------------------------------------------------------------- C-35


def test_c35_parity_map_complete():
    """义务平价映射逐行填实：≥15 行且无空落点。"""
    parity = REPO_ROOT / ".specify" / "specs" / "060-decompose-subagent-dispatch" / "contracts" / "delegation-parity.md"
    text = _read(parity)
    rows = re.findall(r"^\| (P-\d{2}) \|(.+)$", text, re.MULTILINE)
    assert len(rows) >= 15, f"parity map has {len(rows)} rows, expected >=15"
    for pid, body in rows:
        cells = [c.strip() for c in body.split("|")]
        assert len(cells) >= 4 and all(cells[:4]), f"{pid}: empty 新落点/强度/追溯 cell"
