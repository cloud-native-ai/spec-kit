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
        "### 2. Goal progress",
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


# ---------------------------------------------------------------------------
# T072 / C-94…C-96 — the goal/team sentences use the new keys; the
# stage chain, the checkpoint parts and the sentinels are unchanged.
# ---------------------------------------------------------------------------

STAGE_CHAIN = (
    "requirements → clarify → plan → tasks → checklist → analyze → implement → review"
)
RETIRED_SCOPE_SYNTAX = ("--scope spec", "--scope global", "scope = spec",
                        "scope: spec", "scope: global")
LEGACY_SPINE_KEYS = ("temp_goal_slug", "temp_team_slug", "temp_scope_spec_dir")


def test_the_goal_team_sentences_use_the_new_keys_and_the_stage_chain_is_unchanged():
    protocol = _text(PROTOCOL)
    skill = _text(SKILL)

    # The goal/team sentences are written in the binding model's vocabulary.
    assert "goal_slug" in protocol, "the goal sentence names the goal by its binding identity"
    assert "`goal_slug`" in skill, "the driver writes the new spine key"

    # The retired scope syntax appears nowhere in the driver's protocol or manual.
    for text, name in ((protocol, "checkpoint-protocol.md"), (skill, "SKILL.md")):
        for retired in RETIRED_SCOPE_SYNTAX:
            assert retired not in text, (
                f"{name} still carries the retired scope syntax {retired!r}")

    # The legacy spine keys survive only as a read-only alias statement, never as a
    # write instruction: the driver's write rule names the new keys.
    assert "origin_spec_dir" in skill, "the new spine key set is complete"
    assert "MUST 只落新键" in skill or "writes the new keys only" in skill, (
        "the driver states the new keys are the only write targets")

    # Preserved: the stage chain and the completion-sentinel authority.
    assert STAGE_CHAIN in skill, "the stage chain literal is unchanged"
    assert "sentinel" in protocol, "the sentinel remains the completion authority"
    assert "### 5. Direction audit" in protocol, (
        "the direction audit stays a mandatory checkpoint part")

    # Preserved: the five parts stay in order and no new part is inserted.
    headings = [line for line in protocol.splitlines() if line.startswith("### ")]
    numbered = headings[:5]
    assert [h.split()[1] for h in numbered] == ["1.", "2.", "3.", "4.", "5."], (
        f"the checkpoint part sequence changed: {numbered}")

    # Decomposition §22 is retitled to the binding model, not the retired scope.
    decomposition = (
        ROOT / "skills/external/sdd-loop-driver/references/decomposition-model.md"
    ).read_text(encoding="utf-8")
    assert "## 22. Team mode (a goal-bound team)" in decomposition
    for retired in RETIRED_SCOPE_SYNTAX:
        assert retired not in decomposition, (
            f"decomposition-model.md still carries the retired scope syntax {retired!r}")
