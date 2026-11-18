"""Rendering and geometry-recovery contracts of the document-utils pdf family.

Three surfaces are pinned: the page-to-PNG converter (one file per page, the
naming scheme, the long-side cap, directory creation), the validation overlay
(which rectangle is drawn in which colour, and the reported count), and the
structure inventory a field-less form is measured from (what counts as a row
rule, what counts as a tick box, and the top-down rounded coordinates).

Fixtures are real PDFs drawn in a temporary directory plus a plain white PNG, so
the colour assertions read actual pixels rather than a mocked draw call.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("pypdfium2")
pytest.importorskip("PIL")
pytest.importorskip("pdfplumber")
pytest.importorskip("reportlab")

from PIL import Image  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts" / "pdf"


def _load(script_name: str, module_name: str):
    path = SCRIPTS / script_name
    assert path.is_file(), f"script missing: {path}"
    saved_path, saved_argv = list(sys.path), list(sys.argv)
    sys.argv = [str(path)]
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.argv = saved_argv
        sys.path[:] = saved_path
    return module


@pytest.fixture(scope="module")
def converter():
    return _load("convert_pdf_to_images.py", "_du_pdf_convert_test")


@pytest.fixture(scope="module")
def overlay():
    return _load("create_validation_image.py", "_du_pdf_overlay_test")


@pytest.fixture(scope="module")
def structure():
    return _load("extract_form_structure.py", "_du_pdf_structure_test")


@pytest.fixture(scope="module")
def two_page_pdf(tmp_path_factory) -> Path:
    from reportlab.pdfgen import canvas

    path = tmp_path_factory.mktemp("du-pdf-render") / "two.pdf"
    sheet = canvas.Canvas(str(path), pagesize=(612, 792))
    sheet.drawString(72, 720, "First page")
    sheet.showPage()
    sheet.drawString(72, 720, "Second page")
    sheet.showPage()
    sheet.save()
    return path


@pytest.fixture(scope="module")
def small_page_pdf(tmp_path_factory) -> Path:
    from reportlab.pdfgen import canvas

    path = tmp_path_factory.mktemp("du-pdf-small") / "small.pdf"
    sheet = canvas.Canvas(str(path), pagesize=(200, 100))
    sheet.drawString(20, 50, "tiny")
    sheet.showPage()
    sheet.save()
    return path


@pytest.fixture(scope="module")
def geometry_pdf(tmp_path_factory) -> Path:
    """Labels, two row rules, one short rule, two tick boxes, one oversized box, one circle."""
    from reportlab.pdfgen import canvas

    path = tmp_path_factory.mktemp("du-pdf-geometry") / "geometry.pdf"
    sheet = canvas.Canvas(str(path), pagesize=(612, 792))
    sheet.setFont("Helvetica", 11)
    sheet.drawString(72, 720, "Last Name")
    sheet.drawString(72, 680, "Address")
    sheet.line(72, 704, 540, 704)          # spans 468 of 612 points: a row rule
    sheet.line(72, 664, 540, 664)          # second row rule
    sheet.line(72, 620, 172, 620)          # 100 points: too short to be a row rule
    sheet.rect(72, 560, 10, 10)            # tick box
    sheet.rect(200, 558, 12, 12)           # tick box
    sheet.rect(300, 540, 60, 30)           # too large: a cell, not a tick box
    sheet.circle(450, 565, 6)              # a curve: never a tick box
    sheet.showPage()
    sheet.save()
    return path


# --------------------------------------------------------------------------- #
# PDF -> PNG
# --------------------------------------------------------------------------- #
def test_convert_writes_one_png_per_page_in_order(converter, two_page_pdf, tmp_path, capsys):
    target = tmp_path / "images"
    assert converter.convert(str(two_page_pdf), str(target)) == 2
    assert sorted(p.name for p in target.iterdir()) == ["page_1.png", "page_2.png"]
    out = capsys.readouterr().out
    assert f"Saved page 1 as {target / 'page_1.png'}" in out
    assert f"Saved page 2 as {target / 'page_2.png'}" in out
    assert "Converted 2 pages to PNG images" in out
    with Image.open(target / "page_1.png") as image:
        assert image.format == "PNG"


def test_convert_caps_the_long_side_and_keeps_the_aspect(converter, two_page_pdf, tmp_path):
    target = tmp_path / "capped"
    converter.convert(str(two_page_pdf), str(target))
    with Image.open(target / "page_1.png") as image:
        width, height = image.size
    assert max(width, height) <= 1000
    assert height == 1000
    assert width == pytest.approx(1000 * 612 / 792, abs=2)


def test_convert_honours_a_custom_cap(converter, two_page_pdf, tmp_path):
    target = tmp_path / "small"
    converter.convert(str(two_page_pdf), str(target), max_dim=400)
    with Image.open(target / "page_1.png") as image:
        assert max(image.size) <= 400


def test_convert_never_enlarges_a_small_page(converter, small_page_pdf, tmp_path):
    target = tmp_path / "unchanged"
    converter.convert(str(small_page_pdf), str(target))
    with Image.open(target / "page_1.png") as image:
        # 200x100 points at 200 dpi is 556x278 pixels: below the cap, so untouched.
        assert image.size == (556, 278)


def test_convert_creates_a_missing_directory(converter, two_page_pdf, tmp_path):
    target = tmp_path / "deep" / "nested" / "images"
    assert not target.exists()
    converter.convert(str(two_page_pdf), str(target))
    assert (target / "page_1.png").is_file()


def test_convert_cli_usage_and_failure_exit_codes(converter, tmp_path, capsys):
    assert converter.main([]) == 1
    assert "Usage: convert_pdf_to_images.py" in capsys.readouterr().out
    assert converter.main([str(tmp_path / "absent.pdf"), str(tmp_path / "out")]) == 1
    assert "ERROR" in capsys.readouterr().err


# --------------------------------------------------------------------------- #
# Validation overlay
# --------------------------------------------------------------------------- #
def _overlay_fields() -> dict:
    return {
        "pages": [{"page_number": 1, "pdf_width": 612, "pdf_height": 792}],
        "form_fields": [
            {"page_number": 1, "description": "first",
             "label_bounding_box": [10, 100, 90, 120],
             "entry_bounding_box": [100, 100, 200, 120],
             "entry_text": {"text": "a"}},
            {"page_number": 1, "description": "second",
             "label_bounding_box": [10, 200, 90, 220],
             "entry_bounding_box": [100, 200, 200, 220],
             "entry_text": {"text": "b"}},
            {"page_number": 2, "description": "other page",
             "label_bounding_box": [10, 300, 90, 320],
             "entry_bounding_box": [100, 300, 200, 320]},
        ],
    }


@pytest.fixture
def white_page(tmp_path) -> Path:
    path = tmp_path / "page.png"
    Image.new("RGB", (612, 792), "white").save(path)
    return path


def test_overlay_draws_entry_red_and_label_blue(overlay, white_page, tmp_path):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_overlay_fields()), encoding="utf-8")
    output = tmp_path / "overlay.png"
    assert overlay.create_validation_image(1, str(fields), str(white_page), str(output)) == 4

    with Image.open(output) as image:
        assert image.getpixel((100, 100)) == (255, 0, 0)      # entry outline
        assert image.getpixel((10, 100)) == (0, 0, 255)        # label outline
        assert image.getpixel((150, 110)) == (255, 255, 255)   # inside stays untouched
        assert image.getpixel((100, 300)) == (255, 255, 255)   # page 2 not drawn


def test_overlay_counts_only_the_requested_page(overlay, white_page, tmp_path, capsys):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_overlay_fields()), encoding="utf-8")
    output = tmp_path / "overlay2.png"
    assert overlay.create_validation_image(2, str(fields), str(white_page), str(output)) == 2
    assert f"Created validation image at {output} with 2 bounding boxes" in capsys.readouterr().out


def test_overlay_of_an_unmatched_page_draws_nothing(overlay, white_page, tmp_path, capsys):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_overlay_fields()), encoding="utf-8")
    output = tmp_path / "overlay9.png"
    assert overlay.create_validation_image(9, str(fields), str(white_page), str(output)) == 0
    assert "with 0 bounding boxes" in capsys.readouterr().out
    with Image.open(output) as drawn, Image.open(white_page) as original:
        assert drawn.tobytes() == original.tobytes()


def test_overlay_cli_rejects_a_non_numeric_page(overlay, white_page, tmp_path, capsys):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_overlay_fields()), encoding="utf-8")
    assert overlay.main(["one", str(fields), str(white_page), str(tmp_path / "o.png")]) == 1
    assert "Usage: create_validation_image.py" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Structure inventory
# --------------------------------------------------------------------------- #
def test_structure_inventory_filters_and_coordinates(structure, geometry_pdf):
    recovered = structure.extract_form_structure(str(geometry_pdf))
    assert set(recovered) == {"pages", "labels", "lines", "checkboxes", "row_boundaries"}
    assert recovered["pages"] == [{"page_number": 1, "width": 612.0, "height": 792.0}]

    assert [label["text"] for label in recovered["labels"]] == ["Last", "Name", "Address"]
    assert all(set(label) == {"page", "text", "x0", "top", "x1", "bottom"}
               for label in recovered["labels"])

    # Only the two rules spanning more than half the page width are row rules.
    assert [line["y"] for line in recovered["lines"]] == [88.0, 128.0]
    assert all(set(line) == {"page", "y", "x0", "x1"} for line in recovered["lines"])

    # The two small squares are tick boxes; the large rectangle and the circle are not.
    assert len(recovered["checkboxes"]) == 2
    first = recovered["checkboxes"][0]
    assert set(first) == {"page", "x0", "top", "x1", "bottom", "center_x", "center_y"}
    assert (first["x0"], first["top"], first["x1"], first["bottom"]) == (72.0, 222.0, 82.0, 232.0)
    assert (first["center_x"], first["center_y"]) == (77.0, 227.0)

    assert recovered["row_boundaries"] == [
        {"page": 1, "row_top": 88.0, "row_bottom": 128.0, "row_height": 40.0}
    ]


def test_structure_coordinates_are_top_down_and_rounded(structure, geometry_pdf):
    recovered = structure.extract_form_structure(str(geometry_pdf))
    label = recovered["labels"][0]
    assert label["top"] < label["bottom"]                 # y grows downward
    # Drawn at baseline y=720 on a 792-point page: the word sits near the top.
    assert 60 < label["top"] < 70
    assert label["bottom"] - label["top"] == pytest.approx(11, abs=1)
    for group in ("labels", "lines", "checkboxes", "row_boundaries"):
        for record in recovered[group]:
            for key, value in record.items():
                if isinstance(value, float):
                    assert round(value, 1) == value, f"{group}.{key} not rounded"


def test_structure_cli_reports_every_count(structure, geometry_pdf, tmp_path, capsys):
    target = tmp_path / "structure.json"
    assert structure.main([str(geometry_pdf), str(target)]) == 0
    out = capsys.readouterr().out
    assert f"Extracting structure from {geometry_pdf}..." in out
    assert "  - 1 pages" in out
    assert "  - 3 text labels" in out
    assert "  - 2 horizontal lines" in out
    assert "  - 2 checkboxes" in out
    assert "  - 1 row boundaries" in out
    assert f"Saved to {target}" in out
    assert json.loads(target.read_text(encoding="utf-8"))["pages"][0]["page_number"] == 1


def test_structure_of_a_blank_page_is_empty_but_well_formed(structure, tmp_path):
    from reportlab.pdfgen import canvas

    path = tmp_path / "blank.pdf"
    sheet = canvas.Canvas(str(path), pagesize=(612, 792))
    sheet.showPage()
    sheet.save()
    recovered = structure.extract_form_structure(str(path))
    assert recovered["pages"] == [{"page_number": 1, "width": 612.0, "height": 792.0}]
    assert recovered["labels"] == []
    assert recovered["lines"] == []
    assert recovered["checkboxes"] == []
    assert recovered["row_boundaries"] == []