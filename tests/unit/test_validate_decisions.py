"""Unit tests for the decision-governance checker ``scripts/python/validate-decisions.py``.

Feature 107. This module owns the checker's own interface surface and, in later packages,
the record-judging unit tests (M-01 / M-03 / M-04 reverse samples, the C-107 replay test).
Landed by package P1: ``test_cli_surface`` only.

``test_cli_surface`` (T006, red-first; green at T007) pins ``contracts/enforcement-boundary``
C-404 together with ``shared/definitions/script-interface-definitions.md``:

* ``-h`` and ``--help`` answer the same body;
* ``--version`` prints one line ``<script-name> <framework-version>``;
* an undeclared option exits non-zero, and the declared action set is exactly
  ``records|payload|chain|inventory`` (a fifth value is an argument error);
* exit codes are 0 = pass / 1 = a documented check failed / 2 = input or argument error,
  as stated in the help body's ``exit-codes:`` label;
* a run creates no file inside the repository (before/after snapshot over the trees a
  checker could plausibly touch, with bytecode writing disabled for the subprocess).

The test drives the engine as a real process (``subprocess``) so the version line and the
undeclared-option refusal are observed exactly as a shell caller observes them.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "validate-decisions.py"

#: The closed declared action set (T007). Order is part of the help rendering.
ACTIONS = ("records", "payload", "chain", "inventory")

#: Trees a read-only run could plausibly touch (its own source, its mirror, the spec dir
#: passed as ``--spec``, the fixture dir passed as ``--fixture``).
SNAPSHOT_TREES = (
    "scripts/python",
    ".specify/scripts/python",
    ".specify/specs/107-decision-governance",
    "tests/fixtures/decision-governance",
)

VERSION_LINE_RE = re.compile(r"^validate-decisions\.py \S+$")


def run_engine(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def snapshot() -> list[tuple[str, int, int]]:
    """(path, size, mtime_ns) over the snapshot trees; interpreter caches excluded."""
    entries = []
    for rel in SNAPSHOT_TREES:
        base = ROOT / rel
        for path in sorted(base.rglob("*")):
            if "__pycache__" in path.parts:
                continue
            if path.is_file():
                stat = path.stat()
                entries.append((str(path.relative_to(ROOT)), stat.st_size, stat.st_mtime_ns))
    return entries


def test_cli_surface() -> None:
    assert ENGINE.is_file(), f"missing checker: {ENGINE}"

    # --help / -h: one body, exit 0.
    short = run_engine("-h")
    long = run_engine("--help")
    assert short.returncode == 0, f"-h exited {short.returncode}: {short.stderr}"
    assert long.returncode == 0, f"--help exited {long.returncode}: {long.stderr}"
    assert short.stdout == long.stdout, "-h and --help answer different bodies"
    help_text = short.stdout

    # The declared action set is exactly the four, rendered by argparse's choices.
    assert "{%s}" % ",".join(ACTIONS) in help_text, (
        "help does not render the closed action set {records,payload,chain,inventory}"
    )
    assert "--action" in help_text and "--carrier" in help_text and "--json" in help_text

    # The four mandatory help labels: usage/options come from argparse; the two labelled
    # lines are ours (owner: shared/definitions/script-interface-definitions.md § 2).
    assert "side-effects:" in help_text, "help body lacks the side-effects label"
    exit_lines = [ln for ln in help_text.splitlines() if ln.strip().startswith("exit-codes:")]
    assert exit_lines, "help body lacks the exit-codes label"
    exit_line = exit_lines[0]
    # C-404: 0 = pass / 1 = documented check failed / 2 = input or argument error.
    for code in ("0", "1", "2"):
        assert code in exit_line, f"exit-codes label does not state the {code} meaning: {exit_line!r}"

    # --version: one line, <script-name> <framework-version>, exit 0.
    version = run_engine("--version")
    assert version.returncode == 0, f"--version exited {version.returncode}: {version.stderr}"
    vlines = [ln for ln in version.stdout.splitlines() if ln.strip()]
    assert len(vlines) == 1, f"--version printed {len(vlines)} line(s): {vlines}"
    assert VERSION_LINE_RE.match(vlines[0]), f"malformed version line: {vlines[0]!r}"

    # An undeclared option is refused non-zero, with a diagnostic.
    bogus = run_engine("--bogus")
    assert bogus.returncode != 0, "an undeclared option exited 0"
    assert "unrecognized option" in bogus.stderr, bogus.stderr

    # A fifth action value is an argument error (argparse's invalid-choice exit 2).
    bad_action = run_engine("--action", "bogus")
    assert bad_action.returncode == 2, (
        f"--action bogus exited {bad_action.returncode}, expected 2: {bad_action.stderr}"
    )
    assert "invalid choice" in bad_action.stderr, bad_action.stderr

    # Read-only: a run creates no file inside the repository.
    before = snapshot()
    run_engine("--action", "inventory",
               "--spec", ".specify/specs/107-decision-governance",
               "--fixture", "tests/fixtures/decision-governance", "--json")
    run_engine("--action", "records", "--spec", ".specify/specs/107-decision-governance")
    after = snapshot()
    assert before == after, (
        "a run changed the repository tree: "
        f"created={sorted(set(after) - set(before))[:3]} removed={sorted(set(before) - set(after))[:3]}"
    )
