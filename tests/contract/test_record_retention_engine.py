from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "record-retention.py"

OLD = "2026-09-01T00:00:00Z"


def _run(ws: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--workspace-root", str(ws)],
        capture_output=True, text=True, timeout=120)


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no stdout (rc={proc.returncode}): {proc.stderr}"
    return json.loads(proc.stdout)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def seed(ws: Path, created: str = OLD) -> dict:
    (ws / ".specify/memory/exec-quant/records").mkdir(parents=True, exist_ok=True)
    (ws / ".specify/memory/feedback").mkdir(parents=True, exist_ok=True)
    (ws / ".specify/memory/session").mkdir(parents=True, exist_ok=True)

    _write(ws / ".specify/memory/exec-quant/records/old.json", json.dumps({
        "kind": "speckit.exec-quant",
        "schema_version": 2,
        "unit_id": "/speckit.plan",
        "unit_type": "command",
        "run_id": "r-old",
        "collected_at": created,
        "quality": {"tokens": "not_evaluated", "elapsed_ms": "not_evaluated"},
    }) + "\n")

    _write(ws / ".specify/memory/feedback/20260901T000000Z-speckit-plan.md", f"""---
id: "20260901T000000Z-speckit-plan"
unit_id: "/speckit.plan"
unit_type: "command"
run_id: "r-old"
disposition: "processed"
created: "{created}"
summary: "done"
disposition_reason: "consumed in test"
---

## Review
done
""")
    _write(ws / ".specify/memory/feedback/20260901T000000Z-speckit-open.md", f"""---
id: "20260901T000000Z-speckit-open"
unit_id: "/speckit.plan"
unit_type: "command"
run_id: "r-open"
disposition: "open"
created: "{created}"
summary: "open"
---

## Review
open
""")

    def rd(name: str, run: str, settled: str | None) -> None:
        record = {
            "kind": "speckit.run-determination",
            "schema_version": 1,
            "unit_id": "/speckit.plan",
            "unit_type": "command",
            "run_id": run,
            "determined_at": created,
            "settled_at": settled,
            "complexity": "complex",
            "qualification": "qualified",
            "axes": {},
        }
        body = "summary\n\n```json\n" + json.dumps(record, indent=2) + "\n```\n"
        _write(ws / ".specify/memory/session" / name, f"""---
id: "{name[:-3]}"
scope: "session"
source: "/speckit.plan"
tags: ["run-determination", "{run}"]
title: "run-determination {run}"
created: "{created}"
summary: "summary"
---

{body}""")

    rd("20260901T000000Z-run-determination-speckit-plan-r1.md",
       "r1", "2026-09-02T00:00:00Z")
    rd("20260901T000000Z-run-determination-speckit-plan-r2.md", "r2", None)
    _write(ws / ".specify/memory/session/2026-09-01-note.md",
           "# a note\n\nworking context\n")
    promotions = ws / "promotions.json"
    _write(promotions, json.dumps({"promotions": [
        {"entry": "2026-09-01-note.md", "type": "ephemeral",
         "reason": "working context only"},
    ]}) + "\n")
    return {"promotions": promotions}


def _distill(ws: Path, promotions: Path | None = None) -> dict:
    args = ["--action", "distill"]
    if promotions is not None:
        args += ["--promotions", str(promotions)]
    proc = _run(ws, *args)
    assert proc.returncode == 0, proc.stderr
    return _json(proc)


def _plan(ws: Path, *stores: str) -> Path:
    args = ["--action", "plan"]
    if stores:
        args += ["--stores", ",".join(stores)]
    proc = _run(ws, *args)
    assert proc.returncode == 0, proc.stderr
    return Path(_json(proc)["plan"])


def _confirm(plan: Path) -> None:
    node = json.loads(plan.read_text(encoding="utf-8"))
    node["confirmed"] = True
    plan.write_text(json.dumps(node, indent=2) + "\n", encoding="utf-8")


def _apply(ws: Path, plan: Path, *extra: str) -> subprocess.CompletedProcess:
    return _run(ws, "--action", "apply", "--plan", str(plan), *extra)


def test_args_manifest_matches_parser() -> None:
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "args-manifest"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    manifest = json.loads(proc.stdout)
    assert set(manifest) == {"scan", "distill", "plan", "apply", "status",
                             "args-manifest"}
    assert manifest["apply"]["required"] == ["--plan"]


def test_scan_is_read_only_and_reports_blocked(tmp_path: Path) -> None:
    seed(tmp_path)
    before = {p: p.stat().st_mtime_ns for p in tmp_path.rglob("*") if p.is_file()}
    proc = _run(tmp_path, "--action", "scan")
    assert proc.returncode == 0, proc.stderr
    payload = _json(proc)
    after = {p: p.stat().st_mtime_ns for p in tmp_path.rglob("*") if p.is_file()}
    assert before == after
    assert payload["stores"]["exec-quant"]["total"] == 1
    assert payload["stores"]["exec-quant"]["blocked"] == 1
    reasons = {row["reason"] for row in payload["blocked"]}
    assert {"open", "unsettled", "needs-promotion"} <= reasons
    assert payload["candidates"] == []


