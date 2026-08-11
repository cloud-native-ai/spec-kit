"""Unit tests for the feedback processing side: package + upstream detection.

Covers Feature 028 processing-side additions:
- ``package`` produces a zip while leaving source entry files byte-for-byte intact
- MANIFEST carries entry count, version, and install-source fields
- ``detect_upstream`` priority: configured > PEP 610 direct_url.json > none
- red-line guard: the engine source performs no network / push operations
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from tests.script_api import feedback_utils as fu


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _record(workspace: Path, unit_id: str, run_id: str) -> None:
    args = argparse.Namespace(
        workspace_root=str(workspace), unit_id=unit_id, unit_type="command",
        run_id=run_id, review="review prose", review_file=None,
        points="- a point", points_file=None, partial=False,
        feature="028", threshold=100, since=None, limit=5,
        set_url=None, all=False, format="json",
    )
    fu.action_record(args)


def _pkg_args(workspace: Path, take_all: bool = False) -> argparse.Namespace:
    return argparse.Namespace(workspace_root=str(workspace), all=take_all)


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# package: sources untouched
# --------------------------------------------------------------------------- #
def test_package_leaves_source_entries_untouched(tmp_path):
    _record(tmp_path, "/speckit.plan", "r1")
    _record(tmp_path, "/speckit.tasks", "r2")
    store = fu.feedback_dir(tmp_path)
    entry_files = sorted(store.glob("*.md"))
    before = {p.name: _md5(p) for p in entry_files}

    result = fu.action_package(_pkg_args(tmp_path))

    after = {p.name: _md5(p) for p in sorted(store.glob("*.md"))}
    assert before == after, "package must not modify or remove source entry files"
    assert result["packaged"] == 2
    assert result["zip"] and Path(tmp_path / result["zip"]).exists()


def test_package_zip_contains_entries_and_manifest(tmp_path):
    _record(tmp_path, "/speckit.plan", "r1")
    result = fu.action_package(_pkg_args(tmp_path))
    zip_path = tmp_path / result["zip"]
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        manifest = zf.read("MANIFEST.md").decode("utf-8")
    assert "MANIFEST.md" in names
    assert any(n.endswith(".md") and n != "MANIFEST.md" for n in names)
    assert "Entries" in manifest and "spec-kit version" in manifest
    assert "Spec Kit framework itself" in manifest  # positioning statement


def test_package_empty_store_is_noop(tmp_path):
    result = fu.action_package(_pkg_args(tmp_path))
    assert result["packaged"] == 0
    assert result["zip"] is None


def test_package_respects_submitted_at_boundary(tmp_path, monkeypatch):
    # Drive a monotonically increasing clock so mark-submitted lands strictly
    # between the two records (real usage separates them by seconds; the test
    # must not depend on wall-clock or same-second collisions). A counter avoids
    # StopIteration since now_iso() is called several times per action.
    counter = {"n": 0}

    def fake_now():
        counter["n"] += 1
        return f"2026-01-01T00:00:{counter['n']:02d}Z"

    monkeypatch.setattr(fu, "now_iso", fake_now)
    _record(tmp_path, "/speckit.plan", "r1")
    fu.action_mark_submitted(argparse.Namespace(workspace_root=str(tmp_path)))
    _record(tmp_path, "/speckit.tasks", "r2")
    # default: only entries after submitted_at
    assert fu.action_package(_pkg_args(tmp_path))["packaged"] == 1
    # --all: full store
    assert fu.action_package(_pkg_args(tmp_path, take_all=True))["packaged"] == 2


# --------------------------------------------------------------------------- #
# mark-submitted: archive-then-reset (audit fixes F2/F3)
# --------------------------------------------------------------------------- #
def test_mark_submitted_archives_batch_before_reset(tmp_path):
    _record(tmp_path, "/speckit.plan", "r1")
    _record(tmp_path, "/speckit.tasks", "r2")

    result = fu.action_mark_submitted(
        argparse.Namespace(workspace_root=str(tmp_path))
    )

    assert result["reset_from"] == 2
    assert result["packaged"] == 2
    assert result["zip"] and (tmp_path / result["zip"]).exists()
    with zipfile.ZipFile(tmp_path / result["zip"]) as zf:
        names = zf.namelist()
    assert "MANIFEST.md" in names
    assert sum(1 for n in names if n.endswith(".md") and n != "MANIFEST.md") == 2
    index = fu.load_index(tmp_path)
    assert index["count_since_submission"] == 0


def test_mark_submitted_embeds_submission_notes(tmp_path):
    _record(tmp_path, "/speckit.plan", "r1")

    result = fu.action_mark_submitted(
        argparse.Namespace(workspace_root=str(tmp_path),
                           notes="batch applied to templates/commands/x.md")
    )

    with zipfile.ZipFile(tmp_path / result["zip"]) as zf:
        assert "SUBMISSION-NOTES.md" in zf.namelist()
        notes = zf.read("SUBMISSION-NOTES.md").decode("utf-8")
    assert "batch applied to templates/commands/x.md" in notes


def test_mark_submitted_without_pending_entries_still_resets(tmp_path):
    result = fu.action_mark_submitted(
        argparse.Namespace(workspace_root=str(tmp_path))
    )
    assert result["packaged"] == 0
    assert result["zip"] is None
    assert fu.load_index(tmp_path)["count_since_submission"] == 0


# --------------------------------------------------------------------------- #
# record: requirement key vs Feature registry ID (audit fix F1)
# --------------------------------------------------------------------------- #
def test_record_persists_feature_id_distinctly(tmp_path):
    args = argparse.Namespace(
        workspace_root=str(tmp_path), unit_id="/speckit.plan",
        unit_type="command", run_id="f1", review="review prose",
        review_file=None, points="- a point", points_file=None,
        partial=False, feature="038-goal-target", feature_id="041",
        threshold=100, format="json",
    )
    fu.action_record(args)

    entry = fu.load_index(tmp_path)["entries"][0]
    assert entry["feature"] == "038-goal-target"
    assert entry["feature_id"] == "041"
    text = (fu.feedback_dir(tmp_path) / entry["file"]).read_text(encoding="utf-8")
    assert 'feature: "038-goal-target"' in text
    assert 'feature_id: "041"' in text


# --------------------------------------------------------------------------- #
# upstream detection priority
# --------------------------------------------------------------------------- #
def test_upstream_prefers_configured_over_metadata(monkeypatch):
    monkeypatch.setattr(
        fu, "detect_upstream", fu.detect_upstream  # keep real impl
    )
    idx = {"upstream_repo": "https://example.com/custom/spec-kit.git"}
    out = fu.detect_upstream(idx)
    assert out["url"] == "https://example.com/custom/spec-kit.git"
    assert out["source"] == "configured"


def test_upstream_falls_back_to_direct_url(monkeypatch):
    class _Dist:
        def read_text(self, name):
            assert name == "direct_url.json"
            return json.dumps({
                "url": "https://gitlab.example.com/team/spec-kit.git",
                "vcs_info": {"vcs": "git", "commit_id": "abc123"},
            })

    from importlib import metadata as im
    monkeypatch.setattr(im, "distribution", lambda name: _Dist())
    out = fu.detect_upstream({})
    assert out["url"] == "https://gitlab.example.com/team/spec-kit.git"
    assert out["source"] == "install-metadata"
    assert out["commit"] == "abc123"


def test_upstream_none_when_undetectable(monkeypatch):
    from importlib import metadata as im

    def _boom(name):
        raise im.PackageNotFoundError(name)

    monkeypatch.setattr(im, "distribution", _boom)
    out = fu.detect_upstream({})
    assert out["url"] is None and out["source"] is None


def test_action_upstream_persists_set_url(tmp_path):
    args = argparse.Namespace(workspace_root=str(tmp_path), set_url="https://x.example/r.git")
    out = fu.action_upstream(args)
    assert out["url"] == "https://x.example/r.git"
    saved = json.loads(fu.index_path(tmp_path).read_text(encoding="utf-8"))
    assert saved["upstream_repo"] == "https://x.example/r.git"


# --------------------------------------------------------------------------- #
# red line: no network / push in engine source
# --------------------------------------------------------------------------- #
def test_engine_source_has_no_network_or_push():
    src = (Path(fu.__file__)).read_text(encoding="utf-8")
    forbidden = ["urllib.request", "import requests", "import httpx",
                 "http.client", "socket.socket", "git push", "subprocess"]
    hits = [tok for tok in forbidden if tok in src]
    assert not hits, f"engine must perform no network/push operations, found: {hits}"
