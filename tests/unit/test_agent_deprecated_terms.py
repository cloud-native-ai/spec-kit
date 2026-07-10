"""Deprecated-term guard (spec 023 — Agent Framework Redesign, T003).

Asserts there are 0 *live* uses of the deprecated Agent-framework vocabulary:

  - "SubRole" / "Subrole"  (dimension renamed to "Stage")
  - "improver"             (stage renamed to "optimizer")
  - "Meta-Coordinator"     (role merged into the single "Team Supervisor")

Scope (FR-015, SC-002, DoD-4): skills/, templates/, docs/, tests/,
.specify/agents/, .specify/skills/.

Immutable history is excluded (Decision D5): .specify/specs/, CHANGELOG*,
draft/, and .specify/memory/features/019.md. This guard's own source files are
also excluded (they contain the terms as string literals).

Historical/migration context is permitted per Decision D5 and task T035: a line
that also carries a migration marker (e.g. "formerly", "renamed", "废弃", "原",
"→") is describing the rename itself, not using the term as live vocabulary, so
it does not count as a live match.

TDD: this guard MUST fail against the pre-migration tree and pass once the
migration (US2/US3/US4/US5) is complete.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Directories in scope for the zero-live-reference requirement.
SCOPE_DIRS = [
    ROOT / "skills",
    ROOT / "templates",
    ROOT / "docs",
    ROOT / "tests",
    ROOT / ".specify" / "agents",
    ROOT / ".specify" / "skills",
]

# Deprecated terms → the replacement they should have become.
DEPRECATED_PATTERNS = {
    "subrole": re.compile(r"subrole", re.IGNORECASE),
    "improver": re.compile(r"improver", re.IGNORECASE),
    "meta-coordinator": re.compile(r"meta-coordinator", re.IGNORECASE),
}

# A line carrying any of these markers is describing the migration itself
# (historical/migration context) and is therefore allowed (D5, T035).
MIGRATION_MARKERS = re.compile(
    r"formerly|former |deprecated|renamed|\brename\b|replaced|replaces|"
    r"migration|migrat|historical|history|legacy|previously|no longer|"
    r"instead of|→|->|"
    r"废弃|原[「\u300c]|合并|重命名|改为|不再使用|统一为|统一改|历史|迁移",
    re.IGNORECASE,
)

# Files excluded from the guard (own source + immutable history fragments).
SELF_FILES = {
    "test_agent_deprecated_terms.py",
    "test_agent_reference_integrity.py",
}

TEXT_SUFFIXES = {".md", ".py", ".sh", ".txt"}


def _is_immutable_history(path: Path) -> bool:
    parts = path.parts
    if ".specify" in parts and "specs" in parts:
        return True
    if "draft" in parts:
        return True
    if "CHANGELOG" in path.name.upper():
        return True
    if path.name == "019.md" and "features" in parts:
        return True
    return False


def _iter_live_files():
    seen = set()
    for base in SCOPE_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in TEXT_SUFFIXES:
                continue
            if path.name in SELF_FILES:
                continue
            if _is_immutable_history(path):
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def _live_matches(term_key: str, pattern: re.Pattern) -> list[str]:
    hits: list[str] = []
    for path in _iter_live_files():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(lines, start=1):
            if not pattern.search(line):
                continue
            if MIGRATION_MARKERS.search(line):
                continue  # historical/migration context is allowed (D5, T035)
            rel = path.relative_to(ROOT)
            hits.append(f"{rel}:{lineno}: {line.strip()}")
    return hits


@pytest.mark.parametrize("term", sorted(DEPRECATED_PATTERNS))
def test_no_live_deprecated_term(term: str):
    hits = _live_matches(term, DEPRECATED_PATTERNS[term])
    assert not hits, (
        f"Found {len(hits)} live use(s) of deprecated term '{term}' "
        f"(use Stage/optimizer/Team Supervisor instead):\n" + "\n".join(hits)
    )
