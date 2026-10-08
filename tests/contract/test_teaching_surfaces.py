"""Contract test: teaching surfaces teach the real render model
(contracts/teaching-and-guards.md C-1..C-4, contracts/seat-instantiation.md C-3).

Three surfaces must stop teaching the retired per-file symlink model and teach
the real one (renderer-produced real files, `specify render-agents` trigger),
with the retired literals pinned absent so a regression goes red.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

# C-4 pin ①: the retired STR-001 literal (spec Shared Strings table)
RETIRED_SYMLINK_SENTENCE = (
    "Tool-specific directories are symlinks"
)
# C-4 pin ②: SKILL.md-specific retired wording (two distinct phrases)
RETIRED_SKILL_PHRASES = (
    "Per-file symlinked into every officially supported tool's agent config directory",
    "recreates a **per-file** symlink for each",
)

AGENTS_COMMAND_COPIES = [
    REPO_ROOT / "templates" / "commands" / "agents.md",
    REPO_ROOT / ".claude" / "commands" / "speckit.agents.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.agents.prompt.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.agents.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.agents.md",
]

SKILL_COPIES = [
    REPO_ROOT / "skills" / "create-agent" / "SKILL.md",
    REPO_ROOT / ".specify" / "skills" / "create-agent" / "SKILL.md",
]


@pytest.mark.parametrize("copy", AGENTS_COMMAND_COPIES, ids=lambda p: p.name)
def test_c4_retired_symlink_sentence_absent(copy):
    assert copy.is_file(), copy
    assert RETIRED_SYMLINK_SENTENCE not in copy.read_text(encoding="utf-8")


@pytest.mark.parametrize("copy", SKILL_COPIES, ids=lambda p: str(p))
def test_c4_skill_retired_phrases_absent(copy):
    assert copy.is_file(), copy
    text = copy.read_text(encoding="utf-8")
    for phrase in RETIRED_SKILL_PHRASES:
        assert phrase not in text, phrase


def test_c3_trigger_truth_taught_in_agents_command():
    text = (REPO_ROOT / "templates" / "commands" / "agents.md").read_text(encoding="utf-8")
    assert "specify render-agents" in text


def test_c3_trigger_truth_taught_in_create_agent_skill():
    text = (REPO_ROOT / "skills" / "create-agent" / "SKILL.md").read_text(encoding="utf-8")
    assert "specify render-agents" in text


def test_seat_c3_team_scope_key_listed_in_authoring_keys():
    text = (REPO_ROOT / "skills" / "create-agent" / "SKILL.md").read_text(encoding="utf-8")
    assert "team-scope" in text


def test_c1_real_model_taught_in_agents_command():
    text = (REPO_ROOT / "templates" / "commands" / "agents.md").read_text(encoding="utf-8")
    # pin the distinctive fragment of the replacement teaching (C-1)
    assert "renderer-produced real files" in text
