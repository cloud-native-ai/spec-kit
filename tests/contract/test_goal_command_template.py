"""Contract tests for the goal/team command templates (FR-030).

Feature 094, tasks row T074, contracts `owner-rewrites-and-tests.md` C-97 / C-98. The goal
template exposes the `migrate-archive` mode (the single command entry for the unified
migration), both templates cite the scope value set by pointer instead of restating it, and
the team template gains no migration mode of its own.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
GOAL_TEMPLATE = REPO_ROOT / "templates/commands/goal.md"
TEAM_TEMPLATE = REPO_ROOT / "templates/commands/team.md"

SCOPE_OWNER = ".specify/shared/definitions/goal-definitions.md"
ARCHIVE_SECTION = "§ Archive Layers"

RESTATED_SCOPE = re.compile(
    r"--scope\s+(?:global|spec)\b|--scope\s+\w+\|\w+|goal\s*\|\s*teams\s*\|\s*auto")


def _read(path: Path) -> str:
    assert path.is_file(), f"command template missing: {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# T074 / C-97 — the goal template exposes `migrate-archive` and cites the scope owner
# ---------------------------------------------------------------------------

def test_the_goal_template_exposes_migrate_archive_and_cites_the_scope_domain():
    text = _read(GOAL_TEMPLATE)

    assert "migrate-archive" in text, (
        "the goal template must expose the `migrate-archive` mode")
    hint = next((line for line in text.splitlines()
                 if line.startswith("argument-hint:")), "")
    assert "migrate-archive" in hint, (
        "`migrate-archive` must appear in the mode hint so the entry is discoverable; "
        f"hint reads: {hint!r}")

    # The scope value set is cited, never restated (C-97, third element).
    assert SCOPE_OWNER in text and ARCHIVE_SECTION in text, (
        "the scope hint must cite the scope value set's owner by path and section")
    restated = [line.strip() for line in text.splitlines() if RESTATED_SCOPE.search(line)]
    assert not restated, f"the goal template restates the scope value set: {restated}"

    # The retired spec-scoped framing is gone from the positioning text.
    assert "spec-scoped" not in text, "the retired spec-scoped goal framing survives"
    assert "spec 级" not in text, "the retired 中文 spec-scoped framing survives"

    # The engine remains the named action owner for flags and paths.
    assert "goal-utils.py" in text, "the engine action owner is not cited"


# ---------------------------------------------------------------------------
# T074 / C-98 — the team template drops the spec hint and gains no migration mode
# ---------------------------------------------------------------------------

def test_the_team_template_drops_the_spec_hint_and_gains_no_migration_mode():
    text = _read(TEAM_TEMPLATE)

    assert "migrate-archive" not in text, (
        "team migration runs inside the goal entry; the team template must not gain a "
        "migration mode of its own")
    assert "<spec-dir>/team" not in text and "<spec-dir>/goal" not in text, (
        "the team template still points at a spec-local goal/team directory")

    assert SCOPE_OWNER in text and ARCHIVE_SECTION in text, (
        "the team template must cite the scope value set's owner by path and section")
    restated = [line.strip() for line in text.splitlines() if RESTATED_SCOPE.search(line)]
    assert not restated, f"the team template restates the scope value set: {restated}"
