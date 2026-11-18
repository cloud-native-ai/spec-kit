"""Form-field contracts of the document-utils pdf family (original MIT rewrite).

What is pinned here is the caller-facing surface, not the implementation: the
JSON description of a document's fields (names, types, pages, rectangles, legal
values), the validation refusals of the value filler, the annotation geometry of
the field-less route, and the bounding-box audit's verdicts.

Every fixture is a real PDF built in a temporary directory -- an AcroForm with a
text field, a checkbox, a dropdown, a radio group and a second-page field, plus a
list box whose /Opt holds [export, display] pairs. The paired-option case is the
regression that matters most: pypdf's list-box appearance builder joins /Opt as
text and raises on pairs, so the filler must hand it a flattened view and restore
the document's own options afterwards.
"""

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pypdf")
pytest.importorskip("reportlab")

from pypdf import PdfReader, PdfWriter  # noqa: E402
from pypdf.generic import ArrayObject, NameObject, TextStringObject  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts" / "pdf"
PAGE_WIDTH, PAGE_HEIGHT = 612, 792


def _load(script_name: str, module_name: str):
    """Import one skill script by path, with a neutral argv and restored sys.path."""
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
def extractor():
    return _load("extract_form_field_info.py", "_du_pdf_extract_test")


@pytest.fixture(scope="module")
def filler():
    return _load("fill_fillable_fields.py", "_du_pdf_fill_test")


@pytest.fixture(scope="module")
def annotator():
    return _load("fill_pdf_form_with_annotations.py", "_du_pdf_annot_test")


@pytest.fixture(scope="module")
def auditor():
    return _load("check_bounding_boxes.py", "_du_pdf_audit_test")


@pytest.fixture(scope="module")
def detector():
    return _load("check_fillable_fields.py", "_du_pdf_detect_test")


def _set_options(pdf_path: Path, options_by_name: dict) -> None:
    """Pin /Opt to the ISO 32000-1 order: [export value, display text] pairs."""
    writer = PdfWriter(clone_from=PdfReader(str(pdf_path)))
    for reference in writer.root_object["/AcroForm"]["/Fields"]:
        field = reference.get_object()
        name = str(field.get("/T", ""))
        if name not in options_by_name:
            continue
        field[NameObject("/Opt")] = ArrayObject(
            ArrayObject([TextStringObject(value), TextStringObject(text)])
            for value, text in options_by_name[name]
        )
    with open(pdf_path, "wb") as stream:
        writer.write(stream)


def _draw_form(path: Path, *, listbox: bool = False) -> Path:
    """Build a two-page form with one field of every supported type."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    sheet = canvas.Canvas(str(path), pagesize=letter)
    height = PAGE_HEIGHT
    sheet.drawString(72, height - 60, "Membership Application")
    sheet.acroForm.textfield(name="last_name", tooltip="Last name", x=150, y=height - 120,
                             width=200, height=16, forceBorder=True)
    sheet.acroForm.textfield(name="first_name", tooltip="First name", x=150, y=height - 150,
                             width=200, height=16, forceBorder=True)
    sheet.acroForm.checkbox(name="agree", tooltip="Agree", x=72, y=height - 190, size=12,
                            checked=False, buttonStyle="check")
    if listbox:
        sheet.acroForm.listbox(name="country", tooltip="Country", value="US",
                               options=[("US", "United States"), ("CA", "Canada")],
                               x=150, y=height - 230, width=160, height=32,
                               fieldFlags="", forceBorder=True)
    else:
        sheet.acroForm.choice(name="country", tooltip="Country", value="US",
                              options=[("US", "United States"), ("CA", "Canada")],
                              x=150, y=height - 230, width=160, height=16, forceBorder=True)
    sheet.acroForm.radio(name="plan", tooltip="Plan", value="basic", selected=True,
                         x=72, y=height - 270, size=12)
    sheet.acroForm.radio(name="plan", tooltip="Plan", value="pro", selected=False,
                         x=140, y=height - 270, size=12)
    sheet.showPage()
    sheet.drawString(72, height - 60, "Notes")
    sheet.acroForm.textfield(name="notes", tooltip="Notes", x=72, y=height - 120,
                             width=400, height=60, forceBorder=True)
    sheet.showPage()
    sheet.save()
    _set_options(path, {"country": [("US", "United States"), ("CA", "Canada")]})
    return path


@pytest.fixture(scope="module")
def form_pdf(tmp_path_factory) -> Path:
    return _draw_form(tmp_path_factory.mktemp("du-pdf-form") / "form.pdf")


@pytest.fixture(scope="module")
def listbox_pdf(tmp_path_factory) -> Path:
    return _draw_form(tmp_path_factory.mktemp("du-pdf-listbox") / "listbox.pdf", listbox=True)


@pytest.fixture(scope="module")
def plain_pdf(tmp_path_factory) -> Path:
    """A form with no field layer: labels, ruled lines, tick boxes, one circle."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    path = tmp_path_factory.mktemp("du-pdf-plain") / "plain.pdf"
    sheet = canvas.Canvas(str(path), pagesize=letter)
    height = PAGE_HEIGHT
    sheet.setFont("Helvetica", 11)
    sheet.drawString(72, height - 72, "Last Name")
    sheet.drawString(300, height - 72, "First Name")
    sheet.line(72, height - 88, PAGE_WIDTH - 72, height - 88)
    sheet.line(72, height - 128, PAGE_WIDTH - 72, height - 128)
    sheet.rect(72, height - 208, 10, 10)
    sheet.circle(350, height - 203, 6)
    sheet.showPage()
    sheet.save()
    return path


