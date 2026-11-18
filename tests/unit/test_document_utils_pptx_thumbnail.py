"""Contract of pptx/thumbnail.py, and the package validity of the tree scripts.

LibreOffice is not a test dependency: the converter step is replaced by a fake
that writes a real PDF with the page count the case needs, and everything after
it -- PDFium rasterization, Pillow composition, grid naming, the stdout report --
runs for real.  The deck itself is built with python-pptx, so the slide inventory
is read from a genuine package rather than from a hand-written approximation.

The last group closes the loop the other way round: a deck built with python-pptx
is unpacked, edited with add_slide.py and clean.py, repacked, and reopened with
python-pptx.  That is the library-based check that the part surgery those two
scripts do leaves a package a reader still accepts.
"""

import importlib.util
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

pytest.importorskip("pptx", reason="python-pptx is the pptx family's deck library")
pdfium = pytest.importorskip("pypdfium2", reason="PDFium rasterizes the converted deck")
pytest.importorskip("PIL", reason="Pillow composes the grids")

from PIL import Image  # noqa: E402 -- after the availability guards above
from pptx import Presentation  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts"


def _load(script_name: str, module_name: str):
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
def thumbnail():
    return _load("thumbnail.py", "_f3_pptx_thumbnail")


@pytest.fixture(scope="module")
def add_slide():
    return _load("add_slide.py", "_f3_pptx_add_slide_cli")


@pytest.fixture(scope="module")
def clean():
    return _load("clean.py", "_f3_pptx_clean_cli")


def build_deck(path: Path, count: int = 3, hidden=()) -> Path:
    """A real deck: ``count`` slides, the ones named in ``hidden`` marked hidden."""
    presentation = Presentation()
    for index in range(count):
        slide = presentation.slides.add_slide(presentation.slide_layouts[1])
        slide.shapes.title.text = f"Slide {index + 1}"
        if index + 1 in hidden:
            slide.element.set("show", "0")
    presentation.save(str(path))
    return path


@pytest.fixture
def deck(tmp_path: Path) -> Path:
    return build_deck(tmp_path / "deck.pptx", count=3, hidden=(2,))


@pytest.fixture
def fake_soffice(monkeypatch, thumbnail):
    """Replace the converter with one that writes a real PDF of a given size."""
    real_run = subprocess.run
    calls: list[list[str]] = []
    state = {"pages": 3, "returncode": 0, "write_pdf": True}

    def run(cmd, **kwargs):
        if cmd and cmd[0] == "soffice" and "--convert-to" in cmd:
            calls.append(list(cmd))
            outdir = Path(cmd[cmd.index("--outdir") + 1])
            source = Path(cmd[-1])
            if state["write_pdf"]:
                document = pdfium.PdfDocument.new()
                for _ in range(state["pages"]):
                    document.new_page(720, 540)
                document.save(str(outdir / f"{source.stem}.pdf"))
                document.close()
            return subprocess.CompletedProcess(cmd, state["returncode"], "", "")
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(thumbnail.subprocess, "run", run)
    return state, calls


# --------------------------------------------------------------------------- #
# Reading the deck
# --------------------------------------------------------------------------- #
def test_inventory_follows_presentation_order_and_reads_the_hidden_flag(deck, thumbnail):
    assert thumbnail.slide_inventory(deck) == [
        ("slide1.xml", False),
        ("slide2.xml", True),
        ("slide3.xml", False),
    ]


def test_inventory_of_a_deck_without_slides_is_empty(tmp_path, thumbnail):
    empty = tmp_path / "empty.pptx"
    Presentation().save(str(empty))
    assert thumbnail.slide_inventory(empty) == []


