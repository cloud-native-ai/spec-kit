"""Contract test: root-resolution guard against the `.specify/.specify/` stray projection.

Two proven generators of the stray nested projection:
(a) sync-mirrors invoked via its `.specify/scripts/python/` mirror copy —
    `parents[2]` mis-roots to `.specify`, doubling every mirror target;
(b) `specify init` / agent render with a project path that IS a `.specify`
    runtime dir (cwd-based `--here`), installing a framework tree inside it.

House guard (owner: .specify/shared/definitions/dogfooding-definitions.md
§2.1 rule 4): a directory named `.specify` is never a repo/project root.
Engines carrying the guard: sync-mirrors.py, gate-check.py, tools-utils.py
(negative assertion on derived root) and specify_cli (init/render reject).
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from specify_cli import AgentMetadataError, render_agents_for_tool

pytestmark = pytest.mark.contract

REPO = Path(__file__).resolve().parents[2]


def _run(script: Path, cwd: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd, capture_output=True, text=True,
    )


def _sandbox(tmp_path: Path) -> Path:
    """Minimal framework-shaped tree: canonical sources + mirrors + stub regen."""
    for rel in (
        "scripts/python", "scripts/bash", "shared", "skills", "templates",
        ".specify/scripts/python", ".specify/scripts/bash",
        ".specify/shared", ".specify/skills", ".specify/templates",
    ):
        (tmp_path / rel).mkdir(parents=True, exist_ok=True)
    for dest in ("scripts/python/sync-mirrors.py",
                 ".specify/scripts/python/sync-mirrors.py"):
        shutil.copy2(REPO / "scripts/python/sync-mirrors.py", tmp_path / dest)
    for dest in ("scripts/python/gate-check.py",
                 ".specify/scripts/python/gate-check.py"):
        shutil.copy2(REPO / "scripts/python/gate-check.py", tmp_path / dest)
    (tmp_path / "scripts/python/regen-command-copies.py").write_text(
        "import sys; sys.exit(0)\n")
    (tmp_path / "shared/a.md").write_text("canonical a\n")
    (tmp_path / "scripts/bash/x.sh").write_text("#!/bin/sh\ntrue\n")
    (tmp_path / ".specify/scripts/bash/x.sh").write_text("#!/bin/sh\ntrue\n")
    return tmp_path


def test_mirror_placed_sync_mirrors_never_nests(tmp_path):
    sb = _sandbox(tmp_path)
    result = _run(sb / ".specify/scripts/python/sync-mirrors.py", sb, "--write")
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (sb / ".specify" / ".specify").exists()
    assert (sb / ".specify/shared/a.md").read_text() == "canonical a\n"


def test_canonical_and_mirror_check_agree(tmp_path):
    sb = _sandbox(tmp_path)
    canonical = _run(sb / "scripts/python/sync-mirrors.py", sb, "--check")
    mirror = _run(sb / ".specify/scripts/python/sync-mirrors.py", sb, "--check")
    assert (canonical.returncode, canonical.stdout) == (
        mirror.returncode, mirror.stdout)


def test_gate_check_walkup_ignores_stray_nested_specify(tmp_path):
    sb = _sandbox(tmp_path)
    (sb / ".specify/gate.yaml").write_text("allow:\n  - '**'\n")
    (sb / ".specify/.specify/shared").mkdir(parents=True)  # stray contaminant
    canonical = _run(sb / "scripts/python/gate-check.py", sb, "shared/a.md")
    mirror = _run(sb / ".specify/scripts/python/gate-check.py", sb, "shared/a.md")
    assert (canonical.returncode, canonical.stdout) == (
        mirror.returncode, mirror.stdout)
    assert canonical.returncode == 0, canonical.stdout + canonical.stderr


def test_render_rejects_specify_named_project_root(tmp_path):
    with pytest.raises(AgentMetadataError):
        render_agents_for_tool(tmp_path / ".specify", "qoder")
