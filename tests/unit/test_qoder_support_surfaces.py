from pathlib import Path


def test_support_surfaces_include_qoder_name(qoder_support_surface_files: list[Path]):
    for surface in qoder_support_surface_files:
        text = surface.read_text(encoding="utf-8")
        assert "Qoder" in text


def test_support_surfaces_include_qoder_install_url(qoder_support_surface_files: list[Path]):
    docs = [path for path in qoder_support_surface_files if path.suffix == ".md"]
    assert any("https://qoder.com/cli" in path.read_text(encoding="utf-8") for path in docs)
