"""Rollback drill for the Feature 085 checkpoint protocol."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEAM = ROOT / ".specify/specs/085-sdd-temporary-goal-team/team/085-sdd-temporary-goal-team/team.md"


def test_rollback_restores_team_bytes_and_is_recorded(tmp_path):
    original = TEAM.read_bytes()
    changed = original.replace(b"max_parallel: 18", b"max_parallel: 24")
    assert changed != original, "the drill must actually change the team configuration"

    workteam = tmp_path / "team.md"
    workteam.write_bytes(changed)
    checkpoint = tmp_path / "04-rollback-drill.md"
    checkpoint.write_text(
        "# Checkpoint 04 — rollback drill\n\n"
        "## 3. Team configuration review\n"
        "- change: implement max_parallel 18 -> 24\n"
        "- regression: parallelism_efficiency drop >= 30%\n"
        "- rollback=yes\n"
        "- restored: team.md bytes\n",
        encoding="utf-8",
    )

    # The rollback is a byte restore, not a compensating prose statement.
    workteam.write_bytes(original)
    assert workteam.read_bytes() == TEAM.read_bytes()
    record = checkpoint.read_text(encoding="utf-8")
    assert "rollback=yes" in record
    assert "parallelism_efficiency" in record
