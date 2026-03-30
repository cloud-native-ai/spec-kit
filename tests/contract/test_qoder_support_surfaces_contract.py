from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".specify" / "specs" / "006-add-qoder-support" / "contracts" / "qoder-support.openapi.yaml"


def test_support_surface_audit_contract_exists_for_qoder():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "/audits/qoder-support:" in content
    assert "SupportAuditResult" in content


def test_support_surface_contract_marks_qoder_key():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "assistantKey" in content
    assert "enum: [qoder]" in content
