#
# Emitted by `scripts/python/sync-mirrors.py`; the authority for this block is
# `contracts/mirror-projection.contract.md` C-34 / C-36. It depends on nothing
# that exists only in the source tree: it re-derives its own version line (C-36).
_VERSION_SOURCE = "pyproject.toml"
_VERSION_QUOTES = chr(39) + chr(34)
_MAX_UPWARD_LEVELS = 12


def _bridge_version(start):
    _here = start.resolve()
    for _ in range(_MAX_UPWARD_LEVELS + 1):
        if (_here / _VERSION_SOURCE).is_file() and (_here / ".git").exists():
            try:
                _text = (_here / _VERSION_SOURCE).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return "unknown"
            _in_project = False
            for _raw in _text.splitlines():
                _line = _raw.strip()
                if not _line or _line.startswith("#"):
                    continue
                if _line.startswith("[") and _line.endswith("]"):
                    _in_project = _line == "[project]"
                    continue
                if not _in_project:
                    continue
                _key, _sep, _value = _line.partition("=")
                if _sep and _key.strip() == "version":
                    _value = _value.strip()
                    if len(_value) >= 2 and _value[0] == _value[-1] and _value[0] in _VERSION_QUOTES:
                        _value = _value[1:-1]
                    return _value or "unknown"
            return "unknown"
        if _here.parent == _here:
            return "unknown"
        _here = _here.parent
    return "unknown"

def _bridge_main():
    import sys as _bridge_sys
    from pathlib import Path as _bridge_path

    _argv = list(_bridge_sys.argv[1:])
    if "--version" not in _argv:
        return
    if "--" in _argv and _argv.index("--version") > _argv.index("--"):
        return
    _invoked = _bridge_sys.argv[0] if _bridge_sys.argv[0] else "."
    _name = _bridge_path(_invoked).name or "script"
    print("%s %s" % (_name, _bridge_version(_bridge_path(_invoked).resolve().parent)))
    raise SystemExit(0)


_bridge_main()
del _bridge_main
# script-interface:86:begin (feature 086 -- generated; the rule is owned by
# `shared/definitions/script-interface-definitions.md`, its executable form by
# `scripts/python/script_interface_cli.py`. This block owns no rule of its own.)
import sys as _sig_sys
import pathlib as _sig_pathlib

_SIG_OWNER = _sig_pathlib.Path(__file__).resolve().parent
while not ((_SIG_OWNER / 'pyproject.toml').is_file()
           and (_SIG_OWNER / '.git').exists()) and _SIG_OWNER.parent != _SIG_OWNER:
    _SIG_OWNER = _SIG_OWNER.parent
_SIG_OWNER = str(_SIG_OWNER / 'scripts' / 'python')
if _SIG_OWNER not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_OWNER)

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/validators/docx.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: docx.py [options]\n'
    'options:\n'
    '  (none of its own; the arguments it takes are operands)\n'
    '  -h, --help    print this help and exit\n'
    '  --version     print the script name and the framework version, then exit\n'
    +
    'side-effects:' + ' ' + 'writes only through the options it documents; a flag-only invocation writes nothing' + '\n'
    +
    'exit-codes:' + ' ' + '0 success; 1 a documented check failed; 2 argument or environment error' + '\n'
)


def _sig_guard(argv):
    # Answer the flags and reject an undeclared option before any parsing or write.
    # RULES are asked of the owner (script_interface_cli.guard_argv), never restated:
    # the declared vocabulary and the flag forms are its, and C-9 (a recognized option
    # never rescues an unrecognized one) is its judgement. What stays local is the help
    # BODY, because its operand sentence is this script's own.
    try:
        import script_interface_cli as _sig  # noqa: E402 -- deferred: a copied script may lack it
    except ImportError:  # skill-local or sandbox copy: the module's own parser still runs
        return list(argv)
    line = list(argv)
    try:
        _sig.guard_argv(line, declared=_SIG_DECLARED)
    except SystemExit as answered:  # what guard_argv raises; _sig_sys.exit IS SystemExit
        if answered.code == 0:
            raise
        # The owner prints the rejection line and this script's help body is appended after
        # it, so the reader sees the vocabulary and not only the refusal.
        _sig_sys.stderr.write(_SIG_HELP)
        raise _sig_sys.exit(answered.code)
    stop = line.index('--') if '--' in line else len(line)
    if '-h' in line[:stop] or '--help' in line[:stop]:
        _sig_sys.stdout.write(_SIG_HELP)
        raise _sig_sys.exit(0)
    return line

if __name__ == "__main__":
    _sig_sys.argv = [_sig_sys.argv[0]] + _sig_guard(_sig_sys.argv[1:])
# script-interface:86:end

