"""Contract test: the four wiring surfaces (102, US3 + US4).

Pins ``.specify/specs/102-line-registry-registration/contracts/wiring-surfaces.contract.md``.

**Segment 1 (this file today)** — C-01…C-09: the owner document gains the criterion and owns
its threshold; the three downstream surfaces (``templates/commands/status.md``,
``templates/instructions-template.md``, ``.specify/instructions.md`` and its four symlinks)
carry only a pointer and never restate the threshold or the mechanical marker literals.

**Segment 2 (appended by US4, T039)** — C-10…C-13: the run-team skill's §5/§6/§7 steps.

The owner document is the single place allowed to state the threshold and the digest
invariant; the downstream restatement assertions are therefore scoped to the three downstream
surfaces only (never to the owner). The verbatim sentences come from contract C-05 and C-07 —
this file is their red leg.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"
STATUS = REPO_ROOT / "templates" / "commands" / "status.md"
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE = REPO_ROOT / ".specify" / "instructions.md"
LINKS = ("AGENTS.md", "CLAUDE.md", "QODER.md", ".github/copilot-instructions.md")

CARRIER = "scripts/bash/line-run.sh"
ENGINE = "line-registry.py"
NOTHING_RUNNING = "nothing-running"
THRESHOLD = "5 分钟"
MECHANICAL_MEMBERS = ("terraform apply", "run-tests.sh --full", "# line-run-required")

OWNER_HEADING = "## 九"

SINGLE_SOURCE_SENTENCE = (
    "**Single source**: line visibility comes solely from the Line Registry — the digest's "
    "liveness probe is limited to PIDs already recorded on a registry entry and never "
    "discovers an unregistered process, so it MUST NOT be changed to discover unregistered "
    "processes; the obligation is owned by `shared/guidelines/reporting-obligations.md` § 九 "
    "and is reached by path, never restated here."
)

AMBIENT_BULLET = (
    "- **Long tasks must register a line (长任务须登记)**: a long-running task that registers "
    "no line is invisible to `/speckit.status`, so wrap it with `scripts/bash/line-run.sh`; "
    "the criterion and its bounds are owned by `shared/guidelines/reporting-obligations.md` § 九."
)

EXEMPTIONS_PREFIX = "- **Exemptions and precedence"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing surface: {path}"
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    """Return the level-2 section whose heading starts with ``heading_prefix``."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(heading_prefix):
            start = index
            break
    assert start is not None, f"section heading {heading_prefix!r} not found"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def _action_set(text: str) -> set:
    """The command's own action set, read from the authored body.

    The ``## Wrap-up`` block is machine-generated (probe-utils) and names the
    probe engine's actions, which are not this command's actions; scanning them
    would compare an unrelated closed set (C-06 speaks of the status command).
    """
    authored = text.split("\n## Wrap-up", 1)[0]
    return set(re.findall(r"--action\s+([a-z][a-z-]*)", authored))


# ------------------------------------------------------------------ C-01…C-04 owner document
def test_c01_c03_the_owner_section_states_the_criterion_and_its_boundary():
    section = _section(_read(OWNER), OWNER_HEADING)
    assert "登记" in section, "the section must require registering a line"
    assert "关闭" in section, "the section must require closing the line at the end"
    assert THRESHOLD in section, (
        f"the owner MUST state and own the threshold ({THRESHOLD!r}); downstream surfaces "
        "may not carry it instead"
    )
    assert NOTHING_RUNNING in section, (
        "the section must name the empty-set rendering it declares to be accurate"
    )


def test_c01_the_owner_names_the_carrier_and_the_registry_writer():
    section = _section(_read(OWNER), OWNER_HEADING)
    assert CARRIER in section, f"the criterion must name its carrier {CARRIER!r}"
    assert ENGINE in section, f"the registry writer must be named as {ENGINE!r}"


def test_c03_the_owner_states_the_digest_invariant():
    section = _section(_read(OWNER), OWNER_HEADING)
    assert "唯一来源" in section, "the owner must state that the registry is the sole source"
    assert "PID" in section, (
        "the owner must state that any liveness probe is limited to PIDs already recorded "
        "on a registry entry"
    )
    assert "未登记进程" in section, (
        "the owner must state that no unregistered process is ever discovered"
    )


