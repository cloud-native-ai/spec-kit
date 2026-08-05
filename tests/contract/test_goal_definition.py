"""Structural contract tests for the goal definition file (037-goal-registry, T018).

Contract: .specify/specs/037-goal-registry/contracts/goal-definition.contract.md

Template-only artifacts are governed by structural assertions (Constitution VII), so
this suite pins the file's shape and every rejection the contract's "Validation
outcomes" table declares — including GD-3 (composite objective), which the contract
lists and the engine must therefore enforce.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    REPO_ROOT
    / ".specify/specs/037-goal-registry/contracts/goal-definition.contract.md"
)
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.contract


def _engine():
    spec = importlib.util.spec_from_file_location("goal_utils_contract", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_contract"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _engine()


# --------------------------------------------------------------------------
# The contract document itself
# --------------------------------------------------------------------------

def test_contract_exists():
    assert CONTRACT.is_file(), f"contract missing: {CONTRACT}"


def test_contract_declares_the_three_lifecycle_states_and_no_fourth():
    text = CONTRACT.read_text(encoding="utf-8")
    for state in ("active", "achieved", "abandoned"):
        assert state in text
    assert "`superseded` is not a state" in text or "superseded is not a state" in text


def test_contract_validation_table_covers_every_rejection_rule():
    """A rule that is normative but absent from the table would never be tested."""
    text = CONTRACT.read_text(encoding="utf-8")
    table = text.split("## Validation outcomes", 1)[1]
    for needle in ("grammar", "already exists", "status", "Objective", "Success Criteria",
                   "task list", "more than one objective"):
        assert needle in table, f"Validation outcomes table does not cover: {needle}"


# --------------------------------------------------------------------------
# Structure of a produced definition
# --------------------------------------------------------------------------

@pytest.fixture()
def archived(tmp_path):
    return goal_utils.create_goal(
        tmp_path, "structure-probe", "A desired end state holds.", ["A measurable condition."]
    )


def test_definition_lands_at_the_contracted_path(archived, tmp_path):
    assert archived == tmp_path / ".specify/goal/structure-probe/goal.md"


def test_frontmatter_carries_status_created_updated(archived):
    text = archived.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    head = text.split("---", 2)[1]
    for key in ("status:", "created:", "updated:"):
        assert key in head, f"frontmatter missing {key}"


def test_identity_is_not_duplicated_as_a_frontmatter_field(archived):
    head = archived.read_text(encoding="utf-8").split("---", 2)[1]
    assert "slug:" not in head and "identity:" not in head, (
        "identity is the directory name and MUST NOT be repeated in frontmatter"
    )


@pytest.mark.parametrize("heading", ["## Objective", "## Success Criteria", "## History"])
def test_required_sections_present(archived, heading):
    assert heading in archived.read_text(encoding="utf-8")


def test_no_current_value_or_progress_field_on_criteria(archived):
    """GD-5: criteria are measured by degree; progress is derived, not authored."""
    text = archived.read_text(encoding="utf-8").lower()
    for banned in ("progress:", "current_value", "percent:", "score:"):
        assert banned not in text, f"authored definition must not carry {banned}"


# --------------------------------------------------------------------------
# Every rejection in the contract's table
# --------------------------------------------------------------------------

def test_reject_invalid_identity(tmp_path):
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(tmp_path, "-bad", "An outcome.", [])
    assert "identity" in str(exc.value)


def test_reject_duplicate_identity(tmp_path):
    goal_utils.create_goal(tmp_path, "dupe", "An outcome.", [])
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(tmp_path, "dupe", "Another outcome.", [])
    assert "modify" in str(exc.value).lower()


def test_reject_status_outside_the_three_value_set(tmp_path):
    path = goal_utils.create_goal(tmp_path, "statusy", "An outcome.", [])
    path.write_text(
        path.read_text(encoding="utf-8").replace("status: active", "status: superseded"),
        encoding="utf-8",
    )
    ok, problems = goal_utils.validate_goal(path)
    assert not ok and any("status" in p for p in problems)


def test_reject_empty_objective(tmp_path):
    with pytest.raises(goal_utils.GoalError):
        goal_utils.create_goal(tmp_path, "empty-obj", "   ", [])


def test_reject_task_list_objective(tmp_path):
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(tmp_path, "tasky", "- do this\n- do that", [])
    assert "GD-2" in str(exc.value)


def test_reject_composite_objective(tmp_path):
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(
            tmp_path, "compo", "Green the build as well as rewriting the docs.", []
        )
    assert "GD-3" in str(exc.value)


def test_missing_criteria_section_is_invalid(tmp_path):
    path = tmp_path / ".specify/goal/nosec/goal.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "---\nstatus: active\ncreated: 2026-08-05\nupdated: 2026-08-05\n---\n\n"
        "# Goal: nosec\n\n## Objective\n\nAn outcome.\n\n## History\n\n- x\n",
        encoding="utf-8",
    )
    ok, problems = goal_utils.validate_goal(path)
    assert not ok and any("Success Criteria" in p for p in problems)


def test_empty_criteria_requires_the_explicit_marker(tmp_path):
    path = goal_utils.create_goal(tmp_path, "bare-ok", "An outcome.", [])
    assert "None provided." in path.read_text(encoding="utf-8")
    ok, _ = goal_utils.validate_goal(path)
    assert ok


# --------------------------------------------------------------------------
# Change history
# --------------------------------------------------------------------------

def test_criteria_change_appends_the_prior_value(tmp_path):
    path = goal_utils.create_goal(tmp_path, "hist", "An outcome.", ["first"])
    goal_utils.set_criteria(path, ["second"])
    text = path.read_text(encoding="utf-8")
    assert "prior value" in text and "first" in text


def test_terminal_state_retains_the_file(tmp_path):
    path = goal_utils.create_goal(tmp_path, "endstate", "An outcome.", [])
    goal_utils.set_status(path, "abandoned")
    assert path.is_file()
    assert re.search(r"^status: abandoned$", path.read_text(encoding="utf-8"), re.M)
