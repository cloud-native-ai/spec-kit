"""Contract tests for the summary step's write-set and read-only discipline.

Pins `contracts/summary-writeset.contract.md` rules WS-5 / WS-6 / WS-7 (provenance
admissibility) and the byte-invariance group set that SC-003 declares as the single
source of truth.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify/specs/036-team-summary"
REQUIREMENTS = SPEC_DIR / "requirements.md"
WRITESET_CONTRACT = SPEC_DIR / "contracts/summary-writeset.contract.md"

MAPPING_CANONICAL = REPO_ROOT / "skills/create-team/references/summary-mapping.md"
MAPPING_MIRROR = REPO_ROOT / ".specify/skills/create-team/references/summary-mapping.md"

pytestmark = pytest.mark.contract


# --------------------------------------------------------------------------
# WS-5 / WS-6 / WS-7 — provenance admissibility
# --------------------------------------------------------------------------

INADMISSIBLE_DIR_PREFIXES = (
    ".specify/teams/.work/",
    ".specify/agents/execution/logs/",
)

ADMISSIBLE_EXECUTION_PREFIXES = (
    ".specify/agents/execution/configs/",
    ".specify/agents/execution/scripts/",
)


def is_admissible_provenance(path: str) -> bool:
    """WS-5: provenance must be a repository-relative tracked path.

    WS-6 lists the inadmissible locations exhaustively; WS-7 carves the tracked
    execution-layer subdirectories back in.
    """
    if path.startswith(ADMISSIBLE_EXECUTION_PREFIXES):
        return True
    if path.startswith(INADMISSIBLE_DIR_PREFIXES):
        return False
    if path.startswith("/") or path.startswith("~"):
        return False
    if path.startswith("../"):
        return False
    return True


@pytest.mark.parametrize(
    "path",
    [
        ".specify/teams/demo/team.md",
        ".specify/teams/demo/STATE.md",
        ".specify/teams/demo/run-log.jsonl",
        ".specify/teams/demo/items.jsonl",
        ".specify/teams/demo/runs/20260730T094500Z-report.md",
        ".specify/agents/execution/configs/demo.yaml",
        ".specify/agents/execution/scripts/wrap.sh",
    ],
)
def test_tracked_paths_are_admissible(path: str) -> None:
    assert is_admissible_provenance(path), path


@pytest.mark.parametrize(
    "path",
    [
        ".specify/teams/.work/demo/parallel-result-a.md",
        ".specify/teams/.work/demo/gen-3/optimizer-result.md",
        ".specify/agents/execution/logs/a.live.log",
        ".specify/agents/execution/logs/a.jsonl",
        ".specify/agents/execution/logs/a.status",
        "/tmp/spec-kit-dispatch/a.status",
        "~/scratch/notes.md",
        "../outside/repo.md",
    ],
)
def test_untracked_or_outside_paths_are_inadmissible(path: str) -> None:
    assert not is_admissible_provenance(path), path


def test_inadmissible_locations_are_actually_git_ignored() -> None:
    """The rule set must match reality, not just documentation."""
    for probe in (
        ".specify/teams/.work/demo/progress.md",
        ".specify/agents/execution/logs/demo.live.log",
    ):
        result = subprocess.run(
            ["git", "check-ignore", probe],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"{probe} is expected to be git-ignored"


def test_admissible_locations_are_not_git_ignored() -> None:
    for probe in (
        ".specify/teams/demo/items.jsonl",
        ".specify/goal/demo-goal/summary/summary.md",
        ".specify/agents/execution/configs/demo.yaml",
    ):
        result = subprocess.run(
            ["git", "check-ignore", probe],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 1, f"{probe} must NOT be git-ignored"


# --------------------------------------------------------------------------
# Byte-invariance group set — SC-003 is the single source of truth
# --------------------------------------------------------------------------

EXPECTED_INVARIANCE_GROUPS = {
    ".specify/teams/**",
    "monitored targets",
    "summarize-project",
    ".specify/agents/**",
    ".specify/project/",
}


def test_sc003_enumerates_five_invariance_groups() -> None:
    """SC-003 is declared the single source; other artifacts cite its count."""
    text = REQUIREMENTS.read_text(encoding="utf-8")
    match = re.search(r"^\- \*\*SC-003\*\*: (.+)$", text, re.M)
    assert match, "SC-003 not found in requirements.md"
    sc003 = match.group(1)
    assert "五者" in sc003, f"SC-003 must declare five groups, got: {sc003}"
    for token in (".specify/teams/**", ".specify/agents/**", ".specify/project/"):
        assert token in sc003, f"SC-003 omits invariance group {token}"


def test_writeset_contract_table_matches_sc003_group_count() -> None:
    text = WRITESET_CONTRACT.read_text(encoding="utf-8")
    section = text.split("## Byte-invariance set", 1)[1].split("- **WS-1", 1)[0]
    rows = [
        line
        for line in section.splitlines()
        if line.startswith("|") and not line.startswith("| Group") and "---" not in line
    ]
    assert len(rows) == 5, f"expected 5 invariance groups in the contract, got {len(rows)}"


def test_write_whitelist_is_the_goal_directory_not_the_team_directory() -> None:
    """FR-017 / FR-020: the goal side owns the summary; the team side is read-only.

    This reads requirement 036's frozen contract, which states the pre-migration
    path. That document is history and MUST NOT be rewritten (037 FR-022), so the
    assertion keeps 036's wording — its subject is goal-indexed vs team-indexed,
    which the historical path satisfies just as well. The *live* write-set truth is
    pinned separately by tests/contract/test_goal_writeset.py against
    skills/create-team/references/summary-mapping.md.
    """
    text = WRITESET_CONTRACT.read_text(encoding="utf-8")
    whitelist = text.split("## Write whitelist", 1)[1].split("## Byte-invariance", 1)[0]
    assert "project/goal/" in whitelist
    assert ".specify/memory/feedback/" in whitelist
    assert "teams/<slug>/summary" not in whitelist, (
        "the dropped per-team summary directory must not reappear in the whitelist"
    )


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_provenance_discipline_is_documented(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert "FR-011" in text
    for token in (".specify/teams/.work/", "execution/logs/"):
        assert token in text, f"inadmissible location {token} not documented"
    for token in ("execution/configs/", "execution/scripts/"):
        assert token in text, f"admissible execution path {token} not documented"


def test_annotation_preservation_is_delegated_not_reimplemented() -> None:
    """WS-10 — the invoked skill already preserves `## 附注`."""
    text = MAPPING_CANONICAL.read_text(encoding="utf-8")
    assert "附注" in text
    assert "MUST NOT" in text or "不" in text


# --------------------------------------------------------------------------
# US4 (T060-T064) — write-set enforcement measured against the real generator
# --------------------------------------------------------------------------

import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402

GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"

requires_generator = pytest.mark.skipif(
    not GENERATOR.is_file(), reason="generator not implemented"
)

TEAM_MD = """---
name: ws display
slug: ws
description: write-set fixture
goal: >
  验证写入面纪律。成功标准:写入只落交付目录;团队目录字节不变。
