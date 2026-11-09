"""Contract test: the `[green:]` tag's marker semantics in `validate-tasks.py` (T138, F-093-004).

The ruling this file pins (recorded in `notes/analyze-findings.md` § 2 and registered as
F-093-004): a `[green: <contract>#<clause>]` attribution is a **red-first marker** — the
row that first turns that clause green. A claimed clause belongs to exactly one row, and
a feature MAY claim a strict subset of its contract clauses; the clause partition
(条款分区, `.specify/memory/glossary.md`) is scoped to claimed clauses. The tag's
definition stays in `templates/tasks-template.md`; this file guards the *validator's
description* of it from re-acquiring the totality reading the ruling rejected.

Propositions:

* C-1 the rule block in the module docstring states the marker reading;
* C-2 the emitted `green-clause-collision` message states it too (read from a real run);
* C-3 the `--help` banner (the parser description) states it and never the totality form;
* C-4 the drift phrasings are absent from the source;
* C-5 behaviour: a strict-subset claim passes, a double claim warns with the marker
  wording, and a dangling clause is still an error (the check survives the rewording);
* C-6 the green partition on 093's own `tasks.md`: >= 1 claim, 0 double-claimed,
  0 dangling (T138's own acceptance reading);
* C-7 the runtime mirror is the byte-identical projection of the source (never edited);
* C-8 the dead one-line-per-task owner (F-093-015) is re-pointed to the real section,
  in the source template and its mirror, and the section resolves.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = REPO_ROOT / "scripts" / "python" / "validate-tasks.py"
MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "validate-tasks.py"
TASKS_TEMPLATE = REPO_ROOT / "templates" / "tasks-template.md"
TASKS_TEMPLATE_MIRROR = REPO_ROOT / ".specify" / "templates" / "tasks-template.md"
CREATE_TASKS_SKILL = REPO_ROOT / "skills" / "internal" / "create-tasks" / "SKILL.md"
TASKS_093 = REPO_ROOT / ".specify" / "specs" / "093-concurrency-by-default" / "tasks.md"

#: The marker reading's two load-bearing phrases (F-093-004's wording).
MARKER_ROW = "a claimed clause belongs to one row"
MARKER_SUBSET = "a feature MAY claim a strict subset of its contract clauses"

#: The totality readings the ruling rejected; none may survive in the validator source.
FORBIDDEN_TOTALITY = (
    "cut over the same clause twice",
    "each clause is claimed exactly once",
    "every clause is claimed",
    "every clause must be claimed",
)

#: The dead owner path F-093-015 measured as existing in no worktree.
DEAD_POINTER = ".specify/templates/commands/tasks.md"
LIVE_POINTER = ".specify/skills/internal/create-tasks/SKILL.md"
LIVE_SECTION = "One line per task (mechanical-validation contract)"


def _load_validator():
    """Load the real validator module — never a copy of its logic."""
    assert VALIDATOR.is_file(), f"missing artifact: {VALIDATOR}"
    spec = importlib.util.spec_from_file_location("_validate_tasks_green_under_test", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _norm(text: str) -> str:
    return " ".join(text.split())


def _docstring() -> str:
    return _load_validator().__doc__ or ""


def _write_contract(tmp_path: Path) -> str:
    directory = tmp_path / "contracts"
    directory.mkdir()
    (directory / "x.md").write_text(
        "# Contract: x\n\n- **C-1** — one.\n- **C-2** — two.\n", encoding="utf-8")
    return "contracts/x.md"


def _write_tasks(tmp_path: Path, rows: list[str], name: str = "tasks.md") -> Path:
    path = tmp_path / name
    path.write_text(
        "# Tasks\n\n## Phase 1: Setup\n\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return path


# --- C-1: the rule block ---------------------------------------------------

def test_c1_rule_block_states_the_marker_reading():
    doc = _norm(_docstring())
    assert MARKER_ROW in doc, "the docstring rule block lost the row-scoped claim statement"
    assert MARKER_SUBSET.lower() in doc.lower(), (
        "the docstring rule block lost the strict-subset statement")
    # the label still exists (the check roster is not what this ruling removes)
    assert "green-clause-collision" in doc


# --- C-2: the emitted message ---------------------------------------------

def test_c2_emitted_message_states_the_marker_reading(tmp_path):
    mod = _load_validator()
    contract = _write_contract(tmp_path)
    tasks = _write_tasks(tmp_path, [
        f"- [ ] T001 first [green: {contract}#C-1]",
        f"- [ ] T002 second [green: {contract}#C-1]",
    ])
    _errors, warnings = mod.validate(tasks)
    collisions = [w for w in warnings if "green-clause-collision" in w]
    assert len(collisions) == 1, warnings
    message = _norm(collisions[0])
    assert MARKER_ROW in message, f"emitted message lost the marker reading: {message}"
    assert MARKER_SUBSET.lower() in message.lower(), (
        f"emitted message lost the strict-subset statement: {message}")


# --- C-3 / C-4: no totality reading survives -------------------------------

def test_c3_help_banner_states_the_marker_reading():
    parser = _load_validator().build_parser()
    description = _norm(parser.description or "")
    assert MARKER_ROW in description, "--help lost the row-scoped claim statement"
    assert MARKER_SUBSET.lower() in description.lower(), (
        "--help lost the strict-subset statement")


def test_c4_totality_phrasings_are_absent():
    source = VALIDATOR.read_text(encoding="utf-8")
    lowered = source.lower()
    survivors = [phrase for phrase in FORBIDDEN_TOTALITY if phrase in lowered]
    assert not survivors, (
        f"the validator re-acquired a totality reading: {survivors} — the ruling's marker "
        f"reading (F-093-004) admits a strict subset of claimed clauses")


# --- C-5: the check survives the rewording ---------------------------------

def test_c5_strict_subset_passes(tmp_path):
    mod = _load_validator()
    contract = _write_contract(tmp_path)
    tasks = _write_tasks(tmp_path, [
        f"- [ ] T001 first [green: {contract}#C-1]",
        "- [ ] T002 second",
    ])
    errors, warnings = mod.validate(tasks)
    assert errors == [], errors
    assert [w for w in warnings if "green-" in w] == [], warnings


def test_c5_dangling_clause_is_still_an_error(tmp_path):
    mod = _load_validator()
    contract = _write_contract(tmp_path)
    tasks = _write_tasks(tmp_path, [f"- [ ] T001 first [green: {contract}#C-9]"])
    errors, _warnings = mod.validate(tasks)
    assert any("green-dangling" in e for e in errors), errors


# --- C-6: 093's own green partition ----------------------------------------

def test_c6_093_green_partition():
    assert TASKS_093.is_file(), f"missing artifact: {TASKS_093}"
    mod = _load_validator()
    claims: list = []
    errors, _warnings = mod.validate(TASKS_093, claims_out=claims)
    assert claims, "093's tasks.md carries no [green:] claim at all"
    dangling = [e for e in errors if "green-dangling" in e]
    assert dangling == [], dangling
    seen = {}
    duplicates = []
    for claim in claims:
        key = (claim["contract_file"], claim["clause_id"])
        if key in seen:
            duplicates.append(key)
        seen[key] = claim
    assert duplicates == [], f"double-claimed clauses: {duplicates}"


# --- C-7: the mirror is a projection ---------------------------------------

def test_c7_validator_mirror_is_byte_identical():
    assert MIRROR.is_file(), f"missing artifact: {MIRROR}"
    assert MIRROR.read_bytes() == VALIDATOR.read_bytes(), (
        "the .specify/validate-tasks.py mirror drifted from its source; regenerate it with "
        "scripts/python/sync-mirrors.py — never hand-edit the projection")


# --- C-8: the F-093-015 dead pointer is re-pointed --------------------------

def test_c8_dead_owner_pointer_is_repointed():
    assert CREATE_TASKS_SKILL.is_file()
    assert LIVE_SECTION in CREATE_TASKS_SKILL.read_text(encoding="utf-8"), (
        "the re-pointed owner section does not exist in the create-tasks skill")
    for template in (TASKS_TEMPLATE, TASKS_TEMPLATE_MIRROR):
        text = template.read_text(encoding="utf-8")
        assert DEAD_POINTER not in text, (
            f"{template.relative_to(REPO_ROOT)} still names the dead owner {DEAD_POINTER}")
        assert LIVE_POINTER in text, (
            f"{template.relative_to(REPO_ROOT)} does not name the live owner {LIVE_POINTER}")
    assert TASKS_TEMPLATE_MIRROR.read_bytes() == TASKS_TEMPLATE.read_bytes(), (
        "the tasks-template mirror drifted from its source")
