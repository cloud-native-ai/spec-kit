"""Unit tests for ``wp-report.py`` — OR-04…OR-13 metric computation.

The report is derived from the line state spine only: the plan fence (effective
plan after amendments) and the append-only ledger. Every metric whose source
record is missing is the literal string ``not_evaluated``; the report never
writes the spine and never carries raw transcripts.

Clause map: OR-04 wall-clock, OR-05 critical path, OR-06 parallelism
efficiency, OR-07 stage executions per canonical stage, OR-08 retry counts,
OR-09 manual interventions, OR-10 not_evaluated, OR-11 report CLI/files,
OR-12 report content and no transcripts, OR-13 benchmark record (documented by
T029; no measurement is fabricated here).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import wp_fixtures

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "external"
    / "sdd-loop-driver"
    / "scripts"
    / "wp-report.py"
)

NOT_EVALUATED = "not_evaluated"


def _two_package_plan(stage: str = "plan", **overrides) -> dict:
    first = wp_fixtures.make_package(
        "%s-wp01" % stage, stage, outputs=["findings/%s-wp01.md" % stage]
    )
    second = wp_fixtures.make_package(
        "%s-wp02" % stage, stage, outputs=["findings/%s-wp02.md" % stage]
    )
    return wp_fixtures.make_plan(
        packages=[first, second], stage=stage, **overrides
    )


def _chain_plan(stage: str = "plan") -> dict:
    first = wp_fixtures.make_package(
        "%s-wp01" % stage, stage, outputs=["findings/%s-wp01.md" % stage]
    )
    second = wp_fixtures.make_package(
        "%s-wp02" % stage,
        stage,
        outputs=["findings/%s-wp02.md" % stage],
        depends_on=[first["wp_id"]],
    )
    return wp_fixtures.make_plan(
        packages=[first, second],
        stage=stage,
        pattern="serial",
        slot_cap=1,
    )


def _diamond_plan(stage: str = "plan") -> dict:
    root = wp_fixtures.make_package(
        "%s-wp01" % stage, stage, outputs=["findings/%s-wp01.md" % stage]
    )
    left = wp_fixtures.make_package(
        "%s-wp02" % stage,
        stage,
        outputs=["findings/%s-wp02.md" % stage],
        depends_on=[root["wp_id"]],
    )
    right = wp_fixtures.make_package(
        "%s-wp03" % stage,
        stage,
        outputs=["findings/%s-wp03.md" % stage],
        depends_on=[root["wp_id"]],
    )
    return wp_fixtures.make_plan(
        packages=[root, left, right],
        stage=stage,
        pattern="serial",
        slot_cap=2,
    )


def _attempt(
    wp_id: str,
    start: int,
    end: int,
    order: int = 1,
    wp_attempt: int = 1,
    verdict: str = "pass",
    stage_attempt: int = 1,
) -> list:
    return [
        wp_fixtures.dispatch_event(
            wp_id=wp_id,
            stage_attempt=stage_attempt,
            wp_attempt=wp_attempt,
            dispatch_order=order,
            started_at=start,
            attempt_id="%s-a%d-w%d" % (wp_id, stage_attempt, wp_attempt),
        ),
        wp_fixtures.settle_event(wp_id=wp_id, ended_at=end),
        wp_fixtures.verdict_event(wp_id=wp_id, verdict=verdict, at=end + 1),
    ]


def _plan_event(plan: dict, **overrides) -> dict:
    return wp_fixtures.plan_event(
        stage=plan["stage"],
        stage_attempt=plan["stage_attempt"],
        plan_hash=plan["plan_hash"],
        decision=plan["decision"],
        pattern=plan["pattern"],
        slot_cap=plan["slot_cap"],
        **overrides,
    )


def _spine(tmp_path: Path, plan=None, ledger=(), extra: str = "") -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "state.md"
    return wp_fixtures.make_spine(path, plan=plan, ledger=list(ledger), extra=extra)


def _run(spine: Path, out_dir: Path, *args):
    assert SCRIPT.is_file(), "missing report script: %s" % SCRIPT
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--spine",
            str(spine),
            "--out-dir",
            str(out_dir),
            *args,
        ],
        capture_output=True,
        text=True,
    )


def _report(spine: Path, out_dir: Path, *args) -> tuple:
    result = _run(spine, out_dir, *args)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout), out_dir


def _keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            for nested in _keys(item):
                yield nested
    elif isinstance(value, list):
        for item in value:
            for nested in _keys(item):
                yield nested


def test_report_prints_metrics_json_and_writes_both_files(tmp_path):
    """OR-11: both report files land and stdout equals the JSON report."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, out = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )

    json_path = out / "line-demo-plan-a1-coordination.json"
    md_path = out / "line-demo-plan-a1-coordination.md"
    assert json_path.is_file()
    assert md_path.is_file()
    assert json.loads(json_path.read_text(encoding="utf-8")) == report
    assert report["schema_version"] == 1
    assert report["stage"] == "plan"
    assert report["stage_attempt"] == 1
    assert report["decision"] == "decomposed"
    assert report["pattern"] == "parallel"
    assert report["slot_cap"] == 2


