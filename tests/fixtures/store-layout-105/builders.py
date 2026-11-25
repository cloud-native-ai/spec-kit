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
"""

import contextlib
import io
import json
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
    "build_rerun",
    "build_seeded_legacy",
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
