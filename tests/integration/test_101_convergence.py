"""G-9 (T071) — a cleanup applied to the pre-convergence fixture tree converges it.

The subject is the fixture tree after one real `cleanup --apply`: the Anchor store holds no
action-level entry, no retired binding key survives anywhere in a live team definition, and no
`anchor_slug` is left pointing at nothing (FR-064, FR-066).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
FIXTURE = ROOT / "tests/fixtures/anchor-goal-realignment"
ENGINE = ROOT / "scripts/python/goal-utils.py"

OLD_KEY = "goal_slug"
NEW_KEY = re.compile(r"(?m)^\s*anchor_slug\s*:\s*(?P<slug>[A-Za-z0-9_.-]+)\s*$")


def _converged(tmp_path: Path) -> tuple[Path, dict]:
    root = tmp_path / "tree"
    root.mkdir()
    shutil.copytree(FIXTURE / "pre-convergence/.specify", root / ".specify")
    shutil.copy2(FIXTURE / "classification/classification.json", root / "classification.json")
    for command in (["init", "-q", "."], ["add", "-A"], ["commit", "-qm", "fixture"]):
        subprocess.run(
            ["git", "-c", "user.email=guard@example.invalid",
             "-c", "user.name=guard", *command],
            cwd=str(root), check=True, capture_output=True, text=True)
    result = subprocess.run(
        [sys.executable, str(ENGINE), "cleanup", "--apply", "--repo-root", str(root),
         "--classification", str(root / "classification.json"), "--json"],
        cwd=str(root), capture_output=True, text=True, check=False)
    assert result.returncode == 0, (result.returncode, result.stderr)
    payload = json.loads(result.stdout)
    assert payload.get("verdict") == "ok", payload
    return root, json.loads((root / "classification.json").read_text(encoding="utf-8"))


def _anchor_store_problems(root: Path, classification: dict) -> list[str]:
    problems: list[str] = []
    store = root / ".specify/anchoring"
    for child in sorted(store.iterdir()):
        if not child.is_dir():
            continue
        if (child / "goal.md").is_file():
            problems.append(f"{child.name}: retired goal.md still in the Anchor store")
        if not (child / "anchor.md").is_file():
            problems.append(f"{child.name}: no anchor.md in the Anchor store")
    for entry in classification["entries"]:
        if entry["class"] == "action-goal" and (store / entry["slug"]).exists():
            problems.append(f"{entry['slug']}: action-goal entry still in the Anchor store")
        if entry["class"] == "obsolete" and (store / entry["slug"]).exists():
            problems.append(f"{entry['slug']}: obsolete entry still in the Anchor store")
    return problems


def _binding_problems(root: Path) -> tuple[list[str], int]:
    problems: list[str] = []
    bound = 0
    for team in sorted((root / ".specify/teams").glob("*/team.md")):
        text = team.read_text(encoding="utf-8")
        if OLD_KEY in text:
            problems.append(f"{team.parent.name}: retired goal_slug still present")
        for match in NEW_KEY.finditer(text):
            bound += 1
            slug = match.group("slug")
            anchor = root / ".specify/anchoring" / slug / "anchor.md"
            goal = root / ".specify/goals" / slug / "goal.md"
            if not (anchor.is_file() or goal.is_file()):
                problems.append(f"{team.parent.name}: anchor_slug {slug!r} does not resolve")
    return problems, bound


def test_the_fixture_tree_converges(tmp_path):
    root, classification = _converged(tmp_path)

    assert _anchor_store_problems(root, classification) == []
    problems, bound = _binding_problems(root)
    assert problems == []
    assert bound >= 1, "no team kept a binding, so the resolution check proved nothing"
