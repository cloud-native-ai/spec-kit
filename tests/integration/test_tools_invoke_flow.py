"""Integration test for end-to-end preview-and-invoke flow — T030."""

import tempfile
from pathlib import Path

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule
ToolInvocationSession = tools_utils.ToolInvocationSession


def test_end_to_end_preview_and_invoke_flow():
    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record = ToolRecord(
            name="build-docs",
            tool_type="project-script",
            source_identifier="scripts/bash/build-docs.sh",
            description="Builds project documentation",
            behavioral_rules=[
                BehavioralRule(keyword="MUST", constraint_text="run from repo root"),
                BehavioralRule(keyword="MUST NOT", constraint_text="modify source files"),
            ],
            status="Draft",
        )
        record.arguments = [
            tools_utils.ToolArgument(
                name="format", type="string", required=False,
                description="Output format", default="html",
            )
        ]
        record.status = "Verified"
        tools_utils.save_record(tools_dir, record)

        loaded = tools_utils.load_record(tools_dir, "build-docs")
        assert loaded is not None
        assert len(loaded.behavioral_rules) == 2

        session_confirmed = ToolInvocationSession(
            requested_name="build-docs",
            resolved_name="build-docs",
            resolved_type="project-script",
            used_existing_record=True,
            disambiguation_required=False,
            user_confirmed_execution=True,
            result_status="success",
            result_summary="Documentation built successfully",
        )
        assert not session_confirmed.validate()

        session_declined = ToolInvocationSession(
            requested_name="build-docs",
            resolved_name="build-docs",
            resolved_type="project-script",
            used_existing_record=True,
            disambiguation_required=False,
            user_confirmed_execution=False,
            result_status="cancelled",
            result_summary="User declined",
        )
        assert not session_declined.validate()
