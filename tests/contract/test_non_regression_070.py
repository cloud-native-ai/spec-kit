"""Non-regression net for Feature 070 (T033; FN-09…FN-13, FN-16 guard).

The 070 layer adds pre-U4 steps only. This file pins the preserved owners it
must not redefine — 058 sentinels/U4/stage chain, 063 efficiency literals,
064 registry/ownership/worktree/integration interfaces, 067 part brief and
dispatch-log fields, and 068's channel boundary — and the two single-owner
inventories the 070 design artifacts must reference instead of restating.

This is a regression net over behavior that already exists, not new behavior;
it makes no red-first claim (tasks.md § Tests: migration/regression exception).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MD = DRIVER / "SKILL.md"
DISPATCH_RECIPES = DRIVER / "references" / "dispatch-recipes.md"
STAGE_PROMPTS = DRIVER / "references" / "stage-prompts.md"
EFFICIENCY_MODEL = DRIVER / "references" / "efficiency-model.md"
MODEL_DOC = DRIVER / "references" / "decomposition-model.md"
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"

SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "070-subagent-task-teams"
PLAN_MD = SPEC_DIR / "plan.md"
DATA_MODEL_MD = SPEC_DIR / "data-model.md"
FEATURE_REF_MD = SPEC_DIR / "feature-ref.md"
RESEARCH_MD = SPEC_DIR / "research.md"
TASKS_MD = SPEC_DIR / "tasks.md"
WP_MODEL_CONTRACT = SPEC_DIR / "contracts" / "work-package-model.md"

FEATURE_067_REQUIREMENTS = (
    REPO_ROOT
    / ".specify"
    / "specs"
    / "067-loop-efficiency-hardening"
    / "requirements.md"
)
FEATURE_068_REQUIREMENTS = (
    REPO_ROOT
    / ".specify"
    / "specs"
    / "068-exec-quant-feedback-channel"
    / "requirements.md"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _require(text: str, *needles: str) -> None:
    for needle in needles:
        assert needle in text, "owner literal missing: %s" % needle


def _h2_sections(text: str) -> list:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


# ---------------------------------------------------------------- FN-09 / 058


def test_058_sentinels_u4_and_stage_chain_are_unchanged():
    """FN-09: the sentinel/U4/stage-chain obligations of 058 still hold."""
    recipes = _read(DISPATCH_RECIPES)
    _require(
        recipes,
        "requirements → clarify → plan → tasks → checklist → analyze → implement → review",
        "PLAN-DONE",
        "git 状态判定",
    )
    assert "MERGE-DONE" not in recipes, "058 ruling: merge completion is git-state judged"
    prompts = _read(STAGE_PROMPTS)
    _require(prompts, "U4", "独立校验", "哨兵")
    skill = _read(SKILL_MD)
    _require(skill, "U4 VERIFY", "独立校验", "状态脊")


# ---------------------------------------------------------------- FN-10 / 063


def test_063_fast_lane_budget_plan_fix_and_detach_literals_are_unchanged():
    """FN-10: the 063 efficiency owner keeps every literal 070 must preserve."""
    model = _read(EFFICIENCY_MODEL)
    _require(
        model,
        "fast-lane=opt-in",
        "两槽位测试预算",
        "PLAN-EDIT:",
        "nohup",
        "targeted-set-v1",
    )
    skill = _read(SKILL_MD)
    _require(skill, "快车道", "两槽位测试预算", "Plan 只小修", "进度与脱离")
    runtime = _read(MODEL_DOC)
    _require(runtime, "two-slot test budget", "plan minor-fix constraint", "the fast lane")


# ---------------------------------------------------------------- FN-11 / 064


def test_064_registry_ownership_worktree_and_integration_interfaces_are_unchanged():
    """FN-11: 064's registry/ownership/worktree/integration surfaces stay the owners."""
    recipes = _read(DISPATCH_RECIPES)
    _require(
        recipes,
        "line-registry.py",
        "Ownership Manifest",
        "integration-plan",
        "integrate-lines.py",
    )
    skill = _read(SKILL_MD)
    _require(skill, "worktree-per-write-line", "Ownership Manifest", "确定性集成队列")
    runtime = _read(MODEL_DOC)
    _require(runtime, "Feature 064's registry/ownership/worktree/integration semantics")


# ---------------------------------------------------------------- FN-12 / 067


