"""Contract tests for framework source-stamp resolution (043-init-commit-stamp, T002).

Contract: .specify/specs/043-init-commit-stamp/contracts/source-stamp-resolution.contract.md

Pins the single git-probe grammar (_probe_head_commit: bounded subprocess, 40-hex
validation, never raises) and the constant resolution order of
resolve_source_commit: checkout git probe > build-embedded value > unavailable.
Resolution is read-only; unavailability is data (commit=None + reason), never an
exception, and no path may fabricate an id.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

import specify_cli as sc

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

pytestmark = pytest.mark.contract

FAKE_COMMIT = "a" * 40
ALT_FAKE_COMMIT = "b" * 40


@pytest.fixture()
def git_repo(tmp_path):
    """A real throwaway git repo with one commit; returns its root."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "c"],
        cwd=repo, check=True)
    return repo


def _head(repo: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True,
        capture_output=True, text=True).stdout.strip()


def _plain_dir(tmp_path, name="plain"):
    d = tmp_path / name
    d.mkdir()
    return d


def _with_embedded(d: Path, payload) -> Path:
    (d / "_source_commit.json").write_text(
        payload if isinstance(payload, str) else json.dumps(payload),
        encoding="utf-8")
    return d


# --------------------------------------------------------------------------
# C-1 the single probe grammar
# --------------------------------------------------------------------------

def test_probe_returns_head_inside_a_git_repo(git_repo):
    commit, reason = sc._probe_head_commit(git_repo)
    assert commit == _head(git_repo), "probe MUST match git rev-parse HEAD char-for-char"
    assert COMMIT_RE.match(commit)
    assert reason is None


def test_probe_returns_none_with_reason_outside_git(tmp_path):
    commit, reason = sc._probe_head_commit(_plain_dir(tmp_path))
    assert commit is None
    assert reason, "unavailability MUST carry a reason"


def test_probe_never_raises_when_git_binary_missing(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError("no git")
    monkeypatch.setattr(sc.subprocess, "run", boom)
    commit, reason = sc._probe_head_commit(_plain_dir(tmp_path))
    assert commit is None
    assert reason


def test_probe_rejects_non_hex_output(git_repo, monkeypatch):
    monkeypatch.setattr(
        sc.subprocess, "run",
        lambda *a, **k: subprocess.CompletedProcess(a, 0, stdout="not-a-commit\n"))
    commit, reason = sc._probe_head_commit(git_repo)
    assert commit is None and reason


# --------------------------------------------------------------------------
# C-2 constant resolution order: git > embedded > unavailable
# --------------------------------------------------------------------------

def test_resolve_prefers_git_inside_a_checkout(git_repo, monkeypatch):
    monkeypatch.setattr(sc, "MODULE_DIR", git_repo)
    out = sc.resolve_source_commit()
    assert out["origin"] == "git"
    assert out["commit"] == _head(git_repo)
    assert out["reason"] is None


def test_resolve_uses_embedded_when_git_absent(tmp_path, monkeypatch):
    d = _with_embedded(_plain_dir(tmp_path), {"commit": FAKE_COMMIT})
    monkeypatch.setattr(sc, "MODULE_DIR", d)
    out = sc.resolve_source_commit()
    assert out["origin"] == "embedded"
    assert out["commit"] == FAKE_COMMIT
    assert out["reason"] is None


def test_resolve_unavailable_when_nothing_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "MODULE_DIR", _plain_dir(tmp_path))
    out = sc.resolve_source_commit()
    assert out["origin"] == "unavailable"
    assert out["commit"] is None
    assert out["reason"]


# --------------------------------------------------------------------------
# C-3 embedded-file tolerance: malformed input is data, not an exception
# --------------------------------------------------------------------------

def test_resolve_tolerates_malformed_embedded_json(tmp_path, monkeypatch):
    d = _with_embedded(_plain_dir(tmp_path), "{not json")
    monkeypatch.setattr(sc, "MODULE_DIR", d)
    out = sc.resolve_source_commit()
    assert out["origin"] == "unavailable" and out["commit"] is None


def test_resolve_tolerates_invalid_embedded_field(tmp_path, monkeypatch):
    d = _with_embedded(_plain_dir(tmp_path), {"commit": "xyz"})
    monkeypatch.setattr(sc, "MODULE_DIR", d)
    out = sc.resolve_source_commit()
    assert out["origin"] == "unavailable" and out["commit"] is None


