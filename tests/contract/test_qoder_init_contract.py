from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".specify" / "specs" / "006-add-qoder-support" / "contracts" / "qoder-support.openapi.yaml"


def test_init_contract_lists_qoder_as_supported_assistant():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "enum: [copilot, qwen, opencode, qoder]" in content
    assert "/projects/init:" in content


def test_init_contract_defines_qoder_project_assets():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "generatedAssets" in content
    assert "supportSurfacesUpdated" in content
