"""Structure contract tests for the sdd-loop-driver skill (Feature 058).

One test per contract clause of
`.specify/specs/058-sdd-loop-driver/contracts/skill-structure.md`
(C-1..C-13) and `contracts/distribution-and-docs.md` (C-14..C-19),
following the per-clause test convention of test_run_skills_wiring.py.

Clauses are authored incrementally per user story; each story's tests go
red-first (notes/red-first-evidence.md records the red runs).
"""

import filecmp
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MD = SKILL_DIR / "SKILL.md"

PINNED_H2_SECTIONS = [
    "What This Skill Does",
    # 060 C-26: obligation moved to run-agent
    "Driver Topology（驱动拓扑——义务真源：run-agent 派发治理）",
    "When to Load",
    "The Loop (U0–U6)",
    "Hard Requirements",
    "Discipline Defaults",
    # 063 C-3 intentional update (2026-10-20): add the four efficiency
    # optimizations summary + owner pointer. The 064-owned
    # "CLI Capability Profiles" section below is unchanged and not copied.
    "Efficiency Optimizations（运行效率优化）",
    "References",
    "Boundary",
    "Subagent Create & Dispatch Delegation（子代理创建与派发委派）",  # 060 C-29: delegation section
    "Feedback & Probe Points（反馈与探针采集点）",  # 060: in-loop framework-feedback capture points
    "CLI Capability Profiles",  # 064: CLI behaviour knowledge entry
    "Wrap-up",  # compiled section (probe registry; AUTO-GENERATED)
]

CLI_PROFILE_RELS = [
    "references/cli/index.md",
    "references/cli/qodercli.md",
    "references/cli/claude.md",
    "references/cli/codex.md",
    "references/cli/opencode.md",
    "references/cli/hermes.md",
]


def _skill_text() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _parse_frontmatter(text: str):
    """Minimal frontmatter parser (no PyYAML per repo convention).

    Returns (fields: dict[str, str], body: str). Raises if no frontmatter.
    """
    if not text.startswith("---"):
        raise AssertionError("SKILL.md has no frontmatter block")
    end = text.find("\n---", 3)
    assert end != -1, "frontmatter block not closed"
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    fields = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        # YAML scalar semantics: surrounding quotes are part of the syntax,
        # not the value (precedent skills quote skill_id the same way).
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields, body


def _h2_sections(text: str) -> list:
    return [
        line[3:].strip()
        for line in text.splitlines()
        if line.startswith("## ")
    ]


# ---------------------------------------------------------------- C-1


def test_c1_frontmatter_four_fields():
    fields, _ = _parse_frontmatter(_skill_text())
    assert set(fields) == {
        "name",
        "description",
        "skill_id",
        "classification",
    }, f"frontmatter must carry exactly the four convention fields, got {sorted(fields)}"
    assert fields["name"] == "sdd-loop-driver"
    assert fields["description"], "description must be non-empty"
    assert "使用SDD开发模式" in fields["description"], (
        "description must carry the one-shot-entry trigger phrase"
    )
    assert "无人值守" in fields["description"]
    assert fields["skill_id"] == (
        "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"
    )
    assert fields["classification"] == "external"


# ---------------------------------------------------------------- C-2


def test_c2_classification_tension_annotation():
    _, body = _parse_frontmatter(_skill_text())
    head = body[:600]
    assert "依赖轴" in head, (
        "first body paragraph must state the dependency-axis ruling"
    )
    assert "external" in head
    assert "语义耦合" in head or "spec-kit SDD 流程" in head, (
        "annotation must declare the semantic coupling explicitly"
    )


# ---------------------------------------------------------------- C-3


def test_c3_skill_md_section_set():
    sections = _h2_sections(_skill_text())
    assert sections == PINNED_H2_SECTIONS, (
        f"H2 set must equal the pinned routing skeleton, got {sections}"
    )


# ---------------------------------------------------------------- US1 helpers

RECIPES_MD = SKILL_DIR / "references" / "dispatch-recipes.md"

STAGE_CHAIN = (
    "requirements → clarify → plan → tasks → checklist → analyze → implement → review"
)


def _recipes_text() -> str:
    return RECIPES_MD.read_text(encoding="utf-8")


# ---------------------------------------------------------------- C-4


