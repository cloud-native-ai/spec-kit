"""Contract tests for tool definition view and list — T035, T036."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule


def test_view_returns_all_fields_including_behavioral_rules():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="jq-tool",
            tool_type="system-binary",
            source_identifier="/usr/bin/jq",
            description="JSON processor for API responses",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="use --raw-output for strings"),
            ],
            aliases=["jq", "json-query"],
            discovery_origin="discovery-assisted",
        )
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "jq-tool")
        assert loaded is not None
        assert loaded.name == "jq-tool"
        assert loaded.tool_type == "system-binary"
        assert loaded.source_identifier == "/usr/bin/jq"
        assert loaded.description == "JSON processor for API responses"
        assert len(loaded.behavioral_rules) == 1
        assert loaded.behavioral_rules[0].keyword == "MUST"
        assert loaded.discovery_origin == "discovery-assisted"


def test_view_returns_404_when_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        loaded = tools_utils.load_record(tools_dir, "nonexistent")
        assert loaded is None


def test_list_returns_summary_for_multiple_tools():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)

        for tool_info in [
            ("build-docs", "project-script", "scripts/build.sh", "Builds docs"),
            ("jq", "system-binary", "/usr/bin/jq", "JSON processor"),
            ("my-func", "shell-function", "my_func", "Custom shell function"),
        ]:
            record = ToolRecord(
                name=tool_info[0],
                tool_type=tool_info[1],
                source_identifier=tool_info[2],
                description=tool_info[3],
            )
            tools_utils.save_record(tools_dir, record)

        tool_files = list(tools_dir.glob("*.md"))
        assert len(tool_files) == 3

        summaries = []
        for tf in sorted(tool_files):
            loaded = tools_utils.load_record(tools_dir, tf.stem)
            if loaded:
                summaries.append({
                    "name": loaded.name,
                    "tool_type": loaded.tool_type,
                    "description": loaded.description,
                    "status": loaded.status,
                })
        assert len(summaries) == 3
        assert all("name" in s and "tool_type" in s and "description" in s for s in summaries)
