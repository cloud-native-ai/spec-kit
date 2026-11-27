"""Fixture support for Feature 110 (context management) — trees, engine runs, digests.

The fixture family under ``tests/fixtures/context-management/`` carries one workspace
per case, each in the framework-source shape: its own
``shared/definitions/context-management-definitions.md`` and its own four
``shared/declarations/facts/context-*.yaml`` facts at the case root, so the audit
engine's ``--workspace-root`` selects the case and the case's own declaration layer
drives the reading (C-012, C-040, A-17).

Case map — every case deviates from the shared base tree in exactly one judged token
(the engine guard pins the expected finding; this table is the fixture inventory, not a
second rule owner):

* ``all-present``          — clean: every roster source resolves, is readable and non-empty
  (including the three concept-pointer rows).
* ``absence-mixed``        — one missing source (absent), one empty store (empty), one
  dangling-symlink source (unreachable).
* ``concept-missing``      — the ``concept-definitions`` layout row is deleted and one
  declared source (``.specify/glossary.md``) is a dangling symlink.
* ``violation-unknown-layer``    — one extra layout row carries the unknown layer ``runtime``.
* ``violation-unknown-form``     — one row's form is the unknown token ``cache``.
* ``violation-roster-mismatch``  — one roster class's layout row is missing.
* ``violation-roster-order``     — two task-layer rows are swapped.
* ``violation-layer-form``       — one task row is ``read-in-full`` and one system row is
  ``bounded-index`` (exactly two matrix findings, and nothing else).
* ``violation-duplicate-class``  — one class id appears on two rows of its own layer.
* ``violation-empty-layer``      — the task layer carries no layout rows (roster side keeps
  its classes).
* ``violation-cap-missing``      — one ``bounded-index`` row's cap cell reads ``—``.
* ``violation-category-column``  — the layout header gains a seventh ``category`` column.
* ``declaration-unknown-member`` — the classes fact maps an undeclared layer ``runtime``.
* ``declaration-missing``        — ``context-forms.yaml`` is absent.

Owner-document conventions the guards and the engine read (the "layout anchor and row
grammar" that T009/T010 pin): the first pipe table under ``## Forms`` carries the header
``form | legal layers``; the first pipe table under ``## Layout`` carries the fixed six
columns ``class id | layer | form | source | owner | cap reference``. Cells are
pipe-delimited; backticks around a cell value are cosmetic and stripped; a ``source``
cell is a comma-separated workspace-relative path list or a ``runtime-discovery:<id>``
token; a ``legal layers`` cell is a comma-separated layer list.

Standard library only (pytest is the host, not a dependency). No network access.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_ROOT = Path(__file__).resolve().parent / "context-management"
ENGINE = REPO_ROOT / "scripts" / "python" / "context-audit.py"
OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "context-management-definitions.md"
FACTS_DIR = REPO_ROOT / "shared" / "declarations" / "facts"
CONTRACT = REPO_ROOT / "shared" / "declarations" / "contract.yaml"
DECLARATION_READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE_INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
PRE_CHANGE_NOTES = (
    REPO_ROOT / ".specify" / "specs" / "110-context-management" / "notes"
    / "pre-change-measurements.md"
)

FACT_SLUGS = ("context-categories", "context-layers", "context-forms", "context-classes")

LAYOUT_COLUMNS = ("class id", "layer", "form", "source", "owner", "cap reference")
FORMS_COLUMNS = ("form", "legal layers")
TRIGGER_COLUMNS = ("trigger", "composer", "scope", "evidence")
LANDING_COLUMNS = ("cell", "definition", "carriers", "allowed forms", "content vs pointer")
CONCEPT_STRUCTURE_COLUMNS = ("structure", "carrier", "pointer form", "presence surface")
BOUNDARY_COLUMNS = ("neighbour", "owner pointer", "distinction")
PRESENCE_COLUMNS = ("token", "meaning")

# The closed form set and its per-layer matrix (C-005). A literal pinned in a guard is a
# sanctioned duplicate; membership stays owned by `context-forms.yaml`.
FORM_MATRIX = {
    "pointer": ("system", "project", "task"),
    "read-in-full": ("project",),
    "bounded-index": ("project", "task"),
    "runtime-discovery": ("system",),
    "inline-digest": ("task",),
}


# --------------------------------------------------------------------------- #
# Declaration-layer access (the layer's one parser; never a second YAML parser)
# --------------------------------------------------------------------------- #
_READER = None


def declaration_reader():
    """The shared reader module, loaded from its source path (one parser, C-012)."""
    global _READER
    if _READER is None:
        assert DECLARATION_READER.is_file(), f"declaration reader missing: {DECLARATION_READER}"
        spec = importlib.util.spec_from_file_location(
            "declaration_reader_context_110", DECLARATION_READER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _READER = module
    return _READER


def fact_path(slug: str) -> Path:
    return FACTS_DIR / f"{slug}.yaml"


def fact_text(slug: str) -> str:
    path = fact_path(slug)
    assert path.is_file(), f"declaration fact missing: {path}"
    return path.read_text(encoding="utf-8")


def fact_body(slug: str) -> dict:
    body = declaration_reader().parse_subset(fact_text(slug), str(fact_path(slug)))
    assert isinstance(body, dict), f"{fact_path(slug)} does not parse as a mapping"
    return body


def preset_consumer_names() -> tuple:
    """The engine and the declarations guard — the two consumers every fact must name."""
    return ("scripts/python/context-audit.py", "tests/contract/test_context_management_declarations.py")


# --------------------------------------------------------------------------- #
# Owner-document access — headings, pipe tables, marker lists
# --------------------------------------------------------------------------- #
def owner_text() -> str:
    assert OWNER_DOC.is_file(), f"owner document missing: {OWNER_DOC}"
    return OWNER_DOC.read_text(encoding="utf-8")


def section_body(text: str, heading: str) -> str:
    """The body of the first ``## <heading>`` section (heading line excluded).

    Returns an empty string when the heading is absent; callers assert presence.
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return ""
    out = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def table_rows(text: str, heading: str) -> tuple:
    """Parse the first pipe table under ``## <heading>``.

    Returns ``(header, rows)`` where ``header`` is the normalized header cell list and
    ``rows`` is a list of normalized cell lists. Absent heading or table → ``((), [])``.
    A cell is stripped of whitespace and surrounding backticks.
    """
    body = section_body(text, heading)
    if not body:
        return (), []
    table: list = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = _split_row(stripped)
            if table and all(set(cell) <= set("-: ") for cell in cells):
                continue  # separator row
            table.append(cells)
        elif table:
            break
    if not table:
        return (), []
    return tuple(table[0]), table[1:]


