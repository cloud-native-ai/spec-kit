"""Contract guards for the Feature 085 checkpoint protocol."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "skills/external/sdd-loop-driver/references/checkpoint-protocol.md"
SKILL = ROOT / "skills/external/sdd-loop-driver/SKILL.md"
TEAM = ROOT / ".specify/specs/085-sdd-temporary-goal-team/team/085-sdd-temporary-goal-team/team.md"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def test_protocol_has_the_four_parts():
    text = _text(PROTOCOL)
    for part in (
        "### 1. Artifact verification",
        "### 2. Temporary Goal progress",
        "### 3. Team configuration review",
        "### 4. Concurrency and roster decision",
    ):
        assert part in text, f"checkpoint part missing: {part}"


def test_protocol_names_the_checkpoint_path_and_closure():
    text = _text(PROTOCOL)
    assert "checkpoints/<NN>-<stage>.md" in text
    assert "closure.md" in text


def test_protocol_caps_configuration_changes_and_defines_rollback():
    text = _text(PROTOCOL)
    assert "At most one configuration/concurrency/roster change" in text
    for trigger in ("U4 fails", "retries_package", "parallelism_efficiency", "30 percent"):
        assert trigger in text, f"rollback trigger missing: {trigger}"


def test_driver_skill_points_at_the_protocol_owner():
    text = _text(SKILL)
    assert "references/checkpoint-protocol.md" in text
    assert "Checkpoint 协议（085）" in text


def test_temporary_team_declares_the_one_change_policy():
    text = _text(TEAM)
    assert "max_config_changes: 1" in text
    assert "checkpoint_policy:" in text