def test_distill_writes_receipts_and_summaries(tmp_path: Path) -> None:
    seeded = seed(tmp_path)
    payload = _distill(tmp_path, seeded["promotions"])
    assert payload["stores"]["exec-quant"]["receipts"] == 1
    assert payload["stores"]["exec-quant"]["summaries"] == 1
    assert payload["stores"]["feedback"]["receipts"] == 1
    assert payload["stores"]["run-determination"]["receipts"] == 1
    assert payload["stores"]["session-note"]["receipts"] == 1

    receipts = sorted((tmp_path / ".specify/memory/retention/receipts").glob("*.json"))
    assert len(receipts) == 4
    by_store = {}
    for path in receipts:
        node = json.loads(path.read_text(encoding="utf-8"))
        by_store[node["store"]] = node
    assert by_store["feedback"]["carrier"]["type"] == "disposition_reason"
    assert by_store["session-note"]["carrier"]["type"] == "ephemeral"
    assert by_store["exec-quant"]["carrier"]["type"] == "summary"

    scan = _json(_run(tmp_path, "--action", "scan"))
    assert len(scan["candidates"]) == 4
    assert scan["stores"]["feedback"]["blocked"] == 1
    assert scan["stores"]["run-determination"]["blocked"] == 1


def test_apply_requires_confirmation_and_conserves_counts(tmp_path: Path) -> None:
    seeded = seed(tmp_path)
    _distill(tmp_path, seeded["promotions"])
    plan = _plan(tmp_path)

    refused = _apply(tmp_path, plan, "--allow-unversioned")
    assert refused.returncode == 2
    assert "confirmed" in refused.stderr
    assert (tmp_path / ".specify/memory/exec-quant/records/old.json").is_file()

    _confirm(plan)
    applied = _apply(tmp_path, plan, "--allow-unversioned")
    assert applied.returncode == 0, applied.stderr
    payload = _json(applied)
    assert payload["removed"] == 4
    assert payload["remaining"] == 2
    assert payload["conservation_ok"] is True

    assert not (tmp_path / ".specify/memory/exec-quant/records/old.json").exists()
    assert (tmp_path / ".specify/memory/feedback/20260901T000000Z-speckit-open.md").is_file()
    assert (tmp_path / ".specify/memory/session/20260901T000000Z-run-determination-speckit-plan-r2.md").is_file()

    ledger = json.loads(Path(payload["ledger"]).read_text(encoding="utf-8"))
    assert ledger["counts"] == {"before": 6, "removed": 4, "remaining": 2,
                                "expected_remaining": 2}
    assert ledger["conservation_ok"] is True


def test_idempotent_distill(tmp_path: Path) -> None:
    seeded = seed(tmp_path)
    first = _distill(tmp_path, seeded["promotions"])
    second = _distill(tmp_path, seeded["promotions"])
    assert sum(item["receipts"] for item in first["stores"].values()) == 4
    assert sum(item["receipts"] for item in second["stores"].values()) == 0
    assert sum(item["summaries"] for item in second["stores"].values()) == 0


def test_too_young_is_not_planned(tmp_path: Path) -> None:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seeded = seed(tmp_path, created=now)
    _distill(tmp_path, seeded["promotions"])
    scan = _json(_run(tmp_path, "--action", "scan", "--stores", "exec-quant"))
    assert scan["stores"]["exec-quant"]["too_young"] == 1
    assert scan["candidates"] == []
    plan = _plan(tmp_path, "exec-quant")
    assert json.loads(plan.read_text(encoding="utf-8"))["items"] == []


def test_apply_refuses_non_git_without_opt_in(tmp_path: Path) -> None:
    seeded = seed(tmp_path)
    _distill(tmp_path, seeded["promotions"])
    plan = _plan(tmp_path, "exec-quant")
    _confirm(plan)
    refused = _apply(tmp_path, plan)
    assert refused.returncode == 2
    assert "not clean in git" in refused.stderr
    assert (tmp_path / ".specify/memory/exec-quant/records/old.json").is_file()


def test_apply_refuses_dirty_git_targets(tmp_path: Path) -> None:
    seeded = seed(tmp_path)
    _distill(tmp_path, seeded["promotions"])
    plan = _plan(tmp_path, "feedback")
    _confirm(plan)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t",
         "commit", "-qm", "seed"], cwd=tmp_path, check=True)
    target = tmp_path / ".specify/memory/feedback/20260901T000000Z-speckit-plan.md"
    target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    refused = _apply(tmp_path, plan)
    assert refused.returncode == 2
    assert "not clean in git" in refused.stderr
    assert target.is_file()
    applied = _apply(tmp_path, plan, "--allow-unversioned")
    assert applied.returncode == 0, applied.stderr


def test_two_writers_create_distinct_receipt_paths(tmp_path: Path) -> None:
    seed(tmp_path)
    procs = [
        subprocess.Popen(
            [sys.executable, str(ENGINE), "--action", "distill", "--stores",
             "exec-quant", "--workspace-root", str(tmp_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for _ in range(2)
    ]
    for proc in procs:
        _out, err = proc.communicate(timeout=120)
        assert proc.returncode == 0, err
    receipts = list((tmp_path / ".specify/memory/retention/receipts").glob("*.json"))
    assert receipts
    assert len({p.name for p in receipts}) == len(receipts)
    assert not list((tmp_path / ".specify/memory/retention/receipts").glob("*.part"))
    for path in receipts:
        assert json.loads(path.read_text(encoding="utf-8"))["store"] == "exec-quant"
