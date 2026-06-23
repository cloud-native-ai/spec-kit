"""
Integration tests for /speckit.todo prompt template behavior.

Tests the prompt template's workflow: JSON parsing, grouping logic, plan
generation, review gate, confirmation flow, and execution orchestration.
Also covers insertion mode, batching, and safety veto behaviour.

Uses fixtures from tests/fixtures/todo-workspaces/ and the scanner output
from .specify/scripts/bash/search-todo.sh.
"""

import json
import subprocess
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "todo-workspaces"
SEARCH_TODO_SCRIPT = (
    Path(__file__).parent.parent.parent.parent
    / ".specify"
    / "scripts"
    / "bash"
    / "search-todo.sh"
)


@pytest.fixture
def valid_workspace():
    return str(FIXTURES_DIR / "valid")


@pytest.fixture
def oversized_workspace():
    return str(FIXTURES_DIR / "oversized")


@pytest.fixture
def malformed_workspace():
    return str(FIXTURES_DIR / "malformed")


def run_search_todo(workspace: str, json_mode: bool = True) -> dict:
    """Run search-todo.sh and return parsed JSON output."""
    script = str(SEARCH_TODO_SCRIPT)
    cmd = [script, "--json", workspace]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        try:
            return {"exit_code": 0, "data": json.loads(result.stdout.strip())}
        except json.JSONDecodeError:
            return {"exit_code": 1, "error": "json parse failed"}
    return {"exit_code": result.returncode, "stderr": result.stderr}
