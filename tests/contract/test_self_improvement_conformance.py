"""Contract tests for the shared Self-Improvement model."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DEFINITION = ROOT / "shared/definitions/self-improvement-definitions.md"
GUIDELINE = ROOT / "shared/guidelines/self-improvement.md"
PATTERN = ROOT / "shared/patterns/self-improvement-pattern.md"
WORKFLOW = ROOT / "shared/workflow/self-improvement-workflow.md"

CREATE_SKILLS = {
    "create-agent",
    "create-docs",
    "create-pages",
    "create-skills",
    "create-team",
    "create-tools",
}
IMPROVE_SKILLS = {
    "improve-agent",
    "improve-docs",
    "improve-skills",
    "improve-team",
    "improve-tools",
}
SUBJECT_CREATORS = {
    "create-agent": "improve-agent",
    "create-skills": "improve-skills",
    "create-team": "improve-team",
    "create-tools": "improve-tools",
}
NON_SUBJECT_FLOWS = {"create-docs", "create-pages", "improve-docs"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_c1_canonical_documents_exist_with_declared_ownership():
    for path in (DEFINITION, GUIDELINE, PATTERN, WORKFLOW):
        assert path.is_file(), f"missing canonical Self-Improvement document: {path}"
    assert "Single source of truth" in read(DEFINITION)
    assert "Single source of truth" in read(GUIDELINE)
    assert "Single source of truth" in read(WORKFLOW)


def test_c2_definition_distinguishes_self_and_assisted_improvement():
    text = " ".join(read(DEFINITION).split())
    for term in (
        "Execution Subject",
        "Self-Improvement（自我提升）",
        "Assisted Improvement（他者辅助提升）",
        "initiating signal and target share the same durable subject identity",
        "who owns the initiating decision",
    ):
        assert term in text


def test_c3_core_mechanisms_reference_the_model_without_redefining_evidence():
    better_harness = read(ROOT / "shared/guidelines/better-harness.md")
    feedback = read(ROOT / "shared/workflow/feedback-step.md")
    evidence = read(ROOT / "shared/workflow/evidence-step.md")
    assert "self-improvement-definitions.md" in better_harness
    assert "self-improvement-workflow.md" in better_harness
    assert "self-improvement-definitions.md" in feedback
    assert "optional observation sensor" in feedback
    assert "self-improvement-workflow.md" in evidence
    assert "不得重定义 evidenceState" in evidence


def test_c4_canonical_shared_files_are_mirrored_byte_identically():
    for source in (DEFINITION, GUIDELINE, PATTERN, WORKFLOW):
        rel = source.relative_to(ROOT / "shared")
        mirror = ROOT / ".specify/shared" / rel
        assert mirror.is_file(), f"missing shared mirror: {mirror}"
        assert source.read_bytes() == mirror.read_bytes(), f"shared mirror drift: {rel}"


def test_c5_all_create_and_improve_skills_reference_canonical_workflow():
    discovered_create = {path.parent.name for path in (ROOT / "skills").glob("create-*/SKILL.md")}
    discovered_improve = {path.parent.name for path in (ROOT / "skills").glob("improve-*/SKILL.md")}
    assert CREATE_SKILLS <= discovered_create
    assert IMPROVE_SKILLS <= discovered_improve
    for name in sorted(discovered_create | discovered_improve):
        text = read(ROOT / "skills" / name / "SKILL.md")
        assert ".specify/shared/workflow/self-improvement-workflow.md" in text, name


def test_c6_subject_creators_install_a_self_improvement_contract():
    for creator, improver in SUBJECT_CREATORS.items():
        text = read(ROOT / "skills" / creator / "SKILL.md")
        assert "Self-Improvement Contract" in text, creator
        assert improver in text, creator
    assert (ROOT / "skills/create-agent/templates/agent-self-improvement.md").is_file()
    assert (ROOT / "skills/create-tools/templates/tool-self-improvement.md").is_file()
    assert "## Self-Improvement Contract" in read(
        ROOT / "skills/create-team/references/create-mode.md"
    )


def test_c7_non_subject_flows_do_not_claim_artifact_self_improvement():
    for name in NON_SUBJECT_FLOWS:
        text = read(ROOT / "skills" / name / "SKILL.md")
        assert "Execution Subject" in text and "by default" in text, name
        assert "Assisted Improvement" in text, name


def test_c8_improvers_classify_origin_and_defer_outcome_claims():
    for name in sorted(IMPROVE_SKILLS - {"improve-docs"}):
        text = read(ROOT / "skills" / name / "SKILL.md")
        assert "Assisted Improvement" in text, name
        assert "origin=`self`" in text, name
        assert "outcome" in text.lower() and "pending" in text.lower(), name


def test_c9_create_tools_engines_compose_the_contract_fragment():
    shell_script = read(ROOT / "scripts/bash/create-new-tools.sh")
    python_engine = read(ROOT / "scripts/python/tools-utils.py")
    assert "tool-self-improvement.md" in shell_script
    assert 'cat "$self_improvement_template" >> "$record_file"' in shell_script
    assert "tool-self-improvement.md" in python_engine
    assert "_self_improvement_contract()" in python_engine


def test_c10_runtime_skill_mirrors_are_current():
    names = {
        path.parent.name
        for pattern in ("create-*/SKILL.md", "improve-*/SKILL.md")
        for path in (ROOT / "skills").glob(pattern)
    }
    for name in sorted(names):
        source = ROOT / "skills" / name / "SKILL.md"
        mirror = ROOT / ".specify/skills" / name / "SKILL.md"
        assert mirror.is_file(), f"missing Skill mirror: {name}"
        assert source.read_bytes() == mirror.read_bytes(), f"Skill mirror drift: {name}"
