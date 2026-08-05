"""Integration: cumulative refresh of the goal summary.

Covers SC-007 (one current summary + annotation preservation), SC-011 (cross-refresh
identity stability) and SC-012 (breakdown-diagram node bound with full data retention).

The decisive property under test is that cumulative state is authoritative in each
team's tracked ledger, not in the derived database — so a refresh advances existing
records and deleting the delivery directory loses nothing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
SUMMARIZE = REPO_ROOT / "skills/summarize-project/scripts"

pytestmark = [pytest.mark.integration]

requires_generator = pytest.mark.skipif(
    not GENERATOR.is_file(), reason="generator not implemented"
)

# FR-029 / FG-9 — must match AGGREGATE_COMPLETED_ABOVE in the generator
AGGREGATE_ABOVE = 3
# Upstream CG-6 threshold: WBS depth >=2 node count must stay within this
WBS_NODE_THRESHOLD = 15


def team_md(slug: str, *, goal_slug: str | None = None, pattern: str = "continuous") -> str:
    gs = f"goal_slug: {goal_slug}\n" if goal_slug else ""
    return f"""---
name: {slug} display
slug: {slug}
description: accumulation fixture
goal: >
  持续提炼可采纳的改进点。成功标准:四项产出齐全;每条改进点附证据路径;对被分析仓库零写入。
{gs}pattern: {pattern}
created: 2026-07-01
updated: 2026-08-01
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    lifecycle: persistent
config:
  maturity: L1
---

## Goal
持续提炼可采纳的改进点。

## Static Structure
| Role | Stage | Type |
|------|-------|------|
| team-supervisor | optimizer | Meta |

