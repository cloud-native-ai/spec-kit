"""Contract test: loop-effectiveness metrics — read-built, honest, never a gate
(Feature 072, User Story 5).

Pins `contracts/cadence-and-metrics.md` C-40…C-50 against the surfaces that own
them:

* the **cadence definition** (C-40) — "continuous" is capture on every
  qualifying run + the existing non-blocking threshold notice + explicit user
  triggering; no scheduler, resident process, timer, or self-starting periodic
  task exists in any Feature 072 surface;
* the **no-backfill rule and coverage boundary** (C-41, C-49) — metrics cover
  only runs from the channel's arming onward (the creation stamp of the unit's
  first external entry); earlier code-segment records are excluded by rule and
  the exclusion is disclosed, never backfilled;
* the **threshold-protocol × run-determination combination rule** (C-42) — the
  notice still appears only when both hold, stays non-blocking, and the metrics
  never feed its trigger condition, placement, or blocking behavior;
* the **four metrics with explicit numerator/denominator/sources** (C-43) —
  capture coverage, into-loop ratio, closure ratio, repeat-finding rate, all
  derived from the existing store, routing backlog, and code-segment records;
* the **closure evidence rule** (C-44) — closure counts only owner-file change
  evidence (a carried-by-* backlog row whose named owner file exists and whose
  mtime is later than the entry's `created`); `dispose` processed/ignored marks,
  a carried-by row alone, and open-unverified rows are never closure evidence;
* the **repeat-finding proxy** (C-45) — a coarse proxy over (file, severity)
  pairs extracted deterministically from the pointed-to record, labeled as a
  proxy, never phrased as a defect recurrence rate;
* the **read-built discipline** (C-46, C-47) — the engine's read-only
  `client-metrics` action recomputes from existing records on every report,
  persists nothing, has no write point, and is the program-first derivation
  (the agent never recomputes from raw `list` output);
* the **honesty rules** (C-48, C-50) — every zero/missing denominator renders
  that metric `not-evaluated` with its reason (never 0, never 100%, the row is
  never omitted); an entry whose pointed-to record is unreadable is excluded
  from the repeat-finding numerator and denominator together, disclosed with
  count and reason, and never changes the other three metrics.

Behavioural assertions execute inside the disposable client project built by
`tests/fixtures/client_project.py` (C-58); text assertions pin the feedback
command surfaces that carry the digest's metric readings (T022).
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    ClientProject,
    make_client_project,
)

pytestmark = pytest.mark.contract

ENGINE_SRC = FRAMEWORK_ROOT / "scripts" / "python" / "feedback-utils.py"
REVIEW_SCRIPT = (
    FRAMEWORK_ROOT
    / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
)
DOCS_FEEDBACK = FRAMEWORK_ROOT / "docs" / "reference" / "commands" / "feedback.md"
PATH_A = (
    FRAMEWORK_ROOT
    / "skills" / "internal" / "manage-feedback" / "references" / "path-a-digest.md"
)

UNIT = "custom:fixture/unit"
OTHER_UNIT = "custom:fixture/other"

#: The six severity levels (owner: git-delta-review.sh SEVERITY_LEVELS).
SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")

#: Scheduler constructs that must not exist in any Feature 072 engine surface
#: (C-40 / FR-019).
SCHEDULER_TOKENS = (
    "scheduler", "cron", "timer", "daemon", "resident process",
    "background thread", "threading", "asyncio", "periodic task",
)

#: The closed field set of a metric row (C-48/C-50: rows are never omitted;
#: `value` appears only when the metric is evaluated).
REPEAT_PROXY_LABEL_PARTS = ("proxy", "(file", "severity")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_record(project: ClientProject, spec_name: str, run_stamp: str,
                 notes: List[Tuple[str, str, str]]) -> str:
    """Write a code-segment record file mirroring `write_code_segment_record`
    (record header with the ISO run stamp) and `append_note` (the
    `### <icon> [<SEVERITY>] <file>` heading) — the shapes the engines own."""
    icons = {"blocking": "🔴", "important": "🟠", "suggestion": "🟢",
             "nitpick": "⚪", "question": "❓", "praise": "👍"}
    rel = f".specify/specs/{spec_name}/code-review.md"
    headings = "".join(
        f"\n### {icons[sev]} [{sev.upper()}] {path}\n\n> {comment} ({spec_name})\n"
        for sev, path, comment in notes
    )
    project.write(rel, (
        "# Code Review Report\n\n"
        "| 属性 | 值 |\n"
        "|------|-----|\n"
        "| **分支** | main |\n"
        f"| **日期** | `{run_stamp}` |\n"
        "\n## Review 意见\n" + headings
    ))
    return rel


def pointer_entry(project: ClientProject, unit: str, run_id: str,
                  record_rel: str) -> Dict:
    """Create one external pointer entry exactly in the capture payload shape
    (C-15 closed field set), via the engine's record action."""
    payload = "\n".join([
        f"record={record_rel}",
        "triage=run",
        *[f"{sev}=0" for sev in SEVERITIES],
        f"run={run_id}",
        f"unit={unit}",
    ])
    run = project.run_engine(
        "feedback-utils.py", "--action", "record",
        "--unit-id", unit, "--unit-type", "custom-unit", "--run-id", run_id,
        "--review", payload, "--points", "captured: one pointer entry",
        "--workspace-root", str(project.path), "--format", "json",
    )
    assert run.ok, run.describe()
    return run.json_stdout()


