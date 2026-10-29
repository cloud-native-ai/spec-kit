"""Contract tests for the Feature-Line class declaration (077, T003).

Owns ``contracts/class-declaration.md`` C-001…C-010 and C-007's single-source
leg, plus ``contracts/class-resolution.md`` C-008's stderr shape:

* the declaration line is verbatim — ``**Flow Class**`` + half-width colon + one
  space + value, no trailing whitespace, field name and value case sensitive;
* it belongs in the head region (before ``## Related Feature``);
* four author-error codes, each one example, all exit code **1** (never 2):
  ``invalid-class`` / ``declaration-malformed`` (full-width colon, field-name
  case variant, trailing whitespace, inline comment — one form each) /
  ``declaration-duplicate`` (regardless of whether the two values agree) /
  ``declaration-misplaced``;
* every exit-1 diagnostic is one stderr line naming the repo-relative file, the
  line number and the offending value, in the contracted shape
  ``<code>: <path>:<line> carries '<value>', <one sentence>``;
* the exit-1 record carries ``flow_class: null`` + ``source: declaration`` and
  never the ``execution`` + ``default`` pair (a typo must not read as a decision);
* ``templates/requirements-template.md`` carries the field between ``**Status**:``
  and ``**Input**:`` in placeholder form (no class pre-filled, no criteria
  sentence);
* single source of truth — the feature index has no class column and the feature
  detail stores no value (at most a pointer).

The declaration position chosen here is the requirements head region
(``requirements.md`` § Assumptions A4); the four codes' exit-code band is
``contracts/class-declaration.md`` C-010.

Red-first (Constitution IV): the engine ignores the field today, so every
declaration fixture answers ``execution`` / ``source: default`` / exit 0 and the
template carries no field line.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
TEMPLATE = REPO_ROOT / "templates" / "requirements-template.md"
FEATURE_INDEX = REPO_ROOT / ".specify" / "memory" / "features.md"
FEATURE_DETAIL = REPO_ROOT / ".specify" / "memory" / "features" / "077.md"

NINE_FIELDS = {
    "action",
    "checked_at",
    "unit_id",
    "flow_class",
    "source",
    "marker",
    "basis",
    "neutral",
    "error",
}
AUTHOR_ERROR_CODES = (
    "invalid-class",
    "declaration-malformed",
    "declaration-duplicate",
    "declaration-misplaced",
)

OWNER_TEXT = """# Flow Class Definitions (unit-test fixture)

本文件是 077 契约测试的临时夹具，不是仓库所有者。

## 逐流程台账

**台账版本**: 1（2026-10-30）

