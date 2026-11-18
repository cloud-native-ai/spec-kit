"""validate.py: flag entry layer, format detection, and the library-based checks.

The cases run the real script as a subprocess (the entry layer is what a probe
host exercises) against synthetic packages built by
``tests/fixtures/document_utils_office.py``. No optional third-party library is
required: the checks are structural, and the python-docx / python-pptx round
trip reports itself skipped when those libraries are absent.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import document_utils_office as fx

REPO_ROOT = Path(__file__).resolve().parents[2]
OFFICE = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts" / "office"
VALIDATE = OFFICE / "validate.py"

DECLARED = ("--author", "--auto-repair", "--original", "--verbose", "-v")


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, str(VALIDATE), *[str(arg) for arg in args]],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=120,
    )


@pytest.fixture
def docx_tree(tmp_path):
    return fx.write_tree(tmp_path / "unpacked", fx.docx_parts())


@pytest.fixture
def docx_file(tmp_path):
    return fx.write_package(tmp_path / "original.docx", fx.docx_parts())


# --------------------------------------------------------------------------- #
# Entry layer: flags answer before any work, and an undeclared option is refused
# --------------------------------------------------------------------------- #
def test_help_lists_the_declared_flags(tmp_path):
    result = run_cli("--help", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    for flag in DECLARED:
        assert flag in result.stdout
    assert list(tmp_path.iterdir()) == [], "a flag-only invocation must write nothing"


def test_version_names_the_script(tmp_path):
    result = run_cli("--version", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("validate.py ")
    assert list(tmp_path.iterdir()) == []


def test_undeclared_option_is_refused(tmp_path):
    result = run_cli("--bogus", cwd=tmp_path)
    assert result.returncode == 2
    assert "--bogus" in result.stderr


def test_help_flag_does_not_need_a_path(tmp_path):
    result = run_cli("-h", cwd=tmp_path)
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


# --------------------------------------------------------------------------- #
# Format detection
# --------------------------------------------------------------------------- #
def test_missing_path_is_an_argument_error(tmp_path):
    result = run_cli(tmp_path / "absent", cwd=tmp_path)
    assert result.returncode == 2
    assert "does not exist" in result.stderr


def test_directory_without_original_cannot_name_a_format(tmp_path, docx_tree):
    result = run_cli(docx_tree, cwd=tmp_path)
    assert result.returncode == 2
    assert "Cannot determine file type" in result.stderr


def test_original_names_the_format_for_a_directory(tmp_path, docx_tree, docx_file):
    result = run_cli(docx_tree, "--original", docx_file, cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All validations PASSED!" in result.stdout


def test_original_with_an_unsupported_suffix_is_refused(tmp_path, docx_tree):
    other = tmp_path / "original.txt"
    other.write_text("not a package", encoding="utf-8")
    result = run_cli(docx_tree, "--original", other, cwd=tmp_path)
    assert result.returncode == 2
    assert ".docx" in result.stderr


def test_xlsx_is_detected_but_not_validated(tmp_path):
    workbook = fx.write_package(tmp_path / "book.xlsx", fx.xlsx_parts())
    result = run_cli(workbook, cwd=tmp_path)
    assert result.returncode == 1
    assert "Validation not supported for file type .xlsx" in result.stdout


# --------------------------------------------------------------------------- #
# The checks themselves
# --------------------------------------------------------------------------- #
def test_packed_docx_passes(tmp_path, docx_file):
    result = run_cli(docx_file, cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All validations PASSED!" in result.stdout


def test_verbose_reports_each_passing_check(tmp_path, docx_file):
    result = run_cli(docx_file, "--verbose", cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASSED - All XML parts are well-formed" in result.stdout


def test_pptx_passes(tmp_path):
    presentation = fx.write_package(tmp_path / "deck.pptx", fx.pptx_parts())
    result = run_cli(presentation, cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_malformed_xml_fails(tmp_path, docx_tree):
    (docx_tree / "word" / "document.xml").write_text("<w:document>", encoding="utf-8")
    result = run_cli(docx_tree, "--original", fx.write_package(tmp_path / "o.docx", fx.docx_parts()), cwd=tmp_path)
    assert result.returncode == 1
    assert "XML violations" in result.stdout


def test_edge_whitespace_fails_then_auto_repair_fixes_it(tmp_path):
    parts = fx.docx_parts(body=fx.paragraph(" padded "))
    tree = fx.write_tree(tmp_path / "unpacked", parts)
    original = fx.write_package(tmp_path / "original.docx", parts)

    failing = run_cli(tree, "--original", original, cwd=tmp_path)
    assert failing.returncode == 1
    assert "whitespace preservation" in failing.stdout

    repaired = run_cli(tree, "--original", original, "--auto-repair", cwd=tmp_path)
    assert repaired.returncode == 0, repaired.stdout + repaired.stderr
    assert "Auto-repaired" in repaired.stdout
    assert 'xml:space="preserve"' in (tree / "word" / "document.xml").read_text(encoding="utf-8")


def test_out_of_range_durable_id_fails_then_auto_repair_fixes_it(tmp_path):
    body = (
        '<w:p w16cid:durableId="FFFFFFFF"><w:r><w:t>Hello document</w:t></w:r></w:p>'
    )
    parts = fx.docx_parts(body=body)
    tree = fx.write_tree(tmp_path / "unpacked", parts)
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())

    failing = run_cli(tree, "--original", original, cwd=tmp_path)
    assert failing.returncode == 1
    assert "ID constraint violations" in failing.stdout

    repaired = run_cli(tree, "--original", original, "--auto-repair", cwd=tmp_path)
    assert repaired.returncode == 0, repaired.stdout + repaired.stderr
    assert "durableId" in repaired.stdout


def test_broken_relationship_fails(tmp_path, docx_tree):
    rels = docx_tree / "word" / "_rels" / "document.xml.rels"
    rels.write_text(rels.read_text(encoding="utf-8").replace("styles.xml", "absent.xml"), encoding="utf-8")
    result = run_cli(docx_tree, "--original", fx.write_package(tmp_path / "o.docx", fx.docx_parts()), cwd=tmp_path)
    assert result.returncode == 1
    assert "broken reference" in result.stdout


def test_unreferenced_part_fails(tmp_path, docx_tree):
    (docx_tree / "word" / "orphan.xml").write_text(
        fx.XML_HEAD + f'<w:styles xmlns:w="{fx.W}"/>', encoding="utf-8"
    )
    result = run_cli(docx_tree, "--original", fx.write_package(tmp_path / "o.docx", fx.docx_parts()), cwd=tmp_path)
    assert result.returncode == 1
    assert "Unreferenced part" in result.stdout


def test_duplicate_slide_layout_fails(tmp_path):
    parts = fx.pptx_parts()
    rels = parts["ppt/slides/_rels/slide1.xml.rels"]
    parts["ppt/slides/_rels/slide1.xml.rels"] = rels.replace(
        "</Relationships>",
        f'  <Relationship Id="rId2" Type="{fx.RT}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>\n</Relationships>',
    )
    presentation = fx.write_package(tmp_path / "deck.pptx", parts)
    result = run_cli(presentation, cwd=tmp_path)
    assert result.returncode == 1
    assert "duplicate slideLayout" in result.stdout


# --------------------------------------------------------------------------- #
# Tracked-change comparison against the original
# --------------------------------------------------------------------------- #
def test_untracked_edit_fails_against_the_original(tmp_path):
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    body = (
        fx.paragraph("Hello changed document")
        + '<w:p><w:ins w:id="1" w:author="Claude" w:date="2026-01-01T00:00:00Z">'
        '<w:r><w:t>Added</w:t></w:r></w:ins></w:p>'
    )
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    result = run_cli(tree, "--original", original, cwd=tmp_path)
    assert result.returncode == 1
    assert "tracked changes" in result.stdout
    assert "Differences:" in result.stdout


def test_tracked_insertion_passes_against_the_original(tmp_path):
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    body = (
        '<w:p><w:r><w:t>Hello document</w:t></w:r>'
        '<w:ins w:id="1" w:author="Claude" w:date="2026-01-01T00:00:00Z">'
        '<w:r><w:t xml:space="preserve"> and more</w:t></w:r></w:ins></w:p>'
    )
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    result = run_cli(tree, "--original", original, cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Paragraphs: 1 -> 1 (0)" in result.stdout


def test_author_flag_selects_whose_revisions_are_compared(tmp_path):
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    body = (
        '<w:p><w:r><w:t>Hello document</w:t></w:r>'
        '<w:ins w:id="1" w:author="Reviewer" w:date="2026-01-01T00:00:00Z">'
        '<w:r><w:t xml:space="preserve"> reviewer text</w:t></w:r></w:ins></w:p>'
    )
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    # The default author has no revisions here, so the comparison is skipped ...
    assert run_cli(tree, "--original", original, cwd=tmp_path).returncode == 0
    # ... while naming the reviewer makes the insertion accountable.
    named = run_cli(tree, "--original", original, "--author", "Reviewer", cwd=tmp_path)
    assert named.returncode == 0, named.stdout + named.stderr


def test_deleted_text_must_use_deltext(tmp_path):
    body = (
        '<w:p><w:del w:id="1" w:author="Claude" w:date="2026-01-01T00:00:00Z">'
        '<w:r><w:t>gone</w:t></w:r></w:del></w:p>'
    )
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts(body=body))
    result = run_cli(tree, "--original", original, cwd=tmp_path)
    assert result.returncode == 1
    assert "deletion validation violations" in result.stdout


def test_comment_markers_must_pair(tmp_path):
    body = '<w:p><w:commentRangeEnd w:id="7"/><w:r><w:t>Hello document</w:t></w:r></w:p>'
    tree = fx.write_tree(tmp_path / "unpacked", fx.docx_parts(body=body))
    original = fx.write_package(tmp_path / "original.docx", fx.docx_parts())
    result = run_cli(tree, "--original", original, cwd=tmp_path)
    assert result.returncode == 1
    assert "comment marker violations" in result.stdout