def _values_file(path: Path, records: list) -> Path:
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return path


GOOD_VALUES = [
    {"field_id": "last_name", "description": "Family name", "page": 1, "value": "Simpson"},
    {"field_id": "agree", "description": "Consent", "page": 1, "value": "/Yes"},
    {"field_id": "country", "description": "Country", "page": 1, "value": "CA"},
    {"field_id": "plan", "description": "Tier", "page": 1, "value": "/pro"},
    {"field_id": "notes", "description": "Free text", "page": 2, "value": "None"},
]


# --------------------------------------------------------------------------- #
# Field description
# --------------------------------------------------------------------------- #
def test_field_info_describes_every_type_in_reading_order(extractor, form_pdf):
    records = extractor.get_field_info(PdfReader(str(form_pdf)))
    assert [r["field_id"] for r in records] == [
        "last_name", "first_name", "agree", "country", "plan", "notes",
    ]
    by_id = {r["field_id"]: r for r in records}

    assert by_id["last_name"]["type"] == "text"
    assert by_id["last_name"]["page"] == 1
    assert by_id["last_name"]["rect"] == [150, 672, 350, 688]
    assert by_id["notes"]["page"] == 2

    checkbox = by_id["agree"]
    assert checkbox["type"] == "checkbox"
    assert (checkbox["checked_value"], checkbox["unchecked_value"]) == ("/Yes", "/Off")

    choice = by_id["country"]
    assert choice["type"] == "choice"
    assert choice["choice_options"] == [
        {"value": "US", "text": "United States"},
        {"value": "CA", "text": "Canada"},
    ]

    radio = by_id["plan"]
    assert radio["type"] == "radio_group"
    assert [option["value"] for option in radio["radio_options"]] == ["/basic", "/pro"]
    assert radio["radio_options"][0]["rect"] == [72, 522, 84, 534]
    assert radio["page"] == 1


def test_field_info_cli_writes_the_same_json(extractor, form_pdf, tmp_path, capsys):
    target = tmp_path / "field_info.json"
    assert extractor.main([str(form_pdf), str(target)]) == 0
    assert json.loads(target.read_text(encoding="utf-8")) == extractor.get_field_info(
        PdfReader(str(form_pdf))
    )
    assert f"Wrote 6 fields to {target}" in capsys.readouterr().out


def test_plain_string_options_are_value_and_text(tmp_path, extractor):
    """An /Opt of plain strings is legal; each option is both value and display."""
    path = _draw_form(tmp_path / "strings.pdf")
    writer = PdfWriter(clone_from=PdfReader(str(path)))
    for reference in writer.root_object["/AcroForm"]["/Fields"]:
        field = reference.get_object()
        if str(field.get("/T", "")) == "country":
            field[NameObject("/Opt")] = ArrayObject(
                [TextStringObject("US"), TextStringObject("CA")]
            )
    with open(path, "wb") as stream:
        writer.write(stream)
    records = {r["field_id"]: r for r in extractor.get_field_info(PdfReader(str(path)))}
    assert records["country"]["choice_options"] == [
        {"value": "US", "text": "US"},
        {"value": "CA", "text": "CA"},
    ]


def test_qualified_name_joins_ancestors(extractor, form_pdf):
    reader = PdfReader(str(form_pdf))
    kids = [
        reference.get_object()
        for reference in reader.pages[0]["/Annots"]
        if reference.get_object().get("/Parent") is not None
    ]
    assert kids, "fixture must contain radio kids (widgets without their own /T)"
    for widget in kids:
        assert widget.get("/T") is None
        assert extractor.get_full_annotation_field_id(widget) == "plan"


