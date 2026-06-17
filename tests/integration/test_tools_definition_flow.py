"""Integration test for end-to-end tool definition flow — T014."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule


def test_end_to_end_definition_creates_record_with_correct_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir) / ".specify" / "memory" / "tools"
        tools_dir.mkdir(parents=True)

        record = ToolRecord(
            name="build-docs",
            tool_type="project-script",
            source_identifier="scripts/bash/build-docs.sh",
            description="Builds project documentation from markdown sources",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="run from the repository root directory"),
                BehavioralRule(keyword="MUST NOT", constraint_text="modify source files"),
            ],
            discovery_origin="manual-entry",
        )

        saved_path = tools_utils.save_record(tools_dir, record)
        assert saved_path.exists()
        assert saved_path.name == "build-docs.md"

        content = saved_path.read_text(encoding="utf-8")
        assert "## Behavioral Rules" in content
        assert "- MUST run from the repository root directory" in content
        assert "- MUST NOT modify source files" in content
        assert "**Discovery Origin**: manual-entry" in content
        assert "**Tool Type**: `project-script`" in content


def test_definition_flow_status_transitions():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir) / ".specify" / "memory" / "tools"
        tools_dir.mkdir(parents=True)

        record = ToolRecord(
            name="test-tool",
            tool_type="project-script",
            source_identifier="scripts/test.sh",
            description="A test tool",
        )
        assert record.status == "Draft"

        errors = record.validate_strict()
        assert not errors
        record.status = "Verified"
        errors_verified = record.validate_strict()
        assert any("arguments or returns" in e for e in errors_verified)

        record.arguments = [
            tools_utils.ToolArgument(
                name="format", type="string", required=False,
                description="Output format", default="json",
            )
        ]
        errors_final = record.validate_strict()
        assert not errors_final


def test_load_record_preserves_behavioral_rules():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)

        record = ToolRecord(
            name="my-tool",
            tool_type="system-binary",
            source_identifier="/usr/bin/my-tool",
            description="My test tool",
            behavioral_rules=[
                BehavioralRule(keyword="SHOULD", constraint_text="use verbose output"),
                BehavioralRule(keyword="SHOULD NOT", constraint_text="write to stdout without redirect"),
            ],
            discovery_origin="discovery-assisted",
        )
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "my-tool")
        assert loaded is not None
        assert len(loaded.behavioral_rules) == 2
        assert loaded.behavioral_rules[0].keyword == "SHOULD"
        assert loaded.behavioral_rules[0].constraint_text == "use verbose output"
        assert loaded.behavioral_rules[1].keyword == "SHOULD NOT"
        assert loaded.discovery_origin == "discovery-assisted"


def test_definition_registers_tool_id():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir) / ".specify" / "memory" / "tools"
        tools_dir.mkdir(parents=True)

        record = ToolRecord(
            name="indexed-tool",
            tool_type="shell-function",
            source_identifier="my_func",
            description="A shell function",
        )
        tools_utils.save_record(tools_dir, record)
        assert record.tool_id is not None
        assert "indexed-tool" in record.tool_id
