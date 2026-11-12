"""G-5 (T066) — the binding rename: `goal_slug` is gone, every `anchor_slug` resolves.

Scope is every live team definition under `.specify/teams/` (frontmatter or body, archived
included), with `runs/**` excluded — dated run records are not definitions. The disposition set
comes from the feature's classification, never from `lifecycle_state`, because an archived team
may legitimately keep a resolvable binding (087 does) while an R3 disposition must have lost it.

Resolution is by slug presence in the Anchor store (either definition filename); the filename
contract itself belongs to G-3, so a renamed-away `anchor.md` is reported there, not twice here.

Red conditions, each exercised on the pre-convergence fixture tree: an old binding key survives,
a binding does not resolve, an applied disposition has no receipt, or a dangling binding is left
unresolved.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
CLASSIFICATION = ROOT / ".specify/specs/101-anchor-goal-realignment/classification.json"
FIXTURE = REPO_ROOT / "tests/fixtures/anchor-goal-realignment"
FIXTURE_CLASSIFICATION = FIXTURE / "classification/classification.json"
FIXTURE_TREE = FIXTURE / "pre-convergence"

TEAMS_DIR = ".specify/teams"
ANCHORS_DIR = ".specify/anchoring"
OLD_KEY = "goal_slug"
NEW_KEY = "anchor_slug"
DEFINITION_FILES = ("anchor.md", "goal.md")
EXCLUDED_PARTS = {"runs", "__pycache__"}


def _load(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def team_files(root: Path) -> list[Path]:
    base = Path(root) / TEAMS_DIR
    if not base.is_dir():
        return []
    return sorted(path for path in base.rglob("team.md")
                  if not (set(path.relative_to(base).parts) & EXCLUDED_PARTS))


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def binding_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{key}:\s*(\S+)\s*$", frontmatter(text))
    return match.group(1) if match else None


def lifecycle(text: str) -> str | None:
    match = re.search(r"(?m)^lifecycle_state:\s*(\S+)\s*$", frontmatter(text))
    return match.group(1) if match else None


def resolves(root: Path, slug: str) -> bool:
    entry = Path(root) / ANCHORS_DIR / slug
    return any((entry / name).is_file() for name in DEFINITION_FILES)


def binding_problems(root: Path, classification: dict) -> list[str]:
    root = Path(root)
    problems: list[str] = []
    rows = {row["slug"]: row for row in classification.get("teams", [])}
    seen: set[str] = set()
    for path in team_files(root):
        rel = str(path.relative_to(root))
        slug = path.parent.name
        seen.add(slug)
        text = path.read_text(encoding="utf-8")
        if OLD_KEY in text:
            problems.append(f"{rel}: still carries {OLD_KEY}")
        binding = binding_value(text, NEW_KEY)
        if binding and not resolves(root, binding):
            problems.append(f"{rel}: {NEW_KEY} {binding!r} does not resolve")
        row = rows.get(slug)
        if row is None:
            continue
        if row.get("disposition") == "R3":
            if binding is not None:
                problems.append(f"{rel}: R3 disposition still carries {NEW_KEY}")
            if lifecycle(text) != "archived":
                problems.append(f"{rel}: R3 disposition is not archived ({lifecycle(text)})")
        if row.get("disposition") == "R2" and binding != row["bound_slug"]:
            problems.append(f"{rel}: R2 binding {binding!r} != {row['bound_slug']!r}")
        receipt = path.parent / "disposition-receipt.json"
        if row.get("state") == "apply" and not receipt.is_file():
            problems.append(f"{rel}: applied disposition has no {receipt.name}")
    for slug in sorted(set(rows) - seen):
        problems.append(f"{TEAMS_DIR}/{slug}: classification row has no team definition")
    return problems


def test_live_bindings_are_converged() -> None:
    problems = binding_problems(ROOT, _load(CLASSIFICATION))
    assert not problems, problems


def test_live_teams_carry_no_old_binding_key() -> None:
    offenders = [str(path.relative_to(ROOT)) for path in team_files(ROOT)
                 if OLD_KEY in path.read_text(encoding="utf-8")]
    assert not offenders, offenders


def test_every_live_anchor_slug_resolves() -> None:
    dangling = []
    for path in team_files(ROOT):
        binding = binding_value(path.read_text(encoding="utf-8"), NEW_KEY)
        if binding and not resolves(ROOT, binding):
            dangling.append(f"{path.parent.name} -> {binding}")
    assert not dangling, dangling


def test_runs_are_out_of_scope(tmp_path: Path) -> None:
    root = tmp_path / "tree"
    run_dir = root / TEAMS_DIR / "some-team" / "runs"
    run_dir.mkdir(parents=True)
    (run_dir / "team.md").write_text("---\ngoal_slug: retired\n---\n", encoding="utf-8")
    assert team_files(root) == []
    assert not binding_problems(root, {"teams": []})


def test_fixture_tree_exposes_all_four_defect_classes() -> None:
    problems = binding_problems(FIXTURE_TREE, _load(FIXTURE_CLASSIFICATION))
    joined = "\n".join(problems)
    assert "still carries goal_slug" in joined
    assert "anchor_slug 'visualization-skill-selection' does not resolve" in joined
    assert "anchor_slug 'demo-seat-dispatch' does not resolve" in joined
    assert "applied disposition has no disposition-receipt.json" in joined
    assert ".specify/teams/demo-seat-dispatch/team.md: R3 disposition still carries anchor_slug" in joined
    assert "R3 disposition is not archived (active)" in joined
    assert sum(1 for line in problems if "does not resolve" in line) == 2


def test_injection_unresolved_binding_is_red(tmp_path: Path) -> None:
    root = tmp_path / "tree"
    (root / TEAMS_DIR / "t1").mkdir(parents=True)
    (root / ANCHORS_DIR / "real").mkdir(parents=True)
    (root / ANCHORS_DIR / "real" / "anchor.md").write_text("---\n---\n", encoding="utf-8")
    (root / TEAMS_DIR / "t1" / "team.md").write_text(
        "---\nslug: t1\nanchor_slug: missing\ngoal_slug: missing\n---\n", encoding="utf-8")
    problems = binding_problems(root, {"teams": []})
    assert f"{TEAMS_DIR}/t1/team.md: still carries goal_slug" in problems
    assert f"{TEAMS_DIR}/t1/team.md: anchor_slug 'missing' does not resolve" in problems
