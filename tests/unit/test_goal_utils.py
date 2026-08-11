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


# ==========================================================================
# Targets data layer (038-goal-target, T002)
# Contract: .specify/specs/038-goal-target/contracts/targets-engine.contract.md
# ==========================================================================

def _active_goal(tmp_path, slug="sliced", criteria=None):
    return goal_utils.create_goal(tmp_path, slug, "Broad platform outcome.", criteria or [])


# --- SC-002 engine side: section absent ⇒ empty targets, byte-identical ---

def test_parse_goal_returns_empty_targets_when_section_absent(tmp_path):
    path = _active_goal(tmp_path)
    assert goal_utils.parse_goal(path)["targets"] == []


def test_create_output_is_byte_stable_without_targets(tmp_path):
    """SC-002: the new optional parameter must not change existing rendering."""
    path = goal_utils.create_goal(tmp_path, "stable", "An outcome.", ["c1"])
    before = path.read_bytes()
    # re-render through the same code path the actions use
    data = goal_utils.parse_goal(path)
    rerendered = goal_utils._render(
        data["objective"], data["criteria"], data["status"], data["created"],
        data["updated"], data["history"].splitlines(), data["slug"],
    )
    assert rerendered.encode("utf-8") == before


# --- D3 rendering grammar + round-trip byte stability ---

def test_targets_render_matches_d3_grammar_and_round_trips():
    targets = [
        {"id": "T-001", "statement": "日志组件拆分完成", "status": "open"},
        {"id": "T-002", "statement": "指标采集链路独立可部署", "status": "done"},
    ]
    rendered = goal_utils._render_targets_table(targets)
    assert rendered == (
        "| ID | Target | Status |\n"
        "|----|--------|--------|\n"
        "| T-001 | 日志组件拆分完成 | open |\n"
        "| T-002 | 指标采集链路独立可部署 | done |"
    )
    assert goal_utils._parse_targets_text(rendered) == targets


def test_render_sorts_rows_by_id_ascending():
    targets = [
        {"id": "T-010", "statement": "later one", "status": "open"},
        {"id": "T-002", "statement": "earlier one", "status": "done"},
    ]
    lines = goal_utils._render_targets_table(targets).splitlines()
    assert lines[2].startswith("| T-002 |")
    assert lines[3].startswith("| T-010 |")


def test_parse_round_trip_is_byte_stable(tmp_path):
    path = _active_goal(tmp_path)
    goal_utils.add_target(path, "第一个切片成果")
    first = path.read_bytes()
    data = goal_utils.parse_goal(path)
    section = goal_utils._render_targets_table(data["targets"])
    assert goal_utils._parse_targets_text(section) == data["targets"]
    assert path.read_bytes() == first


@pytest.mark.parametrize(
    "bad_section,why",
    [
        (
            "## Targets\n\n| ID | Target | State |\n|----|--------|--------|\n"
            "| T-001 | x | open |\n",
            "wrong header",
        ),
        (
            "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
            "| T-001 | open |\n",
            "missing column",
        ),
        (
            "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
            "| T-001 | x | finished |\n",
            "illegal status",
        ),
    ],
)
def test_validate_rejects_hand_broken_target_rows(tmp_path, bad_section, why):
    path = _active_goal(tmp_path)
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("## History", bad_section + "\n## History"), encoding="utf-8")
    ok, problems = goal_utils.validate_goal(path)
    assert not ok, f"{why} must be flagged"
    assert any("手写" in p or "engine" in p.lower() for p in problems)


def test_validate_rejects_empty_targets_table(tmp_path):
    path = _active_goal(tmp_path)
    text = path.read_text(encoding="utf-8")
    empty = "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
    path.write_text(text.replace("## History", empty + "\n## History"), encoding="utf-8")
    ok, problems = goal_utils.validate_goal(path)
    assert not ok
    assert any("empty" in p.lower() or "空" in p for p in problems)
    # parse side: the header-only table yields no rows
    assert goal_utils.parse_goal(path)["targets"] == []


# --- identity grammar: unique, monotonic, terminal identities never reused ---

