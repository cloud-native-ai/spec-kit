"""Test-entry guard (FR-036, user ruling 2026-11-09) — raw pytest is not an entry.

Rows pinned here (WP4): T159. No contract clause is claimed: the user ruling names this
guard as the mechanical enforcement.

The guard walks the **tracked** framework artifacts — ``git ls-files`` over ``skills/``,
``templates/``, ``agents/``, ``shared/``, ``docs/reference/`` plus the live
``.specify/instructions.md`` — and turns red on a raw ``pytest`` / ``python3 -m pytest``
invocation. The allowlist is EXACTLY:

1. the runner itself (``scripts/bash/run-tests.sh``);
2. ``tests/fixtures/**`` (fixture data, not an execution instruction);
3. dated records (``.specify/memory/{session,feedback,history,evidence}/**`` and any
   ``test-evidence/**`` path);
4. feature spec trees (``.specify/specs/**`` — planning records, not execution
   instructions).

Red-first proof: the same scanner is run over a mutated copy carrying a raw invocation and
must report it; over a prose-only mutation it must stay quiet. The live tree is red until
T156–T158 (WP3) sweep the measured offenders — the failure message names every one.

Test execution for this module itself goes through ``scripts/bash/run-tests.sh`` (FR-036);
the runner name is data here, never an invocation.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

SCAN_ROOTS = ("skills", "templates", "agents", "shared", "docs/reference")
SCAN_EXTRA = (".specify/instructions.md",)

RUNNER_PATH = "scripts/bash/run-tests.sh"
ALLOWED_PREFIXES = (
    "tests/fixtures/",
    ".specify/memory/session/",
    ".specify/memory/feedback/",
    ".specify/memory/history/",
    ".specify/memory/evidence/",
    ".specify/specs/",
)

#: A raw invocation: the interpreter module form, or the bare command followed by a flag
#: or a path-like operand. Prose ("a pytest module", "pytest 模块", "pytest only
#: collects") does not match, because none of its following tokens is flag- or path-shaped.
RAW_INVOCATION = re.compile(
    r"\bpython3?\s+-m\s+pytest\b"
    r"|(?<![\w-])pytest\s+(?=(?:-{1,2}\w)|(?:[\w.<>~/]*[/\\])|(?:[\w.-]+\.py\b))"
)


def _is_allowlisted(path: str) -> bool:
    if path == RUNNER_PATH:
        return True
    if path.startswith(ALLOWED_PREFIXES):
        return True
    return "/test-evidence/" in path or path.startswith("test-evidence/")


def _tracked_files():
    proc = subprocess.run(
        ["git", "ls-files", "--", *SCAN_ROOTS, *SCAN_EXTRA],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0, proc.stderr
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _scan(paths, root=REPO_ROOT):
    """Return ``[(path, lineno, matched_text)]`` for raw invocations outside the allowlist."""
    findings = []
    for relative in paths:
        if _is_allowlisted(relative):
            continue
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in RAW_INVOCATION.finditer(line):
                start = max(0, match.start() - 20)
                findings.append((relative, lineno, line[start:match.end() + 40].strip()))
                break
    return findings


def test_allowlist_is_the_exact_closed_set():
    assert _is_allowlisted(RUNNER_PATH)
    assert _is_allowlisted("tests/fixtures/wp_fixtures.py")
    assert _is_allowlisted(".specify/memory/session/2026-11-09-note.md")
    assert _is_allowlisted(".specify/memory/feedback/x.md")
    assert _is_allowlisted(".specify/memory/history/x.md")
    assert _is_allowlisted(".specify/memory/evidence/x.jsonl")
    assert _is_allowlisted(".specify/specs/093-concurrency-by-default/tasks.md")
    assert not _is_allowlisted("skills/internal/implement-feature/SKILL.md")
    assert not _is_allowlisted("docs/reference/history/00-cross-cutting-lessons.md")
    assert not _is_allowlisted("tests/contract/test_test_entry_guard.py")


def test_mutated_copy_with_a_raw_invocation_turns_the_guard_red(tmp_path):
    source = REPO_ROOT / "shared" / "definitions" / "script-interface-definitions.md"
    mutated = tmp_path / "shared" / "definitions" / "script-interface-definitions.md"
    mutated.parent.mkdir(parents=True)
    mutated.write_text(
        source.read_text(encoding="utf-8")
        + "\nRun `python3 -m pytest tests/unit -q` before reporting.\n",
        encoding="utf-8")
    findings = _scan(["shared/definitions/script-interface-definitions.md"], root=tmp_path)
    assert findings, "the scanner must report a raw python3 -m pytest invocation"
    assert findings[0][0] == "shared/definitions/script-interface-definitions.md"
    assert "python3 -m pytest" in findings[0][2]


def test_mutated_copy_with_prose_only_stays_quiet(tmp_path):
    source = REPO_ROOT / "shared" / "definitions" / "script-interface-definitions.md"
    mutated = tmp_path / "shared" / "definitions" / "script-interface-definitions.md"
    mutated.parent.mkdir(parents=True)
    mutated.write_text(
        source.read_text(encoding="utf-8")
        + "\nA pytest module is exempt; pytest only collects test files; the pytest "
          "interpreter is resolved by the runner.\n",
        encoding="utf-8")
    assert _scan(["shared/definitions/script-interface-definitions.md"], root=tmp_path) == []


def test_the_runner_name_is_not_reported_by_name_alone(tmp_path):
    mutated = tmp_path / "docs" / "reference" / "note.md"
    mutated.parent.mkdir(parents=True)
    mutated.write_text(
        "Every test execution goes through `scripts/bash/run-tests.sh`; "
        "single-test debugging passes paths through it.\n", encoding="utf-8")
    assert _scan(["docs/reference/note.md"], root=tmp_path) == []


def test_live_tree_has_no_raw_invocation():
    findings = _scan(_tracked_files())
    summary = "\n".join("%s:%d: %s" % finding for finding in findings)
    assert findings == [], (
        "%d raw pytest invocation(s) remain in the scanned framework artifacts; the entry "
        "is scripts/bash/run-tests.sh (FR-036):\n%s" % (len(findings), summary))