def test_field_without_a_widget_is_reported_and_omitted(extractor, form_pdf, tmp_path, capsys):
    """A declared field with no widget has no place to put a value: say so, drop it."""
    path = tmp_path / "widgetless.pdf"
    writer = PdfWriter(clone_from=PdfReader(str(form_pdf)))
    # Keep the field in /AcroForm but remove its widget from the page.
    writer.pages[1][NameObject("/Annots")] = ArrayObject()
    with open(path, "wb") as stream:
        writer.write(stream)

    records = extractor.get_field_info(PdfReader(str(path)))
    assert "notes" not in [record["field_id"] for record in records]
    assert all("page" in record for record in records)
    assert "Unable to determine location for field id: notes, ignoring" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Filling the document's own fields
# --------------------------------------------------------------------------- #
def test_fill_writes_values_and_keeps_the_form_fillable(filler, form_pdf, tmp_path):
    values = _values_file(tmp_path / "values.json", GOOD_VALUES)
    output = tmp_path / "filled.pdf"
    assert filler.main([str(form_pdf), str(values), str(output)]) == 0
    assert output.is_file()

    reader = PdfReader(str(output))
    fields = reader.get_fields()
    assert str(fields["last_name"]["/V"]) == "Simpson"
    assert str(fields["agree"]["/V"]) == "/Yes"
    assert str(fields["country"]["/V"]) == "CA"
    assert str(fields["plan"]["/V"]) == "/pro"
    assert str(fields["notes"]["/V"]) == "None"
    assert bool(reader.trailer["/Root"]["/AcroForm"]["/NeedAppearances"]) is True
    assert filler.fill_pdf_fields(str(form_pdf), str(values), str(tmp_path / "again.pdf")) == 0


def test_fill_selects_one_radio_button_and_clears_the_others(filler, form_pdf, tmp_path):
    values = _values_file(tmp_path / "values.json", GOOD_VALUES)
    output = tmp_path / "filled.pdf"
    assert filler.main([str(form_pdf), str(values), str(output)]) == 0
    states = []
    for reference in PdfReader(str(output)).pages[0]["/Annots"]:
        widget = reference.get_object()
        parent = widget.get("/Parent")
        if parent is not None and str(parent.get_object().get("/T")) == "plan":
            states.append(str(widget.get("/AS")))
    assert sorted(states) == ["/Off", "/pro"]


def test_fill_listbox_keeps_paired_options(tmp_path, filler, listbox_pdf):
    """The paired-/Opt regression: fill succeeds and the pairs survive."""
    values = _values_file(tmp_path / "values.json", [
        {"field_id": "country", "page": 1, "value": "CA"},
    ])
    output = tmp_path / "filled.pdf"
    assert filler.main([str(listbox_pdf), str(values), str(output)]) == 0
    field = PdfReader(str(output)).get_fields()["country"]
    assert str(field["/V"]) == "CA"
    assert [[str(v) for v in pair] for pair in field["/Opt"]] == [
        ["US", "United States"], ["CA", "Canada"],
    ]


def test_fill_refuses_every_invalid_record(filler, form_pdf, tmp_path, capsys):
    records = [
        {"field_id": "last_name", "page": 2, "value": "Simpson"},
        {"field_id": "agree", "page": 1, "value": "/Maybe"},
        {"field_id": "country", "page": 1, "value": "MX"},
        {"field_id": "plan", "page": 1, "value": "/free"},
        {"field_id": "nope", "page": 1, "value": "x"},
    ]
    values = _values_file(tmp_path / "bad.json", records)
    output = tmp_path / "filled.pdf"
    assert filler.main([str(form_pdf), str(values), str(output)]) == 1
    assert not output.exists(), "a refused run must not write the output"
    out = capsys.readouterr().out
    assert "ERROR: Incorrect page number for `last_name` (got 2, expected 1)" in out
    assert 'ERROR: Invalid value "/Maybe" for checkbox field "agree"' in out
    assert 'ERROR: Invalid value "MX" for choice field "country"' in out
    assert 'ERROR: Invalid value "/free" for radio group field "plan"' in out
    assert "ERROR: `nope` is not a valid field ID" in out


def test_record_without_value_is_checked_but_not_written(filler, form_pdf, tmp_path):
    values = _values_file(tmp_path / "partial.json", [
        {"field_id": "last_name", "page": 1},
        {"field_id": "notes", "page": 2, "value": "kept"},
    ])
    output = tmp_path / "filled.pdf"
    assert filler.main([str(form_pdf), str(values), str(output)]) == 0
    fields = PdfReader(str(output)).get_fields()
    assert str(fields["notes"]["/V"]) == "kept"
    assert fields["last_name"].get("/V") in (None, "")


