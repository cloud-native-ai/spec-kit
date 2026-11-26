"""BC closure guard for Feature 107 — the plan's closed Backward-Incompatible Change Inventory.

Pins the two migration-side clauses that are machine-decidable over the plan text:

* ``test_bc_row_set_closed_and_mapped`` — C-501: the declared inventory row set equals the
  closed set ``{BC-01…BC-06}``; every row names a resolution from the closed resolution
  vocabulary (``compatibility-bridge``), a migration or deterministic-refusal behavior, and a
  test path that exists on disk. A row naming a bare module filename resolves under
  ``tests/``; a row that refers to another row (``同 BC-01``) inherits that row's pinned test.
  An unmapped row — one row short, one row extra, an empty/dangling test reference, or a
  resolution outside the closed vocabulary — turns the guard red (the mutations below are the
  red-ability proof; C-501's red form is a mutation, not a red-first run, because the
  inventory predates this package).
* ``test_no_fallback_only_row`` — C-505: no row may be resolved solely by a runtime dual-path
  fallback or a manual instruction; every row maps to an executable migration or a
  deterministic refusal.

The inventory is read from ``plan.md`` (its owner) by this module's own row parser, never by a
second copy of the table.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / ".specify" / "specs" / "107-decision-governance" / "plan.md"

#: The closed BC row set (C-501).
CLOSED_ROWS = frozenset(f"BC-{n:02d}" for n in range(1, 7))

#: The closed resolution vocabulary the plan adopts from the requirements candidates.
RESOLUTION_TOKENS = ("compatibility-bridge",)

#: A behavior cell must carry at least one executable marker — a deterministic judgement or a
#: migration surface — for the row to count as "mapped to a migration or a deterministic
#: refusal" (C-505's positive half).
EXECUTABLE_MARKERS = (
    "legacy",
    "拒绝",
    "refuse",
    "renumber",
    "templates-generated",
    "判定式",
    "numstat",
)

#: Markers of a fallback-only or manual-only resolution (C-505's negative half).
FALLBACK_ONLY_MARKERS = (
    "双路径回退",
    "runtime fallback",
    "人工操作说明",
    "人工说明",
    "manual instruction",
)

ROW_RE = re.compile(r"^\| (BC-\d{2}) \|(.*)$")
PY_TOKEN_RE = re.compile(r"`([^`]+\.py)`")
ROW_REF_RE = re.compile(r"BC-\d{2}")


def row_line(text: str, bc_id: str) -> str:
    lines = [line for line in text.splitlines() if line.startswith(f"| {bc_id} |")]
    assert len(lines) == 1, f"expected exactly one {bc_id} row, found {len(lines)}"
    return lines[0]


def inventory_section(text: str) -> str:
    """Body of the ``## Backward-Incompatible Change Inventory`` H2, up to the next H2."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and "Backward-Incompatible Change Inventory" in line:
            start = index
            break
    assert start is not None, "plan lacks § Backward-Incompatible Change Inventory"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start + 1:end])


def rows(section: str) -> dict[str, dict[str, str]]:
    """Row id -> {change, resolution, behavior, evidence} read from the inventory table."""
    parsed: dict[str, dict[str, str]] = {}
    for line in section.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in match.group(2).split("|")]
        assert len(cells) >= 4, f"malformed row {match.group(1)}: {line!r}"
        parsed[match.group(1)] = {
            "change": cells[0],
            "resolution": cells[1],
            "behavior": cells[2],
            "evidence": cells[3],
        }
    return parsed


def resolve_path(token: str, root: Path) -> list[Path]:
    """Resolve a backticked ``.py`` token: an explicit repo path, or a bare filename."""
    if token.startswith("tests/") or token.startswith("src/"):
        return [root / token]
    return sorted((root / "tests").rglob(token))


def row_tests(row: dict[str, str], root: Path) -> list[Path]:
    """Direct ``.py`` tokens of one row's evidence cell that exist on disk."""
    found = []
    for token in PY_TOKEN_RE.findall(row["evidence"]):
        for candidate in resolve_path(token, root):
            if candidate.is_file():
                found.append(candidate)
    return found


def inventory_problems(text: str, root: Path) -> list[str]:
    """Every decidable closure/mapping defect of the inventory text; empty means mapped."""
    problems: list[str] = []
    parsed = rows(inventory_section(text))

    declared = frozenset(parsed)
    if declared != CLOSED_ROWS:
        problems.append(
            f"row set {sorted(declared)} differs from the closed set {sorted(CLOSED_ROWS)}"
        )

    # Fixed point: a row may inherit its pinned test from the rows it references.
    pinned: dict[str, list[Path]] = {bc_id: row_tests(row, root) for bc_id, row in parsed.items()}
    changed = True
    while changed:
        changed = False
        for bc_id, row in parsed.items():
            if pinned[bc_id]:
                continue
            inherited: list[Path] = []
            for ref in ROW_REF_RE.findall(row["evidence"]):
                if ref != bc_id and ref in pinned:
                    inherited.extend(pinned[ref])
            if inherited:
                pinned[bc_id] = inherited
                changed = True

    for bc_id in sorted(parsed):
        row = parsed[bc_id]
        if not row["change"]:
            problems.append(f"{bc_id}: empty change cell")
        if not any(token in row["resolution"] for token in RESOLUTION_TOKENS):
            problems.append(
                f"{bc_id}: resolution {row['resolution']!r} names no closed resolution token"
            )
        if not any(marker in row["behavior"] for marker in EXECUTABLE_MARKERS):
            problems.append(
                f"{bc_id}: behavior cell names no executable migration or deterministic refusal"
            )
        if not pinned[bc_id]:
            problems.append(
                f"{bc_id}: evidence cell names no existing test path and no row reference"
            )
    return problems


