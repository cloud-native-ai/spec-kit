"""Unit tests for the renumber engine (sequence-number collision repair).

Pins the `/speckit.sanitize --lane renumber` contract: duplicate-only repair,
deterministic winner, next-free allocation that skips archived numbers, the
front-loaded confirmation lock, branch-name guard, dated-record exclusion,
in-scope verification, dismissal lifecycle, and concurrent plan paths.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import renumber_utils as engine  # noqa: E402

GIT_CONFIG = ("-c", "user.email=test@example.com", "-c", "user.name=Test")


def git(ws: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ws), *GIT_CONFIG, *args],
                          capture_output=True, text=True)


def commit_all(ws: Path, message: str = "fixture") -> None:
    git(ws, "add", "-A")
    git(ws, "commit", "-m", message)


def write(ws: Path, relpath: str, text: str) -> Path:
    path = ws / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


FEATURES_MD = """# Features

| ID | Feature Name | Brief | Status | Feature Details | Spec Path | Last Updated |
|----|--------------|-------|--------|-----------------|-----------|--------------|
| 001 | Alpha | first | Draft | .specify/memory/features/001.md | .specify/specs/001-alpha/requirements.md | 2026-01-01 |
"""

REGISTER_MD = """# ID Register (编号登记册)

维护方式:手工,无引擎。

