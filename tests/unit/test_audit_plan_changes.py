"""Unit tests for skills/external/sdd-loop-driver/scripts/audit-plan-changes.py.

Red-first: the script does not exist yet. The script mechanically reports the
touched plan-owned paths (committed range + uncommitted changes), the
PLAN-EDIT declaration lines and the final cumulative diff stats. It is
read-only and never classifies minor/substantive semantics itself.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-plan-changes.py"

PLAN_OWNED = ["plan.md", "data-model.md", "contracts", "quickstart.md",
              "research.md", "feature-ref.md"]


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture",
         "-c", "user.email=fixture@example.com", *args],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "checkout", "-b", "fixture")
    spec = repo / ".specify" / "specs" / "012-medium"
    spec.mkdir(parents=True)
    (spec / "plan.md").write_text("# Plan\n\nbase plan\n", encoding="utf-8")
    (spec / "data-model.md").write_text("# Data Model\n", encoding="utf-8")
    (spec / "contracts").mkdir()
    (spec / "contracts" / "c.md").write_text("# Contract\n", encoding="utf-8")
    (spec / "quickstart.md").write_text("# Quickstart\n", encoding="utf-8")
    (spec / "research.md").write_text("# Research\n", encoding="utf-8")
    (spec / "feature-ref.md").write_text("# Feature Ref\n", encoding="utf-8")
    (repo / "README.md").write_text("base\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "base")
    return repo, _git(repo, "rev-parse", "HEAD")


def _commit_change(repo, message="change"):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _declarations(tmp_path, lines):
    path = tmp_path / "declarations.txt"
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def _run(repo, base, head, declarations, plan_owned=None):
    cmd = [sys.executable, str(SCRIPT), "--repo", str(repo), "--base", base,
           "--head", head, "--declarations", str(declarations)]
    for path in (plan_owned or PLAN_OWNED):
        cmd += ["--plan-owned", path]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    payload = None
    if completed.stdout.strip():
        payload = json.loads(completed.stdout)
    return completed, payload


def test_undeclared_plan_change_flagged(tmp_path):
    repo, base = _make_repo(tmp_path)
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\n<!-- plan repair -->\n",
                    encoding="utf-8")
    head = _commit_change(repo, "plan repair")
    completed, payload = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 1, completed.stderr
    assert payload["touched_paths"] == [".specify/specs/012-medium/plan.md"]
    assert payload["undeclared"] is True


def test_uncommitted_plan_change_included(tmp_path):
    repo, base = _make_repo(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\n<!-- uncommitted -->\n",
                    encoding="utf-8")
    completed, payload = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 1, completed.stderr
    assert ".specify/specs/012-medium/plan.md" in payload["touched_paths"]


def test_declared_minor_change_passes(tmp_path):
    repo, base = _make_repo(tmp_path)
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\ntypo\n", encoding="utf-8")
    head = _commit_change(repo)
    declarations = _declarations(tmp_path, [
        "PLAN-EDIT: .specify/specs/012-medium/plan.md — typo fix；分类=minor",
    ])
    completed, payload = _run(repo, base, head, declarations)
    assert completed.returncode == 0, completed.stderr
    assert payload["undeclared"] is False
    assert len(payload["declaration_lines"]) == 1


def test_no_touch_reports_none(tmp_path):
    repo, base = _make_repo(tmp_path)
    (repo / "README.md").write_text("changed\n", encoding="utf-8")
    head = _commit_change(repo)
    completed, payload = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 0, completed.stderr
    assert payload["touched_paths"] == []
    assert payload["undeclared"] is False
    assert payload["classification"] == "none"


def test_diff_stats_and_output_shape(tmp_path):
    repo, base = _make_repo(tmp_path)
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "one\ntwo\n", encoding="utf-8")
    head = _commit_change(repo)
    completed, payload = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 1
    for field in ("base", "head", "touched_paths", "declaration_lines",
                  "undeclared", "diff_stats", "uncommitted_paths",
                  "classification"):
        assert field in payload, "missing output field: %s" % field
    stats = {item["path"]: item for item in payload["diff_stats"]}
    path = ".specify/specs/012-medium/plan.md"
    assert stats[path]["added"] == 2
    assert stats[path]["deleted"] == 0


def test_script_is_read_only(tmp_path):
    repo, base = _make_repo(tmp_path)
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "x\n", encoding="utf-8")
    head = _commit_change(repo)
    before_status = _git(repo, "status", "--porcelain")
    before_head = _git(repo, "rev-parse", "HEAD")
    completed, _ = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 1
    assert _git(repo, "status", "--porcelain") == before_status
    assert _git(repo, "rev-parse", "HEAD") == before_head


def test_accumulated_minor_edits_use_final_diff(tmp_path):
    repo, base = _make_repo(tmp_path)
    plan = repo / ".specify" / "specs" / "012-medium" / "plan.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "first\n", encoding="utf-8")
    _commit_change(repo, "edit 1")
    plan.write_text(plan.read_text(encoding="utf-8") + "second\n", encoding="utf-8")
    head = _commit_change(repo, "edit 2")
    completed, payload = _run(repo, base, head, _declarations(tmp_path, [
        "PLAN-EDIT: plan.md — two line-level fixes；分类=minor"]))
    assert completed.returncode == 0, completed.stderr
    stats = {item["path"]: item for item in payload["diff_stats"]}
    assert stats[".specify/specs/012-medium/plan.md"]["added"] == 2


def test_multi_commit_touch_set(tmp_path):
    repo, base = _make_repo(tmp_path)
    spec = repo / ".specify" / "specs" / "012-medium"
    (spec / "plan.md").write_text("first\n", encoding="utf-8")
    _commit_change(repo, "edit plan")
    (spec / "research.md").write_text("second\n", encoding="utf-8")
    head = _commit_change(repo, "edit research")
    completed, payload = _run(repo, base, head, _declarations(tmp_path, []))
    assert completed.returncode == 1
    assert ".specify/specs/012-medium/plan.md" in payload["touched_paths"]
    assert ".specify/specs/012-medium/research.md" in payload["touched_paths"]
