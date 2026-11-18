"""pack.py / unpack.py: the round trip, the tidying helpers, and the error paths.

A package is unpacked into a tree, the tree is packed back, and the text a
reader would see is compared before and after — that is the property the whole
edit workflow rests on. The remaining cases pin the message shapes callers
parse, the inventories a written package must carry, and the refusals (bad
suffix, corrupt zip, a member name that would escape the destination).
"""

import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from fixtures import document_utils_office as fx

REPO_ROOT = Path(__file__).resolve().parents[2]
OFFICE = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts" / "office"


@pytest.fixture(scope="module", autouse=True)
def office_on_path():
    """The scripts import their siblings flat, exactly as a direct invocation does."""
    saved = list(sys.path)
    sys.path.insert(0, str(OFFICE))
    yield
    sys.path[:] = saved


def load(script: str, name: str):
    path = OFFICE / script
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def unpack_module():
    return load("unpack.py", "_du_office_unpack")


@pytest.fixture(scope="module")
def pack_module():
    return load("pack.py", "_du_office_pack")


def run_cli(script: Path, *args, cwd):
    return subprocess.run(
        [sys.executable, str(script), *[str(arg) for arg in args]],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=120,
    )


def texts(package_or_tree) -> list:
    """Every w:t string in document.xml, in order, from a package or a tree."""
    path = Path(package_or_tree)
    if path.is_dir():
        payload = (path / "word" / "document.xml").read_text(encoding="utf-8")
    else:
        payload = fx.read_part(path, "word/document.xml")
    import ooxml as ox

    doc = ox.parse_string(payload)
    return [ox.text_of(node) for node in ox.iter_elements(doc.documentElement, "t")]


def canonical(payload: bytes) -> bytes:
    """One part's markup with layout whitespace removed, for byte comparison."""
    import ooxml as ox

    doc = ox.parse_string(payload)
    ox.strip_layout_whitespace(doc)
    return ox.document_bytes(doc)


# --------------------------------------------------------------------------- #
# Entry layer
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("script", ["unpack.py", "pack.py"])
def test_flags_answer_without_operands(tmp_path, script):
    result = run_cli(OFFICE / script, "--help", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "--version" in result.stdout
    version = run_cli(OFFICE / script, "--version", cwd=tmp_path)
    assert version.returncode == 0
    assert version.stdout.startswith(f"{script} ")
    refused = run_cli(OFFICE / script, "--bogus", cwd=tmp_path)
    assert refused.returncode == 2
    assert list(tmp_path.iterdir()) == []


# --------------------------------------------------------------------------- #
# Round trip
# --------------------------------------------------------------------------- #
def test_round_trip_preserves_text(tmp_path, unpack_module, pack_module):
    body = (
        fx.paragraph("Hello document")
        + fx.paragraph(" padded ", preserve=True)
        + fx.paragraph("curly \u201cquotes\u201d and \u2018apostrophes\u2019")
    )
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=body))
    tree = tmp_path / "unpacked"

    _, unpacked = unpack_module.unpack(str(source), str(tree))
    assert unpacked.startswith("Unpacked"), unpacked
    rebuilt = tmp_path / "rebuilt.docx"
    _, packed = pack_module.pack(str(tree), str(rebuilt), validate=False)
    assert packed.startswith("Successfully packed"), packed

    assert texts(source) == texts(rebuilt)
    with zipfile.ZipFile(source) as before, zipfile.ZipFile(rebuilt) as after:
        assert sorted(before.namelist()) == sorted(after.namelist())


def test_round_trip_through_the_cli(tmp_path):
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts())
    tree = tmp_path / "unpacked"
    first = run_cli(OFFICE / "unpack.py", source, tree, cwd=tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    assert "(5 XML files)" in first.stdout
    assert "simplified 0 tracked changes" in first.stdout
    assert "merged 0 runs" in first.stdout

    rebuilt = tmp_path / "rebuilt.docx"
    second = run_cli(OFFICE / "pack.py", tree, rebuilt, cwd=tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    assert texts(source) == texts(rebuilt)


def test_tidying_can_be_switched_off(tmp_path):
    body = (
        '<w:p><w:r><w:t>Hello</w:t></w:r><w:r><w:t xml:space="preserve"> document</w:t></w:r></w:p>'
    )
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=body))
    tree = tmp_path / "plain"
    result = run_cli(
        OFFICE / "unpack.py", source, tree,
        "--merge-runs", "false", "--simplify-redlines", "false",
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert "merged" not in result.stdout
    assert "simplified" not in result.stdout
    assert len(texts(tree)) == 2, "runs must stay separate when merging is off"


def test_adjacent_same_format_runs_are_merged(tmp_path, unpack_module):
    body = (
        '<w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Hello</w:t></w:r>'
        '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve"> document</w:t></w:r>'
        '<w:r><w:rPr><w:i/></w:rPr><w:t>!</w:t></w:r></w:p>'
    )
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=body))
    tree = tmp_path / "unpacked"
    _, message = unpack_module.unpack(str(source), str(tree))
    assert "merged 1 runs" in message
    assert texts(tree) == ["Hello document", "!"]


