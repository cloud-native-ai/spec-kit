#!/usr/bin/env python3
"""Read-only long-task registration scanner (feature 102, US2).

The machine-readable owner of the long-task criterion is the constant block below
(requirements A-15); every other surface reaches it by ``import`` or by path, never by
restating the members. The human criterion and its adjudication boundary are owned by
``.specify/shared/guidelines/reporting-obligations.md`` § 九.

Contract: ``.specify/specs/102-line-registry-registration/contracts/line-registration-scan.contract.md``

Read-only: writes no file, creates no directory, spawns no process, reaches no network.
"""

from __future__ import annotations

import os
import sys

LONG_TASK_MARKERS = (
    "terraform apply",
    "run-tests.sh --full",
)
SELF_DECLARATION_MARKER = "# line-run-required"
COMPLIANT_INVOCATIONS = (
    ".specify/scripts/bash/line-run.sh",
    ("line-registry.py", "register"),
    ("line-registry.py", "update"),
    ("line-registry.py", "deregister"),
)
DEFAULT_SCAN_ROOTS = (
    ".specify/scripts/bash",
    ".specify/scripts/python",
    "skills",
)

JUDGED_SUFFIXES = (".sh", ".bash", ".py")

EXIT_CLEAN = 0
EXIT_VIOLATION = 1
EXIT_INPUT_ERROR = 2

USAGE = """usage: line-registration-scan.py [--root <path>]...

Read-only long-task registration scan.

options:
  --root <path>  scan this root instead of the declared default set (repeatable;
                 relative paths resolve against the repository root, not the cwd)
  -h, --help     print this usage and exit 0

A judged file that hits LONG_TASK_MARKERS or SELF_DECLARATION_MARKER and contains no
COMPLIANT_INVOCATIONS member is a violation (exit 1). The criterion constants live in this
module and are read by tests via import; no other surface restates them.

exit codes: 0 clean, 1 at least one violation, 2 input error (2 takes precedence).
"""


def _display(path: str, repo_root: str) -> str:
    rel = os.path.relpath(path, repo_root)
    return rel.replace(os.sep, "/")


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root + os.sep)


def resolve_repo_root(scanner_path: str):
    """Derive the repository root from the scanner's own resolved path.

    The path's directory must be named ``python`` and its parent ``scripts``; when the
    parent of ``scripts`` is the literal ``.specify``, the root is one level higher.
    Any other shape is unresolvable.
    """
    resolved = os.path.realpath(scanner_path)
    python_dir = os.path.dirname(resolved)
    scripts_dir = os.path.dirname(python_dir)
    if os.path.basename(python_dir) != "python" or os.path.basename(scripts_dir) != "scripts":
        return None, resolved
    top = os.path.dirname(scripts_dir)
    if not top or not os.path.basename(top):
        return None, resolved
    if os.path.basename(top) == ".specify":
        top = os.path.dirname(top)
        if not top or not os.path.basename(top):
            return None, resolved
    return top, resolved


def resolve_root(raw: str, repo_root: str) -> str:
    candidate = raw if os.path.isabs(raw) else os.path.join(repo_root, raw)
    return os.path.realpath(candidate)


def _judged_surface(path: str) -> bool:
    if os.path.splitext(path)[1] in JUDGED_SUFFIXES:
        return True
    try:
        with open(path, "rb") as handle:
            return handle.readline(256).startswith(b"#!")
    except OSError:
        return False


def _collect(root: str, repo_root: str, scanner_real: str, owner_state: list):
    found = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(
            name for name in dirnames if not os.path.islink(os.path.join(dirpath, name))
        )
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path) or not os.path.isfile(path):
                continue
            real = os.path.realpath(path)
            if not _within(real, repo_root):
                continue
            if real == scanner_real:
                owner_state[0] = 1
                continue
            if not _judged_surface(real):
                continue
            found.append(real)
    return found


def _read_text(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def _member_present(lines, member) -> bool:
    if isinstance(member, (list, tuple)):
        tokens = [str(token) for token in member]
        return any(all(token in line for token in tokens) for line in lines)
    literal = str(member)
    return any(literal in line for line in lines)


def _first_hit(lines):
    content = None
    for index, line in enumerate(lines, 1):
        for marker in LONG_TASK_MARKERS:
            if marker in line:
                content = (index, "content-marker", marker)
                break
        if content is not None:
            break
    declared = None
    for index, line in enumerate(lines, 1):
        if line.lstrip().startswith("#") and SELF_DECLARATION_MARKER in line:
            declared = (index, "self-declaration", SELF_DECLARATION_MARKER)
            break
    hits = [hit for hit in (content, declared) if hit is not None]
    if not hits:
        return None
    return min(hits, key=lambda hit: (hit[0], 0 if hit[1] == "content-marker" else 1))


def analyse(path: str):
    text = _read_text(path)
    if text is None:
        return None
    lines = text.splitlines()
    if any(_member_present(lines, member) for member in COMPLIANT_INVOCATIONS):
        return None
    return _first_hit(lines)


def _parse(argv):
    roots = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("-h", "--help"):
            return "help", roots, None
        if arg == "--root":
            if index + 1 >= len(argv):
                return "error", roots, "option --root requires a value"
            roots.append(argv[index + 1])
            index += 2
            continue
        return "error", roots, f"undeclared option or argument: {arg}"
    return "run", roots, None


def _input_error(message: str) -> int:
    sys.stderr.write(f"line-registration-scan.py: input error: {message}\n")
    return EXIT_INPUT_ERROR


def main(argv, scanner_path: str) -> int:
    mode, explicit_roots, error = _parse(argv)
    if mode == "help":
        sys.stdout.write(USAGE)
        return EXIT_CLEAN
    if mode == "error":
        return _input_error(error)

    repo_root, scanner_real = resolve_repo_root(scanner_path)
    if repo_root is None:
        return _input_error(f"repo-root-unresolved: {scanner_real}")

    raw_roots = explicit_roots if explicit_roots else list(DEFAULT_SCAN_ROOTS)
    effective = []
    for raw in raw_roots:
        resolved = resolve_root(raw, repo_root)
        if not _within(resolved, repo_root):
            return _input_error(f"root-outside-repo: {raw} (resolved: {resolved})")
        if not os.path.isdir(resolved):
            return _input_error(f"scan root is not a directory: {raw} (resolved: {resolved})")
        effective.append((raw, resolved))

    scanned = {}
    per_root = []
    violations = []
    owner_state = [0]
    for raw, resolved in effective:
        files = _collect(resolved, repo_root, scanner_real, owner_state)
        if not files:
            return _input_error(f"scan root has no judged file: {raw} (resolved: {resolved})")
        per_root.append((resolved, len(files)))
        for path in files:
            if path in scanned:
                continue
            hit = analyse(path)
            scanned[path] = hit
            if hit is not None:
                violations.append((path, hit))

    violations.sort(key=lambda row: _display(row[0], repo_root))
    out = []
    for path, (line_no, criterion, matched) in violations:
        out.append(f"{_display(path, repo_root)}:{line_no}: criterion={criterion} {matched}")
    for resolved, count in per_root:
        out.append(f"root: {_display(resolved, repo_root)} (files: {count})")
    out.append(f"scanned: {len(scanned)} files")
    out.append(f"violations: {len(violations)}")
    out.append(f"owner-skipped: {owner_state[0]}")
    sys.stdout.write("\n".join(out) + "\n")
    return EXIT_VIOLATION if violations else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], __file__))
