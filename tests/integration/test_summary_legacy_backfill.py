"""Integration: legacy backfill and honest degradation (US5).

Covers FR-023 / FR-025 / FR-027 and SC-009. The failure mode this guards against is
fabrication: a team with thin material must produce an honest, gap-declaring summary
rather than an invented schedule.
"""

from __future__ import annotations

import hashlib
import json
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


def team_md(slug: str, *, pattern: str = "iteration", goal: str | None = None) -> str:
    goal = goal or "迭代优化技能定义。成功标准:加权评分达标;报告可溯源。"
    return f"""---
name: {slug} display
slug: {slug}
description: legacy fixture
goal: >
  {goal}
pattern: {pattern}
created: 2026-07-01
updated: 2026-07-30
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    lifecycle: persistent
config:
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
"""


CONTRACT_REPORT = """# Team Run Report: {slug} display

- **Team**: {slug}
- **Goal**: legacy goal
- **Started**: 2026-07-{day}T08:00:00Z  **Finished**: 2026-07-{day}T09:00:00Z
- **Pattern**: iteration
- **Outcome**: {outcome}

## Result Summary
generation {gen} summary.

## Deliverables
| Artifact | Target path |
|----------|-------------|
| {deliverable} | docs/out-{gen}.md |

## Execution Detail
detail.
"""

# The shape continuous teams actually write — no Started/Finished/Outcome at all
CYCLE_REPORT = """# Cycle Report — {slug}

- **Cycle**: {gen}
- **UTC**: 2026-07-{day}T08:20:21Z
- **Maturity**: L1（报告态）

## Goal 对齐
cycle {gen} alignment.
"""


@pytest.fixture()
def legacy(tmp_path: Path) -> Path:
    """A team with ONLY team.md + runs/ — no ledger, no STATE.md, no run-log."""
    (tmp_path / ".specify/teams/legacy/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/legacy/team.md").write_text(team_md("legacy"), encoding="utf-8")
    for gen, day, outcome, deliverable in (
        (1, "10", "max-reached", "第一代变体产物"),
        (2, "20", "converged", "第二代采纳改进"),
    ):
        (tmp_path / f".specify/teams/legacy/runs/202607{day}T080000Z-report.md").write_text(
            CONTRACT_REPORT.format(slug="legacy", day=day, outcome=outcome, gen=gen,
                                   deliverable=deliverable),
            encoding="utf-8",
        )
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )
    return tmp_path


def generate(root: Path, slug: str = "legacy", *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--team", slug, "--repo-root", str(root), "--json", *extra],
        capture_output=True, text=True, cwd=str(root),
    )


def form_of(root: Path, goal: str = "legacy") -> dict:
    return yaml.safe_load(
        (root / f".specify/project/goal/{goal}/data/project-input.yaml").read_text(encoding="utf-8")
    )


# --------------------------------------------------------------------------
# FR-025 — no team rebuild, no history rewriting
# --------------------------------------------------------------------------


@requires_generator
def test_team_with_only_runs_still_produces_a_summary(legacy: Path) -> None:
    result = generate(legacy)
    assert result.returncode == 0, result.stdout + result.stderr
    doc = form_of(legacy)
    assert doc["work_items"], "no work items backfilled from runs/"
    assert doc["phases"], "no phases backfilled from runs/"