## Dynamic Structure
pattern: {pattern}
"""


def event(item_id: str, state: str, ts: str, *, phase: str = "PH-0001",
          title: str | None = None, identity: str = "explicit", **extra) -> dict:
    row = {
        "item_id": item_id,
        "title": title or f"条目 {item_id}",
        "phase_ref": phase,
        "state": state,
        "provenance": ".specify/teams/acc/runs/20260801T090000Z-report.md",
        "ts": ts,
        "identity": identity,
    }
    row.update(extra)
    return row


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    (tmp_path / ".specify/teams/acc/runs").mkdir(parents=True)
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\nrole: team-supervisor\n---\n", encoding="utf-8"
    )
    (tmp_path / ".specify/teams/acc/team.md").write_text(team_md("acc"), encoding="utf-8")
    (tmp_path / ".specify/teams/acc/runs/20260801T090000Z-report.md").write_text(
        "# Team Run Report: acc\n\n- **Outcome**: completed\n", encoding="utf-8"
    )
    return tmp_path


def append_events(sandbox: Path, rows: list[dict]) -> None:
    ledger = sandbox / ".specify/teams/acc/items.jsonl"
    with ledger.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def refresh(sandbox: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--team", "acc", "--repo-root", str(sandbox), "--json"],
        capture_output=True, text=True, cwd=str(sandbox),
    )


def form_of(sandbox: Path) -> dict:
    path = sandbox / ".specify/goal/acc/summary/data/project-input.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# SC-007 — one current summary, annotations preserved, both runs represented
# --------------------------------------------------------------------------


@requires_generator
def test_second_refresh_advances_existing_records(sandbox: Path) -> None:
    append_events(sandbox, [event("TI-0001", "in-progress", "2026-08-01T09:00:00Z")])
    assert refresh(sandbox).returncode == 0
    first = form_of(sandbox)
    assert [w["status"] for w in first["work_items"]] == ["进行中"]

    # a later run completes the same item and adds a new one
    append_events(sandbox, [
        event("TI-0001", "completed", "2026-08-02T09:00:00Z"),
        event("TI-0002", "in-progress", "2026-08-02T09:00:00Z"),
    ])
    assert refresh(sandbox).returncode == 0
    second = form_of(sandbox)

    by_id = {w["item_id"]: w for w in second["work_items"]}
    assert len(by_id) == 2, "both runs' items must appear in the current summary"
    assert by_id["acc.TI-0001"]["status"] == "已完成", "existing record must advance in place"
    assert by_id["acc.TI-0002"]["status"] == "进行中"


@requires_generator
def test_delivery_directory_holds_exactly_one_current_form(sandbox: Path) -> None:
    append_events(sandbox, [event("TI-0001", "completed", "2026-08-01T09:00:00Z")])
    for _ in range(3):
        assert refresh(sandbox).returncode == 0
    forms = list((sandbox / ".specify/goal/acc").rglob("project-input.yaml"))
    assert len(forms) == 1, f"expected exactly one current form, found {forms}"


@requires_generator
def test_reproducible_after_deleting_the_delivery_directory(sandbox: Path) -> None:
    """Cumulative state lives in the ledger, so a full rebuild loses nothing."""
    append_events(sandbox, [
        event("TI-0001", "completed", "2026-08-01T09:00:00Z"),
        event("TI-0002", "delayed", "2026-08-02T09:00:00Z"),
    ])
    assert refresh(sandbox).returncode == 0
    before = (sandbox / ".specify/goal/acc/summary/data/project-input.yaml").read_bytes()

    shutil.rmtree(sandbox / ".specify/goal/acc")
    assert refresh(sandbox).returncode == 0
    after = (sandbox / ".specify/goal/acc/summary/data/project-input.yaml").read_bytes()
    assert before == after, "regeneration from the ledger must be byte-identical"


# --------------------------------------------------------------------------
# SC-011 — identity stability across refreshes
# --------------------------------------------------------------------------


@requires_generator
def test_no_duplicates_and_no_silent_losses_across_refreshes(sandbox: Path) -> None:
    append_events(sandbox, [event(f"TI-{i:04d}", "in-progress", "2026-08-01T09:00:00Z") for i in range(1, 6)])
    assert refresh(sandbox).returncode == 0
    first_ids = [w["item_id"] for w in form_of(sandbox)["work_items"]]

    append_events(sandbox, [event(f"TI-{i:04d}", "completed", "2026-08-02T09:00:00Z") for i in range(1, 6)])
    assert refresh(sandbox).returncode == 0
    second_ids = [w["item_id"] for w in form_of(sandbox)["work_items"]]

    assert len(second_ids) == len(set(second_ids)), "duplicate work-item ids after refresh"
    assert set(first_ids) == set(second_ids), "identity set changed across refreshes"


@requires_generator
def test_rename_under_a_stable_id_does_not_create_a_new_item(sandbox: Path) -> None:
    """FR-026 — an explicit id survives retitling."""
    append_events(sandbox, [event("TI-0001", "in-progress", "2026-08-01T09:00:00Z", title="原标题")])
    assert refresh(sandbox).returncode == 0
    append_events(sandbox, [event("TI-0001", "in-progress", "2026-08-02T09:00:00Z", title="改过的标题")])
    assert refresh(sandbox).returncode == 0
    items = form_of(sandbox)["work_items"]
    assert len(items) == 1, f"rename produced a second record: {items}"
    assert items[0]["item_name"] == "改过的标题"


@requires_generator
def test_inferred_to_explicit_handover_merges_to_one_record(sandbox: Path) -> None:
    """FR-027 / IL-5 — the pair collapses, authoritative on the explicit id."""
    inferred_id = "TIX-abcdef12"
    append_events(sandbox, [
        event(inferred_id, "in-progress", "2026-08-01T09:00:00Z", identity="inferred", title="历史条目"),
    ])
    assert refresh(sandbox).returncode == 0
    assert len(form_of(sandbox)["work_items"]) == 1

    append_events(sandbox, [
        event("TI-0007", "completed", "2026-08-02T09:00:00Z", title="历史条目",
              supersedes=inferred_id),
    ])
    assert refresh(sandbox).returncode == 0
    items = form_of(sandbox)["work_items"]
    ids = [w["item_id"] for w in items]
    assert len(items) == 1, f"handover left duplicate records: {ids}"
    assert ids == ["acc.TI-0007"], ids
    assert items[0]["status"] == "已完成"


@requires_generator
def test_inferred_identities_are_marked_in_the_generation_report(sandbox: Path) -> None:
    append_events(sandbox, [
        event("TIX-deadbeef", "unknown", "2026-08-01T09:00:00Z", identity="inferred"),
    ])
    result = refresh(sandbox)
    assert result.returncode == 0
    report = json.loads(result.stdout)
    fields = " ".join(f["field"] for f in report["inferred_fields"])
    assert "TIX-deadbeef" in fields, f"inferred identity not marked: {report['inferred_fields']}"


# --------------------------------------------------------------------------
# SC-012 / FR-029 — retention in the data layer, aggregation in presentation
# --------------------------------------------------------------------------


@requires_generator
def test_completed_items_are_retained_and_counted_for_aggregation(sandbox: Path) -> None:
    completed = AGGREGATE_ABOVE + 4
    append_events(sandbox, [
        event(f"TI-{i:04d}", "completed", "2026-08-01T09:00:00Z") for i in range(1, completed + 1)
    ])
    append_events(sandbox, [event("TI-9001", "in-progress", "2026-08-01T09:00:00Z")])
    assert refresh(sandbox).returncode == 0
    doc = form_of(sandbox)

    # every item is retained in the data layer — zero deletion
    assert len(doc["work_items"]) == completed + 1
    coverage = doc["coverage"]
    assert coverage["candidate_total"] == completed + 1
    assert coverage["granularity_truncated"] == completed, (
        "completed items above the threshold must be counted as presentation-aggregated"
    )


@requires_generator
def test_aggregation_keeps_expanded_nodes_within_the_upstream_threshold(sandbox: Path) -> None:
    """SC-012 — long-running teams must not blow the CG-6 node bound."""
    append_events(sandbox, [
        event(f"TI-{i:04d}", "completed", "2026-08-01T09:00:00Z") for i in range(1, 41)
    ])
    append_events(sandbox, [
        event(f"TI-9{i:03d}", "in-progress", "2026-08-01T09:00:00Z") for i in range(1, 4)
    ])
    assert refresh(sandbox).returncode == 0
    doc = form_of(sandbox)
    coverage = doc["coverage"]
    expanded = coverage["candidate_total"] - coverage["granularity_truncated"]
    assert expanded <= WBS_NODE_THRESHOLD, (
        f"expanded node count {expanded} exceeds the CG-6 threshold {WBS_NODE_THRESHOLD}"
    )
    assert len(doc["work_items"]) == 43, "data-layer retention must remain 100%"


# --------------------------------------------------------------------------
# FR-019 — a deliberate goal edit keeps history and the directory
# --------------------------------------------------------------------------


@requires_generator
def test_goal_prose_edit_keeps_history_and_directory(sandbox: Path) -> None:
    append_events(sandbox, [event("TI-0001", "completed", "2026-08-01T09:00:00Z")])
    assert refresh(sandbox).returncode == 0
    before_dir = sorted(p.name for p in (sandbox / ".specify/goal").iterdir())

    team_file = sandbox / ".specify/teams/acc/team.md"
    team_file.write_text(
        team_md("acc").replace("持续提炼可采纳的改进点。", "改写后的目标叙述。"), encoding="utf-8"
    )
    result = refresh(sandbox)
    assert result.returncode == 0
    after_dir = sorted(p.name for p in (sandbox / ".specify/goal").iterdir())

    assert before_dir == after_dir, "a goal prose edit must not relocate the delivery directory"
    assert len(form_of(sandbox)["work_items"]) == 1, "history must survive a goal edit"

    # FR-019 — the change is recorded, not silently absorbed
    report = json.loads(result.stdout)
    assert report.get("goal_changed") is True, f"goal change not recorded: {report}"
    assert any("FR-019" in gap for gap in report["material_gaps"]), report["material_gaps"]


@requires_generator
def test_unchanged_goal_does_not_report_a_change(sandbox: Path) -> None:
    append_events(sandbox, [event("TI-0001", "completed", "2026-08-01T09:00:00Z")])
    assert refresh(sandbox).returncode == 0
    result = refresh(sandbox)
    assert result.returncode == 0
    assert json.loads(result.stdout).get("goal_changed") is not True


@requires_generator
def test_chain_still_loads_after_repeated_refreshes(sandbox: Path) -> None:
    """The accumulated form must remain acceptable to the invoked skill."""
    for day, state in ((1, "in-progress"), (2, "completed"), (3, "completed")):
        append_events(sandbox, [event("TI-0001", state, f"2026-08-0{day}T09:00:00Z")])
        assert refresh(sandbox).returncode == 0
    form = sandbox / ".specify/goal/acc/summary/data/project-input.yaml"
    val = subprocess.run(
        [sys.executable, str(SUMMARIZE / "validate-project-input.py"), "--input", str(form), "--json"],
        capture_output=True, text=True, cwd=str(sandbox),
    )
    assert val.returncode == 0, val.stdout + val.stderr
    assert json.loads(val.stdout)["status"] == "ready"