def test_c03_the_owner_does_not_restate_the_mechanical_marker_members():
    """A-15: the criterion constants are the owner of the members; § 九 reaches them by path."""
    section = _section(_read(OWNER), OWNER_HEADING)
    for member in MECHANICAL_MEMBERS:
        assert member not in section, (
            f"the owner section restates the mechanical member {member!r}; the scanner "
            "constants are its single owner (A-15)"
        )


# ------------------------------------------------- C-05 / C-06 status command template
def test_c05_the_status_template_carries_the_single_source_sentence_verbatim():
    text = _read(STATUS)
    assert text.count(SINGLE_SOURCE_SENTENCE) == 1, (
        "templates/commands/status.md must contain the C-05 sentence exactly once"
    )


def test_c06_the_status_template_keeps_its_action_set_and_adds_no_second_surface():
    text = _read(STATUS)
    assert _action_set(text) == {"digest", "guard", "report"}, (
        f"the action set must stay the closed three, got {sorted(_action_set(text))}"
    )
    assert THRESHOLD not in text, "the status template must not restate the owner's threshold"
    for member in MECHANICAL_MEMBERS:
        assert member not in text, (
            f"the status template must not restate the mechanical member {member!r}"
        )
    assert "Single source" in text, "the C-05 sentence is the only permitted addition"


# ---------------------------------------------------------- C-07 / C-08 ambient bullet
def test_c07_the_template_has_exactly_one_pointer_bullet_after_exemptions():
    section = _section(_read(TEMPLATE), "## Progress Reporting Discipline")
    lines = section.splitlines()
    positions = [index for index, line in enumerate(lines) if line.startswith(EXEMPTIONS_PREFIX)]
    assert len(positions) == 1, "expected exactly one Exemptions and precedence bullet"
    anchor = positions[0]
    assert anchor + 1 < len(lines), "no line follows the Exemptions bullet"
    assert lines[anchor + 1] == AMBIENT_BULLET, (
        "the pointer bullet must land immediately after the Exemptions bullet, verbatim "
        "(C-07)"
    )
    assert section.count(AMBIENT_BULLET) == 1, "exactly one pointer bullet is permitted"
    assert section.count(CARRIER) == 1, (
        "the carrier appears once, inside the pointer bullet; no other restatement"
    )


def test_c08_the_ambient_bullet_does_not_restate_the_criterion():
    section = _section(_read(TEMPLATE), "## Progress Reporting Discipline")
    assert THRESHOLD not in section, "the ambient section must not restate the threshold"
    for member in MECHANICAL_MEMBERS:
        assert member not in section, (
            f"the ambient section must not restate the mechanical member {member!r}"
        )


# ------------------------------------------------------ C-09 live file and its symlinks
def test_c09_the_live_instructions_carry_the_bullet_once_and_the_links_resolve():
    live = _read(LIVE)
    section = _section(live, "## Progress Reporting Discipline")
    assert section.count(AMBIENT_BULLET) == 1, (
        ".specify/instructions.md must carry the pointer bullet exactly once (via the "
        "section-level refresh, never a hand edit)"
    )
    live_real = os.path.realpath(LIVE)
    for name in LINKS:
        link = REPO_ROOT / name
        assert link.is_symlink(), f"{name} must remain a symlink"
        assert os.path.realpath(link) == live_real, f"{name} must resolve to {LIVE}"
        assert link.read_text(encoding="utf-8").count(AMBIENT_BULLET) == 1, (
            f"{name} must show the bullet through the live file"
        )


# ======================================================================
# Segment 2 — C-10…C-13: the run-team skill's §5 / §6 / §7 steps (US4)
# ======================================================================
RUN_TEAM = REPO_ROOT / "skills" / "internal" / "run-team" / "SKILL.md"
CREATE_TEAM = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"

ENGINE_CANDIDATES = (
    "skills/external/sdd-loop-driver/scripts/line-registry.py",
    ".specify/skills/sdd-loop-driver/scripts/line-registry.py",
)

