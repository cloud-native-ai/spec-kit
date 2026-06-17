"""Integration test for field-level update preservation — T024."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule


def test_field_level_update_preserves_all_unmodified_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="deploy",
            tool_type="project-script",
            source_identifier="scripts/deploy.sh",
            description="Deploys the application to staging",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="require --env flag"),
                BehavioralRule(keyword="MUST NOT", constraint_text="run with --force in production"),
            ],
            discovery_origin="manual-entry",
        )
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "deploy")
        assert loaded is not None

        snapshot = {
            "name": loaded.name,
            "tool_type": loaded.tool_type,
            "source_identifier": loaded.source_identifier,
            "description": loaded.description,
            "rules_count": len(loaded.behavioral_rules),
        }

        loaded.description = "Deploys the application to staging and production"
        tools_utils.save_record(tools_dir, loaded)

        reloaded = tools_utils.load_record(tools_dir, "deploy")
        assert reloaded is not None
        assert reloaded.name == snapshot["name"]
        assert reloaded.tool_type == snapshot["tool_type"]
        assert reloaded.source_identifier == snapshot["source_identifier"]
        assert reloaded.description == "Deploys the application to staging and production"
        assert len(reloaded.behavioral_rules) == snapshot["rules_count"]
        assert reloaded.behavioral_rules[0].keyword == "MUST"
        assert reloaded.behavioral_rules[1].keyword == "MUST NOT"
