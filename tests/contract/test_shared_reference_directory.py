"""Contract tests for the shared reference directory packaging + core-asset retention.

Feature 029, contract C-INSTALL.
"""

from pathlib import Path

import specify_cli

ROOT = Path(__file__).resolve().parents[2]

TEN_DOCS = {
    "user-input-protocol.md",
    "feature-integration.md",
    "agent-configuration.md",
    "checklist-methodology.md",
    "requirements-guidelines.md",
    "dfx-catalog.md",
    "clarify-taxonomy.md",
    "ignore-patterns.md",
    "tool-definitions.md",
    "feedback-step.md",
}


def test_shared_source_dir_has_ten_docs():
    shared = ROOT / "shared" / "workflow"
    assert shared.is_dir()
    present = {p.name for p in shared.glob("*.md")}
    assert TEN_DOCS.issubset(present)


def test_pyproject_force_includes_shared():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"shared" = "specify_cli/shared"' in text


def test_shared_is_a_retained_core_asset():
    assert ".specify/shared" in specify_cli._CORE_SPECIFY_ASSETS
