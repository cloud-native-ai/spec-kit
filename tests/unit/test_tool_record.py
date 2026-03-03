from scripts.python.tool_models import ToolInvocationSession, ToolRecord


def test_tool_record_requires_core_fields():
    record = ToolRecord(
        name="",
        tool_type="invalid",
        source_identifier="",
        description="",
    )
    errors = record.validate()
    assert errors
    assert any("name is required" in error for error in errors)
    assert any("tool_type" in error for error in errors)


def test_verified_tool_record_requires_arguments_or_returns():
    record = ToolRecord(
        name="valid-tool",
        tool_type="mcp",
        source_identifier="server/tool",
        description="valid",
        status="Verified",
    )
    errors = record.validate()
    assert any("Verified record must include arguments or returns" in error for error in errors)


def test_invocation_session_cancellation_rule():
    session = ToolInvocationSession(
        requested_name="tool",
        resolved_name="tool",
        resolved_type="mcp",
        used_existing_record=True,
        disambiguation_required=False,
        user_confirmed_execution=False,
        result_status="success",
        result_summary="unexpected",
    )
    errors = session.validate()
    assert any("result_status must be cancelled" in error for error in errors)