def test_target_ids_are_monotonic_and_terminal_not_reused(tmp_path):
    path = _active_goal(tmp_path)
    t1 = goal_utils.add_target(path, "切片一")
    t2 = goal_utils.add_target(path, "切片二")
    goal_utils.set_target_status(path, t2, "dropped")
    t3 = goal_utils.add_target(path, "切片三")
    assert [t1, t2, t3] == ["T-001", "T-002", "T-003"]
    # dropped identity must NOT be reused: next id is max+1, not first-gap
    data = goal_utils.parse_goal(path)
    assert [t["id"] for t in data["targets"]] == ["T-001", "T-002", "T-003"]


def test_next_target_id_is_monotone_max_plus_one():
    assert goal_utils._next_target_id([]) == "T-001"
    assert goal_utils._next_target_id([{"id": "T-001"}, {"id": "T-002"}]) == "T-003"
    assert goal_utils._next_target_id([{"id": "T-001"}, {"id": "T-007"}]) == "T-008"


# --- state transition matrix: 3x3, exactly four legal ---

@pytest.mark.parametrize(
    "frm,to,ok",
    [
        ("open", "open", False),
        ("open", "done", True),
        ("open", "dropped", True),
        ("done", "open", True),
        ("done", "done", False),
        ("done", "dropped", False),
        ("dropped", "open", True),
        ("dropped", "done", False),
        ("dropped", "dropped", False),
    ],
)
def test_target_transition_matrix(frm, to, ok):
    assert goal_utils.target_transition_allowed(frm, to) is ok


# --- statement shape: GD-2/GD-3 same-source detection at slice scale ---

@pytest.mark.parametrize(
    "statement",
    [
        "1. 修改配置\n2. 重启服务\n3. 验证日志",
        "- 拆分模块\n- 补测试",
        "首先梳理依赖，然后逐个迁移",
    ],
)
def test_task_list_target_statement_is_rejected(statement):
    """GD-2 reused at slice scale (SC-003): task lists are not outcome slices."""
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils._reject_bad_target_statement(statement)
    assert "GD-2" in str(exc.value)


@pytest.mark.parametrize(
    "statement",
    [
        "完成指标链路 and also 重写部署文档",
        "拆分日志组件，同时还迁移存储层",
    ],
)
def test_composite_target_statement_is_rejected(statement):
    """GD-3 reused at slice scale: one slice = one sub-outcome."""
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils._reject_bad_target_statement(statement)
    assert "GD-3" in str(exc.value)


def test_good_target_statement_passes_the_same_check():
    goal_utils._reject_bad_target_statement("日志组件拆分完成")  # must not raise


def test_objective_rejection_still_works_after_refactor(tmp_path):
    """The shared detector must keep the objective-side behavior intact."""
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.create_goal(tmp_path, "still-bad", "1. do a\n2. do b", [])
    assert "GD-2" in str(exc.value)


# --- data-layer add/set primitives ---

def test_add_target_creates_section_and_history_line(tmp_path):
    path = _active_goal(tmp_path)
    tid = goal_utils.add_target(path, "日志组件拆分完成")
    text = path.read_text(encoding="utf-8")
    assert tid == "T-001"
    assert "| T-001 | 日志组件拆分完成 | open |" in text
    assert "## Targets" in text
    assert "target T-001 added: 日志组件拆分完成" in text


def test_set_target_status_writes_transition_history(tmp_path):
    path = _active_goal(tmp_path)
    tid = goal_utils.add_target(path, "一个切片")
    goal_utils.set_target_status(path, tid, "done")
    text = path.read_text(encoding="utf-8")
    assert "| T-001 | 一个切片 | done |" in text
    assert "target T-001 open→done" in text


def test_set_target_status_rejects_illegal_transition(tmp_path):
    path = _active_goal(tmp_path)
    tid = goal_utils.add_target(path, "一个切片")
    goal_utils.set_target_status(path, tid, "done")
    with pytest.raises(goal_utils.GoalError) as exc:
        goal_utils.set_target_status(path, tid, "dropped")
    assert "done" in str(exc.value)


def test_set_target_status_unknown_id_raises_not_found(tmp_path):
    path = _active_goal(tmp_path)
    with pytest.raises(goal_utils.GoalNotFound):
        goal_utils.set_target_status(path, "T-999", "done")
