"""Contract tests for contracts/workspace-isolation.md (WI-01…WI-21)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    engine_json,
    engine_path,
    git,
    make_git_repo,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
    watcher_path,
)

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "external" / "sdd-loop-driver"


def _register_write(reg: Path, repo: Path, line: str, run: str, worktree: Path, branch: str, **extra) -> dict:
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    args = [
        "--line-id", line, "--run-id", run,
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--write-line",
        "--worktree-path", str(worktree), "--branch", branch, "--base-sha", base,
    ]
    for flag, value in extra.items():
        args += [f"--{flag.replace('_', '-')}", str(value)]
    return engine_json("register", *args, reg=reg)


def _manifest(path: Path, line: str, owned=(), read_only=(), forbidden=(), depends=()) -> Path:
    path.write_text(json.dumps({
        "schema_version": 1,
        "line_id": line,
        "owned_paths": list(owned),
        "read_only_paths": list(read_only),
        "forbidden_paths": list(forbidden),
        "integration_depends_on": list(depends),
    }), encoding="utf-8")
    return path


def _docs() -> str:
    parts = [
        (SKILL_DIR / "references" / "dispatch-recipes.md").read_text(encoding="utf-8"),
        (SKILL_DIR / "references" / "stage-prompts.md").read_text(encoding="utf-8"),
        (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"),
    ]
    return "\n".join(parts)


def test_wi_01_worktree_per_write_line(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("wt")
    worktree = tmp_path / ".spec-kit" / "worktrees" / "repo" / line
    entry = _register_write(reg, repo, line, make_run_id(), worktree, f"line/{line}")
    assert entry["worktree_path"] == str(worktree.resolve())
    assert entry["branch"] == f"line/{line}"
    assert entry["base_sha"] == git(repo, "rev-parse", "HEAD").stdout.strip()


def test_doc_wi_02_branch_discipline(tmp_path):
    prompts = (SKILL_DIR / "references" / "stage-prompts.md").read_text(encoding="utf-8")
    for forbidden in ["git checkout", "git switch", "git worktree"]:
        assert forbidden not in prompts, f"stage prompt must not carry {forbidden!r}"
    assert "MUST NOT 切换分支" in prompts or "不得切换分支" in prompts
    recipes = (SKILL_DIR / "references" / "dispatch-recipes.md").read_text(encoding="utf-8")
    assert "git worktree add -b line/<line>" in recipes


def test_wi_03_target_occupied(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line1 = make_line_id("occ1")
    worktree = tmp_path / "wt-shared"
    _register_write(reg, repo, line1, make_run_id(), worktree, f"line/{line1}")
    proc = run_engine(
        "register", "--line-id", make_line_id("occ2"), "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo), "--state", "active",
        "--write-line", "--worktree-path", str(worktree), "--branch", "line/other",
        "--base-sha", git(repo, "rev-parse", "HEAD").stdout.strip(), reg=reg,
    )
    assert proc.returncode == 2
    assert "worktree" in proc.stdout.lower() or "worktree" in proc.stderr.lower()


def test_wi_04_manifest_projection(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("man")
    worktree = tmp_path / "wt"
    _register_write(reg, repo, line, make_run_id(), worktree, f"line/{line}")
    manifest = _manifest(tmp_path / "m.json", line, owned=["src/a"])
    result = engine_json("ownership-check", "--line-id", line, "--manifest", str(manifest), reg=reg)
    assert result["decision"] == "proceed"
    stored = json.loads((reg / f"{line}.json").read_text())
    assert stored["owned_paths"] == [str((repo / "src/a").resolve())]
    assert stored["ownership_manifest_path"] == str(manifest.resolve())
    assert (reg / "manifests" / f"{line}.json").exists()


def test_wi_05_normalization_overlap(tmp_path):
    repo = make_git_repo(tmp_path)
    target = repo / "src" / "module.py"
    target.parent.mkdir(parents=True)
    target.write_text("x", encoding="utf-8")
    symlink = tmp_path / "link-to-src"
    symlink.symlink_to(repo / "src", target_is_directory=True)
    reg = tmp_path / "reg"
    first = make_line_id("norm1")
    second = make_line_id("norm2")
    _register_write(reg, repo, first, make_run_id(), tmp_path / "wt1", f"line/{first}")
    _register_write(reg, repo, second, make_run_id(), tmp_path / "wt2", f"line/{second}")
    m1 = _manifest(tmp_path / "m1.json", first, owned=["src/module.py"])
    engine_json("ownership-check", "--line-id", first, "--manifest", str(m1), reg=reg)
    m2 = _manifest(tmp_path / "m2.json", second, owned=[str(symlink / "module.py")])
    result = engine_json("ownership-check", "--line-id", second, "--manifest", str(m2), reg=reg)
    assert result["decision"] == "waiting"
    assert result["holder_line_id"] == first
    stored = json.loads((reg / f"{second}.json").read_text())
    assert stored["state"] == "waiting"
    assert stored["waiting_reason"] == "ownership-overlap"
    assert stored["holder_line_id"] == first


def test_wi_06_fifo_serialization(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    first = make_line_id("fifo1")
    second = make_line_id("fifo2")
    _register_write(reg, repo, first, make_run_id(), tmp_path / "w1", f"line/{first}")
    _register_write(reg, repo, second, make_run_id(), tmp_path / "w2", f"line/{second}")
    m1 = _manifest(tmp_path / "m1.json", first, owned=["shared/"])
    engine_json("ownership-check", "--line-id", first, "--manifest", str(m1), reg=reg)
    m2 = _manifest(tmp_path / "m2.json", second, owned=["shared/file"])
    second_result = engine_json("ownership-check", "--line-id", second, "--manifest", str(m2), reg=reg)
    assert second_result["holder_line_id"] == first
    # Releasing the first line's ownership allows an explicit promotion.
    engine_json(
        "release-ownership", "--line-id", first, "--reason", "abandoned",
        "--evidence-ref", "notes/evidence.md", reg=reg,
    )
    promoted = engine_json("promote-waiting", "--line-id", second, reg=reg)
    assert promoted["state"] == "active"


def test_wi_07_dead_holder_no_release(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    holder = make_line_id("hold")
    waiter = make_line_id("wait")
    _register_write(reg, repo, holder, make_run_id(), tmp_path / "h", f"line/{holder}")
    _register_write(reg, repo, waiter, make_run_id(), tmp_path / "w", f"line/{waiter}")
    mh = _manifest(tmp_path / "mh.json", holder, owned=["src/"])
    engine_json("ownership-check", "--line-id", holder, "--manifest", str(mh), reg=reg)
    mw = _manifest(tmp_path / "mw.json", waiter, owned=["src/file"])
    engine_json("ownership-check", "--line-id", waiter, "--manifest", str(mw), reg=reg)
    engine_json(
        "update", "--line-id", holder, "--runner-pid", "999999",
        "--runner-start-token", "0", "--last-event", "dead", reg=reg,
    )
    refused = run_engine("promote-waiting", "--line-id", waiter, reg=reg)
    assert refused.returncode == 3
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"


def _prepare_overlap(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    holder = make_line_id("hold")
    waiter = make_line_id("wait")
    _register_write(reg, repo, holder, make_run_id(), tmp_path / "h", f"line/{holder}")
    _register_write(reg, repo, waiter, make_run_id(), tmp_path / "w", f"line/{waiter}")
    mh = _manifest(tmp_path / "mh.json", holder, owned=["src/"])
    mw = _manifest(tmp_path / "mw.json", waiter, owned=["src/file"])
    engine_json("ownership-check", "--line-id", holder, "--manifest", str(mh), reg=reg)
    result = engine_json("ownership-check", "--line-id", waiter, "--manifest", str(mw), reg=reg)
    assert result["state"] == "waiting" and result["holder_line_id"] == holder
    return repo, reg, holder, waiter, mw


def _states(reg: Path) -> list[str]:
    return [json.loads(path.read_text())["state"] for path in reg.glob("*.json")]


def test_p0_stale_cleanup_is_not_an_ownership_release(tmp_path):
    """Regression for review P0-01: a stale-cleaned holder must keep blocking."""
    _repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    stale = engine_json("deregister", "--line-id", holder, "--reason", "stale-cleanup", reg=reg)
    assert stale["state"] == "stale"
    assert stale["stale_from_state"] == "active"
    assert "closed_at" not in stale
    manifest = json.loads((reg / "manifests" / f"{holder}.json").read_text())
    assert "released_at" not in manifest

    refused = run_engine("promote-waiting", "--line-id", waiter, reg=reg)
    assert refused.returncode == 3, refused.stdout
    payload = json.loads(refused.stdout)
    assert payload["reason"] == "ownership-overlap"
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"
    assert _states(reg).count("active") == 0, "stale-cleanup must never produce a second active line"


def test_p0_explicit_release_unblocks_waiter(tmp_path):
    _repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    engine_json("deregister", "--line-id", holder, "--reason", "stale-cleanup", reg=reg)
    released = engine_json(
        "release-ownership", "--line-id", holder, "--reason", "evidence-expired",
        "--evidence-ref", "notes/evidence.md", reg=reg,
    )
    assert released["state"] == "closed"
    promoted = engine_json("promote-waiting", "--line-id", waiter, reg=reg)
    assert promoted["state"] == "active"
    states = _states(reg)
    assert states.count("active") == 1 and states.count("closed") == 1


def test_p0_merged_u6_close_unblocks_waiter(tmp_path):
    repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    worktree = tmp_path / "h"
    git(repo, "worktree", "add", "-q", "-b", f"line/{holder}", str(worktree), "main")
    (worktree / "src").mkdir()
    (worktree / "src" / "holder.txt").write_text("holder\n", encoding="utf-8")
    git(worktree, "add", "src/holder.txt")
    git(worktree, "commit", "-q", "-m", "holder work")
    line_head = git(worktree, "rev-parse", "HEAD").stdout.strip()
    git(repo, "merge", "--ff-only", line_head)
    commit = git(repo, "rev-parse", "HEAD").stdout.strip()
    engine_json("update", "--line-id", holder, "--state", "completed", reg=reg)
    engine_json(
        "integration-record", "--line-id", holder, "--result", "merged",
        "--commit", commit, reg=reg,
    )
    engine_json("deregister", "--line-id", holder, "--reason", "merged", reg=reg)
    promoted = engine_json("promote-waiting", "--line-id", waiter, reg=reg)
    assert promoted["state"] == "active"
    assert _states(reg).count("active") == 1


def test_p0_update_state_active_cannot_bypass_the_gate(tmp_path):
    _repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    engine_json("deregister", "--line-id", holder, "--reason", "stale-cleanup", reg=reg)
    bypass = run_engine("update", "--line-id", waiter, "--state", "active", reg=reg)
    assert bypass.returncode == 3, bypass.stdout
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"
    assert _states(reg).count("active") == 0


def test_p0_reacquired_ownership_blocks_again(tmp_path):
    repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    engine_json(
        "release-ownership", "--line-id", holder, "--reason", "handoff",
        "--evidence-ref", "notes/handoff.md", reg=reg,
    )
    reacquired = engine_json(
        "ownership-check", "--line-id", holder,
        "--manifest", str(tmp_path / "mh.json"), reg=reg,
    )
    # The waiter already queued an earlier current claim, so the re-acquired
    # holder goes behind it; the old release history must not be treated as a
    # permanent unlock.
    assert reacquired["decision"] == "waiting"
    assert reacquired["holder_line_id"] == waiter
    manifest = json.loads((reg / "manifests" / f"{holder}.json").read_text())
    assert "released_at" not in manifest
    assert manifest["claimed_at"] and manifest["claimed_ns"]

    third = make_line_id("thrd")
    proc = run_engine(
        "register", "--line-id", third, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest",
        str(_manifest(tmp_path / "m3.json", third, owned=["src/other"])), reg=reg,
    )
    assert proc.returncode == 3, proc.stdout
    blocked = run_engine("update", "--line-id", holder, "--state", "active", reg=reg)
    assert blocked.returncode == 3, blocked.stdout
    promoted = engine_json("promote-waiting", "--line-id", waiter, reg=reg)
    assert promoted["state"] == "active"
    assert _states(reg).count("active") == 1


def test_p0_forged_merge_evidence_is_rejected(tmp_path):
    repo, reg, holder, _waiter, _mw = _prepare_overlap(tmp_path)
    forged_update = run_engine(
        "update", "--line-id", holder, "--integration-result",
        '{"status":"merged","commit":"deadbeef"}', reg=reg,
    )
    assert forged_update.returncode == 2
    stored = json.loads((reg / f"{holder}.json").read_text())
    assert "integration_result" not in stored
    engine_json("update", "--line-id", holder, "--state", "completed", reg=reg)
    forged_record = run_engine(
        "integration-record", "--line-id", holder, "--result", "merged",
        "--commit", "deadbeef", reg=reg,
    )
    assert forged_record.returncode == 2, forged_record.stdout
    assert "integration_result" not in json.loads((reg / f"{holder}.json").read_text())
    assert subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", "deadbeef"],
        capture_output=True,
    ).returncode != 0


def test_p0_released_line_cannot_reactivate_without_reacquire(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    holder = make_line_id("relone")
    manifest = _manifest(tmp_path / "mh.json", holder, owned=["src/"])
    engine_json(
        "register", "--line-id", holder, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest", str(manifest), reg=reg,
    )
    released = engine_json(
        "release-ownership", "--line-id", holder, "--reason", "handoff",
        "--evidence-ref", "notes/handoff.md", reg=reg,
    )
    assert released["state"] == "stalled"
    blocked = run_engine("update", "--line-id", holder, "--state", "active", reg=reg)
    assert blocked.returncode == 3, blocked.stdout
    assert "released" in blocked.stdout
    assert json.loads((reg / f"{holder}.json").read_text())["state"] == "stalled"
    reacquired = engine_json(
        "ownership-check", "--line-id", holder, "--manifest", str(manifest), reg=reg
    )
    assert reacquired["decision"] == "proceed"
    assert "released_at" not in json.loads(
        (reg / "manifests" / f"{holder}.json").read_text()
    )
    reactivated = engine_json("update", "--line-id", holder, "--state", "active", reg=reg)
    assert reactivated["state"] == "active"


def test_p0_non_git_forged_merge_with_ownership_rejected(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("nongit")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project),
        "--state", "active", "--owned-paths", '["src/"]', reg=reg,
    )
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    forged = run_engine(
        "integration-record", "--line-id", line, "--result", "merged",
        "--commit", "deadbeef", reg=reg,
    )
    assert forged.returncode == 2, forged.stdout
    stored = json.loads((reg / f"{line}.json").read_text())
    assert "integration_result" not in stored


def test_p0_register_active_with_overlap_is_rejected(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    holder = make_line_id("regh")
    waiter = make_line_id("regw")
    _register_write(reg, repo, holder, make_run_id(), tmp_path / "h", f"line/{holder}")
    engine_json(
        "ownership-check", "--line-id", holder, "--manifest",
        str(_manifest(tmp_path / "mh.json", holder, owned=["src/"])), reg=reg,
    )
    mw = _manifest(tmp_path / "mw.json", waiter, owned=["src/file"])
    proc = run_engine(
        "register", "--line-id", waiter, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest", str(mw), reg=reg,
    )
    assert proc.returncode == 3, proc.stdout
    assert not (reg / f"{waiter}.json").exists()


def test_p0_close_without_evidence_still_blocks(tmp_path):
    _repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    engine_json("deregister", "--line-id", holder, "--reason", "abandoned", reg=reg)
    refused = run_engine("promote-waiting", "--line-id", waiter, reg=reg)
    assert refused.returncode == 3
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"


def test_p0_ownership_check_never_auto_promotes(tmp_path):
    _repo, reg, holder, waiter, mw = _prepare_overlap(tmp_path)
    engine_json(
        "release-ownership", "--line-id", holder, "--reason", "abandoned",
        "--evidence-ref", "notes/evidence.md", reg=reg,
    )
    result = engine_json("ownership-check", "--line-id", waiter, "--manifest", str(mw), reg=reg)
    assert result["decision"] == "proceed"
    assert result["state"] == "waiting"
    assert result.get("promotion_required") is True
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"
    promoted = engine_json("promote-waiting", "--line-id", waiter, reg=reg)
    assert promoted["state"] == "active"


def test_p0_released_waiting_line_cannot_promote(tmp_path):
    _repo, reg, _holder, waiter, _mw = _prepare_overlap(tmp_path)
    released = engine_json(
        "release-ownership", "--line-id", waiter, "--reason", "give-up",
        "--evidence-ref", "notes/give-up.md", reg=reg,
    )
    assert released["state"] == "stalled"
    assert json.loads((reg / "manifests" / f"{waiter}.json").read_text()).get("released_at")
    promote = run_engine("promote-waiting", "--line-id", waiter, reg=reg)
    assert promote.returncode == 2, promote.stdout
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "stalled"


def test_p0_active_release_demotes_holder(tmp_path):
    _repo, reg, holder, waiter, _mw = _prepare_overlap(tmp_path)
    released = engine_json(
        "release-ownership", "--line-id", holder, "--reason", "handoff",
        "--evidence-ref", "notes/handoff.md", reg=reg,
    )
    assert released["state"] == "stalled"
    promoted = engine_json("promote-waiting", "--line-id", waiter, reg=reg)
    assert promoted["state"] == "active"
    assert _states(reg).count("active") == 1, "the released holder must not stay active"


def test_p0_closed_is_terminal(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("term")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    engine_json("deregister", "--line-id", line, "--reason", "done", reg=reg)
    revived = run_engine("update", "--line-id", line, "--state", "active", reg=reg)
    assert revived.returncode == 2, revived.stdout
    assert json.loads((reg / f"{line}.json").read_text())["state"] == "closed"


def test_p0_register_reclaims_a_released_manifest(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    holder = make_line_id("relh")
    manifest = _manifest(tmp_path / "mh.json", holder, owned=["src/"])
    data = json.loads(manifest.read_text())
    data.update({"released_at": "2026-10-20T00:00:00Z", "evidence_ref": "stale.md"})
    manifest.write_text(json.dumps(data), encoding="utf-8")
    registered = engine_json(
        "register", "--line-id", holder, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest", str(manifest), reg=reg,
    )
    assert registered["state"] == "active"
    stored = json.loads((reg / "manifests" / f"{holder}.json").read_text())
    assert "released_at" not in stored
    assert stored["claimed_ns"] > 0
    second = make_line_id("rels")
    proc = run_engine(
        "register", "--line-id", second, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest",
        str(_manifest(tmp_path / "m2.json", second, owned=["src/file"])), reg=reg,
    )
    assert proc.returncode == 3, proc.stdout


def test_p0_merged_requires_worktree_containment(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("nocont")
    _register_write(reg, repo, line, make_run_id(), tmp_path / "missing-wt", f"line/{line}")
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    commit = git(repo, "rev-parse", "HEAD").stdout.strip()
    proc = run_engine(
        "integration-record", "--line-id", line, "--result", "merged",
        "--commit", commit, reg=reg,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "worktree" in (proc.stdout + proc.stderr)
    assert "integration_result" not in json.loads((reg / f"{line}.json").read_text())


def test_p0_concurrent_overlapping_registration_single_winner(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    first = make_line_id("racea")
    second = make_line_id("raceb")
    m1 = _manifest(tmp_path / "r1.json", first, owned=["src/"])
    m2 = _manifest(tmp_path / "r2.json", second, owned=["src/file"])
    env = dict(os.environ, SPECIFY_LINE_REGISTRY_DIR=str(reg))
    procs = []
    for line, manifest in ((first, m1), (second, m2)):
        procs.append(subprocess.Popen(
            [sys.executable, str(engine_path()), "--action", "register",
             "--line-id", line, "--run-id", make_run_id(),
             "--project-dir", str(repo), "--repo-root", str(repo),
             "--state", "active", "--manifest", str(manifest)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
        ))
    results = []
    for proc in procs:
        out, err = proc.communicate(timeout=30)
        results.append((proc.returncode, out, err))
    winners = [row for row in results if row[0] == 0]
    refused = [row for row in results if row[0] == 3]
    assert len(winners) == 1, results
    assert len(refused) == 1, results
    rows = engine_json("list", "--all", reg=reg)
    assert len(rows) == 1
    assert rows[0]["state"] == "active"


def test_p0_closed_not_revived_by_allocate(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("alloc")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    engine_json("deregister", "--line-id", line, "--reason", "done", reg=reg)
    proc = run_engine("allocate-resources", "--line-id", line, reg=reg)
    assert proc.returncode == 2, proc.stdout
    assert json.loads((reg / f"{line}.json").read_text())["state"] == "closed"


def test_p0_update_cannot_revive_stale_or_completed(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    stale = make_line_id("revs")
    engine_json(
        "register", "--line-id", stale, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    engine_json("deregister", "--line-id", stale, "--reason", "stale-cleanup", reg=reg)
    revived_stale = run_engine("update", "--line-id", stale, "--state", "active", reg=reg)
    assert revived_stale.returncode == 2, revived_stale.stdout
    assert json.loads((reg / f"{stale}.json").read_text())["state"] == "stale"

    done = make_line_id("revc")
    engine_json(
        "register", "--line-id", done, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    engine_json("update", "--line-id", done, "--state", "completed", reg=reg)
    revived_done = run_engine("update", "--line-id", done, "--state", "active", reg=reg)
    assert revived_done.returncode == 2, revived_done.stdout
    assert json.loads((reg / f"{done}.json").read_text())["state"] == "completed"


def test_p0_owned_paths_are_normalized_at_register_and_update(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    first = make_line_id("own1")
    second = make_line_id("own2")
    engine_json(
        "register", "--line-id", first, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--owned-paths", '["src/"]', reg=reg,
    )
    stored = json.loads((reg / f"{first}.json").read_text())
    assert stored["owned_paths"] == [str((repo / "src").resolve())]
    proc = run_engine(
        "register", "--line-id", second, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--owned-paths",
        json.dumps([str(repo / "src" / "file")]), reg=reg,
    )
    assert proc.returncode == 3, proc.stdout

    third = make_line_id("own3")
    engine_json(
        "register", "--line-id", third, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", reg=reg,
    )
    gated = run_engine(
        "update", "--line-id", third, "--owned-paths", '["src/file"]', reg=reg
    )
    assert gated.returncode == 3, gated.stdout
    assert "owned_paths" not in json.loads((reg / f"{third}.json").read_text())


def test_p0_worktree_must_be_outside_repo_roots(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("badwt")
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    proc = run_engine(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--write-line",
        "--worktree-path", str(repo), "--branch", f"line/{line}",
        "--base-sha", base, reg=reg,
    )
    assert proc.returncode == 2, proc.stdout
    assert not (reg / f"{line}.json").exists()
    registered = _register_write(reg, repo, line, make_run_id(), tmp_path / "wt-ok", f"line/{line}")
    assert registered["worktree_path"].endswith("wt-ok")
    moved = run_engine(
        "update", "--line-id", line, "--worktree-path", str(repo), reg=reg
    )
    assert moved.returncode == 2, moved.stdout


def test_p0_promote_refuses_a_released_waiting_manifest(tmp_path):
    _repo, reg, _holder, waiter, _mw = _prepare_overlap(tmp_path)
    manifest_file = reg / "manifests" / f"{waiter}.json"
    manifest = json.loads(manifest_file.read_text())
    manifest["released_at"] = "2026-10-20T00:00:00Z"
    manifest["evidence_ref"] = "legacy-release.md"
    manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
    proc = run_engine("promote-waiting", "--line-id", waiter, reg=reg)
    assert proc.returncode == 3, proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["reason"] == "ownership-released"
    assert json.loads((reg / f"{waiter}.json").read_text())["state"] == "waiting"


def test_p0_merged_requires_real_head_containment(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("contain")
    worktree = tmp_path / "wt-containing"
    _register_write(reg, repo, line, make_run_id(), worktree, f"line/{line}")
    git(repo, "worktree", "add", "-q", "-b", f"line/{line}", str(worktree), "main")

    def commit(relative: str, content: str, message: str) -> None:
        path = worktree / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        git(worktree, "add", relative)
        git(worktree, "commit", "-q", "-m", message)

    commit("src/one.txt", "one\n", "one")
    first = git(worktree, "rev-parse", "HEAD").stdout.strip()
    git(repo, "merge", "--ff-only", first)
    merged = git(repo, "rev-parse", "HEAD").stdout.strip()
    commit("src/two.txt", "two\n", "two")
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    proc = run_engine(
        "integration-record", "--line-id", line, "--result", "merged",
        "--commit", merged, reg=reg,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "contain" in (proc.stdout + proc.stderr).lower()


def test_p0_earlier_active_cannot_add_overlapping_paths(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    first = make_line_id("addp1")
    second = make_line_id("addp2")
    engine_json(
        "register", "--line-id", first, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo), reg=reg,
    )
    engine_json(
        "register", "--line-id", second, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--owned-paths", '["src/"]', reg=reg,
    )
    blocked = run_engine(
        "update", "--line-id", first, "--owned-paths", '["src/x"]', reg=reg
    )
    assert blocked.returncode == 3, blocked.stdout
    assert "owned_paths" not in json.loads((reg / f"{first}.json").read_text())


def test_p0_owned_paths_cannot_be_emptied_or_shadow_a_manifest(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("empty1")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--owned-paths", '["src/"]', reg=reg,
    )
    emptied = run_engine(
        "update", "--line-id", line, "--owned-paths", "[]", reg=reg
    )
    assert emptied.returncode == 2, emptied.stdout
    assert json.loads((reg / f"{line}.json").read_text())["owned_paths"]

    manifested = make_line_id("shadow")
    manifest = _manifest(tmp_path / "ms.json", manifested, owned=["docs/"])
    engine_json(
        "register", "--line-id", manifested, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--manifest", str(manifest), reg=reg,
    )
    shadow = run_engine(
        "update", "--line-id", manifested, "--owned-paths", '["src/"]', reg=reg
    )
    assert shadow.returncode == 2, shadow.stdout
    assert "manifest" in shadow.stderr.lower() or "manifest" in shadow.stdout.lower()


def test_p0_manifestless_release_blocks_reactivation(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("relnp")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--owned-paths", '["src/"]', reg=reg,
    )
    released = engine_json(
        "release-ownership", "--line-id", line, "--reason", "handoff",
        "--evidence-ref", "notes/handoff.md", reg=reg,
    )
    assert released["state"] == "stalled"
    blocked = run_engine("update", "--line-id", line, "--state", "active", reg=reg)
    assert blocked.returncode == 3, blocked.stdout
    assert "released" in blocked.stdout
    manifest = _manifest(tmp_path / "mnp.json", line, owned=["src/"])
    engine_json("ownership-check", "--line-id", line, "--manifest", str(manifest), reg=reg)
    reactivated = engine_json("update", "--line-id", line, "--state", "active", reg=reg)
    assert reactivated["state"] == "active"


def test_p0_worktree_path_is_immutable(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("immut")
    _register_write(reg, repo, line, make_run_id(), tmp_path / "wt-imm", f"line/{line}")
    moved = run_engine(
        "update", "--line-id", line,
        "--worktree-path", str(tmp_path / "wt-other"), reg=reg,
    )
    assert moved.returncode == 2, moved.stdout
    assert "immutable" in moved.stderr.lower() or "immutable" in moved.stdout.lower()


def test_p0_lease_and_reserve_refuse_closed_lines(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("lnclosed")
    engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    engine_json("deregister", "--line-id", line, "--reason", "done", reg=reg)
    lease = run_engine(
        "lease-acquire", "--line-id", line, "--session", "s1",
        "--pid", str(os.getpid()), reg=reg,
    )
    assert lease.returncode == 2, lease.stdout
    reserve = run_engine(
        "reserve", "--line-id", line, "--stage", "plan",
        "--run-id", make_run_id(), "--pid", str(os.getpid()),
        "--start-token", "x", reg=reg,
    )
    assert reserve.returncode == 2, reserve.stdout


def test_wi_08_readonly_forbidden_paths(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    first = make_line_id("ro1")
    second = make_line_id("ro2")
    _register_write(reg, repo, first, make_run_id(), tmp_path / "r1", f"line/{first}")
    _register_write(reg, repo, second, make_run_id(), tmp_path / "r2", f"line/{second}")
    m1 = _manifest(tmp_path / "m1.json", first, owned=["src/"], read_only=["docs/"])
    engine_json("ownership-check", "--line-id", first, "--manifest", str(m1), reg=reg)
    m2 = _manifest(tmp_path / "m2.json", second, owned=["docs/guide.md"])
    result = engine_json("ownership-check", "--line-id", second, "--manifest", str(m2), reg=reg)
    assert result["decision"] == "waiting"


def test_wi_09_runtime_path_set_and_exclusions(tmp_path):
    worktree = tmp_path / "wt"
    for rel in [
        ".specify/memory/feedback/f1.md",
        ".specify/memory/session/s1.md",
        ".specify/memory/knowledge/k1.md",
        ".specify/memory/exec-quant/e1.jsonl",
        ".specify/memory/evidence/ev.md",
        ".specify/history/h.md",
        ".specify/memory/trigger/t.md",
    ]:
        path = worktree / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rel, encoding="utf-8")
    dest = tmp_path / "archive"
    result = engine_json(
        "archive-runtime", "--line-id", make_line_id("arch"), "--worktree", str(worktree),
        "--dest", str(dest), reg=tmp_path / "reg",
    )
    archived = {Path(item["original"]).as_posix() for item in result["files"]}
    assert len(archived) == 4
    assert not any("evidence" in item or "history" in item or "trigger" in item for item in archived)
    recipes = (SKILL_DIR / "references" / "dispatch-recipes.md").read_text(encoding="utf-8")
    assert "运行时记录" in recipes and "不提交" in recipes


def test_wi_10_archive_conflict_preserved(tmp_path):
    worktree = tmp_path / "wt"
    src = worktree / ".specify" / "memory" / "feedback"
    src.mkdir(parents=True)
    (src / "same.md").write_text("line-local", encoding="utf-8")
    dest = tmp_path / "archive"
    dest.mkdir()
    (dest / "same.md").write_text("existing", encoding="utf-8")
    line = make_line_id("conf")
    result = engine_json(
        "archive-runtime", "--line-id", line, "--worktree", str(worktree), "--dest", str(dest),
        reg=tmp_path / "reg",
    )
    item = result["files"][0]
    assert item["conflict"] is True
    assert item["archived_name"] == f"same.md.{line}.1"
    assert (dest / "same.md").read_text() == "existing"
    assert (dest / item["archived_name"]).read_text() == "line-local"


def test_doc_wi_11_mirrors_once():
    text = _docs()
    assert "sync-mirrors.py" in text
    assert "整批" in text or "每批" in text
    assert "MUST NOT 每 line" in text or "不得每 line" in text or "不在逐线序列" in text


def test_doc_wi_12_single_coordinator():
    text = _docs()
    assert "单一" in text and ("协调者" in text or "集成者" in text)


def test_wi_13_deterministic_queue(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    lines = [make_line_id(f"q{i}") for i in range(3)]
    for index, line in enumerate(lines):
        _register_write(reg, repo, line, make_run_id(), tmp_path / f"q{index}", f"line/{line}")
        engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
        engine_json("integration-enqueue", "--line-id", line, "--at", f"2026-10-20T12:00:0{index}Z", reg=reg)
    first = engine_json("integration-plan", reg=reg)
    second = engine_json("integration-plan", reg=reg)
    assert first == second
    assert [entry["line_id"] for entry in first if entry.get("order")] == lines


def test_wi_14_per_line_steps_and_failure_retention(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("fail")
    worktree = tmp_path / "wt-fail"
    _register_write(reg, repo, line, make_run_id(), worktree, f"line/{line}")
    git(repo, "worktree", "add", "-q", "-b", f"line/{line}", str(worktree), "main")
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", line, reg=reg)
    result = engine_json(
        "integration-record", "--line-id", line, "--result", "failed", "--reason", "gate-failed", reg=reg
    )
    assert result["state"] == "completed"
    assert result["merge_ready"] is False
    assert result["integration_result"]["status"] == "failed"
    assert worktree.exists(), "failed integration must retain the worktree"
    text = _docs()
    for step in ["rebase", "质量门", "合并", "archive-runtime", "worktree remove"]:
        assert step in text


def test_wi_15_no_force_push():
    for path in [
        SKILL_DIR / "scripts" / "line-registry.py",
        SKILL_DIR / "scripts" / "watch-target.sh",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "git push" not in text
    text = _docs()
    assert "MUST NOT force push" in text or "不得 force push" in text


def test_doc_wi_16_cleanup_without_force():
    text = _docs()
    assert "git worktree remove" in text
    assert "--force" in text  # mentioned as prohibited
    assert "无 `--force`" in text or "不带 --force" in text or "无 --force" in text


def test_doc_wi_17_crash_reentry():
    text = _docs()
    assert "stale lock" in text
    assert "--once" in text
    assert "worktree" in text and "Registry" in text


def test_wi_18_19_20_resources(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line1 = make_line_id("res1")
    line2 = make_line_id("res2")
    line3 = make_line_id("res3")
    for line in (line1, line2, line3):
        _register_write(reg, repo, line, make_run_id(), tmp_path / f"wt-{line}", f"line/{line}")
        engine_json("update", "--line-id", line, "--stage", "plan",
                    "--runner-pid", str(os.getpid()), "--runner-start-token", "1",
                    "--cli-pid", str(os.getpid()), "--cli-start-token", "1",
                    "--status-path", str(tmp_path / f"status-{line}"),
                    "--log-path", str(tmp_path / f"log-{line}"),
                    "--heartbeat-path", str(tmp_path / f"heartbeat-{line}"),
                    "--prompt-path", str(tmp_path / f"prompt-{line}"), reg=reg)
    r1 = engine_json("allocate-resources", "--line-id", line1, reg=reg)
    r2 = engine_json("allocate-resources", "--line-id", line2, reg=reg)
    assert r1["resources"]["ports"] == [39000, 39019]
    assert r2["resources"]["ports"] == [39020, 39039]
    assert r1["resources"]["cache_dir"] != r2["resources"]["cache_dir"]
    assert r1["resources"]["tmp_dir"] != r2["resources"]["tmp_dir"]
    assert r1["resources"]["active_count"] == 3 and r1["resources"]["cap"] == 4
    capped = run_engine("allocate-resources", "--line-id", line3, "--cap", "2", reg=reg)
    assert capped.returncode == 3
    stored = json.loads((reg / f"{line3}.json").read_text())
    assert stored["state"] == "waiting"
    assert stored["waiting_reason"] == "concurrency-cap"


