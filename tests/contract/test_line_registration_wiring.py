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
    return set(re.findall(r"--action\s+([a-z][a-z-]*)", text))


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
