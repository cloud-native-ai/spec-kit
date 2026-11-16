"""Integration test: the live-repository scanner reading (102, US2).

Pins ``contracts/line-registration-scan.contract.md`` **C-04, C-05, C-06, C-12, C-13, C-15**
against the declared live roots (FR-013 / FR-016). The scanner is read-only, so the reading is
persisted by this test — never by the scanner itself — into pytest's ``tmp_path``: writing under
``.specify/specs/**`` at suite time would race the accountant's corpus-stability clause (c20).
The committed ``test-evidence/line-registration-scan-live.txt`` is produced by the implementation
stage, not by this test run.

The test must collect before the scanner exists and fail with a named message; it never turns
a missing scanner into a clean reading, because ``--root`` on an absent directory is an input
error, not an empty set (C-05).
"""
from __future__ import annotations

import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "python" / "line-registration-scan.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCANNER), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=180,
    )


def _expected_root(root: str) -> str:
    return f"root: {root}"


def _require_scanner() -> None:
    # A body-level assertion, not a fixture: pytest reports FAILED (visible to --names-out),
    # not a setup ERROR that name-level baseline comparison cannot see.
    assert SCANNER.is_file(), (
        f"scanner not implemented yet: {SCANNER} "
        "(T022 authors it; this test stays red until then)"
    )


def test_the_declared_live_roots_read_clean_and_the_reading_is_recorded(tmp_path):
    _require_scanner()
    proc = _run()
    combined = (proc.stdout or "") + (proc.stderr or "")

    assert proc.returncode == 0, combined
    assert re.search(r"^violations:\s*0$", proc.stdout, re.MULTILINE), proc.stdout
    assert re.search(r"^owner-skipped:\s*1$", proc.stdout, re.MULTILINE), proc.stdout
    scanned = re.search(r"^scanned:\s*(\d+)\s+files$", proc.stdout, re.MULTILINE)
    assert scanned is not None and int(scanned.group(1)) > 0, proc.stdout

    for root in ("scripts/bash", "scripts/python", "skills"):
        assert _expected_root(root) in proc.stdout, (
            f"the reading must name the declared root {root}:\n{proc.stdout}"
        )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Never write under .specify/specs/** during the suite: the accountant's corpus-stability
    # clause (c20) reads that tree concurrently. The committed evidence file is produced by the
    # implementation stage, not by this test run.
    reading_path = tmp_path / "line-registration-scan-live.txt"
    reading_path.parent.mkdir(parents=True, exist_ok=True)
    reading_path.write_text(
        "\n".join(
            [
                "# Live long-task scan reading (102, T020)",
                "",
                f"Recorded by `tests/integration/test_line_registration_scan_live.py` at {stamp}.",
                "The scanner is read-only; this file is written by the test (FR-016).",
                "",
                "```text",
                "$ python3 scripts/python/line-registration-scan.py",
                proc.stdout.rstrip("\n"),
                "```",
                "",
                f"exit code: {proc.returncode}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_an_absent_root_is_an_input_error_not_a_clean_reading():
    _require_scanner()
    absent = f".specify/.tmp/line-registry-registration/absent-{uuid.uuid4().hex[:12]}"

    proc = _run("--root", absent)
    combined = (proc.stdout or "") + (proc.stderr or "")

    assert proc.returncode == 2, combined
    assert absent in combined, combined
    assert "violations: 0" not in combined, (
        "a missing root must never be rendered as a clean reading (C-05)"
    )
