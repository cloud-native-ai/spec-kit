"""G-10 (T072) — the command surface drifts red: ledger row, reference page, per-layer family.

Three subjects, each with its own red injection:

- the flow-class ledger must carry the `/speckit.anchor` row and a `/speckit.goal` row that
  declares the four-mode scope and the named Anchor-only refusal;
- the reference page `docs/reference/commands/anchor.md` must exist and document all seven
  modes;
- `goal-utils.py command-family` must answer per definition layer (`anchor` / `goal` / `team`),
  not with one boolean.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
ENGINE = ROOT / "scripts/python/goal-utils.py"
LEDGER = ROOT / "shared/definitions/flow-class-definitions.md"
PAGE = ROOT / "docs/reference/commands/anchor.md"

LEDGER_COLUMNS = ("unit_id", "flow_class", "basis", "neutral", "notes")
SEVEN_MODES = ("create", "view", "modify", "targets", "migrate", "migrate-archive",
               "coordinate")
LAYER_KEYS = {"anchor", "goal", "team"}


def _cell(value: str) -> str:
    return value.strip()


def ledger_rows(text: str) -> dict[str, dict[str, str]]:
    """Parse the ledger table by its header names — the parser never guesses columns."""
    rows: dict[str, dict[str, str]] = {}
    header: list[str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None and rows:
                break
            continue
        cells = [_cell(cell) for cell in stripped.strip("|").split("|")]
        if header is None:
            if tuple(cells) == LEDGER_COLUMNS:
                header = cells
            continue
        if set("".join(cells)) <= {"-", ":", " "}:
            continue
        row = dict(zip(header, cells))
        rows[row["unit_id"]] = row
    return rows


def ledger_problems(text: str) -> list[str]:
    problems: list[str] = []
    rows = ledger_rows(text)
    anchor = rows.get("/speckit.anchor")
    if anchor is None:
        problems.append("the ledger has no /speckit.anchor row")
    else:
        if anchor.get("flow_class") != "execution":
            problems.append(f"/speckit.anchor flow_class is {anchor.get('flow_class')!r}")
        if anchor.get("basis") != "behavior-oracle":
            problems.append(f"/speckit.anchor basis is {anchor.get('basis')!r}")
    goal = rows.get("/speckit.goal")
    if goal is None:
        problems.append("the ledger has no /speckit.goal row")
    else:
        notes = goal.get("notes", "")
        if not re.search(r"四模式|four.mode|4.mode", notes, re.I):
            problems.append("/speckit.goal row does not declare its four-mode scope")
        if not re.search(r"Anchor-only", notes, re.I):
            problems.append("/speckit.goal row does not name the Anchor-only refusal")
    return problems


def page_problems(text: str) -> list[str]:
    problems: list[str] = []
    if "templates/commands/anchor.md" not in text:
        problems.append("the page does not cite its source-of-truth template")
    missing = [mode for mode in SEVEN_MODES
               if not re.search(rf"(?<![A-Za-z-]){re.escape(mode)}(?![A-Za-z-])", text)]
    if missing:
        problems.append(f"the page never documents: {', '.join(missing)}")
    return problems


def family_shape_problems(payload: dict) -> list[str]:
    problems: list[str] = []
    layers = payload.get("layers")
    if not isinstance(layers, dict):
        problems.append(f"layers is {type(layers).__name__}, not a per-layer object")
        return problems
    if set(layers) != LAYER_KEYS:
        problems.append(f"layers answers for {sorted(layers)}, not {sorted(LAYER_KEYS)}")
    if any(not isinstance(value, bool) for value in layers.values()):
        problems.append("a layer verdict is not a boolean")
    if payload.get("in_family") is not True:
        problems.append("the command is not in the family at all")
    return problems


def _family(command: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(ENGINE), "command-family", "--command", command, "--json"],
        cwd=str(ROOT), capture_output=True, text=True, check=False)
    assert result.returncode == 0, (result.returncode, result.stderr)
    return json.loads(result.stdout)


def test_ledger_carries_both_command_rows():
    assert ledger_problems(LEDGER.read_text(encoding="utf-8")) == []


def test_reference_page_documents_all_seven_modes():
    assert PAGE.is_file(), f"missing reference page {PAGE}"
    assert page_problems(PAGE.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("command", ["anchor", "goal"])
def test_command_family_answers_per_definition_layer(command):
    assert family_shape_problems(_family(command)) == []


def test_a_ledger_without_the_anchor_row_turns_red():
    text = LEDGER.read_text(encoding="utf-8")
    stripped = "\n".join(line for line in text.splitlines()
                         if "/speckit.anchor" not in line)
    problems = ledger_problems(stripped)
    assert any("/speckit.anchor row" in problem for problem in problems), problems


def test_a_page_missing_one_mode_turns_red():
    text = PAGE.read_text(encoding="utf-8")
    doctored = re.sub(r"coordinate", "group", text)
    problems = page_problems(doctored)
    assert any("coordinate" in problem for problem in problems), problems


def test_a_single_boolean_family_answer_turns_red():
    problems = family_shape_problems({"command": "anchor", "in_family": True,
                                      "layers": True})
    assert any("not a per-layer object" in problem for problem in problems), problems
