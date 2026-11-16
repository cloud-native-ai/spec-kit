"""Contract test: the read-only long-task scanner (102, US2).

Pins ``.specify/specs/102-line-registry-registration/contracts/line-registration-scan.contract.md``
**C-01…C-17**. The criterion members are never typed here: every fixture is built from the
scanner's own module constants (A-15).

Each test starts with ``_require_scanner()`` rather than relying on a fixture-level assertion:
a missing scanner must report as a **FAILED** node (visible to ``--names-out``), not as a setup
error the name-level baseline comparison cannot see. The reason is the same as the red leg
itself — before T022 the scanner does not exist, and none of these tests may pass.

Fixture roots live under the sanctioned, git-ignored ``.specify/.tmp/line-registry-registration/``
(A-21) and are removed by the ``scan_root`` fixture. Each test gets its own subdirectory, so
the module stays parallel-safe under the runner's default ``-n`` mode.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "python" / "line-registration-scan.py"
FIXTURE_PARENT = REPO_ROOT / ".specify" / ".tmp" / "line-registry-registration"

CONSTANT_NAMES = (
    "LONG_TASK_MARKERS",
    "SELF_DECLARATION_MARKER",
    "COMPLIANT_INVOCATIONS",
    "DEFAULT_SCAN_ROOTS",
)


def _unique(label: str) -> str:
    return f"{label}-{uuid.uuid4().hex[:12]}"


def _require_scanner() -> None:
    assert SCANNER.is_file(), (
        f"scanner not implemented yet: {SCANNER} "
        "(T022 authors it; this test stays red until then)"
    )


def _load_scanner():
    """Import the scanner so criterion members come from its constants, never from literals."""
    _require_scanner()
    spec = importlib.util.spec_from_file_location("line_registration_scan_under_test", SCANNER)
    assert spec is not None and spec.loader is not None, f"cannot load {SCANNER}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def scan_root():
    FIXTURE_PARENT.mkdir(parents=True, exist_ok=True)
    root = FIXTURE_PARENT / _unique("root")
    root.mkdir()
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCANNER), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd or REPO_ROOT),
        timeout=120,
    )


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _combined(proc: subprocess.CompletedProcess) -> str:
    return (proc.stdout or "") + (proc.stderr or "")


def _render_member(member) -> str:
    """An invocation member may be a literal or a tuple of tokens; both read as one line."""
    if isinstance(member, (list, tuple)):
        return " ".join(str(part) for part in member)
    return str(member)


def _compliant_block(module) -> str:
    members = list(module.COMPLIANT_INVOCATIONS)
    assert members, "COMPLIANT_INVOCATIONS must name at least one invocation form"
    return "\n".join(_render_member(member) for member in members)


def _self_declaration_line(module) -> str:
    literal = str(module.SELF_DECLARATION_MARKER)
    return literal if literal.lstrip().startswith("#") else "# " + literal


def _summary_int(stdout: str, key: str) -> int:
    match = re.search(rf"^{re.escape(key)}:\s*(\d+)\b", stdout, re.MULTILINE)
    assert match is not None, f"missing '{key}:' summary line in:\n{stdout}"
    return int(match.group(1))


def _snapshot(root: Path):
    rows = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            rows.append((rel, "link", os.readlink(path)))
        elif path.is_file():
            rows.append((rel, "file", hashlib.sha256(path.read_bytes()).hexdigest()))
        elif path.is_dir():
            rows.append((rel, "dir", ""))
    return tuple(rows)


# --------------------------------------------------------------------------- C-08 constants
def test_c08_the_four_criterion_constants_exist_and_are_populated():
    module = _load_scanner()
    for name in CONSTANT_NAMES:
        assert hasattr(module, name), f"module-level constant {name} is missing (C-08)"
    markers = list(module.LONG_TASK_MARKERS)
    assert markers and all(isinstance(m, str) and m for m in markers), markers
    assert isinstance(module.SELF_DECLARATION_MARKER, str)
    assert module.SELF_DECLARATION_MARKER
    forms = list(module.COMPLIANT_INVOCATIONS)
    assert forms, "COMPLIANT_INVOCATIONS must not be empty"
    roots = list(module.DEFAULT_SCAN_ROOTS)
    assert roots and all(isinstance(r, str) and r for r in roots), roots


# ------------------------------------------------------------------------------ C-01 surface
def test_c01_help_answers_zero_and_names_the_root_option(scan_root):
    _require_scanner()
    proc = _run("-h", cwd=scan_root)
    assert proc.returncode == 0, _combined(proc)
    assert "--root" in proc.stdout, proc.stdout


def test_c02_undeclared_option_exits_two(scan_root):
    _require_scanner()
    proc = _run("--bogus", cwd=scan_root)
    assert proc.returncode == 2, _combined(proc)


def test_c02_missing_option_value_exits_two(scan_root):
    _require_scanner()
    proc = _run("--root", cwd=scan_root)
    assert proc.returncode == 2, _combined(proc)


# ---------------------------------------------------------------------- C-05 root predicate
def test_c05_missing_root_is_an_input_error_naming_the_root(scan_root):
    _require_scanner()
    absent = _rel(scan_root / "absent")
    proc = _run("--root", absent)
    assert proc.returncode == 2, _combined(proc)
    assert absent in _combined(proc), _combined(proc)


def test_c05_non_directory_root_is_an_input_error_naming_the_root(scan_root):
    _require_scanner()
    plain = scan_root / "plain.txt"
    plain.write_text("not a directory\n", encoding="utf-8")
    proc = _run("--root", _rel(plain))
    assert proc.returncode == 2, _combined(proc)
    assert _rel(plain) in _combined(proc), _combined(proc)


def test_c05_root_outside_the_repository_is_an_input_error(tmp_path):
    _require_scanner()
    outside = tmp_path / "outside"
    outside.mkdir()
    proc = _run("--root", str(outside))
    assert proc.returncode == 2, _combined(proc)
    assert str(outside) in _combined(proc), _combined(proc)
    assert "root-outside-repo" in _combined(proc), _combined(proc)


def test_c05_a_root_with_no_judged_file_is_an_input_error(scan_root):
    """Existing but empty: input error, never a clean reading (C-05 / A-21)."""
    _require_scanner()
    proc = _run("--root", _rel(scan_root))
    assert proc.returncode == 2, _combined(proc)
    assert _rel(scan_root) in _combined(proc), _combined(proc)
    assert "violations: 0" not in _combined(proc), (
        "an empty root must never be rendered as a clean reading"
    )


# ---------------------------------------------------------------- C-07 judged file surface
def test_c07_markdown_files_do_not_enter_judgement(scan_root):
    module = _load_scanner()
    marker = str(list(module.LONG_TASK_MARKERS)[0])
    (scan_root / "notes.md").write_text(f"prose mentions {marker}\n", encoding="utf-8")
    (scan_root / "clean.sh").write_text("#!/usr/bin/env bash\necho clean\n", encoding="utf-8")

    proc = _run("--root", _rel(scan_root))
    assert proc.returncode == 0, _combined(proc)
    assert _summary_int(proc.stdout, "scanned") == 1, proc.stdout
    assert _summary_int(proc.stdout, "violations") == 0, proc.stdout
    assert "notes.md" not in proc.stdout, proc.stdout


def test_c07_symlinks_are_skipped_and_never_followed(scan_root):
    module = _load_scanner()
    marker = str(list(module.LONG_TASK_MARKERS)[0])
    targets = scan_root.parent / _unique("targets")
    targets.mkdir()
    try:
        target = targets / "violating-target.sh"
        target.write_text(f"#!/usr/bin/env bash\n{marker}\n", encoding="utf-8")
        (scan_root / "clean.sh").write_text("#!/usr/bin/env bash\necho clean\n", encoding="utf-8")
        link = scan_root / "linked.sh"
        link.symlink_to(target)

        proc = _run("--root", _rel(scan_root))
        assert proc.returncode == 0, _combined(proc)
        assert _summary_int(proc.stdout, "scanned") == 1, proc.stdout
        assert _summary_int(proc.stdout, "violations") == 0, proc.stdout
        assert "linked.sh" not in proc.stdout, proc.stdout
    finally:
        shutil.rmtree(targets, ignore_errors=True)


# ------------------------------------------------------------------------ C-10 / C-14 verdict
def test_c10_marker_without_a_compliant_invocation_is_a_violation(scan_root):
    module = _load_scanner()
    marker = str(list(module.LONG_TASK_MARKERS)[0])
    fixture = scan_root / "fixture.sh"
    fixture.write_text(f"#!/usr/bin/env bash\n{marker}\n", encoding="utf-8")

    proc = _run("--root", _rel(scan_root))
    assert proc.returncode == 1, _combined(proc)
    assert f"{_rel(fixture)}:2: criterion=content-marker" in proc.stdout, proc.stdout
    assert _summary_int(proc.stdout, "violations") == 1, proc.stdout
    assert _summary_int(proc.stdout, "scanned") == 1, proc.stdout
    assert _summary_int(proc.stdout, "owner-skipped") == 0, proc.stdout
    assert f"root: {_rel(scan_root)}" in proc.stdout, proc.stdout


def test_c10_the_same_file_with_a_compliant_invocation_is_clean(scan_root):
    module = _load_scanner()
    marker = str(list(module.LONG_TASK_MARKERS)[0])
    fixture = scan_root / "fixture.sh"
    fixture.write_text(
        f"#!/usr/bin/env bash\n{marker}\n{_compliant_block(module)}\n",
        encoding="utf-8",
    )

    proc = _run("--root", _rel(scan_root))
    assert proc.returncode == 0, _combined(proc)
    assert _summary_int(proc.stdout, "violations") == 0, proc.stdout
    assert _summary_int(proc.stdout, "scanned") == 1, proc.stdout


def test_c10_self_declaration_is_a_hit_not_an_exemption(scan_root):
    module = _load_scanner()
    fixture = scan_root / "declared.sh"
    fixture.write_text(
        f"#!/usr/bin/env bash\n{_self_declaration_line(module)}\n",
        encoding="utf-8",
    )

    proc = _run("--root", _rel(scan_root))
    assert proc.returncode == 1, _combined(proc)
    assert f"{_rel(fixture)}:2: criterion=self-declaration" in proc.stdout, proc.stdout


# ---------------------------------------------------------------- C-12 / C-13 reading shape
def test_c12_owner_skip_is_named_on_the_declared_roots():
    _require_scanner()
    proc = _run()
    assert "owner-skipped: 1" in proc.stdout, proc.stdout
    assert _summary_int(proc.stdout, "scanned") > 0, proc.stdout


def test_c13_and_c14_the_reading_is_deterministic_and_read_only(scan_root):
    module = _load_scanner()
    marker = str(list(module.LONG_TASK_MARKERS)[0])
    (scan_root / "a.sh").write_text(f"#!/usr/bin/env bash\n{marker}\n", encoding="utf-8")
    (scan_root / "b.py").write_text(f"# {marker}\n", encoding="utf-8")
    before = _snapshot(scan_root)

    first = _run("--root", _rel(scan_root))
    second = _run("--root", _rel(scan_root))

    assert first.returncode == 1, _combined(first)
    assert second.returncode == 1, _combined(second)
    assert first.stdout == second.stdout, "one tree must render the same lines in the same order"
    assert first.stdout.index(_rel(scan_root / "a.sh")) < first.stdout.index(
        _rel(scan_root / "b.py")
    ), first.stdout
    assert _snapshot(scan_root) == before, "the scanner must write nothing (C-03)"
