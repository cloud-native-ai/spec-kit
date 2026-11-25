"""Integration: US6 store-layout failure surfaces — residue / symlink / readonly /
partial (105 T035).

Green claims: ``contracts/migrate-store-layout.contract.md`` M-2 (rules 1, 8, 9),
M-4 (steps 2, 5, 6), M-5 (the closed refusal table), M-6 (receipt and resume),
M-8 (the four failure fixtures) and ``plan.md`` § Test-First Coverage SC-009.

This module is a migration/regression exception (tasks.md § Tests Mode): the
executor behaviour it guards was delivered by T014, so the red ability is proven
by the T036 mutation drills recorded in ``test-evidence/mutation-drill.md``, not
by a red-first authoring pass.

Mutation pairing for every assertion group (M-8: each reading MUST have a
red-ability drill):

* residue — cancelling the ``unknown-residue`` enumeration (the planner's
  "unclaimed members" branch and the executor's container pass) makes the
  outcome ``applied`` and removes the path listing, so
  ``test_residue_...`` turns red on the outcome and on every listed path.
* dual content (US2 assertion, same drill owner) — deleting the planner's
  ``old_authoritative and new_authoritative`` conflict check turns the US2
  dual-content refusal into a path-collision refusal, so that assertion turns
  red on its named reason.
* partial — treating a resume row as a fresh move (ignoring
  ``status=moved`` and re-moving or re-archiving it) makes the duplicate-entry
  and single-archive-record assertions red.
* symlink / readonly — the refusal classes come from M-2 rules 1 and 8; their
  guards are the ``disposition == "refuse"`` and named-path assertions below.

Fixtures come from ``tests/fixtures/store-layout-105/builders.py`` and are
declaration-driven; nothing here carries a second store roster or a store-name
literal beyond the baseline directories the migration contract itself names.
"""

import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "store-layout-105" / "builders.py"


def _retired_container() -> str:
    """The retired container path, derived from the declaration (never a test literal)."""
    statement, label = specify_cli.store_layout()
    assert not label, f"store layout declaration unreadable: {label}"
    retired = (statement or {}).get("retired_container")
    assert isinstance(retired, str) and retired, "declaration carries no retired_container"
    return retired.rstrip("/")


CONTAINER = _retired_container()


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