def test_067_part_brief_and_dispatch_log_fields_are_unchanged():
    """FN-12: the 067 part brief and dispatch-log fields are extended, not replaced."""
    requirements = _read(FEATURE_067_REQUIREMENTS)
    _require(
        requirements,
        "part brief",
        "run-turn-budget",
        "dispatch log",
        "not_evaluated",
    )
    # FR-001 owns the brief fields; FR-007 owns the dispatch-log fields.
    fr_001 = next(
        line for line in requirements.splitlines() if line.startswith("- **FR-001**")
    )
    fr_007 = next(
        line for line in requirements.splitlines() if line.startswith("- **FR-007**")
    )
    _require(fr_001, "任务 ID", "允许修改的文件", "目标测试命令/node id", "禁改文件")
    _require(fr_007, "part ID", "task IDs", "turn", "测试 pass/fail 增量", "commit", "outcome")

    contract = _read(WP_MODEL_CONTRACT)
    _require(
        contract,
        "part_id",
        "task_ids[]",
        "test_delta{passed,failed,new_failures[]}",
        "duration_seconds",
        "token_cost",
        "one brief format and one dispatch log",
    )
    runtime = _read(MODEL_DOC)
    _require(runtime, "part_id", "task_ids", "test_delta", "part-commit discipline")


# ---------------------------------------------------------------- FN-13 / 068


def test_068_channel_boundary_is_unchanged():
    """FN-13: 068's channel keeps zero automatic transmission and its store split."""
    requirements = _read(FEATURE_068_REQUIREMENTS)
    _require(requirements, "零自动传输", "feedback store", "手动", "非阻塞")
    skill = _read(SKILL_MD)
    _require(skill, "不自动上送", "feedback-utils.py", "exec-quant.py")
    runtime = _read(MODEL_DOC)
    _require(runtime, "Feature 068's feedback channel")


# ---------------------------------------------------------------- owner agreement


def _mirror_pair_rows(text: str) -> list:
    """Rows that pair a driver source with its generated mirror path."""
    return [
        line
        for line in text.splitlines()
        if line.startswith("| `skills/external/sdd-loop-driver/")
        and "`.specify/skills/sdd-loop-driver/" in line
    ]


def test_mirror_obligations_have_exactly_one_owner():
    """plan.md § Mirror Obligations owns the only complete mirror table."""
    plan = _read(PLAN_MD)
    _require(
        plan,
        "### Mirror Obligations",
        "**Owner declaration**: this section is the sole owner of the mirror "
        "source/mirror/verify obligations for this feature.",
        "| Source file (edited) | Mirror / generated copies (must land identically) | Verify |",
    )
    mirror_rows = _mirror_pair_rows(plan)
    assert len(mirror_rows) == 5, (
        "plan.md § Mirror Obligations must own the five source/mirror/verify rows, "
        "got %d" % len(mirror_rows)
    )
    for other, label in (
        (FEATURE_REF_MD, "feature-ref.md"),
        (RESEARCH_MD, "research.md"),
        (MODEL_DOC, "decomposition-model.md"),
    ):
        text = _read(other)
        assert "| Source file (edited) |" not in text, (
            "%s restates the mirror table; it must point to plan.md" % label
        )
        assert not _mirror_pair_rows(text), "%s restates the mirror rows" % label

    feature_ref = _read(FEATURE_REF_MD)
    _require(
        feature_ref,
        "**Pointer only**",
        "`plan.md` § Mirror Obligations",
        "records no separate table",
    )
    tasks = _read(TASKS_MD)
    _require(tasks, "plan.md § Mirror Obligations", "the sole owner")
    runtime = _read(MODEL_DOC)
    _require(
        runtime,
        "**mirror obligations** for the driver source files are owned by "
        "`plan.md` § **Mirror Obligations**",
        "this file does not restate that table",
    )


def test_required_output_inventory_has_exactly_one_owner():
    """data-model.md E13 owns the only complete required-output inventory."""
    data_model = _read(DATA_MODEL_MD)
    _require(
        data_model,
        "## E13 — RetryDelta and DecompositionRule",
        "**Owner declaration**: the table below is the sole authoritative owner of "
        "the per-stage required-output inventory and package-shape guidance",
        "| Rule id | Stage | Package derivation | Required-output inventory |",
    )
    rule_rows = [
        line
        for line in data_model.splitlines()
        if re.match(r"^\| `decompose-[a-z]+-v1` \|", line)
    ]
    assert len(rule_rows) == 4, (
        "E13 must own the four decomposition-rule inventory rows, got %d"
        % len(rule_rows)
    )
    # The complete inventory rows (with their fourth column) exist only in E13.
    for document, label in (
        (PLAN_MD, "plan.md"),
        (FEATURE_REF_MD, "feature-ref.md"),
        (RESEARCH_MD, "research.md"),
        (MODEL_DOC, "decomposition-model.md"),
    ):
        text = _read(document)
        for row in rule_rows:
            assert row not in text, (
                "%s restates the E13 inventory row %r" % (label, row[:80])
            )

    research = _read(RESEARCH_MD)
    _require(
        research,
        "owner: `data-model.md` E13",
        "that table is the sole authoritative copy",
        "MUST NOT restate the rows",
    )
    feature_ref = _read(FEATURE_REF_MD)
    _require(feature_ref, "data-model.md", "E13")
    runtime = _read(MODEL_DOC)
    _require(
        runtime,
        "**required-output inventory** for each rule is owned by "
        "`data-model.md` **E13**",
        "this file does not restate it",
    )


