"""Integration S3: two write lines, worktrees, ownership and the integration queue."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from fixtures.line_fixtures import (
    engine_json,
    git,
    make_git_repo,
    make_line_id,
    make_run_id,
    run_engine,
)


def _register(reg: Path, repo: Path, line: str, worktree: Path) -> dict:
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    return engine_json(
        "register", "--line-id", line, "--run-id", make_run_id(),
        "--project-dir", str(repo), "--repo-root", str(repo),
        "--state", "active", "--write-line",
        "--worktree-path", str(worktree), "--branch", f"line/{line}",
        "--base-sha", base, reg=reg,
    )


def _manifest(path: Path, line: str, owned, read_only=()) -> Path:
    path.write_text(json.dumps({
        "schema_version": 1,
        "line_id": line,
        "owned_paths": list(owned),
        "read_only_paths": list(read_only),
        "forbidden_paths": [],
    }), encoding="utf-8")
    return path


def _add_worktree(repo: Path, worktree: Path, line: str) -> None:
    git(repo, "worktree", "add", "-q", "-b", f"line/{line}", str(worktree), "main")


def _commit(worktree: Path, relative: str, content: str, message: str) -> str:
    path = worktree / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    git(worktree, "add", relative)
    git(worktree, "commit", "-q", "-m", message)
    return git(worktree, "rev-parse", "HEAD").stdout.strip()


def test_overlapping_write_lines_are_serialized(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    l1, l2 = make_line_id("ov1"), make_line_id("ov2")
    wt1, wt2 = tmp_path / "wt1", tmp_path / "wt2"
    _register(reg, repo, l1, wt1)
    _register(reg, repo, l2, wt2)
    _add_worktree(repo, wt1, l1)
    _add_worktree(repo, wt2, l2)
    engine_json("ownership-check", "--line-id", l1, "--manifest",
                str(_manifest(tmp_path / "m1.json", l1, ["src/"])), reg=reg)
    result = engine_json("ownership-check", "--line-id", l2, "--manifest",
                         str(_manifest(tmp_path / "m2.json", l2, ["src/main.py"])), reg=reg)
    assert result["decision"] == "waiting"
    assert result["holder_line_id"] == l1
    stored = json.loads((reg / f"{l2}.json").read_text())
    assert stored["state"] == "waiting"


def test_disjoint_write_lines_commit_concurrently(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    l1, l2 = make_line_id("dis1"), make_line_id("dis2")
    wt1, wt2 = tmp_path / "wt1", tmp_path / "wt2"
    _register(reg, repo, l1, wt1)
    _register(reg, repo, l2, wt2)
    _add_worktree(repo, wt1, l1)
    _add_worktree(repo, wt2, l2)
    r1 = engine_json("ownership-check", "--line-id", l1, "--manifest",
                     str(_manifest(tmp_path / "m1.json", l1, ["a/"])), reg=reg)
    r2 = engine_json("ownership-check", "--line-id", l2, "--manifest",
                     str(_manifest(tmp_path / "m2.json", l2, ["b/"])), reg=reg)
    assert r1["decision"] == "proceed" and r2["decision"] == "proceed"
    c1 = _commit(wt1, "a/one.txt", "one", "line one")
    c2 = _commit(wt2, "b/two.txt", "two", "line two")
    fsck = subprocess.run(["git", "-C", str(repo), "fsck", "--no-dangling"], capture_output=True, text=True)
    assert fsck.returncode == 0, fsck.stderr
    all_commits = git(repo, "rev-list", "--all").stdout.split()
    assert c1 in all_commits and c2 in all_commits
    assert git(wt1, "rev-parse", "HEAD").stdout.strip() == c1
    assert git(wt2, "rev-parse", "HEAD").stdout.strip() == c2


def test_queue_replay_is_byte_identical_and_dependencies_first(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    l1, l2, l3 = (make_line_id(f"que{i}") for i in range(3))
    for line in (l1, l2, l3):
        _register(reg, repo, line, tmp_path / f"wt-{line}")
        engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    # l3 depends on l1 although it is first by timestamp.
    l3_manifest = _manifest(tmp_path / "m3.json", l3, ["c/"])
    data = json.loads(l3_manifest.read_text())
    data["integration_depends_on"] = [l1]
    l3_manifest.write_text(json.dumps(data), encoding="utf-8")
    engine_json("ownership-check", "--line-id", l3, "--manifest", str(l3_manifest), reg=reg)
    engine_json("integration-enqueue", "--line-id", l3, "--at", "2026-10-20T10:00:00Z", reg=reg)
    engine_json("integration-enqueue", "--line-id", l1, "--at", "2026-10-20T11:00:00Z", reg=reg)
    engine_json("integration-enqueue", "--line-id", l2, "--at", "2026-10-20T12:00:00Z", reg=reg)
    first = engine_json("integration-plan", reg=reg)
    second = engine_json("integration-plan", reg=reg)
    assert first == second
    order = [entry["line_id"] for entry in first if entry.get("order")]
    assert order.index(l1) < order.index(l3)
    assert order == [l1, l2, l3]


def test_failed_integration_retains_worktree_and_records(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("failq")
    worktree = tmp_path / "wt-fail"
    _register(reg, repo, line, worktree)
    _add_worktree(repo, worktree, line)
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", line, reg=reg)
    record = engine_json(
        "integration-record", "--line-id", line, "--result", "failed",
        "--reason", "quality-gate", reg=reg,
    )
    assert record["integration_result"]["status"] == "failed"
    assert record["merge_ready"] is False
    assert record["state"] == "completed"
    assert worktree.exists()
    dereg = engine_json("deregister", "--line-id", line, "--reason", "abandoned", reg=reg)
    assert dereg["worktree_retained"] is True


def test_runtime_archive_once_before_removal(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("archq")
    worktree = tmp_path / "wt-arch"
    _register(reg, repo, line, worktree)
    _add_worktree(repo, worktree, line)
    runtime = worktree / ".specify" / "memory" / "feedback"
    runtime.mkdir(parents=True)
    (runtime / "entry.md").write_text("feedback", encoding="utf-8")
    evidence = worktree / ".specify" / "memory" / "evidence"
    evidence.mkdir(parents=True)
    (evidence / "ev.md").write_text("evidence", encoding="utf-8")
    dest = tmp_path / "integration-archive"
    manifest = engine_json(
        "archive-runtime", "--line-id", line, "--worktree", str(worktree),
        "--dest", str(dest), reg=reg,
    )
    assert len(manifest["files"]) == 1
    manifest_file = dest / f"runtime-archive-{line}.json"
    assert manifest_file.exists()
    archived = json.loads(manifest_file.read_text())
    assert archived["line_id"] == line
    assert archived["files"][0]["sha256"]
    assert worktree.exists()


EXECUTOR = (
    Path(__file__).resolve().parents[2]
    / "skills" / "external" / "sdd-loop-driver" / "scripts" / "integrate-lines.py"
)


def _execute(repo: Path, reg: Path, archive: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EXECUTOR), "--repo", str(repo), "--trunk", "main",
         "--registry", str(reg), "--archive", str(archive), *extra],
        capture_output=True, text=True,
    )


def _build_two_line_queue(root: Path):
    repo = make_git_repo(root)
    reg = root / "reg"
    # Fixed IDs keep the two replay scenarios comparable.
    lines = ["ex1-20261020T120000Z-aaaa", "ex2-20261020T120000Z-bbbb"]
    worktrees = []
    for index, line in enumerate(lines):
        worktree = root / f"wt-{index}"
        worktrees.append(worktree)
        _register(reg, repo, line, worktree)
        _add_worktree(repo, worktree, line)
        _commit(worktree, f"src/file{index}.txt", f"line {index}\n", f"line {index}")
        engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
        engine_json("integration-enqueue", "--line-id", line,
                    "--at", f"2026-10-20T12:00:0{index}Z", reg=reg)
    return repo, reg, lines, worktrees


def test_integration_executor_merges_queue_and_replay_is_identical(tmp_path):
    def scenario(root: Path) -> tuple[str, list[str], dict]:
        root.mkdir(parents=True, exist_ok=True)
        repo, reg, lines, worktrees = _build_two_line_queue(root)
        counter = root / "mirror-count"
        proc = _execute(
            repo, reg, root / "archive",
            "--gate-cmd", "test -f README.md",
            "--mirror-cmd", f"printf x >> '{counter}'",
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        summary = json.loads(proc.stdout)
        assert [row["line_id"] for row in summary["results"]] == lines
        assert all(row["status"] == "merged" for row in summary["results"])
        assert summary["archive_calls"] == 2
        assert summary["mirror_calls"] == 1
        assert all(row["worktree_removed"] for row in summary["results"])
        assert counter.read_text() == "x", "mirrors must run once per batch, never per line"
        for worktree in worktrees:
            assert not worktree.exists()
        assert (repo / "src" / "file0.txt").exists() and (repo / "src" / "file1.txt").exists()
        fsck = subprocess.run(
            ["git", "-C", str(repo), "fsck", "--no-dangling"], capture_output=True, text=True
        )
        assert fsck.returncode == 0, fsck.stderr
        tree = git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
        return tree, lines, summary

    first_tree, first_lines, _ = scenario(tmp_path / "run1")
    second_tree, second_lines, _ = scenario(tmp_path / "run2")
    assert first_lines == second_lines
    assert first_tree == second_tree, "merge result must replay to an identical tree"


def test_integration_executor_failure_retains_worktree_and_continues(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    failing, passing = make_line_id("exf"), make_line_id("exp")
    wt_fail, wt_pass = tmp_path / "wt-fail", tmp_path / "wt-pass"
    _register(reg, repo, failing, wt_fail)
    _register(reg, repo, passing, wt_pass)
    _add_worktree(repo, wt_fail, failing)
    _add_worktree(repo, wt_pass, passing)
    _commit(wt_fail, "FAIL_GATE", "fail\n", "failing line")
    _commit(wt_pass, "src/pass.txt", "pass\n", "passing line")
    engine_json("update", "--line-id", failing, "--state", "completed", reg=reg)
    engine_json("update", "--line-id", passing, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", failing,
                "--at", "2026-10-20T12:00:00Z", reg=reg)
    engine_json("integration-enqueue", "--line-id", passing,
                "--at", "2026-10-20T12:00:01Z", reg=reg)

    proc = _execute(
        repo, reg, tmp_path / "archive",
        "--gate-cmd", "test ! -f FAIL_GATE",
    )
    assert proc.returncode == 3, proc.stdout
    summary = json.loads(proc.stdout)
    by_line = {row["line_id"]: row for row in summary["results"]}
    assert by_line[failing]["status"] == "failed"
    assert by_line[failing]["reason"] == "quality-gate"
    assert by_line[passing]["status"] == "merged"
    assert summary["archive_calls"] == 1
    assert wt_fail.exists(), "failed integration must retain its worktree"
    assert not wt_pass.exists()
    stored_fail = json.loads((reg / f"{failing}.json").read_text())
    assert stored_fail["integration_result"]["status"] == "failed"
    stored_pass = json.loads((reg / f"{passing}.json").read_text())
    assert stored_pass["integration_result"]["status"] == "merged"


def test_integration_executor_refuses_preexisting_rebase(tmp_path):
    repo = make_git_repo(tmp_path)
    reg = tmp_path / "reg"
    line = make_line_id("prewh")
    worktree = tmp_path / "wt-pre"
    _register(reg, repo, line, worktree)
    _add_worktree(repo, worktree, line)
    _commit(worktree, "src/pre.txt", "pre\n", "pre")
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", line, reg=reg)
    marker = Path(git(worktree, "rev-parse", "--git-path", "rebase-merge").stdout.strip())
    if not marker.is_absolute():
        marker = worktree / marker
    marker.mkdir(parents=True, exist_ok=True)
    env_marker = marker / "dummy"
    env_marker.write_text("preexisting\n", encoding="utf-8")

    proc = _execute(repo, reg, tmp_path / "archive")
    assert proc.returncode == 3, proc.stdout
    summary = json.loads(proc.stdout)
    assert summary["results"][0]["reason"] == "rebase-in-progress"
    assert marker.exists(), "a pre-existing rebase must never be aborted"
    stored = json.loads((reg / f"{line}.json").read_text())
    assert stored["integration_result"]["status"] == "failed"
    assert worktree.exists()


def test_no_push_in_engine_surfaces():
    skill = Path(__file__).resolve().parents[2] / "skills" / "external" / "sdd-loop-driver"
    for path in [skill / "scripts" / "line-registry.py", skill / "scripts" / "watch-target.sh"]:
        assert "git push" not in path.read_text(encoding="utf-8")