def test_c4_dispatch_recipes_inline_five_mechanisms():
    text = _recipes_text()
    # 060 C-27: same-shape mechanics collapsed to references, deltas retained
    assert ".specify/shared/workflow/external-dispatch-recipes.md" in text, (
        "recipes truth-source reference missing (collapse)"
    )
    assert "dispatch-preflight.md" in text, "preflight reference missing (collapse)"
    # retained deltas: heartbeat mechanism + detached dispatch authority (H-04) + intervals
    assert "heartbeat" in text or "心跳" in text, "heartbeat delta must be retained"
    assert "nohup" in text, "nohup detached dispatch is the authority here (H-04 ruling)"
    assert "间隔" in text or "interval" in text
    # 063 C-4 intentional update (2026-10-20): the per-stage sed derivation
    # form is superseded by the parameterized stage-runner.sh (single testable
    # point, no per-stage copy drift). The old form is retained as a historical
    # note only; silently deleting the assertion is forbidden.
    assert "stage-runner.sh" in text, "runner derivation delta must be retained"
    # closure discipline (orchestration body, retained)
    assert "main" in text
    assert "收尾汇总" in text or "终态" in text


# ---------------------------------------------------------------- C-5


def test_c5_stage_chain_and_sentinel_literals():
    text = _recipes_text()
    assert STAGE_CHAIN in text, "stage chain literal must be inlined"
    assert "-DONE" in text
    assert "PLAN-DONE" in text
    assert "MERGE-DONE" not in text, (
        "clarify ruling: merge completion is git-state judged, no sentinel"
    )
    assert "git 状态判定" in text
    assert "集成分支" in text and "冲突" in text


# ---------------------------------------------------------------- C-6


def test_c6_visibility_contract_operative_rules():
    text = _recipes_text()
    assert "缓冲至退出" in text, (
        "the prohibited buffering-to-exit dispatch must be named"
    )
    assert "> agent.log 2>&1 &" in text, (
        "the concrete prohibited command shape must be shown"
    )
    assert "底稿" in text or "撰写底稿" in text, (
        "the framework truth source must be annotated as drafting basis only"
    )


# ---------------------------------------------------------------- US2 helpers

PROMPTS_MD = SKILL_DIR / "references" / "stage-prompts.md"

G5_DISCIPLINE_LINES = [
    "直接执行不要确认",
    "自行裁决并记录假设",
    "只提交本特性产物",
    "脏文件不提交不还原",
    "不要 push",
]


def _prompts_text() -> str:
    return PROMPTS_MD.read_text(encoding="utf-8")


# ---------------------------------------------------------------- C-7


def test_c7_g5_discipline_lines_inlined():
    text = _prompts_text()
    for line in G5_DISCIPLINE_LINES:
        assert line in text, f"G5 discipline line must be inlined verbatim: {line}"
    assert "不要 push" in text and "明确授权" in text


# ---------------------------------------------------------------- C-8


def test_c8_dispatch_injection_return_contract():
    text = _prompts_text() + _recipes_text()
    assert "显式异常行" in text, (
        "the return contract (sentinel OR explicit anomaly line) must be inlined"
    )
    assert "卡死信号" in text, (
        "neither sentinel nor anomaly line means a stall signal"
    )
    assert "fast-fail" in text or "快速失败" in text, (
        "the alignment source must be annotated (executor cannot resolve framework paths)"
    )


# ---------------------------------------------------------------- C-9


def test_c9_stall_handling_four_element_report_inlined():
    text = _prompts_text()
    for element in ["发现了什么", "为何吃重", "已产生的中间产物", "可选处置"]:
        assert element in text, f"escalation four-element missing: {element}"
    assert "静默等待" in text
    assert "静默修平" in text or "不静默修平" in text
    assert "先写状态后派发" in text or "先写状态" in text, (
        "state-spine write-before-dispatch program must be prescribed"
    )
    for point in ["U2", "U4", "U5"]:
        assert point in text, f"state-spine transition point {point} must be named"
    assert "90 分钟" in text and "2 次" in text, (
        "default timeout/retry values must be inlined with entry-override note"
    )


# ---------------------------------------------------------------- C-10