def entry_id_listing(project: ClientProject, unit: Optional[str] = None) -> List[Dict]:
    args = ["--action", "list", "--kind", "external", "--limit", "0",
            "--format", "json", "--workspace-root", str(project.path)]
    if unit:
        args += ["--unit-id", unit]
    run = project.run_engine("feedback-utils.py", *args)
    assert run.ok, run.describe()
    return run.json_stdout()["matches"]


BACKLOG_HEADER = (
    "| Routed | Source | Finding | Channel | Owner file(s) | Status | Closed by |\n"
    "|--------|--------|---------|---------|---------------|--------|-----------|\n"
)


def backlog_rows(project: ClientProject) -> str:
    path = project.feedback_dir / "backlog.md"
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def add_backlog_row(project: ClientProject, entry_id: str, *,
                    status: str = "carried-by-park",
                    owner: str = "`src/app.py`",
                    source: Optional[str] = None) -> None:
    """Append one routing-backlog row naming the entry (one row per entry,
    C-30) with a carried-by-* status form (E8: 承接类行)."""
    path = project.feedback_dir / "backlog.md"
    if not path.is_file():
        project.write(path.relative_to(project.path).as_posix(), BACKLOG_HEADER)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(
            f"| 2026-10-27 | {source or ('entry ' + entry_id)} | fixture finding | "
            f"park | {owner} | {status} | — |\n"
        )


def client_metrics(project: ClientProject, *extra: str) -> Dict:
    run = project.run_engine(
        "feedback-utils.py", "--action", "client-metrics",
        "--format", "json", "--workspace-root", str(project.path), *extra,
    )
    assert run.ok, run.describe()
    return run.json_stdout()


def metric(payload: Dict, name: str) -> Dict:
    assert name in payload["metrics"], (
        f"C-48: the metric row {name!r} MUST never be omitted; "
        f"got {sorted(payload['metrics'])}"
    )
    return payload["metrics"][name]


def tree_paths(project: ClientProject) -> Set[str]:
    return {
        p.relative_to(project.path).as_posix()
        for p in project.path.rglob("*")
    }


# --------------------------------------------------------------------------- #
# C-40 — "continuous" is capture + non-blocking notice + explicit triggering,
#        never a scheduler
# --------------------------------------------------------------------------- #

def test_c40_no_scheduler_resident_timer_in_any_feature_surface():
    for path in (ENGINE_SRC, REVIEW_SCRIPT):
        source = path.read_text(encoding="utf-8").lower()
        for token in SCHEDULER_TOKENS:
            assert token not in source, (
                f"C-40/FR-019: {token!r} must not exist in {path.name} — "
                "continuous capture is per-run, never scheduled"
            )
    docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
    assert "no scheduler" in docs, (
        "C-40: the feedback command docs page MUST state that continuous means "
        "capture on every qualifying run + the existing non-blocking threshold "
        "notice + explicit triggering, with no scheduler"
    )
    assert "resident process" in docs and "timer" in docs, (
        "C-40: the docs page MUST name the forbidden forms "
        "(scheduler / resident process / timer / self-starting periodic task)"
    )


