"""Contract tests for the `/speckit.team view` command wiring (103-team-view, T007).

Contract: `.specify/specs/103-team-view/contracts/team-view-command.contract.md`
C-01 (frontmatter), C-02 (four-row mode table), C-03 (stale literal), C-06 (View Mode
delegation), C-11 (read-only at the command level). FR-001…FR-004.

This first segment pins the command template only; the docs page, routing flow and the
per-tool copies are pinned by the US3 segment appended later (T026). The template source
is `templates/commands/team.md`; per-tool copies are generated and never hand-edited.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "team.md"

pytestmark = pytest.mark.contract

STR_001 = "team not found"
STR_003 = "[create|modify|run|view] [team-slug] [--target <T-<nnn>>]"
STR_004 = "exactly three modes"

VIEW_MODE_DELEGATE = ".specify/skills/internal/view-team/SKILL.md"
FIXED_EXTRACTION = "scripts/python/team-view.py"


def read_template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def frontmatter_of(text: str) -> dict:
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", "template carries no frontmatter"
    end = lines.index("---", 1)
    data = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data


def section_after(text: str, heading: str) -> str:
    start = text.find(heading)
    assert start >= 0, "missing heading: %s" % heading
    rest = text[start + len(heading):]
    following = re.search(r"^#{2,3} ", rest, re.MULTILINE)
    return rest[:following.start()] if following else rest


def mode_rows(text: str) -> list:
    section = section_after(text, "### Modes → Capability Routing")
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header row


class TestFrontmatter:
    def test_description_names_the_four_team_operations(self):
        data = frontmatter_of(read_template())
        description = data.get("description", "").lower()
        for token in ("create", "modify", "run", "view"):
            assert token in description, "description lacks %s" % token

    def test_short_description_names_four_modes(self):
        data = frontmatter_of(read_template())
        short = data.get("short-description", "").lower()
        for token in ("create", "modify", "run", "view"):
            assert token in short, "short-description lacks %s" % token

    def test_argument_hint_is_the_shared_grammar(self):
        data = frontmatter_of(read_template())
        assert data.get("argument-hint") == STR_003


class TestModeTable:
    def test_exactly_four_rows_in_order(self):
        rows = mode_rows(read_template())
        assert len(rows) == 4, "mode table must carry exactly four rows: %r" % rows
        modes = [re.sub(r"[*`]", "", row[0]).strip() for row in rows]
        assert modes == ["create", "modify", "run", "view"]

    def test_view_row_recognizes_view_intents_and_delegates(self):
        rows = mode_rows(read_template())
        view_row = " | ".join(rows[-1])
        for token in ("查看", "概览", "inspect", "show"):
            assert token in view_row, "view row lacks intent token %s" % token
        assert "view-team" in view_row

    def test_other_rows_keep_their_routing_targets(self):
        rows = mode_rows(read_template())
        joined = [" | ".join(row) for row in rows]
        assert "create-team" in joined[0]
        assert "improve-team" in joined[1]
        assert "run-team" in joined[2]
        for row in rows[:3]:
            assert "view-team" not in " | ".join(row), "view leaked into another row"

    def test_stale_three_modes_literal_is_gone_from_the_template(self):
        assert STR_004 not in read_template()


class TestViewModeSection:
    def test_view_mode_section_exists_and_delegates(self):
        view = section_after(read_template(), "### View Mode")
        assert VIEW_MODE_DELEGATE in view
        assert FIXED_EXTRACTION in view

    def test_view_mode_states_read_only_boundary(self):
        view = section_after(read_template(), "### View Mode")
        assert "只读" in view
        assert "run line" in view
        assert "席位" in view

    def test_view_mode_states_the_missing_team_and_corrupt_paths(self):
        view = section_after(read_template(), "### View Mode")
        assert STR_001 in view
        assert "定义损坏" in view
        assert "create" in view
        assert "概览" in view

    def test_view_mode_keeps_the_five_check_preview_out(self):
        view = section_after(read_template(), "### View Mode")
        assert "run-team" in view
        assert "blocked" in view

    def test_view_target_conflict_declared(self):
        view = section_after(read_template(), "### View Mode")
        conflict_lines = [
            line for line in view.splitlines()
            if "--target" in line and "冲突" in line
        ]
        assert conflict_lines, "View Mode must declare view+--target as a mode/parameter conflict"


# --------------------------------------------------------------------------- #
# US3 segment (T026): routing flow, default/ambiguous behavior, docs page,
# per-tool copies. C-03, C-04, C-05, C-07, C-08, C-09, C-10, C-12.
# --------------------------------------------------------------------------- #
DOCS = REPO_ROOT / "docs" / "reference" / "commands" / "team.md"

COPY_PATHS = (
    REPO_ROOT / ".claude" / "commands" / "speckit.team.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.team.prompt.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.team.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.team.md",
)

VIEW_TOKENS = (
    "查看", "展示", "呈现", "团队状态", "团队详情", "概览",
    "overview", "status", "inspect", "show",
)

DOCS_FALSE_CLAIMS = (
    "never executes before you confirm",
    "Only then does orchestration run",
    "Declining stops without executing",
)


def read_docs() -> str:
    return DOCS.read_text(encoding="utf-8")


def rows_after(text: str, heading: str) -> list:
    section = section_after(text, heading)
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header row


def rows_by_mode(text: str, heading: str) -> dict:
    table = {}
    for row in rows_after(text, heading):
        mode = re.sub(r"[*`]", "", row[0]).strip()
        table[mode] = " | ".join(row)
    return table


class TestRoutingSamples:
    """C-09: the seven-sample routing set through the deterministic token proxy."""

    @pytest.mark.parametrize(
        "sample,token,expected",
        [
            ("查看 cws-workspace-cluster 的结构和状态", "查看", "view"),
            ("show me the team structure", "show", "view"),
            ("overview of all teams", "overview", "view"),
            ("创建一个团队来跑回归", "创建", "create"),
            ("调整团队的人员配置", "调整", "modify"),
            ("运行团队 --target T-001", "运行", "run"),
        ],
    )
    def test_sample_token_lands_in_its_expected_mode_row(self, sample, token, expected):
        assert token in sample, "sample lost its distinctive token: %r" % sample
        rows = rows_by_mode(read_template(), "### Modes → Capability Routing")
        assert token in rows[expected], "sample %r: %r missing from the %s row" % (
            sample, token, expected)

    def test_view_tokens_never_land_in_the_other_mode_rows(self):
        rows = rows_by_mode(read_template(), "### Modes → Capability Routing")
        for token in VIEW_TOKENS:
            for mode in ("create", "modify", "run"):
                assert token not in rows[mode], "%r leaked into the %s row" % (token, mode)

    def test_bare_team_input_reports_capabilities_without_executing(self):
        section = section_after(read_template(), "### Ambiguous or Unsupported Intent")
        for mode in ("create", "modify", "run", "view"):
            assert re.search(r"\*\*%s\*\*" % mode, section), (
                "ambiguous capability list lacks %s" % mode)
        assert "MUST NOT execute any mode" in section


class TestNoGuessRouting:
    """C-04: the routing flow classifies view and keeps the no-guess invariants."""

    def test_routing_flow_classifies_and_delegates_view(self):
        routing = section_after(read_template(), "**Routing flow**")
        assert re.search(r"classify as `create`, `modify`, `run`, or `view`", routing)
        assert re.search(r"^\d+\.\s+\*\*view\*\*\s*→\s*`view-team`", routing, re.MULTILINE), (
            "no dedicated view → view-team routing step")

    def test_view_target_is_a_mode_parameter_conflict_in_routing(self):
        routing = section_after(read_template(), "**Routing flow**")
        conflicts = [
            line for line in routing.splitlines()
            if "view" in line and "--target" in line and "冲突" in line
        ]
        assert conflicts, "routing flow must report view+--target as a mode/parameter conflict"


class TestDefaultBehaviorModes:
    """C-05: the no-argument capability summary names all four modes."""

    def test_capability_summary_names_four_modes(self):
        section = section_after(read_template(), "### Default Behavior (No Arguments)")
        assert "four modes" in section
        for mode in ("create", "modify", "run", "view"):
            assert mode in section, "default-behavior summary lacks %s" % mode

    def test_default_behavior_is_not_an_implicit_view(self):
        section = section_after(read_template(), "### Default Behavior (No Arguments)")
        assert "view-team" not in section, "default behavior must not delegate view"
        assert "informational and non-destructive" in section


class TestDocsPage:
    """C-07: the docs page carries four modes and the View Mode section."""

    def test_opening_and_when_to_use_name_four_modes(self):
        text = read_docs()
        opening = text.split("## When to Use")[0].lower()
        for mode in ("create", "modify", "run", "view"):
            assert mode in opening, "opening paragraph lacks %s" % mode
        when = section_after(text, "## When to Use").lower()
        for mode in ("create", "modify", "run", "view"):
            assert mode in when, "When to Use lacks %s" % mode

    def test_syntax_lists_view(self):
        assert "view" in section_after(read_docs(), "## Syntax")

    def test_mode_table_has_four_rows_in_order(self):
        rows = rows_after(read_docs(), "## Modes → Intent Routing")
        assert len(rows) == 4, "docs mode table must carry four rows: %r" % rows
        modes = [re.sub(r"[*`]", "", row[0]).strip() for row in rows]
        assert modes == ["create", "modify", "run", "view"]

    def test_view_mode_section_covers_the_required_points(self):
        view = section_after(read_docs(), "## View Mode")
        for token in (
            "read-only", "overview", "Exact slug match", STR_001, "create",
            "定义损坏", "Not a run preview",
        ):
            assert token in view, "docs View Mode lacks %r" % token

    def test_companion_skills_lists_view_team(self):
        assert "view-team" in section_after(read_docs(), "## Companion Skills")


class TestDocsRunDrift:
    """C-08: the two run-mode drift corrections land in the same change."""

    def test_run_row_delegates_to_run_team(self):
        rows = rows_by_mode(read_docs(), "## Modes → Intent Routing")
        assert "run-team" in rows["run"]
        assert "create-team (execution path)" not in read_docs()

    def test_preview_is_disclosure_not_a_blocking_gate(self):
        text = read_docs()
        for literal in DOCS_FALSE_CLAIMS:
            assert literal not in text, "stale run claim still present: %r" % literal
        run_section = section_after(text, "## Run Mode")
        assert "披露" in run_section or "disclosure" in run_section.lower()


class TestNamedFilesModeCounts:
    """C-10: both named files carry four mode identifiers and no stale literal."""

    @pytest.mark.parametrize(
        "heading,path",
        [
            ("### Modes → Capability Routing", TEMPLATE),
            ("## Modes → Intent Routing", DOCS),
        ],
        ids=["template", "docs"],
    )
    def test_four_modes_and_no_stale_literal(self, heading, path):
        text = path.read_text(encoding="utf-8")
        assert STR_004 not in text
        rows = rows_after(text, heading)
        modes = [re.sub(r"[*`]", "", row[0]).strip() for row in rows]
        assert len(modes) == 4, "mode table must carry four rows: %r" % modes
        for mode in ("create", "modify", "run", "view"):
            assert mode in modes


class TestPerToolCopies:
    """C-03: every shipped per-tool copy carries view and no stale literal."""

    @pytest.mark.parametrize("path", COPY_PATHS, ids=lambda path: path.name)
    def test_copy_carries_view_and_no_stale_literal(self, path):
        assert path.is_file(), "missing per-tool copy: %s" % path
        text = path.read_text(encoding="utf-8")
        assert STR_004 not in text
        assert "view" in text


class TestRetiredMirror:
    """C-12: no `.specify/templates/commands/` mirror exists."""

    def test_no_specify_template_commands_mirror(self):
        assert not (REPO_ROOT / ".specify" / "templates" / "commands").exists()
