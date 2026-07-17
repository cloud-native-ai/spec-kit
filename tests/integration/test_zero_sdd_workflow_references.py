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

# Sanctioned exception: the CLI's obsolete-asset cleanup registry names legacy
# identifiers solely so init can delete them (a removal manifest, not a live
# reference). The region between these markers is stripped before scanning.
_REGISTRY_START = "OBSOLETE-ASSET-REGISTRY:START"
_REGISTRY_END = "OBSOLETE-ASSET-REGISTRY:END"


def _strip_obsolete_registry(text: str) -> str:
    if _REGISTRY_START not in text or _REGISTRY_END not in text:
        return text
    kept, skipping = [], False
    for line in text.splitlines():
        if _REGISTRY_START in line:
            skipping = True
            continue
        if _REGISTRY_END in line:
            skipping = False
            continue
        if not skipping:
            kept.append(line)
    return "\n".join(kept)


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
        if TOKEN in _strip_obsolete_registry(text):
            offenders.append(str(p.relative_to(ROOT)))
    assert not offenders, f"live sdd-workflow references remain in source: {sorted(offenders)}"


# The 10 docs relocated by Feature 029 (sdd-workflow refactor). This is the gate's
# real invariant — that the relocation happened and these remain present. The set is
# allowed to GROW as later features add shared-workflow protocols (e.g. Feature 031
# added glossary.md), so we assert presence of the relocated docs rather than a brittle
# exact count (see the "hard-coded counts are fragile" lesson).
RELOCATED_DOCS = {
    "agent-configuration.md", "checklist-methodology.md", "clarify-taxonomy.md",
    "dfx-catalog.md", "feature-integration.md", "feedback-step.md",
    "ignore-patterns.md", "requirements-guidelines.md", "tool-definitions.md",
    "user-input-protocol.md",
}


def test_shared_workflow_directory_contains_relocated_docs():
    shared = ROOT / "shared" / "workflow"
    assert shared.is_dir(), "shared/workflow/ must exist"
    docs = {p.name for p in shared.glob("*.md")}
    missing = RELOCATED_DOCS - docs
    assert not missing, f"relocated shared docs missing: {sorted(missing)}"
    assert len(docs) >= len(RELOCATED_DOCS), f"unexpectedly few shared docs: {sorted(docs)}"