def _apply(workspace):
    return _invoke(
        ["migrate", "--workspace", str(workspace), "--apply", "--format", "json"]
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _store_files(root: Path) -> dict:
    """`relpath -> sha256` for every file under a store tree (dirs excluded)."""
    files = {}
    if not root.is_dir():
        return files
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            files[path.relative_to(root).as_posix()] = _sha256(path)
    return files


def _store_items(payload):
    return [
        item for item in payload["items"] if item["dimension"] == "store-layout"
    ]


def _store_targets(payload):
    return [
        item
        for item in _store_items(payload)
        if item["target"] != CONTAINER
    ]


def _container_item(payload):
    return next(
        item for item in _store_items(payload) if item["target"] == CONTAINER
    )


def _receipts(workspace: Path):
    return sorted(specify_cli.migrate_receipts_dir(workspace).glob("*.json"))


def _receipt_payloads(workspace: Path):
    return [
        json.loads(path.read_text(encoding="utf-8")) for path in _receipts(workspace)
    ]


# ---------------------------------------------------------------------------
# Residue — unknown members are listed and preserved, never deleted (M-2 r9)
# ---------------------------------------------------------------------------


def test_residue_lists_every_remaining_path_and_deletes_nothing(tmp_path):
    builders = _builders()
    workspace = builders.build_residue(tmp_path / "residue")
    roster = builders.store_names()
    residue_files = {
        "draft/parked-idea.md": _sha256(
            workspace / CONTAINER / "draft" / "parked-idea.md"
        ),
        "git-workflow.md": _sha256(workspace / CONTAINER / "git-workflow.md"),
    }

    payload = _json_payload(_apply(workspace), 3)

    assert payload["outcome"] == "blocked"
    assert payload["exitCode"] == 3
    store_items = _store_targets(payload)
    assert len(store_items) == len(roster)
    assert all(
        item["status"] == "done" and item["disposition"] == "archive"
        for item in store_items
    ), "every declared store must converge before the container pass reports residue"
    for name in roster:
        assert (workspace / ".specify" / name).is_dir()
        assert not (workspace / CONTAINER / name).exists()

    container = _container_item(payload)
    assert container["disposition"] == "refuse"
    assert container["status"] == "refused"
    assert container["current"] == "unknown-residue"
    reason = container["reason"]
    assert "unknown-residue" in reason
    for relpath in (
        f"{CONTAINER}/draft/",
        f"{CONTAINER}/draft/parked-idea.md",
        f"{CONTAINER}/git-workflow.md",
    ):
        assert relpath in reason, f"the residue listing omits {relpath!r}"

    # Zero deletion: the container and every residue byte survive unchanged.
    assert (workspace / CONTAINER).is_dir()
    for relpath, digest in residue_files.items():
        survived = workspace / CONTAINER / relpath
        assert survived.is_file(), f"the residue {relpath!r} was deleted"
        assert _sha256(survived) == digest, f"the residue {relpath!r} was rewritten"


# ---------------------------------------------------------------------------
# Symlink — refuse, name the path, never follow, never unlink (M-2 r1 / M-5)
# ---------------------------------------------------------------------------


def test_symlink_refuses_naming_the_path_and_leaves_the_link(tmp_path):
    builders = _builders()
    workspace = builders.build_symlink(tmp_path / "symlink", store="feedback")
    link = workspace / CONTAINER / "feedback"
    link_target = os.readlink(link)
    sibling_files = _store_files(workspace / "sibling-content" / "feedback")
    assert sibling_files

    payload = _json_payload(_apply(workspace), 3)

    assert payload["outcome"] == "blocked"
    item = next(
        item
        for item in _store_targets(payload)
        if item["target"] == ".specify/feedback"
    )
    assert item["disposition"] == "refuse"
    assert item["status"] == "refused"
    assert item["current"] == "symlink"
    assert "symlink-source" in item["reason"]
    assert f"{CONTAINER}/feedback" in item["reason"]

    # The link is untouched and was never followed into the sibling tree.
    assert link.is_symlink()
    assert os.readlink(link) == link_target
    assert not (workspace / ".specify" / "feedback").exists()
    assert _store_files(workspace / "sibling-content" / "feedback") == sibling_files

    # Other stores still converge; the container is preserved for the refused one.
    session_item = next(
        item
        for item in _store_targets(payload)
        if item["target"] == ".specify/session"
    )
    assert session_item["status"] == "done"
    assert (workspace / ".specify" / "session" / "entry.md").is_file()
    assert not (workspace / CONTAINER / "session").exists()
    assert (workspace / CONTAINER).is_dir()


# ---------------------------------------------------------------------------
# Readonly — permission-denied, named path, no partial success (M-2 r8 / M-5)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.geteuid() == 0,
    reason=(
        "platform fact: running as root bypasses directory modes, so os.access "
        "answers writable and the fixture cannot exhibit a permission refusal"
    ),
)
def test_readonly_target_refuses_permission_denied_without_partial_success(tmp_path):
    builders = _builders()
    workspace = builders.build_readonly(tmp_path / "readonly", store="feedback")
    old_root = workspace / CONTAINER / "feedback"
    target_root = workspace / ".specify" / "feedback"
    old_before = _store_files(old_root)
    assert old_before

    try:
        payload = _json_payload(_apply(workspace), 3)

        assert payload["outcome"] == "blocked"
        item = next(
            item
            for item in _store_targets(payload)
            if item["target"] == ".specify/feedback"
        )
        assert item["disposition"] == "refuse"
        assert item["status"] == "refused"
        assert item["current"] == "unreadable"
        assert "permission-denied" in item["reason"]
        assert f"{CONTAINER}/feedback" in item["reason"]
        assert ".specify/feedback" in item["reason"]

        # No partial success: the refused store did not move a single byte.
        assert _store_files(old_root) == old_before
        assert target_root.is_dir()
        assert _store_files(target_root) == {}

        # The writable stores still converge; the container keeps the refused store.
        session_item = next(
            item
            for item in _store_targets(payload)
            if item["target"] == ".specify/session"
        )
        assert session_item["status"] == "done"
        assert (workspace / ".specify" / "session" / "entry.md").is_file()
        assert (workspace / CONTAINER).is_dir()
        container = _container_item(payload)
        assert container["status"] == "refused"
        assert "unknown-residue" in container["reason"]
        assert f"{CONTAINER}/feedback/" in container["reason"]
    finally:
        target_root.chmod(0o755)


