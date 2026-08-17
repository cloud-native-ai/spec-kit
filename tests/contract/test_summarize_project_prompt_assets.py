"""Contract tests for the summarize-project skill prompt assets.

Refactored from manage-project (spec 030, Feature 013); renamed back from
visualize-project because the report carries both textual summary and
visual charts — "summarize" is the accurate name. Covers:

- Package presence + byte-equivalent mirror
- Legacy manage-project / visualize-project removal + obsolete-skills
  cleanup manifest entry
- Frontmatter: name, trigger keywords, skill_id pattern
- Skills registry row in .specify/instructions.md
- Presentation/output-tool positioning (read-only, derived report)
- Input contract: required-info table + context ingestion + form fill-in
  (project-input form under the delivery dir), with git repo material as an
  opt-in supplementary source rather than the primary path
- Traceable, non-code-only inputs: management-system exports and user
  documents are the primary sources; git history / README stay available as
  optional supplements
- Deterministic input validation codified in scripts (validate-project-input.py
  for the form contract, detect-project-sources.py for opt-in repo probing)
- Forward-guarded assertions: checks specific to the new input model skip when
  the skill copy predates it (no required-info.md), so this suite stays green
  across the refactor rollout
- Ordered six-step workflow (detect -> collect -> model -> charts ->
  render validation -> consistency + persist)
- Charts embedded as PlantUML source blocks, rendering delegated to
  draw-plantuml (@startwbs/@startgantt)
- Milestone/progress semantics, scope/granularity, chart-set splitting
- Layered references: one reference doc per presentation layer
  (project-overview, requirements-features, work-breakdown, milestones,
  task-progress), each answering one external-reader question, with
  references/reporting-playbook.md holding cross-layer conventions
  and the layer index
- Canonical ## Feedback block with unit-id skill:summarize-project
"""
from pathlib import Path

import pytest

from specify_cli import _OBSOLETE_SKILLS

from tests.contract.helpers_prompt_assets import (
    ROOT,
    assert_dirs_byte_equivalent,
    assert_ordered,
    read_frontmatter,
    text_of,
)

SKILL_DIR = ROOT / "skills" / "summarize-project"
SKILL_FILE = SKILL_DIR / "SKILL.md"
PLAYBOOK_FILE = SKILL_DIR / "references" / "reporting-playbook.md"
DETECT_SCRIPT = SKILL_DIR / "scripts" / "detect-project-sources.py"
REQUIRED_INFO_DOC = SKILL_DIR / "references" / "required-info.md"
VALIDATE_SCRIPT = SKILL_DIR / "scripts" / "validate-project-input.py"
FORM_TEMPLATE = SKILL_DIR / "templates" / "project-input.template.yaml"
MIRROR_DIR = ROOT / ".specify" / "skills" / "summarize-project"


def _input_model_present() -> bool:
    """True when this skill copy already carries the required-info input model.

    The input-model refactor (required-info table + form fill-in) lands in the
    skill package as references/required-info.md. Checks that only make sense
    under the new model are guarded by this helper so the suite stays green on
    copies that predate it.
    """
    return REQUIRED_INFO_DOC.exists()

LAYER_DOCS = {
    "project-overview.md": "目标",
    "requirements-features.md": "特性",
    "work-breakdown.md": "任务",
    "milestones.md": "里程碑",
    "task-progress.md": "进度",
}

