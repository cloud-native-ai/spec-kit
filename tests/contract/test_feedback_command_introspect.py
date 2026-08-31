"""Structural contract test: /speckit.feedback Mode 5 introspect (req 047).

Pins contracts/command-mode.md against templates/commands/feedback.md and the
four regenerated per-tool copies. C-1..C-3 + C-5/C-6/C-7 land in US1 (T006);
C-4/C-8 land in US2 (T010); C-9/C-10 land in US3 (T014).
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "feedback.md"
COPIES = [
    ROOT / ".claude" / "commands" / "speckit.feedback.md",
    ROOT / ".qoder" / "commands" / "speckit.feedback.md",
    ROOT / ".opencode" / "command" / "speckit.feedback.md",
    ROOT / ".github" / "prompts" / "speckit.feedback.prompt.md",
]


def _template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


@pytest.mark.contract
class TestMode5PresenceAndPosition:
    """C-1..C-3: trigger keyword, section presence/position, description lines."""

    def test_mode5_section_present_before_mode4(self):
        text = _template_text()
        mode5 = text.find("### Mode 5")
        mode4 = text.find("### Mode 4")
        assert mode5 > 0, "Mode 5 section missing"
        assert mode4 > 0, "Mode 4 section missing"
        assert mode5 < mode4, "Mode 5 must precede Mode 4 (Mode 4 stays last)"

    def test_introspect_trigger_keyword_documented(self):
        text = _template_text()
        assert "introspect" in text

    def test_description_lines_mention_introspection(self):
        text = _template_text()
        head = text.split("---")[1] if text.startswith("---") else text[:600]
        assert "five execution modes" in head or "Mode 5" in head
        assert "自省" in head


@pytest.mark.contract
class TestMode5Discipline:
    """C-5/C-6/C-7: token discipline + red lines + external-never-upstream."""

    def test_token_efficiency_note(self):
        assert "摘要优先" in _template_text() or "Token 效率" in _template_text()

    def test_red_lines_stated(self):
        text = _template_text()
        mode5 = text[text.find("### Mode 5"):]
        assert "MUST NOT" in mode5 or "禁止" in mode5
        assert "自动传输" in mode5

    def test_external_never_upstream(self):
        mode5 = _template_text()[_template_text().find("### Mode 5"):]
        assert "local-sink" in mode5
        assert "external" in mode5.lower()


@pytest.mark.contract
class TestGeneratedCopies:
    """Mirror Obligations row 2: all four per-tool copies carry Mode 5."""

    @pytest.mark.parametrize("copy", COPIES, ids=[p.parts[-2] for p in COPIES])
    def test_copy_contains_mode5(self, copy: Path):
        assert copy.exists(), f"missing generated copy: {copy}"
        assert "### Mode 5" in copy.read_text(encoding="utf-8")


@pytest.mark.contract
class TestMode5FlowCompleteness:
    """C-4/C-8 (land in US2 via T010): five-step order + re-introspection rule."""

    def _mode5(self) -> str:
        text = _template_text()
        return text[text.find("### Mode 5"):text.find("### Mode 4")]

    def test_five_steps_in_order(self):
        mode5 = self._mode5()
        steps = ["范围快照", "场景化分析", "报告产出", "用户确认", "路由建议"]
        positions = [mode5.find(s) for s in steps]
        assert all(p > 0 for p in positions), \
            f"missing steps: {[s for s, p in zip(steps, positions) if p <= 0]}"
        assert positions == sorted(positions), "steps out of order"

    def test_reintrospection_supersede_rule(self):
        mode5 = self._mode5()
        assert "supersedes" in mode5
        assert "重复自省" in mode5


@pytest.mark.contract
class TestPackagingIntegration:
    """C-9/C-10 (land in US3 via T014): Mode 2 offer + threshold note."""

    def test_mode2_offers_include_introspection(self):
        text = _template_text()
        mode2 = text[text.find("### Mode 2"):text.find("### Mode 3")]
        assert "--include-introspection" in mode2

    def test_threshold_note_suggests_introspect_first(self):
        text = _template_text()
        mode2 = text[text.find("### Mode 2"):text.find("### Mode 3")]
        assert "introspect" in mode2
