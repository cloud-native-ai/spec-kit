"""Integration: US1/US2 store-layout migration — zero-write dry-run, byte-identical
relocation, deterministic dual refusal and idempotent rerun (105 T011).

Green claims: ``contracts/migrate-store-layout.contract.md`` M-2/M-3/M-4/M-6/M-8/M-9 and
``plan.md`` § Test-First Coverage SC-004.

Fixtures come from ``tests/fixtures/store-layout-105/builders.py``, which read every store
name, non-content pattern and the retired-container path from the machine declaration —
never from a snapshot.

Red-first: authored before the store-layout planner/executor exists, so the dry-run plans
no store items, ``--apply`` moves nothing and the receipt store is still the retired one
(readings in ``notes/red-first-evidence.md``).
"""

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "store-layout-105" / "builders.py"


def _builders():
    spec = importlib.util.spec_from_file_location(
        "_store_layout_105_builders", BUILDERS_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _invoke(args):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args)


def _json_payload(result, expected_code):
    assert result.exit_code == expected_code, (
        f"exit {result.exit_code}, expected {expected_code}\n{result.output}"
    )
    return json.loads(result.stdout)


def _dry_run(workspace):
    return _invoke(["migrate", "--workspace", str(workspace), "--format", "json"])


def _apply(workspace):
    return _invoke(
        ["migrate", "--workspace", str(workspace), "--apply", "--format", "json"]
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L {rel} -> {os.readlink(path)}\n".encode("utf-8"))
        elif path.is_dir():
            digest.update(f"D {rel}\n".encode("utf-8"))
        else:
            digest.update(f"F {rel} {_sha256(path)}\n".encode("utf-8"))
    return digest.hexdigest()


def _store_files(root: Path) -> dict:
    """`relpath -> sha256` for every file under a store root (dirs excluded)."""
    files = {}
    if not root.is_dir():
        return files
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            files[path.relative_to(root).as_posix()] = _sha256(path)
    return files


def _receipts(workspace: Path):
    return sorted(
        specify_cli.migrate_receipts_dir(workspace).glob("*.json")
    )


def _git(workspace: Path, *args):
    return subprocess.run(
        ["git", "-C", str(workspace)] + list(args),
        capture_output=True,
        text=True,
        check=True,
    )


def _git_commit_fixture(workspace: Path) -> None:
    _git(workspace, "init", "-q")
    _git(workspace, "add", "-A")
    _git(
        workspace,
        "-c",
        "user.email=fixture@example.invalid",
        "-c",
        "user.name=fixture",
        "commit",
        "-qm",
        "fixture",
    )


def _git_status(workspace: Path) -> str:
    return _git(workspace, "status", "--porcelain").stdout


def _store_items(payload):
    return [
        item for item in payload["items"] if item["dimension"] == "store-layout"
    ]


# ---------------------------------------------------------------------------
# US1 side: a fresh new-layout init already converges for this dimension
# ---------------------------------------------------------------------------


def test_fresh_init_plans_no_store_items(tmp_path):
    workspace = tmp_path / "fresh"
    specify_cli.copy_local_templates(
        workspace, "qoder", "sh", is_current_dir=False
    )

    payload = _json_payload(_dry_run(workspace), 0)

    assert payload["outcome"] == "clean"
    assert _store_items(payload) == []
    assert payload["summary"]["byDimension"]["store-layout"] == 0


# ---------------------------------------------------------------------------
# US2: legacy fixture — dry-run plans every store and writes nothing
# ---------------------------------------------------------------------------


def test_legacy_dry_run_writes_nothing_and_plans_every_store(tmp_path):
    builders = _builders()
    workspace = builders.build_legacy(tmp_path / "legacy")
    roster = builders.store_names()
    _git_commit_fixture(workspace)
    before = _tree_digest(workspace)
    status_before = _git_status(workspace)
    receipt_store = workspace / ".specify" / "migrate"

    first = _json_payload(_dry_run(workspace), 1)

    items = _store_items(first)
    store_targets = sorted(
        item["target"] for item in items if item["target"] != ".specify/memory"
    )
    assert store_targets == sorted(f".specify/{name}" for name in roster)
    assert all(
        item["disposition"] == "archive" and item["mechanism"] == "relocate"
        for item in items
        if item["target"] != ".specify/memory"
    ), "every legacy store must plan an archive/relocate item"
    container = [item for item in items if item["target"] == ".specify/memory"]
    assert len(container) == 1
    assert container[0]["disposition"] == "archive"
    assert container[0]["mechanism"] == "none"
    for item in items:
        if item["target"] == ".specify/memory":
            continue
        assert item["entries"], f"no entries manifest for {item['target']}"
        assert all(row["status"] == "planned" for row in item["entries"])

    # Zero-write: identical tree shape+content, clean git status, no receipt store.
    assert _tree_digest(workspace) == before, "the dry-run wrote to the workspace"
    assert _git_status(workspace) == status_before == ""
    assert not receipt_store.exists(), "a dry-run created the receipt store"
    assert first["receiptPath"] is None

    # Determinism: a second dry-run serializes byte-identical items.
    second = _json_payload(_dry_run(workspace), 1)
    assert second["items"] == first["items"]


# ---------------------------------------------------------------------------
# US2: legacy fixture — apply relocates byte-identically and removes old roots
# ---------------------------------------------------------------------------


def test_legacy_apply_moves_bytes_identically_and_removes_old_roots(tmp_path):
    builders = _builders()
    workspace = builders.build_legacy(tmp_path / "legacy-apply")
    roster = builders.store_names()
    preserved = tmp_path / "preserved"
    for name in roster:
        shutil.copytree(
            workspace / ".specify" / "memory" / name,
            preserved / name,
            symlinks=True,
        )

    payload = _json_payload(_apply(workspace), 0)

    assert payload["outcome"] == "applied"
    assert payload["exitCode"] == 0
    for name in roster:
        assert not (workspace / ".specify" / "memory" / name).exists(), (
            f"the legacy store {name!r} still exists after a successful apply"
        )
        target = workspace / ".specify" / name
        assert target.is_dir(), f"the new store root {name!r} was not created"
        # `diff -r` on the preserved legacy tree vs the relocated root; the migrate
        # store's own receipt directory is this run's transaction record, not content.
        result = subprocess.run(
            ["diff", "-r", "--exclude=receipts", str(preserved / name), str(target)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"store {name!r} is not byte-identical after relocation:\n"
            f"{result.stdout}{result.stderr}"
        )
    assert not (workspace / ".specify" / "memory").exists(), (
        "the retired container survived a fully converged apply"
    )

    files = _receipts(workspace)
    assert len(files) == 1, f"expected exactly one receipt per run, found {files}"
    receipt = json.loads(files[0].read_text(encoding="utf-8"))
    assert receipt["receiptVersion"] == 2
    assert receipt["status"] == "completed"
    assert receipt["outcome"] == "applied"
    layout = receipt["storeLayout"]
    assert layout["stores"] == len(roster)
    assert layout["resolved"] == len(roster)
    assert layout["refused"] == 0
    assert layout["blocked"] == 0
    assert layout["container"] == "removed"
    assert isinstance(layout["manifestDigest"], str) and layout["manifestDigest"]

    store_items = [
        item for item in receipt["items"] if item["dimension"] == "store-layout"
    ]
    moved_digests = set()
    for item in store_items:
        if item["target"] == ".specify/memory":
            continue
        for row in item["entries"]:
            assert row["status"] == "moved", row
            moved_digests.add(row["digest"])
            assert (workspace / row["to"]).is_file()
            assert not (workspace / row["from"]).exists()
    relocated = [
        entry
        for entry in receipt["archives"]
        if entry["change"] == "relocated"
    ]
    assert {entry["digest"] for entry in relocated} == moved_digests
    for entry in relocated:
        assert entry["archiveTo"].startswith(".specify/")
        assert not entry["archiveTo"].startswith(".specify/archive/"), (
            "a pure relocation copied bytes into the archive root"
        )
    assert len(receipt["recover"]) == len(receipt["archives"])


# ---------------------------------------------------------------------------
# US2: dual content refuses deterministically and moves nothing
# ---------------------------------------------------------------------------


def test_dual_content_refuses_with_both_paths_and_leaves_both_trees(tmp_path):
    builders = _builders()
    workspace = builders.build_dual(tmp_path / "dual", store="feedback")
    old_root = workspace / ".specify" / "memory" / "feedback"
    new_root = workspace / ".specify" / "feedback"
    old_before = _store_files(old_root)
    new_before = _store_files(new_root)
    assert old_before and new_before

    payload = _json_payload(_apply(workspace), 3)

    assert payload["outcome"] == "blocked"
    item = next(
        item
        for item in _store_items(payload)
        if item["target"] == ".specify/feedback"
    )
    assert item["disposition"] == "refuse"
    assert item["status"] == "refused"
    reason = item["reason"]
    assert "dual-content" in reason
    assert ".specify/memory/feedback" in reason and ".specify/feedback" in reason
    assert "human adjudication" in reason, (
        "the refusal must name the repair entry, not only the conflict"
    )
    assert _store_files(old_root) == old_before, "the old side changed on a refusal"
    assert _store_files(new_root) == new_before, "the new side changed on a refusal"

    # The container is preserved because the refused store still lives there, and the
    # container pass reports it as residue instead of deleting it.
    assert (workspace / ".specify" / "memory").is_dir()
    container = next(
        item
        for item in _store_items(payload)
        if item["target"] == ".specify/memory"
    )
    assert container["status"] == "refused"
    assert "unknown-residue" in container["reason"]
    assert ".specify/memory/feedback" in container["reason"]


# ---------------------------------------------------------------------------
# US2: a second run after a successful apply is clean and moves nothing
# ---------------------------------------------------------------------------


def test_rerun_after_success_is_clean_with_one_receipt_per_run(tmp_path):
    builders = _builders()
    workspace = builders.build_rerun(tmp_path / "rerun")
    first_receipts = _receipts(workspace)
    assert len(first_receipts) == 1
    first = json.loads(first_receipts[0].read_text(encoding="utf-8"))
    assert first["storeLayout"]["resolved"] == len(builders.store_names())

    payload = _json_payload(_apply(workspace), 0)

    assert payload["outcome"] == "clean"
    assert payload["items"] == []
    assert payload["summary"]["total"] == 0
    receipts = _receipts(workspace)
    assert len(receipts) == 2, "a second run must land its own receipt file"
    run_ids = {
        json.loads(path.read_text(encoding="utf-8"))["runId"] for path in receipts
    }
    assert len(run_ids) == 2
    second = json.loads(
        max(receipts, key=lambda path: path.stat().st_mtime).read_text(
            encoding="utf-8"
        )
    )
    assert second["storeLayout"]["stores"] == 0
    assert second["storeLayout"]["container"] == "absent"
    assert not (workspace / ".specify" / "memory").exists(), (
        "the rerun re-created the retired container"
    )


# ---------------------------------------------------------------------------
# US2 / M-6: a completed resume supersedes the interrupted receipt it resumed
# from, so a third apply is clean instead of replaying the stale receipt
# ---------------------------------------------------------------------------


def _receipt_payloads(workspace):
    return [
        json.loads(path.read_text(encoding="utf-8")) for path in _receipts(workspace)
    ]


def test_third_apply_after_resume_is_clean_because_completed_supersedes(
    tmp_path, monkeypatch
):
    builders = _builders()
    workspace = builders.build_legacy(tmp_path / "resume-supersede")
    retired = workspace / builders.retired_rel()

    real_move = shutil.move
    injected = {"storeMoves": 0}

    def crashing_move(source, destination, *args, **kwargs):
        source_path = Path(str(source))
        if source_path == retired or retired in source_path.parents:
            injected["storeMoves"] += 1
            if injected["storeMoves"] == 2:
                raise OSError("injected: simulated crash on store move 2")
        return real_move(source, destination, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(specify_cli.shutil, "move", crashing_move)
        first = _json_payload(_apply(workspace), 3)

    assert first["outcome"] == "blocked"
    assert injected["storeMoves"] == 2, "the injected crash never fired on a store move"
    interrupted = _receipt_payloads(workspace)
    assert len(interrupted) == 1
    interrupted = interrupted[0]
    assert interrupted["status"] == "aborted"
    assert interrupted["resumedFrom"] is None

    resumed = _json_payload(_apply(workspace), 0)

    assert resumed["outcome"] == "applied"
    assert not retired.exists(), "the resume did not converge the retired container"
    completing = [
        receipt
        for receipt in _receipt_payloads(workspace)
        if receipt["status"] == "completed"
    ]
    assert len(completing) == 1
    completing = completing[0]
    assert completing["resumedFrom"] == interrupted["runId"]
    interrupted_file = _receipts(workspace)[0]
    interrupted_bytes = interrupted_file.read_bytes()

    # A run's own receipt is transaction bookkeeping inside the `migrate` store,
    # not store content (same exclusion as the US2 byte-identity test).
    def content_files(name):
        return {
            rel: digest
            for rel, digest in _store_files(workspace / ".specify" / name).items()
            if not rel.startswith("receipts/")
        }

    store_files_before = {
        name: content_files(name) for name in builders.store_names()
    }

    third = _json_payload(_apply(workspace), 0)

    assert third["outcome"] == "clean", (
        "a completed run that resumed the interrupted receipt must supersede it; "
        "the third apply replayed the stale receipt instead of seeing convergence"
    )
    assert third["items"] == []
    assert third["summary"]["total"] == 0
    receipts = _receipts(workspace)
    assert len(receipts) == 3
    third_receipt = next(
        receipt
        for receipt in _receipt_payloads(workspace)
        if receipt["runId"] not in {interrupted["runId"], completing["runId"]}
    )
    assert third_receipt["status"] == "completed"
    assert third_receipt["resumedFrom"] is None
    assert third_receipt["items"] == []
    assert third_receipt["archives"] == []
    assert interrupted_file.read_bytes() == interrupted_bytes, (
        "supersession is read-only; the interrupted receipt was rewritten"
    )
    for name in builders.store_names():
        assert content_files(name) == store_files_before[name], (
            f"the third apply moved bytes in store {name!r}"
        )
