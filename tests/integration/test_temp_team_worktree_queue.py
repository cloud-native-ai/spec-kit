"""Integration test: two child lines run concurrently, then merge through the 064 queue."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from fixtures.line_fixtures import (
    engine_json,
    git,
    make_git_repo,
    make_run_id,
)

ROOT = Path(__file__).resolve().parents[2]
EXECUTOR = ROOT / "skills/external/sdd-loop-driver/scripts/integrate-lines.py"


def _register(reg: Path, repo: Path, line: str, *, parent: str | None = None,
              worktree: Path | None = None) -> dict:
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    args = [
        "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active",
    ]
    if parent:
        args += [
            "--parent-line-id", parent,
            "--line-role", "agent-write",
            "--write-line",
            "--worktree-path", str(worktree),
            "--branch", f"line/{line}",
            "--base-sha", base,
        ]
    return engine_json("register", *args, reg=reg)


def _add_worktree(repo: Path, worktree: Path, line: str) -> None:
    git(repo, "worktree", "add", "-q", "-b", f"line/{line}", str(worktree), "main")


def _commit(worktree: Path, relative: str, content: str, message: str) -> str:
    path = worktree / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    git(worktree, "add", relative)
    git(worktree, "commit", "-q", "-m", message)
    return git(worktree, "rev-parse", "HEAD").stdout.strip()


def _execute(repo: Path, reg: Path, archive: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EXECUTOR), "--repo", str(repo), "--trunk", "main",
         "--registry", str(reg), "--archive", str(archive),
         "--gate-cmd", "test -f README.md"],
        capture_output=True, text=True,
    )


def test_two_child_lines_are_concurrent_then_merge_in_order(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    parent = "parent-20261020T120000Z-aaaa"
    children = ["child-a-20261020T120000Z-bbbb", "child-b-20261020T120000Z-cccc"]
    worktrees = [tmp_path / "wt-a", tmp_path / "wt-b"]

    _register(reg, repo, parent)
    for child, worktree in zip(children, worktrees):
        _register(reg, repo, child, parent=parent, worktree=worktree)
        _add_worktree(repo, worktree, child)

    # Both child lines are active at the same time under the agent cap.
    stored = [json.loads((reg / f"{child}.json").read_text()) for child in children]
    assert all(row["state"] == "active" for row in stored)
    assert all(row["parent_line_id"] == parent for row in stored)
    assert all(row["agent_cap"] == 24 for row in stored)

    for index, (child, worktree) in enumerate(zip(children, worktrees)):
        _commit(worktree, f"src/child{index}.txt", f"child {index}\n",
                f"child {index}")
        engine_json("update", "--line-id", child, "--state", "completed", reg=reg)
        engine_json("integration-enqueue", "--line-id", child,
                    "--at", f"2026-10-20T12:00:0{index}Z", reg=reg)

    proc = _execute(repo, reg, tmp_path / "archive")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    summary = json.loads(proc.stdout)
    assert [row["line_id"] for row in summary["results"]] == children
    assert all(row["status"] == "merged" for row in summary["results"])
    assert all(worktree.exists() is False for worktree in worktrees)
    assert (repo / "src/child0.txt").exists() and (repo / "src/child1.txt").exists()

    fsck = subprocess.run(["git", "-C", str(repo), "fsck", "--no-dangling"],
                          capture_output=True, text=True)
    assert fsck.returncode == 0, fsck.stderr
    # Rebase may rewrite SHAs; the work is what must survive, not the original hashes.
    messages = git(repo, "log", "--format=%s", "--all").stdout
    assert "child 0" in messages and "child 1" in messages, "a child change was lost"

    for child in children:
        row = json.loads((reg / f"{child}.json").read_text())
        assert row["integration_result"]["status"] == "merged"
