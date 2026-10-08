"""Contract test: conflict-free store state protocol (req 055 / Feature 055).

One behavioral suite run against BOTH engines (feedback-utils / memory-utils)
so the two embedded protocol implementations cannot drift:

1. legacy index migration — every field carried, index retired, migrated
   disclosed;
2. read-side legacy fallback — legacy scalars visible read-only, nothing
   deleted by a read action;
3. reindex idempotence — a second run migrates nothing;
4. concurrent-append isolation — record touches only the new entry file
   (content-hash proof over every pre-existing file, state/ included);
5. two-branch merge demonstration — the motivating scenario: branch A and
   branch B each record one entry, git merge produces zero conflicts and
   both entries survive;
6. atomic writes — a failure mid-write leaves no .part residue.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.script_api import feedback_utils as fu
from tests.script_api import memory_utils as mu

FEEDBACK_STORE = Path(".specify") / "memory" / "feedback"
SESSION_DIR = Path(".specify") / "memory" / "session"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _fb_record(root: Path, run_id: str, review: str = "r", points: str = "- p") -> dict:
    args = argparse.Namespace(
        workspace_root=str(root), unit_id="/speckit.plan", unit_type="command",
        run_id=run_id, review=review, review_file=None,
        points=points, points_file=None, partial=False,
        feature="", feature_id="", threshold=None,
        lifecycle_point=None, format="json",
    )
    return fu.action_record(args)


def _mu_record(root: Path, title: str) -> dict:
    args = argparse.Namespace(
        workspace_root=str(root), scope="session", source="/speckit.plan",
        title=title, content=f"body of {title}", tags="", feature="",
        session_id="", content_file=None, format="json",
    )
    return mu.action_record(args)


def _tree_hash(root: Path) -> dict:
    """Content hash of every file under root (path -> md5 hex)."""
    import hashlib
    out = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            out[path.relative_to(root).as_posix()] = hashlib.md5(
                path.read_bytes()).hexdigest()
    return out


def _seed_legacy_feedback(root: Path) -> None:
    """A full pre-055 store: entry file + index.json with all three scalars
    plus an introspection record."""
    store = root / FEEDBACK_STORE
    store.mkdir(parents=True, exist_ok=True)
    entry_file = store / "20260101T000000Z-speckit-plan.md"
    entry_file.write_text(
        "---\nid: 20260101T000000Z-speckit-plan\n"
        "unit_id: /speckit.plan\nunit_type: command\nrun_id: legacy-run\n"
        "scope: local\nprobe: speckit-plan-wrapup\nkind: internal\n"
        "slice: commands\nfeature: \"\"\nfeature_id: \"\"\ndisposition: \"\"\n"
        "partial: false\ncreated: 2026-01-01T00:00:00Z\nsummary: legacy entry\n"
        "---\n\n## Review\nlegacy\n\n## Optimization Points\n- old\n",
        encoding="utf-8")
    (store / "index.json").write_text(json.dumps({
        "store": "feedback", "updated": "2026-01-01T00:00:00Z",
        "threshold": 7, "count_since_submission": 1,
        "submitted_at": "2025-12-01T00:00:00Z",
        "upstream_repo": "https://example.com/up.git",
        "entries": [{"id": "20260101T000000Z-speckit-plan",
                     "file": "20260101T000000Z-speckit-plan.md",
                     "unit_id": "/speckit.plan", "unit_type": "command",
                     "run_id": "legacy-run", "probe": "speckit-plan-wrapup",
                     "kind": "internal", "slice": "commands", "feature": "",
                     "feature_id": "", "disposition": "",
                     "introspection_ref": "", "disposition_reason": "",
                     "partial": False, "created": "2026-01-01T00:00:00Z",
                     "summary": "legacy entry"}],
        "introspections": [{"id": "introspection-20260101T000000Z",
                            "file": "introspection/introspection-20260101T000000Z.md",
                            "created": "2026-01-01T00:00:00Z",
                            "status": "confirmed", "supersedes": None,
                            "entries": ["20260101T000000Z-speckit-plan"]}],
    }, indent=2), encoding="utf-8")
    report_dir = store / "introspection"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "introspection-20260101T000000Z.md").write_text(
        "---\nid: introspection-20260101T000000Z\n"
        "created: 2026-01-01T00:00:00Z\nstatus: confirmed\n"
        "scope_filter: \"disposition=open\"\n"
        "scope_entries: [\"20260101T000000Z-speckit-plan\"]\n"
        "supersedes: null\nconfirmed_at: \"2026-01-02T00:00:00Z\"\n---\n\n"
        "# Introspection Report\n",
        encoding="utf-8")


def _seed_legacy_memory(root: Path) -> None:
    """A pre-055 memory store: two entry files plus a LYING index.json
    (registers only one of them) — the scan must win."""
    sdir = root / SESSION_DIR
    sdir.mkdir(parents=True, exist_ok=True)
    for name, title in (("20260101T000000Z-first.md", "First note"),
                        ("20260102T000000Z-second.md", "Second note")):
        (sdir / name).write_text(
            f"---\nid: {name[:-3]}\nscope: session\nsource: /speckit.plan\n"
            f"feature: \"\"\ntags: [\"wip\"]\ntitle: {json.dumps(title)}\n"
            f"created: 2026-01-0{1 if 'first' in name else 2}T00:00:00Z\n"
            f"summary: {json.dumps(title)}\n---\n\nbody\n",
            encoding="utf-8")
    (sdir / "index.json").write_text(json.dumps({
        "scope": "session", "updated": "2026-01-02T00:00:00Z",
        "entries": [{"id": "20260101T000000Z-first",
                     "file": "20260101T000000Z-first.md",
                     "scope": "session", "source": "/speckit.plan",
                     "feature": "", "tags": ["wip"], "title": "First note",
                     "created": "2026-01-01T00:00:00Z",
                     "summary": "First note"}],
    }, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. migration carries every legacy field
# --------------------------------------------------------------------------- #
@pytest.mark.contract
class TestFeedbackMigration:
    def test_first_write_migrates_all_scalars_and_retires_index(self, tmp_path):
        _seed_legacy_feedback(tmp_path)
        out = _fb_record(tmp_path, "post-migration")
        assert out["migrated"] is True
        assert not (tmp_path / FEEDBACK_STORE / "index.json").exists()

        sdir = tmp_path / FEEDBACK_STORE / "state"
        assert json.loads((sdir / "threshold.json").read_text()) == {"threshold": 7}
        assert json.loads((sdir / "submitted-at.json").read_text()) == {
            "submitted_at": "2025-12-01T00:00:00Z"}
        assert json.loads((sdir / "upstream-repo.json").read_text()) == {
            "upstream_repo": "https://example.com/up.git"}

        state = fu.load_store_state(tmp_path)
        assert state["legacy"] is False
        assert state["threshold"] == 7
        assert state["submitted_at"] == "2025-12-01T00:00:00Z"
        assert state["upstream_repo"] == "https://example.com/up.git"
        # entries: the legacy one plus the new one — scan-derived, never lost
        assert {e["run_id"] for e in state["entries"]} == {"legacy-run", "post-migration"}
        assert [r["id"] for r in state["introspections"]] == [
            "introspection-20260101T000000Z"]
        assert state["introspections"][0]["status"] == "confirmed"

    def test_reindex_is_the_explicit_migration_entry(self, tmp_path):
        _seed_legacy_feedback(tmp_path)
        args = argparse.Namespace(workspace_root=str(tmp_path), threshold=None)
        out = fu.action_reindex(args)
        assert out == {"reindexed": 1, "migrated": True}
        assert not (tmp_path / FEEDBACK_STORE / "index.json").exists()

    def test_default_threshold_is_not_materialized(self, tmp_path):
        _fb_record(tmp_path, "fresh")
        sdir = tmp_path / FEEDBACK_STORE / "state"
        assert not (sdir / "threshold.json").exists(), (
            "absence = default 10; a state file for the default value would be churn")


@pytest.mark.contract
class TestMemoryMigration:
    def test_record_over_lying_legacy_index_deletes_it(self, tmp_path):
        _seed_legacy_memory(tmp_path)
        out = _mu_record(tmp_path, "Third note")
        assert out["migrated"] is True
        assert not (tmp_path / SESSION_DIR / "index.json").exists()
        entries = mu.load_index(tmp_path, "session")["entries"]
        assert len(entries) == 3

    def test_scan_wins_over_lying_index(self, tmp_path):
        """The pre-055 failure mode this feature closes: the index says one
        entry while three files exist — the scan must see all three."""
        _seed_legacy_memory(tmp_path)
        entries = mu.load_index(tmp_path, "session")["entries"]
        assert len(entries) == 2  # index claimed 1; files say 2

    def test_reindex_migrates_per_scope(self, tmp_path):
        _seed_legacy_memory(tmp_path)
        args = argparse.Namespace(workspace_root=str(tmp_path), scope="all")
        out = mu.action_reindex(args)
        assert out["migrated"] == ["session"]
        assert not (tmp_path / SESSION_DIR / "index.json").exists()
        # idempotent
        out2 = mu.action_reindex(args)
        assert out2["migrated"] == []


# --------------------------------------------------------------------------- #
# 2. read-side legacy fallback (read actions never delete)
# --------------------------------------------------------------------------- #
@pytest.mark.contract
def test_feedback_read_actions_use_legacy_scalars_without_deleting(tmp_path):
    _seed_legacy_feedback(tmp_path)
    args = argparse.Namespace(workspace_root=str(tmp_path), threshold=None)
    status = fu.action_status(args)
    assert status["legacy"] is True
    assert status["threshold"] == 7
    assert status["submitted_at"] == "2025-12-01T00:00:00Z"
    listing = fu.action_list(argparse.Namespace(
        workspace_root=str(tmp_path), unit_id=None, unit_type=None, since=None,
        limit=0, contains=None, slice=None, kind=None, disposition=None))
    assert listing["count"] == 1
    # read-only: the legacy index survives untouched
    assert (tmp_path / FEEDBACK_STORE / "index.json").is_file()


@pytest.mark.contract
def test_feedback_duplicate_record_does_not_migrate(tmp_path):
    _seed_legacy_feedback(tmp_path)
    out = _fb_record(tmp_path, "legacy-run")  # (unit_id, run_id) already exists
    assert out["duplicate"] is True
    assert out["migrated"] is False
    assert (tmp_path / FEEDBACK_STORE / "index.json").is_file(), (
        "a no-op record performs no writes, hence no migration")


# --------------------------------------------------------------------------- #
# 3+4. isolation: record touches only the new entry file
# --------------------------------------------------------------------------- #
@pytest.mark.contract
class TestConcurrentAppendIsolation:
    def test_feedback_record_leaves_every_prior_file_untouched(self, tmp_path):
        _fb_record(tmp_path, "a1")
        (tmp_path / FEEDBACK_STORE / "backlog.md").write_text("# backlog\n")
        before = _tree_hash(tmp_path)
        _fb_record(tmp_path, "a2")
        after = _tree_hash(tmp_path)
        new_files = set(after) - set(before)
        changed = {k for k in set(before) & set(after) if before[k] != after[k]}
        assert not changed, f"record rewrote existing files: {changed}"
        assert len(new_files) == 1 and new_files.pop().endswith(".md")

    def test_memory_record_leaves_every_prior_file_untouched(self, tmp_path):
        _mu_record(tmp_path, "note one")
        before = _tree_hash(tmp_path)
        _mu_record(tmp_path, "note two")
        after = _tree_hash(tmp_path)
        changed = {k for k in set(before) & set(after) if before[k] != after[k]}
        assert not changed, f"record rewrote existing files: {changed}"
        new_files = set(after) - set(before)
        assert len(new_files) == 1
        assert new_files.pop().endswith(".md")

    def test_no_index_json_is_ever_created(self, tmp_path):
        _fb_record(tmp_path, "a")
        _mu_record(tmp_path, "note")
        assert not list((tmp_path / FEEDBACK_STORE).glob("index.json"))
        assert not list((tmp_path / SESSION_DIR).glob("index.json"))


# --------------------------------------------------------------------------- #
# 5. the motivating scenario: two branches, one merge, zero conflicts
# --------------------------------------------------------------------------- #
@pytest.mark.contract
class TestTwoBranchMerge:
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, text=True)

    def _record_on_branch(self, repo: Path, run_id: str) -> None:
        p = subprocess.run(
            [sys.executable, str(repo / "scripts/python/feedback-utils.py"),
             "--action", "record", "--workspace-root", str(repo),
             "--unit-id", "/speckit.plan", "--unit-type", "command",
             "--run-id", run_id, "--review", "r", "--points", "- p"],
            capture_output=True, text=True)
        assert p.returncode == 0, p.stderr

    def test_branch_merge_yields_zero_conflicts_and_both_entries(self, tmp_path):
        import shutil
        import time
        repo = tmp_path / "repo"
        repo.mkdir()
        scripts_dir = repo / "scripts/python"
        scripts_dir.mkdir(parents=True)
        shutil.copy(Path(fu.__file__), scripts_dir / "feedback-utils.py")
        (repo / ".specify").mkdir()
        # Entry filenames carry second granularity: two branches recording
        # the SAME unit within the same wall-clock second collide on the
        # filename itself (a pre-existing property, unchanged by req 055).
        # Cross the boundary so each record lands in its own second — the
        # realistic multi-branch scenario this feature closes.
        self._git(repo, "init", "-q")
        self._git(repo, "config", "user.email", "t@example.com")
        self._git(repo, "config", "user.name", "T")
        self._git(repo, "checkout", "-q", "-b", "main")
        self._record_on_branch(repo, "base-run")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-q", "-m", "base")

        self._git(repo, "checkout", "-q", "-b", "feature-a")
        time.sleep(1.1)
        self._record_on_branch(repo, "run-a")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-q", "-m", "a")

        self._git(repo, "checkout", "-q", "main")
        self._git(repo, "checkout", "-q", "-b", "feature-b")
        time.sleep(1.1)
        self._record_on_branch(repo, "run-b")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-q", "-m", "b")

        self._git(repo, "checkout", "-q", "feature-a")
        merge = self._git(repo, "merge", "--no-edit", "feature-b")
        assert merge.returncode == 0, (
            f"merge conflicted — the exact failure this feature exists to close: "
            f"{merge.stdout}{merge.stderr}")

        # post-merge: both branches' entries are visible, nothing duplicated
        state = fu.load_store_state(repo)
        runs = {e["run_id"] for e in state["entries"]}
        assert runs == {"base-run", "run-a", "run-b"}
        assert not (repo / FEEDBACK_STORE / "index.json").exists()


# --------------------------------------------------------------------------- #
# 6. atomic writes leave no .part residue
# --------------------------------------------------------------------------- #
@pytest.mark.contract
class TestAtomicWrites:
    def test_failed_state_write_leaves_no_part_file(self, tmp_path, monkeypatch):
        _seed_legacy_feedback(tmp_path)

        def flaky_replace(src, dst):
            raise OSError("disk full (simulated)")

        monkeypatch.setattr(fu.os, "replace", flaky_replace)
        with pytest.raises(OSError):
            _fb_record(tmp_path, "never-lands")
        monkeypatch.undo()

        parts = list((tmp_path / FEEDBACK_STORE).rglob("*.part"))
        assert not parts, f".part residue survived a failed write: {parts}"
        # the legacy index still stands — migration never half-finished
        assert (tmp_path / FEEDBACK_STORE / "index.json").is_file()
