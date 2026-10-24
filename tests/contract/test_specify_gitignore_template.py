"""Contract test: the framework ships a scoped .specify/.gitignore template.

`templates/gitignore-specify-template` is the source of truth copied into every
target project's `.specify/.gitignore` during init. It must exist and use
`.specify/`-relative patterns for the transient `.work/` scratch dirs.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "gitignore-specify-template"


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
        "tools/",
        "instructions.md-*",
        "memory/sanitize/",
        "memory/trigger/telemetry.jsonl",
        ".tmp/",
    ):
        assert pattern in body, f"missing .specify-relative rule: {pattern}"
    # Patterns are relative to .specify/, never repo-root-anchored.
    for anchored in (
        ".specify/history/.work/",
        ".specify/teams/.work/",
        ".specify/tools/",
        ".specify/instructions.md-*",
        ".specify/memory/sanitize/",
        ".specify/memory/trigger/telemetry.jsonl",
        ".specify/.tmp/",
    ):
        assert anchored not in body, f"repo-root-anchored rule leaked: {anchored}"
