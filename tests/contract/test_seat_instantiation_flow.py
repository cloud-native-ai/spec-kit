"""Contract test: seat-instantiation + modify-backfill wiring
(contracts/seat-instantiation.md C-4..C-9, contracts/modify-backfill.md C-1..C-3, C-8).

The create-team flow must instantiate stage-frame seats via create-agent
delegation (placeholders resolved, team-scope set) and directly execute the
render trigger; improve-team's modify flow must backfill missing seats opt-in.
Assertions are marker-based (machine-checkable), prose-agnostic.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

CREATE_TEAM_SKILL = REPO_ROOT / "skills" / "create-team" / "SKILL.md"
CREATE_MODE = REPO_ROOT / "skills" / "create-team" / "references" / "create-mode.md"
IMPROVE_TEAM_SKILL = REPO_ROOT / "skills" / "improve-team" / "SKILL.md"

GUIDANCE = "存量团队经一次 modify 即可让席位上注册面"


def test_c4_create_team_create_flow_instantiates_seats():
    text = CREATE_TEAM_SKILL.read_text(encoding="utf-8")
    assert "seat instantiation" in text
    assert "create-agent" in text


def test_c8_create_team_create_flow_runs_render_trigger():
    text = CREATE_TEAM_SKILL.read_text(encoding="utf-8")
    assert "specify render-agents" in text


def test_c8_render_failure_disclosed():
    text = CREATE_TEAM_SKILL.read_text(encoding="utf-8")
    assert "不得静默跳过" in text


def test_c9_create_mode_schema_note_two_member_forms():
    text = CREATE_MODE.read_text(encoding="utf-8")
    assert "team-scope" in text
    assert "seat instantiated by this flow" in text


def test_mb_c1_c2_improve_team_backfills_and_renders():
    text = IMPROVE_TEAM_SKILL.read_text(encoding="utf-8")
    assert "specify render-agents" in text
    assert "回填" in text


def test_mb_c8_guidance_line_in_both_skills():
    assert GUIDANCE in CREATE_TEAM_SKILL.read_text(encoding="utf-8")
    assert GUIDANCE in IMPROVE_TEAM_SKILL.read_text(encoding="utf-8")
