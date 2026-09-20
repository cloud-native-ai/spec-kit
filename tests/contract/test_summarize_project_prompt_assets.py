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

Also absorbs the former test_study_project_uml_assets.py (same spec 030,
Feature 013): the study-project UML-enhancement prompt assets share the
mirror-parity / frontmatter / draw-plantuml-delegation propositions with
summarize-project, so both skills' prompt assets are pinned in one file. The
study-project section is delimited below.
"""
import json

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

# --- study-project UML enhancement (spec 030, Feature 013) -------------------
STUDY_SKILL_DIR = ROOT / "skills" / "study-project"
STUDY_SKILL_FILE = STUDY_SKILL_DIR / "SKILL.md"
STUDY_GUIDE_FILE = STUDY_SKILL_DIR / "references" / "uml-visualization-guide.md"
STUDY_MIRROR_DIR = ROOT / ".specify" / "skills" / "study-project"
BASELINE_FILE = ROOT / "tests" / "fixtures" / "study_project_baseline.json"

UML_TRIGGERS = ["UML", "component diagram", "deployment diagram", "sequence diagram"]


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


@pytest.mark.parametrize(
    "canonical,mirror",
    [(SKILL_DIR, MIRROR_DIR), (STUDY_SKILL_DIR, STUDY_MIRROR_DIR)],
    ids=["summarize-project", "study-project"],
)
def test_mirror_is_byte_equivalent(canonical, mirror):
    assert_dirs_byte_equivalent(canonical, mirror)


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


# ===========================================================================
# study-project UML enhancement prompt assets (spec 030, Feature 013)
#
# Contracts C-14…C-20 from contracts/visual-reporting-skills.openapi.yaml.
# Mirror parity is pinned by the parametrized test_mirror_is_byte_equivalent
# above (both skills). test_primary_view_coverage_statement was dropped: for a
# UML guide, "architecture"/"结构" and "deployment"/"部署" are present no matter
# what, and the diagram-type vocabulary is already pinned as a structured list
# in test_study_guide_exists_with_view_type_mapping.
# ===========================================================================


def _baseline() -> dict:
    return json.loads(BASELINE_FILE.read_text(encoding="utf-8"))


def _section(text: str, heading: str) -> str:
    """Return the body of a markdown section (heading line excluded)."""
    idx = text.find(heading)
    assert idx >= 0, f"Section not found: {heading}"
    rest = text[idx + len(heading):]
    for marker in ("\n## ", "\n### "):
        cut = rest.find(marker)
        if cut >= 0:
            rest = rest[:cut]
    return rest


def test_study_frontmatter_name_preserved():
    fm = read_frontmatter(STUDY_SKILL_FILE)
    assert fm.get("name") == "study-project", f"got name={fm.get('name')}"


def test_study_frontmatter_description_has_uml_triggers():
    fm = read_frontmatter(STUDY_SKILL_FILE)
    desc = str(fm.get("description", "")).lower()
    missing = [t for t in UML_TRIGGERS if t.lower() not in desc]
    assert not missing, f"description missing UML trigger terms: {missing}"


def test_study_phase5_plans_uml_figures_for_primary_views():
    body = _section(text_of(STUDY_SKILL_FILE), "### Phase 5: Dynamic Report Structure Design")
    assert "UML" in body, "Phase 5 must plan UML figures"
    assert "primary" in body.lower() or "主视图" in body, "Phase 5 must reference primary views"


def test_study_phase8_embeds_rendered_figures():
    body = _section(
        text_of(STUDY_SKILL_FILE),
        "### Phase 8: Multi-Source Fusion & Final Report (Main Agent)",
    )
    assert "UML" in body or "figure" in body.lower(), "Phase 8 must assemble UML figures"
    assert "png" in body.lower(), "Phase 8 must state PNG embedding"


def test_study_delegation_to_draw_plantuml_and_no_rendering_code():
    text = text_of(STUDY_SKILL_FILE) + text_of(STUDY_GUIDE_FILE)
    assert "draw-plantuml" in text, "Expected delegation reference to draw-plantuml"
    # The pre-existing scripts/research-project.sh is an analysis helper, not
    # rendering code. The enhancement must not introduce rendering scripts —
    # no script in the package may reference plantuml/render-plantuml.
    offenders = []
    for p in STUDY_SKILL_DIR.rglob("*"):
        if p.is_file() and p.suffix in {".sh", ".py", ".js"}:
            body = p.read_text(encoding="utf-8", errors="ignore").lower()
            if "plantuml" in body or "render-plantuml" in body:
                offenders.append(str(p))
    assert not offenders, f"Rendering code must not be added to the package: {offenders}"


def test_study_guide_exists_with_view_type_mapping():
    assert STUDY_GUIDE_FILE.exists(), f"Expected {STUDY_GUIDE_FILE}"
    text = text_of(STUDY_GUIDE_FILE)
    for term in ["component", "package", "deployment", "sequence", "activity", "class", "ER"]:
        assert term.lower() in text.lower(), f"Mapping missing diagram type: {term}"
    assert "activity" in text.lower(), "behavior-flow must allow activity as alternative"


def test_study_guide_states_docs_figures_convention():
    text = text_of(STUDY_GUIDE_FILE)
    assert "docs/figures/" in text, "Guide must state the docs/figures/ storage convention"


def test_study_degradation_rule_documented():
    text = (text_of(STUDY_SKILL_FILE) + text_of(STUDY_GUIDE_FILE)).lower()
    assert "degradation" in text or "降级" in text, "Expected renderer-unavailable degradation rule"


def test_study_figure_output_conventions():
    text = text_of(STUDY_GUIDE_FILE).lower()
    for needle in ["png", "svg", ".puml", "caption"]:
        assert needle in text, f"Guide must state figure output convention: {needle}"


def test_study_mermaid_scoped_to_secondary_content():
    body = _section(text_of(STUDY_SKILL_FILE), "## Output Requirements")
    assert "UML" in body, "Output Requirements must declare UML as primary-view standard"
    lowered = body.lower()
    assert "secondary" in lowered or "次要" in body, "Mermaid must be scoped to secondary content"


def test_study_deliverable_location_unchanged():
    text = text_of(STUDY_SKILL_FILE)
    assert _baseline()["deliverable_statement"] in text, (
        "Deliverable statement $WORK_DIR/docs/overview.md must remain (SC-007)"
    )


def test_study_baseline_sections_preserved():
    text = text_of(STUDY_SKILL_FILE)
    missing = [h for h in _baseline()["required_headings"] if h not in text]
    assert not missing, f"Baseline sections removed (SC-007): {missing}"


def test_study_reference_guides_preserved():
    for guide in _baseline()["reference_guides"]:
        assert (STUDY_SKILL_DIR / "references" / guide).exists(), f"Missing baseline guide: {guide}"
