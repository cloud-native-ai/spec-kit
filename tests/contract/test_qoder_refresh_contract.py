from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".specify" / "specs" / "006-add-qoder-support" / "contracts" / "qoder-support.openapi.yaml"


def test_refresh_contract_contains_validation_and_refresh_endpoints():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "/assistants/qoder/validate:" in content
    assert "/projects/{projectPath}/assistants/qoder/refresh:" in content


def test_refresh_contract_models_ignore_agent_tools_behavior():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "ignoreAgentTools" in content
    assert "enum: [available, missing, ignored]" in content
