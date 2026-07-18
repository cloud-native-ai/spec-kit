"""Contract tests for the summarize-project skill prompt assets.

Spec: .specify/specs/030-summarize-project (Feature 013 — Skills Command)
Covers contract items C-1…C-13 from
contracts/visual-reporting-skills.openapi.yaml:

- Package presence + byte-equivalent mirror (C-1)
- Frontmatter: name, 7 trigger keywords, skill_id pattern (C-2)
- Skills registry row in .specify/instructions.md (C-3)
- Ordered five-step workflow (C-4)
- Delegation to draw-plantuml @startwbs/@startgantt, no own scripts/ (C-5)
- Milestones + progress status semantics + two-chart consistency (C-6)
- Information-shortfall behavior (C-7), chart-set splitting (C-8)
- references/reporting-playbook.md contents (C-9)
- Report output conventions incl. docs/project-summary/ (C-10, C-11, C-12)
- Canonical ## Feedback block with unit-id skill:summarize-project (C-13)
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

SKILL_DIR = ROOT / "skills" / "summarize-project"
SKILL_FILE = SKILL_DIR / "SKILL.md"
PLAYBOOK_FILE = SKILL_DIR / "references" / "reporting-playbook.md"
MIRROR_DIR = ROOT / ".specify" / "skills" / "summarize-project"

TRIGGER_KEYWORDS = [
    "项目总结",
    "项目汇报",
    "进展报告",
    "项目进展",
    "summarize project",
    "project summary",
    "project report",
]

WORKFLOW_STEPS = [
    "Step 1",
    "Step 2",
    "Step 3",
    "Step 4",
    "Step 5",
]


# ---------------------------------------------------------------------------
# C-1: package presence and mirror equivalence
# ---------------------------------------------------------------------------

def test_skill_package_exists():
    assert SKILL_FILE.exists(), f"Expected {SKILL_FILE} to exist"


def test_playbook_exists():
    assert PLAYBOOK_FILE.exists(), f"Expected {PLAYBOOK_FILE} to exist"


def test_mirror_is_byte_equivalent():
    assert_dirs_byte_equivalent(SKILL_DIR, MIRROR_DIR)


# ---------------------------------------------------------------------------
# C-2: frontmatter
# ---------------------------------------------------------------------------

def test_frontmatter_name_and_skill_id():
    fm = read_frontmatter(SKILL_FILE)
    assert fm.get("name") == "summarize-project", f"got name={fm.get('name')}"
    skill_id = fm.get("skill_id", "")
    assert skill_id == "<SKILL:.specify/skills/summarize-project/SKILL.md>", (
        f"unexpected skill_id: {skill_id}"
    )


def test_frontmatter_description_trigger_keywords():
    fm = read_frontmatter(SKILL_FILE)
    desc = str(fm.get("description", "")).lower()
    missing = [k for k in TRIGGER_KEYWORDS if k.lower() not in desc]
    assert not missing, f"description missing trigger keywords: {missing}"


# ---------------------------------------------------------------------------
# C-3: skills registry row
# ---------------------------------------------------------------------------

def test_registry_has_exactly_one_row():
    rows = skill_registry_rows("summarize-project")
    assert len(rows) == 1, f"Expected exactly 1 registry row, got {len(rows)}: {rows}"


# ---------------------------------------------------------------------------
# C-4/C-5: workflow order and delegation
# ---------------------------------------------------------------------------

def test_five_step_workflow_in_order():
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
        "summarize-project must delegate rendering; no scripts/ directory allowed"
    )


# ---------------------------------------------------------------------------
# C-6/C-7/C-8: consistency, shortfall behavior, chart-set splitting
# ---------------------------------------------------------------------------

def test_milestone_and_status_semantics_documented():
    text = text_of(SKILL_FILE).lower()
    for needle in ["milestone", "里程碑"]:
        assert needle in text, f"Expected milestone semantics ({needle})"
    for needle in ["completed", "in-progress", "not-started"]:
        assert needle in text, f"Expected status semantics: {needle}"


def test_two_chart_consistency_rule_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "一致" in text or "consistency" in text.lower(), (
        "Expected two-chart consistency rule (WBS leaves <-> Gantt entries)"
    )


def test_clarification_round_and_assumption_marking():
    text = (text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)).lower()
    assert "假设" in text or "assumption" in text, "Expected assumption marking guidance"


def test_chart_set_splitting_documented():
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert "图集" in text or "drill-down" in text.lower() or "overview" in text.lower(), (
        "Expected chart-set splitting guidance for large projects"
    )


# ---------------------------------------------------------------------------
# C-10/C-11/C-12: output conventions
# ---------------------------------------------------------------------------

def test_output_location_and_image_conventions():
    text = text_of(SKILL_FILE)
    assert "docs/project-summary/" in text, "Expected default output location docs/project-summary/"
    lowered = text.lower()
    for needle in ["png", "svg", ".puml"]:
        assert needle in lowered, f"Expected image convention mention: {needle}"


def test_report_states_date_scope_assumptions():
    lowered = text_of(SKILL_FILE).lower()
    assert "scope" in lowered or "范围" in lowered, "Expected reporting scope statement rule"


# ---------------------------------------------------------------------------
# C-6 (US2/T015): milestone anchoring, percent-complete, reference marker
# ---------------------------------------------------------------------------

def test_milestone_anchoring_rule_documented():
    """Gantt step requires zero-duration milestone markers anchored to a date
    or to an associated work item's end (FR-007)."""
    text = text_of(SKILL_FILE)
    assert "零工期" in text or "happens" in text.lower(), "Expected zero-duration milestone semantics"
    assert "锚定" in text or "anchor" in text.lower(), "Expected milestone anchoring rule"


def test_percent_complete_and_reference_marker_documented():
    """In-progress items carry percent-complete; mid-flight projects mark the
    current-date reference line (FR-008)."""
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
# US3/T027: reporting-period scoping and audience granularity controls
# ---------------------------------------------------------------------------

def test_scope_and_granularity_controls_documented():
    """SKILL.md documents reporting-period scoping and audience-driven
    granularity control (US3, FR per requirements.md User Story 4-era scope)."""
    text = text_of(SKILL_FILE)
    assert "汇报范围与受众粒度" in text or ("scope" in text.lower() and "粒度" in text), (
        "Expected a scope/granularity section in SKILL.md"
    )
    assert "汇报周期" in text or "周期" in text, "Expected reporting-period scoping guidance"


def test_granularity_rules_in_playbook():
    """Playbook carries period-scoping and granularity rules while preserving
    phase-level structure and the two-chart consistency rule."""
    text = text_of(PLAYBOOK_FILE)
    assert "周期限定" in text or "汇报周期" in text, "Expected period-scoping rule in playbook"
    assert "粒度限定" in text or "高管" in text, "Expected audience-granularity rule in playbook"
    assert "阶段级结构" in text, "Phase-level structure preservation rule required"


# ---------------------------------------------------------------------------
# C-13: canonical Feedback block
# ---------------------------------------------------------------------------

def test_canonical_feedback_block():
    text = text_of(SKILL_FILE)
    assert "## Feedback" in text, "Expected canonical ## Feedback section"
    assert "skill:summarize-project" in text, "Expected unit-id skill:summarize-project"
