from pathlib import Path


def test_support_surfaces_include_claude_name(claude_support_surface_files: list[Path]):
    for surface in claude_support_surface_files:
        text = surface.read_text(encoding="utf-8")
        assert "Claude Code" in text


def test_support_surfaces_include_claude_install_url(
    claude_support_surface_files: list[Path],
):
    docs = [path for path in claude_support_surface_files if path.suffix == ".md"]
    assert any(
        "https://www.anthropic.com/claude-code" in path.read_text(encoding="utf-8")
        for path in docs
    )