def test_c10_stage_prompts_all_sections_present():
    text = _prompts_text()
    # skeleton section complete
    for marker in ["第①段：背景与权威文档", "第②段：执行要求", "第③段：完成尾标与回传契约"]:
        assert marker in text, f"skeleton segment missing: {marker}"
    # variants section complete
    assert "本地拓扑" in text and "简报文件" in text
    assert "构建固化" in text
    # isolation section complete
    assert "并发隔离" in text and "窄读法授权" in text
    # stall/state-spine section complete (C-9 covers literals; here the section)
    assert "Stall Handling" in text and "状态脊" in text
    # no unfilled placeholders from incremental authoring remain
    assert "本章节由" not in text, "placeholder text from incremental authoring remains"


def test_c10_stage_prompts_sections_replace_placeholders():
    text = _prompts_text()
    for section in ["Stall Handling & State Spine", "Concurrency Isolation", "Variants"]:
        idx = text.find(f"## {section}")
        assert idx != -1, f"section missing: {section}"
        following = text[idx:text.find(
            "\n## ", idx + 4) if text.find("\n## ", idx + 4) != -1 else len(text)]
        assert "（本章节由" not in following, f"section {section} still carries a placeholder"


# ---------------------------------------------------------------- C-14 / C-15

DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"


def test_c14_docs_page_content_blocks():
    text = DOCS_PAGE.read_text(encoding="utf-8")
    assert "sdd-loop-driver" in text
    assert "双拓扑" in text and "入口参数" in text, (
        "docs page must carry the two-topology instantiation guide"
    )
    assert "可移植" in text and (".specify" in text), (
        "docs page must explain executor-side zero-dependency portability"
    )
    assert "投递" in text, (
        "docs page must list the three equivalent delivery forms"
    )
    assert "目标项目" in text, (
        "docs page must state that only the target project needs .specify/"
    )


def test_c15_docs_page_form_compliant():
    assert DOCS_PAGE.name == "sdd-loop-driver.md" and DOCS_PAGE.parent.name == "skills"
    text = DOCS_PAGE.read_text(encoding="utf-8")
    assert "运行时必读" not in text, (
        "docs page must not claim to be a runtime-required document"
    )


# ---------------------------------------------------------------- C-16


def test_c16_contract_test_file_complete():
    source = Path(__file__).read_text(encoding="utf-8")
    for i in range(1, 20):
        assert f"def test_c{i}_" in source, (
            f"clause C-{i} has no test function (contract: one test per clause)"
        )


# ---------------------------------------------------------------- C-17


def test_c17_roster_baseline_updated():
    wiring = (
        REPO_ROOT / "tests" / "contract" / "test_run_skills_wiring.py"
    ).read_text(encoding="utf-8")
    assert '"sdd-loop-driver"' in wiring, (
        "BASELINE_EXTERNAL roster must include sdd-loop-driver"
    )


# ---------------------------------------------------------------- C-18


def test_c18_mirror_pair_no_drift():
    src = SKILL_DIR
    dst = REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver"
    assert dst.exists(), "runtime mirror missing — sync-mirrors --write not run"
    for rel in [
        "SKILL.md", "references/dispatch-recipes.md", "references/stage-prompts.md",
        *CLI_PROFILE_RELS,
    ]:
        assert filecmp.cmp(src / rel, dst / rel, shallow=False), (
            f"mirror drift on {rel}"
        )


# ---------------------------------------------------------------- C-11 / C-12 / C-13
FEATURE_DELIVERABLE_PATHS = [
    "skills/external/sdd-loop-driver/SKILL.md",
    "skills/external/sdd-loop-driver/references/dispatch-recipes.md",
    "skills/external/sdd-loop-driver/references/stage-prompts.md",
    "docs/reference/skills/sdd-loop-driver.md",
    "tests/contract/test_sdd_loop_driver_skill.py",
]

ENGINE_PREFIXES = ("templates/", "src/", "scripts/")


def test_c11_self_containment_no_runtime_framework_reads():
    for rel in [
        "SKILL.md",
        "references/dispatch-recipes.md",
        "references/stage-prompts.md",
    ]:
        text = (SKILL_DIR / rel).read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if ".specify/" in line:
                context = line + "|" + \
                    text.splitlines()[lineno - 2] if lineno > 1 else line
                assert not re.search(r"MUST[^.]*\.specify/|必须先读|运行时必读", context), (
                    f"{rel}:{lineno} reads like a runtime obligation on a framework path"
                )


