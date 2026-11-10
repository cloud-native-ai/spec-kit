"""Unit tests: the migrate receipt store (097 T006).

Red-first: authored before the receipt store exists in ``specify_cli``.

Storage contract (data-model.md E-3 / migrate-engine.md C-7):

* one receipt file per run at ``.specify/memory/migrate/receipts/<run-id>.json``;
* run-id shape ``YYYYMMDDTHHMMSSZ-<8 hex>``;
* ``running`` on apply start, ``completed`` on clean close;
* two concurrent writers land on distinct paths and never touch each other's
  file; a dry-run writes no receipt file at all (FR-006 zero-write).
"""

import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

import pytest

FIXED_NOW = datetime(2026, 11, 10, 9, 30, 12, tzinfo=timezone.utc)
RUN_ID_RE = re.compile(r"^\d{8}T\d{6}Z-[0-9a-f]{8}$")


def test_run_id_shape_and_uniqueness():
    from specify_cli import migrate_run_id

    first = migrate_run_id(FIXED_NOW)
    second = migrate_run_id(FIXED_NOW)

    assert RUN_ID_RE.fullmatch(first), first
    assert first.startswith("20261110T093012Z-")
    assert first != second, "same-second runs must carry distinct random suffixes"


def test_one_receipt_file_per_run_in_running_state(tmp_path):
    from specify_cli import create_migrate_receipt, migrate_receipts_dir

    run_id, path = create_migrate_receipt(tmp_path, now=FIXED_NOW)

    assert path == migrate_receipts_dir(tmp_path) / f"{run_id}.json"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["receiptVersion"] == 1
    assert payload["runId"] == run_id
    assert payload["mode"] == "apply"
    assert payload["status"] == "running"
    assert payload["finishedAt"] is None
    assert payload["startedAt"] == "2026-11-10T09:30:12Z"
    assert payload["workspace"] == str(tmp_path.resolve())
    assert payload["items"] == []
    assert payload["archives"] == []
    assert [p.name for p in migrate_receipts_dir(tmp_path).iterdir()] == [
        f"{run_id}.json"
    ]


def test_two_concurrent_writers_land_on_distinct_paths(tmp_path):
    from specify_cli import create_migrate_receipt

    results = []
    barrier = threading.Barrier(2)
    errors = []

    def writer():
        try:
            barrier.wait(timeout=10)
            results.append(create_migrate_receipt(tmp_path, now=FIXED_NOW))
        except BaseException as exc:  # surfaced below, never swallowed
            errors.append(exc)

    threads = [threading.Thread(target=writer) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)

    assert not errors
    assert len(results) == 2
    run_ids = [run_id for run_id, _ in results]
    paths = [path for _, path in results]
    assert len(set(run_ids)) == 2
    assert len(set(paths)) == 2
    assert all(path.is_file() for path in paths)


def test_running_to_completed_transition_never_touches_another_run(tmp_path):
    from specify_cli import (
        complete_migrate_receipt,
        create_migrate_receipt,
        update_migrate_receipt,
    )

    run_one, path_one = create_migrate_receipt(tmp_path, now=FIXED_NOW)
    run_two, path_two = create_migrate_receipt(tmp_path, now=FIXED_NOW)
    untouched_before = path_two.read_bytes()

    update_migrate_receipt(
        path_one,
        items=[
            {
                "id": "abc123abc123",
                "dimension": "migration-residue",
                "target": ".specify/skills/web-test",
                "status": "done",
            }
        ],
    )
    completed = complete_migrate_receipt(path_one)

    payload = json.loads(path_one.read_text(encoding="utf-8"))
    assert payload["status"] == "completed"
    assert payload["finishedAt"] is not None
    assert payload["items"][0]["status"] == "done"
    assert completed["runId"] == run_one
    assert path_two.read_bytes() == untouched_before
    assert json.loads(path_two.read_text(encoding="utf-8"))["runId"] == run_two


def test_dry_run_writes_no_receipt_file(tmp_path):
    from specify_cli import migrate_receipts_dir, migrate_run_id, persist_migrate_receipt

    run_id = migrate_run_id(FIXED_NOW)
    dry_receipt = {
        "receiptVersion": 1,
        "runId": run_id,
        "mode": "dry-run",
        "status": "completed",
        "finishedAt": "2026-11-10T09:30:12Z",
        "items": [],
        "archives": [],
    }

    assert persist_migrate_receipt(tmp_path, dry_receipt) is None
    assert not migrate_receipts_dir(tmp_path).exists()

    dry_receipt["mode"] = "apply"
    path = persist_migrate_receipt(tmp_path, dry_receipt)
    assert path is not None
    assert path.is_file()
    assert json.loads(path.read_text(encoding="utf-8"))["runId"] == run_id


def test_receipt_carries_per_run_file_shape_not_a_shared_aggregate(tmp_path):
    from specify_cli import create_migrate_receipt, migrate_receipts_dir

    create_migrate_receipt(tmp_path, now=FIXED_NOW)
    create_migrate_receipt(tmp_path, now=FIXED_NOW)

    entries = sorted(p.name for p in migrate_receipts_dir(tmp_path).iterdir())
    assert len(entries) == 2
    assert {p.suffix for p in migrate_receipts_dir(tmp_path).iterdir()} == {".json"}
    assert all(RUN_ID_RE.fullmatch(Path(name).stem) for name in entries)
