"""Contract tests for tool definition creation (defineNewTool), tool type validation,
and behavioral rules format — T011, T012, T013."""

from tests.script_api import tools_utils

ToolRecord = tools_utils.ToolRecord
BehavioralRule = tools_utils.BehavioralRule
DiscoveryDraft = tools_utils.DiscoveryDraft


def test_define_tool_with_all_mandatory_fields_produces_valid_record():
    record = ToolRecord(
        name="build-docs",
        tool_type="project-script",
        source_identifier="scripts/bash/build-docs.sh",
        description="Builds project documentation from markdown sources",
    )
    errors = record.validate_strict()
    assert not errors


def test_define_tool_missing_name_returns_422():
    record = ToolRecord(
        name="",
        tool_type="project-script",
        source_identifier="scripts/bash/build-docs.sh",
        description="Builds docs",
    )
    errors = record.validate_strict()
    assert any("name is required" in e for e in errors)


def test_define_tool_missing_description_returns_422():
    record = ToolRecord(
        name="build-docs",
        tool_type="project-script",
        source_identifier="scripts/bash/build-docs.sh",
        description="",
    )
    errors = record.validate_strict()
    assert any("description is required" in e for e in errors)


def test_define_tool_missing_source_identifier_returns_422():
    record = ToolRecord(
        name="build-docs",
        tool_type="project-script",
        source_identifier="",
        description="Builds docs",
    )
    errors = record.validate_strict()
    assert any("source_identifier is required" in e for e in errors)


def test_tool_type_accepts_only_canonical_values():
    for valid_type in ("project-script", "system-binary", "shell-function", "webhook"):
        record = ToolRecord(
            name="test-tool",
            tool_type=valid_type,
            source_identifier="/usr/bin/test",
            description="Test tool",
        )
        errors = record.validate_strict()
        assert not errors, f"Unexpected errors for type {valid_type}: {errors}"


def test_tool_type_rejects_legacy_values():
    for legacy_type in ("mcp", "system", "shell", "project"):
        record = ToolRecord(
            name="test-tool",
            tool_type=legacy_type,
            source_identifier="/usr/bin/test",
            description="Test tool",
        )
        errors = record.validate_strict()
        assert any("tool_type" in e for e in errors), (
            f"Expected rejection of legacy type '{legacy_type}'"
        )


def test_behavioral_rule_requires_valid_keyword():
    rule = BehavioralRule(keyword="MUST", constraint_text="run from repo root")
    assert not rule.validate()

    rule_invalid = BehavioralRule(keyword="COULD", constraint_text="run from repo root")
    errors = rule_invalid.validate()
    assert any("keyword" in e for e in errors)


def test_behavioral_rule_requires_nonempty_constraint():
    rule = BehavioralRule(keyword="MUST", constraint_text="")
    errors = rule.validate()
    assert any("constraint_text" in e for e in errors)


def test_behavioral_rule_keywords_all_accepted():
    for kw in ("MUST", "MUST NOT", "SHOULD", "SHOULD NOT"):
        rule = BehavioralRule(keyword=kw, constraint_text="do something")
        assert not rule.validate(), f"Keyword '{kw}' should be accepted"


def test_behavioral_rule_markdown_roundtrip():
    rule = BehavioralRule(keyword="MUST NOT", constraint_text="modify source files")
    markdown = rule.to_markdown()
    assert markdown == "- MUST NOT modify source files"

    parsed = BehavioralRule.from_markdown(markdown)
    assert parsed is not None
    assert parsed.keyword == "MUST NOT"
    assert parsed.constraint_text == "modify source files"


def test_record_with_invalid_behavioral_rule_reports_errors():
    record = ToolRecord(
        name="test-tool",
        tool_type="project-script",
        source_identifier="scripts/test.sh",
        description="Test",
        behavioral_rules=[BehavioralRule(keyword="INVALID", constraint_text="something")],
    )
    errors = record.validate_strict()
    assert any("keyword" in e for e in errors)


def test_define_tool_conflict_same_name():
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tools_dir = Path(tmpdir)
        record1 = ToolRecord(
            name="deploy",
            tool_type="project-script",
            source_identifier="scripts/deploy.sh",
            description="Deploy the project",
        )
        tools_utils.save_record(tools_dir, record1)
        assert (tools_dir / "deploy.md").exists()

        record2 = ToolRecord(
            name="deploy",
            tool_type="system-binary",
            source_identifier="/usr/bin/deploy",
            description="System deploy command",
        )
        tools_utils.save_record(tools_dir, record2)
        loaded = tools_utils.load_record(tools_dir, "deploy")
        assert loaded is not None