| 编号 | 含义(一行) | 权威路径 | 状态 |
|------|------------|----------|------|
| REC-001-01 | first obligation | spec review | open |
| REC-001-01 | duplicated obligation | spec review again | open |
| REC-001-03 | follow-me obligation | spec review | open |
| D1–D9 | range code, not machine allocated | somewhere | closed |
"""


@pytest.fixture()
def ws(tmp_path: Path) -> Path:
    write(tmp_path, ".specify/specs/001-alpha/requirements.md",
          "# Alpha\n\n**Requirement Branch**: `001-alpha`\n")
    write(tmp_path, ".specify/specs/001-beta/requirements.md",
          "# Beta\n\n**Requirement Branch**: `001-beta`\n")
    write(tmp_path, ".specify/specs/001-beta/review.md",
          "# Review\n\nSee REC-001-03 for the open obligation.\n")
    write(tmp_path, ".specify/specs/.archive/002-old/spec.md", "# Old\n")
    write(tmp_path, ".specify/specs/001-alpha/tasks.md",
          "# Tasks\n\n- [ ] T001 first task\n- [ ] T001 duplicated task\n")
    write(tmp_path, ".specify/specs/001-alpha/checklist.md",
          "# Checklist\n\n- [ ] CHK001 first check\n- [ ] CHK001 duplicated check\n")
    write(tmp_path, ".specify/memory/features.md", FEATURES_MD)
    write(tmp_path, ".specify/memory/register.md", REGISTER_MD)
    write(tmp_path, "docs/guide.md", "Run the 001-beta workflow.\n")
    write(tmp_path, ".specify/memory/feedback/20260101T000000Z-note.md",
          "Dated record mentions 001-beta on purpose.\n")
    git(tmp_path, "init", "-q")
    commit_all(tmp_path)
    return tmp_path


def call(ws: Path, *argv: str):
    args = engine.build_parser().parse_args(["--workspace-root", str(ws), *argv])
    handler = {"scan": engine.action_scan, "plan": engine.action_plan,
               "apply": engine.action_apply, "status": engine.action_status,
               "dismiss": engine.action_dismiss,
               "args-manifest": engine.action_args_manifest}[args.action]
    return handler(args)


def plan_file(ws: Path, *argv: str) -> Path:
    out = ws / "plan.json"
    result = call(ws, "--action", "plan", "--plan-out", str(out), *argv)
    assert result["ok"]
    return Path(result["plan"])


def confirm(path: Path) -> None:
    node = json.loads(path.read_text(encoding="utf-8"))
    node["confirmed"] = True
    path.write_text(json.dumps(node, ensure_ascii=False), encoding="utf-8")


def groups_by_family(scan: dict) -> dict:
    out = {}
    for group in scan["groups"]:
        out.setdefault(group["family"], []).append(group)
    return out


def test_scan_keeps_registered_dir_and_allocates_after_archive(ws):
    scan = call(ws, "--action", "scan")
    spec = groups_by_family(scan)["spec-number"]
    assert len(spec) == 1
    assert spec[0]["keep"] == {"token": "001-alpha", "evidence": "features-row"}
    assert spec[0]["old_token"] == "001-beta"
    # archive/002-old occupies 002, so the next free number is 003.
    assert spec[0]["new_token"] == "003-beta"
    assert spec[0]["status"] == "proposed"


def test_scan_detects_duplicate_register_tokens_and_reports_ranges(ws):
    scan = call(ws, "--action", "scan")
    register = groups_by_family(scan).get("register", [])
    assert [group["old_token"] for group in register] == ["REC-001-01"]
    assert register[0]["new_token"] == "REC-001-04"
    assert register[0]["status"] == "proposed"
    targets = [note["target"] for note in scan["info"]
               if note["kind"] == "non-machine-register-code"]
    assert "D1–D9" in targets


def test_scan_detects_local_duplicates(ws):
    scan = call(ws, "--action", "scan")
    local = groups_by_family(scan).get("local", [])
    pairs = {(group["scope"], group["old_token"], group["new_token"]) for group in local}
    assert (".specify/specs/001-alpha/tasks.md", "T001", "T002") in pairs
    assert (".specify/specs/001-alpha/checklist.md", "CHK001", "CHK002") in pairs


def test_local_duplicate_with_inbound_reference_needs_decision(ws):
    write(ws, ".specify/specs/001-alpha/notes-status.md",
          "status: T001 shipped\n")
    commit_all(ws, "add inbound reference")
    scan = call(ws, "--action", "scan")
    local = [g for g in groups_by_family(scan).get("local", [])
             if g["old_token"] == "T001"]
    assert local and local[0]["status"] == "needs-decision"
    assert local[0]["ambiguous_refs"] >= 1


def test_rec_follow_only_when_token_is_owned_by_the_renamed_spec(ws):
    scan = call(ws, "--action", "scan")
    follow = groups_by_family(scan).get("rec-follow", [])
    assert [group["old_token"] for group in follow] == ["REC-001-03"]
    assert follow[0]["new_token"] == "REC-003-03"
    assert follow[0]["depends_on"]


def test_apply_refuses_unconfirmed_plan_with_zero_side_effects(ws):
    plan = plan_file(ws)
    code = engine.main(["--action", "apply", "--workspace-root", str(ws),
                        "--plan", str(plan)])
    assert code == 2
    assert (ws / ".specify/specs/001-beta").is_dir()
    assert (ws / ".specify/specs/003-beta").exists() is False
    assert not (ws / ".specify/memory/renumber/ledger").exists()


def test_apply_renames_rewrites_and_verifies(ws):
    plan = plan_file(ws)
    confirm(plan)
    result = call(ws, "--action", "apply", "--plan", str(plan))
    assert result["ok"], result
    assert (ws / ".specify/specs/003-beta").is_dir()
    assert not (ws / ".specify/specs/001-beta").exists()
    assert "003-beta" in (ws / "docs/guide.md").read_text(encoding="utf-8")
    features = (ws / ".specify/memory/features.md").read_text(encoding="utf-8")
    assert ".specify/specs/001-alpha/requirements.md" in features
    ledger = json.loads(Path(result["ledger"]).read_text(encoding="utf-8"))
    assert ledger["verification"]["unresolved"] == []
    assert ledger["verification"]["resolved"] == result["groups"]
    # Duplicate repair renumbers the later definition only — the kept one stays.
    register = (ws / ".specify/memory/register.md").read_text(encoding="utf-8")
    assert register.count("REC-001-01") == 1
    assert "REC-001-04" in register
    tasks = (ws / ".specify/specs/001-alpha/tasks.md").read_text(encoding="utf-8")
    assert "T001 first task" in tasks and "T002 duplicated task" in tasks
    # the date-named record is deliberately left alone
    dated = (ws / ".specify/memory/feedback/20260101T000000Z-note.md").read_text(encoding="utf-8")
    assert "001-beta" in dated


def test_apply_refuses_dirty_targets(ws):
    plan = plan_file(ws)
    confirm(plan)
    write(ws, "docs/guide.md", "dirty edit mentions 001-beta\n")
    code = engine.main(["--action", "apply", "--workspace-root", str(ws),
                        "--plan", str(plan)])
    assert code == 2
    assert (ws / ".specify/specs/001-beta").is_dir()


def test_apply_refuses_branch_name_conflict(ws):
    git(ws, "branch", "001-beta-keep")
    plan = plan_file(ws)
    confirm(plan)
    code = engine.main(["--action", "apply", "--workspace-root", str(ws),
                        "--plan", str(plan)])
    assert code == 2
    assert (ws / ".specify/specs/001-beta").is_dir()


def test_apply_refuses_non_git_workspace(tmp_path):
    write(tmp_path, ".specify/specs/001-alpha/requirements.md", "# A\n")
    write(tmp_path, ".specify/specs/001-beta/requirements.md", "# B\n")
    plan = plan_file(tmp_path)
    confirm(plan)
    code = engine.main(["--action", "apply", "--workspace-root", str(tmp_path),
                        "--plan", str(plan)])
    assert code == 2
    assert (tmp_path / ".specify/specs/001-beta").is_dir()


def test_apply_subset_refuses_when_dependency_not_selected(ws):
    plan = plan_file(ws)
    confirm(plan)
    node = json.loads(plan.read_text(encoding="utf-8"))
    follow = next(g for g in node["groups"] if g["family"] == "rec-follow")
    code = engine.main(["--action", "apply", "--workspace-root", str(ws),
                        "--plan", str(plan), "--groups", follow["group_id"]])
    assert code == 2
    assert (ws / ".specify/specs/001-beta").is_dir()


def test_apply_subset_leaves_unselected_groups_pending(ws):
    plan = plan_file(ws)
    confirm(plan)
    node = json.loads(plan.read_text(encoding="utf-8"))
    spec = next(g for g in node["groups"] if g["family"] == "spec-number")
    result = call(ws, "--action", "apply", "--plan", str(plan),
                  "--groups", spec["group_id"])
    assert result["ok"], result
    assert (ws / ".specify/specs/003-beta").is_dir()
    register = (ws / ".specify/memory/register.md").read_text(encoding="utf-8")
    assert register.count("REC-001-01") == 2, "the unselected register group is untouched"
    families = groups_by_family(call(ws, "--action", "scan"))
    assert "spec-number" not in families
    assert "register" in families and "local" in families


def test_second_scan_is_clean_after_apply(ws):
    plan = plan_file(ws)
    confirm(plan)
    assert call(ws, "--action", "apply", "--plan", str(plan))["ok"]
    scan = call(ws, "--action", "scan")
    assert groups_by_family(scan).get("spec-number") is None


def test_dismissal_suppresses_group_until_reopened(ws):
    scan = call(ws, "--action", "scan")
    group_id = groups_by_family(scan)["spec-number"][0]["group_id"]
    dismissed = call(ws, "--action", "dismiss", "--group", group_id,
                     "--reason", "adjudicated in notes/overlap.md")
    assert dismissed["ok"]
    scan = call(ws, "--action", "scan")
    assert groups_by_family(scan).get("spec-number") is None
    assert [group["group_id"] for group in scan["dismissed"]] == [group_id]
    reopened = call(ws, "--action", "dismiss", "--group", group_id, "--reopen")
    assert reopened["ok"]
    scan = call(ws, "--action", "scan")
    assert groups_by_family(scan)["spec-number"][0]["group_id"] == group_id


def test_concurrent_plans_write_distinct_paths(ws):
    first = call(ws, "--action", "plan")
    second = call(ws, "--action", "plan")
    assert first["plan"] != second["plan"]
    assert Path(first["plan"]).is_file() and Path(second["plan"]).is_file()


def test_rewrite_line_refuses_paths_outside_the_scope(ws):
    outside = ws.parent / "outside.md"
    outside.write_text("T001\n", encoding="utf-8")
    outcome = engine.rewrite_line(ws, "../outside.md", 1, "T001", "T002")
    assert outcome == {"ok": False, "problem": "path-outside-scope"}
    assert outside.read_text(encoding="utf-8") == "T001\n"
    assert engine._rename_dir(ws, "../outside.md", ".specify/specs/009-x") == "path-outside-scope"


def test_args_manifest_matches_parser():
    manifest = call(Path.cwd(), "--action", "args-manifest")
    assert set(manifest) == set(engine.ACTIONS)
    assert manifest["apply"]["required"] == ["--plan"]