def _split_row(line: str) -> list:
    inner = line.strip()[1:-1]
    return [_normalize_cell(cell) for cell in inner.split("|")]


def _normalize_cell(cell: str) -> str:
    value = cell.strip()
    while len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def marker_value(text: str, marker: str) -> str:
    """The value of a ``<marker>: <value>`` line inside the document (first match)."""
    for line in text.splitlines():
        stripped = line.strip()
        prefix = f"{marker}:"
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return ""


def marker_list(text: str, marker: str) -> tuple:
    raw = marker_value(text, marker)
    if not raw:
        return ()
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def table_cells(rows: list, column_index: int) -> list:
    return [row[column_index] for row in rows if len(row) > column_index]


def split_layers(cell: str) -> tuple:
    return tuple(part.strip() for part in cell.split(",") if part.strip())


# --------------------------------------------------------------------------- #
# Engine runs (subprocess with `--workspace-root`; interpreter from sys.executable)
# --------------------------------------------------------------------------- #
def run_engine(workspace_root: Path, *args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        f"audit engine missing: {ENGINE} — a red guard that names its missing subject")
    command = [sys.executable, str(ENGINE), *args, "--workspace-root", str(workspace_root)]
    return subprocess.run(command, capture_output=True, text=True, timeout=timeout)


def run_engine_json(workspace_root: Path, *args: str) -> tuple:
    """Run the engine with ``--json``; returns ``(completed, payload_or_None)``."""
    completed = run_engine(workspace_root, *args, "--json")
    payload = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except ValueError:
            payload = None
    return completed, payload


def copy_case_to(destination: Path, case: str) -> Path:
    """Copy one fixture case into ``destination`` (a tmp_path root) and return the root.

    Symlinks are copied as symlinks so the dangling-link absence cases survive.
    """
    source = FIXTURES_ROOT / case
    assert source.is_dir(), f"fixture case missing: {source}"
    root = destination / case
    shutil.copytree(source, root, symlinks=True)
    return root


def rewrite_fact(workspace_root: Path, slug: str, text: str) -> Path:
    path = workspace_root / "shared" / "declarations" / "facts" / f"{slug}.yaml"
    assert path.is_file(), f"fixture fact missing: {path}"
    path.write_text(text, encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# Tree manifests (containment legs) — SHA-256 per entry, `__pycache__` excluded by name
# --------------------------------------------------------------------------- #
def tree_manifest(root: Path) -> dict:
    manifest = {}
    root = Path(root)
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            manifest[relative] = "symlink:" + str(path.readlink())
        elif path.is_dir():
            manifest[relative] = "dir"
        else:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    digest.update(chunk)
            manifest[relative] = "file:" + digest.hexdigest()
    return manifest


def manifest_delta(before: dict, after: dict) -> tuple:
    """``(added, removed, changed)`` path lists between two manifests."""
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(path for path in set(before) & set(after) if before[path] != after[path])
    return added, removed, changed