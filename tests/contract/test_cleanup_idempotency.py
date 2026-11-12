"""G-7a (T068) — a second cleanup apply changes nothing, and receipts must agree with the tree.

The executable subject is `goal-utils.py cleanup --apply` run twice over a scratch copy of the
pre-convergence fixture. Red conditions, each injected below: a second apply rewrites any byte
or adds a receipt; two receipts claim the same target; a receipt's recorded concept digest no
longer matches the definition it names; a receipt lists a Target that the definition's table no
longer carries.

The three receipt predicates are pure functions over the post-apply tree, so each injection is
a small mutation of a converged copy rather than a weakened assertion.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from script_api import load_engine_module

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
FIXTURE = ROOT / "tests/fixtures/anchor-goal-realignment"
ENGINE = ROOT / "scripts/python/goal-utils.py"

MIGRATION_SCHEMA = "101-migration-receipt/v1"
DISPOSITION_SCHEMA = "101-disposition-receipt/v1"


# ---- scratch tree ----------------------------------------------------------

def _scratch(target: Path) -> Path:
    """A committed copy of the fixture tree: the classification's `HEAD` must resolve."""
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


def _apply(root: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(ENGINE), "cleanup", "--apply", "--repo-root", str(root),
         "--classification", str(root / "classification.json"), "--json"],
        cwd=str(root), capture_output=True, text=True, check=False)
    payload = json.loads(result.stdout or "{}")
    assert result.returncode == 0, (result.returncode, result.stderr, payload)
    assert payload.get("verdict") == "ok", payload
    return payload


