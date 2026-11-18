"""Synthetic OPC packages for the document-utils Office regression tests.

The builders here produce the smallest package that satisfies the structural
rules the skill checks: a content-type inventory, a relationship inventory, and
the parts they name. Nothing is copied from a real document, so a case can state
exactly which defect it plants and assert that the checker finds that one.

Three shapes are offered (DOCX, PPTX, XLSX) plus helpers to write them either as
a packed file or as an unpacked tree, which is the pair of forms the Office
scripts move between.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W16CID = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'


def content_types(overrides: dict, defaults=None) -> str:
    defaults = {"rels": f"{PR}", "xml": "application/xml"} if defaults is None else defaults
    lines = [XML_HEAD + f'<Types xmlns="{CT}">']
    for extension, kind in defaults.items():
        lines.append(f'  <Default Extension="{extension}" ContentType="{kind}"/>')
    for part, kind in overrides.items():
        lines.append(f'  <Override PartName="{part}" ContentType="{kind}"/>')
    lines.append("</Types>")
    return "\n".join(lines)


def relationships(entries) -> str:
    lines = [XML_HEAD + f'<Relationships xmlns="{PR}">']
    for rid, kind, target in entries:
        lines.append(f'  <Relationship Id="{rid}" Type="{RT}/{kind}" Target="{target}"/>')
    lines.append("</Relationships>")
    return "\n".join(lines)


def paragraph(text: str, preserve: bool = False) -> str:
    space = ' xml:space="preserve"' if preserve else ""
    return f"<w:p><w:r><w:t{space}>{text}</w:t></w:r></w:p>"


def document(body: str) -> str:
    return (
        XML_HEAD + f'<w:document xmlns:w="{W}" xmlns:w14="{W14}" '
        f'xmlns:w16cid="{W16CID}" xmlns:r="{R}"><w:body>{body}</w:body></w:document>'
    )


def docx_parts(body: str | None = None) -> dict:
    """A one-paragraph DOCX, or the caller's body markup inside the same package."""
    body = paragraph("Hello document") if body is None else body
    return {
        "[Content_Types].xml": content_types(
            {
                "/word/document.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml",
                "/word/styles.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml",
            }
        ),
        "_rels/.rels": relationships([("rId1", "officeDocument", "word/document.xml")]),
        "word/document.xml": document(body),
        "word/_rels/document.xml.rels": relationships([("rId1", "styles", "styles.xml")]),
        "word/styles.xml": XML_HEAD + f'<w:styles xmlns:w="{W}"/>',
    }


def pptx_parts() -> dict:
    """A one-slide presentation with a master, a layout and a theme."""
    presentation = (
        XML_HEAD + f'<p:presentation xmlns:p="{P}" xmlns:r="{R}">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        '<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>'
        "</p:presentation>"
    )
    master = (
        XML_HEAD + f'<p:sldMaster xmlns:p="{P}" xmlns:r="{R}"><p:cSld><p:spTree/></p:cSld>'
        '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
        "</p:sldMaster>"
    )
    return {
        "[Content_Types].xml": content_types(
            {
                "/ppt/presentation.xml": "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
                "/ppt/slides/slide1.xml": "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
                "/ppt/slideLayouts/slideLayout1.xml": "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml",
                "/ppt/slideMasters/slideMaster1.xml": "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml",
                "/ppt/theme/theme1.xml": "application/vnd.openxmlformats-officedocument.theme+xml",
            }
        ),
        "_rels/.rels": relationships([("rId1", "officeDocument", "ppt/presentation.xml")]),
        "ppt/presentation.xml": presentation,
        "ppt/_rels/presentation.xml.rels": relationships(
            [
                ("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
                ("rId2", "slide", "slides/slide1.xml"),
            ]
        ),
        "ppt/slides/slide1.xml": XML_HEAD + f'<p:sld xmlns:p="{P}"><p:cSld><p:spTree/></p:cSld></p:sld>',
        "ppt/slides/_rels/slide1.xml.rels": relationships(
            [("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml")]
        ),
        "ppt/slideLayouts/slideLayout1.xml": XML_HEAD + f'<p:sldLayout xmlns:p="{P}"><p:cSld><p:spTree/></p:cSld></p:sldLayout>',
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": relationships(
            [("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]
        ),
        "ppt/slideMasters/slideMaster1.xml": master,
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": relationships(
            [
                ("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
                ("rId2", "theme", "../theme/theme1.xml"),
            ]
        ),
        "ppt/theme/theme1.xml": XML_HEAD + f'<a:theme xmlns:a="{A}" name="Fixture"/>',
    }


def xlsx_parts() -> dict:
    """A one-sheet workbook, enough for type detection and pack/unpack cases."""
    return {
        "[Content_Types].xml": content_types(
            {
                "/xl/workbook.xml": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml",
                "/xl/worksheets/sheet1.xml": "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml",
            }
        ),
        "_rels/.rels": relationships([("rId1", "officeDocument", "xl/workbook.xml")]),
        "xl/workbook.xml": XML_HEAD + f'<workbook xmlns="{S}" xmlns:r="{R}">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": relationships([("rId1", "worksheet", "worksheets/sheet1.xml")]),
        "xl/worksheets/sheet1.xml": XML_HEAD + f'<worksheet xmlns="{S}"><sheetData/></worksheet>',
    }


def write_tree(root: Path, parts: dict) -> Path:
    """Write parts as an unpacked tree; returns the root."""
    for member, text in parts.items():
        target = root / member
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return root


def write_package(path: Path, parts: dict) -> Path:
    """Write parts as a packed Office file; returns the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for member, text in parts.items():
            archive.writestr(member, text)
    return path


def read_part(path: Path, member: str) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read(member).decode("utf-8")