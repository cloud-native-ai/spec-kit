"""Contract tests for webhook tool type."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule


def test_webhook_tool_definition_validates():
    record = ToolRecord(
        name="trigger-build",
        tool_type="webhook",
        source_identifier="https://ci.example.com/api/trigger-build",
        description="Triggers a CI build via webhook",
    )
    errors = record.validate_strict()
    assert not errors


def test_webhook_tool_roundtrip():
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


def test_webhook_tool_persisted_content():
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
