from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_distribution_surfaces_include_claude_docs_and_templates():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    installation = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8")
    agents_template = (ROOT / "templates" / "commands" / "agents.md").read_text(
        encoding="utf-8"
    )

    assert "Claude Code" in readme
    assert "Claude Code" in installation
    assert "Claude Code" in agents_template


def test_distribution_includes_claudeignore_template_asset():
    assert (ROOT / "templates" / "claudeignore-template").exists()
