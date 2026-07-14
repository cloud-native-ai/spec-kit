"""Integration test: the zero-`sdd-workflow`-reference acceptance gate (Feature 029, contract C-GATE).

No live ``sdd-workflow`` reference may remain in the source-of-truth trees. The token is legitimately
retained only in historical/spec/proposal content, which is excluded. The derived ``.specify/`` mirror
is validated separately after regeneration (task T024), so it is not scanned here.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Source-of-truth trees + files scanned by the gate.
SCAN_TREES = ["src", "scripts", "templates", "skills", "agents"]
SCAN_FILES = ["pyproject.toml", "README.md"]

# docs/ is scanned except history + the refactor proposal (legitimate historical/spec content).
DOCS_EXCLUDE_DIRS = {"history"}
DOCS_EXCLUDE_FILES = {"summary/03-sdd-workflow-refactor-proposal.md"}

TEXT_SUFFIXES = {".md", ".py", ".sh", ".toml", ".txt", ".json"}
TOKEN = "sdd-workflow"


def _scan_paths():
    for tree in SCAN_TREES:
        base = ROOT / tree
        if base.exists():
            yield from (p for p in base.rglob("*") if p.suffix in TEXT_SUFFIXES and p.is_file())
    for name in SCAN_FILES:
        p = ROOT / name
        if p.exists():
            yield p
    docs = ROOT / "docs"
    if docs.exists():
        for p in docs.rglob("*"):
            if p.suffix not in TEXT_SUFFIXES or not p.is_file():
                continue
            rel = p.relative_to(docs)
            if rel.parts and rel.parts[0] in DOCS_EXCLUDE_DIRS:
                continue
            if rel.as_posix() in DOCS_EXCLUDE_FILES:
                continue
            yield p


def test_no_sdd_workflow_reference_in_source():
    offenders = []
    for p in _scan_paths():
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if TOKEN in text:
            offenders.append(str(p.relative_to(ROOT)))
    assert not offenders, f"live sdd-workflow references remain in source: {sorted(offenders)}"


def test_shared_workflow_directory_has_ten_docs():
    shared = ROOT / "shared" / "workflow"
    assert shared.is_dir(), "shared/workflow/ must exist"
    docs = sorted(p.name for p in shared.glob("*.md"))
    assert len(docs) == 10, f"expected 10 shared docs, found {len(docs)}: {docs}"
