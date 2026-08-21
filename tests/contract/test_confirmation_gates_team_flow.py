"""Structural contract tests for the zero-confirmation team flow.

Contract: .specify/specs/044-reduce-confirmation-flows/contracts/team-flow-contract.md
Asserts the SOURCE surfaces (templates/commands/team.md + skills/create-team/);
per-tool copies are covered separately by regen-command-copies --check.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
SKILL = REPO_ROOT / "skills" / "create-team" / "SKILL.md"
CREATE_MODE = REPO_ROOT / "skills" / "create-team" / "references" / "create-mode.md"
EXEC_GUIDE = REPO_ROOT / "skills" / "create-team" / "references" / "execution-guide.md"

BLOCKING_PHRASES = (
    "MUST NOT execute before confirmation",
    "preview → confirm → execute",
    "Confirmation gate",
    "after user confirmation",
    "等待用户确认",
    "Confirm and persist",
    "确认门禁",
    "合并确认",
    "interactive confirmation",
)


def read(path: Path) -> str:
    assert path.is_file(), f"missing source surface: {path}"
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("phrase", BLOCKING_PHRASES)
def test_team_command_has_no_blocking_gate(phrase: str) -> None:
    text = read(TEAM_CMD)
    assert phrase not in text, f"blocking gate phrase survived in team.md: {phrase!r}"


@pytest.mark.parametrize("phrase", BLOCKING_PHRASES)
def test_create_team_skill_has_no_blocking_gate(phrase: str) -> None:
    for path in (SKILL, CREATE_MODE, EXEC_GUIDE):
        text = read(path)
        assert phrase not in text, f"blocking gate phrase survived in {path.name}: {phrase!r}"


def test_team_command_direct_persist_and_report() -> None:
    text = read(TEAM_CMD)
    assert "直接落盘" in text or "Persist directly" in text
    assert "confirmation-gates.md" in text, "single-line taxonomy reference missing"
    assert "执行报告" in text or "execution report" in text.lower()
    assert "modify" in text and ("improve-team" in text), "modification path missing"


def test_run_mode_preview_execute_shape() -> None:
    text = read(TEAM_CMD)
    assert "preview → execute" in text
    assert "continuous" in text and "分级门控" in text, "continuous exception clause missing"


def test_wrapup_submission_prompt_nonblocking() -> None:
    text = read(SKILL)
    assert "非阻塞" in text, "wrap-up submission prompt must be non-blocking"
    assert "/speckit.feedback package" in text, "user-facing submission path must be disclosed"
    assert "自动传输" in text and "MUST NOT" in text, "no-auto-transmission red line missing"


def test_continuous_tiered_gates_untouched() -> None:
    ops = REPO_ROOT / "skills" / "create-team" / "references" / "operating-loops.md"
    ws = REPO_ROOT / "skills" / "create-team" / "templates" / "teams" / "project-cluster.md"
    for path in (ops, ws):
        text = read(path)
        assert "confirm" in text.lower() or "确认" in text, (
            f"continuous-loop tiered gates must be preserved in {path.name}"
        )
