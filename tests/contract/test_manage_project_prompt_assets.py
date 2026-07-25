"""Contract tests for the manage-project skill prompt assets.

Evolved from summarize-project (spec 030, Feature 013). Covers:

- Package presence + byte-equivalent mirror
- Frontmatter: name, trigger keywords, skill_id pattern
- Skills registry row in .specify/instructions.md
- Ordered six-step workflow (load/init -> collect -> decompose ->
  embedded chart sources -> render validation -> consistency + persist)
- Single Markdown management document as source of truth with the four
  project-management elements (background, milestones, WBS, progress)
- Charts embedded as PlantUML source blocks (text-form, editable), with
  rendering delegated to draw-plantuml (@startwbs/@startgantt), no own scripts/
- Milestone tracking view (happens entries + tracking table)
- Progress semantics (three states, percent-complete, current-date reference)
- Incremental update mode for repeat runs
- Information-shortfall behavior, chart-set splitting
- references/management-playbook.md contents
- Canonical ## Feedback block with unit-id skill:manage-project
"""
from pathlib import Path

from tests.contract.helpers_prompt_assets import (
    ROOT,
    assert_dirs_byte_equivalent,
    assert_ordered,
    read_frontmatter,
    skill_registry_rows,
    text_of,
)

SKILL_DIR = ROOT / "skills" / "manage-project"
SKILL_FILE = SKILL_DIR / "SKILL.md"
PLAYBOOK_FILE = SKILL_DIR / "references" / "management-playbook.md"
MIRROR_DIR = ROOT / ".specify" / "skills" / "manage-project"

TRIGGER_KEYWORDS = [
    "项目管理",
    "项目背景",
    "项目里程碑",
    "进度追踪",
    "manage project",
    "project management",
    "progress tracking",
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
    "Step 7",
]

FOUR_ELEMENT_SECTIONS = [
    "项目背景",
    "项目里程碑",
    "主要工作",
    "进度追踪",
]


# ---------------------------------------------------------------------------
# Package presence and mirror equivalence
# ---------------------------------------------------------------------------

def test_skill_package_exists():
    assert SKILL_FILE.exists(), f"Expected {SKILL_FILE} to exist"


def test_playbook_exists():
    assert PLAYBOOK_FILE.exists(), f"Expected {PLAYBOOK_FILE} to exist"


def test_legacy_summarize_project_removed():
    legacy = ROOT / "skills" / "summarize-project"
    legacy_mirror = ROOT / ".specify" / "skills" / "summarize-project"
    assert not legacy.exists(), "summarize-project must be fully evolved into manage-project"
    assert not legacy_mirror.exists(), "stale summarize-project mirror must be removed"


