"""Contract tests for the visualize-project skill prompt assets.

Refactored from manage-project (spec 030, Feature 013). Covers:

- Package presence + byte-equivalent mirror
- Legacy manage-project removal + obsolete-skills cleanup manifest entry
- Frontmatter: name, trigger keywords, skill_id pattern
- Skills registry row in .specify/instructions.md
- Presentation/output-tool positioning (read-only, derived report)
- SpecKit auto-detection (.specify/ structure as primary info source)
- Multi-source inputs (code, README/docs, external documents, git history)
- Deterministic source detection codified in scripts/detect-project-sources.py
- Ordered six-step workflow (detect -> collect -> model -> charts ->
  render validation -> consistency + persist)
- Charts embedded as PlantUML source blocks, rendering delegated to
  draw-plantuml (@startwbs/@startgantt)
- Milestone/progress semantics, scope/granularity, chart-set splitting
- Layered references: one reference doc per presentation layer
  (project-overview, requirements-features, work-breakdown, milestones,
  task-progress), each answering one external-reader question, with
  references/visualization-playbook.md holding cross-layer conventions
  and the layer index
- Canonical ## Feedback block with unit-id skill:visualize-project
"""
from pathlib import Path

from specify_cli import _OBSOLETE_SKILLS

from tests.contract.helpers_prompt_assets import (
    ROOT,
    assert_dirs_byte_equivalent,
    assert_ordered,
    read_frontmatter,
    skill_registry_rows,
    text_of,
)

SKILL_DIR = ROOT / "skills" / "visualize-project"
SKILL_FILE = SKILL_DIR / "SKILL.md"
PLAYBOOK_FILE = SKILL_DIR / "references" / "visualization-playbook.md"
DETECT_SCRIPT = SKILL_DIR / "scripts" / "detect-project-sources.py"
MIRROR_DIR = ROOT / ".specify" / "skills" / "visualize-project"

LAYER_DOCS = {
    "project-overview.md": "目标",
    "requirements-features.md": "特性",
    "work-breakdown.md": "任务",
    "milestones.md": "里程碑",
    "task-progress.md": "进度",
}

TRIGGER_KEYWORDS = [
    "项目可视化",
    "项目现状",
    "需求特性",
    "功能分解",
    "里程碑",
    "进度追踪",
    "visualize project",
    "project visualization",
    "project report",
    "WBS",
    "工作分解",
    "甘特图",
]

WORKFLOW_STEPS = [
    "Step 1",
    "Step 2",
    "Step 3",
    "Step 4",
    "Step 5",
    "Step 6",
]

REPORT_SECTIONS = [
    "项目概览",
    "需求与特性",
    "功能分解",
    "项目里程碑",
    "任务进展",
]


# ---------------------------------------------------------------------------
# Package presence and mirror equivalence
# ---------------------------------------------------------------------------

def test_skill_package_exists():
    assert SKILL_FILE.exists(), f"Expected {SKILL_FILE} to exist"


def test_playbook_exists():
    assert PLAYBOOK_FILE.exists(), f"Expected {PLAYBOOK_FILE} to exist"


def test_detect_script_exists():
    assert DETECT_SCRIPT.exists(), f"Expected {DETECT_SCRIPT} to exist"


def test_legacy_manage_project_removed():
    legacy = ROOT / "skills" / "manage-project"
    legacy_mirror = ROOT / ".specify" / "skills" / "manage-project"
    assert not legacy.exists(), "manage-project must be fully refactored into visualize-project"
    assert not legacy_mirror.exists(), "stale manage-project mirror must be removed"


def test_manage_project_in_obsolete_cleanup_manifest():
    assert "manage-project" in _OBSOLETE_SKILLS, (
        "manage-project must be listed in _OBSOLETE_SKILLS so re-initialized "
        "workspaces prune the stale directory"
    )


def test_mirror_is_byte_equivalent():
    assert_dirs_byte_equivalent(SKILL_DIR, MIRROR_DIR)


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def test_frontmatter_name_and_skill_id():
    fm = read_frontmatter(SKILL_FILE)
    assert fm.get("name") == "visualize-project", f"got name={fm.get('name')}"
    skill_id = fm.get("skill_id", "")
    assert skill_id == "<SKILL:.specify/skills/visualize-project/SKILL.md>", (
        f"unexpected skill_id: {skill_id}"
    )


def test_frontmatter_description_trigger_keywords():
    fm = read_frontmatter(SKILL_FILE)
    desc = str(fm.get("description", "")).lower()
    missing = [k for k in TRIGGER_KEYWORDS if k.lower() not in desc]
    assert not missing, f"description missing trigger keywords: {missing}"


# ---------------------------------------------------------------------------
# Skills registry row
# ---------------------------------------------------------------------------

def test_registry_has_exactly_one_row():
    rows = skill_registry_rows("visualize-project")
    assert len(rows) == 1, f"Expected exactly 1 registry row, got {len(rows)}: {rows}"


def test_registry_has_no_stale_manage_project_row():
    rows = [r for r in skill_registry_rows("manage-project") if r.startswith("| manage-project ")]
    assert not rows, f"Stale manage-project registry row(s) remain: {rows}"


