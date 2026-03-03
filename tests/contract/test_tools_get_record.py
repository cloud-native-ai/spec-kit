from pathlib import Path

from scripts.python.tool_models import ToolRecord
from scripts.python.tool_record_utils import load_record, save_record


def test_get_record_contract_returns_existing_record(tmp_path: Path):
    tools_dir = tmp_path / ".specify" / "memory" / "tools"
    record = ToolRecord(
        name="git-status",
        tool_type="system",
        source_identifier="/usr/bin/git",
        description="Show git status",
    )
    save_record(tools_dir, record)

    loaded = load_record(tools_dir, "git-status")
    assert loaded is not None
    assert loaded.name == "git-status"
    assert loaded.tool_type == "system"
