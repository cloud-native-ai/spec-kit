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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/validators/pptx.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: pptx.py [options]\n'
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

"""PresentationML rules: slide identity, layout wiring, notes ownership.

Original implementation, MIT licensed. A presentation breaks in ways a Word
document does not: two slides can claim the same layout, a master can list a
layout it has no relationship for, and two slides can point at one notes part.
Each check below tests one of those wirings.
"""

import re
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from .. import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

from .base import BaseValidator

UUID_SHAPE = re.compile(
    r"^[{(]?[0-9A-Fa-f]{8}-?[0-9A-Fa-f]{4}-?[0-9A-Fa-f]{4}-?[0-9A-Fa-f]{4}-?[0-9A-Fa-f]{12}[})]?$"
)


class PPTXValidator(BaseValidator):
    """Structural and PresentationML checks for an unpacked .pptx."""

    LIBRARY_MODULE = "pptx"
    LIBRARY_LABEL = "python-pptx"
    PACKAGE_SUFFIX = ".pptx"

    RELATIONSHIP_HINTS = {
        "sldid": "slide",
        "sldmasterid": "slidemaster",
        "notesmasterid": "notesmaster",
        "sldlayoutid": "slidelayout",
        "themeid": "theme",
        "tablestyleid": "tablestyles",
    }

    def validate(self) -> bool:
        if not self.validate_xml():
            return False
        checks = (
            self.validate_namespaces,
            self.validate_unique_ids,
            self.validate_uuid_ids,
            self.validate_file_references,
            self.validate_slide_layout_ids,
            self.validate_content_types,
            self.validate_notes_slide_references,
            self.validate_relationship_ids,
            self.validate_no_duplicate_slide_layouts,
            self.validate_library_roundtrip,
        )
        return all([check() for check in checks])

    def open_package(self, package: Path):
        import pptx

        return pptx.Presentation(str(package))

    # --- identifiers ------------------------------------------------------- #
    @staticmethod
    def _uuid_shaped(value: str) -> bool:
        stripped = value.strip("{}()").replace("-", "")
        return len(stripped) == 32 and stripped.isalnum()

    def validate_uuid_ids(self) -> bool:
        """An id that looks like a GUID must actually be hexadecimal."""
        errors = []
        for path in self.xml_files:
            doc = self.part(path)
            if doc is None:
                continue
            for element in ox.iter_elements(doc.documentElement):
                for index in range(element.attributes.length):
                    attr = element.attributes.item(index)
                    local = ox.local_name(attr).lower()
                    if local != "id" and not local.endswith("id"):
                        continue
                    if self._uuid_shaped(attr.value) and not UUID_SHAPE.match(attr.value):
                        errors.append(
                            f"  {self.rel(path)}: {attr.name}='{attr.value}' looks like a GUID "
                            "but carries non-hexadecimal characters"
                        )
        return self.emit(
            errors,
            "Found {count} UUID ID validation errors:",
            "All GUID-shaped IDs are hexadecimal",
        )

    # --- layouts and notes ------------------------------------------------- #
    def _slide_relationships(self, folder: str):
        return sorted((self.unpacked_dir / folder).glob("*.xml.rels"))

    def validate_slide_layout_ids(self) -> bool:
        errors = []
        masters = sorted((self.unpacked_dir / "ppt" / "slideMasters").glob("*.xml"))
        if not masters:
            return self.emit([], "", "No slide masters to check")
        for master in masters:
            doc = self.part(master)
            if doc is None:
                continue
            rels_file = master.parent / "_rels" / f"{master.name}.rels"
            if not rels_file.is_file():
                errors.append(f"  {self.rel(master)}: missing relationship part {self.rel(rels_file)}")
                continue
            rels_doc = self.part(rels_file)
            if rels_doc is None:
                continue
            layout_rids = {
                ox.get_attr(relation, "Id")
                for relation in ox.iter_elements(rels_doc.documentElement, "Relationship")
                if "slideLayout" in (ox.get_attr(relation, "Type") or "")
            }
            prefixes = ox.ns_prefixes(doc.documentElement, ox.R_NS)
            for layout in ox.iter_elements(doc.documentElement, "sldLayoutId"):
                rid = ox.get_attr_ns(layout, prefixes, "id")
                if rid and rid not in layout_rids:
                    errors.append(
                        f"  {self.rel(master)}: sldLayoutId id='{ox.get_attr(layout, 'id')}' "
                        f"uses r:id='{rid}', which no slideLayout relationship declares"
                    )
        if errors:
            print("Add the missing layout relationships or drop the stale sldLayoutId entries.")
        return self.emit(
            errors,
            "Found {count} slide layout ID validation errors:",
            "All slide layout IDs resolve to a layout relationship",
        )

    def validate_no_duplicate_slide_layouts(self) -> bool:
        errors = []
        for rels_file in self._slide_relationships("ppt/slides/_rels"):
            doc = self.part(rels_file)
            if doc is None:
                continue
            layouts = [
                relation
                for relation in ox.iter_elements(doc.documentElement, "Relationship")
                if "slideLayout" in (ox.get_attr(relation, "Type") or "")
            ]
            if len(layouts) > 1:
                errors.append(
                    f"  {self.rel(rels_file)}: {len(layouts)} slideLayout relationships (one is allowed)"
                )
        return self.emit(
            errors,
            "Found slides with duplicate slideLayout references:",
            "Every slide references exactly one layout",
        )

    def validate_notes_slide_references(self) -> bool:
        errors = []
        owners = {}
        for rels_file in self._slide_relationships("ppt/slides/_rels"):
            doc = self.part(rels_file)
            if doc is None:
                continue
            slide = rels_file.name[: -len(".rels")]
            for relation in ox.iter_elements(doc.documentElement, "Relationship"):
                if "notesSlide" not in (ox.get_attr(relation, "Type") or ""):
                    continue
                target = ox.get_attr(relation, "Target") or ""
                if target:
                    owners.setdefault(target.replace("../", ""), []).append((slide, rels_file))
        for target, claimants in owners.items():
            if len(claimants) < 2:
                continue
            errors.append(
                f"  Notes part '{target}' is claimed by several slides: "
                + ", ".join(slide for slide, _ in claimants)
            )
            for _, rels_file in claimants:
                errors.append(f"    - {self.rel(rels_file)}")
        counted = len([line for line in errors if not line.startswith("    ")])
        if errors:
            print("FAILED - Found {count} notes slide reference validation errors:".format(count=counted))
            for line in errors:
                print(line)
            print("Each slide owns its own notes part; give every slide a separate one.")
            return False
        if self.verbose:
            print("PASSED - All notes slide references are unique")
        return True


if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/validate.py instead.")