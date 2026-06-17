"""Contract tests for confirmation gate — T029."""

from tests.script_api import tools_utils

ToolInvocationSession = tools_utils.ToolInvocationSession


def test_invoke_forbidden_when_not_confirmed():
    session = ToolInvocationSession(
        requested_name="build-docs",
        resolved_name="build-docs",
        resolved_type="project-script",
        used_existing_record=True,
        disambiguation_required=False,
        user_confirmed_execution=False,
        result_status="success",
        result_summary="unexpected execution",
    )
    errors = session.validate()
    assert any("result_status must be cancelled" in e for e in errors)


def test_invoke_cancelled_when_user_declines():
    session = ToolInvocationSession(
        requested_name="build-docs",
        resolved_name="build-docs",
        resolved_type="project-script",
        used_existing_record=True,
        disambiguation_required=False,
        user_confirmed_execution=False,
        result_status="cancelled",
        result_summary="User declined execution",
    )
    errors = session.validate()
    assert not errors
    assert session.result_status == "cancelled"


def test_invoke_proceeds_when_user_confirms():
    session = ToolInvocationSession(
        requested_name="build-docs",
        resolved_name="build-docs",
        resolved_type="project-script",
        used_existing_record=True,
        disambiguation_required=False,
        user_confirmed_execution=True,
        result_status="success",
        result_summary="Docs built successfully",
    )
    errors = session.validate()
    assert not errors
    assert session.result_status == "success"
