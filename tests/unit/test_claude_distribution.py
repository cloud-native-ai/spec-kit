from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_templates_include_claudeignore_asset():
    assert (ROOT / "templates" / "claudeignore-template").exists()


def test_pyproject_keeps_template_resources_packaged():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"templates" = "specify_cli/templates"' in pyproject
