"""DOCX revision acceptance, comment writing, and the LibreOffice wrapper.

The revision and comment cases build a small package, run the real script, and
read the result back: what is pinned is the markup a reader would open, not the
internal call sequence. The LibreOffice cases never start LibreOffice — the
subprocess boundary is recorded by a fake, so the command line, the environment
and the profile isolation are asserted without the program being installed.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import document_utils_office as fx

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts"
OFFICE = SCRIPTS / "office"
DOCX = SCRIPTS / "docx"
STAMP = 'w:date="2026-01-01T00:00:00Z"'


@pytest.fixture(scope="module", autouse=True)
def office_on_path():
    saved = list(sys.path)
    sys.path.insert(0, str(OFFICE))
    yield
    sys.path[:] = saved


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def accept_module():
    return load(DOCX / "accept_changes.py", "_du_docx_accept")


@pytest.fixture(scope="module")
def comment_module():
    return load(DOCX / "comment.py", "_du_docx_comment")


@pytest.fixture(scope="module")
def soffice_module():
    return load(OFFICE / "soffice.py", "_du_office_soffice")


def run_cli(script: Path, *args, cwd):
    return subprocess.run(
        [sys.executable, str(script), *[str(arg) for arg in args]],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=120,
    )


def document_of(path: Path):
    import ooxml as ox

    return ox.parse_string(fx.read_part(path, "word/document.xml")).documentElement


def tags(root) -> list:
    import ooxml as ox

    return [ox.local_name(node) for node in ox.iter_elements(root)]


def text_of(root) -> str:
    import ooxml as ox

    return "".join(ox.text_of(node) for node in ox.iter_elements(root, "t"))


# --------------------------------------------------------------------------- #
# Accepting tracked changes
# --------------------------------------------------------------------------- #
def test_insertions_stay_and_deletions_go(tmp_path, accept_module):
    body = (
        '<w:p><w:r><w:t>Keep</w:t></w:r>'
        f'<w:ins w:id="1" w:author="Claude" {STAMP}><w:r><w:t xml:space="preserve"> added</w:t></w:r></w:ins>'
        f'<w:del w:id="2" w:author="Claude" {STAMP}><w:r><w:delText> removed</w:delText></w:r></w:del>'
        "</w:p>"
    )
    source = fx.write_package(tmp_path / "redlined.docx", fx.docx_parts(body=body))
    before = source.read_bytes()
    target = tmp_path / "clean.docx"

    _, message = accept_module.accept_changes(str(source), str(target))
    assert message == f"Successfully accepted all tracked changes: {source} -> {target}"
    assert source.read_bytes() == before, "the input package must not be touched"

    root = document_of(target)
    assert "ins" not in tags(root)
    assert "del" not in tags(root)
    assert "delText" not in tags(root)
    assert text_of(root) == "Keep added"


def test_deleted_paragraph_mark_joins_the_paragraphs(tmp_path, accept_module):
    body = (
        '<w:p><w:pPr><w:rPr><w:del w:id="1" w:author="Claude" ' + STAMP + '/></w:rPr></w:pPr>'
        '<w:r><w:t>first</w:t></w:r></w:p>'
        '<w:p><w:r><w:t xml:space="preserve"> second</w:t></w:r></w:p>'
    )
    source = fx.write_package(tmp_path / "redlined.docx", fx.docx_parts(body=body))
    target = tmp_path / "clean.docx"
    accept_module.accept_changes(str(source), str(target))

    import ooxml as ox

    root = document_of(target)
    paragraphs = list(ox.iter_elements(root, "p"))
    assert len(paragraphs) == 1
    assert text_of(root) == "first second"


def test_moves_and_formatting_revisions_are_applied(tmp_path, accept_module):
    body = (
        '<w:p><w:r><w:rPr><w:b/><w:rPrChange w:id="1" w:author="Claude" ' + STAMP + '>'
        '<w:rPr><w:i/></w:rPr></w:rPrChange></w:rPr><w:t>text</w:t></w:r>'
        f'<w:moveTo w:id="2" w:author="Claude" {STAMP}><w:r><w:t xml:space="preserve"> moved</w:t></w:r></w:moveTo>'
        f'<w:moveFrom w:id="3" w:author="Claude" {STAMP}><w:r><w:delText> gone</w:delText></w:r></w:moveFrom>'
        '<w:moveFromRangeStart w:id="4" w:name="m"/><w:moveFromRangeEnd w:id="4"/>'
        "</w:p>"
    )
    source = fx.write_package(tmp_path / "redlined.docx", fx.docx_parts(body=body))
    target = tmp_path / "clean.docx"
    accept_module.accept_changes(str(source), str(target))
    root = document_of(target)
    for gone in ("moveTo", "moveFrom", "moveFromRangeStart", "moveFromRangeEnd", "rPrChange"):
        assert gone not in tags(root)
    assert text_of(root) == "text moved"
    assert "b" in tags(root), "the new formatting survives the accepted revision"


def test_parts_without_revisions_are_copied_byte_for_byte(tmp_path, accept_module):
    parts = fx.docx_parts()
    source = fx.write_package(tmp_path / "plain.docx", parts)
    target = tmp_path / "clean.docx"
    _, message = accept_module.accept_changes(str(source), str(target))
    assert message.startswith("Successfully"), message
    assert fx.read_part(target, "word/styles.xml") == parts["word/styles.xml"]


def test_accept_changes_refuses_bad_input(tmp_path, accept_module):
    _, missing = accept_module.accept_changes(str(tmp_path / "absent.docx"), str(tmp_path / "out.docx"))
    assert missing.startswith("Error: Input file not found")

    text_file = tmp_path / "note.txt"
    text_file.write_text("text", encoding="utf-8")
    _, wrong_type = accept_module.accept_changes(str(text_file), str(tmp_path / "out.docx"))
    assert "is not a DOCX file" in wrong_type

    broken = tmp_path / "broken.docx"
    broken.write_bytes(b"not a zip")
    _, corrupt = accept_module.accept_changes(str(broken), str(tmp_path / "out.docx"))
    assert "not a valid DOCX package" in corrupt


def test_accept_changes_cli_answers_flags_and_reports(tmp_path):
    helped = run_cli(DOCX / "accept_changes.py", "--help", cwd=tmp_path)
    assert helped.returncode == 0
    version = run_cli(DOCX / "accept_changes.py", "--version", cwd=tmp_path)
    assert version.returncode == 0 and version.stdout.startswith("accept_changes.py ")
    refused = run_cli(DOCX / "accept_changes.py", "--bogus", cwd=tmp_path)
    assert refused.returncode == 2

    body = f'<w:p><w:ins w:id="1" w:author="Claude" {STAMP}><w:r><w:t>added</w:t></w:r></w:ins></w:p>'
    source = fx.write_package(tmp_path / "redlined.docx", fx.docx_parts(body=body))
    target = tmp_path / "clean.docx"
    ran = run_cli(DOCX / "accept_changes.py", source, target, cwd=tmp_path)
    assert ran.returncode == 0, ran.stdout + ran.stderr
    assert "Successfully accepted all tracked changes" in ran.stdout
    assert target.is_file()


# --------------------------------------------------------------------------- #
# Comments
# --------------------------------------------------------------------------- #
def test_comment_writes_all_four_parts_and_registers_them(tmp_path, comment_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    para_id, message = comment_module.add_comment(str(tree), 0, "First note", author="Reviewer", initials="R")
    assert message == f"Added comment 0 (para_id={para_id})"
    assert len(para_id) == 8 and int(para_id, 16) < 0x80000000

    import ooxml as ox

    for name in ("comments.xml", "commentsExtended.xml", "commentsIds.xml", "commentsExtensible.xml"):
        assert (tree / "word" / name).is_file(), name

    comments = ox.parse_file(tree / "word" / "comments.xml")
    comment = next(ox.iter_elements(comments.documentElement, "comment"))
    assert ox.get_attr(comment, "id") == "0"
    assert ox.get_attr(comment, "author") == "Reviewer"
    assert ox.get_attr(comment, "initials") == "R"
    assert text_of(comment) == "First note"

    rels = ox.parse_file(tree / "word" / "_rels" / "document.xml.rels")
    targets = {ox.get_attr(node, "Target") for node in ox.iter_elements(rels.documentElement, "Relationship")}
    assert {"comments.xml", "commentsExtended.xml", "commentsIds.xml", "commentsExtensible.xml"} <= targets

    types = ox.parse_file(tree / "[Content_Types].xml")
    parts = {ox.get_attr(node, "PartName") for node in ox.iter_elements(types.documentElement, "Override")}
    assert "/word/comments.xml" in parts and "/word/commentsExtensible.xml" in parts


def test_reply_threads_to_the_parent_paragraph(tmp_path, comment_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    parent_para, _ = comment_module.add_comment(str(tree), 0, "Parent note")
    reply_para, message = comment_module.add_comment(str(tree), 1, "Reply note", parent_id=0)
    assert message == f"Added reply 1 (para_id={reply_para})"
    assert reply_para != parent_para

    import ooxml as ox

    extended = ox.parse_file(tree / "word" / "commentsExtended.xml")
    entries = list(ox.iter_elements(extended.documentElement, "commentEx"))
    assert len(entries) == 2
    assert ox.get_attr(entries[1], "paraIdParent") == parent_para
    assert ox.get_attr(entries[0], "paraIdParent") is None


def test_second_comment_appends_and_keeps_ids_unique(tmp_path, comment_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    first, _ = comment_module.add_comment(str(tree), 0, "One")
    second, _ = comment_module.add_comment(str(tree), 1, "Two")
    assert first != second

    import ooxml as ox

    comments = ox.parse_file(tree / "word" / "comments.xml")
    assert [ox.get_attr(node, "id") for node in ox.iter_elements(comments.documentElement, "comment")] == ["0", "1"]
    rels = ox.parse_file(tree / "word" / "_rels" / "document.xml.rels")
    targets = [
        ox.get_attr(node, "Target")
        for node in ox.iter_elements(rels.documentElement, "Relationship")
        if ox.get_attr(node, "Target") == "comments.xml"
    ]
    assert len(targets) == 1, "registration must be idempotent"


def test_comment_text_is_escaped_not_interpolated(tmp_path, comment_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    tricky = 'a & b < c > d "quoted"'
    comment_module.add_comment(str(tree), 0, tricky)

    import ooxml as ox

    comments = ox.parse_file(tree / "word" / "comments.xml")
    assert text_of(comments.documentElement) == tricky


def test_comment_refuses_a_missing_parent_without_writing(tmp_path, comment_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    para_id, message = comment_module.add_comment(str(tree), 1, "Orphan reply", parent_id=99)
    assert para_id == ""
    assert message == "Error: Parent comment 99 not found"
    assert not (tree / "word" / "comments.xml").exists()


def test_comment_refuses_a_tree_without_word(tmp_path, comment_module):
    empty = tmp_path / "empty"
    empty.mkdir()
    para_id, message = comment_module.add_comment(str(empty), 0, "note")
    assert para_id == ""
    assert message == f"Error: {empty / 'word'} not found"


def test_comment_cli_prints_the_marker_markup(tmp_path):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    ran = run_cli(DOCX / "comment.py", tree, 0, "A note", "--author", "Reviewer", cwd=tmp_path)
    assert ran.returncode == 0, ran.stdout + ran.stderr
    assert "Added comment 0" in ran.stdout
    assert '<w:commentRangeStart w:id="0"/>' in ran.stdout
    assert '<w:commentReference w:id="0"/>' in ran.stdout

    replied = run_cli(DOCX / "comment.py", tree, 1, "A reply", "--parent", "0", cwd=tmp_path)
    assert replied.returncode == 0, replied.stdout + replied.stderr
    assert "Added reply 1" in replied.stdout
    assert '<w:commentRangeStart w:id="0"/><w:commentRangeStart w:id="1"/>' in replied.stdout

    helped = run_cli(DOCX / "comment.py", "--help", cwd=tmp_path)
    assert helped.returncode == 0
    for flag in ("--author", "--initials", "--parent"):
        assert flag in helped.stdout


def test_commented_tree_passes_validation_end_to_end(tmp_path, comment_module):
    """The workflow a reader actually performs: comment, place markers, validate."""
    parts = fx.docx_parts()
    original = fx.write_package(tmp_path / "original.docx", parts)
    tree = fx.write_tree(tmp_path / "unpacked", parts)
    comment_module.add_comment(str(tree), 0, "Is this figure final?")

    document = tree / "word" / "document.xml"
    markup = document.read_text(encoding="utf-8")
    marked = markup.replace(
        "<w:r><w:t>Hello document</w:t></w:r>",
        '<w:commentRangeStart w:id="0"/><w:r><w:t>Hello document</w:t></w:r>'
        '<w:commentRangeEnd w:id="0"/>'
        '<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>',
    )
    assert marked != markup
    document.write_text(marked, encoding="utf-8")

    result = run_cli(OFFICE / "validate.py", tree, "--original", original, cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All validations PASSED!" in result.stdout


# --------------------------------------------------------------------------- #
# The LibreOffice wrapper (no LibreOffice required)
# --------------------------------------------------------------------------- #
def test_env_selects_the_headless_plugin_without_touching_the_process(monkeypatch, soffice_module):
    import os

    monkeypatch.setenv("DOCUMENT_UTILS_PROBE", "kept")
    env = soffice_module.get_soffice_env()
    assert env["SAL_USE_VCLPLUGIN"] == "svp"
    assert env["DOCUMENT_UTILS_PROBE"] == "kept"
    assert "SAL_USE_VCLPLUGIN" not in os.environ


def test_missing_libreoffice_is_reported(monkeypatch, soffice_module):
    monkeypatch.setattr(soffice_module.shutil, "which", lambda name: None)
    monkeypatch.setattr(soffice_module, "KNOWN_BINARIES", ())
    assert soffice_module.find_soffice() is None
    with pytest.raises(FileNotFoundError):
        soffice_module.run_soffice(["--headless"])


def test_run_soffice_isolates_the_user_profile(monkeypatch, soffice_module):
    recorded = {}

    def fake_run(command, **kwargs):
        recorded["command"] = command
        recorded["kwargs"] = kwargs
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(soffice_module, "find_soffice", lambda: "/fake/soffice")
    monkeypatch.setattr(soffice_module.subprocess, "run", fake_run)
    result = soffice_module.run_soffice(["--headless", "--convert-to", "pdf", "in.docx"])
    assert result.returncode == 0
    command = recorded["command"]
    assert command[0] == "/fake/soffice"
    assert any(arg.startswith("-env:UserInstallation=file://") for arg in command)
    assert command[-3:] == ["--convert-to", "pdf", "in.docx"]
    assert recorded["kwargs"]["env"]["SAL_USE_VCLPLUGIN"] == "svp"


def test_run_soffice_keeps_a_caller_supplied_profile(monkeypatch, soffice_module):
    recorded = {}

    def fake_run(command, **kwargs):
        recorded["command"] = command
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(soffice_module, "find_soffice", lambda: "/fake/soffice")
    monkeypatch.setattr(soffice_module.subprocess, "run", fake_run)
    soffice_module.run_soffice(["-env:UserInstallation=file:///tmp/mine", "--headless"])
    profiles = [arg for arg in recorded["command"] if arg.startswith("-env:UserInstallation")]
    assert profiles == ["-env:UserInstallation=file:///tmp/mine"]


def test_conversion_entries_build_the_expected_command(monkeypatch, soffice_module, tmp_path):
    seen = []

    def fake_run(args, **kwargs):
        seen.append((list(args), kwargs))
        return subprocess.CompletedProcess(["soffice", *args], 0, "", "")

    monkeypatch.setattr(soffice_module, "run_soffice", fake_run)
    source = tmp_path / "in.docx"
    source.write_text("placeholder", encoding="utf-8")
    outdir = tmp_path / "out"

    soffice_module.convert(source, "pdf", outdir=outdir)
    soffice_module.thumbnail(source, outdir=outdir)
    soffice_module.recalc(source, outdir=outdir)

    formats = [args[args.index("--convert-to") + 1] for args, _ in seen]
    assert formats == ["pdf", "png", 'xlsx:"Calc MS Excel 2007 XML"']
    for args, kwargs in seen:
        assert "--headless" in args and "--norestore" in args
        assert args[args.index("--outdir") + 1] == str(outdir)
        assert args[-1] == str(source)
        assert kwargs["capture_output"] is True
    assert outdir.is_dir()


def test_af_unix_probe_answers_with_a_boolean(soffice_module):
    assert isinstance(soffice_module.af_unix_available(), bool)


def test_soffice_cli_answers_flags(tmp_path):
    helped = run_cli(OFFICE / "soffice.py", "--help", cwd=tmp_path)
    assert helped.returncode == 0
    version = run_cli(OFFICE / "soffice.py", "--version", cwd=tmp_path)
    assert version.returncode == 0 and version.stdout.startswith("soffice.py ")
    assert list(tmp_path.iterdir()) == []