def test_c12_mirror_byte_identical():
    dst = REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver"
    assert dst.exists(), "runtime mirror missing"
    for rel in [
        "SKILL.md", "references/dispatch-recipes.md", "references/stage-prompts.md",
        *CLI_PROFILE_RELS,
    ]:
        assert (dst / rel).read_text(encoding="utf-8") == (SKILL_DIR / rel).read_text(
            encoding="utf-8"
        ), f"mirror not byte-identical: {rel}"


def test_c13_external_roster_and_directory():
    assert SKILL_DIR.is_dir() and (SKILL_DIR / "SKILL.md").exists()
    assert (SKILL_DIR / "references" / "dispatch-recipes.md").exists()
    assert (SKILL_DIR / "references" / "stage-prompts.md").exists()
    wiring = (
        REPO_ROOT / "tests" / "contract" / "test_run_skills_wiring.py"
    ).read_text(encoding="utf-8")
    assert '"sdd-loop-driver"' in wiring


# ---------------------------------------------------------------- C-19


def test_c19_feature_deliverables_never_touch_engine_dirs():
    for rel in FEATURE_DELIVERABLE_PATHS:
        assert not rel.startswith(ENGINE_PREFIXES), (
            f"feature deliverable intrudes into engine dirs: {rel}"
        )


# ---------------------------------------------------------------- C-14


def test_c14_preflight_checks_inlined():
    text = _recipes_text()
    # preflight section exists and precedes the breakpoint-probe recipe
    pre = text.find("前置检查")
    probe = text.find("Recipe 0")
    assert pre != -1 and probe != -1 and pre < probe, (
        "preflight section must exist before the breakpoint-probe recipe"
    )
    # 060 C-27: preflight ownership moved to run-agent — the section references it
    assert "dispatch-preflight.md" in text, "preflight authority reference missing"
    assert "ConnectTimeout" not in text, "five-family table still self-held (060 collapse violated)"
    assert "handoff" in text.lower(
    ) or "sdd-project-setup" in text, "⑤ handoff semantics must be stated"
    assert "状态脊" in text


# ---------------------------------------------------------------- C-20
# Driver Topology anti-nesting redline (defect fix 2026-10-16: a session
# fed the manual to a subagent, which spawned its own subagent — driver
# hierarchy escaped and the session's loop was silently bypassed).


def test_c20_driver_topology_redline_pinned():
    text = _skill_text()
    # 060 C-26: the obligation owner moved to run-agent; this file keeps the
    # driver-perspective self-check line and a reference to the authority
    assert "## Driver Topology（驱动拓扑——义务真源：run-agent 派发治理）" in text
    assert "加载本手册的宿主 agent 就是驱动者" in text
    assert "自检" in text, "loop-perspective self-check must be retained"
    assert "run-agent" in text, "authority reference missing"
    assert "MUST NOT 加载本手册" not in text, "owner literal still self-held (060 C-26 violated)"
    # the owner literal now lives in run-agent's governance section
    assert "反嵌套" in (REPO_ROOT / "skills" / "internal" /
                     "run-agent" / "SKILL.md").read_text(encoding="utf-8")
    # HR-6 carries the same rule in the Hard Requirements list
    hr6 = re.search(r"^6\. \*\*驱动拓扑\*\*.*$", text, re.MULTILINE)
    assert hr6, "Hard Requirement 6 (driver topology) missing"


# ---------------------------------------------------------------- routing guard
# 2026-10-19 defect: a feature description passed to /sdd-loop-driver was
# misrouted to improve-skills and edited the repo directly, skipping U0-U6.


def test_trigger_routing_guard_pinned():
    text = _skill_text()
    for needle in [
        "触发语义与路由",
        "主导流程唯一",
        "加载后的第一个动作",
        "流程不可替换",
        "U0.5 自检",
        "improve-skills",
        "create-skills",
        "只做技能维护",
        "当前工作目录含",
    ]:
        assert needle in text, f"trigger-routing guard missing: {needle}"
    docs = DOCS_PAGE.read_text(encoding="utf-8")
    assert "触发与路由" in docs
