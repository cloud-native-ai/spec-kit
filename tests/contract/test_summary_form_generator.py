"""Contract tests for the team project-form generator.

Pins `contracts/team-project-form.contract.md` rules FG-1…FG-18. The generator is
the one executable deliverable of this requirement, so these are real behavioural
tests against its CLI, not structural assertions.
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
SUMMARIZE_SCRIPTS = REPO_ROOT / "skills/summarize-project/scripts"

pytestmark = pytest.mark.contract

requires_generator = pytest.mark.skipif(
    not GENERATOR.is_file(), reason="build-summary-input.py not implemented yet"
)


# --------------------------------------------------------------------------
# Fixture helpers — build a throwaway teams tree
# --------------------------------------------------------------------------


def write_team(
    teams_dir: Path,
    slug: str,
    *,
    pattern: str = "continuous",
    goal_slug: str | None = None,
    goal: str = "把参考项目的可采纳改进点提炼出来。成功标准:四项产出齐全;每条改进点附证据路径。",
    members: str = """members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    lifecycle: persistent
""",
    items: list[dict] | None = None,
    runs: list[str] | None = None,
) -> Path:
    team = teams_dir / slug
    (team / "runs").mkdir(parents=True, exist_ok=True)
    gs = f"goal_slug: {goal_slug}\n" if goal_slug else ""
    (team / "team.md").write_text(
        f"""---
name: {slug} display
slug: {slug}
description: fixture team
goal: >
  {goal}
{gs}pattern: {pattern}
created: 2026-07-01
updated: 2026-07-30
{members}config:
  maturity: L1
---

## Goal
{goal}

## Static Structure
| Role | Stage | Type |
|------|-------|------|
| team-supervisor | optimizer | Meta |

## Dynamic Structure
pattern: {pattern}
""",
        encoding="utf-8",
    )
    if items is not None:
        (team / "items.jsonl").write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n",
            encoding="utf-8",
        )
    for name in runs or []:
        (team / "runs" / name).write_text(
            f"""# Team Run Report: {slug} display

- **Team**: {slug}
- **Goal**: {goal}
- **Started**: 2026-07-30T08:00:00Z  **Finished**: 2026-07-30T09:00:00Z
- **Pattern**: {pattern}
- **Outcome**: completed

## Result Summary
fixture run

## Deliverables
| Artifact | Target path |
|----------|-------------|
| fixture artifact | docs/fixture.md |

## Execution Detail
fixture detail

