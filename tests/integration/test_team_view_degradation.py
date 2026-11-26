"""Integration tests for the amended team view (108-team-view-degradation).

US1 segment (T007): report recognition, latest selection, residue and overview reuse —
`contracts/report-recognition.contract.md` C-201…C-207, data-model C1–C5, FR-001…FR-006,
FR-018. US2 segment (T013/T014): identity / static / persistence-group degradation states —
`contracts/presentation.contract.md` C-301…C-309, `contracts/report-recognition.contract.md`
C-208, FR-007…FR-019, FR-025. The US3 segment is appended by its own tasks.

Every fixture tree is built under pytest ``tmp_path`` with the shared
``tests/fixtures/team_view_fixtures.py`` builder and every invocation carries
``--repo-root`` pointing at it, so the real repository is never read as a team archive
and never written.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.team_view_fixtures import build_team, default_frontmatter, report_text

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


# --------------------------------------------------------------------------- #
# US2 — identity / static / persistence-group degradation states (T013/T014)
# --------------------------------------------------------------------------- #
GROUP_HEADINGS = (
    "## 1. 身份与绑定（Identity & Binding）",
    "## 2. 静态结构（Static Structure）",
    "## 3. 动态结构（Dynamic Structure）",
    "## 4. 持久化清单（Persistence Inventory）",
    "## 5. 最近运行状态（Recent Run State）",
    "## 6. 其他归档层引用（Archive References）",
)

_ABSENT = object()

DEGRADED_MATRIX_BODY = """## Static Structure

| role | stage | type | lifecycle | responsibility |
|------|-------|------|-----------|----------------|
| lead | plan | Worker | temporary | coordinate the run |
| executor | implement | Worker | temporary | implement the slice |
| evaluator | review | Meta | temporary | review the slice |

## Dynamic Structure

**Pattern**: iteration — looped report cadence.
"""

DUPLICATED_AGENT_BODY = """## Static Structure

