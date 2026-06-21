"""Unit test for init summary tier reporting (T045).

Assert InitializationResultSummary.assistant_tiers populated correctly.
"""

from specify_cli import InitializationResultSummary


def test_set_configured_assistants_populates_tiers():
    summary = InitializationResultSummary()
    summary.set_configured_assistants(["claude", "codex", "qwen"])

    assert summary.assistant_tiers == {
        "claude": "tier1",
        "codex": "tier1",
        "qwen": "tier2",
    }


def test_render_rich_includes_tier_labels():
    summary = InitializationResultSummary()
    summary.set_configured_assistants(["claude", "codex", "qwen"])
    summary.add_created(".codex/commands")

    output = summary.render_rich()
    assert "Tier 1" in output
    assert "Tier 2" in output


def test_to_dict_includes_assistant_tiers():
    summary = InitializationResultSummary()
    summary.set_configured_assistants(["codex"])

    data = summary.to_dict()
    assert "assistant_tiers" in data
    assert data["assistant_tiers"] == {"codex": "tier1"}
