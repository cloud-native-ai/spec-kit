"""G-3 (T064) — the Anchor store holds Anchor definitions and nothing else.

Red when any Anchor-store entry is missing its `anchor.md`, when an entry still carries a
`goal.md` (the retired file name), or when a slug the classification calls `action-goal` /
`obsolete` is still present in the Anchor store. The same predicate runs against the
pre-convergence fixture tree, where every one of those defects exists by construction — a
guard that cannot see them there cannot see them on a live tree either.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
CLASSIFICATION = ROOT / ".specify/specs/101-anchor-goal-realignment/classification.json"
FIXTURE = REPO_ROOT / "tests/fixtures/anchor-goal-realignment"
FIXTURE_CLASSIFICATION = FIXTURE / "classification/classification.json"
FIXTURE_TREE = FIXTURE / "pre-convergence"
ANCHOR_STORE = ".specify/anchoring"


def _load(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def anchor_store_slugs(root: Path) -> list[str]:
    base = Path(root) / ANCHOR_STORE
    if not base.is_dir():
        return []
    return sorted(child.name for child in base.iterdir() if child.is_dir())


def expected_anchor_slugs(classification: dict) -> set[str]:
    """The slugs the Anchor store must hold after convergence, from the classification alone."""
    slugs = {row["slug"] for row in classification["entries"] if row["class"] == "anchor"}
    slugs |= {row["bound_slug"] for row in classification.get("teams", [])
              if row.get("state") == "apply" and row.get("disposition") == "R2"}
    return slugs


def anchor_store_problems(root: Path, classification: dict) -> list[str]:
    root = Path(root)
    problems: list[str] = []
    present = anchor_store_slugs(root)
    for slug in present:
        entry = root / ANCHOR_STORE / slug
        if not (entry / "anchor.md").is_file():
            problems.append(f"{ANCHOR_STORE}/{slug}: no anchor.md")
        if (entry / "goal.md").exists():
            problems.append(f"{ANCHOR_STORE}/{slug}: goal.md still present")
    expected = expected_anchor_slugs(classification)
    for slug in sorted(expected - set(present)):
        problems.append(f"{ANCHOR_STORE}/{slug}: expected anchor entry is absent")
    retired = {row["slug"] for row in classification["entries"] if row["class"] != "anchor"}
    for slug in sorted(retired & set(present)):
        problems.append(f"{ANCHOR_STORE}/{slug}: classified {_class_of(classification, slug)}, still in the Anchor store")
    return problems


def _class_of(classification: dict, slug: str) -> str:
    return next(row["class"] for row in classification["entries"] if row["slug"] == slug)


def test_live_anchor_store_is_converged() -> None:
    problems = anchor_store_problems(ROOT, _load(CLASSIFICATION))
    assert not problems, problems


def test_live_anchor_store_holds_exactly_the_declared_slugs() -> None:
    classification = _load(CLASSIFICATION)
    assert set(anchor_store_slugs(ROOT)) == expected_anchor_slugs(classification)


def test_every_anchor_definition_is_non_empty_and_titled() -> None:
    for slug in anchor_store_slugs(ROOT):
        text = (ROOT / ANCHOR_STORE / slug / "anchor.md").read_text(encoding="utf-8")
        assert text.strip(), f"{slug}: anchor.md is empty"
        assert text.lstrip().startswith("---"), f"{slug}: anchor.md has no frontmatter"


def test_fixture_tree_exposes_every_defect_the_guard_looks_for() -> None:
    problems = anchor_store_problems(FIXTURE_TREE, _load(FIXTURE_CLASSIFICATION))
    joined = "\n".join(problems)
    assert f"{ANCHOR_STORE}/088-speckit-visualization: goal.md still present" in joined
    assert f"{ANCHOR_STORE}/086-efficient-test-execution: no anchor.md" in joined
    assert "classified action-goal, still in the Anchor store" in joined
    assert "classified obsolete, still in the Anchor store" in joined
    assert len(problems) > 20


def test_injection_missing_definition_file_is_red(tmp_path: Path) -> None:
    classification = _load(FIXTURE_CLASSIFICATION)
    root = tmp_path / "tree"
    (root / ANCHOR_STORE / "086-efficient-test-execution").mkdir(parents=True)
    (root / ANCHOR_STORE / "086-efficient-test-execution" / "anchor.md").write_text("---\n---\n", encoding="utf-8")
    (root / ANCHOR_STORE / "088-speckit-visualization" / "goal.md").parent.mkdir(parents=True)
    (root / ANCHOR_STORE / "088-speckit-visualization" / "goal.md").write_text("# Goal:\n", encoding="utf-8")
    problems = anchor_store_problems(root, classification)
    assert f"{ANCHOR_STORE}/088-speckit-visualization: goal.md still present" in problems
    assert f"{ANCHOR_STORE}/088-speckit-visualization: no anchor.md" in problems