def test_report_wall_clock_is_first_dispatch_to_stage_u4(tmp_path):
    """OR-04: stage_u4_at - first started_at, never a commit timestamp."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )

    assert report["wall_clock_seconds"] == 400


def test_report_stage_close_supplies_the_u4_time_after_close(tmp_path):
    """OR-04/OR-11: the CLI input wins; a recorded stage-close is the fallback."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    ledger.append(wp_fixtures.stage_close_event(stage_u4_at=500))
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    from_close, _ = _report(spine, tmp_path / "reports", "--stage", "plan")
    from_cli, _ = _report(
        spine, tmp_path / "reports2", "--stage", "plan", "--stage-u4-at", "510"
    )

    assert from_close["wall_clock_seconds"] == 400
    assert from_cli["wall_clock_seconds"] == 410


def test_report_critical_path_is_the_duration_weighted_longest_path(tmp_path):
    """OR-05: cp[node] = duration[node] + max(cp[dep]); the sum is not the path."""
    plan = _diamond_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 300, 700, order=2)
    ledger += _attempt("plan-wp03", 300, 500, order=3)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "700"
    )

    assert report["wall_clock_seconds"] == 600
    assert report["critical_path_seconds"] == 600
    assert report["critical_path_seconds"] != 800  # sum of durations


def test_report_parallelism_efficiency_puts_the_product_in_the_denominator(
    tmp_path,
):
    """OR-06: sum(durations) / (wall_clock × max_concurrent), not × max."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )

    assert report["max_concurrent"] == 2
    assert report["parallelism_efficiency"] == pytest.approx(0.45)
    assert report["parallelism_efficiency"] != pytest.approx(1.8)


def test_report_max_concurrent_and_overlap_flag_detect_real_overlap(tmp_path):
    """OR-06/OR-12: overlap requires two genuinely overlapping intervals."""
    plan = _chain_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 200, order=1)
    ledger += _attempt("plan-wp02", 200, 300, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    sequential, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "300"
    )

    parallel_plan = _two_package_plan()
    parallel_ledger = [_plan_event(parallel_plan)]
    parallel_ledger += _attempt("plan-wp01", 100, 300, order=1)
    parallel_ledger += _attempt("plan-wp02", 120, 280, order=2)
    parallel_spine = _spine(
        tmp_path / "parallel", plan=parallel_plan, ledger=parallel_ledger
    )
    overlapping, _ = _report(
        parallel_spine,
        tmp_path / "reports2",
        "--stage",
        "plan",
        "--stage-u4-at",
        "500",
    )

    assert sequential["max_concurrent"] == 1
    assert sequential["overlap"] is False
    assert overlapping["max_concurrent"] == 2
    assert overlapping["overlap"] is True


def test_report_stage_executions_ignore_plan_repairs_and_package_retries(
    tmp_path,
):
    """OR-07: distinct dispatched (stage, attempt) pairs only; repairs never count."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger.append(wp_fixtures.plan_event(supersedes_plan_hash=plan["plan_hash"]))
    ledger.append(wp_fixtures.retry_event())
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )

    assert report["stage_attempts"] == 1
    assert report["canonical_stages"] == 8
    assert report["stage_executions_per_canonical"] == pytest.approx(0.125)


def test_report_stage_executions_include_a_reentered_stage_attempt(tmp_path):
    """OR-07/OR-16: a U5 retry dispatches a new attempt and increments the count."""
    plan = _two_package_plan()
    second = dict(plan)
    second["stage_attempt"] = 2
    second = wp_fixtures.make_plan(
        packages=plan["packages"], stage="plan", stage_attempt=2
    )
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger.append(
        wp_fixtures.plan_event(
            stage_attempt=2, plan_hash=second["plan_hash"]
        )
    )
    ledger += _attempt("plan-wp01", 400, 600, order=1, stage_attempt=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger, extra=wp_fixtures.plan_fence(second))

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "700"
    )

    assert report["stage_attempt"] == 2
    assert report["stage_attempts"] == 2
    assert report["stage_executions_per_canonical"] == pytest.approx(0.25)


