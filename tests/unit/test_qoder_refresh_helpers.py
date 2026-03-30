from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_generate_instructions_script_contains_qoder_links():
    script = (ROOT / "scripts" / "bash" / "generate-instructions.sh").read_text(encoding="utf-8")
    assert "mkdir -p .qoder" in script
    assert "QODER.md" in script


def test_usage_doc_documents_qoder_refresh_flow():
    usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
    assert "Qoder Maintenance Workflow" in usage
    assert "generate-instructions.sh" in usage