def test_adjacent_same_author_revisions_are_simplified(tmp_path, unpack_module):
    stamp = 'w:date="2026-01-01T00:00:00Z"'
    body = (
        '<w:p>'
        f'<w:ins w:id="1" w:author="Claude" {stamp}><w:r><w:t>Hello</w:t></w:r></w:ins>'
        f'<w:ins w:id="2" w:author="Claude" {stamp}><w:r><w:t xml:space="preserve"> document</w:t></w:r></w:ins>'
        f'<w:ins w:id="3" w:author="Reviewer" {stamp}><w:r><w:t>!</w:t></w:r></w:ins>'
        "</w:p>"
    )
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=body))
    tree = tmp_path / "unpacked"
    _, message = unpack_module.unpack(str(source), str(tree))
    assert "simplified 1 tracked changes" in message

    import ooxml as ox

    doc = ox.parse_file(tree / "word" / "document.xml")
    authors = [ox.get_attr(node, "author") for node in ox.iter_elements(doc.documentElement, "ins")]
    assert authors == ["Claude", "Reviewer"]


def test_curly_quotes_become_character_references(tmp_path, unpack_module):
    body = fx.paragraph("a \u201cb\u201d c")
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=body))
    tree = tmp_path / "unpacked"
    unpack_module.unpack(str(source), str(tree))
    raw = (tree / "word" / "document.xml").read_text(encoding="utf-8")
    assert "&#x201C;" in raw and "&#x201D;" in raw
    assert "\u201c" not in raw
    assert texts(tree) == ["a \u201cb\u201d c"]


def test_packed_package_puts_content_types_first(tmp_path, pack_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    package = tmp_path / "out.docx"
    pack_module.pack(str(tree), str(package), validate=False)
    with zipfile.ZipFile(package) as archive:
        assert archive.namelist()[0] == "[Content_Types].xml"


def test_packing_removes_layout_whitespace_but_keeps_text(tmp_path, unpack_module, pack_module):
    source = fx.write_package(tmp_path / "source.docx", fx.docx_parts(body=fx.paragraph(" padded ", preserve=True)))
    tree = tmp_path / "unpacked"
    unpack_module.unpack(str(source), str(tree))
    assert "\n  " in (tree / "word" / "document.xml").read_text(encoding="utf-8")
    package = tmp_path / "out.docx"
    pack_module.pack(str(tree), str(package), validate=False)
    assert "\n  " not in fx.read_part(package, "word/document.xml")
    assert texts(package) == [" padded "]


# --------------------------------------------------------------------------- #
# Validation on the way back in
# --------------------------------------------------------------------------- #
def test_pack_validates_against_the_original(tmp_path, pack_module):
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    body = (
        fx.paragraph("Hello changed document")
        + '<w:p><w:ins w:id="1" w:author="Claude" w:date="2026-01-01T00:00:00Z">'
        '<w:r><w:t>Added</w:t></w:r></w:ins></w:p>'
    )
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    _, message = pack_module.pack(str(tree), str(tmp_path / "out.docx"), original_file=str(original))
    assert message.startswith("Error: Validation failed"), message
    assert not (tmp_path / "out.docx").exists()


def test_pack_can_skip_validation(tmp_path, pack_module):
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=fx.paragraph("Hello changed document")))
    _, message = pack_module.pack(
        str(tree), str(tmp_path / "out.docx"), original_file=str(original), validate=False
    )
    assert message.startswith("Successfully packed"), message


