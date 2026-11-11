"""Integration tests for the documented rollback recipe (Feature 100, P7).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md``
          C-110 — rollback is a documented git-level recipe, the engine gains no
          undo action. Walkthrough: ``quickstart.md`` S-6.
Clause:   SC-010 — the recipe returns the tree to the pinned commit byte for
          byte, and skipping any step turns the completion check red.

The replay tree is a throwaway copy of ``tests/fixtures/seal-archive/runtime-present``
under ``tmp_path``; the runtime records are force-tracked there (the fixture's
``.gitignore`` covers ``.specify/state/``) so the inverse runtime write is a
visible part of the clean-tree check. The live repository is never written.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "seal-archive"

PARENT = "100-fixture-parent"
ALPHA = "100a-fixture-alpha"
BETA = "100b-fixture-beta"
SPEC_REL = ".specify/specs/%s" % PARENT
MANIFEST_REL = SPEC_REL + "/archive-manifest.json"
MERGE_REL = SPEC_REL + "/merge-manifest.json"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    })
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
         *args],
        capture_output=True, text=True, encoding="utf-8", check=False, env=env,
    )


def _replay(tmp_path: Path) -> Path:
    repo = tmp_path / "replay"
    shutil.copytree(FIXTURES / "runtime-present", repo)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    assert _git(repo, "add", "-f", ".specify/state").returncode == 0, (
        "C-309: the replay tracks its runtime records so the inverse write is "
        "part of the clean-tree check"
    )
    assert _git(repo, "commit", "-qm", "fixture baseline").returncode == 0
    return repo


def _run(repo: Path, action: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", action,
         "--spec-dir", str(repo / SPEC_REL), "--repo", str(repo), "--json"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert proc.stdout.strip(), (
        f"expected a stdout payload for {action}; exit={proc.returncode} "
        f"stderr={proc.stderr[-800:]!r}"
    )
    return proc, json.loads(proc.stdout)


def _apply(repo: Path) -> dict:
    proc, payload = _run(repo, "archive-apply")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "archived"
    return payload["archive"]["manifest"]


def _lines(path: Path) -> list:
    return path.read_text(encoding="utf-8").splitlines()


def _write_lines(path: Path, lines: list, trailing_newline: bool) -> None:
    path.write_text("\n".join(lines) + ("\n" if trailing_newline else ""),
                    encoding="utf-8")


def _rollback(repo: Path, manifest: dict, skip: str | None = None) -> None:
    """Execute the C-110 / quickstart S-6 recipe step by step.

    ``skip`` names one step to leave out; the negative tests use it to prove the
    completion check is what catches a missing step.
    """
    pinned = manifest["pinned_commit"]
    rows = manifest["references"]["rows"]
    runtime = manifest["references"]["runtime"]

    # ① the rollback plan is read from the manifest itself (slices[] + rows[])
    slices = manifest["slices"]

    # ② inverse `git mv`, per slices[] order
    if skip != "move":
        for entry in slices:
            result = _git(repo, "mv", entry["to"], entry["from"])
            assert result.returncode == 0, result.stderr[-400:]

    # ③ restore every live-rewrite carrier and the parent merge manifest
    carriers = sorted({row["carrier"] for row in rows if row["kind"] == "live-rewrite"}
                      | {MERGE_REL})
    if skip != "restore" and carriers:
        result = _git(repo, "restore", "--source", pinned, "--staged", "--worktree",
                      "--", *carriers)
        assert result.returncode == 0, result.stderr[-400:]

    # ④ inverse-write the runtime carriers: after -> before, line by line
    if skip != "runtime":
        for row in runtime:
            if row["status"] != "runtime-updated" or not row["updates"]:
                continue
            path = repo / row["carrier"]
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            for update in sorted(row["updates"], key=lambda item: item["line"]):
                index = update["line"] - 1
                assert lines[index] == update["after"], (
                    "%s:%d no longer carries the applied line"
                    % (row["carrier"], update["line"]))
                lines[index] = update["before"]
            _write_lines(path, lines, text.endswith("\n"))

    # ⑤ remove the archive record apply created (index first, when tracked)
    if skip != "manifest":
        tracked = _git(repo, "ls-files", "--", MANIFEST_REL)
        if tracked.stdout.strip():
            result = _git(repo, "rm", "-f", "--cached", "--", MANIFEST_REL)
            assert result.returncode == 0, result.stderr[-400:]
        path = repo / MANIFEST_REL
        if path.exists():
            path.unlink()


def _violations(repo: Path, manifest: dict) -> list:
    """The C-110 completion check: tree vs pinned, status, and row-by-row lines."""
    pinned = manifest["pinned_commit"]
    paths = [SPEC_REL]
    paths += [entry["from"] for entry in manifest["slices"]]
    paths += sorted({row["carrier"] for row in manifest["references"]["rows"]})
    problems = []

    diff = _git(repo, "diff", "--exit-code", pinned, "--", *paths)
    if diff.returncode != 0:
        problems.append("tree differs from the pinned commit:\n" + diff.stdout)

    status = _git(repo, "status", "--porcelain")
    if status.stdout.strip():
        problems.append("worktree is not clean:\n" + status.stdout)

    for row in manifest["references"]["rows"]:
        path = repo / row["carrier"]
        if not path.is_file():
            problems.append("carrier absent after rollback: " + row["carrier"])
            continue
        lines = _lines(path)
        index = row["line"] - 1
        actual = lines[index] if 0 <= index < len(lines) else None
        if actual != row["before"]:
            problems.append("%s:%d does not read its `before` line"
                            % (row["carrier"], row["line"]))

    for row in manifest["references"]["runtime"]:
        if row["status"] != "runtime-updated":
            continue
        path = repo / row["carrier"]
        if not path.is_file():
            problems.append("runtime carrier absent: " + row["carrier"])
            continue
        lines = _lines(path)
        for update in row["updates"]:
            index = update["line"] - 1
            actual = lines[index] if 0 <= index < len(lines) else None
            if actual != update["before"]:
                problems.append("%s:%d runtime line not restored"
                                % (row["carrier"], update["line"]))
    return problems


# ---------------------------------------------------------------------------
# SC-010 — the full recipe returns the tree byte for byte
# ---------------------------------------------------------------------------

def test_rollback_restores_byte_identical_tree(tmp_path):
    repo = _replay(tmp_path)
    manifest = _apply(repo)
    assert manifest["references"]["rows"], (
        "the fixture must exercise live rewrites; otherwise step ③ restores nothing"
    )
    runtime = manifest["references"]["runtime"]
    assert any(row["status"] == "runtime-updated" and row["updates"]
               for row in runtime), (
        "the fixture must exercise the runtime inverse write; otherwise step ④ "
        "restores nothing"
    )

    _rollback(repo, manifest)
    assert _violations(repo, manifest) == []

    proc, payload = _run(repo, "archive-plan")
    assert proc.returncode == 0, payload.get("conditions")
    assert payload["outcome"] == "would-archive", (
        "the restored tree is archive-ready again, not a drifted tree"
    )
    assert payload["archive"]["manifest"] == manifest, (
        "C-110: the restored tree reproduces the same plan byte for byte"
    )


# ---------------------------------------------------------------------------
# SC-010 — skipping any step turns the completion check red
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("step", ["move", "restore", "runtime", "manifest"])
def test_skipping_a_rollback_step_turns_the_check_red(tmp_path, step):
    repo = _replay(tmp_path)
    manifest = _apply(repo)
    _rollback(repo, manifest, skip=step)
    assert _violations(repo, manifest), (
        "C-110/SC-010: omitting the `%s` step MUST fail the completion check" % step
    )
