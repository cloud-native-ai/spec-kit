"""Unit tests for InitializationResultSummary categorization.

Validates the structured summary model used by init and refresh operations.
"""

from specify_cli import InitializationResultSummary


class TestInitializationResultSummary:
    def test_empty_summary_is_empty(self):
        s = InitializationResultSummary()
        assert s.is_empty()

    def test_add_created(self):
        s = InitializationResultSummary()
        s.add_created("file1.md", "file2.md")
        assert not s.is_empty()
        assert "file1.md" in s.created
        assert "file2.md" in s.created
        assert len(s.created) == 2

    def test_add_reused(self):
        s = InitializationResultSummary()
        s.add_reused(".specify/memory/features.md")
        assert ".specify/memory/features.md" in s.reused

    def test_add_skipped(self):
        s = InitializationResultSummary()
        s.add_skipped(".gitignore")
        assert ".gitignore" in s.skipped

    def test_add_preserved(self):
        s = InitializationResultSummary()
        s.add_preserved(".specify/instructions.md")
        assert ".specify/instructions.md" in s.preserved

    def test_add_conflict(self):
        s = InitializationResultSummary()
        s.add_conflict(".claude/commands/custom.md")
        assert ".claude/commands/custom.md" in s.conflicts

    def test_add_attention(self):
        s = InitializationResultSummary()
        s.add_attention("Claude Code CLI not found")
        assert "Claude Code CLI not found" in s.attention_required

    def test_set_configured_assistants(self):
        s = InitializationResultSummary()
        s.set_configured_assistants(["copilot", "claude"])
        assert s.configured_assistants == ["copilot", "claude"]

    def test_to_dict_includes_all_categories(self):
        s = InitializationResultSummary()
        s.add_created("a")
        s.add_reused("b")
        s.add_skipped("c")
        s.add_preserved("d")
        s.add_conflict("e")
        s.add_attention("warning")
        s.set_configured_assistants(["copilot"])

        d = s.to_dict()
        assert d["created"] == ["a"]
        assert d["reused"] == ["b"]
        assert d["skipped"] == ["c"]
        assert d["preserved"] == ["d"]
        assert d["conflicts"] == ["e"]
        assert d["attention_required"] == ["warning"]
        assert d["configured_assistants"] == ["copilot"]

    def test_render_rich_contains_categories(self):
        s = InitializationResultSummary()
        s.add_created("test.md")
        s.add_reused("existing.md")
        rendered = s.render_rich()
        assert "Created" in rendered
        assert "test.md" in rendered
        assert "Reused" in rendered
        assert "existing.md" in rendered

    def test_multiple_entries_per_category(self):
        s = InitializationResultSummary()
        s.add_conflict("a.txt", "b.txt", "c.txt")
        assert len(s.conflicts) == 3
        assert s.conflicts == ["a.txt", "b.txt", "c.txt"]