@requires_generator
def test_backfill_does_not_modify_the_team_directory(legacy: Path) -> None:
    """History is read, never rewritten into a new format."""
    team_dir = legacy / ".specify/teams/legacy"
    before = {
        str(p.relative_to(team_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(team_dir.rglob("*")) if p.is_file()
    }
    assert generate(legacy).returncode == 0
    after = {
        str(p.relative_to(team_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(team_dir.rglob("*")) if p.is_file()
    }
    assert before == after
    assert not (team_dir / "items.jsonl").exists(), "backfill must not synthesize a ledger"


@requires_generator
def test_each_run_becomes_its_own_phase(legacy: Path) -> None:
    assert generate(legacy).returncode == 0
    doc = form_of(legacy)
    assert len(doc["phases"]) == 2, f"expected one phase per run, got {doc['phases']}"
    for phase in doc["phases"]:
        assert phase["phase_id"].startswith("legacy.")


# --------------------------------------------------------------------------
# FR-027 — inferred identity is derived and MARKED, never presented as precise
# --------------------------------------------------------------------------


@requires_generator
def test_backfilled_items_use_hashed_inferred_identities(legacy: Path) -> None:
    assert generate(legacy).returncode == 0
    doc = form_of(legacy)
    import re

    for row in doc["work_items"]:
        local = row["item_id"].split(".", 1)[1]
        assert re.match(r"^TIX-[0-9a-f]{8}$", local), (
            f"backfilled id {row['item_id']} is not a hashed inferred identity"
        )


@requires_generator
def test_inferred_identities_are_marked_as_inferred(legacy: Path) -> None:
    result = generate(legacy)
    assert result.returncode == 0
    report = json.loads(result.stdout)
    marked = [f for f in report["inferred_fields"] if "item_id" in f["field"]]
    assert marked, f"no inferred-identity markings recorded: {report['inferred_fields']}"
    for entry in marked:
        assert entry["inferred_from"], "an inferred field carries no basis"


@requires_generator
def test_inferred_identity_is_deterministic_for_the_same_title_and_phase(legacy: Path) -> None:
    assert generate(legacy).returncode == 0
    first = [w["item_id"] for w in form_of(legacy)["work_items"]]
    assert generate(legacy).returncode == 0
    assert [w["item_id"] for w in form_of(legacy)["work_items"]] == first


@requires_generator
def test_rename_during_the_inferred_era_surfaces_as_a_gap_not_a_silent_drop(legacy: Path) -> None:
    """FR-027 — a retitled item cannot be recognised, so it must be declared."""
    assert generate(legacy).returncode == 0
    before_ids = {w["item_id"] for w in form_of(legacy)["work_items"]}

    report = legacy / ".specify/teams/legacy/runs/20260710T080000Z-report.md"
    report.write_text(
        report.read_text(encoding="utf-8").replace("第一代变体产物", "重命名后的产物"),
        encoding="utf-8",
    )
    result = generate(legacy)
    assert result.returncode == 0
    after_ids = {w["item_id"] for w in form_of(legacy)["work_items"]}
    assert before_ids != after_ids, "a retitled inferred item should hash differently"
    assert len(after_ids) == len(before_ids), "the rename must not duplicate the item"


# --------------------------------------------------------------------------
# FR-023 / SC-009 — degrade honestly, fabricate nothing
# --------------------------------------------------------------------------


@requires_generator
def test_no_fabricated_dates_or_durations_or_percentages(legacy: Path) -> None:
    assert generate(legacy).returncode == 0
    doc = form_of(legacy)
    for row in doc["work_items"]:
        for forbidden in ("planned_start", "planned_end", "duration_days", "progress_pct"):
            assert forbidden not in row, (
                f"fabricated {forbidden} on a backfilled item with no scheduling material: {row}"
            )


@requires_generator
def test_thin_material_is_declared_as_a_gap(legacy: Path) -> None:
    result = generate(legacy)
    assert result.returncode == 0
    gaps = json.loads(result.stdout)["material_gaps"]
    assert any("ledger" in g or "台账" in g for g in gaps), (
        f"the absent-ledger limitation was not declared: {gaps}"
    )


@requires_generator
def test_non_contract_report_shape_is_reported_not_guessed(tmp_path: Path) -> None:
    """The continuous 'Cycle Report' shape lacks Outcome — state must stay unknown."""
    (tmp_path / ".specify/teams/cyc/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/cyc/team.md").write_text(
        team_md("cyc", pattern="continuous"), encoding="utf-8"
    )
    (tmp_path / ".specify/teams/cyc/runs/20260730T082021Z-report.md").write_text(
        CYCLE_REPORT.format(slug="cyc", gen=1, day="30"), encoding="utf-8"
    )
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )
    result = generate(tmp_path, "cyc")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = form_of(tmp_path, "cyc")
    assert all(not w.get("status") for w in doc["work_items"]), (
        "a report without an Outcome field must not be guessed as completed"
    )
    gaps = json.loads(result.stdout)["material_gaps"]
    assert any("Report contract" in g for g in gaps), gaps
    # the mandated filename timestamp still yields a baseline date
    assert doc["project"]["baseline_date"] == "2026-07-30"


@requires_generator
def test_material_free_team_is_declined(tmp_path: Path) -> None:
    (tmp_path / ".specify/teams/bare/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/bare/team.md").write_text(team_md("bare"), encoding="utf-8")
    result = generate(tmp_path, "bare")
    assert result.returncode == 3, result.stdout + result.stderr
    assert "declined(no-material)" in result.stdout


@requires_generator
def test_excluded_variants_are_not_counted_as_delayed(tmp_path: Path) -> None:
    """US5 scenario 5 — an eliminated iteration variant enters the excluded bucket."""
    (tmp_path / ".specify/teams/exc/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/exc/team.md").write_text(team_md("exc"), encoding="utf-8")
    (tmp_path / ".specify/teams/exc/runs/20260710T080000Z-report.md").write_text(
        CONTRACT_REPORT.format(slug="exc", day="10", outcome="converged", gen=1, deliverable="产物"),
        encoding="utf-8",
    )
    (tmp_path / ".specify/teams/exc/items.jsonl").write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False)
            for r in (
                {"item_id": "TI-0001", "title": "被采纳变体", "phase_ref": "PH-0001",
                 "state": "completed", "provenance": ".specify/teams/exc/runs/20260710T080000Z-report.md",
                 "ts": "2026-07-10T09:00:00Z", "identity": "explicit"},
                {"item_id": "TI-0002", "title": "被淘汰变体", "phase_ref": "PH-0001",
                 "state": "unknown", "provenance": ".specify/teams/exc/runs/20260710T080000Z-report.md",
                 "ts": "2026-07-10T09:00:00Z", "identity": "explicit",
                 "excluded_reason": "锦标赛中被淘汰"},
            )
        ) + "\n",
        encoding="utf-8",
    )
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )
    assert generate(tmp_path, "exc").returncode == 0
    doc = form_of(tmp_path, "exc")
    assert doc["coverage"]["excluded"] == 1, doc["coverage"]
    excluded = [w for w in doc["work_items"] if "excluded:" in str(w.get("progress_source", ""))]
    assert len(excluded) == 1
    assert excluded[0]["status"] == "", "an excluded variant must not be scored as delayed"