def _manifest(root: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or rel == ".git" or rel == "classification.json":
            continue
        if path.is_file() and "__pycache__" not in rel:
            manifest[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


# ---- receipt predicates ----------------------------------------------------

def _receipts(root: Path) -> list[tuple[str, dict]]:
    rows: list[tuple[str, dict]] = []
    for path in sorted(root.rglob("*.json")):
        rel = path.relative_to(root).as_posix()
        if not rel.startswith(".specify/"):
            continue
        if not path.name.endswith(("migration-receipt.json", "disposition-receipt.json",
                                   "anchor-body-receipt.json", "binding-rename-receipt.json")):
            continue
        rows.append((rel, json.loads(path.read_text(encoding="utf-8"))))
    return rows


def _duplicate_target_claims(root: Path) -> list[str]:
    """Two receipts naming the same (schema, target_path): one move, claimed twice."""
    seen: dict[tuple[str, str], str] = {}
    problems: list[str] = []
    for rel, body in _receipts(root):
        key = (str(body.get("schema")), str(body.get("target_path")))
        if key[1] == "None":
            continue
        if key in seen:
            problems.append(f"{key[1]} claimed by {seen[key]} and {rel}")
        else:
            seen[key] = rel
    return problems


def _digest_mismatches(root: Path) -> list[str]:
    """A migration receipt's target digest must equal the digest the engine recomputes."""
    engine = load_engine_module(ENGINE)
    problems: list[str] = []
    for rel, body in _receipts(root):
        if body.get("schema") != MIGRATION_SCHEMA:
            continue
        target = root / body["target_path"]
        if not target.is_file():
            problems.append(f"{rel}: target {body['target_path']} is absent")
            continue
        mapping = "obsolete" if body.get("action") == "archive-obsolete" else "action-goal"
        recomputed = engine.migration_digest(target.read_text(encoding="utf-8"),
                                             mapping=mapping)
        if recomputed != body.get("concept_digest_target"):
            problems.append(f"{rel}: {body['target_path']} digests {recomputed}, "
                            f"receipt records {body.get('concept_digest_target')}")
        if body.get("concept_digest_source") != body.get("concept_digest_target"):
            problems.append(f"{rel}: source and target digests differ, yet the source is gone")
    return problems


def _migrated_targets(text: str) -> list[str]:
    """The `## Migrated Targets` bullets, in order — where a moved Target table lands."""
    statements: list[str] = []
    inside = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## Migrated Targets":
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and stripped.startswith("- "):
            statements.append(stripped[2:].strip())
    return statements


def _table_targets(text: str) -> list[str]:
    """The `## Targets` table statements — how an archived (copied, unmapped) body keeps them."""
    statements: list[str] = []
    inside = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## Targets":
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            match = re.match(r"^\|\s*(T-\d{3})\s*\|\s*(.+?)\s*\|\s*(open|done|dropped)\s*\|$",
                             stripped)
            if match:
                statements.append(match.group(2))
    return statements


def _target_mismatches(root: Path) -> list[str]:
    """A receipt's `targets[]` must equal the Target statements its definition still carries.

    An `action-goal` migration re-renders the table as `## Migrated Targets` bullets; an
    `obsolete` archive copies the tree whole, so its table survives in place. The predicate
    reads the form the matching action is contracted to leave behind.
    """
    problems: list[str] = []
    for rel, body in _receipts(root):
        if body.get("schema") != MIGRATION_SCHEMA:
            continue
        target = root / body["target_path"]
        if not target.is_file():
            continue
        text = target.read_text(encoding="utf-8")
        carried = (_table_targets(text) if body.get("action") == "archive-obsolete"
                   else _migrated_targets(text))
        recorded = [str(row.get("statement")) for row in body.get("targets") or []]
        if carried != recorded:
            problems.append(f"{rel}: receipt lists {recorded!r}, "
                            f"{body['target_path']} carries {carried!r}")
    return problems


# ---- the converge-once fixture --------------------------------------------

@pytest.fixture(scope="module")
def converged(tmp_path_factory) -> Path:
    root = _scratch(tmp_path_factory.mktemp("idempotency"))
    _apply(root)
    return root


@pytest.fixture()
def copy_of_converged(converged, tmp_path) -> Path:
    root = tmp_path / "copy"
    shutil.copytree(converged, root)
    return root


# ---- tests -----------------------------------------------------------------

def test_second_apply_is_a_byte_level_no_op(converged):
    before = _manifest(converged)
    receipts_before = [rel for rel, _ in _receipts(converged)]
    assert len(receipts_before) == len(set(receipts_before)), "a receipt was duplicated already"

    payload = _apply(converged)

    assert _manifest(converged) == before, "the second apply rewrote a path it had settled"
    assert [rel for rel, _ in _receipts(converged)] == receipts_before, \
        "the second apply added a receipt"


def test_converged_receipts_agree_with_the_tree(converged):
    assert _duplicate_target_claims(converged) == []
    assert _digest_mismatches(converged) == []
    assert _target_mismatches(converged) == []


def test_a_duplicate_receipt_turns_the_guard_red(converged, copy_of_converged):
    source = sorted(copy_of_converged.rglob("migration-receipt.json"))[0]
    clone = source.parent.parent / "migration-receipt.json"
    shutil.copy2(source, clone)

    problems = _duplicate_target_claims(copy_of_converged)
    assert problems, "a second receipt for the same target went unnoticed"
    assert source.relative_to(copy_of_converged).as_posix() in problems[0]


def test_a_mismatched_digest_turns_the_guard_red(copy_of_converged):
    receipt = next(path for path in sorted(copy_of_converged.rglob("migration-receipt.json")))
    body = json.loads(receipt.read_text(encoding="utf-8"))
    target = copy_of_converged / body["target_path"]
    target.write_text(target.read_text(encoding="utf-8").replace(
        "## Objective", "## Objective\n\nInjected concept drift.", 1), encoding="utf-8")

    problems = _digest_mismatches(copy_of_converged)
    assert problems, "a definition whose concept payload moved went unnoticed"


def test_a_dropped_target_turns_the_guard_red(copy_of_converged):
    receipt = next(path for path in sorted(copy_of_converged.rglob("migration-receipt.json"))
                   if (lambda b: b.get("action") == "migrate-action-goal" and b.get("targets"))(
                       json.loads(path.read_text(encoding="utf-8"))))
    body = json.loads(receipt.read_text(encoding="utf-8"))
    target = copy_of_converged / body["target_path"]
    dropped = body["targets"][0]["statement"]
    kept = [line for line in target.read_text(encoding="utf-8").splitlines()
            if line.strip() != f"- {dropped}"]
    target.write_text("\n".join(kept) + "\n", encoding="utf-8")

    problems = _target_mismatches(copy_of_converged)
    assert problems, "a receipt claimed a Target the definition no longer carries"
