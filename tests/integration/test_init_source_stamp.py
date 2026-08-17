"""Integration tests: init writes the framework source stamp (043-init-commit-stamp, T006).

Spec: .specify/specs/043-init-commit-stamp/ — US1 independent test: run a real
`specify init` (CliRunner, minimal resource fixture) and assert the stamp lands
at .specify/source.json carrying the framework repo's actual HEAD; plus the
SC-002 reverse-lookup closure: two distinct commits stamped, `git show` hits
both in the framework repo.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import specify_cli as sc
from tests.script_api import RUNNER, app

pytestmark = pytest.mark.integration

STAMP_RELPATH = ".specify/source.json"


def _repo_head(rev: str = "HEAD") -> str:
    return subprocess.run(
        ["git", "rev-parse", rev], cwd=Path(__file__).resolve().parents[2],
        check=True, capture_output=True, text=True).stdout.strip()


def _invoke_init(monkeypatch, tmp_path, resource_path, project="demo-proj"):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sc, "get_resource_path", lambda: resource_path)
    return RUNNER.invoke(app, [
        "init", project, "--ai", "qoder", "--no-git",
        "--ignore-agent-tools", "--skip-tls"])


def test_init_lands_the_stamp_with_real_head(
        tmp_path, monkeypatch, qoder_minimal_resource_path):
    result = _invoke_init(monkeypatch, tmp_path, qoder_minimal_resource_path)
    assert result.exit_code == 0, result.output
    stamp = tmp_path / "demo-proj" / STAMP_RELPATH
    assert stamp.is_file(), "init MUST land the source stamp"
    payload = json.loads(stamp.read_text(encoding="utf-8"))
    assert payload["framework"] == "spec-kit"
    assert payload["commit"] == _repo_head(), \
        "checkout-form init MUST stamp the framework repo's HEAD"
    assert "reason" not in payload


def test_reverse_lookup_hits_both_stamped_commits(tmp_path, monkeypatch):
    """SC-002 closure: stamp two distinct commits, `git show` hits each."""
    repo = Path(__file__).resolve().parents[2]
    head = _repo_head("HEAD")
    parent = _repo_head("HEAD~1")
    assert head != parent
    for value in (head, parent):
        monkeypatch.setattr(
            sc, "resolve_source_commit",
            lambda v=value: {"commit": v, "origin": "git", "reason": None})
        assert sc.write_source_stamp(tmp_path) is True
        payload = json.loads((tmp_path / STAMP_RELPATH).read_text(encoding="utf-8"))
        assert payload["commit"] == value
        show = subprocess.run(["git", "show", "--quiet", value],
                              cwd=repo, capture_output=True)
        assert show.returncode == 0, f"git show failed for {value}"


def test_reinit_refreshes_the_stamp(tmp_path, monkeypatch,
                                    qoder_minimal_resource_path):
    """US2: a second init (upgrade path via --here --force) overwrites the
    stamp with the new source commit — zero stale residue."""
    result = _invoke_init(monkeypatch, tmp_path, qoder_minimal_resource_path)
    assert result.exit_code == 0, result.output
    project = tmp_path / "demo-proj"
    old = json.loads((project / STAMP_RELPATH).read_text(encoding="utf-8"))

    fresh = "e" * 40
    monkeypatch.chdir(project)
    monkeypatch.setattr(
        sc, "resolve_source_commit",
        lambda: {"commit": fresh, "origin": "git", "reason": None})
    again = RUNNER.invoke(app, [
        "init", "--here", "--force", "--ai", "qoder", "--no-git",
        "--ignore-agent-tools", "--skip-tls"])
    assert again.exit_code == 0, again.output
    text = (project / STAMP_RELPATH).read_text(encoding="utf-8")
    assert old["commit"] not in text, "stale commit must not survive re-init"
    assert json.loads(text)["commit"] == fresh


def test_legacy_project_gains_the_stamp(tmp_path, monkeypatch,
                                        qoder_minimal_resource_path):
    """US2/FR-007: a project initialized before this feature (no stamp file)
    gains it on the next init with zero migration."""
    project = tmp_path / "legacy"
    (project / ".specify").mkdir(parents=True)
    (project / ".specify" / "instructions.md").write_text("# legacy\n",
                                                          encoding="utf-8")
    monkeypatch.chdir(project)
    monkeypatch.setattr(sc, "get_resource_path",
                        lambda: qoder_minimal_resource_path)
    result = RUNNER.invoke(app, [
        "init", "--here", "--force", "--ai", "qoder", "--no-git",
        "--ignore-agent-tools", "--skip-tls"])
    assert result.exit_code == 0, result.output
    stamp = json.loads((project / STAMP_RELPATH).read_text(encoding="utf-8"))
    assert stamp["commit"] == _repo_head()


def test_unavailable_resolution_still_leaves_init_green(tmp_path, monkeypatch,
                                                        qoder_minimal_resource_path):
    """US3/FR-005: honest degradation — sentinel stamp, init unaffected."""
    monkeypatch.setattr(
        sc, "resolve_source_commit",
        lambda: {"commit": None, "origin": "unavailable", "reason": "no git"})
    result = _invoke_init(monkeypatch, tmp_path, qoder_minimal_resource_path)
    assert result.exit_code == 0, result.output
    payload = json.loads(
        (tmp_path / "demo-proj" / STAMP_RELPATH).read_text(encoding="utf-8"))
    assert payload["commit"] == "unavailable"
    assert payload["reason"] == "no git"
