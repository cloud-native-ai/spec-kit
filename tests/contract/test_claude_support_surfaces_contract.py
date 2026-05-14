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


def test_support_surface_audit_contract_exists_for_claude():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "/audits/claude-code-support:" in content
    assert "SupportAuditResult" in content


def test_support_surface_contract_marks_claude_key():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "assistantKey" in content
    assert "enum: [claude]" in content
    assert "/assistants/claude/commands/coverage:" in content
