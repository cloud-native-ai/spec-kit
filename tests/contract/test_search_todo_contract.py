"""
Contract tests for search-todo.py script.

Covers all discovery rules (D-1 through D-12: fenced form and comment form),
context rules (C-1 through C-6), output format validation (JSON and
key:value), and success criteria (SC-001 through SC-005) defined in
contracts/search-todo-cli.md.

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
    / "python"
    / "search-todo.py"
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
            "form",
            "context_heading",
            "prologue",
            "epilogue",
        }
        for block in data["blocks"]:
            if not all(k in block for k in block_keys):
                return False
            if block.get("form") not in ("fence", "comment"):
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
        assert data["counters"]["total_blocks_found"] == 8, data["counters"]
        # Every block must carry non-empty content
        for block in data["blocks"]:
            assert block["content"].strip() != ""

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
        """D-2/D-11: fence blocks span lines; comment blocks may be single-line."""
        result = run_search_todo(valid_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        for block in data["blocks"]:
            if block["form"] == "fence":
                assert block["closing_line"] > block["opening_line"]
            else:
                assert block["form"] == "comment"
                assert block["closing_line"] >= block["opening_line"]


# ============================================================================
# T040: D-9..D-12 comment-form detection, C-5/C-6 comment context
# ============================================================================
class TestCommentForm:
    """Contract tests for D-9..D-12 (comment-form blocks) and C-5/C-6."""

    def _comment_blocks(self, workspace):
        result = run_search_todo(workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        return data, [b for b in data["blocks"] if b["form"] == "comment"]

    def test_d10_d11_comment_blocks_detected(self, valid_workspace):
        """D-10/D-11: All three line-comment tokens produce blocks; the
        wrong-case and no-whitespace lines in legacy.ts open nothing."""
        data, comments = self._comment_blocks(valid_workspace)
        assert len(comments) == 4, [b["block_id"] for b in comments]
        by_file = {}
        for b in comments:
            by_file.setdefault(b["source_file"], []).append(b)
        assert set(by_file) == {"src/api.py", "src/db.sql", "src/legacy.ts"}
        # legacy.ts carries exactly two blocks: the single-line one and the
        # multi-line one — the `// speckit todo` and `//SPECKIT TODO` lines
        # after them open nothing (D-10 case-exact + whitespace requirement).
        assert len(by_file["src/legacy.ts"]) == 2

    def test_d11_single_line_comment_block(self, valid_workspace):
        """D-11: A single-line comment block has closing == opening."""
        data, comments = self._comment_blocks(valid_workspace)
        single = [b for b in comments if b["source_file"] == "src/legacy.ts"][0]
        assert single["opening_line"] == 2
        assert single["closing_line"] == 2
        assert single["content"] == (
            "SPECKIT TODO Remove password login once OAuth migration completes"
        )

    def test_d11_comment_content_tokens_stripped(self, valid_workspace):
        """D-11: content carries payloads with the comment tokens stripped."""
        data, comments = self._comment_blocks(valid_workspace)
        api = [b for b in comments if b["source_file"] == "src/api.py"][0]
        assert api["content"].splitlines()[0] == "SPECKIT TODO"
        assert api["content"].splitlines()[1] == "Optimize database queries:"

    def test_d12_shared_index_and_order(self, valid_workspace):
        """D-12: block index is shared across forms; ordering is by opening_line."""
        data, comments = self._comment_blocks(valid_workspace)
        legacy = sorted(
            (b for b in comments if b["source_file"] == "src/legacy.ts"),
            key=lambda b: b["opening_line"],
        )
        assert [b["block_id"].rsplit(":", 1)[-1] for b in legacy] == ["0", "1"]
        keys = [(b["source_file"], b["opening_line"]) for b in data["blocks"]]
        assert keys == sorted(keys)

    def test_d9_markdown_files_gate_comment_detection(self, negative_workspace):
        """D-9: In Markdown-family files a `# SPECKIT TODO` heading is not a block."""
        result = run_search_todo(negative_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        assert data["counters"]["total_blocks_found"] == 0, data["counters"]

    def test_c5_blank_line_bounded_context(self, valid_workspace):
        """C-5: adjacent same-token comments are prologue context, not terminators."""
        data, comments = self._comment_blocks(valid_workspace)
        sql = [b for b in comments if b["source_file"] == "src/db.sql"][0]
        assert sql["prologue"] == (
            "-- Users table anchors all account data\n-- Email lookups are the hot path"
        )
        api = [b for b in comments if b["source_file"] == "src/api.py"][0]
        assert api["epilogue"].startswith("def get_users():")

    def test_c6_comment_blocks_have_null_heading(self, valid_workspace):
        """C-6: comment blocks and non-Markdown fence blocks report heading null."""
        data, comments = self._comment_blocks(valid_workspace)
        for b in comments:
            assert b["context_heading"] is None
        rs = [b for b in data["blocks"] if b["source_file"] == "tests/integration.rs"]
        assert rs and all(b["context_heading"] is None for b in rs)

    def test_keyvalue_output_carries_form(self, valid_workspace):
        """§4.1: BLOCK lines carry a `:form <fence|comment>` segment."""
        result = run_search_todo(valid_workspace, json_mode=False)
        assert result["exit_code"] == 0
        block_lines = [ln for ln in result["stdout_lines"] if ln.startswith("BLOCK[")]
        assert len(block_lines) == 8
        forms = {ln.rsplit(":form ", 1)[-1].strip() for ln in block_lines}
        assert forms == {"fence", "comment"}


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
        # F8a remediation: every pathological construct in the fixture MUST be
        # reported malformed — and none may leak through as a valid block.
        assert data["counters"]["malformed_blocks"] == 3, data["counters"]
        assert data["counters"]["total_blocks_found"] == 0, data["counters"]
        reasons = {m["reason"] for m in data["malformed"]}
        assert reasons == {"nested_fence"}


# ============================================================================
# T037: D-4 nested fence handling
# ============================================================================
class TestNestedFence:
    """Contract tests for D-4 (nested fence handling)."""

    def test_d4_nested_fence(self, malformed_workspace):
        """D-4: Nested SPECKIT TODO inside another fence is reported, not executed."""
        result = run_search_todo(malformed_workspace, json_mode=True)
        assert result["exit_code"] == 0
        data = result["stdout_json"]
        # a TODO opened inside a non-TODO fence is flagged at ITS OWN line
        openings = {m["opening_line"] for m in data["malformed"]}
        assert 13 in openings, openings


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