## Run Workspace
- Intermediates: `.specify/teams/.work/{slug}/`
""",
            encoding="utf-8",
        )
    return team


def item(item_id: str, *, state: str = "completed", phase: str = "PH-0001",
         title: str = "条目", identity: str = "explicit", **extra) -> dict:
    row = {
        "item_id": item_id,
        "title": title,
        "phase_ref": phase,
        "state": state,
        "provenance": ".specify/teams/demo/runs/20260730T080000Z-report.md",
        "ts": "2026-07-30T09:00:00Z",
        "identity": identity,
    }
    row.update(extra)
    return row


def run_generator(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    """A miniature repo root containing only .specify/teams and .specify/agents."""
    (tmp_path / ".specify/teams").mkdir(parents=True)
    (tmp_path / ".specify/agents/templates").mkdir(parents=True)
    (tmp_path / ".specify/agents/instances").mkdir(parents=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\nrole: team-supervisor\n---\n\nbody\n", encoding="utf-8"
    )
    return tmp_path


# --------------------------------------------------------------------------
# FG interface surface
# --------------------------------------------------------------------------


@requires_generator
def test_unknown_slug_is_an_input_error(workspace: Path) -> None:
    result = run_generator("--team", "no-such-team", cwd=workspace)
    assert result.returncode == 2, result.stdout + result.stderr


@requires_generator
def test_materialless_goal_is_declined_with_exit_3(workspace: Path) -> None:
    """FG-12: no ledger and no run reports → refuse, do not fabricate a form."""
    write_team(workspace / ".specify/teams", "empty-team", items=None, runs=[])
    result = run_generator("--team", "empty-team", cwd=workspace)
    assert result.returncode == 3, result.stdout + result.stderr
    assert not list((workspace / ".specify/project").rglob("project-input.yaml"))


@requires_generator
def test_goal_criteria_alone_do_not_manufacture_a_form(workspace: Path) -> None:
    """FG-12: a goal with verifiable criteria but zero execution material still refuses."""
    write_team(
        workspace / ".specify/teams",
        "criteria-only",
        goal="达成 A;达成 B;达成 C。",
        items=None,
        runs=[],
    )
    assert run_generator("--team", "criteria-only", cwd=workspace).returncode == 3


@requires_generator
def test_generates_a_form_from_a_ledger(workspace: Path) -> None:
    write_team(
        workspace / ".specify/teams",
        "demo",
        items=[item("TI-0001"), item("TI-0002", state="in-progress")],
        runs=["20260730T080000Z-report.md"],
    )
    result = run_generator("--team", "demo", "--json", cwd=workspace)
    assert result.returncode == 0, result.stdout + result.stderr
    form = workspace / ".specify/project/goal/demo/data/project-input.yaml"
    assert form.is_file(), f"form not written; stdout={result.stdout}"


@requires_generator
def test_generation_is_deterministic(workspace: Path) -> None:
    """FG-1: two runs over identical inputs produce byte-identical forms."""
    write_team(
        workspace / ".specify/teams",
        "demo",
        items=[item("TI-0001")],
        runs=["20260730T080000Z-report.md"],
    )
    assert run_generator("--team", "demo", cwd=workspace).returncode == 0
    first = (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_bytes()
    assert run_generator("--team", "demo", cwd=workspace).returncode == 0
    second = (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_bytes()
    assert first == second


@requires_generator
def test_baseline_date_is_supplied_explicitly(workspace: Path) -> None:
    """FG-6 / FR-005: never leave the baseline for the invoked skill to infer."""
    write_team(
        workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[]
    )
    assert run_generator("--team", "demo", cwd=workspace).returncode == 0
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert doc["project"]["baseline_date"], "baseline_date must be populated"
    assert doc["project"]["baseline_date"] == "2026-07-30"


@requires_generator
def test_repos_is_always_empty(workspace: Path) -> None:
    """FG-5: repository derivation stays opt-in and unused by this mechanism."""
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert doc["project"].get("repos") in ([], None)


@requires_generator
def test_coverage_block_is_always_emitted(workspace: Path) -> None:
    """FG-8: absent coverage fails the upstream CG-COVERAGE gate on every WBS report."""
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    coverage = doc.get("coverage")
    assert coverage, "coverage block missing"
    for key in (
        "candidate_total",
        "excluded",
        "granularity_truncated",
        "unattributed",
        "source_label",
    ):
        assert key in coverage, f"coverage.{key} missing"


@requires_generator
def test_all_seven_entities_are_present_or_explicitly_empty(workspace: Path) -> None:
    """FG-7: no entity may be silently omitted."""
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    for entity in (
        "project",
        "people",
        "phases",
        "work_items",
        "milestones",
        "features",
        "sources",
    ):
        assert entity in doc, f"entity `{entity}` absent from the form"


@requires_generator
def test_every_work_item_carries_provenance(workspace: Path) -> None:
    """FG-4 / FR-010: a value without provenance is omitted, never defaulted."""
    write_team(
        workspace / ".specify/teams",
        "demo",
        items=[item("TI-0001"), item("TI-0002")],
        runs=[],
    )
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert doc["work_items"]
    for row in doc["work_items"]:
        assert row.get("source"), f"work item {row} lacks provenance"


@requires_generator
def test_inadmissible_provenance_is_rejected(workspace: Path) -> None:
    """FG-2 / WS-6: run intermediates and runtime logs cannot back a value."""
    write_team(
        workspace / ".specify/teams",
        "demo",
        items=[
            item("TI-0001", provenance=".specify/teams/.work/demo/parallel-result-a.md"),
        ],
        runs=[],
    )
    result = run_generator("--team", "demo", "--json", cwd=workspace)
    if result.returncode == 0:
        doc = yaml.safe_load(
            (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
                encoding="utf-8"
            )
        )
        for row in doc.get("work_items") or []:
            assert not row.get("source", "").startswith(".specify/teams/.work/"), (
                "inadmissible provenance leaked into the form"
            )
    else:
        assert result.returncode == 3


@requires_generator
def test_people_names_come_from_the_agent_definition(workspace: Path) -> None:
    """FR-004: owner_name is the referenced definition's frontmatter `name`."""
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    names = {p.get("owner_name") for p in doc.get("people") or []}
    assert "Team Supervisor" in names, f"expected the agent definition name, got {names}"


@requires_generator
def test_instance_definition_wins_over_template(workspace: Path) -> None:
    (workspace / ".specify/agents/instances/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Instance Supervisor\nrole: team-supervisor\n---\n", encoding="utf-8"
    )
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    names = {p.get("owner_name") for p in doc.get("people") or []}
    assert "Instance Supervisor" in names, names


@requires_generator
def test_milestones_derive_from_goal_success_criteria(workspace: Path) -> None:
    """FR-003: this is what makes the R-tier group constraint satisfiable."""
    write_team(
        workspace / ".specify/teams",
        "demo",
        goal="持续提升质量。成功标准:四项产出齐全;每条改进点附证据路径;对全部仓库零写入。",
        items=[item("TI-0001")],
        runs=[],
    )
    run_generator("--team", "demo", cwd=workspace)
    doc = yaml.safe_load(
        (workspace / ".specify/project/goal/demo/data/project-input.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert doc.get("milestones"), "no milestones derived from the goal criteria"


@requires_generator
def test_explicit_out_path_is_honoured(workspace: Path) -> None:
    write_team(workspace / ".specify/teams", "demo", items=[item("TI-0001")], runs=[])
    out = workspace / "custom/form.yaml"
    assert run_generator("--team", "demo", "--out", str(out), cwd=workspace).returncode == 0
    assert out.is_file()
