"""Contract tests for discovery-assisted draft creation — T015."""

from tests.script_api import tools_utils

DiscoveryDraft = tools_utils.DiscoveryDraft
BehavioralRule = tools_utils.BehavioralRule


def test_discovery_draft_includes_draft_label():
    draft = DiscoveryDraft(
        proposed_name="jq",
        proposed_type="system-binary",
        proposed_source="/usr/bin/jq",
        proposed_description="JSON processor",
    )
    assert draft.draft_label == "Draft — pending user confirmation"


def test_discovery_draft_converts_to_record_with_discovery_origin():
    draft = DiscoveryDraft(
        proposed_name="jq",
        proposed_type="system-binary",
        proposed_source="/usr/bin/jq",
        proposed_description="JSON processor",
    )
    record = draft.to_record()
    assert record.name == "jq"
    assert record.tool_type == "system-binary"
    assert record.source_identifier == "/usr/bin/jq"
    assert record.description == "JSON processor"
    assert record.discovery_origin == "discovery-assisted"
    assert record.status == "Draft"


def test_discovery_draft_not_persisted_without_confirmation():
    """Draft records have status 'Draft' and must be explicitly confirmed
    before they can be marked 'Verified'."""
    draft = DiscoveryDraft(
        proposed_name="curl",
        proposed_type="system-binary",
        proposed_source="/usr/bin/curl",
        proposed_description="HTTP client",
    )
    record = draft.to_record()
    assert record.status == "Draft"
    errors = record.validate_strict()
    assert not any("name" in e for e in errors)


def test_discovery_draft_confidence_levels():
    for level in ("high", "medium", "low"):
        draft = DiscoveryDraft(
            proposed_name="test",
            proposed_type="system-binary",
            proposed_source="/usr/bin/test",
            proposed_description="Test",
            confidence=level,
        )
        assert draft.confidence == level
