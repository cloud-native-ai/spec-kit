"""Shared assertion helpers for skill prompt-asset contract tests.

Used by test_summarize_project_prompt_assets.py and
test_analysis_project_uml_assets.py (spec 030-summarize-project, Feature 013).
Modeled on the conventions of test_create_skills_prompt_assets.py.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

INSTRUCTIONS_FILE = ROOT / ".specify" / "instructions.md"


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
    """Map relative path -> file text for every file under base."""
    return {
        str(p.relative_to(base)): p.read_text(encoding="utf-8")
        for p in sorted(base.rglob("*"))
        if p.is_file()
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


def skill_registry_rows(skill_name: str) -> list[str]:
    """Return SKILLS registry table rows mentioning the given skill name."""
    text = text_of(INSTRUCTIONS_FILE)
    start = text.find("<!-- SKILLS_REGISTRY_START -->")
    end = text.find("<!-- SKILLS_REGISTRY_END -->")
    assert 0 <= start < end, "SKILLS registry markers not found in instructions.md"
    block = text[start:end]
    return [
        line for line in block.splitlines()
        if line.startswith("|") and skill_name in line
    ]
