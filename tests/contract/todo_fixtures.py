"""
Test fixtures and helpers for /speckit.todo contract tests
"""

import json
import subprocess
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "todo-workspaces"


@pytest.fixture
def valid_workspace():
    """Returns path to valid workspace fixture"""
    return str(FIXTURES_DIR / "valid")


@pytest.fixture
def malformed_workspace():
    """Returns path to malformed workspace fixture"""
    return str(FIXTURES_DIR / "malformed")


@pytest.fixture
def empty_workspace():
    """Returns path to empty workspace fixture"""
    return str(FIXTURES_DIR / "empty")


@pytest.fixture
def negative_workspace():
    """Returns path to negative workspace fixture (non-SPECKIT TODOs)"""
    return str(FIXTURES_DIR / "negative")


@pytest.fixture
def oversized_workspace():
    """Returns path to oversized workspace fixture (>10 TODO blocks)"""
    return str(FIXTURES_DIR / "oversized")


@pytest.fixture
def search_todo_script():
    """Returns absolute path to search-todo.sh script"""
    script = (
        Path(__file__).parent.parent.parent.parent
        / ".specify"
        / "scripts"
        / "bash"
        / "search-todo.sh"
    )
    return str(script)


def run_search_todo(workspace: str, json_mode: bool = False, **kwargs) -> dict:
    """
    Run search-todo.sh against a workspace and return parsed output.

    Args:
        workspace: Path to workspace directory
        json_mode: If True, pass --json flag
        **kwargs: Additional flags (--exclude, --context-depth, etc.)

    Returns:
        dict with keys: exit_code, stdout_json (if json_mode), stdout_lines

    Raises:
        subprocess.CalledProcessError if script not found
    """
    script = (
        Path(workspace).parent.parent.parent.parent.parent
        / ".specify"
        / "scripts"
        / "bash"
        / "search-todo.sh"
    )
    if not script.exists():
        script = (
            Path(__file__).parent.parent.parent.parent
            / ".specify"
            / "scripts"
            / "bash"
            / "search-todo.sh"
        )

    cmd = [str(script), workspace]
    if json_mode:
        cmd.insert(1, "--json")

    for flag, value in kwargs.items():
        cmd.extend([f"--{flag}", str(value)])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    output = {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

    if json_mode and result.returncode == 0:
        try:
            output["stdout_json"] = json.loads(result.stdout.strip())
        except json.JSONDecodeError as e:
            output["json_parse_error"] = str(e)
            output["stdout_json"] = None

    if not json_mode:
        output["stdout_lines"] = (
            result.stdout.strip().split("\n") if result.stdout else []
        )

    return output


def validate_json_schema(data: dict) -> bool:
    """Validate that JSON output matches contract §4.2 schema"""
    required_top_keys = {
        "repository",
        "branch",
        "scanned_at",
        "counters",
        "blocks",
        "malformed",
        "excluded_files",
    }
    if not all(k in data for k in required_top_keys):
        return False

    # Validate counters structure
    if "counters" in data:
        counter_keys = {
            "total_files_scanned",
            "total_blocks_found",
            "malformed_blocks",
            "excluded_files_count",
        }
        if not all(k in data["counters"] for k in counter_keys):
            return False

    # Validate blocks structure
    if "blocks" in data and isinstance(data["blocks"], list):
        block_keys = {
            "block_id",
            "source_file",
            "opening_line",
            "closing_line",
            "content",
            "context_heading",
            "prologue",
            "epilogue",
        }
        for block in data["blocks"]:
            if not all(k in block for k in block_keys):
                return False

    # Validate malformed structure
    if "malformed" in data and isinstance(data["malformed"], list):
        malformed_keys = {
            "source_file",
            "opening_line",
            "reason",
            "content_snippet",
            "line_after_eof",
        }
        for mf in data["malformed"]:
            if not all(k in mf for k in malformed_keys):
                return False

    return True