pattern: continuous
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
验证写入面纪律。

## Static Structure
| Role | Stage | Type |
|------|-------|------|
| team-supervisor | optimizer | Meta |

## Dynamic Structure
pattern: continuous
"""


def _fingerprint(root: Path) -> dict[str, str]:
    import hashlib

    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            out[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


@pytest.fixture()
def ws_sandbox(tmp_path: Path) -> Path:
    (tmp_path / ".specify/teams/ws/runs").mkdir(parents=True)
    (tmp_path / ".specify/teams/ws/team.md").write_text(TEAM_MD, encoding="utf-8")
    (tmp_path / ".specify/teams/ws/runs/20260801T090000Z-report.md").write_text(
        "# Team Run Report: ws\n\n- **Outcome**: completed\n", encoding="utf-8"
    )
    (tmp_path / ".specify/teams/ws/items.jsonl").write_text(
        json.dumps(
            {
                "item_id": "TI-0001",
                "title": "条目一",
                "phase_ref": "PH-0001",
                "state": "completed",
                "provenance": ".specify/teams/ws/runs/20260801T090000Z-report.md",
                "ts": "2026-08-01T09:00:00Z",
                "identity": "explicit",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )
    # a pre-existing .specify/project artifact that FR-036 protects
    (tmp_path / ".specify/project").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/project/project.md").write_text("legacy manage-project doc\n", encoding="utf-8")
    return tmp_path


def _generate(sandbox: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--team", "ws", "--repo-root", str(sandbox), *extra],
        capture_output=True, text=True, cwd=str(sandbox),
    )


@requires_generator
def test_team_tree_is_byte_invariant_across_generation(ws_sandbox: Path) -> None:
    """FR-020 / SC-003 group 1 — the team index is a read-only fact source."""
    teams = ws_sandbox / ".specify/teams"
    before = _fingerprint(teams)
    assert _generate(ws_sandbox).returncode == 0
    assert _fingerprint(teams) == before, "the team tree changed during generation"


@requires_generator
def test_preexisting_project_artifacts_are_untouched(ws_sandbox: Path) -> None:
    """FR-036 / SC-003 group 5 — goal/ is additive, never destructive."""
    legacy = ws_sandbox / ".specify/project/project.md"
    before = legacy.read_bytes()
    assert _generate(ws_sandbox).returncode == 0
    assert legacy.read_bytes() == before
    assert legacy.is_file()


@requires_generator
def test_agent_layers_are_byte_invariant(ws_sandbox: Path) -> None:
    """Pre-seeded constraint 4 / WS-3 — a pure derivation step touches no agent layer."""
    agents = ws_sandbox / ".specify/agents"
    before = _fingerprint(agents)
    assert _generate(ws_sandbox).returncode == 0
    assert _fingerprint(agents) == before


@requires_generator
def test_writes_land_only_in_the_goal_delivery_directory(ws_sandbox: Path) -> None:
    """W-1 — the whitelist is the goal directory, nothing else."""
    before = _fingerprint(ws_sandbox)
    assert _generate(ws_sandbox).returncode == 0
    after = _fingerprint(ws_sandbox)
    changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    assert changed, "generation produced no output at all"
    stray = [p for p in changed if not p.startswith(".specify/goal/")]
    assert not stray, f"writes outside the goal delivery directory: {stray}"


@requires_generator
def test_every_emitted_value_carries_resolvable_tracked_provenance(ws_sandbox: Path) -> None:
    """FR-010 / SC-004 — 100% provenance coverage, paths that actually resolve."""
    assert _generate(ws_sandbox).returncode == 0
    import yaml as _yaml

    doc = _yaml.safe_load(
        (ws_sandbox / ".specify/goal/ws/summary/data/project-input.yaml").read_text(encoding="utf-8")
    )
    assert doc["work_items"]
    for row in doc["work_items"]:
        source = row.get("source", "")
        assert source, f"work item without provenance: {row}"
        assert is_admissible_provenance(source), f"inadmissible provenance emitted: {source}"
        assert (ws_sandbox / source.split("#")[0]).exists(), f"provenance does not resolve: {source}"
    for row in doc.get("milestones") or []:
        assert row.get("source"), f"milestone without provenance: {row}"


@requires_generator
def test_items_with_inadmissible_provenance_are_dropped_with_a_declared_gap(ws_sandbox: Path) -> None:
    """WS-8 — degrade to a declared gap, never silently import an untracked value."""
    ledger = ws_sandbox / ".specify/teams/ws/items.jsonl"
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(
            json.dumps(
                {
                    "item_id": "TI-0002",
                    "title": "来自运行中间物的条目",
                    "phase_ref": "PH-0001",
                    "state": "completed",
                    "provenance": ".specify/teams/.work/ws/parallel-result-a.md",
                    "ts": "2026-08-01T10:00:00Z",
                    "identity": "explicit",
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    result = _generate(ws_sandbox, "--json")
    assert result.returncode == 0
    report = json.loads(result.stdout)
    import yaml as _yaml

    doc = _yaml.safe_load(
        (ws_sandbox / ".specify/goal/ws/summary/data/project-input.yaml").read_text(encoding="utf-8")
    )
    ids = [w["item_id"] for w in doc["work_items"]]
    assert "ws.TI-0002" not in ids, "an item backed only by run intermediates was imported"
    assert any("TI-0002" in gap for gap in report["material_gaps"]), report["material_gaps"]


@requires_generator
def test_reader_sections_carry_no_internal_identifiers(ws_sandbox: Path) -> None:
    """WS-14 / FR-022 — attribution by team slug is fine; internals are not."""
    assert _generate(ws_sandbox).returncode == 0
    text = (ws_sandbox / ".specify/goal/ws/summary/data/project-input.yaml").read_text(encoding="utf-8")
    for forbidden in (".work/", "parallel-result-", ".live.log", ".status", "execution/logs/"):
        assert forbidden not in text, f"internal identifier {forbidden!r} leaked into the form"


@requires_generator
def test_intake_does_not_double_when_run_count_doubles(ws_sandbox: Path) -> None:
    """SC-005 / FR-009 — consumption must not grow linearly with run count."""
    runs_dir = ws_sandbox / ".specify/teams/ws/runs"
    ledger = ws_sandbox / ".specify/teams/ws/items.jsonl"

    def form_size(k: int) -> int:
        for i in range(2, k + 2):
            (runs_dir / f"2026080{i % 9 + 1}T09{i:02d}00Z-report.md").write_text(
                "# Team Run Report: ws\n\n- **Outcome**: completed\n", encoding="utf-8"
            )
            with ledger.open("a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps(
                        {
                            "item_id": "TI-0001",
                            "title": "条目一",
                            "phase_ref": "PH-0001",
                            "state": "completed",
                            "provenance": ".specify/teams/ws/runs/20260801T090000Z-report.md",
                            "ts": f"2026-08-0{i % 9 + 1}T09:00:00Z",
                            "identity": "explicit",
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        assert _generate(ws_sandbox).returncode == 0
        return len(
            (ws_sandbox / ".specify/goal/ws/summary/data/project-input.yaml").read_text(
                encoding="utf-8"
            )
        )

    at_k = form_size(3)
    at_2k = form_size(6)
    assert at_2k < at_k * 2, (
        f"intake proxy doubled with run count: {at_k} -> {at_2k}; the fold must collapse "
        "repeated events per item rather than accumulate them"
    )


# --------------------------------------------------------------------------
# T063 / T069 / T070 — the prompt-layer rules that no script can enforce
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_only_the_supervisor_writes_tracked_artifacts(path: Path) -> None:
    """FR-021 / WS-4 — sub-agents never write tracked team or summary artifacts."""
    text = path.read_text(encoding="utf-8")
    assert "FR-021" in text
    assert re.search(r"子代理 MUST NOT 写入", text), (
        "the sub-agent write prohibition is not stated"
    )


@pytest.mark.parametrize(
    "path", [MAPPING_CANONICAL, MAPPING_MIRROR], ids=["canonical", "mirror"]
)
def test_invariance_scoping_distinguishes_summary_step_from_cycle_writes(path: Path) -> None:
    """WS-1 — without this distinction FR-020 reads as 'a team may never write STATE.md'."""
    text = path.read_text(encoding="utf-8")
    assert "FR-020" in text
    assert "SUMMARIZE" in text and "cycle" in text.lower(), (
        "the summary-step vs normal-cycle-write boundary is not documented"
    )
    assert re.search(r"状态行.*正常 cycle 写入|正常 cycle 写入.*状态行", text, re.S), (
        "the run-report status-line write is not carved out of the invariance rule"
    )


def test_state_md_id_cross_reference_convention_is_documented() -> None:
    """FR-026 — STATE.md entries carry the item id inline for human cross-reference."""
    text = MAPPING_CANONICAL.read_text(encoding="utf-8")
    assert "[TI-nnnn]" in text, "the STATE.md inline id convention is not documented"
