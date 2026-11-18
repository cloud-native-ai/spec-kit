"""Contract of the PPTX unpacked-tree scripts: add_slide.py and clean.py.

Both scripts operate on a directory of OOXML parts, not on a zipped deck, so the
fixture here is a small unpacked tree written part by part.  What is pinned is
the caller-facing surface -- operands, stdout lines, exit codes -- plus the two
properties that make the scripts safe to run between hand edits: they touch only
the parts they must, and they refuse input that could expand or escape.

The tree is deliberately minimal.  A full package's validity is checked in
test_document_utils_pptx_thumbnail.py, where python-pptx builds and reopens a real
deck; nothing here needs that library, so these cases run on a bare interpreter.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts"

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
SLIDE_CT = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"


def _load(script_name: str, module_name: str):
    """Import a skill script the way the sibling skill tests do."""
    path = SCRIPTS / "pptx" / script_name
    assert path.is_file(), f"script missing: {path}"
    saved_path, saved_argv = list(sys.path), list(sys.argv)
    sys.argv = [str(path)]
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    finally:
        sys.argv = saved_argv
        sys.path[:] = saved_path
    return module


@pytest.fixture(scope="module")
def add_slide():
    return _load("add_slide.py", "_f3_pptx_add_slide")


@pytest.fixture(scope="module")
def clean():
    return _load("clean.py", "_f3_pptx_clean")


@pytest.fixture(scope="module")
def parts():
    return _load("ooxml_parts.py", "_f3_pptx_parts")


def _rels(*entries: str) -> str:
    body = "".join(
        f'<Relationship Id="{rid}" Type="{R_NS}/{kind}" Target="{target}"/>'
        for rid, kind, target in entries
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="{PR_NS}">{body}</Relationships>'


def _slide(text: str) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<p:sld xmlns:p="{P_NS}" xmlns:a="{A_NS}" xmlns:r="{R_NS}">'
        f"<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id=\"1\" name=\"\"/>"
        f"<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>"
        f"<p:sp><p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>"
        f"</p:spTree></p:cSld></p:sld>"
    )


@pytest.fixture
def deck(tmp_path: Path) -> Path:
    """An unpacked two-slide deck with media, notes, a theme and a parked part."""
    root = tmp_path / "unpacked"
    overrides = [
        ("/ppt/presentation.xml", "presentation.main+xml"),
        ("/ppt/slides/slide1.xml", "slide+xml"),
        ("/ppt/slides/slide2.xml", "slide+xml"),
        ("/ppt/slideLayouts/slideLayout1.xml", "slideLayout+xml"),
        ("/ppt/slideMasters/slideMaster1.xml", "slideMaster+xml"),
        ("/ppt/theme/theme1.xml", "theme+xml"),
        ("/ppt/notesSlides/notesSlide1.xml", "notesSlide+xml"),
    ]
    prefix = "application/vnd.openxmlformats-officedocument.presentationml."
    files = {
        "[Content_Types].xml": (
            f'<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="{CT_NS}">'
            f'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            f'<Default Extension="xml" ContentType="application/xml"/>'
            f'<Default Extension="png" ContentType="image/png"/>'
            + "".join(
                f'<Override PartName="{name}" ContentType="{prefix}{kind}"/>'
                for name, kind in overrides
            )
            + "</Types>"
        ),
        "_rels/.rels": _rels(("rId1", "officeDocument", "ppt/presentation.xml")),
        "ppt/presentation.xml": (
            f'<?xml version="1.0" encoding="UTF-8"?>\n<p:presentation xmlns:p="{P_NS}" xmlns:r="{R_NS}">'
            f'<p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId3"/></p:sldIdLst>'
            f"</p:presentation>"
        ),
        "ppt/_rels/presentation.xml.rels": _rels(
            ("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
            ("rId2", "slide", "slides/slide1.xml"),
            ("rId3", "slide", "slides/slide2.xml"),
        ),
        "ppt/slides/slide1.xml": _slide("First slide"),
        "ppt/slides/_rels/slide1.xml.rels": _rels(
            ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "image", "../media/kept.png"),
            ("rId3", "notesSlide", "../notesSlides/notesSlide1.xml"),
        ),
        "ppt/slides/slide2.xml": _slide("Second slide"),
        "ppt/slides/_rels/slide2.xml.rels": _rels(
            ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
        ),
        "ppt/slideLayouts/slideLayout1.xml": (
            f'<?xml version="1.0" encoding="UTF-8"?>\n<p:sldLayout xmlns:p="{P_NS}"/>'
        ),
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": _rels(
            ("rId1", "slideMaster", "../slideMasters/slideMaster1.xml"),
        ),
        "ppt/slideMasters/slideMaster1.xml": (
            f'<?xml version="1.0" encoding="UTF-8"?>\n<p:sldMaster xmlns:p="{P_NS}"/>'
        ),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": _rels(
            ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "theme", "../theme/theme1.xml"),
        ),
        "ppt/theme/theme1.xml": f'<?xml version="1.0" encoding="UTF-8"?>\n<a:theme xmlns:a="{A_NS}"/>',
        "ppt/notesSlides/notesSlide1.xml": f'<?xml version="1.0" encoding="UTF-8"?>\n<p:notes xmlns:p="{P_NS}"/>',
        "ppt/notesSlides/_rels/notesSlide1.xml.rels": _rels(
            ("rId1", "slide", "../slides/slide1.xml"),
        ),
        "ppt/media/kept.png": b"\x89PNG\r\n\x1a\nkept",
        "ppt/media/orphan.png": b"\x89PNG\r\n\x1a\norphan",
        "[trash]/parked.xml": "<parked/>",
    }
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    return root


def _drop_slide_from_list(root: Path, slide_id: str) -> None:
    """Do what a manual edit does: delete one <p:sldId> and leave the part."""
    path = root / "ppt" / "presentation.xml"
    text = path.read_text(encoding="utf-8")
    start = text.index(f'<p:sldId id="{slide_id}"')
    end = text.index("/>", start) + 2
    path.write_text(text[:start] + text[end:], encoding="utf-8")


# --------------------------------------------------------------------------- #
# add_slide.py
# --------------------------------------------------------------------------- #
def test_add_slide_from_layout_writes_part_rels_and_registrations(deck, add_slide, capsys):
    before = (deck / "ppt" / "presentation.xml").read_bytes()

    assert add_slide.main([str(deck), "slideLayout1.xml"]) == 0

    out = capsys.readouterr().out.splitlines()
    assert out[0] == "Created slide3.xml from slideLayout1.xml"
    assert out[1] == (
        'Add to presentation.xml <p:sldIdLst>: <p:sldId id="258" r:id="rId4"/>'
    )

    slide = deck / "ppt" / "slides" / "slide3.xml"
    assert slide.is_file()
    assert "<p:spTree>" in slide.read_text(encoding="utf-8")

    rels = (deck / "ppt" / "slides" / "_rels" / "slide3.xml.rels").read_text(encoding="utf-8")
    assert 'Type="%s/slideLayout"' % R_NS in rels
    assert 'Target="../slideLayouts/slideLayout1.xml"' in rels

    assert 'PartName="/ppt/slides/slide3.xml"' in (deck / "[Content_Types].xml").read_text()
    pres_rels = (deck / "ppt" / "_rels" / "presentation.xml.rels").read_text(encoding="utf-8")
    assert 'Id="rId4"' in pres_rels and 'Target="slides/slide3.xml"' in pres_rels

    # Slide order is the caller's decision: the presentation part is untouched.
    assert (deck / "ppt" / "presentation.xml").read_bytes() == before


def test_add_slide_duplicate_copies_content_and_drops_notes(deck, add_slide, capsys):
    source = (deck / "ppt" / "slides" / "slide1.xml").read_bytes()

    assert add_slide.main([str(deck), "slide1.xml"]) == 0

    assert capsys.readouterr().out.splitlines()[0] == "Created slide3.xml from slide1.xml"
    assert (deck / "ppt" / "slides" / "slide3.xml").read_bytes() == source

    rels = (deck / "ppt" / "slides" / "_rels" / "slide3.xml.rels").read_text(encoding="utf-8")
    assert "notesSlide" not in rels
    assert "../media/kept.png" in rels
    # The source keeps its own notes relationship.
    assert "notesSlide" in (deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels").read_text()


def test_add_slide_numbering_continues_past_the_highest_in_use(deck, add_slide, capsys):
    (deck / "ppt" / "slides" / "slide9.xml").write_text(_slide("Nine"), encoding="utf-8")
    pres_rels = deck / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels.write_text(
        pres_rels.read_text().replace('Id="rId3"', 'Id="rId12"'), encoding="utf-8"
    )

    assert add_slide.main([str(deck), "slideLayout1.xml"]) == 0

    out = capsys.readouterr().out.splitlines()
    assert out[0] == "Created slide10.xml from slideLayout1.xml"
    assert 'r:id="rId13"' in out[1]


def test_add_slide_second_run_adds_a_second_relationship(deck, add_slide, capsys):
    assert add_slide.main([str(deck), "slideLayout1.xml"]) == 0
    capsys.readouterr()
    assert add_slide.main([str(deck), "slideLayout1.xml"]) == 0

    assert capsys.readouterr().out.splitlines()[0] == "Created slide4.xml from slideLayout1.xml"
    rels = (deck / "ppt" / "_rels" / "presentation.xml.rels").read_text(encoding="utf-8")
    assert 'Target="slides/slide3.xml"' in rels and 'Target="slides/slide4.xml"' in rels


@pytest.mark.parametrize(
    "argv, message",
    [
        ([], "Usage: python add_slide.py"),
        (["only-one"], "Usage: python add_slide.py"),
        (["a", "b", "c"], "Usage: python add_slide.py"),
    ],
)
def test_add_slide_usage_errors(deck, add_slide, capsys, argv, message):
    assert add_slide.main(argv) == 1
    captured = capsys.readouterr()
    assert message in captured.err
    assert captured.out == ""


def test_add_slide_missing_operand_is_reported(deck, add_slide, capsys, tmp_path):
    assert add_slide.main([str(deck), "slideLayout7.xml"]) == 1
    assert "slideLayout7.xml not found" in capsys.readouterr().err

    assert add_slide.main([str(deck), "slide7.xml"]) == 1
    assert "slide7.xml not found" in capsys.readouterr().err

    assert add_slide.main([str(tmp_path / "absent"), "slide1.xml"]) == 1
    assert "not found" in capsys.readouterr().err


# --------------------------------------------------------------------------- #
# clean.py
# --------------------------------------------------------------------------- #
def test_clean_removes_a_slide_dropped_from_the_slide_list(deck, clean, capsys):
    _drop_slide_from_list(deck, "257")

    assert clean.main([str(deck)]) == 0

    out = capsys.readouterr().out
    assert out.startswith("Removed ")
    assert "ppt/slides/slide2.xml" in out
    assert "ppt/slides/_rels/slide2.xml.rels" in out
    assert not (deck / "ppt" / "slides" / "slide2.xml").exists()
    assert (deck / "ppt" / "slides" / "slide1.xml").exists()

    pres_rels = (deck / "ppt" / "_rels" / "presentation.xml.rels").read_text(encoding="utf-8")
    assert 'Target="slides/slide2.xml"' not in pres_rels
    assert 'Target="slides/slide1.xml"' in pres_rels
    assert 'PartName="/ppt/slides/slide2.xml"' not in (deck / "[Content_Types].xml").read_text()


def test_clean_keeps_referenced_media_and_removes_the_rest(deck, clean, capsys):
    assert clean.main([str(deck)]) == 0

    assert "ppt/media/orphan.png" in capsys.readouterr().out
    assert (deck / "ppt" / "media" / "kept.png").exists()
    assert not (deck / "ppt" / "media" / "orphan.png").exists()


def test_clean_removes_the_parked_parts_directory(deck, clean, capsys):
    (deck / "[trash]" / "nested").mkdir()
    (deck / "[trash]" / "nested" / "deep.xml").write_text("<deep/>", encoding="utf-8")

    assert clean.main([str(deck)]) == 0

    out = capsys.readouterr().out
    assert "[trash]/parked.xml" in out
    assert "[trash]/nested/deep.xml" in out
    assert not (deck / "[trash]").exists()


def test_clean_removes_notes_whose_slide_no_longer_names_them(deck, clean, capsys):
    rels = deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels"
    text = rels.read_text(encoding="utf-8")
    start = text.index('<Relationship Id="rId3"')
    rels.write_text(text[:start] + text[text.index("/>", start) + 2:], encoding="utf-8")

    assert clean.main([str(deck)]) == 0

    out = capsys.readouterr().out
    assert "ppt/notesSlides/notesSlide1.xml" in out
    assert "ppt/notesSlides/_rels/notesSlide1.xml.rels" in out
    assert not (deck / "ppt" / "notesSlides" / "notesSlide1.xml").exists()


def test_clean_removes_an_unreferenced_theme_with_its_relationships(deck, clean, capsys):
    rels = deck / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
    text = rels.read_text(encoding="utf-8")
    start = text.index('<Relationship Id="rId2"')
    rels.write_text(text[:start] + text[text.index("/>", start) + 2:], encoding="utf-8")

    assert clean.main([str(deck)]) == 0

    out = capsys.readouterr().out
    assert "ppt/theme/theme1.xml" in out
    assert not (deck / "ppt" / "theme" / "theme1.xml").exists()
    assert not (deck / "ppt" / "theme" / "_rels" / "theme1.xml.rels").exists()


def test_clean_reaches_a_fixed_point(deck, clean, capsys):
    """A chart that nothing names takes the picture it embedded with it."""
    charts = deck / "ppt" / "charts"
    (charts / "_rels").mkdir(parents=True)
    (charts / "chart1.xml").write_text("<chart/>", encoding="utf-8")
    (charts / "_rels" / "chart1.xml.rels").write_text(
        _rels(("rId1", "image", "../media/chart-image.png")), encoding="utf-8"
    )
    (deck / "ppt" / "media" / "chart-image.png").write_bytes(b"\x89PNGchart")

    assert clean.main([str(deck)]) == 0

    out = capsys.readouterr().out
    assert "ppt/charts/chart1.xml" in out
    assert "ppt/charts/_rels/chart1.xml.rels" in out
    assert "ppt/media/chart-image.png" in out
    assert not (charts / "chart1.xml").exists()
    assert not (deck / "ppt" / "media" / "chart-image.png").exists()


def test_clean_on_a_tidy_tree_reports_nothing_and_deletes_nothing(deck, clean, capsys):
    (deck / "ppt" / "media" / "orphan.png").unlink()
    import shutil

    shutil.rmtree(deck / "[trash]")
    before = {p.relative_to(deck).as_posix() for p in deck.rglob("*") if p.is_file()}

    assert clean.main([str(deck)]) == 0

    assert capsys.readouterr().out.strip() == "No unreferenced files found"
    after = {p.relative_to(deck).as_posix() for p in deck.rglob("*") if p.is_file()}
    assert after == before


def test_clean_keeps_a_part_named_by_an_external_relationship(deck, clean, capsys):
    """An external target names no part, so it cannot keep a local file alive."""
    rels = deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels"
    rels.write_text(
        rels.read_text(encoding="utf-8").replace(
            "</Relationships>",
            '<Relationship Id="rId9" Type="%s/hyperlink" Target="https://example.invalid/x" TargetMode="External"/>'
            "</Relationships>" % R_NS,
        ),
        encoding="utf-8",
    )

    assert clean.main([str(deck)]) == 0

    assert "ppt/media/orphan.png" in capsys.readouterr().out
    assert (deck / "ppt" / "media" / "kept.png").exists()


@pytest.mark.parametrize("argv", [[], ["a", "b"]])
def test_clean_usage_errors(clean, capsys, argv):
    assert clean.main(argv) == 1
    captured = capsys.readouterr()
    assert "Usage: python clean.py" in captured.err
    assert captured.out == ""


def test_clean_missing_directory(clean, capsys, tmp_path):
    assert clean.main([str(tmp_path / "absent")]) == 1
    assert "not found" in capsys.readouterr().err


# --------------------------------------------------------------------------- #
# Part plumbing: the guards that make hand-edited input safe
# --------------------------------------------------------------------------- #
def test_parts_refuse_a_dtd(deck, parts, clean, capsys):
    payload = (
        '<?xml version="1.0"?>\n'
        '<!DOCTYPE Relationships [<!ENTITY a "aaaaaaaaaa"><!ENTITY b "&a;&a;&a;&a;&a;">]>\n'
        '<Relationships xmlns="%s">&b;</Relationships>' % PR_NS
    )
    (deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels").write_text(payload, encoding="utf-8")

    with pytest.raises(parts.OoxmlError):
        parts.parse_file(deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels")

    assert clean.main([str(deck)]) == 1
    assert "DTD" in capsys.readouterr().err


def test_parts_refuse_a_target_that_climbs_out_of_the_package(deck, parts):
    rels_file = deck / "ppt" / "slides" / "_rels" / "slide1.xml.rels"
    assert parts.resolve_target(rels_file, "../../../../etc/passwd", deck) is None
    assert parts.resolve_target(rels_file, "https://example.invalid/a.png", deck) is None
    assert parts.resolve_target(rels_file, "", deck) is None
    assert parts.resolve_target(rels_file, "../media/kept.png", deck) == Path("ppt/media/kept.png")


def test_rewrite_keeps_namespace_declarations_it_did_not_use(deck, parts):
    """A prefix named by mc:Ignorable must survive a relationship prune."""
    rels = deck / "ppt" / "_rels" / "presentation.xml.rels"
    original = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:unused="http://example.invalid/unused" mc:Ignorable="unused">\n'
        '  <Relationship Id="rId2" Type="%s/slide" Target="slides/slide1.xml"/>\n'
        '  <Relationship Id="rId3" Type="%s/slide" Target="slides/slide2.xml"/>\n'
        "</Relationships>" % (PR_NS, R_NS, R_NS)
    )
    rels.write_text(original, encoding="utf-8")
    _drop_slide_from_list(deck, "257")

    doc = parts.parse_file(rels)
    for rel in parts.relationships(doc):
        if parts.attr(rel, "Target") == "slides/slide2.xml":
            parts.remove_element(rel)
    parts.write_part(rels, doc)

    written = rels.read_text(encoding="utf-8")
    assert 'xmlns:unused="http://example.invalid/unused"' in written
    assert 'mc:Ignorable="unused"' in written
    assert 'Target="slides/slide1.xml"' in written
    assert 'Target="slides/slide2.xml"' not in written
    # The surviving relationship keeps the indentation it was written with.
    assert '\n  <Relationship Id="rId2"' in written


def test_hidden_flag_reads_the_slide_attribute_not_the_slide_list(parts):
    assert parts.hidden_flag("0") is True
    assert parts.hidden_flag("false") is True
    assert parts.hidden_flag(None) is False
    assert parts.hidden_flag("1") is False
    assert parts.hidden_flag("true") is False