# ---------------------------------------------------------------- additive-only


PREDECESSOR_H2_SECTIONS = [
    "What This Skill Does",
    "Driver Topology（驱动拓扑——义务真源：run-agent 派发治理）",
    "When to Load",
    "The Loop (U0–U6)",
    "Hard Requirements",
    "Discipline Defaults",
    "Efficiency Optimizations（运行效率优化）",
    "References",
    "Boundary",
    "Subagent Create & Dispatch Delegation（子代理创建与派发委派）",
    "Feedback & Probe Points（反馈与探针采集点）",
    "CLI Capability Profiles",
    "Wrap-up",
]

DECOMPOSITION_H2 = "Task Decomposition & Team Coordination（任务拆解与配合）"


def test_skill_sections_are_additive_only():
    """The 070 section is inserted; every predecessor H2 keeps its position."""
    sections = _h2_sections(_read(SKILL_MD))
    expected = (
        PREDECESSOR_H2_SECTIONS[:7]
        + [DECOMPOSITION_H2]
        + PREDECESSOR_H2_SECTIONS[7:]
    )
    assert sections == expected, (
        "the 070 section must be the only SKILL.md H2 insertion, got %r" % sections
    )


PREDECESSOR_DOCS_H2 = [
    "加载与投递",
    "双拓扑实例化（入口参数清单）",
    "执行侧可移植性",
    "机制归属（Feature 060 委派化）",
    "统一监听模型",
    "状态感知快照（065a-state-awareness）",
    "运行效率优化（063-sdd-loop-efficiency 切片；058 演化）",
    "并发归属与生命周期",
    "CLI 能力档案",
    "Hook 兜底与远程 SSH（2026-10-19 增强）",
    "触发与路由",
    "边界",
]

DOCS_DECOMPOSITION_H2 = "任务拆解与配合（070-subagent-task-teams 切片）"


def test_docs_page_sections_are_additive_only():
    """The docs page gains one pointer section; predecessor sections remain."""
    sections = _h2_sections(_read(DOCS_PAGE))
    expected = (
        PREDECESSOR_DOCS_H2[:7] + [DOCS_DECOMPOSITION_H2] + PREDECESSOR_DOCS_H2[7:]
    )
    assert sections == expected, (
        "the 070 docs section must be the only docs-page H2 insertion, got %r"
        % sections
    )


MODEL_SECTIONS_BEFORE = [
    "## 1. Work Package record",
    "## 2. ID assignment, layers, and tie-break (WP-04)",
    "## 3. Fences and spine write authority",
    "## 4. Canonical plan hash and replay (WP-06, WP-16)",
    "## 5. Amendments, retries, and split children (WP-07, WP-08)",
    "## 6. Attempt-scoped evidence files (WP-11, OR-02)",
    "## 7. Implement: projection of the 067 part brief (WP-12)",
    "## 8. Decomposition rules and required-output coverage (WP-15)",
    "## 9. Single-package representation (WP-13)",
    "## 10. Ledger (WP-09, WP-10, OR-01)",
    "## 11. Timestamp units (WP-17)",
    "## 12. Gate invocation, repair, and fallback pointers",
    "## 13. Scheduler and dispatch (SD-01…SD-16)",
    "## 14. Retry, delta, and escalation (OR-14…OR-16)",
    "## 15. Independent verification (VI-01…VI-06)",
    "## 16. Integration and stage close (VI-07…VI-14)",
    "## 17. Stage-team preset and adapter (ST-01…ST-12)",
    "## 18. Observability, metrics, and stage close (OR-03…OR-16)",
    "## 19. Non-regression boundaries",
]


def test_runtime_owner_sections_are_additive_only():
    """Existing runtime-owner sections keep their content position."""
    headings = [
        line for line in _read(MODEL_DOC).splitlines() if line.startswith("## ")
    ]
    assert headings[: len(MODEL_SECTIONS_BEFORE)] == MODEL_SECTIONS_BEFORE, (
        "an existing decomposition-model section was renamed, removed, or reordered"
    )