def test_report_retry_counts_package_and_stage_separately(tmp_path):
    """OR-08: retries_package counts retry events; retries_stage = attempt - 1."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger.append(wp_fixtures.plan_event(stage_attempt=2))
    ledger += _attempt(
        "plan-wp01", 400, 700, order=1, wp_attempt=2, stage_attempt=2
    )
    ledger.insert(
        len(ledger) - 2,
        wp_fixtures.retry_event(
            retry_delta={
                "changed": ["budget"],
                "reason": "budget exhausted",
                "budget": {
                    "from_max_turns": 120,
                    "to_max_turns": 160,
                    "evidence_ref": "wp/line-plan-plan-wp01-a2w1.result.json",
                },
            }
        ),
    )
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine,
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-attempt",
        "2",
        "--stage-u4-at",
        "700",
    )

    assert report["retries_package"] == 1
    assert report["retries_stage"] == 1


def test_report_manual_interventions_rate_uses_the_session_count(tmp_path):
    """OR-09: the per-session rate needs both inputs; the count still reports."""
    plan = _chain_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 200, order=1)
    ledger += _attempt("plan-wp02", 200, 300, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    both, _ = _report(
        spine,
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-u4-at",
        "300",
        "--manual-interventions",
        "3",
        "--sessions",
        "2",
    )
    count_only, _ = _report(
        spine,
        tmp_path / "reports2",
        "--stage",
        "plan",
        "--stage-u4-at",
        "300",
        "--manual-interventions",
        "3",
    )
    neither, _ = _report(
        spine, tmp_path / "reports3", "--stage", "plan", "--stage-u4-at", "300"
    )

    assert both["manual_interventions"] == 3
    assert both["sessions"] == 2
    assert both["manual_interventions_per_session"] == pytest.approx(1.5)
    assert count_only["manual_interventions"] == 3
    assert count_only["manual_interventions_per_session"] == NOT_EVALUATED
    assert neither["manual_interventions"] == NOT_EVALUATED
    assert neither["sessions"] == NOT_EVALUATED
    assert neither["manual_interventions_per_session"] == NOT_EVALUATED


def test_report_token_cost_sums_only_when_every_dispatch_has_a_value(tmp_path):
    """OR-12: token cost is summed when available, otherwise not_evaluated."""
    plan = _two_package_plan(stage="implement", rule="decompose-implement-v1")
    ledger = [_plan_event(plan)]
    ledger += _attempt("implement-wp01", 100, 300, order=1)
    ledger += _attempt("implement-wp02", 100, 260, order=2)
    for event in ledger:
        if event["event"] == "dispatch":
            event["token_cost"] = 10 if event["wp_id"].endswith("01") else 20
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    summed, _ = _report(
        spine, tmp_path / "reports", "--stage", "implement", "--stage-u4-at", "500"
    )

    for event in ledger:
        if event["event"] == "dispatch" and event["wp_id"].endswith("02"):
            event["token_cost"] = NOT_EVALUATED
    partial_spine = _spine(
        tmp_path / "partial", plan=plan, ledger=ledger
    )
    partial, _ = _report(
        partial_spine,
        tmp_path / "reports2",
        "--stage",
        "implement",
        "--stage-u4-at",
        "500",
    )

    assert summed["token_cost"] == 30
    assert partial["token_cost"] == NOT_EVALUATED


def test_report_missing_timestamps_are_not_evaluated_not_zero(tmp_path):
    """OR-10 / Scenario E: a deleted timestamp is not_evaluated; wall-clock stays."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    for event in ledger:
        if event["event"] == "settle" and event["wp_id"] == "plan-wp02":
            del event["ended_at"]
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )
    no_u4, _ = _report(spine, tmp_path / "reports2", "--stage", "plan")

    assert report["wall_clock_seconds"] == 400
    assert report["critical_path_seconds"] == NOT_EVALUATED
    assert report["parallelism_efficiency"] == NOT_EVALUATED
    assert report["max_concurrent"] == NOT_EVALUATED
    assert report["critical_path_seconds"] != 0
    assert report["parallelism_efficiency"] != 0
    assert no_u4["wall_clock_seconds"] == NOT_EVALUATED


