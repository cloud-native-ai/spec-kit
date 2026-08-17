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
