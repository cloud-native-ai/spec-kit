"""Unit tests: workspace-guard snapshots and detects branch/spec drift."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "python" / "workspace-guard.py"


def _git(tree: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(tree), check=True, capture_output=True, text=True)


def _repo(tmp_path: Path) -> Path:
    tree = tmp_path / "repo"
    one = tree / ".specify" / "specs" / "001-one"
    one.mkdir(parents=True)
    (one / "requirements.md").write_text("# one\n", encoding="utf-8")
    _git(tree, "init", "-q")
    _git(tree, "config", "user.email", "guard@example.invalid")
    _git(tree, "config", "user.name", "guard")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "one")
    return tree


def _run(*args: str):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def test_snapshot_then_check_is_clean(tmp_path):
    tree = _repo(tmp_path)
    snap = tmp_path / "snap.json"
    assert _run("--snapshot", str(snap), "--repo", str(tree)).returncode == 0
    proc = _run("--check", str(snap), "--repo", str(tree))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "clean" in proc.stdout


def test_branch_and_spec_drift_is_detected(tmp_path):
    tree = _repo(tmp_path)
    snap = tmp_path / "snap.json"
    _run("--snapshot", str(snap), "--repo", str(tree))
    _git(tree, "branch", "leak-branch")
    (tree / ".specify" / "specs" / "999-leak").mkdir()
    proc = _run("--check", str(snap), "--repo", str(tree), "--json")
    assert proc.returncode == 1
    assert "refs" in proc.stdout and "specs" in proc.stdout


def test_input_error_is_two(tmp_path):
    proc = _run("--check", str(tmp_path / "absent.json"), "--repo", str(tmp_path))
    assert proc.returncode == 2


def test_contract_surface(tmp_path):
    help_proc = _run("--help")
    assert help_proc.returncode == 0
    for label in ("usage:", "options", "side-effects:", "exit-codes:"):
        assert label in help_proc.stdout, label
    ver = _run("--version")
    assert ver.returncode == 0 and len(ver.stdout.strip().splitlines()) == 1
    assert _run("--no-such-flag").returncode == 2
