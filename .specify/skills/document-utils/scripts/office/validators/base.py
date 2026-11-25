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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/validators/base.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: base.py [options]\n'
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

"""Package-level checks every Office format shares.

Original implementation, MIT licensed. The checks are structural, not schema
based: an OPC package is a ZIP of XML parts plus two inventories (relationships
and content types), and a document opens only when those inventories agree with
the parts on disk. Each check below tests one such agreement and prints what it
found, so a failure names the part and the value that broke it.

The vendored XSD tree this skill used to carry is gone. What replaces it is a
library round trip (``validate_library_roundtrip``): the parts are re-packed and
opened with the format's own Python library, which is the same judgement a
consumer application makes. The round trip is skipped, not failed, when that
optional library is absent.
"""

import importlib
import tempfile
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from .. import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox


class BaseValidator:
    """Structural checks over an unpacked OPC package.

    Subclasses add the format-specific rules and name the library used for the
    round trip. ``repair()`` returns the number of edits it made.
    """

    #: element local name -> (id attribute, uniqueness scope)
    ID_RULES = {
        "comment": ("id", "file"),
        "commentrangestart": ("id", "file"),
        "commentrangeend": ("id", "file"),
        "bookmarkstart": ("id", "file"),
        "bookmarkend": ("id", "file"),
        "sldid": ("id", "file"),
        "sldmasterid": ("id", "global"),
        "sldlayoutid": ("id", "global"),
        "cm": ("authorid", "file"),
        "sheet": ("sheetid", "file"),
        "definedname": ("id", "file"),
        "sp": ("id", "file"),
        "pic": ("id", "file"),
        "cxnsp": ("id", "file"),
        "grpsp": ("id", "file"),
    }

    #: containers whose ids are allowed to repeat (legacy section list)
    ID_EXEMPT_CONTAINERS = {"sectionlst"}

    #: element local name -> relationship type fragment its r:id must point at
    RELATIONSHIP_HINTS = {}

    #: roots that must carry an Override in [Content_Types].xml
    DECLARABLE_ROOTS = {
        "document",
        "workbook",
        "worksheet",
        "presentation",
        "sld",
        "sldlayout",
        "sldmaster",
        "theme",
    }

    MEDIA_TYPES = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "tif": "image/tiff",
        "tiff": "image/tiff",
        "wmf": "image/x-wmf",
        "emf": "image/x-emf",
    }

    #: optional library used for the round trip; None disables it
    LIBRARY_MODULE = None
    LIBRARY_LABEL = "package"
    PACKAGE_SUFFIX = ".docx"

    def __init__(self, unpacked_dir, original_file=None, verbose=False):
        self.unpacked_dir = Path(unpacked_dir).resolve()
        self.original_file = Path(original_file) if original_file else None
        self.verbose = verbose
        self.xml_files = ox.xml_parts(self.unpacked_dir)
        self._documents = {}
        if not self.xml_files:
            print(f"Warning: No XML files found in {self.unpacked_dir}")

    # --- plumbing ---------------------------------------------------------- #
    def part(self, path):
        """Parse a part once; return None when it is unreadable or malformed."""
        path = Path(path)
        if path not in self._documents:
            try:
                self._documents[path] = ox.parse_file(path)
            except Exception:
                self._documents[path] = None
        return self._documents[path]

    def rel(self, path) -> str:
        return str(Path(path).relative_to(self.unpacked_dir))

    def emit(self, errors, headline: str, ok_line: str) -> bool:
        """Print one check's verdict: a counted failure list or a verbose pass."""
        if errors:
            print(f"FAILED - {headline.format(count=len(errors))}")
            for line in errors:
                print(line)
            return False
        if self.verbose:
            print(f"PASSED - {ok_line}")
        return True

    def validate(self):
        raise NotImplementedError("a format validator must implement validate()")

    def repair(self) -> int:
        return self.repair_whitespace_preservation()

    # --- checks ------------------------------------------------------------ #
    def validate_xml(self) -> bool:
        errors = []
        for path in self.xml_files:
            try:
                ox.parse_file(path)
            except Exception as exc:
                errors.append(f"  {self.rel(path)}: {exc}")
        return self.emit(errors, "Found {count} XML violations:", "All XML parts are well-formed")

    def validate_namespaces(self) -> bool:
        """Every prefix listed in an mc:Ignorable attribute must be declared."""
        errors = []
        for path in self.xml_files:
            doc = self.part(path)
            if doc is None:
                continue
            root = doc.documentElement
            declared = set()
            for index in range(root.attributes.length):
                attr = root.attributes.item(index)
                if attr.name.startswith("xmlns:"):
                    declared.add(attr.name.split(":", 1)[1])
            for index in range(root.attributes.length):
                attr = root.attributes.item(index)
                if ox.local_name(attr).endswith("Ignorable"):
                    for prefix in attr.value.split():
                        if prefix not in declared:
                            errors.append(
                                f"  {self.rel(path)}: prefix '{prefix}' is ignorable but not declared"
                            )
        return self.emit(errors, "{count} namespace issues:", "All ignorable prefixes are declared")

    def validate_unique_ids(self) -> bool:
        errors = []
        global_seen = {}
        for path in self.xml_files:
            try:
                doc = ox.parse_file(path)
            except Exception:
                continue
            root = doc.documentElement
            for fallback in list(ox.iter_elements(root, "AlternateContent")):
                ox.remove_node(fallback)
            file_seen = {}
            for element in ox.iter_elements(root):
                tag = ox.local_name(element).lower()
                rule = self.ID_RULES.get(tag)
                if rule is None:
                    continue
                if any(
                    ox.local_name(parent).lower() in self.ID_EXEMPT_CONTAINERS
                    for parent in self._ancestors(element)
                ):
                    continue
                attr_name, scope = rule
                value = ox.get_attr(element, attr_name)
                if value is None:
                    continue
                if scope == "global":
                    if value in global_seen:
                        errors.append(
                            f"  {self.rel(path)}: <{tag}> id '{value}' already used in {global_seen[value]}"
                        )
                    else:
                        global_seen[value] = f"{self.rel(path)} <{tag}>"
                else:
                    key = (tag, attr_name)
                    seen = file_seen.setdefault(key, {})
                    if value in seen:
                        errors.append(
                            f"  {self.rel(path)}: duplicate {attr_name}='{value}' in <{tag}> "
                            f"(first seen on element {seen[value]})"
                        )
                    else:
                        seen[value] = len(seen) + 1
        return self.emit(errors, "Found {count} ID uniqueness violations:", "All required IDs are unique")

    @staticmethod
    def _ancestors(element):
        node = element.parentNode
        while node is not None and node.nodeType == node.ELEMENT_NODE:
            yield node
            node = node.parentNode

    def validate_file_references(self) -> bool:
        """Relationship targets must exist, and every part must be reachable."""
        errors = []
        rels_files = ox.relationship_parts(self.unpacked_dir)
        if not rels_files:
            return self.emit([], "", "No relationship parts to check")

        inventories = {
            path
            for path in self.unpacked_dir.rglob("*")
            if path.is_file()
            and path.name != ox.CONTENT_TYPES_PART
            and not path.name.endswith(".rels")
        }
        reached = set()
        for rels_file in rels_files:
            doc = self.part(rels_file)
            if doc is None:
                errors.append(f"  {self.rel(rels_file)}: unreadable relationship part")
                continue
            for relation in ox.iter_elements(doc.documentElement, "Relationship"):
                target = ox.get_attr(relation, "Target")
                if not target or ox.is_external_target(target):
                    continue
                if ox.get_attr(relation, "TargetMode") == "External":
                    continue
                resolved = ox.resolve_target(self.unpacked_dir, rels_file, target)
                if resolved.is_file():
                    reached.add(resolved)
                else:
                    errors.append(f"  {self.rel(rels_file)}: broken reference to {target}")

        for orphan in sorted(inventories - reached):
            errors.append(f"  Unreferenced part: {self.rel(orphan)}")
        if errors:
            print(
                "These make the document look corrupt: repair broken references, "
                "and reference or remove unreferenced parts."
            )
        return self.emit(
            errors,
            "Found {count} relationship validation errors:",
            "All references resolve and all parts are referenced",
        )

    def validate_relationship_ids(self) -> bool:
        """r:id / r:embed / r:link must name a relationship of the right type."""
        errors = []
        for path in self.xml_files:
            if path.name.endswith(".rels"):
                continue
            rels_file = path.parent / "_rels" / f"{path.name}.rels"
            if not rels_file.is_file():
                continue
            rels_doc = self.part(rels_file)
            doc = self.part(path)
            if rels_doc is None or doc is None:
                continue
            types = {}
            for relation in ox.iter_elements(rels_doc.documentElement, "Relationship"):
                rid = ox.get_attr(relation, "Id")
                if not rid:
                    continue
                if rid in types:
                    errors.append(f"  {self.rel(rels_file)}: duplicate relationship Id '{rid}'")
                rel_type = ox.get_attr(relation, "Type") or ""
                types[rid] = rel_type.rsplit("/", 1)[-1]
            for element in ox.iter_elements(doc.documentElement):
                tag = ox.local_name(element)
                prefixes = ox.ns_prefixes(element, ox.R_NS)
                for attr in ("id", "embed", "link"):
                    rid = ox.get_attr_ns(element, prefixes, attr)
                    if not rid:
                        continue
                    if rid not in types:
                        known = ", ".join(sorted(types)[:5]) + ("..." if len(types) > 5 else "")
                        errors.append(
                            f"  {self.rel(path)}: <{tag}> r:{attr}='{rid}' names no relationship "
                            f"(declared: {known})"
                        )
                    elif attr == "id":
                        expected = self._expected_type(tag)
                        if expected and expected not in types[rid].lower():
                            errors.append(
                                f"  {self.rel(path)}: <{tag}> r:id='{rid}' points at "
                                f"'{types[rid]}' but a '{expected}' relationship is required"
                            )
        return self.emit(
            errors,
            "Found {count} relationship ID reference errors:",
            "All relationship ID references resolve",
        )

    def _expected_type(self, element_name: str):
        tag = element_name.lower()
        if tag in self.RELATIONSHIP_HINTS:
            return self.RELATIONSHIP_HINTS[tag]
        if tag.endswith("id") and len(tag) > 2:
            stem = tag[:-2]
            return "slide" if stem == "sld" else stem
        if tag.endswith("reference") and len(tag) > 9:
            return tag[:-9]
        return None

    def validate_content_types(self) -> bool:
        errors = []
        ct_file = self.unpacked_dir / ox.CONTENT_TYPES_PART
        if not ct_file.is_file():
            print(f"FAILED - {ox.CONTENT_TYPES_PART} is missing")
            return False
        doc = self.part(ct_file)
        if doc is None:
            print(f"FAILED - {ox.CONTENT_TYPES_PART} is not well-formed")
            return False
        root = doc.documentElement
        overrides = {
            (ox.get_attr(node, "PartName") or "").lstrip("/")
            for node in ox.iter_elements(root, "Override")
        }
        defaults = {
            (ox.get_attr(node, "Extension") or "").lower()
            for node in ox.iter_elements(root, "Default")
        }

        for path in self.xml_files:
            member = self.rel(path)
            if path.name.endswith(".rels") or "docProps/" in member or "_rels/" in member:
                continue
            if member == ox.CONTENT_TYPES_PART:
                continue
            part_doc = self.part(path)
            if part_doc is None:
                continue
            root_name = ox.local_name(part_doc.documentElement)
            if root_name.lower() in self.DECLARABLE_ROOTS and member not in overrides:
                errors.append(f"  {member}: <{root_name}> part has no Override in {ox.CONTENT_TYPES_PART}")

        for path in sorted(self.unpacked_dir.rglob("*")):
            if not path.is_file() or path.suffix in (".xml", ".rels"):
                continue
            member = self.rel(path)
            if member == ox.CONTENT_TYPES_PART or "_rels" in path.parts or "docProps" in path.parts:
                continue
            extension = path.suffix.lstrip(".").lower()
            if extension and extension not in defaults and extension in self.MEDIA_TYPES:
                errors.append(
                    f"  {member}: extension '{extension}' is undeclared; add "
                    f'<Default Extension="{extension}" ContentType="{self.MEDIA_TYPES[extension]}"/>'
                )
        return self.emit(
            errors,
            "Found {count} content type declaration errors:",
            "All parts are declared in [Content_Types].xml",
        )

    def validate_library_roundtrip(self) -> bool:
        """Re-pack the parts and open them with the format's own library."""
        if not self.LIBRARY_MODULE:
            return True
        try:
            importlib.import_module(self.LIBRARY_MODULE)
        except ImportError:
            if self.verbose:
                print(
                    f"SKIPPED - {self.LIBRARY_LABEL} round trip "
                    f"({self.LIBRARY_MODULE} is not installed)"
                )
            return True
        with tempfile.TemporaryDirectory() as scratch:
            package = Path(scratch) / f"roundtrip{self.PACKAGE_SUFFIX}"
            ox.write_package(package, ox.directory_parts(self.unpacked_dir))
            try:
                self.open_package(package)
            except Exception as exc:
                print(f"FAILED - {self.LIBRARY_LABEL} cannot open the re-packed document: {exc}")
                return False
        if self.verbose:
            print(f"PASSED - {self.LIBRARY_LABEL} opens the re-packed document")
        return True

    def open_package(self, package: Path):
        raise NotImplementedError

    # --- repairs ----------------------------------------------------------- #
    def repair_whitespace_preservation(self) -> int:
        """Mark text runs that begin or end with whitespace as preserve."""
        repairs = 0
        for path in self.xml_files:
            try:
                doc = ox.parse_file(path)
            except Exception:
                continue
            changed = False
            for element in ox.iter_elements(doc.documentElement):
                if ox.local_name(element) != "t":
                    continue
                text = ox.text_of(element)
                if not text or not (text[0] in " \t\n\r" or text[-1] in " \t\n\r"):
                    continue
                if ox.get_attr(element, "space") == "preserve":
                    continue
                element.setAttribute("xml:space", "preserve")
                preview = repr(text if len(text) <= 30 else text[:30] + "...")
                print(f"  Repaired: {path.name}: xml:space='preserve' added to {element.tagName}: {preview}")
                repairs += 1
                changed = True
            if changed:
                ox.write_document(path, doc)
                self._documents.pop(path, None)
        return repairs