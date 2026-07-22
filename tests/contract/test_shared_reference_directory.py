"""Contract tests for the shared reference directory packaging + core-asset retention.

Feature 029, contract C-INSTALL.
"""

from pathlib import Path

import specify_cli

ROOT = Path(__file__).resolve().parents[2]

TYPED_DOCS = {
    "workflow": {
        "user-input-protocol.md",
        "feature-integration.md",
        "agent-configuration.md",
        "feedback-step.md",
    },
    "guidelines": {
        "checklist-methodology.md",
        "requirements-guidelines.md",
    },
    "constants": {
        "clarify-taxonomy.md",
        "dfx-catalog.md",
        "ignore-patterns.md",
    },
    "definitions": {
        "tool-definitions.md",
    },
    "patterns": {
        "reconcile-pattern.md",
    },
}


def test_shared_source_dirs_have_typed_docs():
    for subdir, expected in TYPED_DOCS.items():
        typed_dir = ROOT / "shared" / subdir
        assert typed_dir.is_dir(), f"shared/{subdir}/ must exist"
        present = {p.name for p in typed_dir.glob("*.md")}
        assert expected.issubset(present), f"shared/{subdir}/ missing: {sorted(expected - present)}"


def test_pyproject_force_includes_shared():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"shared" = "specify_cli/shared"' in text


def test_shared_is_a_retained_core_asset():
    assert ".specify/shared" in specify_cli._CORE_SPECIFY_ASSETS
