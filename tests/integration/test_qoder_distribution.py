from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_packaging_keeps_template_and_script_resources_for_qoder_assets():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"templates" = "specify_cli/templates"' in pyproject
    assert '"scripts" = "specify_cli/scripts"' in pyproject


def test_public_docs_and_instructions_are_qoder_consistent():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    install = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8")
    instructions = (ROOT / ".ai" / "instructions.md").read_text(encoding="utf-8")

    assert "Qoder" in readme
    assert "https://qoder.com/cli" in install
    assert "Qoder" in instructions
