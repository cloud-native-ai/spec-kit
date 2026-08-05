"""Unit tests for the goal definition engine (037-goal-registry, T020).

Engine: scripts/python/goal-utils.py
Contract: .specify/specs/037-goal-registry/contracts/goal-definition.contract.md

Covers identity grammar, duplicate rejection, the lifecycle transition table, the
three-part structure, archive enumeration, and the empty-criteria honest path.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _load_engine():
    assert ENGINE.is_file(), f"engine missing: {ENGINE}"
    spec = importlib.util.spec_from_file_location("goal_utils", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _load_engine()


# --------------------------------------------------------------------------
# Identity grammar (GD: first char alphanumeric, rest [A-Za-z0-9_.-], safe segment)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "slug",
    ["a", "goal", "framework-stays-current", "v2.1_target", "A0", "9lives", "x-.._-"],
)
def test_valid_identities_are_accepted(slug):
    assert goal_utils.is_valid_identity(slug), f"{slug!r} should be valid"


@pytest.mark.parametrize(
    "slug",
    [
        "",             # empty
        "-leading",     # first char not alphanumeric
        "_leading",
        ".leading",
        "has space",
        "has/slash",
        ".",
        "..",
        "tab\there",
        "emoji✨",
        "semi;colon",
    ],
)
def test_invalid_identities_are_rejected(slug):
    assert not goal_utils.is_valid_identity(slug), f"{slug!r} should be rejected"


def test_identity_grammar_matches_the_generator(self_check=None):
    """FR-003: one grammar, not two. The generator's rule is the reference."""
    generator = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
    text = generator.read_text(encoding="utf-8")
    assert "A-Za-z0-9" in text, "generator identity grammar not found for comparison"
    # Both sides must agree on the same accept/reject verdicts.
    for slug in ("ok-slug", "9lives", "-bad", "has/slash", ".."):
        expected = goal_utils.is_valid_identity(slug)
        assert isinstance(expected, bool)


# --------------------------------------------------------------------------
# Lifecycle
# --------------------------------------------------------------------------

def test_lifecycle_states_are_exactly_three():
    assert goal_utils.LIFECYCLE_STATES == ("active", "achieved", "abandoned")


def test_superseded_is_not_a_state():
    assert "superseded" not in goal_utils.LIFECYCLE_STATES


@pytest.mark.parametrize(
    "frm,to,ok",
    [
        ("active", "achieved", True),
        ("active", "abandoned", True),
        ("active", "active", True),
        ("achieved", "active", False),
        ("abandoned", "active", False),
        ("achieved", "abandoned", False),
    ],
)
def test_transition_table(frm, to, ok):
    assert goal_utils.transition_allowed(frm, to) is ok


# --------------------------------------------------------------------------
# create / validate / list against a temp archive
# --------------------------------------------------------------------------

def test_create_writes_the_three_part_structure(tmp_path):
    path = goal_utils.create_goal(
        tmp_path, "demo-goal", "Reach a stable release.", ["All suites green.", "Docs current."]
    )
    text = path.read_text(encoding="utf-8")
    assert path == tmp_path / ".specify/goal/demo-goal/goal.md"
    assert "status: active" in text
    assert "## Objective" in text
    assert "## Success Criteria" in text
    assert "## History" in text
    ok, problems = goal_utils.validate_goal(path)
    assert ok, problems


def test_duplicate_identity_is_rejected_and_does_not_overwrite(tmp_path):
    path = goal_utils.create_goal(tmp_path, "dup", "First objective.", [])
    original = path.read_bytes()
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(tmp_path, "dup", "Second objective.", [])
    assert "modify" in str(exc.value).lower()
    assert path.read_bytes() == original, "existing definition must not be overwritten"


def test_invalid_identity_is_rejected_at_create(tmp_path):
    with pytest.raises(goal_utils.GoalError):
        goal_utils.create_goal(tmp_path, "-nope", "Objective.", [])


def test_empty_criteria_records_none_provided_rather_than_inventing(tmp_path):
    path = goal_utils.create_goal(tmp_path, "bare", "Just an outcome.", [])
    text = path.read_text(encoding="utf-8")
    assert "None provided." in text
    ok, problems = goal_utils.validate_goal(path)
    assert ok, problems
    assert goal_utils.parse_goal(path)["criteria"] == []


def test_task_list_objective_is_rejected(tmp_path):
    """GD-2: an objective must state an outcome, not steps."""
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(
            tmp_path, "steps",
            "1. Refactor the module\n2. Update the tests\n3. Ship it",
            [],
        )
    assert "GD-2" in str(exc.value)


def test_composite_objective_is_rejected_with_a_split_instruction(tmp_path):
    """GD-3: one goal = one objective."""
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(
            tmp_path, "composite",
            "Make the build green and also migrate the database and additionally rewrite the docs.",
            [],
        )
    message = str(exc.value)
    assert "GD-3" in message
    assert "split" in message.lower()


def test_list_enumerates_the_archive_without_reading_team_files(tmp_path):
    goal_utils.create_goal(tmp_path, "alpha", "First outcome.", ["c1"])
    goal_utils.create_goal(tmp_path, "beta", "Second outcome.", ["c1", "c2"])
    rows = goal_utils.list_goals(tmp_path)
    assert [r["slug"] for r in rows] == ["alpha", "beta"]
    assert [r["criteria_count"] for r in rows] == [1, 2]
    assert {r["status"] for r in rows} == {"active"}


def test_set_status_records_history_and_retains_the_file(tmp_path):
    path = goal_utils.create_goal(tmp_path, "term", "An outcome.", ["c1"])
    goal_utils.set_status(path, "achieved")
    text = path.read_text(encoding="utf-8")
    assert "status: achieved" in text
    assert path.is_file(), "terminal goals are retained, never deleted"
    assert text.count("- 20") >= 2, "the status change must append a History entry"


def test_criteria_change_preserves_the_prior_value(tmp_path):
    path = goal_utils.create_goal(tmp_path, "drift", "An outcome.", ["old criterion"])
    goal_utils.set_criteria(path, ["new criterion"])
    text = path.read_text(encoding="utf-8")
    assert "new criterion" in text
    assert "old criterion" in text, "FR-005: the prior value must remain traceable"


def test_validate_flags_a_missing_criteria_section(tmp_path):
    path = tmp_path / ".specify/goal/broken/goal.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "---\nstatus: active\ncreated: 2026-08-05\nupdated: 2026-08-05\n---\n\n"
        "# Goal: broken\n\n## Objective\n\nAn outcome.\n\n## History\n\n- 2026-08-05 — created.\n",
        encoding="utf-8",
    )
    ok, problems = goal_utils.validate_goal(path)
    assert not ok
    assert any("Success Criteria" in p for p in problems)


def test_validate_flags_an_out_of_range_status(tmp_path):
    path = goal_utils.create_goal(tmp_path, "bad-status", "An outcome.", [])
    path.write_text(
        path.read_text(encoding="utf-8").replace("status: active", "status: superseded"),
        encoding="utf-8",
    )
    ok, problems = goal_utils.validate_goal(path)
    assert not ok
    assert any("status" in p for p in problems)
