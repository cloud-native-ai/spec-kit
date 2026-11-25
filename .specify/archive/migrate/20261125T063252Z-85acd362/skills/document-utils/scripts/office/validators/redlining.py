"""Tracked-change honesty check for a redlined Word document.

Original implementation, MIT licensed. The question this validator answers is
narrow: if the named author's revisions were undone, would the document read
exactly like the original? Anything else means text was changed outside a
tracked change, or another author's revision was edited in place.

The comparison is textual, per paragraph, and the reported difference is a
word-level diff computed with the standard library (no external diff tool).
"""

import difflib
import re
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from .. import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

TOKENS = re.compile(r"\S+|\s+")


class RedliningValidator:
    """Compare a redlined document against its original, one author at a time."""

    def __init__(self, unpacked_dir, original_docx, verbose=False, author="Claude"):
        self.unpacked_dir = Path(unpacked_dir)
        self.original_docx = Path(original_docx)
        self.verbose = verbose
        self.author = author

    def repair(self) -> int:
        """Nothing here is mechanically repairable: the edit itself is wrong."""
        return 0

    def validate(self) -> bool:
        modified_part = self.unpacked_dir / "word" / "document.xml"
        if not modified_part.is_file():
            print(f"FAILED - Modified document.xml not found at {modified_part}")
            return False
        try:
            modified = ox.parse_file(modified_part)
        except Exception as exc:
            print(f"FAILED - Error parsing XML files: {exc}")
            return False

        if not self._author_revisions(modified.documentElement):
            if self.verbose:
                print(f"PASSED - No tracked changes by {self.author} found.")
            return True

        try:
            payload = ox.read_part(self.original_docx, "word/document.xml")
        except Exception as exc:
            print(f"FAILED - Error unpacking original docx: {exc}")
            return False
        if payload is None:
            print(f"FAILED - Original document.xml not found in {self.original_docx}")
            return False
        try:
            original = ox.parse_string(payload)
        except Exception as exc:
            print(f"FAILED - Error parsing XML files: {exc}")
            return False

        self._undo_author_revisions(original.documentElement)
        self._undo_author_revisions(modified.documentElement)
        before = self._paragraph_text(original.documentElement)
        after = self._paragraph_text(modified.documentElement)
        if before == after:
            if self.verbose:
                print(f"PASSED - All changes by {self.author} are properly tracked")
            return True

        print(f"FAILED - Document text doesn't match after removing {self.author}'s tracked changes")
        print("")
        print("Usual causes:")
        print("  1. Text was edited inside another author's revision instead of outside it")
        print("  2. An edit was made without wrapping it in a tracked change")
        print("  3. Another author's insertion was removed instead of being deleted inside it")
        print("")
        print("Patterns that keep the comparison clean:")
        print("  - Rejecting someone else's insertion: nest <w:del> inside their <w:ins>")
        print("  - Restoring someone else's deletion: add a new <w:ins> after their <w:del>")
        print("")
        print("Differences:")
        print("============")
        print(self._word_diff(before, after))
        return False

    # --- revision handling ------------------------------------------------- #
    def _author_revisions(self, root) -> bool:
        for tag in ("ins", "del"):
            for element in ox.iter_elements(root, tag):
                if ox.get_attr(element, "author") == self.author:
                    return True
        return False

    def _undo_author_revisions(self, root) -> None:
        """Drop the author's insertions and restore the author's deletions."""
        for parent in list(ox.iter_elements(root)):
            for kid in list(parent.childNodes):
                if ox.is_element(kid, "ins") and ox.get_attr(kid, "author") == self.author:
                    parent.removeChild(kid)
        for parent in list(ox.iter_elements(root)):
            for kid in list(parent.childNodes):
                if not (ox.is_element(kid, "del") and ox.get_attr(kid, "author") == self.author):
                    continue
                for deleted in list(ox.iter_elements(kid)):
                    tag = ox.local_name(deleted)
                    if tag in ("delText", "delInstrText"):
                        prefix = deleted.tagName.rpartition(":")[0]
                        live = "t" if tag == "delText" else "instrText"
                        deleted.tagName = f"{prefix}:{live}" if prefix else live
                ox.unwrap_node(kid)

    @staticmethod
    def _paragraph_text(root) -> str:
        paragraphs = []
        for paragraph in ox.iter_elements(root, "p"):
            text = "".join(ox.text_of(node) for node in ox.iter_elements(paragraph, "t"))
            if text:
                paragraphs.append(text)
        return "\n".join(paragraphs)

    @staticmethod
    def _word_diff(before: str, after: str) -> str:
        """A word-level diff: [-removed-] and {+added+}, in reading order."""
        old = TOKENS.findall(before)
        new = TOKENS.findall(after)
        pieces = []
        matcher = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == "equal":
                pieces.append("".join(old[i1:i2]))
            else:
                if op in ("replace", "delete"):
                    pieces.append("[-" + "".join(old[i1:i2]) + "-]")
                if op in ("replace", "insert"):
                    pieces.append("{+" + "".join(new[j1:j2]) + "+}")
        return "".join(pieces).strip() or "(no textual difference isolated)"


#
# Emitted by `.specify/scripts/python/sync-mirrors.py`; the authority for this block is
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
# `.specify/shared/definitions/script-interface-definitions.md`, its executable form by
# `.specify/scripts/python/script_interface_cli.py`. This block owns no rule of its own.)
import sys as _sig_sys
import pathlib as _sig_pathlib

_SIG_OWNER = _sig_pathlib.Path(__file__).resolve().parent
while not ((_SIG_OWNER / 'pyproject.toml').is_file()
           and (_SIG_OWNER / '.git').exists()) and _SIG_OWNER.parent != _SIG_OWNER:
    _SIG_OWNER = _SIG_OWNER.parent
_SIG_OWNER = str(_SIG_OWNER / 'scripts' / 'python')
if _SIG_OWNER not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_OWNER)

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/office/validators/redlining.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: redlining.py [options]\n'
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

if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/validate.py instead.")