def test_labels_name_the_parts_on_disk_not_a_renumbered_sequence(tmp_path, thumbnail, clean, capsys):
    """A gapped deck keeps its own file names.

    python-pptx assigns slide1..slideN in memory when ``.slides`` is first read.
    A label drawn from that renumbering would point a reviewer at a part that
    does not exist, so the inventory has to report the names the package carries.
    """
    deck = build_deck(tmp_path / "source.pptx", count=3)
    tree = _unpack(deck, tmp_path / "unpacked")
    presentation = tree / "ppt" / "presentation.xml"
    text = presentation.read_text(encoding="utf-8")
    start = text.index('<p:sldId id="257"')
    presentation.write_text(
        text[:start] + text[text.index("/>", start) + 2:], encoding="utf-8"
    )
    assert clean.main([str(tree)]) == 0
    capsys.readouterr()
    gapped = _pack(tree, tmp_path / "gapped.pptx")

    assert thumbnail.slide_inventory(gapped) == [
        ("slide1.xml", False),
        ("slide3.xml", False),
    ]


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #
def test_default_run_writes_one_grid_named_thumbnails(deck, thumbnail, fake_soffice, monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    assert thumbnail.main([str(deck)]) == 0

    out = capsys.readouterr().out.splitlines()
    assert out[0] == "Created 1 grid(s):"
    assert out[1].strip() == "thumbnails.jpg"
    with Image.open(tmp_path / "thumbnails.jpg") as grid:
        # Three cells of 300 px, four gutters of 20 px; a 4:3 page renders to
        # 300x225 at 100 dpi, plus a 30 px label band and two gutters.
        assert grid.size == (980, 295)


def test_prefix_and_cols_shape_the_output(deck, thumbnail, fake_soffice, monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    assert thumbnail.main([str(deck), "review", "--cols", "2"]) == 0

    assert "review.jpg" in capsys.readouterr().out
    with Image.open(tmp_path / "review.jpg") as grid:
        # Two columns: three gutters of 20 px across, and two rows of 255 px
        # (225 px of slide plus a 30 px label band) with three gutters down.
        assert grid.size == (660, 570)


def test_cols_above_the_maximum_are_clamped_and_announced(deck, thumbnail, fake_soffice, monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    assert thumbnail.main([str(deck), "wide", "--cols", "9"]) == 0

    out = capsys.readouterr().out.splitlines()
    assert out[0] == "Warning: Columns limited to 6"
    with Image.open(tmp_path / "wide.jpg") as grid:
        assert grid.size == (20 * 7 + 300 * 6, 295)


def test_cols_below_one_is_rejected(deck, thumbnail, fake_soffice, capsys):
    assert thumbnail.main([str(deck), "--cols", "0"]) == 1
    assert "--cols must be at least 1" in capsys.readouterr().err


def test_a_long_deck_splits_into_numbered_grids(tmp_path, thumbnail, fake_soffice, monkeypatch, capsys):
    long_deck = build_deck(tmp_path / "long.pptx", count=14)
    fake_soffice[0]["pages"] = 14
    monkeypatch.chdir(tmp_path)

    assert thumbnail.main([str(long_deck), "grid"]) == 0

    out = capsys.readouterr().out.splitlines()
    assert out[0] == "Created 2 grid(s):"
    assert [line.strip() for line in out[1:]] == ["grid-1.jpg", "grid-2.jpg"]
    assert (tmp_path / "grid-1.jpg").is_file()
    assert (tmp_path / "grid-2.jpg").is_file()
    assert not (tmp_path / "grid.jpg").exists()


@pytest.mark.parametrize("name", ["absent.pptx", "notes.txt"])
def test_input_that_is_not_a_deck_is_rejected(tmp_path, thumbnail, fake_soffice, capsys, name):
    if name == "notes.txt":
        (tmp_path / name).write_text("not a deck", encoding="utf-8")

    assert thumbnail.main([str(tmp_path / name)]) == 1
    assert f"Error: Invalid PowerPoint file: {tmp_path / name}" in capsys.readouterr().err


def test_a_failed_conversion_is_reported(deck, thumbnail, fake_soffice, capsys):
    fake_soffice[0].update(returncode=1, write_pdf=False)

    assert thumbnail.main([str(deck)]) == 1
    assert "Error: LibreOffice did not produce a PDF" in capsys.readouterr().err


def test_a_deck_without_slides_reports_no_slides(tmp_path, thumbnail, fake_soffice, capsys):
    empty = tmp_path / "empty.pptx"
    Presentation().save(str(empty))

    assert thumbnail.main([str(empty)]) == 1
    assert "Error: No slides found" in capsys.readouterr().err


def test_converter_is_asked_for_a_pdf_of_this_deck(deck, thumbnail, fake_soffice, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert thumbnail.main([str(deck)]) == 0

    state, calls = fake_soffice
    assert len(calls) == 1
    command = calls[0]
    assert command[0] == "soffice"
    assert "--headless" in command
    assert command[command.index("--convert-to") + 1] == "pdf"
    assert command[-1] == str(deck)


# --------------------------------------------------------------------------- #
# Hidden slides and partial exports
# --------------------------------------------------------------------------- #
def _render_pages(work: Path, count: int) -> list[Path]:
    """Rasterize a real ``count``-page PDF the way the converter step would."""
    pdf = work / "converted.pdf"
    document = pdfium.PdfDocument.new()
    for _ in range(count):
        document.new_page(720, 540)
    document.save(str(pdf))
    document.close()

    reopened = pdfium.PdfDocument(str(pdf))
    images = []
    try:
        for index in range(len(reopened)):
            target = work / f"slide-{index + 1:03d}.jpg"
            reopened[index].render(scale=100 / 72).to_pil().convert("RGB").save(target, "JPEG")
            images.append(target)
    finally:
        reopened.close()
    return images


def test_a_skipped_hidden_slide_becomes_a_labelled_placeholder(deck, thumbnail, fake_soffice, tmp_path):
    fake_soffice[0]["pages"] = 2  # the converter exported the visible slides only
    work = tmp_path / "work"
    work.mkdir()
    rendered = _render_pages(work, 2)

    pairs = thumbnail.pair_slides(thumbnail.slide_inventory(deck), rendered, work)

    assert [label for _, label in pairs] == [
        "slide1.xml",
        "slide2.xml (hidden)",
        "slide3.xml",
    ]
    assert pairs[1][0].name == "hidden-slide2.xml.jpg"
    with Image.open(pairs[1][0]) as placeholder:
        assert placeholder.size == (1000, 750)


def test_an_exported_hidden_slide_keeps_its_own_render(deck, thumbnail, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    rendered = _render_pages(work, 3)

    pairs = thumbnail.pair_slides(thumbnail.slide_inventory(deck), rendered, work)

    assert [path.name for path, _ in pairs] == [path.name for path in rendered]
    assert pairs[1][1] == "slide2.xml (hidden)"


# --------------------------------------------------------------------------- #
# The office wrapper owns the LibreOffice environment
# --------------------------------------------------------------------------- #
def test_soffice_env_delegates_to_the_office_wrapper(thumbnail, monkeypatch):
    import types

    sentinel = {"SAL_USE_VCLPLUGIN": "svp", "MARKER": "from-the-wrapper"}
    package = types.ModuleType("office")
    package.__path__ = []
    wrapper = types.ModuleType("office.soffice")
    wrapper.get_soffice_env = lambda: sentinel
    monkeypatch.setitem(sys.modules, "office", package)
    monkeypatch.setitem(sys.modules, "office.soffice", wrapper)

    assert thumbnail._soffice_env() is sentinel


def test_soffice_env_survives_a_tree_without_the_wrapper(thumbnail, monkeypatch):
    # A None entry in sys.modules is how Python reports "this import fails".
    monkeypatch.setitem(sys.modules, "office", None)
    monkeypatch.setitem(sys.modules, "office.soffice", None)

    env = thumbnail._soffice_env()
    assert env["PATH"] == __import__("os").environ["PATH"]


# --------------------------------------------------------------------------- #
# The tree scripts leave a package a reader accepts
# --------------------------------------------------------------------------- #
def _unpack(deck: Path, target: Path) -> Path:
    with zipfile.ZipFile(deck) as archive:
        archive.extractall(target)
    return target


def _pack(tree: Path, target: Path) -> Path:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for part in sorted(tree.rglob("*")):
            if part.is_file():
                archive.write(part, part.relative_to(tree).as_posix())
    return target


def test_add_slide_then_clean_round_trips_through_python_pptx(tmp_path, add_slide, clean, capsys):
    deck = build_deck(tmp_path / "source.pptx", count=3)
    tree = _unpack(deck, tmp_path / "unpacked")

    assert add_slide.main([str(tree), "slideLayout2.xml"]) == 0
    printed = capsys.readouterr().out.splitlines()[1]
    match = re.search(r'<p:sldId id="(\d+)" r:id="([^"]+)"/>', printed)
    assert match, printed

    # The caller inserts the printed element where the new slide belongs.
    presentation = tree / "ppt" / "presentation.xml"
    text = presentation.read_text(encoding="utf-8")
    presentation.write_text(
        text.replace("</p:sldIdLst>", match.group(0) + "</p:sldIdLst>"), encoding="utf-8"
    )

    # A slide dropped from the list, and a picture nothing names any more.
    text = presentation.read_text(encoding="utf-8")
    start = text.index('<p:sldId id="257"')
    presentation.write_text(
        text[:start] + text[text.index("/>", start) + 2:], encoding="utf-8"
    )
    (tree / "ppt" / "media").mkdir(exist_ok=True)
    (tree / "ppt" / "media" / "stray.png").write_bytes(b"\x89PNGstray")

    assert clean.main([str(tree)]) == 0
    reported = capsys.readouterr().out
    assert "ppt/slides/slide2.xml" in reported
    assert "ppt/media/stray.png" in reported

    reopened = Presentation(str(_pack(tree, tmp_path / "edited.pptx")))
    # Read the package's own part names first: touching .slides renumbers them
    # in memory, which is a python-pptx convenience and not what is on disk.
    on_disk = sorted(
        str(part.partname)
        for part in reopened.part.package.iter_parts()
        if str(part.partname).startswith("/ppt/slides/slide")
    )
    assert on_disk == [
        "/ppt/slides/slide1.xml",
        "/ppt/slides/slide3.xml",
        "/ppt/slides/slide4.xml",
    ]
    assert len(reopened.slides) == 3
    assert reopened.slides[2].slide_layout.name == "Title and Content"
    assert not (tree / "ppt" / "slides" / "slide2.xml").exists()


def test_duplicate_of_a_real_slide_round_trips(tmp_path, add_slide, capsys):
    deck = build_deck(tmp_path / "source.pptx", count=2)
    tree = _unpack(deck, tmp_path / "unpacked")

    assert add_slide.main([str(tree), "slide1.xml"]) == 0
    printed = capsys.readouterr().out.splitlines()[1]
    element = re.search(r'<p:sldId id="\d+" r:id="[^"]+"/>', printed).group(0)
    presentation = tree / "ppt" / "presentation.xml"
    presentation.write_text(
        presentation.read_text(encoding="utf-8").replace("</p:sldIdLst>", element + "</p:sldIdLst>"),
        encoding="utf-8",
    )

    reopened = Presentation(str(_pack(tree, tmp_path / "edited.pptx")))
    assert len(reopened.slides._sldIdLst) == 3
    assert reopened.slides[2].shapes.title.text == "Slide 1"


# --------------------------------------------------------------------------- #
# The flag entry layer answers without the runtime dependencies
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "flag, code", [("--help", 0), ("-h", 0), ("--version", 0), ("--not-an-option", 2)]
)
def test_flag_entry_layer(flag, code):
    finished = subprocess.run(
        [sys.executable, str(SCRIPTS / "pptx" / "thumbnail.py"), flag],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert finished.returncode == code
    if flag == "--version":
        assert re.fullmatch(r"thumbnail\.py \S+\n?", finished.stdout)