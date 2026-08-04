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
        ".specify/project/goal/demo-goal/summary.md",
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
    """FR-017 / FR-020: the goal side owns the summary; the team side is read-only."""
    text = WRITESET_CONTRACT.read_text(encoding="utf-8")
    whitelist = text.split("## Write whitelist", 1)[1].split("## Byte-invariance", 1)[0]
    assert ".specify/project/goal/" in whitelist
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