def test_c40_capture_happens_per_qualifying_run_via_existing_fifth_step():
    """The cadence mechanism is the existing per-run capture step — a qualified
    run produces its entry without any new scheduling machinery (behavioural
    proof the cadence is run-attached, reusing the US1 fixture flow)."""
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        record_rel = write_record(
            project, "run-a", iso(now),
            [("blocking", "src/app.py", "defect one")],
        )
        pointer_entry(project, UNIT, iso(now), record_rel)
        assert len(entry_id_listing(project, UNIT)) == 1


# --------------------------------------------------------------------------- #
# C-41 — no backfill; the coverage boundary is stated in the report itself
# --------------------------------------------------------------------------- #

def test_c41_records_before_arming_are_excluded_never_backfilled():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        old_rel = write_record(
            project, "pre-arming", iso(now - timedelta(hours=2)),
            [("blocking", "src/old.py", "pre-arming defect")],
        )
        # The channel arms (first external entry appears) AFTER the old record.
        # Post-arming stamps carry a margin: the arming boundary is the entry's
        # created stamp at 1-second precision, so stamps must clear it by more
        # than a sub-second race.
        new_rel = write_record(
            project, "post-arming", iso(now + timedelta(minutes=5)),
            [("blocking", "src/app.py", "post-arming defect")],
        )
        pointer_entry(project, UNIT, iso(now + timedelta(minutes=5)), new_rel)
        payload = client_metrics(project, "--unit", UNIT)
        coverage = metric(payload, "capture_coverage")
        assert coverage["status"] == "evaluated", coverage
        assert coverage["excluded_before_arming"] == 1, (
            "C-41/C-49: exactly one record predates the arming boundary and "
            f"its exclusion MUST be disclosed; got {coverage}"
        )
        assert coverage["denominator"] == 1, coverage
        assert coverage["numerator"] == 1, coverage
        assert coverage["value"] == 1.0, coverage
        # No backfill: the old record never gains an entry, even though the
        # metric run saw it.
        assert len(entry_id_listing(project, UNIT)) == 1, (
            "C-41: reading the metrics MUST NOT create entries for "
            "pre-arming records (no backfill)"
        )
        assert old_rel not in {
            e["run_id"] for e in entry_id_listing(project, UNIT)
        }
        docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
        assert re.search(r"never backfill", docs, re.IGNORECASE), (
            "C-41: the metrics surface MUST state the coverage boundary "
            "(arming onward) and that pre-arming records are never backfilled"
        )


# --------------------------------------------------------------------------- #
# C-42 — the threshold-protocol × run-determination combination rule is unchanged
# --------------------------------------------------------------------------- #

def test_c42_threshold_combination_rule_unchanged_and_metrics_never_feed_it():
    source = ENGINE_SRC.read_text(encoding="utf-8")
    assert re.search(r"def should_prompt\(count: int, threshold: int\) -> bool:\n"
                     r"    return count >= threshold\n", source), (
        "C-42: the threshold predicate stays count >= threshold — the existing "
        "combination rule (both the threshold hold AND the run-determination "
        "verdict hold → notice) must not be re-shaped by this feature"
    )
    action_match = re.search(
        r"def action_client_metrics\(.*?\n(?=\ndef |\n_ACTIONS)", source, re.S)
    assert action_match, "C-47: the client-metrics action must exist"
    action_src = action_match.group(0)
    assert "should_prompt" not in action_src, (
        "C-42/C-48: the metrics action MUST NOT invoke the threshold prompt "
        "machinery — the readings are not a threshold input"
    )
    assert "threshold" not in action_src, (
        "C-48: the metrics action MUST NOT read or write threshold state"
    )
    docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
    assert re.search(r"both (hold|true)", docs), (
        "C-42: the docs surface MUST record that the notice still appears only "
        "when both the threshold hold and the run-determination verdict hold"
    )
    assert re.search(r"non-blocking", docs), (
        "C-42: the docs surface MUST record that the notice stays non-blocking"
    )


