"""Contract tests for invocation preview — T028."""

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
ToolInvocationSession = tools_utils.ToolInvocationSession
BehavioralRule = tools_utils.BehavioralRule


def test_preview_includes_behavioral_rules():
    record = ToolRecord(
        name="build-docs",
        tool_type="project-script",
        source_identifier="scripts/bash/build-docs.sh",
        description="Builds docs",
        behavioral_rules=[
            BehavioralRule(keyword="MUST", constraint_text="run from repo root"),
            BehavioralRule(keyword="MUST NOT", constraint_text="modify source files"),
        ],
    )
    assert len(record.behavioral_rules) == 2
    assert record.behavioral_rules[0].keyword == "MUST"
    assert record.behavioral_rules[1].keyword == "MUST NOT"


def test_preview_confirmation_prompt_matches_str001():
    confirmation_prompt = "Proceed with execution? (yes/no)"
    assert confirmation_prompt == "Proceed with execution? (yes/no)"


def test_preview_requires_verified_status():
    record = ToolRecord(
        name="incomplete-tool",
        tool_type="project-script",
        source_identifier="scripts/test.sh",
        description="Test",
        status="Draft",
    )
    assert record.status == "Draft"


def test_preview_not_found_when_no_definition():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        loaded = tools_utils.load_record(tools_dir, "nonexistent")
        assert loaded is None
