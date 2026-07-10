"""Reference-integrity guard (spec 023 — Agent Framework Redesign, T004).

Two invariants (FR-016, M5, SC-004):

1. No *live* reference resolves to a pre-migration path/name:
     - agent-subrole-*                          (renamed to agent-stage-*)
     - agent-role-meta-coordinator-template.md  (merged into team-supervisor)
     - agent-team-supervisor-template.md        (merged; canonical is
                                                  agent-role-team-supervisor-template.md)
2. Every referenced `agent-*-template.md` basename exists under the canonical
   template home `skills/create-agent/templates/` (its installed mirror
   `.specify/skills/create-agent/templates/` is accepted as equivalent).

Scope: skills/, templates/, docs/, tests/, .specify/agents/, .specify/skills/.
Immutable history (Decision D5) and this guard's own source files are excluded.
Lines carrying a migration marker are treated as historical context and skipped
for invariant (1), matching T035's allowance for design.md.

TDD: MUST fail pre-migration (old paths are still referenced) and pass once the
rename/merge/reference-fix work (US2/US5) is complete.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_TEMPLATES = ROOT / "skills" / "create-agent" / "templates"
MIRROR_TEMPLATES = ROOT / ".specify" / "skills" / "create-agent" / "templates"

SCOPE_DIRS = [
    ROOT / "skills",
    ROOT / "templates",
    ROOT / "docs",
    ROOT / "tests",
    ROOT / ".specify" / "agents",
    ROOT / ".specify" / "skills",
]

SELF_FILES = {
    "test_agent_deprecated_terms.py",
    "test_agent_reference_integrity.py",
}

# Test files that name removed templates purely to assert their ABSENCE — these
# are negative assertions, not live references, and are skipped for invariant (2).
NEGATIVE_ASSERTION_FILES = {
    "test_legacy_removal.py",
}

TEXT_SUFFIXES = {".md", ".py", ".sh", ".txt"}

# Pre-migration paths/names that MUST NOT be referenced by live artifacts.
OLD_PATH_PATTERNS = [
    re.compile(r"agent-subrole-[a-z0-9-]*"),
    re.compile(r"agent-role-meta-coordinator-template\.md"),
    re.compile(r"agent-team-supervisor-template\.md"),
]

TEMPLATE_REF = re.compile(r"agent-[a-z0-9-]+-template\.md")

MIGRATION_MARKERS = re.compile(
    r"formerly|former |deprecated|renamed|\brename\b|replaced|replaces|"
    r"migration|migrat|historical|history|legacy|previously|no longer|"
    r"instead of|→|->|"
    r"废弃|原[「\u300c]|合并|重命名|改为|不再使用|统一为|统一改|历史|迁移",
    re.IGNORECASE,
)


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
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            if path.name in SELF_FILES or _is_immutable_history(path):
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def test_no_reference_to_premigration_paths():
    hits: list[str] = []
    for path in _iter_live_files():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(lines, start=1):
            if MIGRATION_MARKERS.search(line):
                continue  # historical/migration context allowed (D5, T035)
            for pat in OLD_PATH_PATTERNS:
                if pat.search(line):
                    rel = path.relative_to(ROOT)
                    hits.append(f"{rel}:{lineno}: {line.strip()}")
                    break
    assert not hits, (
        f"Found {len(hits)} live reference(s) to pre-migration template "
        f"paths/names:\n" + "\n".join(hits)
    )


def test_referenced_templates_exist_in_canonical_home():
    missing: list[str] = []
    for path in _iter_live_files():
        if path.name in NEGATIVE_ASSERTION_FILES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(lines, start=1):
            if MIGRATION_MARKERS.search(line):
                continue  # historical mentions of removed templates allowed
            for basename in TEMPLATE_REF.findall(line):
                if (CANONICAL_TEMPLATES / basename).exists():
                    continue
                if (MIRROR_TEMPLATES / basename).exists():
                    continue
                rel = path.relative_to(ROOT)
                missing.append(f"{rel}:{lineno}: {basename}")
    assert not missing, (
        "Referenced agent-*-template.md files not found under "
        f"skills/create-agent/templates/:\n" + "\n".join(missing)
    )
