"""Integration tests for the amended team view (108-team-view-degradation).

US1 segment (T007): report recognition, latest selection, residue and overview reuse —
`contracts/report-recognition.contract.md` C-201…C-207, data-model C1–C5, FR-001…FR-006,
FR-018. US2/US3 segments are appended to this file by their own tasks.

Every fixture tree is built under pytest ``tmp_path`` with the shared
``tests/fixtures/team_view_fixtures.py`` builder and every invocation carries
``--repo-root`` pointing at it, so the real repository is never read as a team archive
and never written.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.team_view_fixtures import build_team, report_text

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"

pytestmark = pytest.mark.integration


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


def envelope(root, *args):
    result = view(root, *args, "--json")
    assert result.returncode in (0, 5), result.stderr + result.stdout
    return json.loads(result.stdout)


# --------------------------------------------------------------------------- #
# US1 — report recognition, latest selection, residue (T007)
# --------------------------------------------------------------------------- #
PRODUCTION_REPLICA = (
    ("20261124T074500Z-report.md", report_text(result_summary="Old conforming run.")),
    ("20261125T121924Z-93cc-stage.md", report_text(result_summary="4-hex stage report.")),
    ("2026-11-25T140000Z-report.md", report_text(result_summary="Newest ISO-dashed run.")),
    ("20261008T214100Z-report.md", report_text(result_summary="Same-stamp run report.")),
    ("20261008T214100Z-seat-result.md", "Seat result auxiliary artifact.\n"),
    ("2026-10-07-progress-snapshot.md", "Snapshot without a time stamp.\n"),
    ("2026-10-06-S1-judgment-contract.md", "Judgment contract without a time stamp.\n"),
)

CORPUS_REPLICA_NAMES = (
    "2026-06-11T09-12-31Z-report.md",
    "2026-07-03T16-40-05Z-report.md",
    "2026-08-02T10-00-00Z-report.md",
    "2026-08-21T13-22-47Z-report.md",
    "2026-09-17T11-54-53Z-report.md",
    "2026-06-02T081500Z-report.md",
    "2026-06-18T114500Z-report.md",
    "2026-07-01T093000Z-report.md",
    "2026-07-22T170500Z-report.md",
    "2026-08-05T102210Z-report.md",
    "2026-08-30T135900Z-report.md",
    "2026-09-04T074020Z-report.md",
    "20260812T0930Z-report.md",
)


def test_production_replica_latest_is_the_parsed_maximum(tmp_path):
    build_team(tmp_path, "prod-replica", reports=PRODUCTION_REPLICA)
    result = view(tmp_path, "prod-replica")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    assert "最近报告（latest_report）: 2026-11-25T140000Z-report.md" in output
    assert "最近报告（latest_report）: 20261124T074500Z-report.md" not in output
    assert "最近报告（latest_report）: 20261125T121924Z-93cc-stage.md" not in output
    assert "运行报告: 已列出（共 4 份" in output
    assert "  - 20261125T121924Z-93cc-stage.md" in output
    assert "  - 2026-11-25T140000Z-report.md" in output
    assert (
        "辅助产物（auxiliary）: 共 1 份；示例: 20261008T214100Z-seat-result.md（省略 0）"
        in output
    )
    assert (
        "未识别（unrecognized）: 共 2 份；示例: 2026-10-06-S1-judgment-contract.md, "
        "2026-10-07-progress-snapshot.md（省略 0）" in output
    )
    assert "降级（degraded）" in output
    assert "report-recognition-uncertain" in output
    payload = envelope(tmp_path, "prod-replica")
    assert payload["as_of"]["latest_report_timestamp"] == "20261125T140000Z"
    assert payload["degraded"] is True
    assert [error["code"] for error in payload["errors"]] == ["report-recognition-uncertain"]


def test_corpus_style_reports_are_recognized(tmp_path):
    build_team(
        tmp_path,
        "corpus-replica",
        reports=[(name, report_text()) for name in CORPUS_REPLICA_NAMES],
    )
    result = view(tmp_path, "corpus-replica")
    assert result.returncode == 0, result.stderr + result.stdout
    output = result.stdout
    assert "运行报告: 已列出（共 13 份" in output
    assert "运行报告: 为空" not in output
    assert "运行报告: 缺失" not in output
    for name in CORPUS_REPLICA_NAMES:
        assert "  - %s" % name in output, "report not presented: %s" % name
    assert "最近报告（latest_report）: 2026-09-17T11-54-53Z-report.md" in output
    payload = envelope(tmp_path, "corpus-replica")
    assert payload["as_of"]["latest_report_timestamp"] == "20260917T115453Z"
    assert payload["degraded"] is False


def test_residue_only_runs_state_is_not_empty_or_missing(tmp_path):
    build_team(
        tmp_path,
        "residue-only",
        reports=[
            ("2026-10-07-progress-snapshot.md", "Snapshot without a time stamp.\n"),
            ("2026-10-06-S1-judgment-contract.md", "Judgment contract without a time stamp.\n"),
        ],
    )
    result = view(tmp_path, "residue-only")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    assert "运行报告: 未识别（unrecognized）—— 仅残留，最新不可确定" in output
    assert "运行报告: 为空" not in output
    assert "运行报告: 缺失" not in output
    assert (
        "未识别（unrecognized）: 共 2 份；示例: 2026-10-06-S1-judgment-contract.md, "
        "2026-10-07-progress-snapshot.md（省略 0）" in output
    )
    assert "最近报告（latest_report）: 未记录" in output
    assert "降级（degraded）" in output
    assert "report-recognition-uncertain" in output


def test_auxiliary_artifact_never_becomes_latest(tmp_path):
    build_team(
        tmp_path,
        "aux-team",
        reports=[
            ("20261008T214100Z-report.md", report_text(result_summary="Report.")),
            ("20261008T214100Z-seat-result.md", "Seat result.\n"),
            ("20261008T214100Z-verification.md", "Verification.\n"),
        ],
    )
    result = view(tmp_path, "aux-team")
    assert result.returncode == 0, result.stderr + result.stdout
    output = result.stdout
    assert "最近报告（latest_report）: 20261008T214100Z-report.md" in output
    assert "辅助产物（auxiliary）: 共 2 份" in output
    assert "report-recognition-uncertain" not in output
    payload = envelope(tmp_path, "aux-team")
    assert payload["as_of"]["latest_report_timestamp"] == "20261008T214100Z"
    assert payload["degraded"] is False


def test_same_stamp_tie_break_is_name_ascending(tmp_path):
    build_team(
        tmp_path,
        "tie-team",
        reports=[
            ("20260101T000000Z-report.md", report_text(result_summary="Plain.")),
            ("20260101T000000Z-93cc-report.md", report_text(result_summary="4-hex.")),
        ],
    )
    result = view(tmp_path, "tie-team")
    assert result.returncode == 0, result.stderr + result.stdout
    assert "最近报告（latest_report）: 20260101T000000Z-93cc-report.md" in result.stdout


def test_overview_matches_single_view_and_discloses_uncertainty(tmp_path):
    build_team(
        tmp_path,
        "clean-team",
        reports=[("20260102T000000Z-report.md", report_text())],
    )
    build_team(
        tmp_path,
        "residue-team",
        reports=[
            ("2026-01-03T08-30-00Z-report.md", report_text()),
            ("2026-10-07-progress-snapshot.md", "Snapshot without a time stamp.\n"),
        ],
    )
    overview = view(tmp_path)
    assert overview.returncode == 0, overview.stderr + overview.stdout
    output = overview.stdout
    assert "20260102T000000Z" in output
    assert "20260103T083000Z（report-recognition-uncertain：残留 1）" in output
    clean = envelope(tmp_path, "clean-team")
    residue = envelope(tmp_path, "residue-team")
    assert clean["as_of"]["latest_report_timestamp"] == "20260102T000000Z"
    assert residue["as_of"]["latest_report_timestamp"] == "20260103T083000Z"
    payload = envelope(tmp_path)
    assert payload["degraded"] is False
    assert payload["errors"] == []
    rows = {row["slug"]: row for row in payload["overview"]["rows"]}
    assert rows["clean-team"]["latest_run"] == clean["as_of"]["latest_report_timestamp"]
    assert rows["residue-team"]["latest_run"] == residue["as_of"]["latest_report_timestamp"]
    assert rows["residue-team"]["latest_residue"] == 1