# ---------------------------------------------------------------------------
# Presentation/output-tool positioning
# ---------------------------------------------------------------------------

def test_presentation_tool_positioning():
    text = text_of(SKILL_FILE)
    assert "呈现" in text, "Expected presentation (呈现) positioning"
    assert "派生" in text, "Expected derived-report (派生) semantics"
    assert "只读" in text or "只读取" in text, "Expected read-only source guarantee"
    assert "不修改" in text, "Expected explicit no-modification rule for source artifacts"


def test_report_is_regenerable_derived_artifact():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "刷新" in text or "重生成" in text, "Expected refresh/regenerate semantics for repeat runs"
    assert "附注" in text, "Expected preserved user-notes section (附注) rule"


# ---------------------------------------------------------------------------
# SpecKit auto-detection and multi-source inputs
# ---------------------------------------------------------------------------

def test_speckit_detection_documented():
    text = text_of(SKILL_FILE)
    assert ".specify" in text, "Expected .specify/ detection rule"
    for anchor in ["requirements.md", "features.md", "tasks.md"]:
        assert anchor in text, f"Expected SpecKit artifact anchor: {anchor}"
    assert "非 SpecKit" in text, "Expected non-SpecKit fallback column"
    assert "检测" in text, "Expected detection step wording"


def test_multi_source_inputs_documented():
    text = (text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)).lower()
    assert "git" in text, "Expected git history as an input source"
    assert "readme" in text, "Expected README as an input source"
    assert "外部" in text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE), (
        "Expected external files/documents as input sources"
    )
    assert "不限于代码" in text_of(SKILL_FILE), (
        "Expected explicit 'inputs not limited to code' statement"
    )


def test_detect_script_referenced_and_structured():
    text = text_of(SKILL_FILE)
    assert "detect-project-sources.py" in text, "Expected detect script invocation in SKILL.md"
    script = text_of(DETECT_SCRIPT)
    assert "--target" in script, "Expected --target CLI argument"
    assert "json" in script, "Expected JSON output"
    assert "default_report_path" in script, "Expected default report path in script output"


def test_default_report_paths_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert ".specify/project/visualization.md" in text, (
        "Expected SpecKit default report path .specify/project/visualization.md"
    )
    assert "docs/project-visualization.md" in text, (
        "Expected non-SpecKit default report path docs/project-visualization.md"
    )


# ---------------------------------------------------------------------------
# Workflow order and delegation
# ---------------------------------------------------------------------------

def test_six_step_workflow_in_order():
    text = text_of(SKILL_FILE)
    assert_ordered(text, WORKFLOW_STEPS, context="in SKILL.md workflow")


def test_delegates_rendering_to_draw_plantuml():
    text = text_of(SKILL_FILE)
    assert "draw-plantuml" in text, "Expected delegation reference to draw-plantuml"
    assert "@startwbs" in text, "Expected @startwbs WBS delegation reference"
    assert "@startgantt" in text, "Expected @startgantt Gantt delegation reference"


def test_charts_embedded_as_plantuml_source():
    text = text_of(SKILL_FILE)
    assert "```plantuml" in text, (
        "Expected charts embedded as ```plantuml source blocks in the report"
    )
    assert "源码" in text and "嵌入" in text, "Expected embedded-source (text-form chart) rule"


# ---------------------------------------------------------------------------
# Report content: five presentation sections
# ---------------------------------------------------------------------------

def test_five_presentation_sections_documented():
    text = text_of(SKILL_FILE)
    for section in REPORT_SECTIONS:
        assert section in text, f"Expected report section: {section}"


def test_playbook_defines_report_skeleton():
    text = text_of(PLAYBOOK_FILE)
    for section in REPORT_SECTIONS:
        assert section in text, f"Expected skeleton section in playbook: {section}"
    assert "元信息" in text, "Expected meta-info section in skeleton"
    assert "信息源" in text, "Expected source-list in meta-info"


# ---------------------------------------------------------------------------
# Milestones, progress semantics, consistency
# ---------------------------------------------------------------------------

def test_milestone_and_status_semantics_documented():
    text = text_of(SKILL_FILE).lower()
    for needle in ["milestone", "里程碑"]:
        assert needle in text, f"Expected milestone semantics ({needle})"
    for needle in ["completed", "in-progress", "not-started"]:
        assert needle in text, f"Expected status semantics: {needle}"


def test_milestone_view_and_tracking_table_documented():
    text = text_of(SKILL_FILE)
    assert "happens" in text, "Expected milestone happens-entry semantics"
    assert "表格" in text, "Expected milestone tracking table"


def test_chart_consistency_rule_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "一致" in text or "consistency" in text.lower(), (
        "Expected chart consistency rule (WBS leaves <-> Gantt entries <-> milestones)"
    )


def test_clarification_round_and_assumption_marking():
    text = (text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)).lower()
    assert "假设" in text or "assumption" in text, "Expected assumption marking guidance"


