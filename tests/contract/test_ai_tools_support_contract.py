"""Contract tests for AI Tools Support Feature (022).

Validates the OpenAPI contract completeness for assistant profiles,
initialization, refresh, preservation, command coverage, and support audits.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / ".specify"
    / "specs"
    / "011-ai-tools-support"
    / "contracts"
    / "ai-tools-support.openapi.yaml"
)

# pytest marker so we can run contract tests selectively
pytestmark = pytest.mark.contract


def _contract_text() -> str:
    return CONTRACT.read_text(encoding="utf-8")


class TestContractFileExists:
    def test_contract_file_is_readable(self):
        assert CONTRACT.exists(), f"Contract file not found at {CONTRACT}"
        assert CONTRACT.is_file(), f"Contract path is not a file: {CONTRACT}"


class TestContractStructure:
    def test_has_openapi_version(self):
        text = _contract_text()
        assert "openapi: 3.1.0" in text or "openapi: 3.0" in text

    def test_has_info_section(self):
        text = _contract_text()
        assert "AI Tools Support" in text

    def test_has_paths(self):
        text = _contract_text()
        assert "/assistants:" in text
        assert "/projects/init:" in text
        assert "projectPath" in text

    def test_has_components_schemas(self):
        text = _contract_text()
        assert "AssistantSupportProfile" in text
        assert "InitializationResultSummary" in text


class TestAssistantSchemas:
    def test_profile_has_required_fields(self):
        text = _contract_text()
        assert "AssistantSupportProfile" in text
        # Check that key schema fields exist in the contract
        assert "key:" in text
        assert "display_name" in text or "displayName" in text
        assert "root_folder" in text or "rootFolder" in text
        assert "officially_supported" in text or "officiallySupported" in text

    def test_result_summary_has_categories(self):
        text = _contract_text()
        assert "InitializationResultSummary" in text
        for cat in [
            "created",
            "reused",
            "skipped",
            "preserved",
            "conflicts",
            "attentionRequired",
            "configuredAssistants",
        ]:
            assert cat in text, f"Missing summary category '{cat}' in contract"

    def test_official_assistant_enum_is_complete(self):
        """Verify all 5 official assistants are referenced in the contract."""
        text = _contract_text()
        for assistant in ["copilot", "claude", "qwen", "opencode", "qoder"]:
            assert assistant in text, f"Assistant '{assistant}' not found in contract"