# --------------------------------------------------------------------------- #
# C-43 — four metrics, each with explicit numerator, denominator, source
# --------------------------------------------------------------------------- #

def test_c43_four_metrics_with_explicit_numerator_denominator_and_values():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel_a = write_record(project, "m-a", iso(now + timedelta(minutes=5)),
                             [("blocking", "src/app.py", "defect A")])
        entry_a = pointer_entry(project, UNIT, iso(now + timedelta(minutes=5)), rel_a)
        time.sleep(1.1)                       # deterministic entry ordering
        rel_b = write_record(project, "m-b", iso(now + timedelta(minutes=6)),
                             [("blocking", "src/app.py", "defect A again")])
        entry_b = pointer_entry(project, UNIT, iso(now + timedelta(minutes=6)), rel_b)
        # Entry A is routed (carried) and its owner file changed after creation.
        add_backlog_row(project, entry_a["id"])
        project.write("src/app.py", "def f():\n    return 2\n")
        payload = client_metrics(project, "--unit", UNIT)
        assert set(payload["metrics"]) == {
            "capture_coverage", "into_loop_ratio", "closure_ratio",
            "repeat_finding_rate",
        }, payload
        coverage = metric(payload, "capture_coverage")
        assert (coverage["numerator"], coverage["denominator"]) == (2, 2)
        assert coverage["value"] == 1.0
        into_loop = metric(payload, "into_loop_ratio")
        assert (into_loop["numerator"], into_loop["denominator"]) == (1, 2)
        assert into_loop["value"] == 0.5
        closure = metric(payload, "closure_ratio")
        assert (closure["numerator"], closure["denominator"]) == (1, 2), closure
        assert closure["value"] == 0.5
        repeat = metric(payload, "repeat_finding_rate")
        # Entry B's record repeats the (src/app.py, blocking) pair of entry A's.
        assert (repeat["numerator"], repeat["denominator"]) == (1, 2), repeat
        assert repeat["value"] == 0.5


def test_c43_metric_sources_are_existing_records_only():
    """Every input face is named: the store entries, the routing backlog, and
    the code-segment records — no new store, index, or ledger participates."""
    source = ENGINE_SRC.read_text(encoding="utf-8")
    action_match = re.search(
        r"def action_client_metrics\(.*?\n(?=\ndef |\n_ACTIONS)", source, re.S)
    assert action_match, "C-47: the client-metrics action must exist"
    action_src = action_match.group(0)
    for forbidden in ("ensure_feedback_dir", "write_text_atomic",
                      "write_state_file", "migrate_legacy_index"):
        assert forbidden not in action_src, (
            f"C-46/C-47: the read-only action MUST NOT call {forbidden} "
            "— it has no write point"
        )


# --------------------------------------------------------------------------- #
# C-44 — closure requires owner-file change evidence; routing marks never count
# --------------------------------------------------------------------------- #

def test_c44_closure_counts_only_owner_file_change_evidence():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        # Owner file exists but predates both entries (no change evidence).
        project.write("src/app.py", "def f():\n    return 1\n")
        time.sleep(1.1)
        rel_a = write_record(project, "c-a", iso(now), [("nitpick", "src/app.py", "n")])
        entry_a = pointer_entry(project, UNIT, iso(now), rel_a)
        time.sleep(1.1)
        rel_b = write_record(project, "c-b", iso(now + timedelta(minutes=1)),
                             [("nitpick", "src/other.py", "n")])
        entry_b = pointer_entry(project, UNIT, iso(now + timedelta(minutes=1)), rel_b)
        # Entry A: carried row + owner file changed after creation → closed.
        add_backlog_row(project, entry_a["id"])
        time.sleep(1.1)
        project.write("src/app.py", "def f():\n    return 2\n")
        # Entry B: disposed `processed` with NO backlog row — a routing mark
        # alone must never count as into-loop or closure evidence.
        run = project.run_engine(
            "feedback-utils.py", "--action", "dispose", "--id", entry_b["id"],
            "--to", "processed", "--workspace-root", str(project.path),
        )
        assert run.ok, run.describe()
        payload = client_metrics(project, "--unit", UNIT)
        into_loop = metric(payload, "into_loop_ratio")
        closure = metric(payload, "closure_ratio")
        assert (into_loop["numerator"], into_loop["denominator"]) == (1, 2), into_loop
        assert (closure["numerator"], closure["denominator"]) == (1, 2), closure
        docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
        assert re.search(r"processed/ignored.*(local metadata|never)|"
                         r"(never|not)[^\n]*processed/ignored", docs), (
            "C-44: the docs surface MUST state that dispose processed/ignored "
            "marks are local metadata and never closure evidence"
        )
        assert re.search(r"carried[^\n]*(not |never )[^\n]*clos|clos[^\n]*change evidence",
                         docs, re.IGNORECASE), (
            "C-44: the docs surface MUST state routing ≠ completion — "
            "closure needs owner-file change evidence"
        )