| unit_id | flow_class | basis | neutral |
|---------|------------|-------|---------|
| /speckit.implement | execution | mixed-oracle | |
"""


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), "flow-class engine missing: %s" % ENGINE
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _lookup(repo: Path, unit_id: str) -> subprocess.CompletedProcess:
    return _run("--repo", str(repo), "--action", "lookup", "--unit-id", unit_id,
                "--format", "json")


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON record on stdout (stderr=%r)" % proc.stderr
    )
    return json.loads(proc.stdout)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _repo_with(tmp_path: Path, name: str, text: str) -> Path:
    repo = tmp_path / "repo"
    (repo / "templates" / "commands").mkdir(parents=True, exist_ok=True)
    _write(repo / "shared" / "definitions" / "flow-class-definitions.md", OWNER_TEXT)
    _write(
        repo / ".specify" / "shared" / "definitions" / "flow-class-definitions.md",
        OWNER_TEXT,
    )
    _write(repo / ".specify" / "specs" / name / "requirements.md", text)
    return repo


def _diagnostic_lines(proc: subprocess.CompletedProcess) -> list[str]:
    return [line for line in proc.stderr.splitlines() if line.strip()]


def _assert_author_error(
    proc: subprocess.CompletedProcess,
    code: str,
    *,
    name: str,
    line_numbers: set[int],
    value_fragment: str = "execution",
) -> dict:
    """Assert one exit-1 author error, its stderr shape and its record."""
    assert proc.returncode == 1, (
        "%s must be exit 1 (blocking), never the exit-2 degradation "
        "(stdout=%r stderr=%r)" % (code, proc.stdout, proc.stderr)
    )
    lines = _diagnostic_lines(proc)
    assert lines, "an exit-1 finding must say what it found on stderr"
    first = lines[0]
    assert first.startswith(code + ": "), first
    assert ".specify/specs/%s/requirements.md" % name in first, (
        "the diagnostic must name the repo-relative declaration file: %r" % first
    )
    found = {int(number) for number in re.findall(r":(\d+)(?=\D|$)", first)}
    assert line_numbers <= found, (
        "the diagnostic must name line(s) %r; got %r" % (sorted(line_numbers), first)
    )
    assert value_fragment in first, (
        "the diagnostic must carry the offending value/form: %r" % first
    )
    assert re.search(r"carries '.*', .+", first), (
        "the contracted shape is `<code>: <path>:<line> carries '<value>', "
        "<one sentence>`; got %r" % first
    )
    record = _json(proc)
    assert set(record) == NINE_FIELDS
    assert record["flow_class"] is None, (
        "an author error must not present a decided class"
    )
    assert record["source"] == "declaration"
    assert record["error"] and record["error"]["label"] == code
    return record


# --------------------------------------------------------------------------- #
# A. verbatim grammar — value forms that are legal / illegal
# --------------------------------------------------------------------------- #
def test_well_formed_declaration_is_read_verbatim(tmp_path):
    repo = _repo_with(
        tmp_path, "fx-ok", "# fixture spec\n\n**Flow Class**: expression\n"
    )

    proc = _lookup(repo, "spec:fx-ok")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "expression"
    assert record["source"] == "declaration"
    assert record["marker"] is None


@pytest.mark.parametrize(
    "declaration",
    [
        "**Flow Class**：execution",                   # full-width colon
        "**flow class**: execution",                   # field-name case variant
        "**Flow Class**: execution   ",                # trailing whitespace
        "**Flow Class**: execution <!-- keep -->",     # inline comment
    ],
    ids=["full-width-colon", "field-name-case", "trailing-space", "inline-comment"],
)
def test_malformed_forms_report_declaration_malformed(tmp_path, declaration):
    repo = _repo_with(
        tmp_path, "fx-malformed", "# fixture spec\n\n%s\n" % declaration
    )

    proc = _lookup(repo, "spec:fx-malformed")

    _assert_author_error(
        proc, "declaration-malformed", name="fx-malformed", line_numbers={3}
    )


def test_value_is_case_sensitive_and_outside_set_reports_invalid_class(tmp_path):
    repo = _repo_with(
        tmp_path, "fx-case", "# fixture spec\n\n**Flow Class**: Expression\n"
    )

    proc = _lookup(repo, "spec:fx-case")

    _assert_author_error(
        proc,
        "invalid-class",
        name="fx-case",
        line_numbers={3},
        value_fragment="Expression",
    )


def test_invalid_class_names_the_file_line_and_value(tmp_path):
    repo = _repo_with(
        tmp_path, "fx-bad", "# fixture spec\n\n**Flow Class**: expressive\n"
    )

    proc = _lookup(repo, "spec:fx-bad")

    record = _assert_author_error(
        proc,
        "invalid-class",
        name="fx-bad",
        line_numbers={3},
        value_fragment="expressive",
    )
    assert record["marker"] is None, (
        "source: declaration and the default marker are mutually exclusive"
    )


# --------------------------------------------------------------------------- #
# B. position — head region only
# --------------------------------------------------------------------------- #
def test_declaration_after_related_feature_reports_misplaced(tmp_path):
    text = (
        "# fixture spec\n"                      # 1
        "\n"                                    # 2
        "## Related Feature *(mandatory)*\n"    # 3
        "\n"                                    # 4
        "**Flow Class**: execution\n"           # 5
    )
    repo = _repo_with(tmp_path, "fx-misplaced", text)

    proc = _lookup(repo, "spec:fx-misplaced")

    _assert_author_error(
        proc, "declaration-misplaced", name="fx-misplaced", line_numbers={5}
    )


def test_field_in_the_head_region_stays_legal(tmp_path):
    text = (
        "# fixture spec\n"                               # 1
        "\n"                                             # 2
        "**Flow Class**: execution\n"                    # 3
        "\n"                                             # 4
        "## Related Feature *(mandatory)*\n"             # 5
        "\n"                                             # 6
        "**Feature ID**: 999\n"                          # 7
    )
    repo = _repo_with(tmp_path, "fx-head", text)

    proc = _lookup(repo, "spec:fx-head")

    assert proc.returncode == 0, proc.stderr
    assert _json(proc)["source"] == "declaration"


# --------------------------------------------------------------------------- #
# C. uniqueness — two lines are always a duplicate, whatever the values are
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "first,second",
    [("execution", "execution"), ("execution", "expression")],
    ids=["same-value", "different-values"],
)
def test_second_declaration_reports_duplicate(tmp_path, first, second):
    text = (
        "# fixture spec\n"                       # 1
        "\n"                                     # 2
        "**Flow Class**: {first}\n"              # 3
        "\n"                                     # 4
        "**Flow Class**: {second}\n"             # 5
        "\n"                                     # 6
        "## Related Feature *(mandatory)*\n"     # 7
    ).format(first=first, second=second)
    repo = _repo_with(tmp_path, "fx-dup", text)

    proc = _lookup(repo, "spec:fx-dup")

    # The diagnostic names the second (offending) line and its value; both line
    # numbers appear so the author can see the two sources of truth.
    _assert_author_error(
        proc,
        "declaration-duplicate",
        name="fx-dup",
        line_numbers={3, 5},
        value_fragment=second,
    )


def test_duplicate_outranks_misplaced_for_the_same_root_cause(tmp_path):
    text = (
        "# fixture spec\n"                      # 1
        "\n"                                    # 2
        "**Flow Class**: execution\n"           # 3
        "\n"                                    # 4
        "## Related Feature *(mandatory)*\n"    # 5
        "\n"                                    # 6
        "**Flow Class**: execution\n"           # 7
    )
    repo = _repo_with(tmp_path, "fx-both", text)

    proc = _lookup(repo, "spec:fx-both")

    _assert_author_error(
        proc, "declaration-duplicate", name="fx-both", line_numbers={3, 7}
    )
    assert "declaration-misplaced" not in proc.stderr, (
        "one root cause is reported once — duplicate outranks misplaced"
    )


# --------------------------------------------------------------------------- #
# D. the four codes sit in exit 1, never in exit 2
# --------------------------------------------------------------------------- #
def test_the_four_author_error_codes_never_collapse_into_exit_2(tmp_path):
    fixtures = {
        "fx-invalid": ("# f\n\n**Flow Class**: expressive\n", "invalid-class"),
        "fx-malformed": ("# f\n\n**Flow Class**：execution\n", "declaration-malformed"),
        "fx-dup": (
            "# f\n\n**Flow Class**: execution\n\n**Flow Class**: execution\n",
            "declaration-duplicate",
        ),
        "fx-misplaced": (
            "# f\n\n## Related Feature *(mandatory)*\n\n**Flow Class**: execution\n",
            "declaration-misplaced",
        ),
    }
    codes = set()
    for name, (text, expected) in fixtures.items():
        repo = _repo_with(tmp_path / name, name, text)
        proc = _lookup(repo, "spec:%s" % name)
        assert proc.returncode == 1, (name, proc.returncode, proc.stderr)
        codes.add(_json(proc)["error"]["label"])
        assert _json(proc)["error"]["label"] == expected
    assert codes == set(AUTHOR_ERROR_CODES)


def test_absent_field_is_not_an_author_error(tmp_path):
    repo = _repo_with(
        tmp_path,
        "fx-absent",
        "# fixture spec\n\n## Related Feature *(mandatory)*\n\n**Feature ID**: 999\n",
    )

    proc = _lookup(repo, "spec:fx-absent")

    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record["flow_class"] == "execution"
    assert record["source"] == "default"
    assert record["marker"], "the undeclared case must carry the default marker"
    label = (record.get("error") or {}).get("label")
    assert label in (None, "declaration-absent"), (
        "the only admissible advisory on an absent field is declaration-absent"
    )


# --------------------------------------------------------------------------- #
# E. templates/requirements-template.md — position and placeholder form
# --------------------------------------------------------------------------- #
def _template_lines() -> list[str]:
    assert TEMPLATE.is_file(), "requirements template missing: %s" % TEMPLATE
    return TEMPLATE.read_text(encoding="utf-8").splitlines()


def test_template_carries_the_field_between_status_and_input():
    lines = _template_lines()
    status = next(i for i, line in enumerate(lines) if line.startswith("**Status**:"))
    field = next(
        (i for i, line in enumerate(lines) if line.startswith("**Flow Class**: ")),
        None,
    )
    assert field is not None, (
        "the requirements template must carry one `**Flow Class**: ` field line"
    )
    input_line = next(i for i, line in enumerate(lines) if line.startswith("**Input**:"))
    assert status < field < input_line, (
        "the field belongs after `**Status**:` and before `**Input**:` "
        "(status=%d field=%d input=%d)" % (status, field, input_line)
    )


def test_template_placeholder_does_not_prefill_a_class():
    lines = _template_lines()
    line = next(line for line in lines if line.startswith("**Flow Class**: "))
    value = line[len("**Flow Class**: "):]
    assert value.strip(), "the field value must be a visible placeholder"
    assert value.strip() not in {"execution", "expression"}, (
        "the template must not pre-fill one of the closed values"
    )
    assert value.strip().startswith("[") and value.strip().endswith("]"), (
        "the placeholder form follows the template's `[PLACEHOLDER]` convention; "
        "got %r" % value
    )
    assert line == line.rstrip(), (
        "the field line must not carry trailing whitespace — a copied line would "
        "immediately be declaration-malformed"
    )


def test_template_carries_no_criteria_or_how_to_decide_text():
    text = TEMPLATE.read_text(encoding="utf-8")
    for token in ("behavior-oracle", "reader-oracle", "mixed-oracle"):
        assert token not in text, (
            "the template must not restate the classification criteria (%r)" % token
        )
    assert not re.search(r"^[^\n]*(判据|如何判定)", text, re.MULTILINE), (
        "the template must not carry a how-to-decide sentence"
    )


# --------------------------------------------------------------------------- #
# F. single source of truth — index and detail carry no value
# --------------------------------------------------------------------------- #
def test_feature_index_has_no_class_column():
    text = FEATURE_INDEX.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        for cell in cells:
            assert cell not in {"flow_class", "Flow Class"}, (
                "the feature index must not gain a class column (C-007); "
                "header row: %r" % line
            )


def test_feature_detail_stores_no_class_value():
    text = FEATURE_DETAIL.read_text(encoding="utf-8")
    assert not re.search(r"^\s*\*\*Flow Class\*\*:", text, re.MULTILINE), (
        "the feature detail must not carry a second declaration line"
    )
    assert not re.search(r"^\s*(?:[-*]\s*)?flow_class\s*[:=]", text, re.MULTILINE), (
        "the feature detail must not store the class value; at most a pointer"
    )