"""WordprocessingML rules: text runs, tracked changes, identifiers, comments.

Original implementation, MIT licensed. These are the DOCX-specific agreements a
Word document relies on beyond the package structure its base class checks:
whitespace that must be marked preserve, deleted text that must live in
``w:delText``, identifiers that must fit the ranges Word reserves, and comment
markers that must pair up and point at a real comment.
"""

import random
import re
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from .. import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

from .base import BaseValidator

PARA_ID_LIMIT = 0x80000000
DURABLE_ID_LIMIT = 0x7FFFFFFF
EDGE_WHITESPACE = re.compile(r"^[ \t\n\r]|[ \t\n\r]$")


class DOCXValidator(BaseValidator):
    """Structural and WordprocessingML checks for an unpacked .docx."""

    LIBRARY_MODULE = "docx"
    LIBRARY_LABEL = "python-docx"
    PACKAGE_SUFFIX = ".docx"

    def validate(self) -> bool:
        if not self.validate_xml():
            return False
        checks = (
            self.validate_namespaces,
            self.validate_unique_ids,
            self.validate_file_references,
            self.validate_content_types,
            self.validate_relationship_ids,
            self.validate_whitespace_preservation,
            self.validate_deletions,
            self.validate_insertions,
            self.validate_id_constraints,
            self.validate_comment_markers,
            self.validate_library_roundtrip,
        )
        verdicts = [check() for check in checks]
        self.compare_paragraph_counts()
        return all(verdicts)

    def open_package(self, package: Path):
        import docx

        return docx.Document(str(package))

    # --- text runs --------------------------------------------------------- #
    def _document_parts(self):
        return [path for path in self.xml_files if path.name == "document.xml"]

    def validate_whitespace_preservation(self) -> bool:
        errors = []
        for path in self._document_parts():
            doc = self.part(path)
            if doc is None:
                continue
            for element in ox.iter_elements(doc.documentElement, "t"):
                text = ox.text_of(element)
                if not text or not EDGE_WHITESPACE.search(text):
                    continue
                if ox.get_attr(element, "space") == "preserve":
                    continue
                preview = repr(text)[:50] + ("..." if len(repr(text)) > 50 else "")
                errors.append(
                    f"  {self.rel(path)}: {element.tagName} with edge whitespace lacks "
                    f"xml:space='preserve': {preview}"
                )
        return self.emit(
            errors,
            "Found {count} whitespace preservation violations:",
            "All edge whitespace is marked preserve",
        )

    def validate_deletions(self) -> bool:
        """Deleted content belongs in w:delText / w:delInstrText, never w:t."""
        errors = []
        for path in self._document_parts():
            doc = self.part(path)
            if doc is None:
                continue
            for deletion in ox.iter_elements(doc.documentElement, "del"):
                for element in ox.iter_elements(deletion):
                    tag = ox.local_name(element)
                    if tag not in ("t", "instrText"):
                        continue
                    preview = repr(ox.text_of(element))[:50]
                    replacement = "w:delText" if tag == "t" else "w:delInstrText"
                    errors.append(
                        f"  {self.rel(path)}: <{element.tagName}> inside <w:del> "
                        f"(use {replacement}): {preview}"
                    )
        return self.emit(
            errors,
            "Found {count} deletion validation violations:",
            "No live text elements inside w:del",
        )

    def validate_insertions(self) -> bool:
        """w:delText inside w:ins is only legal when a w:del wraps it."""
        errors = []
        for path in self._document_parts():
            doc = self.part(path)
            if doc is None:
                continue
            for insertion in ox.iter_elements(doc.documentElement, "ins"):
                for element in ox.iter_elements(insertion, "delText"):
                    if any(ox.local_name(parent) == "del" for parent in self._ancestors(element)):
                        continue
                    errors.append(
                        f"  {self.rel(path)}: <w:delText> inside <w:ins> without <w:del>: "
                        f"{repr(ox.text_of(element))[:50]}"
                    )
        return self.emit(
            errors,
            "Found {count} insertion validation violations:",
            "No stray w:delText inside w:ins",
        )

    # --- identifiers ------------------------------------------------------- #
    @staticmethod
    def _id_attributes(element):
        """Yield (attribute name, value) for the two Word identifier attributes."""
        for index in range(element.attributes.length):
            attr = element.attributes.item(index)
            if ox.local_name(attr) in ("paraId", "durableId"):
                yield attr.name, attr.value

    @staticmethod
    def _id_violation(attr_name: str, value: str, part_name: str):
        local = attr_name.rsplit(":", 1)[-1]
        limit = PARA_ID_LIMIT if local == "paraId" else DURABLE_ID_LIMIT
        base = 10 if (local == "durableId" and part_name == "numbering.xml") else 16
        try:
            number = int(value, base)
        except ValueError:
            return f"{attr_name}={value} must be {'decimal' if base == 10 else 'hexadecimal'} in {part_name}"
        if number >= limit:
            return f"{attr_name}={value} >= {limit:#x}"
        return None

    def validate_id_constraints(self) -> bool:
        errors = []
        for path in self.xml_files:
            doc = self.part(path)
            if doc is None:
                continue
            for element in ox.iter_elements(doc.documentElement):
                for attr_name, value in self._id_attributes(element):
                    problem = self._id_violation(attr_name, value, path.name)
                    if problem:
                        errors.append(f"  {path.name}: {problem}")
        return self.emit(
            errors,
            "{count} ID constraint violations:",
            "All paraId/durableId values are within their limits",
        )

    # --- comments ---------------------------------------------------------- #
    def validate_comment_markers(self) -> bool:
        errors = []
        document = next((path for path in self._document_parts() if "word" in path.parts), None)
        if document is None:
            return self.emit([], "", "No document.xml to check for comment markers")
        doc = self.part(document)
        if doc is None:
            return self.emit([f"  {self.rel(document)}: unreadable"], "{count} comment marker violations:", "")

        def marker_ids(tag):
            return {
                ox.get_attr(node, "id")
                for node in ox.iter_elements(doc.documentElement, tag)
                if ox.get_attr(node, "id") is not None
            }

        starts = marker_ids("commentRangeStart")
        ends = marker_ids("commentRangeEnd")
        references = marker_ids("commentReference")

        def ordered(values):
            return sorted(values, key=lambda value: int(value) if value.isdigit() else 0)

        for value in ordered(ends - starts):
            errors.append(f'  document.xml: commentRangeEnd id="{value}" has no commentRangeStart')
        for value in ordered(starts - ends):
            errors.append(f'  document.xml: commentRangeStart id="{value}" has no commentRangeEnd')

        comments = next((path for path in self.xml_files if path.name == "comments.xml"), None)
        if comments is not None:
            comments_doc = self.part(comments)
            if comments_doc is not None:
                known = {
                    ox.get_attr(node, "id")
                    for node in ox.iter_elements(comments_doc.documentElement, "comment")
                }
                for value in ordered((starts | ends | references) - known):
                    errors.append(f'  document.xml: marker id="{value}" names no comment in comments.xml')
        return self.emit(
            errors,
            "{count} comment marker violations:",
            "All comment markers pair up and resolve",
        )

    # --- paragraph census -------------------------------------------------- #
    def count_paragraphs_in_unpacked(self) -> int:
        total = 0
        for path in self._document_parts():
            doc = self.part(path)
            if doc is not None:
                total += len(list(ox.iter_elements(doc.documentElement, "p")))
        return total

    def count_paragraphs_in_original(self) -> int:
        if self.original_file is None:
            return 0
        try:
            payload = ox.read_part(self.original_file, "word/document.xml")
            if payload is None:
                return 0
            doc = ox.parse_string(payload)
            return len(list(ox.iter_elements(doc.documentElement, "p")))
        except Exception as exc:
            print(f"Error counting paragraphs in original document: {exc}")
            return 0

    def compare_paragraph_counts(self) -> None:
        before = self.count_paragraphs_in_original()
        after = self.count_paragraphs_in_unpacked()
        delta = after - before
        signed = f"+{delta}" if delta > 0 else str(delta)
        print(f"\nParagraphs: {before} -> {after} ({signed})")

    # --- repairs ----------------------------------------------------------- #
    def repair(self) -> int:
        return self.repair_whitespace_preservation() + self.repair_id_limits()

    def repair_id_limits(self) -> int:
        """Rewrite out-of-range or malformed paraId/durableId values."""
        repairs = 0
        for path in self.xml_files:
            try:
                doc = ox.parse_file(path)
            except Exception:
                continue
            taken = set()
            for element in ox.iter_elements(doc.documentElement):
                for _, value in self._id_attributes(element):
                    for base in (10, 16):
                        try:
                            taken.add(int(value, base))
                        except ValueError:
                            pass
            changed = False
            for element in ox.iter_elements(doc.documentElement):
                for attr_name, value in list(self._id_attributes(element)):
                    if not self._id_violation(attr_name, value, path.name):
                        continue
                    local = attr_name.rsplit(":", 1)[-1]
                    limit = PARA_ID_LIMIT if local == "paraId" else DURABLE_ID_LIMIT
                    number = random.randint(1, limit - 2)
                    while number in taken:
                        number = random.randint(1, limit - 2)
                    taken.add(number)
                    replacement = (
                        str(number)
                        if local == "durableId" and path.name == "numbering.xml"
                        else f"{number:08X}"
                    )
                    element.setAttribute(attr_name, replacement)
                    print(f"  Repaired: {path.name}: {attr_name} {value} -> {replacement}")
                    repairs += 1
                    changed = True
            if changed:
                ox.write_document(path, doc)
                self._documents.pop(path, None)
        return repairs


if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/validate.py instead.")