from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / ".specify"
    / "specs"
    / "009-claude-code-support"
    / "contracts"
    / "claude-code-support.openapi.yaml"
)


def test_init_contract_lists_claude_as_supported_assistant():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "enum: [copilot, qwen, opencode, qoder, claude]" in content
    assert "/projects/init:" in content


def test_init_contract_defines_claude_project_assets():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "generatedAssets" in content
    assert "commandCoverage" in content
    assert "ignorePolicyStatus" in content
