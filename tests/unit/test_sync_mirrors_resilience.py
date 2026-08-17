"""Unit tests for sync-mirrors write-mode resilience (038 backlog: per-file error collection).

A write failure on one mirror file (e.g. a root-owned leftover) must not abort
the pass: the remaining files still sync, the failure is reported per file, and
the run exits 1 with a summary — a stale mirror never passes silently.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/sync-mirrors.py"

pytestmark = pytest.mark.unit

skip_if_root = pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    reason="root ignores file-mode write protection",
)


def _load_engine():
    spec = importlib.util.spec_from_file_location("sync_mirrors_resilience", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sync_mirrors_resilience"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    module = _load_engine()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(module, "MIRROR_PAIRS", [("csrc", "cdst", False, frozenset())])
    src = tmp_path / "csrc"
    src.mkdir()
    (src / "a.md").write_text("canonical A v2\n", encoding="utf-8")
    (src / "b.md").write_text("canonical B\n", encoding="utf-8")
    dst = tmp_path / "cdst"
    dst.mkdir()
    (dst / "a.md").write_text("stale A v1\n", encoding="utf-8")
    return module, tmp_path


def _run(module, monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["sync-mirrors.py", *argv])
    return module.main()


@skip_if_root
def test_unwritable_file_is_collected_and_rest_still_syncs(sandbox, monkeypatch, capsys):
    module, root = sandbox
    stale = root / "cdst/a.md"
    stale.chmod(0o444)  # write-protected target ⇒ copy2 raises PermissionError
    try:
        rc = _run(module, monkeypatch, "--write")
    finally:
        stale.chmod(0o644)  # restore so pytest cleanup can remove the tree
    assert rc == 1, "a write failure must end non-zero"
    out = capsys.readouterr().out
    assert "FAIL  cdst/a.md" in out
    assert "SYNC FAILURES: 1" in out
    # the sibling file still synced — the pass did not abort
    assert (root / "cdst/b.md").read_text(encoding="utf-8") == "canonical B\n"
    # the unwritable mirror stayed stale, never silently overwritten-or-skipped
    assert stale.read_text(encoding="utf-8") == "stale A v1\n"


def test_clean_write_exits_zero(sandbox, monkeypatch):
    module, root = sandbox
    rc = _run(module, monkeypatch, "--write")
    assert rc == 0
    assert (root / "cdst/a.md").read_text(encoding="utf-8") == "canonical A v2\n"
    assert (root / "cdst/b.md").read_text(encoding="utf-8") == "canonical B\n"


@skip_if_root
def test_summary_lists_every_failure(sandbox, monkeypatch, capsys):
    module, root = sandbox
    (root / "csrc/c.md").write_text("canonical C\n", encoding="utf-8")
    (root / "cdst/c.md").write_text("stale C\n", encoding="utf-8")
    for name in ("a.md", "c.md"):
        (root / "cdst" / name).chmod(0o444)
    try:
        rc = _run(module, monkeypatch, "--write")
    finally:
        for name in ("a.md", "c.md"):
            (root / "cdst" / name).chmod(0o644)
    assert rc == 1
    out = capsys.readouterr().out
    assert "SYNC FAILURES: 2" in out
    assert "FAIL  cdst/a.md" in out and "FAIL  cdst/c.md" in out
