"""Structural contract tests for the evidence-step convention and its consumers.

Spec 034 US4/US5 — collect-evidence skill, evidence-step.md single source of truth,
and the three improve-* skill integrations (contracts C-B7, FR-008..FR-010).
"""

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

COLLECT_SKILL = REPO_ROOT / "skills" / "collect-evidence" / "SKILL.md"
COLLECT_SKILL_MIRROR = REPO_ROOT / ".specify" / "skills" / "collect-evidence" / "SKILL.md"
CONTRACT_REF = REPO_ROOT / "skills" / "collect-evidence" / "references" / "evidence-contract.md"
DISCIPLINE_REF = REPO_ROOT / "skills" / "collect-evidence" / "references" / "evidence-discipline.md"
EVIDENCE_STEP = REPO_ROOT / ".specify" / "shared" / "workflow" / "evidence-step.md"
EVIDENCE_STEP_SRC = REPO_ROOT / "shared" / "workflow" / "evidence-step.md"

IMPROVE_SKILLS = {
    "improve-skills": REPO_ROOT / "skills" / "improve-skills" / "SKILL.md",
    "improve-agent": REPO_ROOT / "skills" / "improve-agent" / "SKILL.md",
    "improve-team": REPO_ROOT / "skills" / "improve-team" / "SKILL.md",
}

SEVEN_STATES = [
    "Present", "Wired", "Exercised", "Outcome-supported",
    "Missing", "Unobserved", "Not applicable",
]

# Verdict-language ban for the neutral evidence layer (Chinese + English markers).
VERDICT_PATTERNS = [
    r"severity", r"aiFixPrompt", r"修复方案", r"严重度", r"优先级排序",
]


class TestCollectEvidenceSkill:
    def test_skill_exists_with_frontmatter(self):
        assert COLLECT_SKILL.is_file()
        text = COLLECT_SKILL.read_text(encoding="utf-8")
        assert text.startswith("---")
        for field in ("name: collect-evidence", "description:", "skill_id:"):
            assert field in text.split("---")[1], field

    def test_under_500_lines(self):
        assert len(COLLECT_SKILL.read_text(encoding="utf-8").splitlines()) <= 500

    def test_orchestration_steps_present(self):
        text = COLLECT_SKILL.read_text(encoding="utf-8")
        for marker in ("范围解析", "doctor", "collect", "边界申明"):
            assert marker in text, marker

    def test_feedback_section_present(self):
        assert "## Feedback" in COLLECT_SKILL.read_text(encoding="utf-8")

    def test_neutrality_no_verdict_language(self):
        text = COLLECT_SKILL.read_text(encoding="utf-8")
        for pattern in VERDICT_PATTERNS:
            assert not re.search(pattern, text, re.I), pattern

    def test_mirror_identical(self):
        assert COLLECT_SKILL_MIRROR.is_file(), "mirror missing"
        assert COLLECT_SKILL.read_bytes() == COLLECT_SKILL_MIRROR.read_bytes()

    def test_references_exist(self):
        assert CONTRACT_REF.is_file()
        assert DISCIPLINE_REF.is_file()


class TestEvidenceDiscipline:
    def test_seven_states_defined(self):
        text = DISCIPLINE_REF.read_text(encoding="utf-8")
        for state in SEVEN_STATES:
            assert state in text, state

    def test_four_disciplines_present(self):
        text = DISCIPLINE_REF.read_text(encoding="utf-8")
        for marker in ("配置存在", "Unobserved", "计数", "隐私"):
            assert marker in text, marker

    def test_subset_boundary_sentence(self):
        text = DISCIPLINE_REF.read_text(encoding="utf-8")
        assert "只进事实" in text and "不进观点" in text


class TestEvidenceStepConvention:
    def test_canonical_file_exists(self):
        assert EVIDENCE_STEP.is_file()

    def test_mirrored_to_source_side(self):
        assert EVIDENCE_STEP_SRC.is_file(), "shared/workflow mirror missing"
        assert EVIDENCE_STEP.read_bytes() == EVIDENCE_STEP_SRC.read_bytes()

    def test_triage_rules_present(self):
        text = EVIDENCE_STEP.read_text(encoding="utf-8")
        assert "Exercised" in text and "Outcome-supported" in text
        assert "Missing" in text
        assert "候选" in text and "冻结" in text

    def test_unobserved_red_line(self):
        text = EVIDENCE_STEP.read_text(encoding="utf-8")
        assert re.search(r"Unobserved.*(禁止|不得|MUST NOT)", text, re.S)

    def test_counting_rule(self):
        text = EVIDENCE_STEP.read_text(encoding="utf-8")
        assert re.search(r"计数.*(不得|禁止|MUST NOT)", text, re.S)


class TestImproveSkillIntegration:
    """US5 assertions (enabled by T029)."""

    @pytest.fixture(params=list(IMPROVE_SKILLS.items()), ids=list(IMPROVE_SKILLS))
    def skill(self, request):
        name, path = request.param
        return name, path, path.read_text(encoding="utf-8")

    def test_references_evidence_step(self, skill):
        name, path, text = skill
        assert "evidence-step.md" in text, f"{name} must reference the single source of truth"

    def test_unobserved_red_line_present(self, skill):
        name, path, text = skill
        assert "Unobserved" in text, name

    def test_under_500_lines(self, skill):
        name, path, text = skill
        assert len(text.splitlines()) <= 500, name

    def test_mirror_identical(self, skill):
        name, path, text = skill
        mirror = REPO_ROOT / ".specify" / "skills" / name / "SKILL.md"
        assert mirror.is_file(), f"{name} mirror missing"
        assert path.read_bytes() == mirror.read_bytes()

    def test_improve_team_consumes_runs_lane_not_raw_artifacts(self):
        text = IMPROVE_SKILLS["improve-team"].read_text(encoding="utf-8")
        assert "runs" in text and "findings" in text
        # Raw-artifact parsing instructions must be gone; mentions must only appear
        # as lane-source descriptions (behind evidence-utils), not as direct reads.
        direct_read = re.search(
            r"(read|parse|读取|解析)[^。\n]{0,60}(STATE\.md|run-log\.jsonl)", text, re.I)
        assert not direct_read, f"improve-team still instructs direct artifact parsing: {direct_read.group(0)!r}"
