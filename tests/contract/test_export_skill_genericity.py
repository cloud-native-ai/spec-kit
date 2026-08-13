"""Contract tests for archive-session genericity (039-session-export, T009).

Contract: .specify/specs/039-session-export/contracts/export-skill-rework.contract.md §1/§4

Pins the generalization surface on BOTH skill files: no platform-specific
dependency residue (aone-open usage reporting, x-source marker, outbound
URLs), the support matrix table holding exactly the six normative tools, and
the removed six products leaving zero residue in SKILL.md as well as the
engine (the engine-only residue pin lives in test_export_skill_rework.py).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "skills/archive-session/scripts/export.py"
SKILL = REPO_ROOT / "skills/archive-session/SKILL.md"

pytestmark = pytest.mark.contract

SIX_TOOLS = ["claude-code", "codex-cli", "qoder-cli", "copilot", "opencode", "hermes"]

#: Removed products — identifier-level markers, zero residue in BOTH files.
REMOVED_MARKERS = [
    "qwen-code", "qwen_", "_qwen_", "qoderwork", "oh-my-pi", "_omp_root",
    "kimi-code", "kimi_", "_kimi_", "codex-app", "codexapp",
]

#: Platform-specific dependency markers (aone-open lineage).
PLATFORM_MARKERS = ["a1 skill report", "x-source", "aone-open", "aone_open"]


@pytest.mark.parametrize("marker", PLATFORM_MARKERS)
def test_no_platform_specific_dependency_residue(marker):
    for path in (SKILL, ENGINE):
        text = path.read_text(encoding="utf-8")
        assert marker not in text, f"platform dependency {marker!r} in {path.name}"


def test_no_outbound_network_calls():
    for path in (SKILL, ENGINE):
        text = path.read_text(encoding="utf-8")
        assert "http://" not in text and "https://" not in text, (
            f"outbound URL in {path.name} — the skill must be network-free"
        )


@pytest.mark.parametrize("marker", REMOVED_MARKERS)
def test_removed_products_leave_zero_residue_in_skill(marker):
    for path in (SKILL, ENGINE):
        text = path.read_text(encoding="utf-8")
        assert marker not in text, f"{marker!r} residue in {path.name}"


def test_support_matrix_is_exactly_the_six_tools():
    text = SKILL.read_text(encoding="utf-8")
    for tool in SIX_TOOLS:
        assert f"`{tool}`" in text, f"matrix row missing for {tool}"
    # removed tool names must not appear even as prose
    for legacy in ("qwen", "kimi", "oh-my-pi", "qoderwork"):
        assert legacy not in text.lower(), f"legacy tool {legacy!r} mentioned in SKILL.md"


def test_skill_describes_the_directory_product_shape():
    text = SKILL.read_text(encoding="utf-8")
    assert "SESSION.md" in text, "description doc flow must be documented"
    assert "session-meta.json" in text, "meta output must be documented"
    assert ".session-export" in text, "export root must be documented"


def test_skill_documents_the_name_argument_and_exit_codes():
    text = SKILL.read_text(encoding="utf-8")
    assert "--name" in text
    for code in ("0", "2", "3", "4", "5"):
        assert f"| {code} |" in text, f"exit-code row missing: {code}"