def test_chart_set_splitting_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "图集" in text or "drill-down" in text.lower() or "overview" in text.lower(), (
        "Expected chart-set splitting guidance for large projects"
    )


def test_milestone_anchoring_rule_documented():
    """Milestones are zero-duration diamond markers anchored to a date or an
    associated work item's end."""
    text = text_of(SKILL_FILE)
    assert "零工期" in text or "happens" in text.lower(), "Expected zero-duration milestone semantics"
    assert "锚定" in text or "anchor" in text.lower(), "Expected milestone anchoring rule"


def test_percent_complete_and_reference_marker_documented():
    """In-progress items carry percent-complete; mid-flight projects mark the
    current-date reference line."""
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "百分比" in text or "percent" in text.lower(), "Expected percent-complete rule"
    assert "参照线" in text or "today" in text.lower(), "Expected current-date reference marker rule"


def test_status_inference_and_degenerate_states_documented():
    """Task-progress layer doc carries status inference rules and
    degenerate-state handling (project not started / fully complete)."""
    text = text_of(SKILL_DIR / "references" / "task-progress.md")
    assert "推断" in text, "Expected status inference rules in task-progress layer doc"
    assert "退化" in text, "Expected degenerate-state handling in task-progress layer doc"


def test_deterministic_today_anchoring_rule():
    """Gantt today line must be anchored relative to project start, not the
    rendering environment clock."""
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "days after start" in text, "Expected deterministic today anchoring rule"


# ---------------------------------------------------------------------------
# Scope and audience granularity controls
# ---------------------------------------------------------------------------

def test_scope_and_granularity_controls_documented():
    text = text_of(SKILL_FILE)
    assert "范围与受众粒度" in text or ("scope" in text.lower() and "粒度" in text), (
        "Expected a scope/granularity section in SKILL.md"
    )
    assert "周期" in text, "Expected period scoping guidance"


def test_granularity_rules_in_playbook():
    text = text_of(PLAYBOOK_FILE)
    assert "周期限定" in text, "Expected period-scoping rule in playbook"
    assert "粒度限定" in text or "高管" in text, "Expected audience-granularity rule in playbook"
    assert "阶段级结构" in text, "Phase-level structure preservation rule required"


# ---------------------------------------------------------------------------
# Layered references: one doc per presentation layer
# ---------------------------------------------------------------------------

def test_layer_reference_docs_exist():
    for doc in LAYER_DOCS:
        path = SKILL_DIR / "references" / doc
        assert path.exists(), f"Expected layer reference doc: {path}"


def test_skill_links_every_layer_doc():
    text = text_of(SKILL_FILE)
    for doc in LAYER_DOCS:
        assert f"references/{doc}" in text, f"SKILL.md must link layer doc {doc}"


def test_playbook_has_layer_index():
    text = text_of(PLAYBOOK_FILE)
    for doc in LAYER_DOCS:
        assert doc in text, f"Playbook layer index must reference {doc}"


def test_layer_docs_answer_external_reader_questions():
    """Each layer maps to an external-reader question surfaced in SKILL.md:
    goals, capabilities, tasks, milestones (which achieved), per-task status +
    overall schedule."""
    text = text_of(SKILL_FILE)
    for needle in ["目标是什么", "包含哪些任务", "完成了哪些里程碑", "整体进度安排"]:
        assert needle in text, f"Expected external-reader question mapping: {needle}"


def test_layer_docs_share_uniform_structure():
    for doc in LAYER_DOCS:
        text = text_of(SKILL_DIR / "references" / doc)
        for heading in ["呈现要素", "落笔检查"]:
            assert heading in text, f"{doc} missing uniform section: {heading}"


def test_milestone_layer_doc_tracks_achievement():
    text = text_of(SKILL_DIR / "references" / "milestones.md")
    for needle in ["achieved", "pending", "at-risk", "happens", "锚定"]:
        assert needle in text, f"milestones.md missing: {needle}"


def test_task_progress_layer_doc_covers_schedule():
    text = text_of(SKILL_DIR / "references" / "task-progress.md")
    for needle in ["days after start", "百分比", "假设", "整体进度"]:
        assert needle in text, f"task-progress.md missing: {needle}"


def test_overview_layer_doc_covers_goals():
    text = text_of(SKILL_DIR / "references" / "project-overview.md")
    for needle in ["目标", "背景", "范围", "出处"]:
        assert needle in text, f"project-overview.md missing: {needle}"


def test_work_breakdown_layer_doc_is_single_data_source():
    text = text_of(SKILL_DIR / "references" / "work-breakdown.md")
    assert "@startwbs" in text, "work-breakdown.md must reference @startwbs"
    assert "唯一数据源" in text or "单一" in text, (
        "work-breakdown.md must state the single-data-source rule"
    )


# ---------------------------------------------------------------------------
# Canonical Feedback block
# ---------------------------------------------------------------------------

def test_canonical_feedback_block():
    text = text_of(SKILL_FILE)
    assert "## Feedback" in text, "Expected canonical ## Feedback section"
    assert "skill:visualize-project" in text, "Expected unit-id skill:visualize-project"