def test_validation_error_helper_is_type_aware(filler):
    checkbox = {"field_id": "c", "type": "checkbox", "checked_value": "/Yes", "unchecked_value": "/Off"}
    assert filler.validation_error_for_field_value(checkbox, "/Yes") is None
    assert filler.validation_error_for_field_value(checkbox, "/Off") is None
    assert "ERROR" in filler.validation_error_for_field_value(checkbox, "/No")
    text = {"field_id": "t", "type": "text"}
    assert filler.validation_error_for_field_value(text, "anything") is None


# --------------------------------------------------------------------------- #
# The field-less route: free-text annotations
# --------------------------------------------------------------------------- #
def _fields_document(page_record: dict, entry_box: list, text: str = "Simpson") -> dict:
    return {
        "pages": [page_record],
        "form_fields": [{
            "page_number": 1,
            "description": "Family name entry",
            "field_label": "Last Name",
            "label_bounding_box": [72, 60, 128, 74],
            "entry_bounding_box": entry_box,
            "entry_text": {"text": text, "font_size": 11},
        }],
    }


def test_transform_helpers_flip_and_scale(annotator):
    assert annotator.transform_from_pdf_coords([10, 20, 110, 40], 792) == (10, 752, 110, 772)
    assert annotator.transform_from_image_coords([10, 20, 110, 40], 306, 396, 612, 792) == (
        20.0, 712.0, 220.0, 752.0,
    )


def test_annotation_fill_uses_top_down_points(annotator, plain_pdf, tmp_path, capsys):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_fields_document(
        {"page_number": 1, "pdf_width": PAGE_WIDTH, "pdf_height": PAGE_HEIGHT},
        [140, 62, 290, 78],
    )), encoding="utf-8")
    output = tmp_path / "annotated.pdf"
    assert annotator.main([str(plain_pdf), str(fields), str(output)]) == 0

    annotations = [a.get_object() for a in PdfReader(str(output)).pages[0]["/Annots"]]
    assert len(annotations) == 1
    assert str(annotations[0]["/Subtype"]) == "/FreeText"
    assert str(annotations[0]["/Contents"]) == "Simpson"
    assert [float(v) for v in annotations[0]["/Rect"]] == [140.0, 714.0, 290.0, 730.0]
    out = capsys.readouterr().out
    assert f"Successfully filled PDF form and saved to {output}" in out
    assert "Added 1 text annotations" in out


def test_annotation_fill_scales_pixel_boxes(annotator, plain_pdf, tmp_path):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(_fields_document(
        {"page_number": 1, "image_width": 1224, "image_height": 1584},
        [280, 124, 580, 156],
    )), encoding="utf-8")
    output = tmp_path / "annotated.pdf"
    assert annotator.main([str(plain_pdf), str(fields), str(output)]) == 0
    rect = [float(v) for v in PdfReader(str(output)).pages[0]["/Annots"][0].get_object()["/Rect"]]
    assert rect == [140.0, 714.0, 290.0, 730.0]


def test_annotation_fill_skips_blank_entries(annotator, plain_pdf, tmp_path, capsys):
    document = _fields_document(
        {"page_number": 1, "pdf_width": PAGE_WIDTH, "pdf_height": PAGE_HEIGHT},
        [140, 62, 290, 78],
    )
    document["form_fields"].append(dict(document["form_fields"][0], entry_text={"text": ""}))
    document["form_fields"].append({
        "page_number": 1, "description": "no text member",
        "label_bounding_box": [0, 0, 1, 1], "entry_bounding_box": [10, 10, 20, 20],
    })
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "annotated.pdf"
    assert annotator.main([str(plain_pdf), str(fields), str(output)]) == 0
    assert "Added 1 text annotations" in capsys.readouterr().out


def test_annotation_fill_refuses_a_page_without_a_record(annotator, plain_pdf, tmp_path):
    document = _fields_document(
        {"page_number": 1, "pdf_width": PAGE_WIDTH, "pdf_height": PAGE_HEIGHT},
        [140, 62, 290, 78],
    )
    document["form_fields"][0]["page_number"] = 7
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "annotated.pdf"
    assert annotator.main([str(plain_pdf), str(fields), str(output)]) == 1
    assert not output.exists()