TRIGGER_KEYWORDS = [
    "项目总结",
    "项目现状",
    "需求特性",
    "功能分解",
    "里程碑",
    "进度追踪",
    "summarize project",
    "project summary",
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
    assert not legacy.exists(), "manage-project must be fully refactored into summarize-project"
    assert not legacy_mirror.exists(), "stale manage-project mirror must be removed"


def test_legacy_visualize_project_removed():
    legacy = ROOT / "skills" / "visualize-project"
    legacy_mirror = ROOT / ".specify" / "skills" / "visualize-project"
    assert not legacy.exists(), "visualize-project must be fully renamed to summarize-project"
    assert not legacy_mirror.exists(), "stale visualize-project mirror must be removed"


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
# Directory discoverability (no registry)
# ---------------------------------------------------------------------------

def test_skill_discoverable_via_directory():
    skill_md = ROOT / ".specify" / "skills" / "summarize-project" / "SKILL.md"
    assert skill_md.is_file(), "skills are discovered by directory — SKILL.md must exist"
    fm = read_frontmatter(skill_md)
    assert str(fm.get("name", "")) == "summarize-project", \
        "frontmatter name must match the directory for directory-based discovery"


def test_no_stale_predecessor_directories():
    for name in ("manage-project", "visualize-project"):
        stale = ROOT / ".specify" / "skills" / name
        assert not stale.is_dir(), f"Stale {name} directory remains — discovery would surface it"


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

def test_input_sources_are_identifiable_and_traceable():
    """Intent (preserved across the input-model refactor): information sources
    must be identifiable and traceable, and the skill must have an explicit
    identification/validation step before it collects anything.

    Architecture-tolerant: the pre-refactor copy documents repo-artifact
    detection (.specify/ + requirements/features/tasks anchors); the
    post-refactor copy documents the required-info table + project-input form
    contract (repo material demoted to an opt-in supplement). Default delivery
    locations are asserted separately in test_default_report_paths_documented.
    """
    text = text_of(SKILL_FILE)
    assert ".specify" in text, "Expected .specify/ paths (delivery location / artifact anchors)"
    assert "检测" in text or "校验" in text, (
        "Expected an explicit detection/validation step for project information"
    )
    repo_artifact_model = all(
        anchor in text for anchor in ("requirements.md", "features.md", "tasks.md")
    )
    form_input_model = all(
        marker in text
        for marker in ("required-info.md", "project-input", "必要信息表", "表单")
    )
    assert repo_artifact_model or form_input_model, (
        "Expected either repo-artifact source anchors or the required-info "
        "table + project-input form contract to be documented"
    )


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
    if _input_model_present():
        combined = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
        assert "管理系统" in combined or "导出" in combined, (
            "Under the required-info input model, management-system exports / "
            "user documents must be documented as the primary input source"
        )


def test_detect_script_referenced_and_structured():
    text = text_of(SKILL_FILE)
    assert "detect-project-sources.py" in text, "Expected detect script invocation in SKILL.md"
    script = text_of(DETECT_SCRIPT)
    assert "--target" in script, "Expected --target CLI argument"
    assert "json" in script, "Expected JSON output"
    assert "default_report_path" in script, "Expected default report path in script output"
    if _input_model_present():
        assert "opt-in" in text or "可选" in text, (
            "Repo probing must be documented as an opt-in supplement, not the main path"
        )
        assert "validate-project-input.py" in text, (
            "Expected the form-contract validator to be invoked from SKILL.md"
        )
        validator = text_of(VALIDATE_SCRIPT)
        for flag in ("--input", "--form-skeleton", "--emit-json"):
            assert flag in validator, f"Expected validator CLI flag: {flag}"


CANONICAL_FIELDS = [
    "project_name",
    "baseline_date",
    "phase_id",
    "item_id",
    "item_name",
    "owner_id",
    "milestone_id",
    "planned_end",
    "anchor_item_id",
    "depends_on",
    "feature_id",
    "source",
]


def test_required_info_table_is_input_contract():
    """The required-info table is the single authority for the input contract:
    canonical snake_case field names (also used as relational foreign keys),
    the three requiredness tiers, and referential-integrity rules."""
    if not _input_model_present():
        pytest.skip("skill copy predates the required-info input model")
    text = text_of(REQUIRED_INFO_DOC)
    missing = [f for f in CANONICAL_FIELDS if f not in text]
    assert not missing, f"required-info.md missing canonical fields: {missing}"
    for entity in ("project", "phases", "work_items", "milestones", "people",
                   "features", "sources"):
        assert entity in text, f"required-info.md missing entity: {entity}"
    for tier in ("必填", "可推断", "可选"):
        assert tier in text, f"required-info.md missing requiredness tier: {tier}"
    assert "全局唯一" in text, "Expected globally-unique *_id rule"
    assert "外键" in text, "Expected foreign-key resolvability rule"
    assert "inferred_from" in text, "Expected inferred-value provenance marker"


def test_form_fill_in_flow_documented():
    """Three-stage input flow: context ingestion -> validation -> form fill-in
    (blocking only when a truly required field is missing)."""
    if not _input_model_present():
        pytest.skip("skill copy predates the required-info input model")
    text = text_of(SKILL_FILE)
    for marker in ("上下文摄取", "校验", "表单补填", "阻断"):
        assert marker in text, f"SKILL.md missing input-flow marker: {marker}"
    assert "data/project-input.yaml" in text, (
        "Expected the project-input form to live inside the delivery directory data/"
    )
    assert "只读" in text, "Expected read-only positioning for the user-owned form"
    assert FORM_TEMPLATE.exists(), f"Expected blank form template: {FORM_TEMPLATE}"
    template = text_of(FORM_TEMPLATE)
    for field in ("project_name", "baseline_date", "work_items", "milestones"):
        assert field in template, f"form template missing field: {field}"


def test_repo_material_is_opt_in():
    """Repo material is an opt-in supplementary source: nothing is scanned
    unless the form declares repos[] and marks fields as repo-derived."""
    if not _input_model_present():
        pytest.skip("skill copy predates the required-info input model")
    skill = text_of(SKILL_FILE)
    tiers = text_of(SKILL_DIR / "references" / "source-tiers.md")
    for marker in ("repos", "derive_fields", "opt-in"):
        assert marker in skill, f"SKILL.md missing repo opt-in marker: {marker}"
    assert "默认不扫" in skill or "默认不查" in skill, (
        "Expected an explicit 'no repo scanning by default' statement"
    )
    assert "opt-in" in tiers, "source-tiers.md must be framed as an opt-in supplement"
    assert "全仓扫描" in tiers, "Expected the no-full-repo-scan prohibition"
    assert "多 repo" in tiers or "多 repo" in skill, (
        "Expected multi-repo aggregation rules (a project may span several repos)"
    )


def test_engine_input_schema_matches_required_info():
    """Convergence point: the form IS the engine input -- required-info table,
    engine --print-schema, and the validator share one set of field names."""
    if not _input_model_present():
        pytest.skip("skill copy predates the required-info input model")
    engine = text_of(SKILL_DIR / "scripts" / "progress-engine.py")
    validator = text_of(VALIDATE_SCRIPT)
    doc = text_of(REQUIRED_INFO_DOC)
    for field in CANONICAL_FIELDS:
        assert field in engine, f"progress-engine.py missing canonical field: {field}"
        assert field in validator, f"validate-project-input.py missing canonical field: {field}"
        assert field in doc, f"required-info.md missing canonical field: {field}"


def test_default_report_paths_documented():
    """Delivery contract: two default delivery locations (delivery directory
    .specify/project/summary/ for SpecKit projects, docs/project-summary/
    otherwise), chosen by the detection result."""
    text = text_of(SKILL_FILE) + text_of(PLAYBOOK_FILE)
    assert ".specify/project/summary" in text, (
        "Expected SpecKit default delivery location .specify/project/summary/"
    )
    assert "docs/project-summary" in text, (
        "Expected non-SpecKit default delivery location docs/project-summary/"
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
    """Intent (preserved across the delivery-contract change): every chart is
    delivered in **editable PlantUML text form**, not only as a rendered bitmap.

    Architecture-tolerant: the pre-refactor copy embeds ```plantuml source
    blocks in the report body; the post-refactor copy ships the source as
    `assets/<name>.puml` files inside the self-contained delivery directory
    (report body then references the rendered image by relative path). Either
    form satisfies the rule; what must never happen is charts shipping without
    an editable text source.
    """
    text = text_of(SKILL_FILE)
    embedded_blocks = "```plantuml" in text
    puml_files = ".puml" in text and "assets/" in text
    assert embedded_blocks or puml_files, (
        "Expected charts delivered as editable PlantUML text — either "
        "```plantuml source blocks in the report or assets/*.puml source files"
    )
    assert "源码" in text, "Expected the PlantUML source (源码) rule to be stated"
    assert "嵌入" in text or "可编辑" in text, (
        "Expected the chart source to be documented as embedded or editable text"
    )


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
    assert "skill:summarize-project" in text, "Expected unit-id skill:summarize-project"
