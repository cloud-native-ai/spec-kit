from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord


def test_source_specific_tool_records_validate_for_all_supported_types():
    source_types = ["mcp", "system", "shell", "project"]
    records = [
        ToolRecord(
            name=f"demo-{source_type}",
            tool_type=source_type,
            source_identifier=f"source/{source_type}",
            description="demo",
        )
        for source_type in source_types
    ]

    for record in records:
        assert record.validate() == []
