"""Non-regression contract guards for Feature 064 (NG-01…NG-13, additive)."""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    engine_json,
    four_piece,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
    run_watcher,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
ENGINE = SKILL_DIR / "scripts" / "line-registry.py"
WATCHER = SKILL_DIR / "scripts" / "watch-target.sh"
SPEC = REPO_ROOT / ".specify" / "specs" / "064-subagent-concurrency"
DOCS = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"


def test_ng_01_no_push_and_push_stub(tmp_path):
    for path in (ENGINE, WATCHER):
        assert "git push" not in path.read_text(encoding="utf-8")
    real_git = shutil.which("git")
    assert real_git, "git not available for the push-stub scenario"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "git-calls.log"
    log.write_text("", encoding="utf-8")
    stub = bin_dir / "git"
    stub.write_text(f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{log}"\nexec "{real_git}" "$@"\n', encoding="utf-8")
    stub.chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("push")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), "--state", "active", reg=reg,
    )
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", line, reg=reg)
    engine_json("integration-plan", reg=reg)
    engine_json(
        "integration-record", "--line-id", line, "--result", "failed",
        "--reason", "gate", reg=reg,
    )
    calls = [row for row in log.read_text().splitlines() if row.strip()]
    assert not any("push" in row for row in calls), calls


def test_ng_02_no_uncommitted_deletion():
    source = ENGINE.read_text(encoding="utf-8")
    assert "shutil.rmtree" not in source
    assert "--force" not in source
    archive_start = source.find("def action_archive_runtime")
    archive_body = source[archive_start:source.find("\ndef ", archive_start + 10)]
    assert ".unlink(" not in archive_body, "archive-runtime must not remove the source"
    docs = (SKILL_DIR / "references" / "dispatch-recipes.md").read_text(encoding="utf-8")
    assert "不得删除未提交工作" in docs or "MUST NOT 删除未提交工作" in docs or "保留 worktree" in docs


def test_ng_03_migration_content_preserved():
    notes = (SPEC / "notes" / "063-overlap-adjudication.md").read_text(encoding="utf-8")
    for index in range(1, 11):
        assert f"CP-{index:02d}" in notes, f"063 clause CP-{index:02d} missing from adjudication"
    for index in range(44, 50):
        assert f"FR-{index:03d}" in notes, f"063 clause FR-{index:03d} missing from adjudication"
    assert "Branch verification record" in notes
    contract = (SPEC / "contracts" / "cli-profiles.md").read_text(encoding="utf-8")
    for index in range(1, 11):
        assert f"CP-{index:02d}" in contract, f"064 carrier missing for CP-{index:02d}"


def test_ng_04_watcher_exit_codes_unchanged():
    source = WATCHER.read_text(encoding="utf-8")
    expected = {
        "EXIT_DONE=0": 0, "EXIT_RUNNING=10": 10, "EXIT_ANOMALY=11": 11,
        "EXIT_FAILED=12": 12, "EXIT_DEAD=13": 13, "EXIT_TIMEOUT=14": 14,
        "EXIT_INCOMPLETE=15": 15, "EXIT_NO_SIGNAL=16": 16, "EXIT_USAGE=2": 2,
    }
    for literal, code in expected.items():
        assert literal in source
        assert f"{code}" in literal
    help_text = subprocess.run(["bash", str(WATCHER), "--help"], capture_output=True, text=True).stdout
    for code, verdict in [
        (0, "DONE"), (10, "RUNNING"), (11, "ANOMALY"), (12, "FAILED"),
        (13, "DEAD"), (14, "TIMEOUT"), (15, "INCOMPLETE"), (16, "NO_SIGNAL"),
    ]:
        assert f"{code} {verdict}" in help_text


def test_ng_05_stdlib_only_engine():
    tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                imports.add(node.module.split(".")[0])
    allowed = {
        "argparse", "contextlib", "errno", "fcntl", "hashlib", "json", "os", "re",
        "secrets", "shutil", "socket", "subprocess", "sys", "tempfile", "time",
        "datetime", "pathlib", "__future__",
    }
    external = imports - allowed
    assert external == set(), f"non-stdlib imports: {sorted(external)}"
    assert WATCHER.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")


def test_ng_08_mirror_no_new_drift():
    skill = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "sync-mirrors.py"),
         "--check", "--only", "skills/external/sdd-loop-driver"],
        capture_output=True, text=True,
    )
    assert skill.returncode == 0, skill.stdout + skill.stderr
    probe = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "sync-mirrors.py"),
         "--check", "--only", "shared/definitions/probe-definitions.md"],
        capture_output=True, text=True,
    )
    assert probe.returncode == 0, probe.stdout + probe.stderr
    shared = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "sync-mirrors.py"),
         "--check", "--only", "shared/definitions"],
        capture_output=True, text=True,
    )
    baseline = {
        "agent-definitions.md", "contract-clause-definitions.md", "derivation-definitions.md",
        "dogfooding-definitions.md", "framework-map.md", "goal-definitions.md",
        "self-improvement-definitions.md", "subagent-definitions.md", "tool-definitions.md",
    }
    diffs = {
        Path(line.split()[-1]).name
        for line in shared.stdout.splitlines() if line.startswith("DIFF")
    }
    assert diffs == baseline, f"shared/definitions drift changed: {sorted(diffs)}"


def test_ng_09_docs_entry():
    text = DOCS.read_text(encoding="utf-8")
    assert "并发归属与生命周期" in text
    assert "CLI 能力档案" in text
    assert "references/cli/" in text
    assert "BASH_MAX_TIMEOUT_MS" not in text


def test_ng_07_single_line_compat(tmp_path):
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    proc = run_watcher(paths, line, run, "PLAN-DONE")
    assert proc.returncode == 0 and "verdict=DONE" in proc.stdout
    assert "attribution=own" in proc.stdout


def test_ng_13_planned_test_matrix_present():
    files = [
        "tests/unit/test_line_registry_engine.py",
        "tests/contract/test_line_registry_contract.py",
        "tests/contract/test_line_envelope_contract.py",
        "tests/contract/test_workspace_isolation_contract.py",
        "tests/contract/test_lifecycle_detach_reattach.py",
        "tests/contract/test_sdd_loop_driver_cli_profiles.py",
        "tests/contract/test_sdd_loop_driver_skill.py",
        "tests/integration/test_two_line_isolation.py",
        "tests/integration/test_worktree_integration_queue.py",
        "tests/integration/test_session_kill_reattach.py",
    ]
    for rel in files:
        assert (REPO_ROOT / rel).exists(), rel
    two_line = (REPO_ROOT / "tests" / "integration" / "test_two_line_isolation.py").read_text(encoding="utf-8")
    crash = (REPO_ROOT / "tests" / "integration" / "test_session_kill_reattach.py").read_text(encoding="utf-8")
    queue = (REPO_ROOT / "tests" / "integration" / "test_worktree_integration_queue.py").read_text(encoding="utf-8")
    assert "PLAN-DONE" in two_line and "foreign" in two_line
    assert "SIGHUP" in crash and "reservation" in crash
    assert "git fsck" in queue or "fsck" in queue
