from pathlib import Path

from scripts.python.tool_models import ToolArgument, ToolRecord
from scripts.python.tool_record_utils import load_record, save_record


def test_record_creation_and_reuse_flow(tmp_path: Path):
    tools_dir = tmp_path / ".specify" / "memory" / "tools"
    record = ToolRecord(
        name="kubectl-get-pods",
        tool_type="system",
        source_identifier="/usr/bin/kubectl",
        description="List pods",
        arguments=[
            ToolArgument(
                name="namespace",
                type="string",
                required=False,
                description="Kubernetes namespace",
            )
        ],
    )

    save_record(tools_dir, record)
    reused = load_record(tools_dir, "kubectl-get-pods")

    assert reused is not None
    assert reused.name == record.name
    assert reused.source_identifier == record.source_identifier