def test_c44_carried_row_with_missing_or_unchanged_owner_file_is_not_closed():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        project.write("src/app.py", "def f():\n    return 1\n")
        time.sleep(1.1)
        rel = write_record(project, "c-missing", iso(now),
                           [("nitpick", "src/never.py", "n")])
        entry = pointer_entry(project, UNIT, iso(now), rel)
        add_backlog_row(project, entry["id"], owner="`src/does-not-exist.py`")
        payload = client_metrics(project, "--unit", UNIT)
        into_loop = metric(payload, "into_loop_ratio")
        closure = metric(payload, "closure_ratio")
        assert (into_loop["numerator"], into_loop["denominator"]) == (1, 1), into_loop
        assert (closure["numerator"], closure["denominator"]) == (0, 1), (
            "C-44: a carried row naming a missing owner file is carried, "
            f"never closed; got {closure}"
        )


# --------------------------------------------------------------------------- #
# C-45 — repeat-finding rate is a labeled coarse proxy over (file, severity)
# --------------------------------------------------------------------------- #

def test_c45_repeat_finding_rate_is_a_proxy_labeled_coarse():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel_a = write_record(project, "p-a", iso(now),
                             [("blocking", "src/app.py", "dup defect")])
        pointer_entry(project, UNIT, iso(now), rel_a)
        time.sleep(1.1)
        # Same unit, same (file, severity) pair → the later entry repeats.
        rel_b = write_record(project, "p-b", iso(now + timedelta(minutes=1)),
                             [("blocking", "src/app.py", "dup defect again")])
        pointer_entry(project, UNIT, iso(now + timedelta(minutes=1)), rel_b)
        time.sleep(1.1)
        # A different unit's entry with the same pair must NOT count (pairs
        # compare within the same unit only).
        project.arm(OTHER_UNIT)
        rel_c = write_record(project, "p-c", iso(now + timedelta(minutes=2)),
                             [("blocking", "src/app.py", "other unit")])
        pointer_entry(project, OTHER_UNIT, iso(now + timedelta(minutes=2)), rel_c)
        payload = client_metrics(project)          # no unit filter: all units
        repeat = metric(payload, "repeat_finding_rate")
        assert repeat["proxy"] is True, (
            "C-45: the proxy label MUST travel with the repeat-finding rate"
        )
        label = repeat["proxy_label"]
        for part in REPEAT_PROXY_LABEL_PARTS:
            assert part in label, (
                f"C-45: the proxy label MUST name itself a coarse proxy over "
                f"(file, severity) pairs; missing {part!r} in {label!r}"
            )
        assert "not a defect recurrence rate" in label, (
            "C-45: the label MUST disclaim the defect-recurrence reading"
        )
        assert (repeat["numerator"], repeat["denominator"]) == (1, 3), repeat
        docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
        assert "coarse proxy" in docs and "never a defect recurrence rate" in docs, (
            "C-45: the docs surface MUST label the repeat-finding rate a "
            "coarse proxy and never phrase it as a defect recurrence rate"
        )


# --------------------------------------------------------------------------- #
# C-46 — read-built: recomputed every report, nothing persisted, no scoring
# --------------------------------------------------------------------------- #

