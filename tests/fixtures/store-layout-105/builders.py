"""Declaration-driven migration fixtures for feature 105 (``store-layout`` dimension).

Every store name, non-content pattern and the retired-container name are read
from ``shared/declarations/facts/runtime-store-layout.yaml`` through the CLI's
own reader (``specify_cli.store_layout``). A declaration that stops describing a
store makes the builder raise, never silently build a stale fixture
(FR-023 / F-3 of ``contracts/migrate-store-layout.contract.md`` M-8).

Entry points:

* ``build_legacy``        — new-layout shell, every declared store populated under
  the retired container (authoritative entry + ``.gitkeep`` + one generated
  artifact where the store declares one); no ``.specify/<store>`` roots.
* ``build_seeded_legacy`` — ``build_legacy`` after ``specify init`` runs over it
  (anchors at the root, seeded memory tiers, a tools inventory JSON) — the A-7
  clarification case where new-side content exists but is not authoritative.
* ``build_dual``          — ``build_legacy`` plus authoritative content under both
  roots of one store (the refusal case).
* ``build_rerun``         — ``build_legacy`` after one successful ``--apply``
  (the idempotent-rerun case).
* ``build_residue``       — ``build_legacy`` plus the legacy ``draft/`` directory and
  a stray ``git-workflow.md`` under the retired container (the unknown-residue case).
* ``build_symlink``       — ``build_legacy`` with one store's legacy path replaced by a
  symbolic link to a sibling directory (the symlink refusal case).
* ``build_readonly``      — ``build_legacy`` with one store's target root pre-created
  read-only (the permission-denied case; a root-run test records the platform fact
  and skips — process privileges bypass the directory mode).
* ``build_partial``       — ``build_legacy`` after an interrupted ``--apply``: a
  ``running`` receipt whose manifest records half the entries as moved, with exactly
  those bytes physically relocated (the resume case, M-6).
"""

import contextlib
import io
import json
import os
import shutil
from pathlib import Path

import specify_cli

DEFAULT_ASSISTANT = "qoder"
DEFAULT_SCRIPT_VARIANT = "sh"
AUTHORITATIVE_NAME = "entry.md"

__all__ = [
    "AUTHORITATIVE_NAME",
    "build_dual",
    "build_legacy",
    "build_partial",
    "build_readonly",
    "build_rerun",
    "build_residue",
    "build_seeded_legacy",
    "build_symlink",
    "generated_name",
    "retired_rel",
    "store_names",
    "store_roster",
]


def _statement():
    statement, label = specify_cli.store_layout()
    if label:
        raise RuntimeError(f"store layout declaration unreadable: {label}")
    if not isinstance(statement.get("stores"), dict) or not statement["stores"]:
        raise RuntimeError("store layout declaration carries no store roster")
    return statement


def store_roster() -> dict:
    """`name -> declaration entry`, exactly as the machine owner declares it."""
    return dict(_statement()["stores"])


def store_names() -> tuple:
    return tuple(sorted(store_roster()))


def retired_rel() -> str:
    """The retired container path as the declaration spells it (never a code literal)."""
    retired = _statement().get("retired_container")
    if not isinstance(retired, str) or not retired:
        raise RuntimeError("store layout declaration carries no retired_container")
    return retired


def generated_name(store_entry: dict):
    """One concrete file name for the store's first declared non-content glob."""
    patterns = [
        pattern
        for pattern in (store_entry.get("non_content") or [])
        if isinstance(pattern, str) and pattern
    ]
    if not patterns:
        return None
    return patterns[0].replace("*", "project")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_legacy(dest) -> Path:
    """The new-layout shell mutated back into the pre-105 store layout."""
    dest = Path(dest)
    specify_cli.copy_local_templates(
        dest, DEFAULT_ASSISTANT, DEFAULT_SCRIPT_VARIANT, is_current_dir=False
    )
    specify = dest / ".specify"
    retired = specify / Path(retired_rel()).name
    roster = store_roster()
    for name, entry in sorted(roster.items()):
        new_root = specify / name
        old_root = retired / name
        old_root.mkdir(parents=True, exist_ok=True)
        if new_root.is_dir():
            for path in sorted(new_root.rglob("*")):
                if path.is_dir() and not path.is_symlink():
                    continue
                rel = path.relative_to(new_root)
                target = old_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path), str(target))
            shutil.rmtree(new_root)
        _write(old_root / AUTHORITATIVE_NAME, f"# {name} authoritative entry\n")
        _write(old_root / ".gitkeep", "")
        generated = generated_name(entry)
        if generated:
            _write(old_root / generated, f"{name} generated artifact\n")
    for name in roster:
        if (specify / name).exists():
            raise AssertionError(
                f"legacy fixture still carries a new-layout root: .specify/{name}"
            )
    if not retired.is_dir():
        raise AssertionError("legacy fixture did not create the retired container")
    return dest


