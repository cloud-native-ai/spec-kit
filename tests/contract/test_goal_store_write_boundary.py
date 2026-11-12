"""G-4 (T065) — one definition writer: a static write-surface audit.

The audit walks `scripts/`, `.specify/scripts/`, both skill layers, `src/` and `templates/`,
and collects every executable file that both **constructs a definition-store path** (a store
literal or one of the engine's path helpers) and **performs a write**. That intersection must
equal the declared allowlist: the definition engine (canonical + mirror) and the declared
derived `summary/**` writer (`build-summary-input.py`, canonical + mirror). Anything else is a
second definition writer and turns the guard red.

FR-065's boundary is enforced from both sides: the engine is the only definition writer, and
the derived writer's own destination construction must stay under `summary/`.

The two-writer simulation runs two real `goal-create` processes against one scratch root and
requires the two slugs to land at two distinct paths.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

AUDIT_ROOTS = ("scripts", ".specify/scripts", "skills", ".specify/skills", "src", "templates")
EXECUTABLE_SUFFIXES = {".py", ".sh", ".ps1"}

ENGINE_WRITERS = {"scripts/python/goal-utils.py", ".specify/scripts/python/goal-utils.py"}
DERIVED_WRITERS = {
    "skills/internal/create-team/scripts/build-summary-input.py",
    ".specify/skills/internal/create-team/scripts/build-summary-input.py",
}
ALLOWLIST = ENGINE_WRITERS | DERIVED_WRITERS

STORE_PATH = re.compile(r"\.specify/anchoring|\.specify/goals|\.specify/goal(?![a-z])")
PATH_HELPER = re.compile(
    r"\b(anchor_root|goals_root|definition_path|definition_filename|summary_dir|layer_root)\s*\(")
WRITE_OP = re.compile(
    r"write_text\(|write_bytes\(|open\([^)]*[\"'](?:w|a|wb|x|ab)[\"']"
    r"|os\.replace\(|shutil\.(?:move|copy|copyfile|copytree)\("
    r"|\.unlink\(|rmtree\(|\.mkdir\(")


def definition_writers(root: Path) -> dict[str, list[str]]:
    """Files under the audit roots that can write into a definition store -> the signals seen."""
    root = Path(root)
    found: dict[str, list[str]] = {}
    for rel in AUDIT_ROOTS:
        base = root / rel
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in EXECUTABLE_SUFFIXES:
                continue
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            signals = []
            if STORE_PATH.search(text):
                signals.append("store-path-literal")
            if PATH_HELPER.search(text):
                signals.append("path-helper")
            if not signals or not WRITE_OP.search(text):
                continue
            found[str(path.relative_to(root))] = signals
    return found


def derived_writer_escapes_summary(path: Path) -> list[str]:
    """Lines where the derived writer builds a destination outside a `summary/` subtree."""
    escapes = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not STORE_PATH.search(line):
            continue
        if not re.search(r"delivery_dir|out_path|open\(|write_text\(", line):
            continue
        if "summary" not in line:
            escapes.append(f"{number}: {line.strip()}")
    return escapes


def test_audit_roots_exist() -> None:
    missing = [rel for rel in AUDIT_ROOTS if not (REPO_ROOT / rel).is_dir()]
    assert not missing, f"audited roots missing: {missing}"


def test_the_only_definition_writers_are_the_engine_and_the_derived_writer() -> None:
    writers = definition_writers(REPO_ROOT)
    assert set(writers) == ALLOWLIST, {
        "unexpected": sorted(set(writers) - ALLOWLIST),
        "missing": sorted(ALLOWLIST - set(writers)),
    }


def test_engine_is_the_only_file_naming_a_definition_file_target() -> None:
    for rel, signals in definition_writers(REPO_ROOT).items():
        if rel in DERIVED_WRITERS:
            continue
        assert "path-helper" in signals or "store-path-literal" in signals, rel
        assert rel in ENGINE_WRITERS, f"{rel} could write a definition file"


def test_derived_writer_constructs_only_summary_destinations() -> None:
    for rel in sorted(DERIVED_WRITERS):
        escapes = derived_writer_escapes_summary(REPO_ROOT / rel)
        assert not escapes, f"{rel} builds a destination outside summary/: {escapes}"


def test_two_writers_put_two_slugs_at_two_paths(tmp_path: Path) -> None:
    root = tmp_path / "writer-sim"
    (root / ".specify").mkdir(parents=True)
    created = []
    for slug in ("alpha-writer", "beta-writer"):
        result = subprocess.run(
            [sys.executable, str(ENGINE), "goal-create", slug, "--repo-root", str(root),
             "--guidance", f"Ship the {slug} slice.", "--done", f"{slug} is verifiable.", "--json"],
            capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        created.append(str(root / ".specify/goals" / slug / "goal.md"))
    assert len(set(created)) == 2
    for path in created:
        assert Path(path).is_file()
    files = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
    assert files == [".specify/goals/alpha-writer/goal.md",
                     ".specify/goals/beta-writer/goal.md"], files


def test_anchor_writer_and_goal_writer_never_share_a_path(tmp_path: Path) -> None:
    root = tmp_path / "layer-sim"
    (root / ".specify").mkdir(parents=True)
    goal = subprocess.run(
        [sys.executable, str(ENGINE), "goal-create", "same-slug", "--repo-root", str(root),
         "--guidance", "Ship the goal slice.", "--done", "The goal slice is verifiable.", "--json"],
        capture_output=True, text=True, check=False)
    anchor = subprocess.run(
        [sys.executable, str(ENGINE), "create", "same-slug", "--repo-root", str(root),
         "--objective", "Reach the anchor end state.", "--criterion",
         "The anchor end state is demonstrated.", "--json"],
        capture_output=True, text=True, check=False)
    assert goal.returncode == 0, goal.stderr
    assert anchor.returncode == 0, anchor.stderr
    assert (root / ".specify/goals/same-slug/goal.md").is_file()
    assert (root / ".specify/anchoring/same-slug/anchor.md").is_file()


def test_injection_out_of_engine_definition_write_is_red(tmp_path: Path) -> None:
    root = tmp_path / "audit"
    (root / "scripts").mkdir(parents=True)
    rogue = root / "scripts" / "rogue-writer.py"
    rogue.write_text(
        "from pathlib import Path\n"
        "def write_definition(root):\n"
        "    target = Path(root) / '.specify/goals/rogue/goal.md'\n"
        "    target.parent.mkdir(parents=True, exist_ok=True)\n"
        "    target.write_text('# Goal: rogue\\n', encoding='utf-8')\n",
        encoding="utf-8")
    writers = definition_writers(root)
    assert set(writers) == {"scripts/rogue-writer.py"}, writers
    assert not set(writers) <= ALLOWLIST


def test_injection_derived_writer_escape_is_red(tmp_path: Path) -> None:
    copy = tmp_path / "build-summary-input.py"
    copy.write_text(
        'delivery_dir = repo_root / ".specify/anchoring" / goal_slug\n'
        'out_path = delivery_dir / "data/project-input.yaml"\n',
        encoding="utf-8")
    escapes = derived_writer_escapes_summary(copy)
    assert len(escapes) == 1, escapes
    assert ".specify/anchoring" in escapes[0]
    assert not derived_writer_escapes_summary(
        REPO_ROOT / "skills/internal/create-team/scripts/build-summary-input.py")


def test_live_tree_is_not_an_audit_fixture_only_check() -> None:
    """The live audit is the criterion; the injections above only prove it can go red."""
    writers = definition_writers(REPO_ROOT)
    assert ENGINE_WRITERS <= set(writers)
    assert DERIVED_WRITERS <= set(writers)
