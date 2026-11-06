"""Integration tests: `--action obligation` end-to-end scenarios (spec 087).

Owner of the assertion names and of each assertion's red-when condition: `plan.md` § Test Plan table A (rows
`C-002`, `C-006`, `C-011`, `C-012` and the `C-008a` rows of table B). Every case runs the engine as a
subprocess against a `tmp_path` copy of a fixture space, so nothing this file does can touch the repository
copy of a fixture — that invariant is the whole reason `tests/fixtures/docs-obligation/conftest.py::copy_fixture`
exists.

Read-only is asserted the way a reader can check it: run the engine, then ask git whether the space moved.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs-obligation"

sys.path.insert(0, str(FIXTURES))

import conftest as fixtures  # noqa: E402

DOC = "docs/concepts/widget-overview.md"


def run_engine(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
    )


def record_arg(space: Path) -> str:
    """The one trace-record file a fixture ships, as an absolute `--record` value."""
    runs = space / "docs" / ".speckit" / "runs"
    names = sorted(p.name for p in runs.glob("*.json"))
    assert len(names) == 1, f"expected exactly one trace record in {runs}, got {names}"
    return str(runs / names[0])


def git_status(space: Path) -> str:
    """`git status --porcelain` restricted to the space.

    The space lives under a `tmp_path`, outside the repository, so it is initialised as its own throwaway
    repository — which is exactly the question this assertion asks: did the engine's run change any byte, add
    any path, or touch any tracked file?
    """
    env = {
        "PATH": "/usr/bin:/bin",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_AUTHOR_NAME": "fixture",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    }
    subprocess.run(["git", "init", "-q"], cwd=space, check=True, capture_output=True, env=env)
    subprocess.run(["git", "add", "-A"], cwd=space, check=True, capture_output=True, env=env)
    subprocess.run(["git", "commit", "-qm", "fixture baseline"], cwd=space, check=True,
                   capture_output=True, env=env)
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=space, capture_output=True,
                          text=True, env=env, check=True)
    return proc.stdout


def obligation(space: Path, *extra: str) -> dict:
    proc = run_engine("--action", "obligation", "--root", str(space), *extra)
    assert proc.returncode == 0, f"engine exited {proc.returncode}: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# C-002 (read-only by construction) and C-006 rule 1/2 (determinism, idempotence)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_c002_two_runs_identical_json(tmp_path: Path):
    """Two runs over one input produce byte-identical stdout, and neither run moves a byte on disk.

    red-when: the two payloads differ in any byte (ordering, field set, a timestamp leaking into the output),
    or the space is dirty after either run.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record = record_arg(space)
    assert git_status(space) == "", "the fixture baseline commit must leave a clean tree"

    first = run_engine("--action", "obligation", "--root", str(space), "--record", record)
    after_first = git_status(space)
    second = run_engine("--action", "obligation", "--root", str(space), "--record", record)
    after_second = git_status(space)

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout, "two runs of one input must serialise identically"
    assert after_first == "", f"the first run wrote to the space: {after_first!r}"
    assert after_second == "", f"the second run wrote to the space: {after_second!r}"


@pytest.mark.integration
def test_c002_no_writes_on_dirty_fixture(tmp_path: Path):
    """A space that is already dirty is judged without the engine adding to the dirt.

    The dirty state is deliberate: an unjudgeable extra carrier plus an unreadable exemption record. Whatever
    the engine decides, it decides read-only.

    red-when: `git status --porcelain` grows after the run — the engine created, modified or deleted a file.
    """
    space = fixtures.copy_fixture("exempt-bad", tmp_path)
    (space / "docs" / "concepts" / "extra.md").write_text(
        "# Extra carrier\n\nNo diagram here either.\n", encoding="utf-8")
    before = git_status(space)
    assert before != "", "this case needs a dirty baseline to be meaningful"

    obligation(space)
    after = git_status(space)
    assert after == before, f"the engine wrote to a dirty space: before={before!r} after={after!r}"
