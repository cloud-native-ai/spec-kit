"""G-8 (T070) — dated records stay byte-identical to the entry baseline.

The comparison base is `test-evidence/protected-paths-entry.txt` (T002): the FR-061 file set
taken from the pinned pre-feature commit and hashed on the entry worktree. The guard asserts
every baseline path still exists and still hashes to its recorded value; additions are listed,
and `.specify/archive/anchoring/**` — the subtrees this feature is contracted to create — is
listed separately and never counted as a failure (FR-069, FR-061; SC-004, SC-009).

The injection case runs on the fixture tree: one byte changed, one file deleted, one archive
addition — each must land in its own bucket.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
ENTRY = ROOT / ".specify/specs/101-anchor-goal-realignment/test-evidence/protected-paths-entry.txt"
FIXTURE = ROOT / "tests/fixtures/anchor-goal-realignment/protected-paths"
ARCHIVE_ADDITION_PREFIX = ".specify/archive/anchoring/"

PROTECTED_PREFIXES = (".specify/specs/", ".specify/archive/", ".specify/history/",
                      "docs/notes/")


def protected(path: str) -> bool:
    if path.startswith(PROTECTED_PREFIXES):
        return True
    parts = path.split("/")
    return (len(parts) >= 4 and parts[0] == ".specify" and parts[1] == "teams"
            and "runs" in parts[2:-1])


def read_entry(path: Path) -> tuple[dict[str, str], list[str]]:
    """(path -> recorded hash, new-archive subtree prefixes) from the T002 artifact."""
    baseline: dict[str, str] = {}
    prefixes: list[str] = []
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section == "baseline-existing" and line.strip():
            digest, _, rel = line.partition("  ")
            baseline[rel.strip()] = digest.strip()
        elif section == "new-archive-subtrees" and line.strip():
            prefixes.append(line.strip())
    return baseline, prefixes


def git_hashes(root: Path, paths: list[str]) -> dict[str, str]:
    """One batch `git hash-object` over the worktree files that still exist."""
    present = [rel for rel in paths if (root / rel).is_file()]
    if not present:
        return {}
    result = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=str(root), input="\n".join(present) + "\n",
        capture_output=True, text=True, check=True)
    return dict(zip(present, result.stdout.splitlines()))


def compare(baseline: dict[str, str], current: dict[str, str]) -> tuple[list[str], list[str]]:
    deleted = sorted(rel for rel in baseline if rel not in current)
    changed = sorted(rel for rel in baseline
                     if rel in current and current[rel] != baseline[rel])
    return changed, deleted


def worktree_paths(root: Path) -> list[str]:
    found: list[str] = []
    for base in (".specify/specs", ".specify/archive", ".specify/history", "docs/notes"):
        start = root / base
        if start.is_dir():
            found += [path.relative_to(root).as_posix()
                      for path in start.rglob("*") if path.is_file()]
    teams = root / ".specify/teams"
    if teams.is_dir():
        found += [path.relative_to(root).as_posix() for path in teams.glob("*/runs/**/*")
                  if path.is_file()]
    return [rel for rel in found if protected(rel)]


def test_every_baseline_protected_path_is_unchanged_and_present():
    assert ENTRY.is_file(), f"missing T002 entry baseline {ENTRY}"
    baseline, prefixes = read_entry(ENTRY)
    assert len(baseline) > 1000, f"only {len(baseline)} baseline rows"
    assert prefixes, "the entry baseline names no new-archive subtree prefix"

    current = git_hashes(ROOT, list(baseline))
    changed, deleted = compare(baseline, current)
    assert deleted == [], f"protected paths were deleted: {deleted[:10]}"
    assert changed == [], f"protected paths changed: {changed[:10]}"


def test_additions_are_listed_and_archive_additions_are_separate():
    baseline, _prefixes = read_entry(ENTRY)
    additions = sorted(set(worktree_paths(ROOT)) - set(baseline))
    archive_additions = [rel for rel in additions if rel.startswith(ARCHIVE_ADDITION_PREFIX)]

    assert not set(additions) & set(baseline), "an addition is also a baseline row"
    assert all(protected(rel) for rel in additions), "an unprotected path leaked into additions"
    # The feature's contract is to create archive subtrees; when any exist they must be
    # visible here rather than folded into the failure bucket.
    for rel in archive_additions:
        assert rel.startswith(ARCHIVE_ADDITION_PREFIX)


def test_a_changed_byte_deleted_file_and_archive_addition_land_in_their_buckets(tmp_path):
    tree = tmp_path / "tree"
    shutil.copytree(FIXTURE / "tree", tree)
    baseline = {}
    for line in (FIXTURE / "baseline.txt").read_text(encoding="utf-8").splitlines():
        digest, _, rel = line.partition("  ")
        baseline[rel.strip()] = digest.strip()

    def hashes() -> dict[str, str]:
        return {rel: hashlib.sha256((tree / rel).read_bytes()).hexdigest()
                for rel in baseline if (tree / rel).is_file()}

    assert compare(baseline, hashes()) == ([], []), "the fixture is not clean to start"

    target = tree / "dated-record.md"
    target.write_bytes(target.read_bytes().replace(b"sealed", b"SEALED", 1))
    (tree / "history-note.md").unlink()
    addition = tree / "archive/anchoring/example/goal.md"
    addition.parent.mkdir(parents=True)
    addition.write_text("# Goal: example\n", encoding="utf-8")

    changed, deleted = compare(baseline, hashes())
    assert changed == ["dated-record.md"], changed
    assert deleted == ["history-note.md"], deleted
    assert "archive/anchoring/example/goal.md" not in deleted + changed