def test_resolve_passes_embedded_unavailable_through(tmp_path, monkeypatch):
    d = _with_embedded(_plain_dir(tmp_path),
                       {"commit": "unavailable", "reason": "built without git"})
    monkeypatch.setattr(sc, "MODULE_DIR", d)
    out = sc.resolve_source_commit()
    assert out["origin"] == "embedded"
    assert out["commit"] is None
    assert out["reason"] == "built without git"


def test_resolve_is_read_only(tmp_path, monkeypatch):
    d = _plain_dir(tmp_path)
    monkeypatch.setattr(sc, "MODULE_DIR", d)
    sc.resolve_source_commit()
    assert list(d.iterdir()) == [], "resolution MUST not write anything"


# --------------------------------------------------------------------------
# write face (043 US1): source-stamp-write.contract.md C-1..C-3
# --------------------------------------------------------------------------

STAMP_RELPATH = ".specify/source.json"  # [[STR-001]]
FRAMEWORK_NAME = "spec-kit"             # [[STR-003]]
STAMP_TS_RE = re.compile(r"^\d{8}T\d{6}Z$")


def _resolve_result(commit=FAKE_COMMIT, origin="git", reason=None):
    return {"commit": commit, "origin": origin, "reason": reason}


def test_write_lands_the_exact_payload(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit",
                        lambda: _resolve_result())
    assert sc.write_source_stamp(tmp_path) is True
    stamp = tmp_path / STAMP_RELPATH
    assert stamp.is_file(), "stamp MUST land at .specify/source.json"
    payload = json.loads(stamp.read_text(encoding="utf-8"))
    assert payload["framework"] == FRAMEWORK_NAME
    assert payload["commit"] == FAKE_COMMIT
    assert "reason" not in payload, "reason key MUST be absent when commit is valid"
    assert STAMP_TS_RE.match(payload["stamped_at"])


def test_write_payload_is_pretty_json(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit",
                        lambda: _resolve_result(commit=ALT_FAKE_COMMIT))
    sc.write_source_stamp(tmp_path)
    text = (tmp_path / STAMP_RELPATH).read_text(encoding="utf-8")
    assert text.startswith("{\n  \""), "indent-2 pretty JSON expected"
    assert text.endswith("}\n"), "trailing newline expected"


def test_write_creates_specify_dir_defensively(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit", lambda: _resolve_result())
    assert sc.write_source_stamp(tmp_path) is True
    assert (tmp_path / ".specify").is_dir()


def test_write_failure_warns_and_never_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit", lambda: _resolve_result())
    real_write = Path.write_text

    def boom(self, *a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(Path, "write_text", boom)
    assert sc.write_source_stamp(tmp_path) is False, \
        "write failure MUST return False, not raise (stamping never blocks init)"
    monkeypatch.setattr(Path, "write_text", real_write)


# --------------------------------------------------------------------------
# refresh face (043 US2): full-overwrite, zero stale residue, no version key
# --------------------------------------------------------------------------

OLD_COMMIT = "c" * 40
NEW_COMMIT = "d" * 40


def test_refresh_overwrites_with_zero_stale_residue(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit",
                        lambda: _resolve_result(commit=OLD_COMMIT))
    assert sc.write_source_stamp(tmp_path) is True
    monkeypatch.setattr(sc, "resolve_source_commit",
                        lambda: _resolve_result(commit=NEW_COMMIT))
    assert sc.write_source_stamp(tmp_path) is True
    text = (tmp_path / STAMP_RELPATH).read_text(encoding="utf-8")
    assert OLD_COMMIT not in text, "stale commit MUST leave zero residue (FR-006)"
    assert NEW_COMMIT in text, "the NEW form must be present and correct"


def test_payload_values_never_carry_the_formal_version(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "resolve_source_commit", lambda: _resolve_result())
    sc.write_source_stamp(tmp_path)
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
    payload = json.loads((tmp_path / STAMP_RELPATH).read_text(encoding="utf-8"))
    assert all(value != version for value in payload.values()), \
        "the pyproject version must never be a payload value (FR-002)"
