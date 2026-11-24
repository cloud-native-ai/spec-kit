"""Unit tests for the team-view program's pure parsers (103-team-view, T005).

Contracts pinned here:
  `.specify/specs/103-team-view/contracts/team-view-program.contract.md`
  C-32 (deterministic ordering), C-33 (bounded latest-report excerpt), C-35 (frontmatter
  closed subset). Data model: E3 (static matrix), E6 (latest-report summary), E5 (ledger).
FR coverage: FR-009, FR-011, FR-012, FR-015.

The program file name carries a hyphen, so it is loaded through ``importlib``; these tests
read its pure functions only and start no subprocess. Before the program exists this module
fails at import — that is the intended red-first reading (T009).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"


def _load_program():
    spec = importlib.util.spec_from_file_location("team_view_program_unit", PROGRAM)
    module = importlib.util.module_from_spec(spec)
    sys.modules["team_view_program_unit"] = module
    spec.loader.exec_module(module)
    return module


team_view = _load_program()


FRONTMATTER_DOC = """---
slug: fixture-team
name: "Quoted Name: with colon"
description: plain text
pattern: serial
lifecycle_state: active
anchor_slug: fixture-anchor
territory:
  write: [scripts/**, tests/**]
  read: ["**"]
  non_path:
    - { type: runtime, target: host concurrency }
members:
  - agent: agent-a
    role: executor
    lifecycle: temporary
    territory: [scripts/**]
  - agent: agent-b
    role: evaluator
    lifecycle: persistent
seats:
  agent-a:
    sdd-invocation: forbidden
config:
  isolation: worktree
  summary:
    enabled: false
    every: 5
---

## Goal

Body.
"""


class TestFrontmatterSubset:
    def test_scalars_quotes_and_defaults(self):
        data, problems = team_view.parse_frontmatter(FRONTMATTER_DOC)
        assert data["slug"] == "fixture-team"
        assert data["name"] == "Quoted Name: with colon"
        assert data["pattern"] == "serial"
        assert data["created"] is None  # absent key is absent, never invented
        assert problems == {}

    def test_inline_lists(self):
        data, _ = team_view.parse_frontmatter(FRONTMATTER_DOC)
        assert data["territory"]["write"] == ["scripts/**", "tests/**"]
        assert data["territory"]["read"] == ["**"]

    def test_bounded_nested_map(self):
        data, _ = team_view.parse_frontmatter(FRONTMATTER_DOC)
        assert data["config"]["summary"] == {"enabled": False, "every": 5}
        assert data["seats"]["agent-a"]["sdd-invocation"] == "forbidden"

    def test_block_sequence_of_maps(self):
        data, _ = team_view.parse_frontmatter(FRONTMATTER_DOC)
        assert [row["agent"] for row in data["members"]] == ["agent-a", "agent-b"]
        assert data["members"][0]["territory"] == ["scripts/**"]

    def test_flow_map_inside_a_block_sequence(self):
        data, problems = team_view.parse_frontmatter(FRONTMATTER_DOC)
        assert data["territory"]["non_path"] == [
            {"type": "runtime", "target": "host concurrency"}
        ]
        assert "territory" not in problems

    def test_block_scalar_is_unreadable_not_guessed(self):
        text = "---\nslug: t\ngoal: >\n  folded text\n  continues\n---\n\n## Goal\n\nx\n"
        data, problems = team_view.parse_frontmatter(text)
        assert problems.get("goal") == "不可读"
        assert "goal" not in data

    def test_duplicate_key_is_malformed(self):
        text = "---\nslug: one\nslug: two\n---\n\n## Goal\n\nx\n"
        data, problems = team_view.parse_frontmatter(text)
        assert problems.get("slug") == "形态异常"
        assert "slug" not in data

    def test_missing_frontmatter_fence_is_reported(self):
        data, problems = team_view.parse_frontmatter("## Goal\n\nno frontmatter\n")
        assert data == {}
        assert problems.get("frontmatter") == "缺失"


class TestStaticMatrix:
    def test_six_column_matrix_parses_in_file_order(self):
        rows, state = team_view.parse_static_matrix("""
## Static Structure

| role | stage | type | agent | lifecycle | responsibility |
|------|-------|------|-------|-----------|----------------|
| Executor | executor | Worker | agent-a | temporary | produce |
| Evaluator | evaluator | Meta | agent-b | persistent | judge |
""")
        assert state is None
        assert [row["role"] for row in rows] == ["Executor", "Evaluator"]
        assert rows[1]["type"] == "Meta"
        assert rows[0]["agent"] == "agent-a"

    def test_heading_suffix_and_header_normalisation(self):
        rows, state = team_view.parse_static_matrix("""
## Static Structure (Role × Stage × Type)

| Role | Stage | Type |
|------|-------|------|
| supervisor | optimizer | Meta |
""")
        assert state is None
        assert rows == [{"role": "supervisor", "stage": "optimizer", "type": "Meta"}]

    def test_missing_section_is_missing(self):
        rows, state = team_view.parse_static_matrix("## Goal\n\nnothing\n")
        assert rows == []
        assert state == "缺失"

    def test_missing_required_column_is_unreadable(self):
        rows, state = team_view.parse_static_matrix("""
## Static Structure

| role | type | agent |
|------|------|-------|
| Executor | Worker | agent-a |
""")
        assert rows == []
        assert state == "不可读"

    def test_duplicate_required_column_is_unreadable(self):
        rows, state = team_view.parse_static_matrix("""
## Static Structure

| role | stage | type | stage |
|------|-------|------|-------|
| Executor | executor | Worker | executor |
""")
        assert rows == []
        assert state == "不可读"

    def test_ragged_row_is_malformed(self):
        rows, state = team_view.parse_static_matrix("""
## Static Structure

| role | stage | type |
|------|-------|------|
| Executor | executor |
""")
        assert rows == []
        assert state == "形态异常"


class TestReportSegments:
    REPORT = """# Team Run Report: Fixture

- **Team**: fixture · **Goal**: fixture-goal · **Pattern**: serial · **Outcome**: completed
- **Target 指派**: T-002

## Result Summary

The run did the thing.

## Verification

Checks passed.

## Nested SDD Runs

- outcome: completed · artifact paths: a · evidence paths: b · routing-verdict reference: r · anomalies: none
"""

    def test_outcome_and_target_assignment(self):
        parsed = team_view.parse_report(self.REPORT)
        assert parsed["outcome"] == "completed"
        assert parsed["target_assignment"] == "T-002"

    def test_sections_extracted_until_next_heading(self):
        parsed = team_view.parse_report(self.REPORT)
        assert parsed["result_summary"].strip() == "The run did the thing."
        assert "Checks passed." in parsed["verification"]
        assert "Nested SDD Runs" not in parsed["result_summary"]

    def test_missing_segments_are_none(self):
        text = "# Report\n\n- **Team**: t · **Pattern**: serial · **Outcome**: completed\n"
        parsed = team_view.parse_report(text)
        assert parsed["outcome"] == "completed"
        assert parsed["target_assignment"] is None
        assert parsed["verification"] is None
        assert parsed["nested_runs"] is None

    def test_nested_absent_is_unrecorded(self):
        text = "# Report\n\n- **Outcome**: completed\n"
        assert team_view.summarize_nested(team_view.parse_report(text)["nested_runs"]) == "未记录"

    def test_nested_own_none_declaration(self):
        section = "本次无嵌套 SDD 调用。"
        assert team_view.summarize_nested(section) == "本次无嵌套 SDD 调用"

    def test_nested_anomalies_are_listed_verbatim(self):
        section = (
            "- outcome: completed · artifact paths: a · evidence paths: b · "
            "routing-verdict reference: r · anomalies: 1 stale record\n"
        )
        assert team_view.summarize_nested(section) == ["1 stale record"]

    def test_nested_without_anomalies_field_is_never_no_anomaly(self):
        section = "- outcome: completed · artifact paths: a\n"
        result = team_view.summarize_nested(section)
        assert result == "未记录"
        assert "无异常" not in str(result)

    def test_bounded_excerpt_line_cap(self):
        text = "\n".join("line %d" % index for index in range(1, 13))
        excerpt = team_view.bounded_excerpt(text)
        assert "line 10" in excerpt
        assert "line 11" not in excerpt
        assert excerpt.endswith("…（截断）")

    def test_bounded_excerpt_char_cap(self):
        text = "x" * 900
        excerpt = team_view.bounded_excerpt(text)
        assert excerpt.startswith("x" * 800)
        assert excerpt.endswith("…（截断）")
        assert len(excerpt) < 900

    def test_bounded_excerpt_short_text_unchanged(self):
        assert team_view.bounded_excerpt("short body") == "short body"


def _event(item_id, state, ts, **extra):
    row = {
        "item_id": item_id,
        "title": "title",
        "phase_ref": "PH-0001",
        "state": state,
        "provenance": ".specify/teams/fixture/runs/r.md",
        "ts": ts,
        "identity": "explicit",
    }
    row.update(extra)
    return row


class TestLedgerAggregation:
    def test_last_event_by_ts_decides_state(self):
        import json

        lines = [
            json.dumps(_event("TI-0001", "not-started", "2026-01-01T00:00:00Z")),
            json.dumps(_event("TI-0001", "completed", "2026-01-02T00:00:00Z")),
        ]
        result = team_view.aggregate_ledger(lines)
        assert result["by_state"] == {"completed": 1}
        assert result["non_terminal"] == []

    def test_same_ts_last_file_position_wins(self):
        import json

        lines = [
            json.dumps(_event("TI-0001", "completed", "2026-01-01T00:00:00Z")),
            json.dumps(_event("TI-0001", "delayed", "2026-01-01T00:00:00Z")),
        ]
        result = team_view.aggregate_ledger(lines)
        assert result["by_state"] == {"delayed": 1}
        assert result["non_terminal"] == [{"item_id": "TI-0001", "state": "delayed"}]

    def test_bad_lines_are_counted_and_do_not_interrupt(self):
        import json

        lines = [
            json.dumps(_event("TI-0001", "completed", "2026-01-01T00:00:00Z")),
            "not json at all",
            json.dumps({"item_id": "TI-0002"}),
            json.dumps(_event("TI-0003", "weird-state", "2026-01-01T00:00:00Z")),
        ]
        result = team_view.aggregate_ledger(lines)
        assert result["total_lines"] == 4
        assert result["bad_lines"] == 3
        assert result["by_state"] == {"completed": 1}

    def test_excluded_reason_suppresses_non_terminal(self):
        import json

        lines = [
            json.dumps(_event("TI-0001", "delayed", "2026-01-01T00:00:00Z",
                              excluded_reason="excluded by owner")),
            json.dumps(_event("TI-0002", "in-progress", "2026-01-01T00:00:00Z")),
        ]
        result = team_view.aggregate_ledger(lines)
        assert result["non_terminal"] == [{"item_id": "TI-0002", "state": "in-progress"}]

    def test_empty_input(self):
        result = team_view.aggregate_ledger([])
        assert result["total_lines"] == 0
        assert result["bad_lines"] == 0
        assert result["by_state"] == {}
        assert result["non_terminal"] == []