def test_c46_readings_identical_across_reports_and_store_tree_unchanged():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel = write_record(project, "rb", iso(now), [("nitpick", "src/a.py", "n")])
        entry = pointer_entry(project, UNIT, iso(now), rel)
        add_backlog_row(project, entry["id"])
        project.write("src/a.py", "x = 2\n")
        before_paths = tree_paths(project)
        first = client_metrics(project, "--unit", UNIT)
        second = client_metrics(project, "--unit", UNIT)
        assert first == second, (
            "SC-005: same records → same readings; the metrics are read-built, "
            "never persisted aggregates"
        )
        assert tree_paths(project) == before_paths, (
            "C-46/SC-005: the store tree MUST gain no aggregate, index, or "
            "score file from a metrics report"
        )
        for name, row in first["metrics"].items():
            for forbidden in ("score", "total", "weight", "grade"):
                assert forbidden not in row, (
                    f"C-46: no scoring vocabulary may attach to {name!r}: "
                    f"{forbidden!r} found in {row}"
                )


def test_c46_action_has_no_write_point_even_against_a_read_only_store():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel = write_record(project, "ro", iso(now), [("nitpick", "src/a.py", "n")])
        pointer_entry(project, UNIT, iso(now), rel)
        project.feedback_dir.chmod(0o555)
        try:
            run = project.run_engine(
                "feedback-utils.py", "--action", "client-metrics",
                "--format", "json", "--workspace-root", str(project.path),
            )
        finally:
            project.feedback_dir.chmod(0o755)
        assert run.ok, (
            "C-46/C-47: the read-only action MUST succeed against a read-only "
            f"store — it has no write point; got\n{run.describe()}"
        )


# --------------------------------------------------------------------------- #
# C-47 — program-first: the engine action is the derivation surface
# --------------------------------------------------------------------------- #

def test_c47_engine_action_is_the_machine_readable_derivation():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel = write_record(project, "pf", iso(now), [("praise", "src/a.py", "ok")])
        pointer_entry(project, UNIT, iso(now), rel)
        run_out = client_metrics(project, "--unit", UNIT)
        source = ENGINE_SRC.read_text(encoding="utf-8")
        assert '"client-metrics"' in re.search(
            r'choices=\[(.*?)\]', source[source.index('"--action"'):], re.S).group(1), (
            "C-47: client-metrics MUST be an explicit --action choice"
        )
        assert re.search(r'"client-metrics":\s*action_client_metrics', source), (
            "C-47: the action must be wired into the engine's _ACTIONS table"
        )
        manifest = re.search(
            r'"client-metrics":\s*\{[^}]*\}', source)
        assert manifest and '"--unit"' in manifest.group(0), (
            "C-47: ARG_MANIFEST must classify client-metrics (source: --unit)"
        )
        out = project.run_engine(
            "feedback-utils.py", "--action", "args-manifest", "--format", "json",
            "--workspace-root", str(project.path),
        )
        assert out.ok, out.describe()
        assert "client-metrics" in out.json_stdout(), (
            "C-47: the machine-readable argument manifest must expose the action"
        )
        assert run_out["unit"] == UNIT, run_out
        assert run_out["boundary"] is not None, (
            "C-49: the arming boundary MUST be visible in the output"
        )


# --------------------------------------------------------------------------- #
# C-48 — zero/missing denominators render not-evaluated with reason, never
#        0, never 100%, and the row is never omitted
# --------------------------------------------------------------------------- #

def test_c48_zero_denominators_report_not_evaluated_with_reason():
    with make_client_project() as project:
        project.arm(UNIT)
        payload = client_metrics(project, "--unit", UNIT)
        for name in ("capture_coverage", "into_loop_ratio", "closure_ratio",
                     "repeat_finding_rate"):
            row = metric(payload, name)
            assert row["status"] == "not-evaluated", (
                f"C-48: with no client entries {name!r} MUST report "
                f"not-evaluated; got {row}"
            )
            assert row.get("reason"), (
                f"C-48: not-evaluated rows MUST carry a reason; got {row}"
            )
            assert "value" not in row, (
                f"C-48: not-evaluated rows MUST NOT render a ratio "
                f"(never 0, never 100%); got {row}"
            )
        # A unit filter matching nothing renders the same honesty …
        payload = client_metrics(project, "--unit", "custom:nobody/there")
        for name in payload["metrics"]:
            assert payload["metrics"][name]["status"] == "not-evaluated", (
                f"C-48: unit filter with no entries: {name!r} must be "
                f"not-evaluated; got {payload['metrics'][name]}"
            )


