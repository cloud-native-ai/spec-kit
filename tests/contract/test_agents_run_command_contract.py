"""Contract tests for the explicit run wiring — command face (104-agents-run, US1).

Clause source: .specify/specs/104-agents-run/contracts/agents-run-command.contract.md
(C-01..C-10, artifact-class; C-08 is the routing sample set with deterministic proxies).

Clause-class honesty (FR-023): every assertion here pins an artifact — template
frontmatter, a delegation table row, a stated stop path, a generated copy, the
documented Syntax block. No test claims to cover runtime behaviour.

Red-first (Constitution IV): authored at T002 before T004 edits the template, so the
C-01..C-05 / C-10 legs fail against the unchanged tree; C-06 stays red until the
command reference is merged (T017) and C-09 stays red once the template body moves
ahead of the generated copies (regenerated at T027).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "agents.md"
SKILL = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
DOCS = REPO_ROOT / "docs" / "reference" / "commands" / "agents.md"
TEAM = REPO_ROOT / "templates" / "commands" / "team.md"

COPIES = (
    REPO_ROOT / ".claude" / "commands" / "speckit.agents.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.agents.prompt.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.agents.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.agents.md",
)

STR_001 = "[create|refine|run] [agent-name] [task]"      # [[STR-001]]
STR_002 = "agent not found"                              # [[STR-002]]
STR_003 = "missing agent name"                           # [[STR-003]]
STR_004 = "missing task"                                 # [[STR-004]]

RUN_SYNTAX = "run <agent-name> [task]"
SKILL_PATHS = {
    "run": ".specify/skills/internal/run-agent/SKILL.md",
    "create": ".specify/skills/internal/create-agent/SKILL.md",
    "refine": ".specify/skills/internal/improve-agent/SKILL.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    """Collapse whitespace so a phrase assertion is not defeated by line wrapping."""
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


def _frontmatter(text: str) -> list[str]:
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", "file must open with YAML frontmatter"
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:i]
    raise AssertionError("unterminated YAML frontmatter")


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


def _delegation_rows() -> list[str]:
    rows = _table_rows(_section(_read(TEMPLATE), "## Delegation"))
    return [r for r in rows if not r.startswith("| Intent ")]


def _row_for(table_key: str) -> str:
    rows = [r for r in _delegation_rows() if table_key in r]
    assert len(rows) == 1, f"expected exactly one delegation row for {table_key}, got {len(rows)}"
    return rows[0]


def test_c01_template_declares_the_argument_grammar():
    """C-01: the frontmatter `argument-hint` is exactly [[STR-001]]."""
    hint = None
    for line in _frontmatter(_read(TEMPLATE)):
        if line.strip().startswith("argument-hint:"):
            hint = line.split(":", 1)[1].strip()
    assert hint is not None, "templates/commands/agents.md lacks the argument-hint key"
    assert hint == f'"{STR_001}"', f"argument-hint is {hint!r}, expected the verbatim {STR_001!r}"


def test_c02_three_skill_rows_and_run_row_carries_the_explicit_form():
    """C-02: exactly the three skill rows remain; the run row keeps its explicit input."""
    rows = _delegation_rows()
    assert len(rows) == 3, f"delegation table must have exactly three data rows, got {len(rows)}"
    for verb, path in SKILL_PATHS.items():
        holders = [r for r in rows if path in r]
        assert len(holders) == 1, f"expected one {verb} row for {path}, got {len(holders)}"
    run_row = _row_for(SKILL_PATHS["run"])
    assert RUN_SYNTAX in run_row, "the run row's input cell must carry `run <agent-name> [task]`"
    assert "AgentAuthoringRequest" in _row_for(SKILL_PATHS["create"]), (
        "the create row's input description was changed"
    )
    assert "Targeted, evidence-based edits" in _row_for(SKILL_PATHS["refine"]), (
        "the refine row's output description was changed"
    )


def test_c03_explicit_verb_priority_team_redirect_and_ambiguity():
    """C-03: explicit verb wins; team intent is redirected, never served; ambiguity is three-way."""
    raw = _read(TEMPLATE)
    text = _norm(raw)
    section = _norm(_section(raw, "## Delegation"))
    assert "explicit leading verb" in section, "explicit-verb priority is not stated"
    assert "wins over context inference" in section, "explicit-verb priority lacks its comparison"
    assert "MUST NOT be served by this command" in section, "team intent is not refused here"
    assert "`/speckit.team`" in section, "the team redirect target is missing"
    assert "three capabilities (create / refine / run)" in text, (
        "the ambiguity report does not name the three capabilities"
    )
    assert "requests the missing intent" in text, "the ambiguity report does not request the intent"
    assert "without executing any mode" in text, "ambiguity must not execute a mode while asking"


def test_c04_explicit_run_without_agent_name_stops_at_the_command():
    """C-04: [[STR-003]] + three capabilities + usage; no inference, no listing fallback."""
    text = _norm(_read(TEMPLATE))
    assert STR_003 in text, "the missing-agent-name string is absent from the template"
    assert "three capabilities (create / refine / run)" in text
    assert "usage" in text.lower(), "the missing-name stop must show the usage line"
    assert "dispatches nothing" in text, "the missing-name path is not a zero-dispatch stop"
    assert "MUST NOT infer an agent from conversation context" in text
    assert "MUST NOT fall into the no-argument listing behaviour" in text


def test_c05_no_argument_behaviour_is_unchanged():
    """C-05: empty input keeps the skill-owned list + suggestions + capability summary."""
    template = _norm(_read(TEMPLATE))
    assert "Default Behavior (No Arguments)" in template
    assert "If empty" in template
    body = _norm(_section(_read(SKILL), "### Default Behavior (No Arguments)"))
    assert "List all existing agents" in body
    assert "contextual suggestions" in body
    assert "capability summary" in body
    assert "three modes (create / refine / run)" in body


def test_c06_the_three_syntax_faces_agree_verbatim():
    """C-06: template hint, skill input contract and docs Syntax block carry [[STR-001]]."""
    template_hint = [line for line in _frontmatter(_read(TEMPLATE))
                     if line.strip().startswith("argument-hint:")]
    assert template_hint and STR_001 in template_hint[0], "template face lacks [[STR-001]]"

    skill_input = _norm(_section(_read(SKILL), "## Input Contract"))
    assert STR_001 in skill_input, "skill input contract lacks [[STR-001]]"
    assert RUN_SYNTAX in skill_input, "skill input contract lacks the run-specific form"

    docs_syntax = _norm(_section(_read(DOCS), "## Syntax"))
    assert STR_001 in docs_syntax, "docs Syntax block lacks [[STR-001]]"
    assert f"/speckit.agents {RUN_SYNTAX}" in docs_syntax, (
        "docs Syntax block lacks the explicit /speckit.agents run line"
    )


def test_c07_skill_owns_the_missing_task_stop():
    """C-07: `run <agent-name>` without task presents the agent, reports [[STR-004]], asks."""
    body = _norm(_section(_read(SKILL), "## Input Contract"))
    assert STR_004 in body, "the missing-task string is absent from the skill input contract"
    assert "presents the resolved agent" in body, "the resolved agent is not presented"
    assert "name, layer, description" in body, "the presentation omits the resolution fields"
    assert "requests the task" in body, "the stop does not ask for the task"
    assert "MUST NOT dispatch an empty task brief" in body
    assert "MUST NOT fall into the no-argument listing behaviour" in body


def test_c08_routing_sample_set_proxies():
    """C-08: the seven sample inputs each resolve to their deterministic proxy."""
    template = _norm(_read(TEMPLATE))
    run_row = _row_for(SKILL_PATHS["run"])
    create_row = _row_for(SKILL_PATHS["create"])
    refine_row = _row_for(SKILL_PATHS["refine"])

    # 1 explicit run → run row + run-agent path
    assert re.search(r"\brun\b", run_row, re.IGNORECASE) and "run-agent" in run_row
    # 2 natural-language run (运行 / 执行 / run) → the run row's intent text
    assert re.search(r"运行|执行|run", run_row), "the run row lacks its run-intent text"
    # 3 create → create-agent row
    assert "create-agent" in create_row and re.search(r"\bcreate\b", create_row, re.IGNORECASE)
    # 4 refine → improve-agent row
    assert "improve-agent" in refine_row and re.search(r"\brefine\b", refine_row, re.IGNORECASE)
    # 5 team intent → the redirect sentence, and the run row claims no orchestration
    assert "`/speckit.team`" in template, "the team redirect target is missing"
    assert not re.search(r"parallel|serial|iteration|multiple agents|team", run_row, re.IGNORECASE), (
        "the run row claims multi-agent orchestration"
    )
    # 6 empty input → the skill-owned no-argument behaviour
    assert "If empty" in template and "Default Behavior (No Arguments)" in template
    # 7 ambiguous → the three capabilities
    assert "three capabilities (create / refine / run)" in template
    assert "requests the missing intent" in template


def test_c09_per_tool_copies_are_generated_and_carry_the_run_form():
    """C-09: the four generated copies contain the run row; the generator reports no drift."""
    for copy in COPIES:
        assert copy.is_file(), f"generated copy missing: {copy}"
        assert RUN_SYNTAX in _read(copy), f"{copy.name} lacks the explicit run form"
    result = subprocess.run(
        [sys.executable, "scripts/python/regen-command-copies.py", "--check"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        "the generated copies drifted from the template (regenerate, never hand-edit):\n"
        + (result.stdout + result.stderr)[-800:]
    )


def test_c10_three_error_paths_stop_with_zero_dispatches():
    """C-10: each shared error string sits in its owning surface and names a stop."""
    template = _norm(_read(TEMPLATE))
    skill_input = _norm(_section(_read(SKILL), "## Input Contract"))
    assert STR_002 in skill_input, "[[STR-002]] must sit in the skill input contract"
    assert "no dispatch" in skill_input, "the not-found path is not stated as a no-dispatch stop"
    assert STR_003 in template, "[[STR-003]] must sit in the template"
    assert "dispatches nothing" in template, "the missing-name path is not a zero-dispatch stop"
    assert STR_004 in skill_input, "[[STR-004]] must sit in the skill input contract"
    assert "MUST NOT dispatch an empty task brief" in skill_input, (
        "the missing-task path is not stated as a no-dispatch stop"
    )
