"""Contract tests for documentation same-source — one syntax, one body, no stale literals
(104-agents-run, US4).

Clause source: .specify/specs/104-agents-run/contracts/agents-run-docs.contract.md
(C-23..C-34, artifact-class). C-35 (the mutation drill) is a recorded exercise, not a test
here.

Red-first (Constitution IV): authored at T016 while `docs/reference/commands/agents.md` is
still the three-copy concatenation (`^# /speckit.agents` count = 3) and the tutorials /
routing scenario still carry the stale no-argument claims — so C-23..C-34 fail against the
unchanged tree. C-23..C-31 turn green when the four reference surfaces land (T017..T020);
C-32..C-34 close with the tutorials, the routing scenario and the US4 checkpoint (T021..T023).

Clause-class honesty (FR-023): these are artifact-class pins (counts, literals, section
content). This module does not claim contract coverage of runtime behaviour.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

R1 = REPO_ROOT / "docs" / "reference" / "commands" / "agents.md"
R2 = REPO_ROOT / "docs" / "reference" / "agents" / "command-and-skills.md"
R3 = REPO_ROOT / "docs" / "reference" / "agents" / "overview.md"
R4 = REPO_ROOT / "docs" / "reference" / "agents" / "design.md"
R5 = REPO_ROOT / "docs" / "tutorials" / "installation.md"
R6 = REPO_ROOT / "docs" / "tutorials" / "quickstart.md"
R7 = REPO_ROOT / "tests" / "scenarios" / "agents-command" / "single-entry-routing-scenario.md"

SEVEN_FILES = {"R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5, "R6": R6, "R7": R7}

STR_001 = "[create|refine|run] [agent-name] [task]"          # [[STR-001]]
STR_005 = "capabilities (create / refine)"                    # [[STR-005]]
STR_006 = "create and refine one agent"                       # [[STR-006]]
STR_007 = "Generate role-based agents or create custom agents"  # [[STR-007]]
STR_008 = "generates the seven role-based workflow agents"    # [[STR-008]]
BOLD_VARIANT = "creates or refines **one** agent"             # measured variant of STR-006
RUN_SYNTAX = "run <agent-name> [task]"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    """Collapse whitespace so phrase assertions survive line wrapping."""
    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    """Body of a markdown heading section, up to the next heading of same-or-higher level."""
    lines = text.splitlines()
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    assert start is not None, f"section {heading!r} not found"
    body = []
    for line in lines[start:]:
        if line.startswith("#"):
            head = len(line) - len(line.lstrip("#"))
            if head <= level:
                break
        body.append(line)
    return "\n".join(body)


def _table_rows(section: str) -> list[str]:
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if set(stripped) <= set("|-: "):
            continue
        rows.append(stripped)
    return rows


def _stale_counts() -> list[tuple[str, int]]:
    """Occurrence counts for the closed C-34 predicate table over the seven named files."""
    texts = {key: _read(path) for key, path in SEVEN_FILES.items()}

    def fixed(literal: str, case_insensitive: bool = False) -> int:
        total = 0
        for text in texts.values():
            haystack = text.lower() if case_insensitive else text
            needle = literal.lower() if case_insensitive else literal
            total += haystack.count(needle)
        return total

    def noarg_generate_lines() -> int:
        hits = 0
        for text in texts.values():
            for line in text.splitlines():
                low = line.lower()
                if "no arguments" in low and "generate" in low:
                    hits += 1
        return hits

    return [
        ("STR-005", fixed(STR_005)),
        ("STR-006", fixed(STR_006)),
        ("bold variant of STR-006", fixed(BOLD_VARIANT)),
        ("STR-007", fixed(STR_007)),
        ("STR-008", fixed(STR_008)),
        ("ci: generate role-based agents", fixed("generate role-based agents", True)),
        ("ci: generate project-aware role agents", fixed("generate project-aware role agents", True)),
        ("ci: generate seven", fixed("generate seven", True)),
        ("line with 'no arguments' and 'generate'", noarg_generate_lines()),
    ]


def test_c23_one_command_reference_body():
    """C-23: exactly one top-level `# /speckit.agents` heading."""
    text = _read(R1)
    headings = [line for line in text.splitlines() if line.startswith("# /speckit.agents")]
    assert len(headings) == 1, (
        f"the command reference still carries {len(headings)} concatenated bodies"
    )


def test_c24_opening_description_names_three_capabilities():
    """C-24: the opening paragraph describes create, refine and run; STR-006 is gone."""
    lines = _read(R1).splitlines()
    opening: list[str] = []
    started = False
    for line in lines:
        if line.startswith("# "):
            if started:
                break
            started = True
            continue
        if started:
            if line.startswith("#"):
                break
            opening.append(line)
    paragraph = _norm("\n".join(opening))
    assert "entry point" in paragraph, "the opening paragraph lost its entry-point statement"
    for verb in ("create", "refine", "run"):
        assert re.search(rf"\b{verb}\b", paragraph), (
            f"the opening paragraph does not name the {verb} capability"
        )
    assert STR_006 not in _read(R1), "[[STR-006]] still appears in the command reference"


def test_c25_syntax_block_carries_the_explicit_run_form():
    """C-25: [[STR-001]] verbatim, the explicit run line, a no-arg line, an intent line."""
    syntax = _norm(_section(_read(R1), "## Syntax"))
    assert STR_001 in syntax, "the Syntax block lacks [[STR-001]]"
    assert f"/speckit.agents {RUN_SYNTAX}" in syntax, (
        "the Syntax block lacks the explicit `/speckit.agents run <agent-name> [task]` line"
    )
    lowered = syntax.lower()
    assert "no arguments" in lowered, "the no-argument line is missing"
    assert "list" in lowered and "suggest" in lowered, (
        "the no-argument line no longer describes list + grounded suggestions"
    )
    assert "natural-language" in lowered, "the natural-language intent line is missing"


def test_c26_intent_table_run_row_and_three_way_ambiguity():
    """C-26: the intent table has a run row beside create/refine; ambiguity names three."""
    table = _section(_read(R1), "## Intent Routing")
    rows = _table_rows(table)
    run_rows = [row for row in rows if "run-agent" in row]
    create_rows = [row for row in rows if "create-agent" in row]
    refine_rows = [row for row in rows if "improve-agent" in row]
    assert len(run_rows) == 1, f"expected exactly one run row, got {len(run_rows)}"
    assert re.search(r"\brun\b", run_rows[0], re.IGNORECASE), "the run row lost its verb"
    assert len(create_rows) == 1 and len(refine_rows) == 1
    assert "create / refine / run" in _norm(table), (
        "the ambiguity sentence does not report the three capabilities"
    )
    assert STR_005 not in _read(R1), "[[STR-005]] still appears in the command reference"


def test_c27_companion_skills_lists_three_skills():
    """C-27: create-agent, improve-agent and run-agent are all listed with their role."""
    section = _norm(_section(_read(R1), "## Companion Skills"))
    for name in ("create-agent", "improve-agent", "run-agent"):
        assert f"- `{name}` —" in section, f"the companion-skills list lost the {name} row"


def test_c28_no_argument_behaviour_matches_the_template():
    """C-28: list -> suggestions -> three-mode summary; no generate claim; C-34 holds for R1."""
    section = _norm(_section(_read(R1), "## Default Behavior (No Arguments)"))
    assert "list every existing agent" in section.lower(), "the listing step is missing"
    assert "suggestions" in section.lower(), "the grounded-suggestion step is missing"
    assert "three-mode" in section.lower() or "three modes" in section.lower(), (
        "the three-mode capability summary is missing"
    )
    raw = _read(R1)
    assert STR_008 not in raw, "[[STR-008]] still appears in the command reference"
    for predicate, count in _stale_counts():
        if predicate in ("STR-005", "STR-006", "bold variant of STR-006", "STR-007"):
            # measured per-file below in C-34; each must still be zero in R1
            assert count >= 0
    r1_text = raw.lower()
    assert "generate role-based agents" not in r1_text
    assert "generate seven" not in r1_text


def test_c29_command_and_skills_becomes_three_capability():
    """C-29: three capabilities, run row + flow, a run-agent section by pointer, no stale forms."""
    raw = _read(R2)
    text = _norm(raw)
    for verb in ("create", "refine", "run"):
        assert re.search(rf"\b{verb}\b", text), f"the description does not name {verb}"
    assert "three skills" in text.lower(), "the skill-count statement is not three"
    rows = _table_rows(_section(raw, "### Intent → capability routing"))
    assert any("run-agent" in row for row in rows), "the intent table lacks a run row"
    assert "### `run-agent`" in raw, "the run-agent section heading is missing"
    run_section = _norm(_section(raw, "### `run-agent` — dispatch engine"))
    for step in ("resolve", "present", "dispatch", "external", "report"):
        assert step in run_section.lower(), f"the run-agent section omits the {step} step"
    assert "skills/internal/run-agent/SKILL.md" in run_section, (
        "the run-agent section does not cite its output contract by path"
    )
    for stale in (STR_006, BOLD_VARIANT, STR_005):
        assert stale not in raw, f"a two-capability statement survives in R2: {stale!r}"


def test_c30_overview_gains_run_and_the_third_skill():
    """C-30: capability statement, both skill-count statements, and the diagram carry run."""
    text = _read(R3)
    command_line = next(
        (line for line in text.splitlines() if line.startswith("- **命令（Command）**")), None
    )
    assert command_line is not None, "the command capability bullet is missing"
    for verb in ("创作", "优化", "运行"):
        assert verb in command_line, f"the command capability bullet lost {verb}"
    assert "三个技能" in text, "the prose skill-count statement is not three"
    nav_line = next(
        (line for line in text.splitlines() if "command-and-skills.md" in line and line.startswith("|")),
        None,
    )
    assert nav_line is not None and "三个单 Agent 技能" in nav_line, (
        "the navigation row still says two single-agent skills"
    )
    blocks = re.findall(r"```.*?```", text, re.DOTALL)
    diagram = next((block for block in blocks if "/speckit.agents" in block), None)
    assert diagram is not None, "the entry diagram block is missing"
    assert "run-agent" in diagram, "the entry diagram's skill layer lacks run-agent"


def test_c31_design_gains_run_and_the_third_skill():
    """C-31: capability line, workflow step and single-agent skill list carry run."""
    text = _read(R4)
    capability_line = next(
        (line for line in text.splitlines() if "单 Agent" in line and "唯一入口" in line), None
    )
    assert capability_line is not None, "the single-agent capability line is missing"
    assert "运行" in capability_line, "the capability line does not name the run capability"
    workflow = text.split("单 Agent 命令工作流程", 1)[1].split("###", 1)[0]
    assert "run-agent" in workflow, "the workflow does not carry the run step"
    skills_section = text.split("### 6.2 技能", 1)[1].split("###", 1)[0]
    assert "run-agent" in skills_section, "the single-agent skill list lacks run-agent"


def test_c32_tutorials_carry_run_and_drop_the_stale_claims():
    """C-32: command-table rows name create/refine/run; STR-007 and stale predicates are gone."""
    for path in (R5, R6):
        text = _read(path)
        row = next(
            (line for line in text.splitlines() if line.strip().startswith("| `/speckit.agents`")),
            None,
        )
        assert row is not None, f"{path.name} lost its /speckit.agents command-table row"
        for verb in ("create", "refine", "run"):
            assert verb in row.lower(), f"{path.name} command-table row does not name {verb}"
        assert STR_007 not in text, f"{path.name} still carries [[STR-007]]"
        lowered = text.lower()
        assert "generate role-based agents" not in lowered
        assert "generate project-aware role agents" not in lowered
        assert "generate seven" not in lowered
        assert not any(
            "no arguments" in line.lower() and "generate" in line.lower()
            for line in text.splitlines()
        ), f"{path.name} still claims no-argument generation"


def test_c33_routing_scenario_is_three_capability():
    """C-33: single-agent scope is create/refine/run; explicit run samples; STR-005 gone."""
    raw = _read(R7)
    text = _norm(raw)
    assert "create / refine / run" in text, "the single-agent scope is not three-capability"
    assert RUN_SYNTAX in text, "the scenario lacks the explicit run syntax sample"
    assert re.search(r"run[\s\S]{0,80}run-agent", text), (
        "no routing sample connects the run intent to run-agent"
    )
    assert "create / refine / run" in _norm(raw.split("I4", 1)[-1]), (
        "the ambiguous-input expectation is not three-way"
    )
    assert STR_005 not in raw, "[[STR-005]] still appears in the routing scenario"


def test_c34_stale_literal_set_is_empty_and_history_is_untouched():
    """C-34: every predicate in the closed table counts zero across the seven named files."""
    counts = _stale_counts()
    nonzero = [(predicate, count) for predicate, count in counts if count != 0]
    assert nonzero == [], f"stale-literal predicates still fire: {nonzero}"
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "docs/reference/history/"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "", (
        "docs/reference/history/ carries changes — dated records are read-only:\n" + result.stdout
    )
