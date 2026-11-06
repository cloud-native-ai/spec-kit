"""Contract tests for Feature 085 child lines in the 064 line registry."""

from __future__ import annotations

import json
import subprocess

import pytest

from fixtures.line_fixtures import (
    base_env,
    engine_json,
    make_git_repo,
    make_line_id,
    make_run_id,
    run_engine,
)

pytestmark = pytest.mark.contract


def _register(reg, project, **overrides):
    args = [
        "--line-id", overrides.pop("line_id", make_line_id()),
        "--run-id", overrides.pop("run_id", make_run_id()),
        "--project-dir", str(overrides.pop("project_dir", project)),
        "--repo-root", str(overrides.pop("repo_root", project)),
        "--state", overrides.pop("state", "active"),
    ]
    for flag, value in overrides.items():
        flag = f"--{flag.replace('_', '-')}"
        if value is True:
            args.append(flag)
        elif value is not None:
            args += [flag, str(value)]
    return engine_json("register", *args, reg=reg)


def _head(repo):
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def test_child_line_requires_parent_and_write_isolation(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    parent = _register(reg, repo, line_id="parent-20260101T000000Z-aaaa")
    child = _register(
        reg, repo,
        parent_line_id=parent["line_id"],
        line_role="agent-write",
        write_line=True,
        worktree_path=str(tmp_path / "wt-child"),
        branch=f"line/{make_line_id('child')}",
        base_sha=_head(repo),
    )
    assert child["parent_line_id"] == parent["line_id"]
    assert child["line_role"] == "agent-write"
    assert child["agent_cap"] == 24


def test_grandchild_is_rejected(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    parent = _register(reg, repo, line_id="parent-20260101T000000Z-bbbb")
    child = _register(
        reg, repo,
        parent_line_id=parent["line_id"],
        line_role="agent-write",
        write_line=True,
        worktree_path=str(tmp_path / "wt-child-2"),
        branch=f"line/{make_line_id('child')}",
        base_sha=_head(repo),
    )
    proc = run_engine(
        "register",
        "--line-id", "grandchild-20260101T000000Z-cccc",
        "--run-id", make_run_id(),
        "--project-dir", str(repo),
        "--repo-root", str(repo),
        "--parent-line-id", child["line_id"],
        "--line-role", "agent-write",
        "--write-line",
        "--worktree-path", str(tmp_path / "wt-grandchild"),
        "--branch", f"line/{make_line_id('grandchild')}",
        "--base-sha", _head(repo),
        reg=reg,
    )
    assert proc.returncode != 0
    assert "must not itself be a child" in (proc.stdout + proc.stderr)


def test_agent_concurrency_cap_is_enforced(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    parent = _register(reg, repo, line_id="parent-20260101T000000Z-dddd")
    env = base_env(reg, {"SPECIFY_AGENT_CONCURRENCY_CAP": "1"})
    first = engine_json(
        "register",
        "--line-id", "child-a-20260101T000000Z-eeee",
        "--run-id", make_run_id(),
        "--project-dir", str(repo),
        "--repo-root", str(repo),
        "--parent-line-id", parent["line_id"],
        "--line-role", "agent-write",
        "--write-line",
        "--worktree-path", str(tmp_path / "wt-a"),
        "--branch", f"line/{make_line_id('a')}",
        "--base-sha", _head(repo),
        reg=reg, env=env,
    )
    assert first["line_role"] == "agent-write"
    proc = run_engine(
        "register",
        "--line-id", "child-b-20260101T000000Z-ffff",
        "--run-id", make_run_id(),
        "--project-dir", str(repo),
        "--repo-root", str(repo),
        "--parent-line-id", parent["line_id"],
        "--line-role", "agent-write",
        "--write-line",
        "--worktree-path", str(tmp_path / "wt-b"),
        "--branch", f"line/{make_line_id('b')}",
        "--base-sha", _head(repo),
        reg=reg, env=env,
    )
    assert proc.returncode == 3
    assert "agent-concurrency-cap" in (proc.stdout + proc.stderr)


def test_child_lines_do_not_consume_the_root_concurrency_cap(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    parent = _register(reg, repo, line_id="parent-20260101T000000Z-gggg", stage="implement")
    _register(
        reg, repo,
        parent_line_id=parent["line_id"],
        line_role="agent-write",
        write_line=True,
        stage="implement",
        worktree_path=str(tmp_path / "wt-child-3"),
        branch=f"line/{make_line_id('child')}",
        base_sha=_head(repo),
    )
    env = base_env(reg, {"SPECIFY_LINE_CONCURRENCY_CAP": "1"})
    proc = run_engine(
        "allocate-resources", "--line-id", parent["line_id"], "--cap", "1",
        reg=reg, env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload.get("resources", {}).get("ports"), "root line should receive resources"
