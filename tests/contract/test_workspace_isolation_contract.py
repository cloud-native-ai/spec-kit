"""Contract tests for contracts/workspace-isolation.md (WI-01…WI-21)."""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    engine_json,
    engine_path,
    git,
    make_git_repo,
    make_line_id,
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


def test_wi_02_branch_discipline(tmp_path):
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


def test_wi_11_mirrors_once():
    text = _docs()
    assert "sync-mirrors.py" in text
    assert "整批" in text or "每批" in text
    assert "MUST NOT 每 line" in text or "不得每 line" in text or "不在逐线序列" in text


def test_wi_12_single_coordinator():
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


def test_wi_16_cleanup_without_force():
    text = _docs()
    assert "git worktree remove" in text
    assert "--force" in text  # mentioned as prohibited
    assert "无 `--force`" in text or "不带 --force" in text or "无 --force" in text


def test_wi_17_crash_reentry():
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


def test_wi_21_two_write_line_delegate():
    integration = (
        Path(__file__).resolve().parents[1] / "integration" / "test_worktree_integration_queue.py"
    )
    text = integration.read_text(encoding="utf-8")
    for needle in ["git", "fsck", "overlap", "replay", "archive"]:
        assert needle in text