def build_seeded_legacy(dest) -> Path:
    """`build_legacy` after `specify init` runs over the legacy workspace."""
    dest = build_legacy(dest)
    specify_cli.copy_local_templates(
        dest, DEFAULT_ASSISTANT, DEFAULT_SCRIPT_VARIANT, is_current_dir=False
    )
    specify = dest / ".specify"
    for name in specify_cli.seeded_store_names(_statement()):
        if not (specify / name / ".gitkeep").is_file():
            raise AssertionError(f"init did not seed the declared memory tier {name!r}")
    _write(specify / "tools" / "project.json", json.dumps({"tools": []}) + "\n")
    return dest


def build_dual(dest, store: str = "feedback") -> Path:
    """`build_legacy` plus authoritative content on both sides of one store."""
    dest = build_legacy(dest)
    roster = store_roster()
    if store not in roster:
        raise AssertionError(f"{store!r} is not a declared store")
    _write(dest / ".specify" / store / AUTHORITATIVE_NAME, "# new-side authoritative entry\n")
    return dest


def build_rerun(dest) -> Path:
    """`build_legacy` after one successful `specify migrate --apply`."""
    dest = build_legacy(dest)
    with contextlib.redirect_stdout(io.StringIO()):
        exit_code = specify_cli._run_migrate(dest, apply_mode=True, output_format="json")
    if exit_code != 0:
        raise RuntimeError(f"fixture apply failed with exit {exit_code}")
    if (dest / retired_rel()).exists():
        raise RuntimeError("fixture apply left the retired container in place")
    return dest


def _dry_run_payload(dest) -> dict:
    """The plan a dry-run serializes for this workspace (zero writes, M-2)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exit_code = specify_cli._run_migrate(dest, apply_mode=False, output_format="json")
    if exit_code not in (0, 1):
        raise RuntimeError(f"fixture dry-run failed with exit {exit_code}")
    return json.loads(buffer.getvalue())


def build_residue(dest) -> Path:
    """`build_legacy` plus the two legacy non-store members (unknown residue)."""
    dest = build_legacy(dest)
    retired = dest / retired_rel()
    _write(retired / "draft" / "parked-idea.md", "# parked legacy idea (no new home)\n")
    _write(retired / "git-workflow.md", "# legacy git workflow (superseded)\n")
    return dest


def build_symlink(dest, store: str = "feedback") -> Path:
    """`build_legacy` with one store's legacy path replaced by a symbolic link."""
    dest = build_legacy(dest)
    if store not in store_roster():
        raise AssertionError(f"{store!r} is not a declared store")
    retired = dest / retired_rel()
    sibling = dest / "sibling-content" / store
    sibling.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(retired / store), str(sibling))
    os.symlink(os.path.relpath(sibling, retired), retired / store)
    if not (retired / store).is_symlink():
        raise AssertionError("symlink fixture did not create the store link")
    return dest


def build_readonly(dest, store: str = "feedback") -> Path:
    """`build_legacy` with one store's target root pre-created read-only.

    The target root is the parent directory of every relocated entry, so the
    planner's writability probe and the executor's re-check both refuse it (M-2
    rule 8). Running as root makes `os.access` answer writable regardless of the
    mode; the caller records that platform fact and skips the refusal reading.
    """
    dest = build_legacy(dest)
    if store not in store_roster():
        raise AssertionError(f"{store!r} is not a declared store")
    target = dest / ".specify" / store
    target.mkdir(parents=True, exist_ok=True)
    target.chmod(0o555)
    return dest


def build_partial(dest) -> Path:
    """`build_legacy` after an interrupted `--apply` (a `running` receipt, half moved).

    The fixture takes the real dry-run plan, physically relocates the upper half
    of every store item's entries (so each store has moved and remaining rows),
    flips exactly those rows to ``status=moved`` with the planned digests, and
    lands the plan in a ``running`` receipt — the resume oracle of M-6. The
    interrupted receipt's ``archives[]`` stays empty: an interruption persists
    only manifest snapshots, so the completing run owns the archive record.
    """
    dest = build_legacy(dest)
    payload = _dry_run_payload(dest)
    items = [
        item for item in payload["items"] if item["dimension"] == "store-layout"
    ]
    store_items = [item for item in items if item["target"] != retired_rel()]
    if not store_items:
        raise RuntimeError("partial fixture: the dry-run planned no store items")
    for item in store_items:
        rows = item.get("entries") or []
        for row in rows[len(rows) // 2:]:
            from_path = dest / row["from"]
            to_path = dest / row["to"]
            to_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(from_path), str(to_path))
            row["status"] = "moved"
        item["status"] = "planned"
    run_id, receipt_path = specify_cli.create_migrate_receipt(dest)
    specify_cli.update_migrate_receipt(receipt_path, items=items)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "running":
        raise AssertionError("partial fixture receipt is not in the running state")
    moved = [
        row
        for item in store_items
        for row in item.get("entries") or []
        if row.get("status") == "moved"
    ]
    if not moved:
        raise AssertionError("partial fixture moved no entries")
    return dest
