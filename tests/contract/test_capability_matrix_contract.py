"""Contract test for capability matrix audit (T030).

Asserts audit_capability_matrix returns entries for 6 tools x 6 dimensions.
"""

import pytest

from pathlib import Path

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    _ASSISTANT_TIERS,
    _CAPABILITY_DIMENSIONS,
    audit_capability_matrix,
    copy_local_templates,
)

pytestmark = pytest.mark.contract


def test_audit_returns_correct_entry_count(tmp_path: Path):
    project = tmp_path / "audit_project"
    project.mkdir()
    result = audit_capability_matrix(project)
    expected_count = len(_OFFICIAL_ASSISTANT_KEYS) * len(_CAPABILITY_DIMENSIONS)
    assert len(result["entries"]) == expected_count


def test_audit_summary_has_tier_rates(tmp_path: Path):
    project = tmp_path / "audit_project"
    project.mkdir()
    result = audit_capability_matrix(project)
    assert "tier1_pass_rate" in result["summary"]
    assert "tier2_pass_rate" in result["summary"]


def test_audit_entries_have_required_fields(tmp_path: Path):
    project = tmp_path / "audit_project"
    project.mkdir()
    result = audit_capability_matrix(project)
    for entry in result["entries"]:
        assert "tool_key" in entry
        assert "dimension" in entry
        assert "status" in entry
        assert entry["status"] in ("pass", "fail", "missing")


def test_audit_initialized_project_has_some_passes(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )
    project = tmp_path / "initialized"
    copy_local_templates(project, "codex", "sh")

    result = audit_capability_matrix(project)
    pass_entries = [e for e in result["entries"] if e["status"] == "pass"]
    assert len(pass_entries) > 0
