"""Contract test: pre-analyze derives the repo root when ``--repo`` is omitted.

The old default was an empty string, and ``check_paths`` returned early on it, so an
omitted ``--repo`` silently disabled every declared-path check (backlog F10, 2026-11-23).
The fix derives the repo from the nearest ancestor carrying a ``.specify/`` child:
the standard spec tree is ``<repo>/.specify/specs/<NNN-slug>/``. An explicit ``--repo``
still wins; a spec tree with no ``.specify`` ancestor is not silently green — it warns
on stderr and states that path checks are skipped.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "pre-analyze-check.py"
MISSING = "docs/missing-file.md"


def _run(spec_dir: Path, out: Path, repo: Path | None = None):
    args = [
        sys.executable, str(ENGINE),
        "--spec-dir", str(spec_dir),
        "--stage", "requirements",
        "--json-out", str(out),
    ]
    if repo is not None:
        args += ["--repo", str(repo)]
    return subprocess.run(args, cwd=str(spec_dir), capture_output=True, text=True)


def _record(out: Path) -> dict:
    assert out.is_file(), "the engine wrote no --json-out record"
    return json.loads(out.read_text(encoding="utf-8"))


def _has_missing_path(record: dict, path: str) -> bool:
    return any(
        "path does not exist under the repo: %s" % path in finding.get("message", "")
        for finding in record.get("findings", [])
    )


def _spec_tree(root: Path) -> Path:
    spec = root / ".specify" / "specs" / "001-test"
    spec.mkdir(parents=True)
    (spec / "requirements.md").write_text(
        "# Requirements\n\n**Flow Class**: expression\n\nSee `%s` for the missing deliverable.\n" % MISSING,
        encoding="utf-8",
    )
    return spec


def test_omitted_repo_derives_the_specify_ancestor(tmp_path):
    repo = tmp_path / "repo"
    spec = _spec_tree(repo)
    out = tmp_path / "record.json"
    proc = _run(spec, out)
    assert proc.returncode != 2, proc.stderr
    assert _has_missing_path(_record(out), MISSING), (
        "an omitted --repo silently skipped the declared-path check; the derived repo "
        "root must judge %r" % MISSING
    )


def test_explicit_repo_still_wins(tmp_path):
    repo = tmp_path / "repo"
    spec = _spec_tree(repo)
    out = tmp_path / "record.json"
    proc = _run(spec, out, repo=repo)
    assert proc.returncode != 2, proc.stderr
    assert _has_missing_path(_record(out), MISSING)


def test_no_specify_ancestor_warns_instead_of_silent_green(tmp_path):
    spec = tmp_path / "loose-spec"
    spec.mkdir()
    (spec / "requirements.md").write_text(
        "# Requirements\n\n**Flow Class**: expression\n\nSee `%s`.\n" % MISSING,
        encoding="utf-8",
    )
    out = tmp_path / "record.json"
    proc = _run(spec, out)
    assert proc.returncode != 2, proc.stderr
    assert "repo root not resolved" in proc.stderr, (
        "a spec tree with no .specify ancestor must state that path checks are skipped, "
        "not look green silently"
    )
    assert not _has_missing_path(_record(out), MISSING)
