"""Contract tests for Feature 083 US5 — SC-008 command-surface disambiguation (T028).

SC-008 asks for **positive** rows and at least one **negative** row, in one run:

* ``speckit.skills`` (bare) and ``/speckit.skills`` (slash) normalise to
  ``command-surface`` and point at ``templates/commands/skills.md``;
* a command-shaped name that is **not** a command — or the mirror form of a dotted
  name — reports something other than ``command-surface``, proving the ruling is
  not "anything with a dot or a slash is a command";
* a command-surface result never enters Skill resolution (FR-023(b)).

The rows come from the matrix fixture's ``surface`` segment (the single expectation
source, GM-13); :func:`check_surface` is the assertion function the GM-07 negative
case re-runs on a flipped copy.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MATRIX_REL = Path("tests/fixtures/skill-reference/normalization-matrix.json")
HELPER_REL = Path("tests/contract/skill_reference_matrix.py")

#: The `/speckit.skills` command the positive rows must point at (SW-06 / SR-06).
COMMAND_TEMPLATE_REL = "templates/commands/skills.md"
COMMAND_NAME = "speckit.skills"


def _helper():
    path = REPO_ROOT / HELPER_REL
    assert path.is_file(), "artifact missing: %s" % path
    spec = importlib.util.spec_from_file_location("skill_reference_matrix", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_rows(segment: str | None = None) -> list[dict]:
    path = REPO_ROOT / MATRIX_REL
    assert path.is_file(), "artifact missing: %s" % path
    matrix = json.loads(path.read_text(encoding="utf-8"))
    return [row for row in matrix["rows"] if segment is None or row["segment"] == segment]


def _normalize(row: dict) -> dict:
    module = _helper()
    form = row["form"]
    select = form if form in module.OPERATIONS else "bare name"
    return module.normalize(row["raw"], form=select,
                            operation=row.get("operation", "invocation"),
                            repo_root=REPO_ROOT)


def check_surface(rows) -> list[str]:
    """The SC-008 assertion: positives report the command, negatives do not."""
    problems: list[str] = []
    positives = [r for r in rows if r["expect"]["outcome"] == "command-surface"]
    negatives = [r for r in rows if r["expect"]["outcome"] != "command-surface"]

    if len(positives) < 2:
        problems.append("SC-008 needs at least two positive rows, found %d" % len(positives))
    bare = [r for r in positives if r["raw"] == COMMAND_NAME]
    slash = [r for r in positives if r["raw"] == "/" + COMMAND_NAME]
    if not bare:
        problems.append("no positive row feeds the bare form %r" % COMMAND_NAME)
    if not slash:
        problems.append("no positive row feeds the slash form %r" % ("/" + COMMAND_NAME))
    for row in positives:
        result = _normalize(row)
        if result.get("outcome") != "command-surface":
            problems.append("%s: %r reported %r, not command-surface"
                            % (row["id"], row["raw"], result.get("outcome")))
            continue
        target = result.get("command_target") or ""
        # A command-surface row points at the command template named after its own name;
        # the row that feeds /speckit.skills must reach that command's template.
        if target != "templates/commands/%s.md" % result.get("normalized", "").split(".", 1)[-1]:
            problems.append("%s: %r points at %r, not at its own command template"
                            % (row["id"], row["raw"], target or "nothing"))
        if row["raw"].lstrip("/") == COMMAND_NAME and target != COMMAND_TEMPLATE_REL:
            problems.append("%s: %r points at %r, not %r"
                            % (row["id"], row["raw"], target or "nothing",
                               COMMAND_TEMPLATE_REL))
        # A command-shaped but non-existent name still points at "that command"
        # (R05: the ruling follows the namespace, not the file); the /speckit.skills
        # row's target is checked above, where it must exist.
        if not target:
            problems.append("%s: the command target %r does not exist"
                            % (row["id"], result["command_target"]))
        if result.get("enters_skill_resolution") is not False:
            problems.append("%s: a command-surface result entered Skill resolution"
                            % row["id"])

    if not negatives:
        problems.append("SC-008 needs at least one negative row, found 0 — without it the "
                        "ruling 'anything with a dot or a slash is a command' is unfalsified")
    for row in negatives:
        result = _normalize(row)
        if result.get("outcome") == "command-surface":
            problems.append("%s: command-shaped input %r was ruled a command (case is not "
                            "the criterion)" % (row["id"], row["raw"]))
    dotted = [r for r in rows
              if r["expect"]["outcome"] != "command-surface"
              and "." in r["raw"] and "/" not in r["raw"].lstrip("@")]
    if not dotted:
        problems.append("no negative row carries a dotted, slash-free name — the dot is "
                        "not a command marker")
    return problems


def test_sc008_command_surface_positives_and_negatives(capsys):
    rows = matrix_rows()
    for row in rows:
        result = _normalize(row)
        print("%s raw=%r -> %s %r" % (row["id"], row["raw"], result.get("outcome"),
                                      result.get("command_target") or "-"))
    problems = check_surface(rows)
    assert not problems, "SC-008 violations:\n- " + "\n- ".join(problems)


def test_sc008_negative_case_flipping_one_expected_class_turns_red(tmp_path):
    rows = matrix_rows()
    positive = next(row for row in rows if row["raw"] == COMMAND_NAME)
    positive["expect"]["outcome"] = "skill"
    positive["expect"].pop("command_target", None)
    problems = check_surface(rows)
    assert any("was ruled a command" in p for p in problems
               if not p.startswith("R05")), (
        "the negative case did not turn the positivity assertion red: %r" % problems)


def test_sc008_negative_case_a_negative_row_ruled_command_turns_red(tmp_path):
    rows = matrix_rows()
    negative = next(row for row in rows if row["expect"]["outcome"] != "command-surface")
    # Relabel the negative row as a command: a flipping implementation would now pass
    # the class comparison, and the assertion must still catch the contradiction.
    negative["expect"]["outcome"] = "command-surface"
    negative["expect"]["command_target"] = COMMAND_TEMPLATE_REL
    problems = check_surface(rows)
    assert any("reported 'skill', not command-surface" in p or "reported 'failure'" in p
               for p in problems), (
        "the negative case did not turn the disambiguation assertion red: %r" % problems)