# ---------------------------------------------------------------------------
# Partial — resume moves only the remainder, once, with one archive record (M-6)
# ---------------------------------------------------------------------------


def test_partial_resume_moves_only_the_remainder_with_one_archive_record(tmp_path):
    builders = _builders()
    workspace = builders.build_partial(tmp_path / "partial")
    roster = builders.store_names()
    receipts_before = _receipts(workspace)
    assert len(receipts_before) == 1
    interrupted_path = receipts_before[0]
    interrupted_bytes = interrupted_path.read_bytes()
    interrupted = json.loads(interrupted_bytes.decode("utf-8"))
    assert interrupted["status"] == "running"
    assert interrupted["archives"] == []
    moved_rows = [
        (item["target"], row)
        for item in interrupted["items"]
        if item["dimension"] == "store-layout"
        and item["target"] != CONTAINER
        for row in item.get("entries") or []
        if row["status"] == "moved"
    ]
    assert moved_rows, "the fixture must record moved entries in its running receipt"
    moved_before = {
        row["to"]: _sha256(workspace / row["to"]) for _target, row in moved_rows
    }

    payload = _json_payload(_apply(workspace), 0)

    assert payload["outcome"] == "applied"
    assert payload["exitCode"] == 0
    store_items = _store_targets(payload)
    assert len(store_items) == len(roster)
    assert all(item["status"] == "done" for item in store_items)
    for name in roster:
        assert (workspace / ".specify" / name).is_dir()
        assert not (workspace / CONTAINER / name).exists()
    assert not (workspace / CONTAINER).exists(), (
        "the container survived a fully converged resume"
    )

    # The previously moved entries were verified in place, never moved twice and
    # never rewritten (the raw pre-apply bytes are the independent oracle).
    verified_digests = set()
    for target, row in moved_rows:
        moved_to = workspace / row["to"]
        assert moved_to.is_file(), f"resume lost {row['to']!r}"
        assert _sha256(moved_to) == moved_before[row["to"]], (
            f"resume changed the bytes of {row['to']!r}"
        )
        assert not (workspace / row["from"]).exists()
        verified_digests.add(row["digest"])

    receipts = _receipt_payloads(workspace)
    assert len(receipts) == 2, "each run lands exactly one receipt file"
    assert len({receipt["runId"] for receipt in receipts}) == 2
    assert interrupted_path.read_bytes() == interrupted_bytes, (
        "the interrupted receipt is a read-only resume input; it was rewritten"
    )
    completed = next(receipt for receipt in receipts if receipt["status"] == "completed")
    assert completed["outcome"] == "applied"

    for item in completed["items"]:
        if item["dimension"] != "store-layout" or item["target"] == CONTAINER:
            continue
        rows = item.get("entries") or []
        relpaths = [row["relpath"] for row in rows]
        assert len(relpaths) == len(set(relpaths)), (
            f"{item['target']}: the resume duplicated an entry row"
        )
        assert all(row["status"] == "moved" for row in rows), rows

    archived = [entry["path"] for entry in completed["archives"]]
    assert len(archived) == len(set(archived)), (
        "the completing run recorded an object twice"
    )
    archived_paths = {
        entry["path"]: entry for entry in completed["archives"]
    }
    for _target, row in moved_rows:
        assert row["from"] in archived_paths, (
            f"the moved entry {row['from']!r} has no archive record in the completing run"
        )
    assert verified_digests <= {entry["digest"] for entry in completed["archives"]}
    assert len(completed["recover"]) == len(completed["archives"])
    assert all(
        not entry["archiveTo"].startswith(".specify/archive/")
        for entry in completed["archives"]
    ), "a pure relocation copied bytes into the archive root"
    assert not (workspace / ".specify" / "archive" / "migrate").exists()
