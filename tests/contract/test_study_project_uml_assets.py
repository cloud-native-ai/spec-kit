"""Contract tests for the study-project UML enhancement prompt assets.

Spec: .specify/specs/030-summarize-project (Feature 013 — Skills Command)
Covers contract items C-14…C-20 from
contracts/visual-reporting-skills.openapi.yaml:

- Frontmatter keeps name; description gains UML trigger terms (C-14)
- UML actions assigned to primary views; delegation to draw-plantuml;
  no rendering code added (C-15)
- View-to-diagram-type mapping in references/uml-visualization-guide.md (C-16)
- Mermaid scoped to secondary content; deliverable location and existing
  conventions unchanged — SC-007 regression guard (C-17)
- Renderer-unavailable degradation rule (C-18)
- Figure output conventions incl. docs/figures/ storage (C-19)
- Primary-figure coverage statement (C-20)
"""
import json

from tests.contract.helpers_prompt_assets import (
    ROOT,
    assert_dirs_byte_equivalent,
    read_frontmatter,
    text_of,
)

SKILL_DIR = ROOT / "skills" / "study-project"
SKILL_FILE = SKILL_DIR / "SKILL.md"
GUIDE_FILE = SKILL_DIR / "references" / "uml-visualization-guide.md"
MIRROR_DIR = ROOT / ".specify" / "skills" / "study-project"
BASELINE_FILE = ROOT / "tests" / "fixtures" / "study_project_baseline.json"

UML_TRIGGERS = ["UML", "component diagram", "deployment diagram", "sequence diagram"]


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


# ---------------------------------------------------------------------------
# C-1/SR-1: mirror equivalence
# ---------------------------------------------------------------------------

def test_mirror_is_byte_equivalent():
    assert_dirs_byte_equivalent(SKILL_DIR, MIRROR_DIR)


# ---------------------------------------------------------------------------
# C-14: frontmatter
# ---------------------------------------------------------------------------

def test_frontmatter_name_preserved():
    fm = read_frontmatter(SKILL_FILE)
    assert fm.get("name") == "study-project", f"got name={fm.get('name')}"


def test_frontmatter_description_has_uml_triggers():
    fm = read_frontmatter(SKILL_FILE)
    desc = str(fm.get("description", "")).lower()
    missing = [t for t in UML_TRIGGERS if t.lower() not in desc]
    assert not missing, f"description missing UML trigger terms: {missing}"


# ---------------------------------------------------------------------------
# C-15: UML actions at injection points; delegation, no rendering code
# ---------------------------------------------------------------------------

def test_phase5_plans_uml_figures_for_primary_views():
    body = _section(text_of(SKILL_FILE), "### Phase 5: Dynamic Report Structure Design")
    assert "UML" in body, "Phase 5 must plan UML figures"
    assert "primary" in body.lower() or "主视图" in body, "Phase 5 must reference primary views"


def test_phase8_embeds_rendered_figures():
    body = _section(text_of(SKILL_FILE), "### Phase 8: Multi-Source Fusion & Final Report (Main Agent)")
    assert "UML" in body or "figure" in body.lower(), "Phase 8 must assemble UML figures"
    assert "png" in body.lower(), "Phase 8 must state PNG embedding"


def test_delegation_to_draw_plantuml_and_no_rendering_code():
    text = text_of(SKILL_FILE) + text_of(GUIDE_FILE)
    assert "draw-plantuml" in text, "Expected delegation reference to draw-plantuml"
    # The pre-existing scripts/research-project.sh is an analysis helper, not
    # rendering code. The enhancement must not introduce rendering scripts —
    # no script in the package may reference plantuml/render-plantuml.
    offenders = []
    for p in SKILL_DIR.rglob("*"):
        if p.is_file() and p.suffix in {".sh", ".py", ".js"}:
            body = p.read_text(encoding="utf-8", errors="ignore").lower()
            if "plantuml" in body or "render-plantuml" in body:
                offenders.append(str(p))
    assert not offenders, f"Rendering code must not be added to the package: {offenders}"


# ---------------------------------------------------------------------------
# C-16/C-18/C-19: guide content — mapping, degradation, figures storage
# ---------------------------------------------------------------------------

def test_guide_exists_with_view_type_mapping():
    assert GUIDE_FILE.exists(), f"Expected {GUIDE_FILE}"
    text = text_of(GUIDE_FILE)
    for term in ["component", "package", "deployment", "sequence", "activity", "class", "ER"]:
        assert term.lower() in text.lower(), f"Mapping missing diagram type: {term}"
    assert "activity" in text.lower(), "behavior-flow must allow activity as alternative"


def test_guide_states_docs_figures_convention():
    text = text_of(GUIDE_FILE)
    assert "docs/figures/" in text, "Guide must state the docs/figures/ storage convention"


def test_degradation_rule_documented():
    text = (text_of(SKILL_FILE) + text_of(GUIDE_FILE)).lower()
    assert "degradation" in text or "降级" in text, "Expected renderer-unavailable degradation rule"


def test_figure_output_conventions():
    text = text_of(GUIDE_FILE).lower()
    for needle in ["png", "svg", ".puml", "caption"]:
        assert needle in text, f"Guide must state figure output convention: {needle}"


# ---------------------------------------------------------------------------
# C-17/C-20 + SC-007 regression guard
# ---------------------------------------------------------------------------

def test_mermaid_scoped_to_secondary_content():
    body = _section(text_of(SKILL_FILE), "## Output Requirements")
    assert "UML" in body, "Output Requirements must declare UML as primary-view standard"
    lowered = body.lower()
    assert "secondary" in lowered or "次要" in body, "Mermaid must be scoped to secondary content"


def test_deliverable_location_unchanged():
    text = text_of(SKILL_FILE)
    assert _baseline()["deliverable_statement"] in text, (
        "Deliverable statement $WORK_DIR/docs/overview.md must remain (SC-007)"
    )


def test_baseline_sections_preserved():
    text = text_of(SKILL_FILE)
    missing = [h for h in _baseline()["required_headings"] if h not in text]
    assert not missing, f"Baseline sections removed (SC-007): {missing}"


def test_reference_guides_preserved():
    for guide in _baseline()["reference_guides"]:
        assert (SKILL_DIR / "references" / guide).exists(), f"Missing baseline guide: {guide}"


def test_primary_view_coverage_statement():
    text = text_of(SKILL_FILE) + text_of(GUIDE_FILE)
    assert "architecture" in text.lower() or "结构" in text, "Primary structural view coverage required"
    assert "deployment" in text.lower() or "部署" in text, "Primary deployment view coverage required"