def test_mirror_is_byte_equivalent():
    assert_dirs_byte_equivalent(SKILL_DIR, MIRROR_DIR)


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def test_frontmatter_name_and_skill_id():
    fm = read_frontmatter(SKILL_FILE)
    assert fm.get("name") == "manage-project", f"got name={fm.get('name')}"
    skill_id = fm.get("skill_id", "")
    assert skill_id == "<SKILL:.specify/skills/manage-project/SKILL.md>", (
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
    rows = skill_registry_rows("manage-project")
    assert len(rows) == 1, f"Expected exactly 1 registry row, got {len(rows)}: {rows}"


def test_registry_has_no_stale_summarize_project_row():
    rows = [r for r in skill_registry_rows("summarize-project") if r.startswith("| summarize-project ")]
    assert not rows, f"Stale summarize-project registry row(s) remain: {rows}"


# ---------------------------------------------------------------------------
# Workflow order and delegation
# ---------------------------------------------------------------------------

def test_seven_step_workflow_in_order():
    text = text_of(SKILL_FILE)
    assert_ordered(text, WORKFLOW_STEPS, context="in SKILL.md workflow")


def test_delegates_rendering_to_draw_plantuml():
    text = text_of(SKILL_FILE)
    assert "draw-plantuml" in text, "Expected delegation reference to draw-plantuml"
    assert "@startwbs" in text, "Expected @startwbs WBS delegation reference"
    assert "@startgantt" in text, "Expected @startgantt Gantt delegation reference"


def test_no_own_scripts_directory():
    scripts_dir = SKILL_DIR / "scripts"
    assert not scripts_dir.exists(), (
        "manage-project must delegate rendering; no scripts/ directory allowed"
    )


# ---------------------------------------------------------------------------
# Single management document with the four PM elements
# ---------------------------------------------------------------------------

def test_management_document_is_source_of_truth():
    text = text_of(SKILL_FILE)
    assert ".specify/project/" in text, (
        "Expected default management document location .specify/project/"
    )
    assert "单一事实源" in text, "Expected single-source-of-truth principle"


def test_four_pm_elements_documented():
    text = text_of(SKILL_FILE)
    for section in FOUR_ELEMENT_SECTIONS:
        assert section in text, f"Expected PM element section: {section}"


def test_charts_embedded_as_plantuml_source():
    text = text_of(SKILL_FILE)
    assert "```plantuml" in text, (
        "Expected charts embedded as ```plantuml source blocks in the document"
    )
    assert "源码" in text and "嵌入" in text, "Expected embedded-source (text-form chart) rule"


def test_incremental_update_mode_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "更新模式" in text, "Expected update mode for repeat runs"
    assert "增量" in text, "Expected incremental update rule"


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
    """Playbook carries status inference rules and degenerate-state handling
    (project not started / fully complete)."""
    text = text_of(PLAYBOOK_FILE)
    assert "推断" in text, "Expected status inference rules in playbook"
    assert "退化" in text, "Expected degenerate-state handling in playbook"


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
# Playbook management-document structure
# ---------------------------------------------------------------------------

def test_playbook_defines_document_skeleton():
    text = text_of(PLAYBOOK_FILE)
    assert ".specify/project/project.md" in text, (
        "Expected default document path in playbook skeleton"
    )
    for section in FOUR_ELEMENT_SECTIONS:
        assert section in text, f"Expected skeleton section in playbook: {section}"
    assert "元信息" in text, "Expected meta-info section in skeleton"


# ---------------------------------------------------------------------------
# Agile management loop, concept mapping, extension points
# ---------------------------------------------------------------------------

def test_agile_loop_documented():
    """SKILL.md defines the basic agile loop: requirement -> feature ->
    task (staffing) -> testcase -> evaluation, iterated continuously."""
    text = text_of(SKILL_FILE)
    for needle in ["需求", "特性", "任务", "测试用例", "评估", "迭代", "人力分配"]:
        assert needle in text, f"Expected agile loop element: {needle}"
    assert "管理循环" in text, "Expected a management-loop section"


def test_speckit_concept_mapping_documented():
    """Loop stages anchor to existing spec-kit artifacts instead of
    reinventing them; non-spec-kit projects get a fallback."""
    text = text_of(SKILL_FILE)
    for anchor in ["requirements.md", "features.md", "tasks.md", "verification.md"]:
        assert anchor in text, f"Expected spec-kit artifact anchor: {anchor}"
    assert "非 spec-kit" in text, "Expected non-spec-kit fallback column"


def test_iteration_log_section_in_skeleton():
    text = text_of(SKILL_FILE)
    playbook = text_of(PLAYBOOK_FILE)
    assert "迭代记录" in text, "Expected iteration-log element in SKILL.md"
    assert "迭代记录" in playbook, "Expected iteration-log section in playbook skeleton"
    assert "只追加" in playbook or "不改写" in playbook, (
        "Expected append-only rule for iteration history rows"
    )


def test_integration_extension_points_reserved_not_implemented():
    """Future Jira/CI-CD/SCM integration is a reserved extension seam;
    no external calls are implemented now."""
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "Jira" in text, "Expected Jira named as a future integration direction"
    assert "预留" in text, "Expected extension points marked as reserved"
    assert "不实现" in text or "不得引入" in text, (
        "Expected explicit no-implementation red line for external integrations"
    )
    assert "source" in text.lower() or "来源" in text, "Expected source convention for loop stages"


def test_deterministic_today_anchoring_rule():
    """Gantt today line must be anchored relative to project start, not the
    rendering environment clock (dogfood-run regression)."""
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "days after start" in text, "Expected deterministic today anchoring rule"


# ---------------------------------------------------------------------------
# Canonical Feedback block
# ---------------------------------------------------------------------------

def test_canonical_feedback_block():
    text = text_of(SKILL_FILE)
    assert "## Feedback" in text, "Expected canonical ## Feedback section"
    assert "skill:manage-project" in text, "Expected unit-id skill:manage-project"
