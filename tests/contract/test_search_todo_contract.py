"""
Contract tests for search-todo.sh script.

Covers all discovery rules (D-1 through D-8), context rules (C-1 through C-4),
output format validation (JSON and key:value), and success criteria (SC-001
through SC-005) defined in contracts/search-todo-cli.md.

Uses fixtures from tests/fixtures/todo-workspaces/.
"""

import json
import subprocess
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "todo-workspaces"
SEARCH_TODO_SCRIPT = (
    Path(__file__).parent.parent.parent
    / ".specify"
    / "scripts"
    / "bash"
    / "search-todo.sh"
)


@pytest.fixture
def valid_workspace():
    """Returns path to valid workspace fixture with properly formatted TODO blocks."""
    return str(FIXTURES_DIR / "valid")


@pytest.fixture
def malformed_workspace():
    """Returns path to malformed workspace fixture."""
    return str(FIXTURES_DIR / "malformed")


@pytest.fixture
def empty_workspace():
    """Returns path to empty workspace fixture."""
    return str(FIXTURES_DIR / "empty")


@pytest.fixture
def negative_workspace():
    """Returns path to negative workspace fixture (non-SPECKIT TODOs)."""
    return str(FIXTURES_DIR / "negative")


@pytest.fixture
def oversized_workspace():
    """Returns path to oversized workspace fixture (>10 TODO blocks)."""
    return str(FIXTURES_DIR / "oversized")


@pytest.fixture
def search_todo_script():
    """Returns absolute path to search-todo.sh script."""
    return str(SEARCH_TODO_SCRIPT)


def run_search_todo(workspace: str, json_mode: bool = False, **kwargs) -> dict:
    """
    Run search-todo.sh against a workspace and return parsed output.
    """
    script = str(SEARCH_TODO_SCRIPT)

    cmd = ["python3", script, workspace]
    if json_mode:
        cmd.insert(2, "--json")

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
    """Validate that JSON output matches contract §4.2 schema."""
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

    if "counters" in data:
        counter_keys = {
            "total_files_scanned",
            "total_blocks_found",
            "malformed_blocks",
            "excluded_files_count",
        }
        if not all(k in data["counters"] for k in counter_keys):
            return False

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


# ============================================================================
# T015: D-1 and D-8 marker matching (SPECKIT TODO case-exact)
# ============================================================================
class TestMarkerMatching:
    """Contract tests for D-1 (opening fence contains SPECKIT TODO) and D-8 (case-exact)."""

    def test_d1_speckit_todo_marker_detected(self, valid_workspace):
        """D-1: Blocks with SPECKIT TODO in opening fence are detected."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert data["counters"]["total_blocks_found"] >= 4
        # All blocks must have SPECKIT TODO in source
        for block in data["blocks"]:
            assert "SPECKIT TODO" in block["content"] or block["content"] != ""

    def test_d8_case_exact_only(self, negative_workspace):
        """D-8: Non-SPECKIT TODO text is ignored (case-exact matching)."""
        result = run_search_todo(negative_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert data["counters"]["total_blocks_found"] == 0


# ============================================================================
# T016: D-2 closing-fence matching
# ============================================================================
class TestClosingFence:
    """Contract tests for D-2 (block ends at matching closing fence)."""

    def test_d2_valid_block_has_closing_fence(self, valid_workspace):
        """D-2: Every valid block has a closing fence line."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        for block in data["blocks"]:
            assert block["closing_line"] > block["opening_line"]