# --------------------------------------------------------------------------- #
# Geometry audit and route detection
# --------------------------------------------------------------------------- #
def _audit(auditor, document: dict) -> list:
    return auditor.get_bounding_box_messages(io.StringIO(json.dumps(document)))


def _field(description, label, entry, page=1, font_size=None):
    record = {
        "page_number": page, "description": description,
        "label_bounding_box": label, "entry_bounding_box": entry,
    }
    if font_size is not None:
        record["entry_text"] = {"text": "x", "font_size": font_size}
    return record


def test_audit_accepts_disjoint_boxes(auditor):
    document = {"form_fields": [
        _field("a", [0, 0, 10, 10], [20, 0, 60, 16]),
        _field("b", [0, 20, 10, 30], [20, 20, 60, 36]),
    ]}
    assert _audit(auditor, document) == ["Read 2 fields", "SUCCESS: All bounding boxes are valid"]


def test_audit_reports_label_inside_its_own_entry(auditor):
    document = {"form_fields": [_field("a", [25, 2, 40, 8], [20, 0, 60, 12])]}
    lines = _audit(auditor, document)
    assert lines[0] == "Read 1 fields"
    assert any(line.startswith("FAILURE: intersection between label and entry") for line in lines)
    assert not any(line.startswith("SUCCESS") for line in lines)


def test_audit_reports_cross_field_overlap_with_both_roles(auditor):
    document = {"form_fields": [
        _field("a", [0, 0, 10, 10], [20, 0, 60, 12]),
        _field("b", [30, 2, 45, 8], [70, 0, 90, 12]),
    ]}
    lines = _audit(auditor, document)
    failure = next(line for line in lines if line.startswith("FAILURE"))
    assert "entry bounding box for `a`" in failure
    assert "label bounding box for `b`" in failure


def test_audit_ignores_boxes_on_different_pages(auditor):
    document = {"form_fields": [
        _field("a", [0, 0, 10, 10], [20, 0, 60, 16], page=1),
        _field("b", [0, 0, 10, 10], [20, 0, 60, 16], page=2),
    ]}
    assert _audit(auditor, document)[-1] == "SUCCESS: All bounding boxes are valid"


def test_touching_edges_are_not_an_overlap(auditor):
    document = {"form_fields": [_field("a", [0, 0, 20, 10], [20, 0, 60, 16])]}
    assert _audit(auditor, document)[-1] == "SUCCESS: All bounding boxes are valid"


def test_audit_reports_an_entry_shorter_than_its_font(auditor):
    document = {"form_fields": [_field("a", [0, 0, 10, 10], [20, 0, 60, 4], font_size=10)]}
    lines = _audit(auditor, document)
    assert any("entry bounding box height (4)" in line and "font size: 10" in line for line in lines)


def test_audit_defaults_the_font_size_to_fourteen(auditor):
    document = {"form_fields": [_field("a", [0, 0, 10, 10], [20, 0, 60, 12])]}
    assert any("font size: 14" in line for line in _audit(auditor, document))


def test_audit_stops_at_its_message_budget(auditor):
    document = {"form_fields": [
        _field(f"f{i}", [0, 0, 10, 10], [0, 0, 10, 10]) for i in range(30)
    ]}
    lines = _audit(auditor, document)
    assert len(lines) == 21
    assert lines[-1] == "Aborting further checks; fix bounding boxes and try again"


def test_audit_cli_exit_status_is_not_the_verdict(auditor, tmp_path, capsys):
    fields = tmp_path / "fields.json"
    fields.write_text(json.dumps({"form_fields": [
        _field("a", [25, 2, 40, 8], [20, 0, 60, 12]),
    ]}), encoding="utf-8")
    assert auditor.main([str(fields)]) == 0
    assert "FAILURE" in capsys.readouterr().out


def test_detection_names_the_route(detector, form_pdf, plain_pdf, capsys):
    assert detector.main([str(form_pdf)]) == 0
    assert capsys.readouterr().out.strip() == "This PDF has fillable form fields"
    assert detector.main([str(plain_pdf)]) == 0
    assert capsys.readouterr().out.strip() == (
        "This PDF does not have fillable form fields; "
        "you will need to visually determine where to enter data"
    )


def test_scripts_run_from_an_unrelated_working_directory(form_pdf, tmp_path):
    """The filler loads its sibling extractor by path, not by cwd."""
    values = _values_file(tmp_path / "values.json", GOOD_VALUES)
    output = tmp_path / "filled.pdf"
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "fill_fillable_fields.py"),
         str(form_pdf), str(values), str(output)],
        cwd=str(tmp_path), capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert output.is_file()