def test_report_without_plan_fence_does_not_invent_a_decomposition(tmp_path):
    """V-REP.6: no plan fence means decision=not_evaluated, not a guessed plan."""
    spine = _spine(
        tmp_path, ledger=[], extra="line_id: line-demo\nrun_id: run-demo"
    )

    report, out = _report(
        spine,
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-attempt",
        "1",
        "--stage-u4-at",
        "500",
    )

    assert report["decision"] == NOT_EVALUATED
    assert report["pattern"] == NOT_EVALUATED
    assert report["slot_cap"] == NOT_EVALUATED
    assert report["wall_clock_seconds"] == NOT_EVALUATED
    assert report["critical_path_seconds"] == NOT_EVALUATED
    assert report["stage_attempts"] == 0
    assert report["stage_executions_per_canonical"] == pytest.approx(0.0)
    assert (out / "line-demo-plan-a1-coordination.json").is_file()


def test_report_integration_order_is_declared_then_graph_derived(tmp_path):
    """VI-07/OR-12: the integrate event wins; otherwise the declared graph order."""
    plan = _chain_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 200, order=1)
    ledger += _attempt("plan-wp02", 200, 300, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    derived, _ = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "300"
    )

    ledger.append(
        wp_fixtures.integrate_event(order=["plan-wp02", "plan-wp01"])
    )
    declared_spine = _spine(tmp_path / "declared", plan=plan, ledger=ledger)
    declared, _ = _report(
        declared_spine,
        tmp_path / "reports2",
        "--stage",
        "plan",
        "--stage-u4-at",
        "300",
    )

    assert derived["integration_order"] == ["plan-wp01", "plan-wp02"]
    assert declared["integration_order"] == ["plan-wp02", "plan-wp01"]


def test_report_markdown_and_json_carry_the_same_values(tmp_path):
    """OR-12 / V-REP.4: both report files carry the same values."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, out = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )
    markdown = (out / "line-demo-plan-a1-coordination.md").read_text(
        encoding="utf-8"
    )

    assert "| wall_clock_seconds | 400 |" in markdown
    assert "| critical_path_seconds | 200 |" in markdown
    assert "| parallelism_efficiency | 0.45 |" in markdown
    assert "| max_concurrent | 2 |" in markdown
    assert "| overlap | true |" in markdown
    assert "plan-wp01" in markdown and "plan-wp02" in markdown


def test_report_never_writes_the_spine(tmp_path):
    """OR-11: the report reads the spine and never writes it."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 300, order=1)
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)
    before = spine.read_bytes()

    result = _run(
        spine,
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-u4-at",
        "500",
    )

    assert result.returncode == 0, result.stderr
    assert spine.read_bytes() == before


def test_report_does_not_copy_raw_transcripts_or_unknown_event_fields(tmp_path):
    """OR-12/V-LED.1: raw logs are never copied; unknown events are ignored."""
    plan = _two_package_plan()
    ledger = [_plan_event(plan)]
    attempts = _attempt("plan-wp01", 100, 300, order=1)
    attempts[0]["raw_log"] = "SECRET RAW TRANSCRIPT"
    ledger += attempts
    ledger += _attempt("plan-wp02", 100, 260, order=2)
    ledger.append({"event": "note", "detail": "UNKNOWN EVENT DETAIL"})
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    report, out = _report(
        spine, tmp_path / "reports", "--stage", "plan", "--stage-u4-at", "500"
    )
    markdown = (out / "line-demo-plan-a1-coordination.md").read_text(
        encoding="utf-8"
    )
    serialized = json.dumps(report)

    assert "SECRET RAW TRANSCRIPT" not in serialized
    assert "SECRET RAW TRANSCRIPT" not in markdown
    assert "UNKNOWN EVENT DETAIL" not in serialized
    for key in _keys(report):
        lowered = key.lower()
        assert "transcript" not in lowered
        assert "raw" not in lowered
        assert lowered not in {"stdout", "stderr", "log_body"}


def test_report_exits_2_for_unreadable_input(tmp_path):
    """OR-11 input errors use the deterministic input-error exit."""
    result = _run(
        tmp_path / "missing-state.md",
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-u4-at",
        "500",
    )

    assert result.returncode == 2
    assert "cannot read" in result.stderr.lower()
    assert not (tmp_path / "reports").exists() or not any(
        (tmp_path / "reports").iterdir()
    )


def test_report_rejects_negative_intervention_inputs(tmp_path):
    """OR-09: counts are non-negative integers."""
    plan = _chain_plan()
    ledger = [_plan_event(plan)]
    ledger += _attempt("plan-wp01", 100, 200, order=1)
    ledger += _attempt("plan-wp02", 200, 300, order=2)
    spine = _spine(tmp_path, plan=plan, ledger=ledger)

    result = _run(
        spine,
        tmp_path / "reports",
        "--stage",
        "plan",
        "--stage-u4-at",
        "300",
        "--manual-interventions",
        "-1",
    )

    assert result.returncode == 2
