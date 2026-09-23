"""Contract tests for the goal-utils `targets` action group (038-goal-target, T005)
and the `/speckit.goal` command surface that delivers it (037-goal-registry, T019).

Contracts:
  .specify/specs/038-goal-target/contracts/targets-engine.contract.md
  .specify/specs/037-goal-registry/contracts/goal-command.contract.md

Engine half — pins §1 CLI grammar, §2 the validation table row by row (exit codes
included), §3 rendering invariants, §4 the D6 history notation verbatim, and the
four-value exit-code semantics. The CLI is exercised in-process through main() so
exit codes are asserted directly.

Command-surface half (merged from the former `test_goal_command_surface.py`) —
pins the delivery fan-out (source → 4 per-tool copies), the engine mirror
byte-identity, the reference-doc convention, and FR-021's option-collision
prohibition. The prose-wording pins that file also carried are gone: a bare word
like `view`/`confirm`/`annex` in a 10 KB command template passes no matter what
the mode table says. What survives below names a machine identifier (a CLI
grammar example, a table-row literal, a config key, the concept-authority path)
or a file/parity property. Wording-level propositions are owned by the engine
half of this same file, which executes `main()` rather than grepping for a word.
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
    / ".specify/specs/038-goal-target/contracts/targets-engine.contract.md"
)
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.contract


def _engine():
    spec = importlib.util.spec_from_file_location("goal_utils_targets_contract", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_targets_contract"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _engine()


@pytest.fixture()
def repo(tmp_path):
    """A temp repo root with one active goal carrying two criteria."""
    goal_utils.create_goal(
        tmp_path, "sliced-goal", "A broad platform outcome holds.",
        ["平台整体可用性达到 99.9%", "文档与代码同步更新"],
    )
    return tmp_path


def _run(*argv):
    return goal_utils.main(list(argv))


def _goal_path(repo):
    return repo / ".specify/goal/sliced-goal/goal.md"


# --------------------------------------------------------------------------
# The contract document itself
# --------------------------------------------------------------------------

def test_contract_exists():
    assert CONTRACT.is_file(), f"contract missing: {CONTRACT}"


# test_contract_declares_the_three_target_states removed: asserting that the words
# "open"/"done"/"dropped" occur somewhere in a contract document about Target
# states is true by construction. The three states are owned behaviorally below —
# test_add_issues_open_target_and_renders_the_section (open),
# test_illegal_transition_is_rejected_exit_2 (done -> dropped is illegal),
# test_list_output_is_machine_parsable (exact `T-00N\topen\t...` rows).


# --------------------------------------------------------------------------
# §1 CLI grammar: mutual exclusion and pairing
# --------------------------------------------------------------------------

def test_no_flag_is_an_input_error(repo):
    assert _run("targets", "sliced-goal", "--repo-root", str(repo)) == 2


def test_conflicting_flags_are_an_input_error(repo):
    assert _run("targets", "sliced-goal", "--add", "一个切片", "--list",
                "--repo-root", str(repo)) == 2


def test_set_without_id_is_an_input_error(repo):
    goal_utils.add_target(_goal_path(repo), "先有的切片")
    assert _run("targets", "sliced-goal", "--set", "done",
                "--repo-root", str(repo)) == 2


def test_id_without_set_is_an_input_error(repo):
    goal_utils.add_target(_goal_path(repo), "先有的切片")
    assert _run("targets", "sliced-goal", "--id", "T-001",
                "--repo-root", str(repo)) == 2


def test_unknown_slug_is_not_found(repo):
    assert _run("targets", "no-such-goal", "--list",
                "--repo-root", str(repo)) == 3


# --------------------------------------------------------------------------
# §2 validation table, row by row
# --------------------------------------------------------------------------

def test_terminal_goal_is_read_only_for_add(repo):
    goal_utils.set_status(_goal_path(repo), "achieved")
    code = _run("targets", "sliced-goal", "--add", "新切片",
                "--repo-root", str(repo))
    assert code == 2
    assert "## Targets" not in _goal_path(repo).read_text(encoding="utf-8")


def test_terminal_goal_is_read_only_for_set(repo):
    tid = goal_utils.add_target(_goal_path(repo), "一个切片")
    goal_utils.set_status(_goal_path(repo), "abandoned")
    assert _run("targets", "sliced-goal", "--set", "done", "--id", tid,
                "--repo-root", str(repo)) == 2


def test_empty_statement_is_rejected(repo):
    assert _run("targets", "sliced-goal", "--add", "   ",
                "--repo-root", str(repo)) == 2


def test_gd2_task_list_statement_is_rejected_at_slice_scale(repo):
    """SC-003: the 037 rejection samples rewritten at slice scale, 100% rejected."""
    samples = [
        "1. 修改配置\n2. 重启服务\n3. 验证日志",
        "- 拆分模块\n- 补测试",
        "首先梳理依赖，然后逐个迁移",
    ]
    for sample in samples:
        assert _run("targets", "sliced-goal", "--add", sample,
                    "--repo-root", str(repo)) == 2, f"not rejected: {sample!r}"


def test_gd3_composite_statement_is_rejected_at_slice_scale(repo):
    samples = [
        "完成指标链路 and also 重写部署文档",
        "拆分日志组件，同时还迁移存储层",
    ]
    for sample in samples:
        assert _run("targets", "sliced-goal", "--add", sample,
                    "--repo-root", str(repo)) == 2, f"not rejected: {sample!r}"


def test_statement_normalized_equal_to_a_criterion_is_rejected(repo):
    """FR-004 / D5: punctuation-and-case-insensitive equality with a criterion."""
    assert _run("targets", "sliced-goal", "--add", "平台整体可用性达到 99.9%。",
                "--repo-root", str(repo)) == 2
    assert _run("targets", "sliced-goal", "--add", "文档与代码同步更新！",
                "--repo-root", str(repo)) == 2


def test_unknown_id_is_not_found_exit_3(repo):
    goal_utils.add_target(_goal_path(repo), "一个切片")
    assert _run("targets", "sliced-goal", "--set", "done", "--id", "T-999",
                "--repo-root", str(repo)) == 3


def test_illegal_transition_is_rejected_exit_2(repo):
    tid = goal_utils.add_target(_goal_path(repo), "一个切片")
    _run("targets", "sliced-goal", "--set", "done", "--id", tid,
         "--repo-root", str(repo))
    assert _run("targets", "sliced-goal", "--set", "dropped", "--id", tid,
                "--repo-root", str(repo)) == 2


def test_noop_set_returns_zero_and_writes_no_history(repo):
    tid = goal_utils.add_target(_goal_path(repo), "一个切片")
    before = _goal_path(repo).read_bytes()
    assert _run("targets", "sliced-goal", "--set", "open", "--id", tid,
                "--repo-root", str(repo)) == 0
    assert _goal_path(repo).read_bytes() == before


# --------------------------------------------------------------------------
# §1/§3 add, list, rendering
# --------------------------------------------------------------------------

def test_add_issues_open_target_and_renders_the_section(repo):
    code = _run("targets", "sliced-goal", "--add", "日志组件拆分完成",
                "--repo-root", str(repo))
    assert code == 0
    text = _goal_path(repo).read_text(encoding="utf-8")
    assert "| T-001 | 日志组件拆分完成 | open |" in text
    assert "## Targets" in text


def test_add_sequence_is_monotone_and_terminal_not_reused(repo):
    for statement in ("切片一", "切片二", "切片三"):
        assert _run("targets", "sliced-goal", "--add", statement,
                    "--repo-root", str(repo)) == 0
    _run("targets", "sliced-goal", "--set", "dropped", "--id", "T-002",
         "--repo-root", str(repo))
    assert _run("targets", "sliced-goal", "--add", "切片四",
                "--repo-root", str(repo)) == 0
    data = goal_utils.parse_goal(_goal_path(repo))
    assert [t["id"] for t in data["targets"]] == ["T-001", "T-002", "T-003", "T-004"]


def test_list_output_is_machine_parsable(repo):
    _run("targets", "sliced-goal", "--add", "切片甲", "--repo-root", str(repo))
    _run("targets", "sliced-goal", "--add", "切片乙", "--repo-root", str(repo))
    import io
    import contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = _run("targets", "sliced-goal", "--list", "--repo-root", str(repo))
    assert code == 0
    lines = buffer.getvalue().splitlines()
    assert lines == ["T-001\topen\t切片甲", "T-002\topen\t切片乙"]


def test_list_of_targetless_goal_is_empty_output_exit_zero(repo):
    import io
    import contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = _run("targets", "sliced-goal", "--list", "--repo-root", str(repo))
    assert code == 0
    assert buffer.getvalue() == ""


# --------------------------------------------------------------------------
# §4 History notation (D6), verbatim
# --------------------------------------------------------------------------

def test_add_appends_the_d6_history_line(repo):
    _run("targets", "sliced-goal", "--add", "日志组件拆分完成",
         "--repo-root", str(repo))
    text = _goal_path(repo).read_text(encoding="utf-8")
    assert re.search(
        r"^- \d{4}-\d{2}-\d{2} target T-001 added: 日志组件拆分完成$",
        text, re.M,
    )


def test_transition_appends_the_d6_history_line(repo):
    _run("targets", "sliced-goal", "--add", "一个切片", "--repo-root", str(repo))
    _run("targets", "sliced-goal", "--set", "done", "--id", "T-001",
         "--repo-root", str(repo))
    text = _goal_path(repo).read_text(encoding="utf-8")
    assert re.search(r"^- \d{4}-\d{2}-\d{2} target T-001 open→done$", text, re.M)


# --------------------------------------------------------------------------
# Exit-code semantics: 0/2/3 exercised; 4 belongs to validate
# --------------------------------------------------------------------------

def test_validate_still_owns_exit_code_4(repo):
    path = _goal_path(repo)
    text = path.read_text(encoding="utf-8")
    bad = "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
    path.write_text(text.replace("## History", bad + "\n## History"), encoding="utf-8")
    assert _run("validate", "sliced-goal", "--repo-root", str(repo)) == 4


def test_ok_path_returns_zero(repo):
    assert _run("targets", "sliced-goal", "--add", "合法切片",
                "--repo-root", str(repo)) == 0


# ==========================================================================
# /speckit.goal command surface (037-goal-registry, T019) — merged from the
# former tests/contract/test_goal_command_surface.py
# ==========================================================================

GOAL_CANONICAL = REPO_ROOT / "templates/commands/goal.md"
GOAL_PER_TOOL_COPIES = (
    REPO_ROOT / ".claude/commands/speckit.goal.md",
    REPO_ROOT / ".github/prompts/speckit.goal.prompt.md",
    REPO_ROOT / ".qoder/commands/speckit.goal.md",
    REPO_ROOT / ".opencode/command/speckit.goal.md",
)
REFERENCE_DOC = REPO_ROOT / "docs/reference/commands/goal.md"
ENGINE_MIRROR = REPO_ROOT / ".specify/scripts/python/goal-utils.py"

AUTHORITY = ".specify/shared/definitions/goal-definitions.md"


def test_canonical_source_exists():
    assert GOAL_CANONICAL.is_file(), f"command source of truth missing: {GOAL_CANONICAL}"


def test_canonical_has_frontmatter_with_a_description():
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "command template must open with frontmatter"
    head = text.split("---", 2)[1]
    assert "description:" in head


# test_mirror_is_byte_identical removed 2026-08-17: the .specify/templates/commands/
# mirror is retired — per-tool copies are generated straight from templates/commands/.


@pytest.mark.parametrize("path", GOAL_PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copy_exists_and_is_generated(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text, f"{path.name} lacks the AUTO-GENERATED header"
    assert "templates/commands/goal.md" in text, (
        f"{path.name} does not name its source template"
    )


def test_reference_doc_joins_the_one_per_command_convention():
    """docs/reference/commands/ holds one file per command and no index."""
    docs = sorted(p.name for p in (REPO_ROOT / "docs/reference/commands").glob("*.md"))
    assert "goal.md" in docs
    assert "README.md" not in docs, "nested README.md is a reserved-name violation"


def test_engine_exists_with_its_mirror():
    assert ENGINE.is_file()
    assert ENGINE_MIRROR.is_file(), "run sync-mirrors.py --write"
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes()


# --------------------------------------------------------------------------
# FR-021 — no colliding option name
# --------------------------------------------------------------------------

def test_no_new_goal_option_is_introduced():
    """`--goal` is already claimed with two different meanings, so identity is positional."""
    for path in (GOAL_CANONICAL, ENGINE):
        text = path.read_text(encoding="utf-8")
        assert "--goal " not in text and '"--goal"' not in text, (
            f"{path.name} introduces a --goal option, colliding with "
            "build-summary-input.py (goal identity) and match-team-preset.py (goal text)"
        )


# --------------------------------------------------------------------------
# Concept-authority discipline (GC-8)
# --------------------------------------------------------------------------

def test_command_links_to_the_concept_authority():
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    assert AUTHORITY in text or "goal-definitions.md" in text, (
        "the command must link to the concept authority"
    )


# --------------------------------------------------------------------------
# 038 — the targets action group on the command surface
# --------------------------------------------------------------------------

def test_targets_mode_row_is_documented():
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    assert "| `targets` |" in text, "Modes table must carry a targets row"


def test_engine_invocation_examples_cover_the_targets_action_group():
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    for example in ("targets <goal-slug> --add", "targets <goal-slug> --list",
                    "targets <goal-slug> --set"):
        assert example in text, f"engine example missing: {example}"


def test_command_block_is_grouped_by_read_and_write():
    """F-13 ②: the command surface declares which actions write, and reaches the
    flag set by reference instead of restating it."""
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    assert "读组" in text and "写组" in text, "the command block lost its read/write split"
    assert "--help" in text, "the flag owner must be named, not copied"


def test_command_names_the_destructive_write_and_its_bucket_owner():
    """F-13 ③: goal's destructive write is registered, and the command reaches the
    bucket owner by reference. The wording MUST stay off the scanner's blocking
    patterns — the gate budget's integer headroom is 0, so the only route back to
    green is rewording, never re-freezing a baseline."""
    text = GOAL_CANONICAL.read_text(encoding="utf-8")
    assert "--clear" in text, "the explicit empty-overwrite flag is not disclosed"
    assert "破坏性动作清单" in text, "the bucket owner is not referenced"
    assert "exit 2" in text, "the argument-less rejection is not disclosed"


@pytest.mark.parametrize("path", GOAL_PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_the_targets_content(path):
    """Derived from the same GOAL_PER_TOOL_COPIES fixture — no second copy list."""
    text = path.read_text(encoding="utf-8")
    assert "targets <goal-slug> --add" in text, f"{path.name} lacks targets content"
