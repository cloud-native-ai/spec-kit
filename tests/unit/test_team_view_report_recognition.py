"""Unit tests for run-report recognition in the team-view program (108, T006).

Pins `.specify/specs/108-team-view-degradation/contracts/report-recognition.contract.md`
C-201…C-206 and data-model C1–C5. FR-001…FR-005.

The program file name carries a hyphen, so it is loaded through ``importlib``; these tests
read its pure functions only and start no subprocess. Fixtures are built with the shared
``tests/fixtures/team_view_fixtures.py`` builder under pytest ``tmp_path``.
"""
from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

from fixtures.team_view_fixtures import build_team

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM = REPO_ROOT / "scripts" / "python" / "team-view.py"


def _load_program():
    spec = importlib.util.spec_from_file_location("team_view_program_recognition", PROGRAM)
    module = importlib.util.module_from_spec(spec)
    sys.modules["team_view_program_recognition"] = module
    spec.loader.exec_module(module)
    return module


team_view = _load_program()


def team_dir(root, slug):
    return root / ".specify" / "teams" / slug


def test_stamp_grammar_accepts_exactly_the_five_forms():
    expected = datetime(2026, 11, 25, 14, 0, 0, tzinfo=timezone.utc)
    for name in (
        "20261125T140000Z-report.md",
        "20261125T1400Z-report.md",
        "2026-11-25T14:00:00Z-report.md",
        "2026-11-25T14-00-00Z-report.md",
        "2026-11-25T140000Z-report.md",
    ):
        assert team_view.parse_stamp(name) == expected, name
    for name in (
        "2026-10-07-progress-snapshot.md",
        "2026-10-06-S1-judgment-contract.md",
        "20261301T000000Z-report.md",
        "20260230T000000Z-report.md",
        "20261125T240000Z-report.md",
        "2026-11-25T14:00:00+08:00-report.md",
        "x20261125T140000Z-report.md",
    ):
        assert team_view.parse_stamp(name) is None, name


def test_classification_order_is_fixed():
    cases = {
        "20261125T140000Z-report.md": "report",
        "20261125T140000Z-93cc-report.md": "report",
        "20261125T140000Z-stage.md": "report",
        "20261125T1400Z-93cc-stage.md": "report",
        "20261125T140000Z-verification.md": "auxiliary",
        "20261125T140000Z-seat-result.md": "auxiliary",
        "20261125T140000Z-93cc-verification.md": "auxiliary",
        "20261125T140000Z-ABCD-report.md": "auxiliary",
        "20261125T140000Z-abc-report.md": "auxiliary",
        "20261125T140000Z-progress-snapshot.md": "auxiliary",
        "2026-10-07-progress-snapshot.md": "residue",
        "20261301T000000Z-report.md": "residue",
        "notes.txt": "residue",
    }
    for name, kind in cases.items():
        record = team_view.classify_run_file(name)
        assert record["kind"] == kind, (name, record)


def test_latest_is_maximum_parsed_timestamp_with_name_tiebreak(tmp_path):
    build_team(
        tmp_path,
        "recency-team",
        reports=[
            ("20261124T074500Z-report.md", "oldest\n"),
            ("20261125T121924Z-93cc-stage.md", "stage file\n"),
            ("20261125T140000Z-report.md", "newest, later name\n"),
            ("20261125T140000Z-93cc-report.md", "newest, same stamp, earlier name\n"),
        ],
    )
    inventory = team_view.classify_runs(team_dir(tmp_path, "recency-team"))
    names = [record["name"] for record in inventory["reports"]]
    assert names == [
        "20261125T140000Z-93cc-report.md",
        "20261125T140000Z-report.md",
        "20261125T121924Z-93cc-stage.md",
        "20261124T074500Z-report.md",
    ]
    assert inventory["total"] == 4
    assert Path(inventory["latest_path"]).name == "20261125T140000Z-93cc-report.md"
    assert inventory["latest_token"] == "20261125T140000Z"


def test_normalized_token_is_the_single_value(tmp_path):
    build_team(
        tmp_path,
        "token-team",
        reports=[
            ("2026-09-17T11-54-53Z-report.md", "newest\n"),
            ("20260901T080000Z-report.md", "older\n"),
        ],
    )
    inventory = team_view.classify_runs(team_dir(tmp_path, "token-team"))
    latest = inventory["reports"][0]
    assert latest["token"] == "20260917T115453Z"
    assert inventory["latest_token"] == latest["token"]
    assert inventory["reports"][1]["token"] == "20260901T080000Z"


def test_residue_presentation_is_bounded(tmp_path):
    names = [
        "2026-10-02-notes.md",
        "2026-10-03-notes.md",
        "2026-10-04-notes.md",
        "2026-10-05-notes.md",
        "2026-10-06-S1-judgment-contract.md",
    ]
    build_team(tmp_path, "residue-team", reports=[(name, "x\n") for name in names])
    inventory = team_view.classify_runs(team_dir(tmp_path, "residue-team"))
    residue = inventory["residue"]
    assert residue["count"] == 5
    assert residue["examples"] == names[:3]
    assert residue["omitted"] == 2
    assert inventory["reports"] == []
    assert inventory["state"] == "未识别（unrecognized）"


def test_uncertainty_predicate_needs_readable_runs_and_residue(tmp_path):
    build_team(
        tmp_path,
        "with-residue",
        reports=[
            ("20260101T000000Z-report.md", "report\n"),
            ("2026-10-07-progress-snapshot.md", "residue\n"),
        ],
    )
    inventory = team_view.classify_runs(team_dir(tmp_path, "with-residue"))
    assert inventory["state"] == "已列出"
    assert inventory["uncertain"] is True

    build_team(
        tmp_path,
        "auxiliary-only",
        reports=[
            ("20260101T000000Z-report.md", "report\n"),
            ("20260101T000000Z-seat-result.md", "auxiliary\n"),
        ],
    )
    inventory = team_view.classify_runs(team_dir(tmp_path, "auxiliary-only"))
    assert inventory["residue"]["count"] == 0
    assert inventory["residue"]["auxiliary_count"] == 1
    assert inventory["uncertain"] is False

    build_team(tmp_path, "no-runs")
    inventory = team_view.classify_runs(team_dir(tmp_path, "no-runs"))
    assert inventory["state"] == "缺失"
    assert inventory["uncertain"] is False

    empty = build_team(tmp_path, "empty-runs")
    (empty / "runs").mkdir()
    inventory = team_view.classify_runs(empty)
    assert inventory["state"] == "为空"
    assert inventory["uncertain"] is False