#: Engine options that a restated parameter table would enumerate (C-13).
ENGINE_OPTIONS = (
    "--action",
    "--line-id",
    "--run-id",
    "--last-event",
    "--state",
    "--reason",
    "--project-dir",
    "--repo-root",
)


def _subsection(text: str, heading_prefix: str) -> str:
    """Return the subsection whose heading starts with ``heading_prefix``."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(heading_prefix):
            start = index
            break
    assert start is not None, f"subsection heading {heading_prefix!r} not found"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    return "\n".join(lines[start:end])


# ---------------------------------------------------------------------------- C-10 §5 register
def test_c10_section_5_registers_the_line_at_both_engine_candidates():
    body = _subsection(_read(RUN_TEAM), "### 5.")
    for candidate in ENGINE_CANDIDATES:
        assert candidate in body, (
            f"§5 must name the A-17 engine candidate {candidate!r} (framework source first, "
            "then the downstream-only copy)"
        )
    assert "register" in body, "§5 must register the run's line through the engine's register action"
    assert "<team-slug>-<run-id>" in body, (
        "§5 must compose the registry id as <team-slug>-<run-id> (A-18)"
    )
    assert "RUN_ID_RE" in body, (
        "§5 must generate the run id in the engine-valid form and point at RUN_ID_RE, never a "
        "bare UTC timestamp (A-18)"
    )
    assert "--help" in body, (
        "§5 must read the engine's actions, parameters and exit codes from its --help rather "
        "than restating them (C-10)"
    )


def test_c10_section_5_fails_closed_before_dispatching_any_seat():
    body = _subsection(_read(RUN_TEAM), "### 5.")
    fail_closed = ("fail-closed" in body) or ("fail closed" in body) or ("登记失败" in body)
    assert fail_closed, "§5 must fail closed when the registration fails (C-10)"
    assert "派发" in body or "dispatch" in body, (
        "§5 must place the registration before any seat is dispatched"
    )


# ----------------------------------------------------------------- C-11 §6 step-boundary update
def test_c11_section_6_refreshes_at_each_step_boundary_with_no_second_channel():
    body = _subsection(_read(RUN_TEAM), "### 6.")
    assert "update" in body, "§6 must refresh the line through the engine's update action"
    assert "--last-event" in body, (
        "§6 must carry the step label as the refreshed last event at each orchestration step "
        "boundary (C-11)"
    )
    assert "定时器" in body, "§6 must state that no timer exists"
    assert "守护" in body, "§6 must state that no daemon exists"
    assert "第二" in body, "§6 must state that no second liveness channel exists"


# ------------------------------------------------------------------------ C-12 §7 close+line_id
def test_c12_section_7_closes_before_the_report_and_carries_the_line_id():
    body = _subsection(_read(RUN_TEAM), "### 7.")
    assert "deregister" in body, "§7 must close the run's line through the engine (C-12)"
    assert "line_id" in body, (
        "§7 must require the composed line_id to appear in the report body (C-12, STR-007)"
    )
    assert "关闭失败" in body or "close failure" in body, (
        "§7 must name a close failure as an outcome it handles"
    )
    assert "写明" in body or "stated" in body, (
        "§7 must require a close failure to be stated in the report, never swallowed"
    )


# -------------------------------------------------------------------- C-13 no leak, no option table
def test_c13_the_create_team_report_contract_is_not_touched():
    text = _read(CREATE_TEAM)
    report = _subsection(text, "### Report contract")
    assert "line_id" not in report, (
        "the Report contract belongs to create-team; the line_id obligation is carried by "
        "run-team §7 (C-13)"
    )
    assert "line-registry.py" not in report, (
        "the create-team Report contract must not reach for the registry engine (C-13)"
    )


def test_c13_the_skill_carries_no_engine_parameter_table():
    text = _read(RUN_TEAM)
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        named = [option for option in ENGINE_OPTIONS if option in line]
        assert len(named) < 2, (
            f"{RUN_TEAM}:{number} enumerates engine options {named}; §5/§6/§7 must read the "
            "engine's parameters from --help, not restate a table (C-13)"
        )
