"""Contract test: spec ↔ feature binding integrity (goal 2026-08-15 audit).

Guards against the stale-reference class found in the full specs audit: the
user flattened ``.specify/specs/.archive/`` (parallel commits a7318075 /
d70b0519), after which Feature rows still pointed at dead ``.archive/`` paths.
Deprecated specs now live under ``.specify/archive/spec/`` (new convention).

C-0: every row of the features.md table MUST conform to the seven-column
     schema. A row with a bare (unescaped) ``|`` inside a cell or without a
     closing ``|`` is a schema violation and MUST fail with its line number;
     silently skipping it is forbidden (a skipped row hides its Spec Path from
     C-1).
C-1: every spec path referenced by a features.md row (when not ``-``) MUST
     exist on disk.
C-2: every ACTIVE spec's numeric ``Feature ID`` binding MUST have a matching
     row in features.md.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FEATURES_MD = REPO_ROOT / ".specify" / "features.md"
SPECS_DIR = REPO_ROOT / ".specify" / "specs"
ARCHIVE_DIR = REPO_ROOT / ".specify" / "archive" / "spec"

_TABLE_HEADER = "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |"
_COLUMNS = ("ID", "Name", "Description", "Status", "Feature Details", "Spec Path", "Last Updated")
# Split on unescaped pipes only: a markdown table cell escapes a literal pipe as \|.
_CELL_SEP = re.compile(r"(?<!\\)\|")
_ROW_ID = re.compile(r"^\|\s*(\d{3})\s*\|")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}\b")


def _table_lines():
    """Yield ``(lineno, line)`` for the main Features table, 1-based."""
    lines = FEATURES_MD.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == _TABLE_HEADER), None)
    assert start is not None, f"{FEATURES_MD.name}: feature table header not found"
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("## "):
            break
        yield index + 1, line


def _split_row(lineno: int, line: str) -> tuple[dict[str, str] | None, list[str]]:
    """Validate one data row's whole-row shape; never skip malformed rows."""
    errors = []
    stripped = line.rstrip()
    closed = stripped.endswith("|")
    if not closed:
        errors.append(f"{FEATURES_MD.name}:{lineno}: row is missing its closing '|'")
    cells = _CELL_SEP.split(stripped)
    # Drop the empty head (leading '|') and, when present, the empty tail.
    data_cells = cells[1:-1] if closed else cells[1:]
    if len(data_cells) != len(_COLUMNS):
        errors.append(
            f"{FEATURES_MD.name}:{lineno}: expected {len(_COLUMNS)} columns, "
            f"found {len(data_cells)} (unescaped '|' inside a cell?)"
        )
    if errors:
        return None, errors
    row = dict(zip(_COLUMNS, (cell.strip().replace("\\|", "|") for cell in data_cells)))
    return row, errors


def _parse_feature_rows() -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for lineno, line in _table_lines():
        if not line.strip():
            continue
        if not line.startswith("|"):
            errors.append(f"{FEATURES_MD.name}:{lineno}: non-table content inside Feature table")
            continue
        if set(line.strip()) <= set("|-: "):
            continue  # header separator row
        match = _ROW_ID.match(line)
        if not match:
            errors.append(
                f"{FEATURES_MD.name}:{lineno}: Feature table row does not start "
                "with a three-digit ID"
            )
            continue
        row, row_errors = _split_row(lineno, line)
        errors.extend(row_errors)
        if row is None:
            continue
        if row["ID"] in seen:
            errors.append(f"{FEATURES_MD.name}:{lineno}: duplicate Feature ID {row['ID']}")
        seen.add(row["ID"])
        spec = row["Spec Path"]
        if spec != "-" and not spec.startswith(".specify/"):
            errors.append(
                f"{FEATURES_MD.name}:{lineno}: Feature {row['ID']} Spec Path column "
                f"(column 6) is neither a .specify/ path nor '-': {spec!r}"
            )
        detail = row["Feature Details"]
        if detail != "-" and not detail.startswith(".specify/features/"):
            errors.append(
                f"{FEATURES_MD.name}:{lineno}: Feature {row['ID']} Feature Details "
                f"(column 5) is neither a .specify/features/ path nor '-': {detail!r}"
            )
        if not _DATE.match(row["Last Updated"]):
            errors.append(
                f"{FEATURES_MD.name}:{lineno}: Feature {row['ID']} Last Updated "
                f"does not start with YYYY-MM-DD: {row['Last Updated']!r}"
            )
        rows.append({
            "id": row["ID"],
            "name": row["Name"],
            "description": row["Description"],
            "status": row["Status"],
            "detail": row["Feature Details"],
            "spec": row["Spec Path"],
            "last_updated": row["Last Updated"],
        })
    return rows, errors


def _feature_rows() -> list[dict[str, str]]:
    rows, errors = _parse_feature_rows()
    assert not errors, "features.md feature table schema violations: " + "; ".join(errors)
    return rows


@pytest.mark.contract
def test_c0_features_table_rows_conform_to_schema():
    _, errors = _parse_feature_rows()
    assert not errors, "features.md feature table schema violations:\n" + "\n".join(errors)


@pytest.mark.contract
def test_c1_every_referenced_spec_path_exists():
    bad = []
    for row in _feature_rows():
        spec = row["spec"]
        if spec in ("-", "") or not spec.startswith(".specify"):
            continue
        if not (REPO_ROOT / spec).exists():
            bad.append(f"Feature {row['id']}: {spec}")
    assert not bad, (
        "features.md references non-existent spec paths (stale archive/move "
        f"references): {bad}"
    )


@pytest.mark.contract
def test_c2_active_spec_feature_bindings_resolve():
    feature_ids = {row["id"] for row in _feature_rows()}
    bad = []
    for spec_dir in sorted(SPECS_DIR.iterdir()):
        if spec_dir.name.startswith(".") or not spec_dir.is_dir():
            continue
        req = spec_dir / "requirements.md"
        if not req.exists():
            continue
        m = re.search(r"\*\*Feature ID\*\*:\s*(\d{3})",
                      req.read_text(encoding="utf-8"))
        if m and m.group(1) not in feature_ids:
            bad.append(f"{spec_dir.name}: Feature {m.group(1)} has no row")
    assert not bad, f"active specs bind unregistered Features: {bad}"
