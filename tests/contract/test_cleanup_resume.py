"""G-7b (T069) — a cleanup interrupted at either declared seam resumes from that seam.

The engine declares two fault points (`GOAL_UTILS_CLEANUP_FAULT_AFTER`): after the target is
written and after the receipt is written. Both are injected here through the real environment,
so the assertion subject is the shipped interruption path, not a mock.

Red conditions: an interrupted run that does not report the phase it reached; a resume that does
not continue at the next phase; a receipt-less target re-blessed by a later run; a source removed
before its receipt exists; a resumed removal that rewrites the receipt it already wrote.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
FIXTURE = ROOT / "tests/fixtures/anchor-goal-realignment"
ENGINE = ROOT / "scripts/python/goal-utils.py"

FAULT_ENV = "GOAL_UTILS_CLEANUP_FAULT_AFTER"
INTERRUPTED_EXIT = 3  # docstring: "not found or migration interrupted"
HALF_STATE_EXIT = 4   # a definition exists but cannot be interpreted


def _scratch(target: Path) -> Path:
    root = target / "tree"
    root.mkdir(parents=True)
    shutil.copytree(FIXTURE / "pre-convergence/.specify", root / ".specify")
    shutil.copy2(FIXTURE / "classification/classification.json", root / "classification.json")
    for command in (["init", "-q", "."], ["add", "-A"], ["commit", "-qm", "fixture"]):
        subprocess.run(
            ["git", "-c", "user.email=guard@example.invalid",
             "-c", "user.name=guard", *command],
            cwd=str(root), check=True, capture_output=True, text=True)
    return root


def _run(root: Path, *, apply: bool, fault: str | None = None):
    env = dict(os.environ)
    env.pop(FAULT_ENV, None)
    if fault is not None:
        env[FAULT_ENV] = fault
    result = subprocess.run(
        [sys.executable, str(ENGINE), "cleanup", "--apply" if apply else "--check",
         "--repo-root", str(root), "--classification", str(root / "classification.json"),
         "--json"],
        cwd=str(root), capture_output=True, text=True, check=False, env=env)
    return result.returncode, json.loads(result.stdout or "{}")


def _row(decisions: list[dict], slug: str) -> dict:
    return next(row for row in decisions if row.get("slug") == slug)


def _receipts(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix()
                  for path in root.rglob("*-receipt.json"))


def test_the_run_interrupted_before_remove_source_reports_that_phase(tmp_path):
    root = _scratch(tmp_path)
    code, payload = _run(root, apply=True, fault="write-target")
    assert code == INTERRUPTED_EXIT, (code, payload)
    assert payload.get("result") == "interrupted", payload
    assert payload.get("reached_phase") == "write-target", payload
    assert payload.get("target_exists") is True

    receipt = root / payload["receipt_path"]
    assert not receipt.exists(), "the write-target seam stopped before the receipt"
    slug = payload["target_path"].split("/")[-2]
    source = payload["target_path"].replace("/goals/", "/anchoring/").rsplit("/", 1)[0]
    assert (root / source / "goal.md").is_file(), "the interruption removed its source"

    code, payload = _run(root, apply=True)
    assert code == 0, payload
    assert payload.get("verdict") == "ok", payload
    row = _row(payload["decisions"], slug)
    assert (row.get("action"), row.get("resumed_at")) == ("resume-receipt", "write-receipt")
    assert receipt.is_file() and not (root / source).exists(), \
        "the resumed run must write the receipt before removing the source"
    assert len(_receipts(root)) == len(set(_receipts(root))), "a receipt was duplicated"


def test_the_run_interrupted_after_write_receipt_resumes_the_removal(tmp_path):
    root = _scratch(tmp_path)
    code, payload = _run(root, apply=True, fault="write-receipt")
    assert code == INTERRUPTED_EXIT, (code, payload)
    assert payload.get("reached_phase") == "write-receipt", payload
    assert payload.get("target_exists") is True

    receipt = root / payload["receipt_path"]
    assert receipt.is_file(), "the write-receipt seam must leave its receipt in place"
    settled_bytes = hashlib.sha256(receipt.read_bytes()).hexdigest()
    slug = payload["target_path"].split("/")[-2]
    source = payload["target_path"].replace("/goals/", "/anchoring/").rsplit("/", 1)[0]
    assert (root / source / "goal.md").is_file(), "the source is removed too early"

    code, payload = _run(root, apply=True)
    assert code == 0, payload
    assert payload.get("verdict") == "ok", payload
    row = _row(payload["decisions"], slug)
    assert (row.get("action"), row.get("resumed_at")) == ("resume-remove", "remove-source")
    assert not (root / source).exists(), "the resumed run did not finish the removal"
    assert hashlib.sha256(receipt.read_bytes()).hexdigest() == settled_bytes, \
        "the resumed removal rewrote a receipt it had already written"


def test_a_receipt_less_target_is_the_exit_4_half_state(tmp_path):
    root = _scratch(tmp_path)
    code, payload = _run(root, apply=True)
    assert code == 0 and payload.get("verdict") == "ok", payload

    receipt = next(path for path in sorted(root.rglob("migration-receipt.json")))
    body = json.loads(receipt.read_text(encoding="utf-8"))
    target = root / body["target_path"]
    settled = hashlib.sha256(target.read_bytes()).hexdigest()
    receipt.unlink()
    assert not (root / body["source_path"]).exists(), "the fixture source is still present"

    for apply in (False, True):
        code, payload = _run(root, apply=apply)
        assert code == HALF_STATE_EXIT, (apply, code, payload)
        assert "half-state" in payload.get("error", ""), payload
        assert body["target_path"] in payload["error"], payload

    assert not receipt.exists(), "the engine silently blessed a receipt-less target"
    assert hashlib.sha256(target.read_bytes()).hexdigest() == settled, \
        "the half-state run rewrote the un-receipted definition"