@requires_generator
def test_backfilled_form_still_passes_the_upstream_validator(legacy: Path) -> None:
    assert generate(legacy).returncode == 0
    form = legacy / ".specify/project/goal/legacy/data/project-input.yaml"
    val = subprocess.run(
        [sys.executable, str(SUMMARIZE / "validate-project-input.py"), "--input", str(form), "--json"],
        capture_output=True, text=True, cwd=str(legacy),
    )
    assert val.returncode == 0, val.stdout + val.stderr
    assert json.loads(val.stdout)["status"] == "ready"


@requires_generator
def test_maturity_promotion_does_not_retroactively_rewrite_earlier_states(tmp_path: Path) -> None:
    """LC-10 — report-only-era items stay as recorded after an L1 -> L2 promotion.

    The property holds because the ledger is append-only (IL-1) and each event
    carries the maturity in force when it happened; a later promotion appends, it
    never mutates. This asserts that the generator honours that rather than
    re-deriving state from the team's *current* maturity.
    """
    (tmp_path / ".specify/teams/mat/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/mat/team.md").write_text(
        team_md("mat", pattern="continuous"), encoding="utf-8"
    )
    (tmp_path / ".specify/teams/mat/runs/20260710T080000Z-report.md").write_text(
        CONTRACT_REPORT.format(slug="mat", day="10", outcome="completed", gen=1, deliverable="产物"),
        encoding="utf-8",
    )
    ledger = tmp_path / ".specify/teams/mat/items.jsonl"
    ledger.write_text(
        json.dumps(
            {
                "item_id": "TI-0001",
                "title": "L1 期间只观测未行动的条目",
                "phase_ref": "PH-0001",
                "state": "unknown",
                "provenance": ".specify/teams/mat/runs/20260710T080000Z-report.md",
                "ts": "2026-07-10T09:00:00Z",
                "identity": "explicit",
                "maturity_at_event": "L1",
            },
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )

    assert generate(tmp_path, "mat").returncode == 0
    before = form_of(tmp_path, "mat")["work_items"][0]
    assert before["status"] == "", "an L1 report-only item must not be scored as actioned"

    # promote the team to L2 — the historical event must be unaffected
    team_file = tmp_path / ".specify/teams/mat/team.md"
    team_file.write_text(
        team_file.read_text(encoding="utf-8").replace("maturity: L1", "maturity: L2"),
        encoding="utf-8",
    )
    assert generate(tmp_path, "mat").returncode == 0
    after = form_of(tmp_path, "mat")["work_items"][0]
    assert after == before, (
        "a maturity promotion retroactively changed a report-only-era item"
    )