def test_pack_repairs_before_packing(tmp_path, pack_module):
    parts = fx.docx_parts(body=fx.paragraph(" padded "))
    original = fx.write_package(tmp_path / "original.docx", parts)
    tree = fx.write_tree(tmp_path / "unpacked", parts)
    _, message = pack_module.pack(str(tree), str(tmp_path / "out.docx"), original_file=str(original))
    assert message.startswith("Successfully packed"), message
    assert 'xml:space="preserve"' in fx.read_part(tmp_path / "out.docx", "word/document.xml")


# --------------------------------------------------------------------------- #
# Refusals
# --------------------------------------------------------------------------- #
def test_unpack_refuses_a_missing_file(tmp_path, unpack_module):
    _, message = unpack_module.unpack(str(tmp_path / "absent.docx"), str(tmp_path / "tree"))
    assert message == f"Error: {tmp_path / 'absent.docx'} does not exist"


def test_unpack_refuses_an_unsupported_suffix(tmp_path, unpack_module):
    document = tmp_path / "note.txt"
    document.write_text("text", encoding="utf-8")
    _, message = unpack_module.unpack(str(document), str(tmp_path / "tree"))
    assert "must be a .docx, .pptx, or .xlsx file" in message


def test_unpack_refuses_a_corrupt_package(tmp_path, unpack_module):
    broken = tmp_path / "broken.docx"
    broken.write_bytes(b"this is not a zip archive")
    _, message = unpack_module.unpack(str(broken), str(tmp_path / "tree"))
    assert "is not a valid Office file" in message


def test_unpack_refuses_a_traversing_member(tmp_path, unpack_module):
    evil = tmp_path / "evil.docx"
    with zipfile.ZipFile(evil, "w") as archive:
        archive.writestr("../escaped.xml", "<x/>")
    destination = tmp_path / "tree"
    _, message = unpack_module.unpack(str(evil), str(destination))
    assert message.startswith("Error unpacking:"), message
    assert not (tmp_path / "escaped.xml").exists()


def test_pack_refuses_a_missing_tree(tmp_path, pack_module):
    _, message = pack_module.pack(str(tmp_path / "absent"), str(tmp_path / "out.docx"))
    assert "is not a directory" in message


def test_pack_refuses_an_unsupported_suffix(tmp_path, pack_module):
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts())
    _, message = pack_module.pack(str(tree), str(tmp_path / "out.txt"))
    assert "must be a .docx, .pptx, or .xlsx file" in message


def test_pack_refuses_malformed_xml(tmp_path, pack_module):
    parts = fx.docx_parts()
    parts["word/document.xml"] = "<w:document>"
    tree = fx.write_tree(tmp_path / "unpacked", parts)
    _, message = pack_module.pack(str(tree), str(tmp_path / "out.docx"), validate=False)
    assert message.startswith("Error: word/document.xml is not well-formed"), message


def test_cli_exit_codes_follow_the_message(tmp_path):
    failing = run_cli(OFFICE / "pack.py", tmp_path / "absent", tmp_path / "out.docx", cwd=tmp_path)
    assert failing.returncode == 1
    assert "Error" in failing.stdout
    unpacking = run_cli(OFFICE / "unpack.py", tmp_path / "absent.docx", tmp_path / "tree", cwd=tmp_path)
    assert unpacking.returncode == 1


# --------------------------------------------------------------------------- #
# The other two formats travel the same road
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("builder,suffix", [(fx.pptx_parts, ".pptx"), (fx.xlsx_parts, ".xlsx")])
def test_round_trip_for_pptx_and_xlsx(tmp_path, unpack_module, pack_module, builder, suffix):
    source = fx.write_package(tmp_path / f"source{suffix}", builder())
    tree = tmp_path / "unpacked"
    _, message = unpack_module.unpack(str(source), str(tree))
    assert message.startswith("Unpacked"), message
    assert "merged" not in message, "run merging is DOCX only"
    rebuilt = tmp_path / f"rebuilt{suffix}"
    _, packed = pack_module.pack(str(tree), str(rebuilt), validate=False)
    assert packed.startswith("Successfully packed"), packed
    with zipfile.ZipFile(source) as before, zipfile.ZipFile(rebuilt) as after:
        assert sorted(before.namelist()) == sorted(after.namelist())
        for member in before.namelist():
            if member.endswith((".xml", ".rels")):
                assert canonical(before.read(member)) == canonical(after.read(member)), member