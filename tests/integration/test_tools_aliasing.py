import pytest

from scripts.python.tool_models import ToolRecord
from scripts.python.tool_record_utils import add_alias, rename_record, resolve_alias


def test_tool_aliasing_workflow_resolves_alias_to_canonical_record():
    record = ToolRecord(
        name="git-status",
        tool_type="system",
        source_identifier="/usr/bin/git",
        description="Show git status",
    )
    add_alias(record, "gs")

    resolved, alias = resolve_alias("gs", [record])
    assert resolved is not None
    assert resolved.name == "git-status"
    assert alias == "gs"


def test_rename_record_detects_conflict(tmp_path):
    tools_dir = tmp_path / ".specify" / "memory" / "tools"
    record_a = ToolRecord(
        name="git-status",
        tool_type="system",
        source_identifier="/usr/bin/git",
        description="status",
    )
    record_b = ToolRecord(
        name="git-log",
        tool_type="system",
        source_identifier="/usr/bin/git",
        description="log",
    )

    with pytest.raises(ValueError):
        rename_record(tools_dir, record_a, "git-log", [record_a, record_b])
