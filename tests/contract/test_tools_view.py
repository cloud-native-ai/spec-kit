"""Contract tests for tool definition persistence: view, list, and modify — T023, T035, T036.

Everything here drives the real ``save_record`` / ``load_record`` pair against a
temporary tools directory, so the markdown serialization format is exercised rather
than assumed. ``test_tools_define.py`` owns the in-memory validation rules; this file
owns what survives a write/read cycle.
"""

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


def test_modify_preserves_unmodified_fields():
    """T023: re-saving a loaded record after editing one field keeps the others."""
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


def test_behavioral_rules_roundtrip_in_declared_order():
    """Multiple rules survive the markdown round trip in the order they were declared.

    A single-rule record cannot distinguish "ordered" from "kept the only one"; the
    per-keyword assertions below catch a serializer that sorts, dedupes or drops.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="deploy-hook",
            tool_type="webhook",
            source_identifier="https://deploy.example.com/api/v1/deploy",
            description="Triggers production deployment via webhook",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="include Authorization header with bearer token"),
                BehavioralRule(keyword="MUST NOT", constraint_text="invoke more than once per deployment cycle"),
                BehavioralRule(keyword="SHOULD", constraint_text="verify response status is 200 before reporting success"),
            ],
            discovery_origin="manual-entry",
        )
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "deploy-hook")
        assert loaded is not None
        assert loaded.name == "deploy-hook"
        assert loaded.tool_type == "webhook"
        assert loaded.source_identifier == "https://deploy.example.com/api/v1/deploy"
        assert len(loaded.behavioral_rules) == 3
        assert loaded.behavioral_rules[0].keyword == "MUST"
        assert loaded.behavioral_rules[1].keyword == "MUST NOT"
        assert loaded.behavioral_rules[2].keyword == "SHOULD"


def test_saved_markdown_carries_type_and_source():
    """The written file itself — not just the record re-parsed from it — carries the
    tool type and the source identifier verbatim, so a human reader and ``load_record``
    cannot drift apart."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="notify-slack",
            tool_type="webhook",
            source_identifier="https://hooks.slack.com/services/T00/B00/xxx",
            description="Sends a notification to Slack channel",
        )
        tools_utils.save_record(tools_dir, record)

        content = (tools_dir / "notify-slack.md").read_text(encoding="utf-8")
        assert "**Tool Type**: `webhook`" in content
        assert "https://hooks.slack.com/services/T00/B00/xxx" in content
