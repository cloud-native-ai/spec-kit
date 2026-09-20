"""Shared assertion helpers for skill prompt-asset contract tests.

Used by test_summarize_project_prompt_assets.py and
test_study_project_uml_assets.py (spec 030-summarize-project, Feature 013).
"""
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

INSTRUCTIONS_FILE = ROOT / ".specify" / "instructions.md"


def _mirror_ignore_names() -> frozenset:
    """Reuse sync-mirrors.py's IGNORE_NAMES rather than restating it.

    sync-mirrors.py owns the definition of a mirror difference and already skips
    runtime junk; a comparison stricter than the tool it verifies fails on
    git-ignored, never-authored bytecode (__pycache__/*.pyc), whose presence on
    each side depends on import order — making the result order-dependent.
    Loaded by path because the filename is hyphenated (house pattern:
    tests/script_api.py).
    """
    path = ROOT / "scripts" / "python" / "sync-mirrors.py"
    spec = importlib.util.spec_from_file_location("_sync_mirrors_ignore", path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return frozenset(module.IGNORE_NAMES)


MIRROR_IGNORE_NAMES = _mirror_ignore_names()


def read_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a Markdown file; {} when absent/invalid."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def text_of(path: Path) -> str:
    """Read a file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def ordered_occurrences(text: str, needles: list[str]) -> list[int]:
    """Return the index of each needle in text; -1 when missing."""
    lowered = text.lower()
    return [lowered.find(n.lower()) for n in needles]


def assert_ordered(text: str, needles: list[str], context: str = "") -> None:
    """Assert every needle is present and appears in the given order."""
    positions = ordered_occurrences(text, needles)
    missing = [n for n, p in zip(needles, positions) if p < 0]
    assert not missing, f"Missing sections {missing} {context}".strip()
    assert positions == sorted(positions), (
        f"Sections out of order {needles} at {positions} {context}".strip()
    )


def dir_file_map(base: Path) -> dict[str, str]:
    """Map relative path -> file text for every non-junk file under base.

    Paths containing an ignored name (see MIRROR_IGNORE_NAMES) are skipped: they
    are runtime artifacts, never authored, git-ignored, and their presence on
    each side depends on import order.
    """
    return {
        str(p.relative_to(base)): p.read_text(encoding="utf-8")
        for p in sorted(base.rglob("*"))
        if p.is_file() and not (MIRROR_IGNORE_NAMES & set(p.relative_to(base).parts))
    }


def assert_dirs_byte_equivalent(canonical: Path, mirror: Path) -> None:
    """Assert two directory trees contain identical files with identical text."""
    assert canonical.is_dir(), f"Missing canonical dir {canonical}"
    assert mirror.is_dir(), f"Missing mirror dir {mirror}"
    left, right = dir_file_map(canonical), dir_file_map(mirror)
    assert set(left) == set(right), (
        f"Tree mismatch: only-canonical={sorted(set(left) - set(right))} "
        f"only-mirror={sorted(set(right) - set(left))}"
    )
    diffs = [rel for rel in left if left[rel] != right[rel]]
    assert not diffs, f"Byte differences in mirrored files: {diffs}"
