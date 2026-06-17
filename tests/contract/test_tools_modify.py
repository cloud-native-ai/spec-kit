"""Contract tests for tool definition modification — T023."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule


def test_modify_preserves_unmodified_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="build-docs",
            tool_type="project-script",
            source_identifier="scripts/bash/build-docs.sh",
            description="Builds project documentation from markdown sources",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="run from repo root"),
            ],
        )
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "build-docs")
        assert loaded is not None
        original_name = loaded.name
        original_type = loaded.tool_type
        original_source = loaded.source_identifier

        loaded.behavioral_rules.append(
            BehavioralRule(keyword="SHOULD", constraint_text="generate a table of contents")
        )
        tools_utils.save_record(tools_dir, loaded)

        reloaded = tools_utils.load_record(tools_dir, "build-docs")
        assert reloaded is not None
        assert reloaded.name == original_name
        assert reloaded.tool_type == original_type
        assert reloaded.source_identifier == original_source
        assert len(reloaded.behavioral_rules) == 2


def test_modify_nonexistent_tool_returns_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        loaded = tools_utils.load_record(tools_dir, "nonexistent-tool")
        assert loaded is None


def test_modify_clearing_mandatory_field_causes_validation_error():
    record = ToolRecord(
        name="my-tool",
        tool_type="system-binary",
        source_identifier="/usr/bin/my-tool",
        description="",
    )
    errors = record.validate_strict()
    assert any("description is required" in e for e in errors)
