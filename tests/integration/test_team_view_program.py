"""Integration tests for the team-view program on fixture trees (103-team-view, T008).

Contract: `.specify/specs/103-team-view/contracts/team-view-program.contract.md`
C-29 (six groups / overview), C-30 (state vocabulary), C-31 (caps and shared strings),
C-33 (bounded latest-report excerpt), C-34 (as-of). Data model E2–E8, invariants
INV-01, INV-03, INV-07, INV-08, INV-10, INV-12, INV-13. FR-004, FR-008…FR-013, FR-015,
FR-016, FR-020; SC-001, SC-002, SC-006.

Every fixture tree is built under pytest ``tmp_path`` and every invocation carries
``--repo-root`` pointing at it, so the real repository is never read as a team archive
and never written.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from fixtures.team_view_fixtures import (
    DEFAULT_BODY,
    build_team,
    default_frontmatter,
    report_text,
    snapshot,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"

pytestmark = pytest.mark.integration

HEADINGS = [
    "## 1. 身份与绑定",
    "## 2. 静态结构",
    "## 3. 动态结构",
    "## 4. 持久化清单",
    "## 5. 最近运行状态",
    "## 6. 其他归档层引用",
]


def run_program(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(PROGRAM), *args],
        cwd=str(cwd) if cwd is not None else None,
        capture_output=True,
        text=True,
        timeout=120,
    )


def view(root, *args):
    return run_program(*args, "--repo-root", str(root))


def ledger_line(item_id, state, ts, **extra):
    row = {
        "item_id": item_id,
        "title": "fixture item",
        "phase_ref": "PH-0001",
        "state": state,
        "provenance": ".specify/teams/fixture/runs/r.md",
        "ts": ts,
        "identity": "explicit",
    }
    row.update(extra)
    return row


def complete_team(root):
    frontmatter = default_frontmatter("complete-team")
    frontmatter["name"] = "Complete Fixture"
    frontmatter["anchor_slug"] = "complete-anchor"
    frontmatter["handoff_ref"] = ".specify/handoffs/complete-team.md"
    frontmatter["seats"] = {"agent-a": {"sdd-invocation": "forbidden"}}
    frontmatter["stage_seats"] = {
        "plan": {"seats": ["agent-a", "agent-b"], "max_parallel": 2}
    }
    frontmatter["config"] = {
        "isolation": "worktree",
        "summary": {"enabled": False, "every": 1},
    }
    reports = [
        ("20260101T000000Z-report.md", report_text(result_summary="First fixture run.")),
        ("20260102T000000Z-report.md", report_text(
            outcome="completed",
            target="T-002",
            result_summary="Second fixture run.",
            verification="Fixture checks passed.",
        )),
    ]
    items = [
        ledger_line("TI-0001", "completed", "2026-01-01T00:00:00Z"),
        ledger_line("TI-0002", "in-progress", "2026-01-02T00:00:00Z"),
    ]
    return build_team(
        root,
        "complete-team",
        frontmatter=frontmatter,
        reports=reports,
        items_lines=items,
        spine=["constraints.md", "STATE.md", "run-log.jsonl"],
    )


class TestSingleTeamRendering:
    def test_single_team_renders_six_groups(self, tmp_path):
        complete_team(tmp_path)
        result = view(tmp_path, "complete-team")
        assert result.returncode == 0, result.stderr
        output = result.stdout
        for heading in HEADINGS:
            assert heading in output, "missing group heading: %s" % heading
        positions = [output.index(heading) for heading in HEADINGS]
        assert positions == sorted(positions), "group headings are out of order"
        for member in ("agent-a", "agent-b"):
            assert member in output, "member not covered: %s" % member
        for report in ("20260101T000000Z-report.md", "20260102T000000Z-report.md"):
            assert report in output, "report not covered: %s" % report
        assert re.search(r"as-of: \S+（文件时间；非实时探测）", output)

    def test_minimal_team_marks_missing_without_fabricated_zeros(self, tmp_path):
        build_team(tmp_path, "minimal-team")
        result = view(tmp_path, "minimal-team")
        assert result.returncode == 0, result.stderr
        output = result.stdout
        assert "运行报告: 缺失" in output
        assert "台账: 缺失" in output
        assert "constraints.md 缺失" in output
        assert "运行报告: 0" not in output
        assert "台账: 0" not in output

    def test_legacy_goal_slug_is_disclosed(self, tmp_path):
        frontmatter = default_frontmatter("legacy-team")
        frontmatter["goal_slug"] = "old-anchor"
        build_team(tmp_path, "legacy-team", frontmatter=frontmatter)
        output = view(tmp_path, "legacy-team").stdout
        assert "old-anchor" in output
        assert "legacy" in output

    def test_missing_anchor_slug_is_disclosed_as_inferred(self, tmp_path):
        build_team(tmp_path, "inferred-team")
        output = view(tmp_path, "inferred-team").stdout
        assert "inferred" in output
        assert "inferred-team" in output

    def test_archived_team_renders_normally(self, tmp_path):
        frontmatter = default_frontmatter("archived-team")
        frontmatter["lifecycle_state"] = "archived"
        build_team(tmp_path, "archived-team", frontmatter=frontmatter)
        result = view(tmp_path, "archived-team")
        assert result.returncode == 0, result.stderr
        assert "archived" in result.stdout

    def test_ledger_bad_line_is_counted_without_interrupting(self, tmp_path):
        build_team(
            tmp_path,
            "ledger-team",
            items_lines=[
                ledger_line("TI-0001", "completed", "2026-01-01T00:00:00Z"),
                "this line is not json",
            ],
        )
        result = view(tmp_path, "ledger-team")
        assert result.returncode == 0, result.stderr
        assert "坏行 1" in result.stdout

    def test_roster_mismatch_is_presented_on_both_sides(self, tmp_path):
        body = DEFAULT_BODY.replace("agent-b", "agent-c")
        build_team(tmp_path, "mismatch-team", body=body)
        output = view(tmp_path, "mismatch-team").stdout
        assert "仅正文矩阵: agent-c" in output
        assert "仅 frontmatter: agent-b" in output

    def test_report_names_are_capped_with_an_omitted_count(self, tmp_path):
        base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        names = [
            (base + timedelta(minutes=index)).strftime("%Y%m%dT%H%M%SZ") + "-report.md"
            for index in range(25)
        ]
        build_team(
            tmp_path,
            "many-reports",
            reports=[(name, report_text()) for name in names],
        )
        output = view(tmp_path, "many-reports").stdout
        assert names[-1] in output
        assert names[0] not in output
        assert "省略 5" in output

    def test_missing_report_segments_are_unrecorded_never_no_anomaly(self, tmp_path):
        build_team(
            tmp_path,
            "sparse-report-team",
            reports=[(
                "20260101T000000Z-report.md",
                report_text(verification=None, nested_runs=None),
            )],
        )
        output = view(tmp_path, "sparse-report-team").stdout
        assert "Verification: 未记录" in output
        assert "Nested SDD Runs: 未记录" in output
        assert "无异常" not in output


class TestOverview:
    """US2 (T020): the no-slug overview — FR-007, INV-04; C-29, C-31, C-32."""

    def test_overview_lists_two_teams_sorted_with_seven_fields(self, tmp_path):
        build_team(tmp_path, "alpha-team")
        frontmatter = default_frontmatter("bravo-team")
        frontmatter["anchor_slug"] = "bravo-anchor"
        build_team(
            tmp_path,
            "bravo-team",
            frontmatter=frontmatter,
            reports=[("20260102T000000Z-report.md", report_text())],
        )
        before = snapshot(tmp_path)
        result = view(tmp_path)
        assert result.returncode == 0, result.stderr
        assert snapshot(tmp_path) == before, "the overview wrote to the tree"
        output = result.stdout
        assert "alpha-team" in output and "bravo-team" in output
        assert output.index("| alpha-team") < output.index("| bravo-team"), "rows are not slug-ascending"
        table = [line for line in output.splitlines() if line.strip().startswith("|")]
        assert len(table) >= 4, "overview table missing header/separator/data rows"
        header = [cell.strip() for cell in table[0].strip().strip("|").split("|")]
        assert len(header) == 7, "overview row must cover seven fields: %r" % header
        for label in ("slug", "name", "pattern", "lifecycle", "updated", "最近运行"):
            assert label in table[0], "overview header lacks %s" % label
        alpha_row = next(line for line in table if "| alpha-team" in line)
        alpha_cells = [cell.strip() for cell in alpha_row.strip().strip("|").split("|")]
        assert len(alpha_cells) == 7
        for value in ("Fixture Team alpha-team", "serial", "active", "inferred", "2026-01-02", "未记录"):
            assert value in alpha_row, "alpha row lacks %r: %r" % (value, alpha_row)
        bravo_row = next(line for line in table if "| bravo-team" in line)
        bravo_cells = [cell.strip() for cell in bravo_row.strip().strip("|").split("|")]
        assert len(bravo_cells) == 7
        for value in ("Fixture Team bravo-team", "serial", "active", "declared", "bravo-anchor", "20260102T000000Z"):
            assert value in bravo_row, "bravo row lacks %r: %r" % (value, bravo_row)
        assert re.search(r"as-of: \S+（文件时间；非实时探测）", output)

    def test_empty_archive_reports_no_teams_found(self, tmp_path):
        result = view(tmp_path)
        assert result.returncode == 0, result.stderr
        assert "No teams found" in result.stdout


class TestEnvelopeAndReadOnly:
    def test_json_and_default_render_share_one_extraction(self, tmp_path):
        complete_team(tmp_path)
        result = view(tmp_path, "complete-team", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["mode"] == "single"
        assert payload["degraded"] is False
        definition = payload["team"]["definition"]
        assert definition["slug"] == "complete-team"
        assert definition["name"] == "Complete Fixture"
        plain = view(tmp_path, "complete-team").stdout
        assert "Complete Fixture" in plain

    def test_view_leaves_tree_byte_identical(self, tmp_path):
        complete_team(tmp_path)
        before = snapshot(tmp_path)
        result = view(tmp_path, "complete-team")
        assert result.returncode == 0, result.stderr
        assert snapshot(tmp_path) == before
        result = view(tmp_path, "complete-team", "--json")
        assert result.returncode == 0, result.stderr
        assert snapshot(tmp_path) == before