def fallback_only_rows(text: str) -> list[str]:
    """Rows whose resolution/behavior name only a fallback or a manual instruction (C-505)."""
    offenders = []
    for bc_id, row in sorted(rows(inventory_section(text)).items()):
        combined = f"{row['resolution']} {row['behavior']}"
        if any(marker in combined for marker in FALLBACK_ONLY_MARKERS) and not any(
            marker in row["behavior"] for marker in EXECUTABLE_MARKERS
        ):
            offenders.append(bc_id)
    return offenders


# --------------------------------------------------------------------------- #
# C-501 — row-set closure and row → test mapping
# --------------------------------------------------------------------------- #

def test_bc_row_set_closed_and_mapped() -> None:
    """C-501: the closed six rows are each mapped to an existing test and a behavior."""
    real = PLAN.read_text(encoding="utf-8") if PLAN.is_file() else None
    assert real is not None, f"missing plan: {PLAN}"
    assert inventory_problems(real, ROOT) == [], inventory_problems(real, ROOT)

    # Red-ability proof (the C-501 red form is a mutation, not a red-first run): a doctored
    # inventory loses a row, gains a seventh row, dangles a test reference, points at a
    # nonexistent test, or leaves the closed resolution vocabulary.
    missing = real.replace(row_line(real, "BC-05") + "\n", "")
    assert "row set" in " ".join(inventory_problems(missing, ROOT)), (
        "a missing BC row did not turn the closure guard red"
    )

    extra = real.replace(
        row_line(real, "BC-06"),
        row_line(real, "BC-06")
        + "\n| BC-07 | 新行 | `compatibility-bridge` | legacy | `tests/unit/test_validate_decisions.py` |",
    )
    assert "row set" in " ".join(inventory_problems(extra, ROOT)), (
        "a seventh BC row did not turn the closure guard red"
    )

    unresolved = real.replace(
        "| `test_decision_governance_guards.py`（同载体重复 id 夹具）+ register 夹具 |",
        "| 见上文 |",
    )
    assert unresolved != real, "the BC-03 evidence cell form changed; the mutation did not apply"
    assert any("BC-03" in problem for problem in inventory_problems(unresolved, ROOT)), (
        "a dangling test reference did not turn the mapping guard red"
    )

    dangling = real.replace(
        "`tests/integration/test_decision_governance_migrate_dryrun.py`：`specify migrate --format json`",
        "`tests/integration/test_absent_migrate_dryrun.py`：`specify migrate --format json`",
    )
    assert dangling != real, "the BC-04 evidence cell form changed; the mutation did not apply"
    assert any(
        "BC-04" in problem and "test path" in problem
        for problem in inventory_problems(dangling, ROOT)
    ), "a nonexistent test path did not turn the mapping guard red"

    bad_resolution = real.replace(
        row_line(real, "BC-01"),
        row_line(real, "BC-01").replace("`compatibility-bridge`", "runtime-fallback"),
    )
    assert any(
        "BC-01" in problem and "resolution" in problem
        for problem in inventory_problems(bad_resolution, ROOT)
    ), "a resolution outside the closed vocabulary did not turn the guard red"


# --------------------------------------------------------------------------- #
# C-505 — no fallback-only resolution
# --------------------------------------------------------------------------- #

def test_no_fallback_only_row() -> None:
    """C-505: every row maps to an executable behavior, none to a fallback or manual note."""
    real = PLAN.read_text(encoding="utf-8") if PLAN.is_file() else None
    assert real is not None, f"missing plan: {PLAN}"
    assert fallback_only_rows(real) == [], fallback_only_rows(real)

    # Red-ability proof: a row resolved by a runtime dual-path fallback plus a manual
    # instruction alone must be named.
    doctored = real.replace(
        row_line(real, "BC-05"),
        "| BC-05 | 新守卫面对旧记录 | `compatibility-bridge` | 以运行时双路径回退与人工操作说明收口 | "
        "同 BC-01 的 legacy 夹具 + `--numstat` 零删除读数（无删除行、无删除文件） |",
    )
    assert doctored != real, "the BC-05 row form changed; the mutation did not apply"
    assert fallback_only_rows(doctored) == ["BC-05"], fallback_only_rows(doctored)
