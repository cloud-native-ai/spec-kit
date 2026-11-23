"""Reclaim the parts of an unpacked PPTX directory that nothing references.

Usage: python clean.py <unpacked_dir>

Editing an unpacked deck leaves debris: a slide dropped from ``<p:sldIdLst>``
still sits in ``ppt/slides``, the picture it used still sits in ``ppt/media``,
and the relationship files that named them still point at both.  Packing that
tree produces a package that carries every orphan.  This script removes them.

What goes:

* slide parts absent from ``<p:sldIdLst>``, their relationship files, and the
  presentation relationships that named them;
* the ``[trash]`` directory, which is where a manual edit parks a part it is no
  longer sure about;
* relationship files under ``charts``, ``diagrams`` and ``drawings`` whose own
  part is gone or is no longer named by a slide;
* files under ``media``, ``embeddings``, ``charts``, ``diagrams``, ``tags``,
  ``drawings`` and ``ink`` that no relationship names;
* ``theme/theme<n>.xml`` parts no relationship names, with their relationships;
* notes slides no relationship names, and notes relationships whose slide is
  gone;
* the ``[Content_Types].xml`` overrides of everything removed above.

Removal is a fixed point, not one pass: deleting a chart orphans the image the
chart embedded, so the reachability set is recomputed until a pass removes
nothing.  Reachability is the union of every internal relationship target in the
tree, which is what keeps a part alive while any surviving relationship still
names it.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pptx/clean.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: clean.py [options]\n'
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

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ooxml_parts as op  # noqa: E402 -- beside this file, after the path bootstrap

#: Directories whose parts are resources: a slide (or another resource) reaches
#: them through a relationship, never through the presentation's slide list.
RESOURCE_DIRS = ("media", "embeddings", "charts", "diagrams", "tags", "drawings", "ink")

#: Resources that own a relationship file of their own.
RESOURCE_RELS_DIRS = ("charts", "diagrams", "drawings")

TRASH_DIR = "[trash]"


def _rel(root: Path, path: Path) -> str:
    """A part name as the package spells it: relative, forward slashes."""
    return path.relative_to(root).as_posix()


def _rels_file(part: Path) -> Path:
    return part.parent / "_rels" / (part.name + ".rels")


def _delete(root: Path, path: Path, removed: list[str]) -> None:
    removed.append(_rel(root, path))
    path.unlink()


def shown_slides(root: Path) -> set[str]:
    """Slide file names the presentation still shows, in ``<p:sldIdLst>``."""
    pres = root / "ppt" / "presentation.xml"
    pres_rels = root / "ppt" / "_rels" / "presentation.xml.rels"
    if not pres.is_file() or not pres_rels.is_file():
        return set()
    return set(op.shown_slide_names(op.parse_file(pres), op.parse_file(pres_rels)))


def prune_slides(root: Path) -> list[str]:
    """Remove slides the presentation no longer shows, and their relationships."""
    slides = root / "ppt" / "slides"
    if not slides.is_dir():
        return []

    keep = shown_slides(root)
    removed: list[str] = []
    for part in sorted(slides.glob("slide*.xml")):
        if part.name in keep:
            continue
        _delete(root, part, removed)
        rels = _rels_file(part)
        if rels.is_file():
            _delete(root, rels, removed)

    pres_rels = root / "ppt" / "_rels" / "presentation.xml.rels"
    if removed and pres_rels.is_file():
        doc = op.parse_file(pres_rels)
        changed = False
        for rel in op.relationships(doc):
            target = op.attr(rel, "Target")
            if op.relationship_type(rel) != op.RT_SLIDE or not target.startswith("slides/"):
                continue
            if target[len("slides/"):] not in keep:
                op.remove_element(rel)
                changed = True
        if changed:
            op.write_part(pres_rels, doc)
    return removed


def prune_trash(root: Path) -> list[str]:
    """Remove the parked-parts directory, reporting every file it held."""
    trash = root / TRASH_DIR
    if not trash.is_dir():
        return []
    removed = [_rel(root, p) for p in sorted(trash.rglob("*")) if p.is_file()]
    shutil.rmtree(trash)
    return removed


def slide_referenced(root: Path) -> set[str]:
    """Part names the surviving slides reach through their own relationships."""
    rels_dir = root / "ppt" / "slides" / "_rels"
    if not rels_dir.is_dir():
        return set()
    reached: set[str] = set()
    for rels_file in sorted(rels_dir.glob("*.rels")):
        for rel in op.relationships(op.parse_file(rels_file)):
            if op.is_external(rel):
                continue
            target = op.resolve_target(rels_file, op.attr(rel, "Target"), root)
            if target is not None:
                reached.add(target.as_posix())
    return reached


def prune_resource_rels(root: Path) -> list[str]:
    """Remove relationship files whose resource is gone or unreferenced."""
    reached = slide_referenced(root)
    removed: list[str] = []
    for name in RESOURCE_RELS_DIRS:
        rels_dir = root / "ppt" / name / "_rels"
        if not rels_dir.is_dir():
            continue
        for rels_file in sorted(rels_dir.glob("*.rels")):
            owner = rels_dir.parent / rels_file.name[: -len(".rels")]
            if not owner.is_file() or _rel(root, owner) not in reached:
                _delete(root, rels_file, removed)
    return removed


def prune_resources(root: Path, referenced: set[str]) -> list[str]:
    """Remove resource, theme and notes parts that no relationship names."""
    removed: list[str] = []

    for name in RESOURCE_DIRS:
        directory = root / "ppt" / name
        if not directory.is_dir():
            continue
        for part in sorted(directory.iterdir()):
            if part.is_file() and _rel(root, part) not in referenced:
                _delete(root, part, removed)

    theme = root / "ppt" / "theme"
    if theme.is_dir():
        for part in sorted(theme.glob("theme*.xml")):
            if _rel(root, part) in referenced:
                continue
            _delete(root, part, removed)
            rels = _rels_file(part)
            if rels.is_file():
                _delete(root, rels, removed)

    notes = root / "ppt" / "notesSlides"
    if notes.is_dir():
        for part in sorted(notes.glob("*.xml")):
            if part.is_file() and _rel(root, part) not in referenced:
                _delete(root, part, removed)
        notes_rels = notes / "_rels"
        if notes_rels.is_dir():
            for rels_file in sorted(notes_rels.glob("*.rels")):
                owner = notes / rels_file.name[: -len(".rels")]
                if not owner.exists():
                    _delete(root, rels_file, removed)

    return removed


def prune_content_types(root: Path, removed: list[str]) -> None:
    """Drop the content-type overrides of the parts that were removed."""
    path = root / "[Content_Types].xml"
    if not removed or not path.is_file():
        return
    doc = op.parse_file(path)
    if op.remove_overrides(doc, removed):
        op.write_part(path, doc)


def clean(root: Path) -> list[str]:
    """Remove every unreferenced part; return the removed names, in order."""
    removed: list[str] = []
    removed.extend(prune_slides(root))
    removed.extend(prune_trash(root))

    while True:
        pass_removed = prune_resource_rels(root)
        referenced = {p.as_posix() for p in op.referenced_parts(root)}
        pass_removed.extend(prune_resources(root, referenced))
        if not pass_removed:
            break
        removed.extend(pass_removed)

    prune_content_types(root, removed)
    return removed


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        sys.stderr.write(
            "Usage: python clean.py <unpacked_dir>\n"
            "Example: python clean.py unpacked/\n"
        )
        return 1

    root = Path(argv[0])
    if not root.is_dir():
        sys.stderr.write(f"Error: {root} not found\n")
        return 1

    try:
        removed = clean(root)
    except (op.OoxmlError, OSError) as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1

    if removed:
        print(f"Removed {len(removed)} unreferenced files:")
        for name in removed:
            print(f"  {name}")
    else:
        print("No unreferenced files found")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))