"""Contract test: agent-surface docs (contracts/teaching-and-guards.md C-5..C-8).

The host-registration-surface concept lands once in agent-definitions.md
(owner); symlink-model.md and supported-agent-tools.md carry their additions
as pointers, with the verified IDE/CLI provenance pinned.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_DEFINITIONS = REPO_ROOT / "shared" / "definitions" / "agent-definitions.md"
SYMLINK_MODEL = REPO_ROOT / "shared" / "workflow" / "symlink-model.md"
SUPPORTED_TOOLS = REPO_ROOT / "docs" / "reference" / "cli" / "supported-agent-tools.md"

PROVENANCE_URLS = (
    "https://docs.qoder.com/extensions/subagent",
    "https://docs.qoder.com/cli/subagent",
)


def test_c5_host_registration_surface_defined_once_in_owner():
    text = AGENT_DEFINITIONS.read_text(encoding="utf-8")
    assert "Host Registration Surface" in text
    # C-8 pointer discipline: the section heading appears exactly once
    assert text.count("## Host Registration Surface") == 1


def test_c5_seat_instance_taxonomy_entry():
    text = AGENT_DEFINITIONS.read_text(encoding="utf-8")
    assert "Seat Instance" in text
    assert "team-scope" in text


def test_c6_symlink_model_agent_surface_entry_with_provenance():
    text = SYMLINK_MODEL.read_text(encoding="utf-8")
    for url in PROVENANCE_URLS:
        assert url in text
    assert "2026-10-08" in text
    # pointer, not restatement
    assert "agent-definitions.md" in text


def test_c7_supported_tools_qoder_agent_surface():
    text = SUPPORTED_TOOLS.read_text(encoding="utf-8")
    assert ".qoder/agents" in text
    assert "frontmatter" in text
    assert "~/.qoder/agents" in text


def test_c8_pointer_discipline_no_restatement():
    sym = SYMLINK_MODEL.read_text(encoding="utf-8")
    sup = SUPPORTED_TOOLS.read_text(encoding="utf-8")
    # the concept definition section lives only in the owner
    assert "## Host Registration Surface" not in sym
    assert "## Host Registration Surface" not in sup
    # both reference the owner
    assert "agent-definitions.md" in sym
    assert "agent-definitions.md" in sup