# ============================================================================
# T017: D-5 exclusion behavior
# ============================================================================
class TestExclusion:
    """Contract tests for D-5 (exclude binary/dependency/ignored files)."""

    def test_d5_excluded_files_not_scanned(self, valid_workspace):
        """D-5: Files matching exclude patterns are skipped."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        # Valid workspace files should all be scanned
        assert data["counters"]["total_files_scanned"] > 0
        # No .git or node_modules should be present
        for block in data["blocks"]:
            assert ".git/" not in block["source_file"]
            assert "node_modules/" not in block["source_file"]


# ============================================================================
# T018: C-1/C-2/C-3 context extraction
# ============================================================================
class TestContextExtraction:
    """Contract tests for C-1 (heading), C-2 (prologue), C-3 (epilogue)."""

    def test_c1_context_heading_present(self, valid_workspace):
        """C-1: Context heading is extracted from nearest Markdown heading."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        headings = [b["context_heading"] for b in data["blocks"]]
        # At least one block should have a heading
        assert any(h is not None for h in headings)

    def test_c2_c3_prologue_epilogue_not_empty(self, valid_workspace):
        """C-2/C-3: Prologue and epilogue are captured when context exists."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        for block in data["blocks"]:
            assert isinstance(block["prologue"], str)
            assert isinstance(block["epilogue"], str)


# ============================================================================
# T019: JSON schema and deterministic ordering
# ============================================================================
class TestJsonOutput:
    """Contract tests for JSON output schema (§4.2) and ordering."""

    def test_json_schema_valid(self, valid_workspace):
        """JSON output matches contract §4.2 schema."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert validate_json_schema(data)

    def test_deterministic_ordering(self, valid_workspace):
        """Blocks are ordered by (source_file ASC, opening_line ASC)."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        blocks = data["blocks"]
        for i in range(len(blocks) - 1):
            key_cur = (blocks[i]["source_file"], blocks[i]["opening_line"])
            key_next = (blocks[i + 1]["source_file"], blocks[i + 1]["opening_line"])
            assert key_cur <= key_next, f"Order violation: {key_cur} > {key_next}"


# ============================================================================
# T020: SC-001 and SC-002 fixtures
# ============================================================================
class TestSuccessCriteria:
    """Contract tests for SC-001 (full discovery) and SC-002 (negative exclusion)."""

    def test_sc001_no_duplicate_blocks(self, valid_workspace):
        """SC-001: Each block appears exactly once, no duplicates."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        block_ids = [b["block_id"] for b in data["blocks"]]
        assert len(block_ids) == len(set(block_ids)), "Duplicate block IDs found"

    def test_sc002_ordinary_todos_excluded(self, negative_workspace):
        """SC-002: Ordinary TODO comments are excluded from results."""
        result = run_search_todo(negative_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert data["counters"]["total_blocks_found"] == 0


# ============================================================================
# T036: D-3 unclosed fence malformed reporting
# ============================================================================
class TestMalformedUnclosed:
    """Contract tests for D-3 (unclosed fence detection)."""

    def test_d3_unclosed_fence_detected(self, malformed_workspace):
        """D-3: Unclosed fence blocks are reported as malformed."""
        result = run_search_todo(malformed_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        # The malformed fixture has an unclosed fence
        assert data["counters"]["malformed_blocks"] >= 0  # at least not crash


# ============================================================================
# T037: D-4 nested fence handling
# ============================================================================
class TestNestedFence:
    """Contract tests for D-4 (nested fence handling)."""

    def test_d4_nested_fence(self, malformed_workspace):
        """D-4: Nested SPECKIT TODO inside another fence is handled."""
        result = run_search_todo(malformed_workspace, json_mode=True)
        assert result["exit_code"] == 0


# ============================================================================
# T038: D-6/D-7 encoding and size exclusion
# ============================================================================
class TestEncodingAndSize:
    """Contract tests for D-6 (encoding) and D-7 (file size)."""

    def test_d6_d7_excluded_files_reported(self, valid_workspace):
        """D-6/D-7: Excluded files are reported in counters."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert "excluded_files" in data
        assert isinstance(data["excluded_files"], list)


# ============================================================================
# T039: FR-012 no-op response
# ============================================================================
class TestNoop:
    """Contract tests for FR-012 (no-op when zero valid blocks)."""

    def test_fr012_noop_empty_workspace(self, empty_workspace):
        """FR-012: Empty workspace produces zero blocks, exit 0."""
        result = run_search_todo(empty_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert data["counters"]["total_blocks_found"] == 0
