"""Contract test: the framework ships a scoped .specify/.gitignore template.

`templates/gitignore-specify-template` is the source of truth copied into every
target project's `.specify/.gitignore` during init. It must exist and use
`.specify/`-relative patterns for the transient `.work/` scratch dirs.

Feature 105 (C-4): the tools rule narrows to the generated inventories only
(`tools/*.json`; records `tools/*.md` stay tracked), and the sanitize / trigger
rules move with the runtime stores to the `.specify/` top level. The template and
the repo's installed copy are one change: they must stay byte-identical.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "gitignore-specify-template"
INSTALLED = REPO_ROOT / ".specify" / ".gitignore"


@pytest.mark.contract
def test_template_exists():
    assert TEMPLATE.is_file(), "templates/gitignore-specify-template must exist"


@pytest.mark.contract
def test_template_uses_specify_relative_patterns():
    body = TEMPLATE.read_text(encoding="utf-8")
    for pattern in (
        "history/.work/",
        "teams/.work/",
        "agents/execution/logs/",
        "tools/*.json",
        "instructions.md-*",
        "sanitize/",
        "trigger/telemetry.jsonl",
        ".tmp/",
        "state/",
    ):
        assert pattern in body, f"missing .specify-relative rule: {pattern}"
    # Patterns are relative to .specify/, never repo-root-anchored.
    for anchored in (
        ".specify/history/.work/",
        ".specify/teams/.work/",
        ".specify/tools/*.json",
        ".specify/instructions.md-*",
        ".specify/sanitize/",
        ".specify/trigger/telemetry.jsonl",
        ".specify/.tmp/",
        ".specify/state/",
    ):
        assert anchored not in body, f"repo-root-anchored rule leaked: {anchored}"


@pytest.mark.contract
def test_retired_whole_directory_and_memory_rules_are_gone():
    body = TEMPLATE.read_text(encoding="utf-8")
    assert "\ntools/\n" not in body, (
        "a whole-directory tools rule would silently drop tracked Tool records (C-4)"
    )
    assert "memory/sanitize/" not in body
    assert "memory/trigger/telemetry.jsonl" not in body


@pytest.mark.contract
def test_installed_copy_is_byte_identical_to_the_template():
    assert INSTALLED.is_file(), "the framework repo ships an installed .specify/.gitignore"
    assert TEMPLATE.read_bytes() == INSTALLED.read_bytes(), (
        "the template and the installed copy must land in the same change, byte-identical (C-4)"
    )