| role | stage | type | agent | agent | lifecycle | responsibility |
|------|-------|------|-------|-------|-----------|----------------|
| lead | plan | Worker | member-01 | member-01 | temporary | coordinate the run |
| executor | implement | Worker | member-02 | member-02 | temporary | implement the slice |
"""

DEGRADED_MEMBERS = [
    {"agent": "member-%02d" % index, "role": "worker", "lifecycle": "temporary"}
    for index in range(1, 10)
]

DEGRADED_GOAL = (
    "Ship the log metrics collection system to the staging cluster "
    "before the next review gate"
)


def degraded_frontmatter(slug, binding=_ABSENT, pattern="iteration"):
    frontmatter = {
        "slug": slug,
        "name": "Degraded Fixture Team",
        "description": "Production-shape degraded definition",
        "lifecycle_state": "active",
        "anchor_slug": "degraded-anchor",
        "goal": DEGRADED_GOAL,
        "members": [dict(member) for member in DEGRADED_MEMBERS],
        "seats": {"member-01": {"sdd-invocation": "forbidden"}},
        "config": {"isolation": "none"},
    }
    if pattern is not _ABSENT:
        frontmatter["pattern"] = pattern
    if binding is not _ABSENT:
        frontmatter["binding"] = binding
    return frontmatter


def degraded_team(
    root,
    slug="degraded-team",
    binding=_ABSENT,
    pattern="iteration",
    body=DEGRADED_MATRIX_BODY,
    reports=(),
):
    return build_team(
        root,
        slug,
        frontmatter=degraded_frontmatter(slug, binding=binding, pattern=pattern),
        body=body,
        reports=reports,
    )


def line_starting(output, prefix):
    return next((line for line in output.splitlines() if line.startswith(prefix)), None)


def unreadable_report(team_dir, name, text):
    """Write ``runs/<name>`` and remove its read permission (premise asserted)."""
    runs = team_dir / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    path = runs / name
    path.write_text(text, encoding="utf-8")
    path.chmod(0)
    assert not os.access(path, os.R_OK), (
        "test premise: mode 000 must be unreadable for this account")
    return path


def test_degraded_definition_names_every_state(tmp_path):
    team_dir = degraded_team(
        tmp_path, reports=[("20260105T000000Z-report.md", report_text())])
    unreadable_report(
        team_dir, "20260105T000000Z-report.md",
        report_text(result_summary="Unreadable newest run."))
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    # identity — binding unreadable with the engine's verbatim reason
    assert "绑定（binding）: 不可读（binding-missing:" in output
    assert "carries no binding block" in output
    # identity — goal named state and an unchanged declared identity
    assert "goal 需归一为 anchor_slug" in output
    assert "锚点身份（anchor_identity）: declared — degraded-anchor" in output
    # static — matrix anomaly with parsed rows still listed
    assert "正文矩阵: 形态异常（缺列: agent）" in output
    assert "  | lead | plan | Worker | temporary | coordinate the run |" in output
    # static — roster not comparable with a reason, never 未记录
    assert "名册差异（roster_delta）: 不可比对（not comparable）（原因：" in output
    assert "名册差异（roster_delta）: 未记录" not in output
    # persistence — ledger missing with its consequences
    assert "台账: 缺失（" in output
    assert "后果：无台账聚合计数、无非终态信号" in output
    # persistence — spine inapplicable by the declared pattern
    assert "按声明 pattern 不适用" in output
    assert "operating-loops.md § 8" in output
    # latest — names the unreadable report instead of silently recording 未记录
    assert "最近报告（latest_report）: 20260105T000000Z-report.md（不可读：" in output
    assert "- Outcome: 不可读" in output
    # static — members fully listed; seats / stage_seats disclosure kept
    assert "成员（frontmatter）: 9 名" in output
    for index in range(1, 10):
        assert "agent=member-%02d" % index in output
    assert "seats: 已声明" in output
    assert "stage_seats: 未声明（默认值见 create-mode.md § Schema notes）" in output
    # degradation — every active reason named, no fabricated value
    assert "降级（degraded）" in output
    assert "engine-degraded" in output
    assert "report-recognition-uncertain" not in output
    assert output.count("/speckit.team modify") >= 1
    assert "owner=未记录" not in output
    assert "台账: 0" not in output
    assert "运行报告: 0" not in output
    payload = envelope(tmp_path, "degraded-team")
    assert payload["degraded"] is True
    assert [error["code"] for error in payload["errors"]] == ["engine-degraded"]


def test_binding_unreadable_carries_engine_reason_and_repair_pointers(tmp_path):
    degraded_team(tmp_path)
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    binding_line = line_starting(result.stdout, "- 绑定（binding）:")
    assert binding_line is not None
    assert "不可读" in binding_line
    assert "binding-missing:" in binding_line
    assert "carries no binding block" in binding_line
    repair_line = line_starting(result.stdout, "- 绑定修复（binding repair）:")
    assert repair_line is not None
    assert "/speckit.team modify" in repair_line
    assert "goal-utils.py bind" in repair_line
    assert "anchor-definitions.md § The Binding Record" in repair_line


def test_partial_binding_keys_name_the_missing_keys(tmp_path):
    degraded_team(tmp_path, binding={"owner": "human"})
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    binding_line = line_starting(result.stdout, "- 绑定（binding）:")
    assert binding_line is not None
    assert "binding-missing:" in binding_line
    assert "missing the binding key(s) owner_id, origin" in binding_line
    assert "carries no binding block" not in binding_line
    repair_line = line_starting(result.stdout, "- 绑定修复（binding repair）:")
    assert repair_line is not None
    assert "/speckit.team modify" in repair_line
    assert "goal-utils.py bind" in repair_line


def test_inline_goal_is_a_named_state_with_repair_pointers(tmp_path):
    degraded_team(tmp_path)
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    goal_line = line_starting(result.stdout, "- goal 归一（goal）:")
    assert goal_line is not None
    assert "goal 需归一为 anchor_slug" in goal_line
    assert "/speckit.team modify" in goal_line
    assert "goal-utils.py migrate" in goal_line
    assert "锚点身份（anchor_identity）: declared — degraded-anchor" in result.stdout
    assert "declared — %s" % DEGRADED_GOAL not in result.stdout


def test_slug_form_goal_under_readable_binding_adds_no_state_line(tmp_path):
    frontmatter = default_frontmatter("slug-goal-team")
    frontmatter["goal"] = "anchor-slug-form"
    build_team(tmp_path, "slug-goal-team", frontmatter=frontmatter)
    result = view(tmp_path, "slug-goal-team")
    assert result.returncode == 0, result.stderr + result.stdout
    assert "goal 需归一为 anchor_slug" not in result.stdout
    assert "其它声明键: goal" in result.stdout


def test_matrix_without_agent_column_is_malformed_and_roster_not_comparable(tmp_path):
    degraded_team(tmp_path)
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    assert "正文矩阵: 形态异常（缺列: agent）" in output
    for row in (
        "  | lead | plan | Worker | temporary | coordinate the run |",
        "  | executor | implement | Worker | temporary | implement the slice |",
        "  | evaluator | review | Meta | temporary | review the slice |",
    ):
        assert row in output, "parsed matrix row not presented: %r" % row
    delta_line = line_starting(output, "- 名册差异（roster_delta）:")
    assert delta_line is not None
    assert "不可比对（not comparable）" in delta_line
    assert "原因：" in delta_line
    assert "未记录" not in delta_line
    assert "成员（frontmatter）: 9 名" in output

    build_team(
        tmp_path,
        "duplicated-agent",
        frontmatter=degraded_frontmatter("duplicated-agent"),
        body=DUPLICATED_AGENT_BODY,
    )
    duplicated = view(tmp_path, "duplicated-agent")
    assert duplicated.returncode == 5, duplicated.stderr + duplicated.stdout
    assert "正文矩阵: 形态异常（重复列: agent）" in duplicated.stdout
    assert "  | lead | plan | Worker | member-01 | temporary | coordinate the run |" in (
        duplicated.stdout)


def test_missing_ledger_carries_its_consequences(tmp_path):
    team_dir = degraded_team(tmp_path)
    result = view(tmp_path, "degraded-team")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    ledger_line = line_starting(output, "- 台账: 缺失")
    assert ledger_line is not None
    assert str(team_dir / "items.jsonl") in ledger_line
    assert "后果：无台账聚合计数、无非终态信号" in ledger_line
    assert "台账: 0" not in output
    assert "已聚合" not in output

    empty_dir = degraded_team(tmp_path, slug="empty-ledger")
    (empty_dir / "items.jsonl").write_text("", encoding="utf-8")
    empty = view(tmp_path, "empty-ledger")
    assert empty.returncode == 5, empty.stderr + empty.stdout
    empty_line = line_starting(empty.stdout, "- 台账: 为空")
    assert empty_line is not None
    assert "后果：" not in empty_line


def test_spine_applicability_follows_declared_pattern(tmp_path):
    degraded_team(tmp_path, slug="iteration-team")
    iteration = view(tmp_path, "iteration-team")
    assert iteration.returncode == 5, iteration.stderr + iteration.stdout
    for name in ("constraints.md", "STATE.md", "run-log.jsonl"):
        line = line_starting(iteration.stdout, "- %s 缺失" % name)
        assert line is not None, "missing spine line for %s" % name
        assert "按声明 pattern 不适用" in line
        assert "pattern=iteration" in line
        assert "operating-loops.md § 8" in line

    frontmatter = default_frontmatter("continuous-team")
    frontmatter["pattern"] = "continuous"
    build_team(tmp_path, "continuous-team", frontmatter=frontmatter)
    continuous = view(tmp_path, "continuous-team")
    assert continuous.returncode == 0, continuous.stderr + continuous.stdout
    for name in ("constraints.md", "STATE.md", "run-log.jsonl"):
        line = line_starting(continuous.stdout, "- %s 缺失" % name)
        assert line is not None
        assert "按声明 pattern 不适用" not in line
        assert "适用性不可判定" not in line

    frontmatter = default_frontmatter("undeclared-pattern-team")
    frontmatter.pop("pattern")
    build_team(tmp_path, "undeclared-pattern-team", frontmatter=frontmatter)
    undeclared = view(tmp_path, "undeclared-pattern-team")
    assert undeclared.returncode == 0, undeclared.stderr + undeclared.stdout
    line = line_starting(undeclared.stdout, "- STATE.md 缺失")
    assert line is not None
    assert "适用性不可判定" in line
    assert "create-mode.md § Schema notes" in line
    assert "按声明 pattern 不适用" not in line

    partial_dir = degraded_team(tmp_path, slug="partial-spine-team")
    (partial_dir / "constraints.md").write_text("", encoding="utf-8")
    partial = view(tmp_path, "partial-spine-team")
    assert partial.returncode == 5, partial.stderr + partial.stdout
    assert "脊柱文件（存在）: constraints.md" in partial.stdout
    state_line = line_starting(partial.stdout, "- STATE.md 缺失")
    assert state_line is not None
    assert "按声明 pattern 不适用" in state_line


def test_unreadable_latest_report_is_named_not_unrecorded(tmp_path):
    team_dir = build_team(
        tmp_path,
        "unreadable-latest",
        reports=[("20260101T000000Z-report.md", report_text())],
    )
    report = team_dir / "runs" / "20260101T000000Z-report.md"
    report.chmod(0)
    assert not os.access(report, os.R_OK), (
        "test premise: mode 000 must be unreadable for this account")
    result = view(tmp_path, "unreadable-latest")
    assert result.returncode == 0, result.stderr + result.stdout
    output = result.stdout
    latest_line = line_starting(output, "- 最近报告（latest_report）:")
    assert latest_line is not None
    assert "20260101T000000Z-report.md" in latest_line
    assert "不可读" in latest_line
    assert str(report) in latest_line
    for field in ("Outcome", "Target 指派", "Result Summary", "Verification", "Nested SDD Runs"):
        field_line = line_starting(output, "- %s:" % field)
        assert field_line is not None, "missing field line: %s" % field
        assert "不可读" in field_line
        assert "未记录" not in field_line
    assert "降级（degraded）" not in output


def test_four_state_discipline_on_new_surfaces(tmp_path):
    build_team(tmp_path, "state-missing")
    missing = view(tmp_path, "state-missing")
    assert missing.returncode == 0, missing.stderr + missing.stdout
    assert "运行报告: 缺失（" in missing.stdout
    assert "台账: 缺失（" in missing.stdout

    empty_dir = build_team(tmp_path, "state-empty")
    (empty_dir / "runs").mkdir()
    (empty_dir / "items.jsonl").write_text("", encoding="utf-8")
    empty = view(tmp_path, "state-empty")
    assert empty.returncode == 0, empty.stderr + empty.stdout
    assert "运行报告: 为空（" in empty.stdout
    assert "台账: 为空（" in empty.stdout

    unreadable_dir = build_team(
        tmp_path,
        "state-unreadable",
        reports=[("20260101T000000Z-report.md", report_text())],
    )
    report = unreadable_dir / "runs" / "20260101T000000Z-report.md"
    report.chmod(0)
    assert not os.access(report, os.R_OK), (
        "test premise: mode 000 must be unreadable for this account")
    unreadable = view(tmp_path, "state-unreadable")
    assert unreadable.returncode == 0, unreadable.stderr + unreadable.stdout
    latest_line = line_starting(unreadable.stdout, "- 最近报告（latest_report）:")
    assert latest_line is not None and "不可读" in latest_line

    residue_dir = build_team(
        tmp_path,
        "state-residue",
        reports=[("2026-10-07-progress-snapshot.md", "Snapshot without a stamp.\n")],
    )
    assert residue_dir.is_dir()
    residue = view(tmp_path, "state-residue")
    assert residue.returncode == 5, residue.stderr + residue.stdout
    assert "运行报告: 未识别（unrecognized）—— 仅残留，最新不可确定" in residue.stdout

    for output in (missing.stdout, empty.stdout, unreadable.stdout, residue.stdout):
        assert "运行报告: 0" not in output
        assert "台账: 0" not in output
        assert "运行报告: 未记录" not in output


def test_undeclared_pattern_and_zero_line_ledger_states(tmp_path):
    frontmatter = degraded_frontmatter("undeclared-degraded")
    frontmatter.pop("pattern")
    team_dir = build_team(
        tmp_path,
        "undeclared-degraded",
        frontmatter=frontmatter,
        body=DEGRADED_MATRIX_BODY,
    )
    (team_dir / "items.jsonl").write_text("", encoding="utf-8")
    result = view(tmp_path, "undeclared-degraded")
    assert result.returncode == 5, result.stderr + result.stdout
    output = result.stdout
    assert "适用性不可判定" in output
    assert "create-mode.md § Schema notes" in output
    assert "台账: 为空（" in output
    positions = []
    for heading in GROUP_HEADINGS:
        assert heading in output, "missing group heading: %s" % heading
        positions.append(output.index(heading))
    assert positions == sorted(positions), "group headings are out of order"
    for prefix in (
        "- slug: ",
        "- name: ",
        "- description: ",
        "- lifecycle: ",
        "- 绑定（binding）: ",
        "- 锚点身份（anchor_identity）: ",
        "- handoff_ref: ",
        "- 其它声明键: ",
        "- type 来源（type_source）: ",
        "- 正文矩阵: ",
        "- 成员（frontmatter）: ",
        "- seats: ",
        "- stage_seats: ",
        "- pattern: ",
        "- config: ",
        "- 可选键声明（optional keys）: ",
        "- focus_target: ",
        "- 团队目录（team_dir）: ",
        "- 运行报告: ",
        "- 最近报告（latest_report）: ",
        "- Outcome: ",
        "- Target 指派: ",
        "- Result Summary: ",
        "- Verification: ",
        "- Nested SDD Runs: ",
        "- 台账信号: ",
        "- 锚点（anchor）: ",
        "- 内容入口: ",
    ):
        assert any(line.startswith(prefix) for line in output.splitlines()), (
            "existing line missing after the additive change: %r" % prefix)