def test_c48_capture_coverage_not_evaluated_when_no_record_qualifies():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        # The only record predates the arming boundary → denominator zero.
        write_record(project, "ancient", iso(now - timedelta(hours=3)),
                     [("nitpick", "src/old.py", "old")])
        new_rel = write_record(project, "fresh", iso(now), [("nitpick", "src/a.py", "n")])
        pointer_entry(project, UNIT, iso(now), new_rel)
        # Remove the qualifying record from disk: the captured run's record is
        # gone → numerator defined over qualifying record stamps only.
        (project.path / ".specify/specs/fresh/code-review.md").unlink()
        payload = client_metrics(project, "--unit", UNIT)
        coverage = metric(payload, "capture_coverage")
        assert coverage["status"] == "not-evaluated", coverage
        assert "value" not in coverage, coverage


# --------------------------------------------------------------------------- #
# C-49 — the capture-coverage boundary is the first external entry's created
# --------------------------------------------------------------------------- #

def test_c49_boundary_is_first_external_entry_and_exclusion_is_disclosed():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        # A record captured IMMEDIATELY at arming keeps a run stamp that can
        # predate the first entry's created stamp (real clock skew across the
        # capture) — the boundary rule excludes it from the coverage base.
        early_rel = write_record(project, "skew", iso(now - timedelta(seconds=90)),
                                 [("blocking", "src/app.py", "skew")])
        pointer_entry(project, UNIT, iso(now - timedelta(seconds=90)), early_rel)
        payload = client_metrics(project, "--unit", UNIT)
        coverage = metric(payload, "capture_coverage")
        assert coverage["status"] == "not-evaluated", (
            "C-49: a record whose run stamp predates the first external "
            f"entry's created stamp is excluded by rule; got {coverage}"
        )
        assert coverage.get("excluded_before_arming", 0) >= 1, coverage
        assert payload["boundary"] is not None
        # The exclusion is disclosed, not silently dropped.
        reason_text = json.dumps(payload, ensure_ascii=False)
        assert "excluded_before_arming" in reason_text


# --------------------------------------------------------------------------- #
# C-50 — an entry whose pointed-to record is unreadable is excluded from the
#        repeat-finding numerator and denominator together, disclosed, and
#        the other three metrics are unchanged
# --------------------------------------------------------------------------- #

def test_c50_unreadable_record_excluded_from_repeat_rate_only():
    with make_client_project() as project:
        project.arm(UNIT)
        now = datetime.now(timezone.utc)
        rel_ok = write_record(project, "u-ok", iso(now),
                              [("blocking", "src/app.py", "live")])
        entry_ok = pointer_entry(project, UNIT, iso(now), rel_ok)
        time.sleep(1.1)
        # This entry points at a record that does not exist.
        pointer_entry(project, UNIT, iso(now + timedelta(minutes=1)),
                      ".specify/specs/gone/code-review.md")
        add_backlog_row(project, entry_ok["id"])
        payload = client_metrics(project, "--unit", UNIT)
        repeat = metric(payload, "repeat_finding_rate")
        assert repeat["excluded_unreadable_records"] == 1, (
            "C-50: the unreadable-record exclusion MUST be counted; "
            f"got {repeat}"
        )
        assert repeat.get("excluded_reason"), repeat
        assert (repeat["numerator"], repeat["denominator"]) == (0, 1), (
            "C-50: the unreadable entry leaves both numerator and denominator "
            f"together; got {repeat}"
        )
        # The other three metrics still count the entry in their denominators.
        into_loop = metric(payload, "into_loop_ratio")
        closure = metric(payload, "closure_ratio")
        assert into_loop["denominator"] == 2, into_loop
        assert closure["denominator"] == 2, (
            "C-50: the repeat-rate exclusion never changes the other metrics; "
            f"got {closure}"
        )
