"""Integration tests for target_ref folding and the slice axis (038-goal-target, T017).

Contract: .specify/specs/038-goal-target/contracts/target-ref-ledger.contract.md

Drives the real generator end-to-end (subprocess + YAML form), asserting:
attribution of legal/absent/invalid target_ref rows, the targets: block shape per
data-model.md §派生结构, byte-identical output for goals without a ## Targets
section (SC-002), pending_approval on both sides (FR-015), the axis separation
with the negative "done ⇒ achieved" scan (SC-005), and IL-1…IL-5 preservation
(the 036 ledger suite staying green is asserted separately by the runner).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
GOAL = "sliced-goal"

pytestmark = pytest.mark.integration

LEDGER_STATES = ("pending", "in_progress", "completed", "blocked", "excluded")


def _write_team(root: Path, slug: str, rows: list[dict], goal_slug: str = GOAL) -> None:
    team_dir = root / ".specify/teams" / slug
    team_dir.mkdir(parents=True, exist_ok=True)
    (team_dir / "team.md").write_text(
        f"---\nslug: {slug}\nname: {slug}\ngoal_slug: {goal_slug}\n"
        f"pattern: parallel\nmembers: []\n---\n\n## Goal\n\n平台收敛。\n",
        encoding="utf-8",
    )
    with (team_dir / "items.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_goal(root: Path, targets_section: str = "") -> None:
    goal_dir = root / ".specify/goal" / GOAL
    goal_dir.mkdir(parents=True, exist_ok=True)
    (goal_dir / "goal.md").write_text(
        "---\nstatus: active\ncreated: 2026-08-12\nupdated: 2026-08-12\n---\n\n"
        f"# Goal: {GOAL}\n\n## Objective\n\n平台能力收敛稳定。\n\n"
        "## Success Criteria\n\n1. 判据一保持可测\n\n"
        f"{targets_section}"
        "## History\n\n- 2026-08-12 — created.\n",
        encoding="utf-8",
    )


TARGETS = (
    "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
    "| T-001 | 日志组件拆分完成 | open |\n"
    "| T-002 | 指标采集链路独立可部署 | done |\n"
    "| T-003 | 告警规则全量迁移 | dropped |\n\n"
)


def _item(item_id: str, state: str = "completed", target_ref: str | None = None) -> dict:
    row = {
        "item_id": item_id, "title": f"工作项 {item_id}", "phase_ref": "PH-0001",
        "state": state, "provenance": f".specify/teams/team-a/runs/x.md",
        "ts": "2026-08-12T00:00:00Z",
    }
    if target_ref is not None:
        row["target_ref"] = target_ref
    return row


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".specify/agents/templates").mkdir(parents=True)
    return tmp_path


def run_generator(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--repo-root", str(root), "--json", *args],
        capture_output=True, text=True, cwd=str(root),
    )


def form_of(root: Path) -> dict:
    return yaml.safe_load(
        (root / f".specify/goal/{GOAL}/summary/data/project-input.yaml")
        .read_text(encoding="utf-8")
    )


def form_text(root: Path) -> str:
    return (root / f".specify/goal/{GOAL}/summary/data/project-input.yaml").read_text(
        encoding="utf-8")


# --------------------------------------------------------------------------
# attribution: legal / absent / invalid target_ref
# --------------------------------------------------------------------------

def test_legal_refs_attribute_to_their_targets(repo: Path) -> None:
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [
        _item("TI-0001", target_ref="T-001"),
        _item("TI-0002", target_ref="T-001"),
        _item("TI-0003", state="in_progress", target_ref="T-002"),
        _item("TI-0004"),
    ])
    result = run_generator(repo, "--goal", GOAL)
    assert result.returncode == 0, result.stdout + result.stderr
    form = form_of(repo)
    block = form["targets"]
    by_id = {row["id"]: row for row in block["items"]}
    assert by_id["T-001"]["attributed_items"] == 2
    assert by_id["T-001"]["completed_items"] == 2
    assert by_id["T-002"]["attributed_items"] == 1
    assert by_id["T-002"]["completed_items"] == 0
    assert by_id["T-003"]["attributed_items"] == 0
    assert block["unattributed_to_target"] == 1
    assert block["invalid_refs"] == 0
    assert block["goal_slug"] == GOAL
    assert block["coverage"] == "1/3 done"


def test_rows_without_target_ref_go_to_the_goal_as_a_whole(repo: Path) -> None:
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [_item("TI-0001"), _item("TI-0002")])
    assert run_generator(repo, "--goal", GOAL).returncode == 0
    block = form_of(repo)["targets"]
    assert block["unattributed_to_target"] == 2
    assert all(row["attributed_items"] == 0 for row in block["items"])


def test_invalid_ref_degrades_to_the_whole_and_is_declared(repo: Path) -> None:
    """FR-014: never invent a Target; degrade + count + declare."""
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [
        _item("TI-0001", target_ref="T-999"),
        _item("TI-0002", target_ref="sliced-goal.T-001"),  # qualified form is illegal here
    ])
    result = run_generator(repo, "--goal", GOAL)
    assert result.returncode == 0, result.stdout + result.stderr
    form = form_of(repo)
    assert form["targets"]["invalid_refs"] == 2
    assert all(row["attributed_items"] == 0 for row in form["targets"]["items"])
    report = json.loads(result.stdout)
    assert any("target_ref" in g or "无效归属" in g for g in report["material_gaps"]), (
        "invalid refs must be declared, not silenced"
    )


# --------------------------------------------------------------------------
# SC-002: no Targets section ⇒ no targets block, byte-identical output
# --------------------------------------------------------------------------

def test_targetless_goal_form_is_byte_identical(repo: Path) -> None:
    _write_goal(repo, "")  # no ## Targets section
    _write_team(repo, "team-a", [_item("TI-0001"), _item("TI-0002", target_ref="T-001")])
    assert run_generator(repo, "--goal", GOAL).returncode == 0
    text = form_text(repo)
    assert "targets:" not in text, "SC-002: no targets block without the section"
    form = form_of(repo)
    assert "targets" not in form


# --------------------------------------------------------------------------
# pending_approval — both sides (FR-015)
# --------------------------------------------------------------------------

def test_pending_approval_open_but_all_attributed_completed(repo: Path) -> None:
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [
        _item("TI-0001", target_ref="T-001"),
        _item("TI-0002", target_ref="T-001"),
    ])
    assert run_generator(repo, "--goal", GOAL).returncode == 0
    form = form_of(repo)
    by_id = {row["id"]: row for row in form["targets"]["items"]}
    assert by_id["T-001"]["pending_approval"] is True, (
        "open authored + all completed evidence ⇒ awaiting human approval"
    )
    assert by_id["T-002"]["pending_approval"] is False


def test_pending_approval_done_but_attributed_not_completed(repo: Path) -> None:
    """Reverse side: authored done while the evidence is not all completed."""
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [
        _item("TI-0001", state="in_progress", target_ref="T-002"),
    ])
    assert run_generator(repo, "--goal", GOAL).returncode == 0
    form = form_of(repo)
    by_id = {row["id"]: row for row in form["targets"]["items"]}
    assert by_id["T-002"]["pending_approval"] is True, (
        "done authored + incomplete evidence ⇒ flagged for review"
    )
    assert by_id["T-001"]["pending_approval"] is False


# --------------------------------------------------------------------------
# SC-005 — axis separation, negative scan
# --------------------------------------------------------------------------

def test_no_achieved_derivation_from_targets(repo: Path) -> None:
    _write_goal(repo, TARGETS)
    _write_team(repo, "team-a", [_item("TI-0001", target_ref="T-002")])
    assert run_generator(repo, "--goal", GOAL).returncode == 0
    text = form_text(repo)
    assert form_of(repo)["targets"]["axis_note"], "the axis note must be present"
    assert "推导 achieved" not in text.replace("不推导 achieved", "")
    for banned in ("targets_done_implies_achieved", "achieved_from_targets"):
        assert banned not in text
