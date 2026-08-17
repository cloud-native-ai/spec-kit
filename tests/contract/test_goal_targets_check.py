"""Contract tests for the goal-utils `targets --check` dry-run (042-goal-team-creation, T010).

Contract: .specify/specs/042-goal-team-creation/contracts/decomposition-proposal.contract.md §C-1

`--check` validates a candidate Target statement against the SAME grammar as
`--add` (GD-2 / GD-3 / criteria-restatement) while performing ZERO writes — no
identity issuance, no goal.md mutation, no `## History` line. This suite pins the
exit-code table (0 ok / 2 rejected / 3 unknown slug / 4 terminal goal), the
mutual-exclusion rule, the --json verdict shape, and the byte-identity of
goal.md across every path. The CLI is exercised in-process through main() so
exit codes are asserted directly (same style as test_goal_targets_engine.py).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.contract


def _engine():
    spec = importlib.util.spec_from_file_location("goal_utils_check_contract", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_check_contract"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _engine()


@pytest.fixture()
def repo(tmp_path):
    """A temp repo root with one active goal carrying two criteria (038 fixture shape)."""
    goal_utils.create_goal(
        tmp_path, "sliced-goal", "A broad platform outcome holds.",
        ["平台整体可用性达到 99.9%", "文档与代码同步更新"],
    )
    return tmp_path


@pytest.fixture()
def terminal_repo(tmp_path):
    goal_utils.create_goal(
        tmp_path, "done-goal", "A finished outcome holds.", ["判据一"]
    )
    goal_utils.set_status(goal_utils.definition_path(tmp_path, "done-goal"), "achieved")
    return tmp_path


def _run(*argv) -> int:
    return goal_utils.main(list(argv))


def _goal_path(repo) -> Path:
    return repo / ".specify/goal/sliced-goal/goal.md"


VALID = "评测引擎的会话取证链路拆分完成"


# --------------------------------------------------------------------------
# exit 0: a valid outcome-form statement passes, and nothing is written
# --------------------------------------------------------------------------

def test_valid_statement_passes_exit_0(repo):
    before = _goal_path(repo).read_bytes()
    mtime = _goal_path(repo).stat().st_mtime_ns
    assert _run("targets", "sliced-goal", "--check", VALID,
                "--repo-root", str(repo)) == 0
    assert _goal_path(repo).read_bytes() == before, "goal.md MUST stay byte-identical"
    assert _goal_path(repo).stat().st_mtime_ns == mtime, "goal.md MUST not be rewritten"


def test_check_issues_no_identity_and_no_history(repo):
    assert _run("targets", "sliced-goal", "--check", VALID,
                "--repo-root", str(repo)) == 0
    data = goal_utils.parse_goal(_goal_path(repo))
    assert data["targets"] == [], "no identity may be issued by --check"
    assert "target T-" not in data["history"], "no history line may be recorded"


def test_check_does_not_advance_the_next_identity(repo):
    assert _run("targets", "sliced-goal", "--check", VALID,
                "--repo-root", str(repo)) == 0
    tid = goal_utils.add_target(_goal_path(repo), "另一个成果形切片")
    assert tid == "T-001", "a dry-run check must not consume an identity slot"


# --------------------------------------------------------------------------
# exit 2: statement rejections (same-source grammar as --add)
# --------------------------------------------------------------------------

def test_gd2_step_form_is_rejected_exit_2(repo):
    for sample in ("1. 修改配置\n2. 重启服务", "首先梳理依赖，然后逐个迁移"):
        assert _run("targets", "sliced-goal", "--check", sample,
                    "--repo-root", str(repo)) == 2, f"not rejected: {sample!r}"


def test_gd3_composite_is_rejected_exit_2(repo):
    assert _run("targets", "sliced-goal", "--check", "完成指标链路 and also 重写部署文档",
                "--repo-root", str(repo)) == 2


def test_criteria_restatement_is_rejected_exit_2(repo):
    assert _run("targets", "sliced-goal", "--check", "平台整体可用性达到 99.9%。",
                "--repo-root", str(repo)) == 2
    assert _run("targets", "sliced-goal", "--check", "文档与代码同步更新！",
                "--repo-root", str(repo)) == 2


def test_empty_statement_is_rejected_exit_2(repo):
    assert _run("targets", "sliced-goal", "--check", "   ",
                "--repo-root", str(repo)) == 2


def test_rejection_leaves_goal_md_untouched(repo):
    before = _goal_path(repo).read_bytes()
    _run("targets", "sliced-goal", "--check", "首先做 A，然后做 B",
         "--repo-root", str(repo))
    assert _goal_path(repo).read_bytes() == before


# --------------------------------------------------------------------------
# exit 3 / exit 4: unknown slug / terminal goal
# --------------------------------------------------------------------------

def test_unknown_slug_is_exit_3(repo):
    assert _run("targets", "no-such-goal", "--check", VALID,
                "--repo-root", str(repo)) == 3


def test_terminal_goal_is_exit_4(terminal_repo):
    """Contract §C-1: the goal-state rejection is EXIT_INVALID (4), distinct
    from statement rejections (2) — a proposal has nowhere to land on a
    terminal goal."""
    before = (terminal_repo / ".specify/goal/done-goal/goal.md").read_bytes()
    assert _run("targets", "done-goal", "--check", VALID,
                "--repo-root", str(terminal_repo)) == 4
    assert (terminal_repo / ".specify/goal/done-goal/goal.md").read_bytes() == before


# --------------------------------------------------------------------------
# mutual exclusion with --add / --list / --set
# --------------------------------------------------------------------------

def test_check_is_mutually_exclusive_with_add(repo):
    assert _run("targets", "sliced-goal", "--check", VALID, "--add", VALID,
                "--repo-root", str(repo)) == 2
    assert _goal_path(repo).read_bytes() != b"" and \
        "T-001" not in goal_utils.parse_goal(_goal_path(repo))["history"], \
        "the conflicting invocation must not fall through to --add"


def test_check_is_mutually_exclusive_with_list(repo):
    assert _run("targets", "sliced-goal", "--check", VALID, "--list",
                "--repo-root", str(repo)) == 2


def test_bare_targets_still_demands_exactly_one_action(repo):
    assert _run("targets", "sliced-goal", "--repo-root", str(repo)) == 2


# --------------------------------------------------------------------------
# --json verdict shape
# --------------------------------------------------------------------------

def test_json_success_carries_verdict_ok(repo, capsys):
    assert _run("targets", "sliced-goal", "--check", VALID,
                "--repo-root", str(repo), "--json") == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload.get("verdict") == "ok"


def test_json_rejection_carries_verdict_and_reason(repo, capsys):
    assert _run("targets", "sliced-goal", "--check", "首先做 A，然后做 B",
                "--repo-root", str(repo), "--json") == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload.get("verdict") == "rejected"
    assert payload.get("error"), "the rejection reason MUST accompany the verdict"


def test_json_terminal_carries_verdict_goal_terminal(terminal_repo, capsys):
    assert _run("targets", "done-goal", "--check", VALID,
                "--repo-root", str(terminal_repo), "--json") == 4
    payload = json.loads(capsys.readouterr().out)
    assert payload.get("verdict") == "goal-terminal"
