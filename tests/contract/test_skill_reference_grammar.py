"""Contract tests for Feature 082 US5 — the owner's grammar (T025).

Owns the GR-01 … GR-06 text legs of
``.specify/specs/082-mechanism-policy-separation/contracts/skill-reference.contract.md``
against ``shared/definitions/skill-reference-definitions.md`` (GR-08's reference
coordinate: the framework-source path, never the generated mirror).

Legs:

* **GR-01** — the head declares the four owned fact groups and the two not-owned
  facts with their owner paths, and every declaration has a landing section.
* **GR-02** — ``§ Accepted forms`` holds all six rows, literal-equal to
  ``data-model.md`` E-8, and declares the set closed.
* **GR-03** — ``§ Normalization`` maps one-to-one onto NP-1 … NP-8, with NP-3 and
  NP-4 ordered before NP-6, and the order is declared non-exchangeable.
* **GR-03 / GR-04** — the output is the closed three values with no fourth, and the
  paired report carries raw + normalized + decision class.
* **GR-03** — the two-pass case rule closes a multi-hit as the ``dual-layer`` failure.
* **GR-06** — the failure table has exactly four rows with the E-10 report items.

Red-first (Constitution IV / GM-11): the owner document predates this module, so the
legs go red on a missing or drifted shape, never on a collection error — every read
goes through :func:`_read`, which reports ``artifact missing`` instead of raising
``FileNotFoundError``. Each leg carries a GM-07 negative case that mutates a
``tmp_path`` copy and asserts the same assertion function turns red.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER_REL = Path("shared/definitions/skill-reference-definitions.md")
DATAMODEL_REL = Path(".specify/specs/082-mechanism-policy-separation/data-model.md")

#: § Normalization — the eight steps, in the only order the owner may state.
NORMALIZATION_STEPS = tuple("NP-%d" % i for i in range(1, 9))

#: § Acceptance — the closed three-valued output (GR-04); there is no fourth.
OUTCOMES = ("command-surface", "skill", "failure")

#: § Failure semantics — the four classes, order as the owner's table lists them.
FAILURE_CLASSES = ("zero-hit", "out-of-ladder", "unreadable", "dual-layer")

#: Required report items per class, literal with ``data-model.md`` E-10.
REQUIRED_REPORT_ITEMS = {
    "zero-hit": ("raw", "normalized", "searched"),
    "out-of-ladder": ("path", "known location"),
    "unreadable": ("path", "defect"),
    "dual-layer": ("candidate",),
}

#: GR-01 — the four owned fact groups, each with its landing section heading.
OWNED_FACTS = (
    ("accepted forms", "Accepted forms"),
    ("normalization order", "Normalization"),
    ("disambiguation rules", "Disambiguation rules"),
    ("failure semantics", "Failure semantics"),
)

#: GR-01 — the two facts this file does not own, with the owner path it must name.
NOT_OWNED_FACTS = {
    "position ladder": "skills/internal/run-skills/SKILL.md",
    "mirror generation": "scripts/python/sync-mirrors.py",
}

#: A step row's leading cell, ``| **NP-3** |`` — the step id is taken from the label, so
#: swapping two rows' positions moves their ids with them (an id read before the bold
#: marker would stay pinned to the row and hide the move).
_NP_ROW_RE = re.compile(r"^\|\s*\**(NP-\d)\**\s*\|", re.MULTILINE)
_FORM_ROW_RE = re.compile(r"^\|\s*([a-z][a-z ]*?)\s*\|", re.MULTILINE)


def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """Return the body of ``## <heading>`` (fenced code inside the body is kept)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## " + heading:
            start = i
            break
    assert start is not None, "artifact missing: § %s" % heading
    body = [lines[start]]
    in_fence = False
    for line in lines[start + 1:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _head(text: str, lines: int = 12) -> str:
    return "\n".join(text.splitlines()[:lines])


def _plain(text: str) -> str:
    """Drop the Markdown emphasis markers; case folding is the caller's business."""
    return text.replace("*", "").replace("`", "")


def _names(text: str, fact: str) -> bool:
    """Does the prose name ``fact``, ignoring the emphasis markers?"""
    return fact in _plain(text).lower()


def _table_rows(section_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_fence = False
    for line in section_text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows


# --------------------------------------------------------------------------- #
# GR-01 — head ownership declaration
# --------------------------------------------------------------------------- #
def assert_head_ownership(text: str) -> list[str]:
    problems: list[str] = []
    head = _head(text)
    for fact, landing in OWNED_FACTS:
        # The declaration must be in the head's *prose*: a fact named only inside the
        # literal ``§ Normalization`` / ``§ Accepted forms`` landing pointers would be a
        # declared-but-unowned fact group.
        if not _names(head, fact):
            problems.append("the head does not name the owned fact group %r" % fact)
        try:
            body = _section(text, landing)
        except AssertionError:
            problems.append("owned fact %r declares landing § %r, which does not exist "
                            "(dangling ownership declaration)" % (fact, landing))
            continue
        if not body.strip():
            problems.append("landing section § %s is empty" % landing)
    for fact, owner_path in NOT_OWNED_FACTS.items():
        if owner_path not in head:
            problems.append("the head does not hand %r to its owner path %r"
                            % (fact, owner_path))
    # GR-01's own contract text: the head declares itself by the literal ``single source
    # of truth`` (the emphasis markers are Markdown, not part of the literal).
    if "single source of truth" not in _plain(head).lower():
        problems.append("the head does not declare itself the single source of truth")
    return problems


def test_gr01_head_declares_owned_and_not_owned_facts_with_landings():
    problems = assert_head_ownership(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "GR-01 violations:\n- " + "\n- ".join(problems)


def test_gr01_negative_case_dropping_a_not_owned_path_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    mutated = text.replace(NOT_OWNED_FACTS["mirror generation"], "", 1)
    assert mutated != text, "artifact missing: the head names no mirror owner to drop"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_head_ownership(_read(copied))
    assert any("mirror generation" in p for p in problems), (
        "the negative case did not turn the head-ownership assertion red")


def test_gr01_negative_case_removing_a_landing_section_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    mutated = text.replace("## Disambiguation rules", "## Disambiguation", 1)
    assert mutated != text, "artifact missing: no § Disambiguation rules heading to rename"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_head_ownership(_read(copied))
    assert any("dangling ownership declaration" in p for p in problems), (
        "the negative case did not turn the landing-section assertion red")


# --------------------------------------------------------------------------- #
# GR-02 — accepted forms
# --------------------------------------------------------------------------- #
def _e8_forms(datamodel: str) -> list[tuple[str, str]]:
    """The six (form, example) pairs of ``data-model.md`` E-8, read, never retyped."""
    block = _section(datamodel, "E-8 — 技能引用（Skill Reference）")
    start = block.find("**封闭接受形式集合**")
    assert start != -1, "artifact missing: data-model E-8 has no closed-form table"
    rows = _table_rows(block[start:])
    # The example is the code span the cell opens with; any trailing prose in the cell
    # (E-8's "(a trailing `/` is allowed)") is a remark, not part of the form literal.
    pairs = []
    for cells in rows[1:]:
        if len(cells) < 3:
            continue
        span = re.match(r"`([^`]+)`", cells[1])
        assert span, "artifact missing: data-model E-8 example %r is not a code span" % cells[1]
        pairs.append((cells[0], span.group(1)))
    forms = [p[0] for p in pairs]
    assert forms[:6] == ["bare name", "slash reference", "at reference",
                         "labelled reference", "canonical path", "directory path"], (
        "artifact missing: data-model E-8 no longer lists the six forms in order: %r" % forms)
    return pairs[:6]


def assert_accepted_forms(text: str, datamodel: str) -> list[str]:
    problems: list[str] = []
    try:
        section = _section(text, "Accepted forms")
    except AssertionError as exc:
        return ["artifact missing: § Accepted forms (%s)" % exc]
    rows = _table_rows(section)
    assert rows, "artifact missing: § Accepted forms holds no table"
    header, body = rows[0], rows[1:]
    if [h.lower() for h in header[:3]] != ["form", "example", "meaning"]:
        problems.append("§ Accepted forms header is %r, not | form | example | meaning |"
                        % header[:3])
    e8 = _e8_forms(datamodel)
    if len(body) != 6:
        problems.append("§ Accepted forms has %d rows, not the six of E-8" % len(body))
    for i, (form, example) in enumerate(e8):
        if i >= len(body):
            problems.append("§ Accepted forms is missing the %r row" % form)
            continue
        cells = body[i]
        if cells[0] != form:
            problems.append("§ Accepted forms row %d is %r, not the E-8 form %r"
                            % (i + 1, cells[0], form))
        if len(cells) < 2 or cells[1].strip("`") != example:
            problems.append("§ Accepted forms %r example is %r, not the E-8 literal %r"
                            % (form, cells[1] if len(cells) > 1 else "", example))
        if len(cells) < 3 or not cells[2].strip():
            problems.append("§ Accepted forms %r row carries no meaning" % form)
    if "closed" not in section:
        problems.append("§ Accepted forms does not declare the set closed")
    return problems


def test_gr02_accepted_forms_are_six_and_literal_with_e8():
    problems = assert_accepted_forms(
        _read(REPO_ROOT / OWNER_REL), _read(REPO_ROOT / DATAMODEL_REL))
    assert not problems, "GR-02 violations:\n- " + "\n- ".join(problems)


def test_gr02_negative_case_dropping_one_accepted_form_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    mutated = re.sub(r"^\| at reference \|.*\n", "", text, count=1, flags=re.MULTILINE)
    assert mutated != text, "artifact missing: § Accepted forms has no 'at reference' row"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_accepted_forms(_read(copied), _read(REPO_ROOT / DATAMODEL_REL))
    assert any("at reference" in p for p in problems), (
        "the negative case did not turn the accepted-form assertion red")


# --------------------------------------------------------------------------- #
# GR-03 — the normalization order
# --------------------------------------------------------------------------- #
def normalization_order(text: str) -> list[str]:
    """The step ids in the order § Normalization states them."""
    section = _section(text, "Normalization")
    return _NP_ROW_RE.findall(section)


def assert_normalization_order(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Normalization")
    order = normalization_order(text)
    if sorted(order) != sorted(NORMALIZATION_STEPS):
        problems.append("§ Normalization states %r, not the eight steps NP-1 … NP-8"
                        % order)
    if len(set(order)) != len(order):
        problems.append("§ Normalization states a step twice: %r" % order)
    if set(order) == set(NORMALIZATION_STEPS):
        for before in ("NP-3", "NP-4"):
            if order.index(before) > order.index("NP-6"):
                problems.append("%s is stated after NP-6 — the strip steps must run "
                                "before the channel test" % before)
    if "not exchangeable" not in section:
        problems.append("§ Normalization does not declare the step order non-exchangeable")
    return problems


def test_gr03_normalization_steps_are_one_to_one_with_np1_to_np8():
    problems = assert_normalization_order(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "GR-03 violations:\n- " + "\n- ".join(problems)


def _swap_rows(text: str, left: str, right: str) -> str:
    """Exchange the two table rows whose leading cell is ``left`` / ``right``."""
    lines = text.splitlines(keepends=True)
    body = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")]
    assert body, "artifact missing: § Normalization has no table rows"
    first, last = body[0], body[-1]
    found = {}
    for i in range(first, last + 1):
        label = _NP_ROW_RE.match(lines[i].lstrip())
        if label and label.group(1) in (left, right):
            found[label.group(1)] = i
    assert set(found) == {left, right}, "artifact missing: no %s / %s rows to swap" % (
        left, right)
    # The label moves with the row: each row keeps its own action text, so exchanging
    # the two lines is the whole swap (replacing the id inside a moved line would leave
    # every id pinned to its old position).
    a, b = found[left], found[right]
    lines[a], lines[b] = lines[b], lines[a]
    return "".join(lines)


def test_gr03_negative_case_swapping_two_steps_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    order = normalization_order(text)
    # Move a strip step behind the channel test: the exact shape the owner forbids.
    pair = next(((a, b) for a in ("NP-3", "NP-4") for b in ("NP-6", "NP-7", "NP-8")
                 if a in order and b in order and order.index(a) < order.index(b)), None)
    assert pair is not None, (
        "artifact missing: no strip step (NP-3 / NP-4) can be found after a later step, "
        "so the negative case has nothing to swap: %r" % order)
    mutated = _swap_rows(text, pair[0], pair[1])
    assert mutated != text, "artifact missing: the swap changed nothing"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_normalization_order(_read(copied))
    assert any("must run before the channel test" in p for p in problems), (
        "the negative case did not turn the ordering assertion red: %r" % problems)


# --------------------------------------------------------------------------- #
# GR-03 / GR-04 — the closed three-value output and the paired report
# --------------------------------------------------------------------------- #
def assert_output_shape(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Normalization")
    table = section[section.index("**Output shape**"):]
    rows = _table_rows(table)
    stated = {cells[0].strip("`* ") for cells in rows[1:]}
    for value in OUTCOMES:
        if value not in stated:
            problems.append("the output shape does not carry the value %r" % value)
    survivors = {v for v in stated if v and not v.startswith("NP-")} - set(OUTCOMES)
    if survivors:
        problems.append("the output shape carries a fourth value: %r" % sorted(survivors))
    if "no fourth value" not in section:
        problems.append("the output shape is not declared closed ('no fourth value')")
    for needle in ("raw identifier", "normalized identifier", "decision class"):
        if needle not in section:
            problems.append("the paired report is missing %r" % needle)
    return problems


def test_gr0304_output_is_the_closed_three_values_and_paired(tmp_path):
    problems = assert_output_shape(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "GR-03/GR-04 violations:\n- " + "\n- ".join(problems)


def test_gr0304_negative_case_adding_a_fourth_value_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    anchor = "| `failure` |"
    assert anchor in text, "artifact missing: the output table has no `failure` row"
    mutated = text.replace(anchor, "| `raw` | return the input unchanged |\n" + anchor, 1)
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_output_shape(_read(copied))
    assert any("fourth value" in p for p in problems), (
        "the negative case did not turn the closed-output assertion red")


# --------------------------------------------------------------------------- #
# GR-03 — the two-pass case rule
# --------------------------------------------------------------------------- #
def assert_case_rule(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Normalization")
    if "only on zero hits" not in section:
        problems.append("the case rule does not stop the insensitive pass at zero hits")
    if "case-insensitive pass" not in section or "more than one" not in section:
        problems.append("the case rule does not state the multi-hit condition")
    if "`dual-layer` failure" not in section:
        problems.append("a multi-hit case pass is not closed as the `dual-layer` failure")
    if "never pick one" not in section:
        problems.append("the case rule does not forbid picking one candidate")
    return problems


def test_gr03_two_pass_case_rule_closes_a_multi_hit_as_failure():
    problems = assert_case_rule(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "GR-03 violations:\n- " + "\n- ".join(problems)


def test_gr03_negative_case_relaxing_the_case_rule_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    mutated = text.replace("never pick one", "pick the nearest one", 1)
    assert mutated != text, "artifact missing: the case rule states no 'never pick one'"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_case_rule(_read(copied))
    assert any("forbid" in p for p in problems), (
        "the negative case did not turn the case-rule assertion red")


# --------------------------------------------------------------------------- #
# GR-06 — the failure table
# --------------------------------------------------------------------------- #
def assert_failure_table(text: str) -> list[str]:
    problems: list[str] = []
    try:
        section = _section(text, "Failure semantics")
    except AssertionError as exc:
        return ["artifact missing: § Failure semantics (%s)" % exc]
    rows = _table_rows(section)
    assert rows, "artifact missing: § Failure semantics holds no table"
    body = rows[1:]
    names = [cells[0].strip("`* ") for cells in body]
    if names != list(FAILURE_CLASSES):
        problems.append("§ Failure semantics rows are %r, not the four of E-10 %r"
                        % (names, list(FAILURE_CLASSES)))
    for cells in body:
        name = cells[0].strip("`* ")
        if name not in REQUIRED_REPORT_ITEMS or len(cells) < 3:
            continue
        for item in REQUIRED_REPORT_ITEMS[name]:
            if item not in cells[2]:
                problems.append("%s does not require %r among its report items"
                                % (name, item))
    if "mutually exclusive" not in section:
        problems.append("the failure table does not declare the four classes mutually "
                        "exclusive")
    return problems


def test_gr06_failure_table_has_four_rows_with_report_items():
    problems = assert_failure_table(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "GR-06 violations:\n- " + "\n- ".join(problems)


def test_gr06_negative_case_relabelling_a_class_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    mutated = text.replace("| `unreadable` |", "| `unreadable-dir` |", 1)
    assert mutated != text, "artifact missing: the failure table has no `unreadable` row"
    copied = tmp_path / OWNER_REL.name
    copied.write_text(mutated, encoding="utf-8")
    problems = assert_failure_table(_read(copied))
    assert any("not the four of E-10" in p for p in problems), (
        "the negative case did not turn the failure-table assertion red")
