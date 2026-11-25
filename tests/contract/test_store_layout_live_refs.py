"""105 live-reference containment — SC-006 product classes and the tests-class confinement.

Pins `contracts/live-reference-migration.contract.md` L-5 (and L-3 for the tests class):

1. compute the retired-root literal occurrence file set per product class and assert equality
   with the declared allowlist (both directions);
2. inside each allowlisted file, assert every matching line satisfies that file's allowed-line
   rule (the tombstone row and the ``retired_container`` key occur exactly once);
3. assert the in-test allowlist literal equals the contract's L-5 table (the table is the human
   face; the literal below is the pinned copy);
4. (L-3) assert no test file outside the declared legacy-test set carries the literal, while the
   two guard files are declared carriers by construction.

The retired-root literal is STR-001: ``.specify/memory/`` plus the bare container literal
``.specify/memory`` not followed by a path character (research R-2).

Mutation drills (declared here; executed in T032, readings in ``test-evidence/mutation-drill.md``):
moving the literal into an unlisted live file turns the set assertion red; placing it on an
unlisted line of an allowlisted file turns the line-rule assertion red; each restores green.

``tests/**`` is not part of SC-006's measured product classes (requirements.md SC-006); the
tests-class function below pins the L-3 confinement instead.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    REPO_ROOT
    / ".specify"
    / "specs"
    / "105-runtime-store-layout"
    / "contracts"
    / "live-reference-migration.contract.md"
)

RETIRED_LITERAL = re.compile(r"\.specify/memory(?![A-Za-z0-9_-])")

PRODUCT_CLASSES = {
    "framework-source": ("templates", "skills", "shared", "scripts", "src"),
    "runtime-guide": (".specify/instructions.md", ".specify/glossary.md"),
    "current-docs": ("docs",),
}

# L-4 dated-record exclusions: the two explicit classes plus the declared archive/static/notes
# extension (Decision Tension T-004).
DATED_EXCLUSIONS = (
    "docs/reference/history/",
    "docs/decisions/",
    "docs/archive/",
    "docs/static/",
    "docs/notes/",
)

# L-5 allowlist — each entry must occur at least once; the allowed-line rules are per file.
TOMBSTONE_ROW = re.compile(r"^\|\s*Tombstone[^|]*\|\s*`\.specify/memory/`\s*\|")
DECLARATION_KEY = re.compile(r"^\s*retired_container:\s*\.specify/memory\s*$")
LEGACY_CONTEXT = re.compile(r"legacy", re.IGNORECASE)
LEGACY_RESIDUE = re.compile(
    r'(?:"(?:memory-draft|memory-indexes|legacy-memory-gitworkflow-state)",\s*"\.specify/memory[^"]*"'
    r'|\("\.specify/git-workflow\.md",\s*"\.specify/memory/git-workflow\.md"\))'
)

ALLOWLIST = {
    "shared/definitions/framework-map.md": (TOMBSTONE_ROW,),
    "shared/declarations/facts/runtime-store-layout.yaml": (DECLARATION_KEY,),
    "scripts/python/anchor-layout-migrate.py": (LEGACY_CONTEXT,),
    "scripts/python/sanitize-utils.py": (LEGACY_RESIDUE,),
}

# Files whose matching-line count is pinned exactly as well as filtered.
EXACT_OCCURRENCE_FILES = {
    "shared/definitions/framework-map.md": 1,
    "shared/declarations/facts/runtime-store-layout.yaml": 1,
}

# L-3 tests-class declaration: pre-migration workspaces built on purpose (migrate-097 builders,
# anchor-layout / sanitize-legacy / store-layout legacy fixtures) plus the two guard files.
LEGACY_TEST_FILES = (
    "tests/fixtures/migrate-097/builders.py",
    "tests/integration/test_migrate_us1_converge.py",
    "tests/integration/test_migrate_us2_safety.py",
    "tests/integration/test_store_layout_migration_us1_us2.py",
    "tests/unit/test_migrate_planner.py",
    "tests/unit/test_sanitize_checks_migration.py",
)
GUARD_TEST_FILES = (
    "tests/contract/test_runtime_store_layout.py",
    "tests/contract/test_store_layout_live_refs.py",
    "tests/contract/test_tools_domain.py",
    "tests/integration/test_dispatch_injection_paths.py",
    "tests/integration/test_init_new_layout.py",
    "tests/integration/test_memory_preservation.py",
    # Guards that carry the retired form by construction: they translate it (a mechanical
    # live-path mapping applied to a recorded baseline), so their own source must name it.
    "tests/contract/test_decision_tension_contract.py",
    "tests/contract/test_script_interface_contract.py",
)


def _iter_files(rel_root: str):
    path = REPO_ROOT / rel_root
    if path.is_file():
        yield path
        return
    if not path.is_dir():
        return
    for child in sorted(path.rglob("*")):
        if child.is_file() and not child.is_symlink():
            yield child


def _carries_literal(path: Path) -> bool:
    try:
        return RETIRED_LITERAL.search(path.read_text(encoding="utf-8")) is not None
    except UnicodeDecodeError:
        return False


def _class_of(relpath: str):
    if any(relpath.startswith(root + "/") for root in PRODUCT_CLASSES["framework-source"]):
        return "framework-source"
    if relpath in PRODUCT_CLASSES["runtime-guide"]:
        return "runtime-guide"
    if relpath.startswith("docs/"):
        if relpath.startswith(DATED_EXCLUSIONS):
            return None
        return "current-docs"
    return None


def _measured_product_sets():
    measured = {name: set() for name in PRODUCT_CLASSES}
    for class_name, roots in PRODUCT_CLASSES.items():
        for rel_root in roots:
            for path in _iter_files(rel_root):
                relpath = path.relative_to(REPO_ROOT).as_posix()
                if _class_of(relpath) != class_name:
                    continue
                if _carries_literal(path):
                    measured[class_name].add(relpath)
    return measured


def _matching_lines(relpath: str):
    path = REPO_ROOT / relpath
    lines = path.read_text(encoding="utf-8").splitlines()
    return [(number, line) for number, line in enumerate(lines, 1) if RETIRED_LITERAL.search(line)]


def _contract_allowlist():
    text = CONTRACT.read_text(encoding="utf-8")
    section = text.split("## L-5", 1)[1].split("\n## ", 1)[0]
    files = set()
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        first_cell = line.strip().strip("|").split("|")[0]
        files.add(first_cell.strip().strip("`").strip())
    return files


def test_allowlist_pinned_copy_equals_the_contract_table():
    """L-5 item 3: the in-test literal is a pinned copy of the contract's table."""
    assert set(ALLOWLIST) == _contract_allowlist(), (
        "the allowlist literal drifted from contracts/live-reference-migration.contract.md L-5"
    )
    for relpath in ALLOWLIST:
        assert _class_of(relpath) == "framework-source", (
            f"{relpath} is allowlisted but does not sit in a measured product class"
        )


