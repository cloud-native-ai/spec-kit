"""Contract tests for interrupted migrations and their resumption.

Feature 094, `contracts/unified-archive-and-migration.md` C-35/C-39; tasks rows
T031 and T040 (FR-010, SC-011). The interruption point is injected with the
engine's declared test seam `GOAL_UTILS_FAULT_AFTER` (closed values
`target-write` / `source-move`), so the reading is the engine's real behaviour,
not a story about it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

GOAL_SOURCE = """---
status: active
created: 2026-11-09
updated: 2026-11-09
---

# Goal: resumed

## Objective

Resume the interrupted archive move without moving the tree a second time.

## Success Criteria

1. The second call finishes the receipt.

## History

- 2026-11-09 — created in the spec-local layout.
"""


def _run(root: Path, *args: str, fault: str | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if fault is not None:
        env["GOAL_UTILS_FAULT_AFTER"] = fault
    else:
        env.pop("GOAL_UTILS_FAULT_AFTER", None)
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT, env=env)


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no JSON payload; stderr={proc.stderr!r}"
    return json.loads(proc.stdout)


def _receipt(root: Path, kind: str, slug: str) -> dict:
    path = root / ".specify/archive/goal-team/receipts" / f"{kind}-{slug}.yaml"
    assert path.is_file(), f"missing receipt: {path}"
    fields: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition(":")
        if sep and key and not key.startswith(" "):
            fields[key.strip()] = value.strip()
    return fields


def _seed(root: Path, spec: str = "091-interrupt", slug: str = "alpha") -> Path:
    tree = root / ".specify/specs" / spec / "goal" / slug
    tree.mkdir(parents=True, exist_ok=True)
    (tree / "goal.md").write_text(GOAL_SOURCE, encoding="utf-8")
    (tree / "keep.txt").write_text("one copy only\n", encoding="utf-8")
    return tree


def test_an_interrupted_run_reports_its_step_and_resumes_without_a_second_move(tmp_path):
    spec = "091-interrupt"
    for fault in ("target-write", "source-move"):
        root = tmp_path / fault
        source = _seed(root)

        first = _run(root, "migrate-archive", "--apply", fault=fault)
        assert first.returncode == 3, (
            f"an interruption exits 3 (distinct from 0 complete and 2 input error); got "
            f"{first.returncode}: {first.stdout!r} {first.stderr!r}")
        state = _payload(first)
        assert state["reached_step"] == fault
        assert state["target_exists"] is True
        assert state["archived_path"] == (
            f".specify/archive/goal-team/trees/{spec}/goal/alpha")

        receipt = _receipt(root, "goal", "alpha")
        assert receipt["result"] == "interrupted"
        assert receipt["reached_step"] == fault
        assert receipt["delete_policy"] == "archive-not-delete"

        second = _run(root, "migrate-archive", "--apply")
        assert second.returncode == 0, second.stdout + second.stderr
        decisions = _payload(second)["decisions"]
        assert [(d["kind"], d["slug"], d["result"]) for d in decisions] == [
            ("goal", "alpha", "migrated")]
        assert _receipt(root, "goal", "alpha")["result"] == "migrated"

        # The resumed call completed the move exactly once: the source position is gone
        # and the one archived copy (including the extra file) is readable under trees/.
        archived = root / ".specify/archive/goal-team/trees" / spec / "goal" / "alpha"
        assert (archived / "goal.md").is_file()
        assert (archived / "keep.txt").read_text(encoding="utf-8") == "one copy only\n"
        assert not source.exists(), "a resumed call must not move a tree a second time"

        third = _run(root, "migrate-archive", "--apply")
        assert third.returncode == 0
        assert _payload(third)["decisions"][0]["result"] == "noop"
