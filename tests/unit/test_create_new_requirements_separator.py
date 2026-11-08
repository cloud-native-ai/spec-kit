"""T093 — the requirements scaffold honours `--` and never waits on stdin."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_REL = "scripts/bash/create-new-requirements.sh"


def _tree(tmp_path: Path) -> Path:
    tree = tmp_path / "tree"
    (tree / ".specify" / "specs").mkdir(parents=True)
    shutil.copytree(ROOT / "scripts" / "bash", tree / "scripts" / "bash")
    (tree / "pyproject.toml").write_text('[project]\nname = "s"\nversion = "1.0.0"\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tree, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.invalid"], cwd=tree, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tree, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-q", "-m", "init"], cwd=tree, check=True)
    return tree


def _run(tree: Path, *args: str):
    return subprocess.run(["bash", SCRIPT_REL, *args], cwd=tree, capture_output=True,
                          text=True, timeout=20, stdin=subprocess.DEVNULL,
                          env=dict(os.environ))


def test_a_token_after_separator_is_an_operand_and_does_not_hang(tmp_path):
    tree = _tree(tmp_path)
    before = sorted((tree / ".specify" / "specs").iterdir())
    proc = _run(tree, "--", "--script-interface-check-after-separator")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    after = [p for p in (tree / ".specify" / "specs").iterdir() if p not in before]
    assert len(after) == 1, f"expected exactly one scaffolded spec, got {after}"
    assert "script-interface" in after[0].name


def test_no_input_exits_with_usage_without_reading_stdin(tmp_path):
    tree = _tree(tmp_path)
    before = sorted((tree / ".specify" / "specs").iterdir())
    proc = _run(tree)
    assert proc.returncode != 0
    assert "Usage:" in proc.stderr, proc.stderr
    assert sorted((tree / ".specify" / "specs").iterdir()) == before