def test_product_class_occurrence_sets_equal_the_allowlist():
    """L-5 item 1: measured occurrence sets equal the declared allowlist, both directions."""
    measured = _measured_product_sets()
    for class_name in PRODUCT_CLASSES:
        declared = {relpath for relpath in ALLOWLIST if _class_of(relpath) == class_name}
        assert measured[class_name] == declared, (
            f"{class_name}: unexpected={sorted(measured[class_name] - declared)} "
            f"missing={sorted(declared - measured[class_name])}"
        )

    union = set().union(*measured.values())
    assert sorted(union - set(ALLOWLIST)) == [], "a file outside the four-file allowlist carries the literal"
    assert sorted(set(ALLOWLIST) - union) == [], "an allowlisted file lost its occurrence (L-5: each MUST carry one)"


def test_allowlisted_files_keep_only_allowed_lines():
    """L-5 item 2: every matching line inside an allowlisted file satisfies its line rule."""
    for relpath, rules in ALLOWLIST.items():
        hits = _matching_lines(relpath)
        assert hits, f"{relpath}: the allowlisted file must carry at least one occurrence"
        off_rule = [
            (number, line.strip()[:160])
            for number, line in hits
            if not any(rule.search(line) for rule in rules)
        ]
        assert not off_rule, (
            f"{relpath}: the literal escaped its allowed lines (L-5): {off_rule}"
        )
        exact = EXACT_OCCURRENCE_FILES.get(relpath)
        if exact is not None:
            assert len(hits) == exact, (
                f"{relpath}: expected exactly {exact} matching line(s), got {len(hits)}"
            )


def test_tests_literal_confined_to_declared_set():
    """L-3: no test file outside the declared legacy/guard set carries the literal."""
    measured = set()
    for path in _iter_files("tests"):
        if _carries_literal(path):
            measured.add(path.relative_to(REPO_ROOT).as_posix())
    declared = set(LEGACY_TEST_FILES) | set(GUARD_TEST_FILES)
    outside = sorted(measured - declared)
    assert not outside, (
        "test files carry the retired-root literal outside the declared legacy/guard set: "
        f"{outside}"
    )
    missing = sorted(set(LEGACY_TEST_FILES) - measured)
    assert not missing, (
        f"declared legacy fixtures no longer carry their pre-migration literal: {missing}"
    )
