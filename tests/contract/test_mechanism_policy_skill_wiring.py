"""Contract tests for Feature 082 US1/US2 — meta-skill wiring (T009, T013).

Owns the *wiring* face of
``.specify/specs/082-mechanism-policy-separation/contracts/skill-wiring.contract.md``
that ``tasks.md`` T009 / T013 / T017 name. The judgement criteria themselves belong
to ``shared/definitions/mechanism-policy-definitions.md`` (the owner); this module
only pins that each consumer **points at** the owner from the right place, once,
and that it copies none of the owner's tables (SW-01…SW-04).

Legs:

* **SW-01 (`create-skills` § 6, T009)** — exactly one ``Minimum checks`` item
  carries the literal ``Mechanism / policy separation``, it is appended after the
  previous last item, it holds one judgement sentence covering **both** sides plus
  an anchor to ``./references/mechanism-policy-check.md`` and an owner-path
  reference, and it inlines no owner table row (the maximum permitted inline is one
  keyword phrase per misplacement class).
* **SW-01 reference doc (T009/T012)** — ``create-skills/references/
  mechanism-policy-check.md`` exists and stays within its 12-line judgement-step
  budget without restating the owner's symptom table.
* **SW-02 (`improve-skills` § 2 / § 3, T013)** — one survey question reading the
  referenced environment files together with the body and answering "where does the
  policy take its value"; the ``policy source missing or ambiguous`` candidate
  category carrying the freeze discipline, the prohibition on inheriting a
  hard-coded value and the run-time direction; the batch statement lives in
  ``./references/loop-playbook.md`` with only a pointer in the body.
* **SW-04 side-effect ordering (T017)** — every named wiring point precedes its
  side effect, names the owner's Consumption Contract by path, restates no prompt
  wording of its own, and keeps the missing-policy and environment-error wordings
  distinguishable.

Red-first (Constitution IV / GM-01): before T011 / T014 land, the legs red as
"artifact missing" or as a moved-away assertion — never as an import or collection
error. Each helper asserts the artifact path first.

Every leg that asserts a shape also carries a **negative case** (GM-07): the same
assertion function is run against a ``tmp_path`` copy that is broken on purpose and
must turn red. A shape assertion that cannot go red proves nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER_REL = Path("shared/definitions/mechanism-policy-definitions.md")
OWNER = REPO_ROOT / OWNER_REL
OWNER_LITERAL = "shared/definitions/mechanism-policy-definitions.md"

CREATE_REL = Path("skills/external/create-skills/SKILL.md")
IMPROVE_REL = Path("skills/external/improve-skills/SKILL.md")
MERGE_REL = Path("skills/external/merge-skills/SKILL.md")
CHECK_DOC_REL = Path("skills/external/create-skills/references/mechanism-policy-check.md")
PLAYBOOK_REL = Path("skills/external/improve-skills/references/loop-playbook.md")

JUDGEMENT_LITERAL = "Mechanism / policy separation"
CANDIDATE_LITERAL = "policy source missing or ambiguous"

# The only inline content SW-01 permits from the owner: one keyword phrase per
# misplacement class. Anything longer is a copied table row (FR-015).
MECHANISM_KEYWORDS = ("environment path", "reusable logic")
POLICY_KEYWORDS = ("environment path", "hard-coded")


# --------------------------------------------------------------------------- #
# helpers — text extraction, deliberately small and shared by both legs
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    """Return the body of the first ``##``/``###`` heading, or ordered step, matching the prefix."""
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if 2 <= depth <= 3 and stripped.startswith(" " + heading_prefix):
            start, level = i, depth
            break
        if re.match(r"^\d+\.\s", line) and heading_prefix.lstrip("0123456789. ") in line:
            start, level = i, 0
            break
    assert start is not None, "section not found: %r" % heading_prefix
    body = [lines[start]]
    in_fence = False
    for line in lines[start + 1:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        is_heading = line.startswith("#") and stripped.startswith(" ")
        if not in_fence and is_heading and depth == level:
            break
        if not in_fence and level == 0 and is_heading and depth <= 2:
            break
        if not in_fence and level == 0 and re.match(r"^\d+\.\s", line):
            break
        if not in_fence and level == 0 and re.match(r"^##\s", line):
            break
        body.append(line)
    return "\n".join(body)


def _checkbox_items(section_text: str) -> list[str]:
    """Return each ``- [ ]`` item of a checklist section (continuation lines folded)."""
    items: list[str] = []
    for line in section_text.splitlines():
        if line.lstrip().startswith("- ["):
            items.append(line.strip())
        elif items and line.startswith((" ", "\t")) and line.strip():
            items[-1] += " " + line.strip()
    return items


def _table_rows(section_text: str) -> list[str]:
    return [line for line in section_text.splitlines() if line.lstrip().startswith("|")]


# --------------------------------------------------------------------------- #
# SW-01 — create-skills § 6 Minimum checks
# --------------------------------------------------------------------------- #
def assert_create_skills_judgement(path: Path) -> list[str]:
    """Assert the SW-01 item shape in ``path`` and return the list of violations."""
    text = _read(path)
    problems: list[str] = []
    section = _section(text, "6. Validate the Skill")
    items = _checkbox_items(section)
    assert items, "artifact missing: %s § 6 carries no checklist items" % path

    carries = [i for i in items if JUDGEMENT_LITERAL in i]
    if len(carries) != 1:
        problems.append(
            "expected exactly one Minimum checks item carrying %r, found %d"
            % (JUDGEMENT_LITERAL, len(carries))
        )
    if carries:
        item = carries[0]
        if item is not items[-1]:
            problems.append(
                "the judgement item is not the last Minimum checks item — SW-01 "
                "appends after the previous last item"
            )
        lowered = item.lower()
        if not any(k.lower() in lowered for k in MECHANISM_KEYWORDS):
            problems.append(
                "the judgement item names no mechanism-side misplacement "
                "(expected one of %r); a policy-only judgement misses US1 scenario 2"
                % (MECHANISM_KEYWORDS,)
            )
        if not any(k.lower() in lowered for k in POLICY_KEYWORDS):
            problems.append(
                "the judgement item names no policy-side misplacement "
                "(expected one of %r); both sides must be judged" % (POLICY_KEYWORDS,)
            )
        if "continue to judge the other side" not in lowered:
            problems.append(
                "the judgement item carries no through-line that keeps judging the "
                "other side after a hit (US1 scenario 2 needs both sides, not first-hit)"
            )
        if "./references/mechanism-policy-check.md" not in item:
            problems.append(
                "the judgement item carries no anchor to ./references/mechanism-policy-check.md"
            )
        if OWNER_LITERAL not in item:
            problems.append(
                "the judgement item carries no owner-path reference (%s)" % OWNER_LITERAL
            )
        if item.count("|") >= 2:
            problems.append(
                "the judgement item inlines a table row — the maximum permitted inline "
                "is one keyword phrase per misplacement class"
            )
        if len(item) > 900:
            problems.append(
                "the judgement item is %d chars — long enough to be a copied rule set, "
                "not one executable judgement sentence" % len(item)
            )
    return problems


def test_sw01_create_skills_carries_one_judgement_item():
    problems = assert_create_skills_judgement(REPO_ROOT / CREATE_REL)
    assert not problems, "SW-01 violations:\n- " + "\n- ".join(problems)


def test_sw01_negative_case_deleting_the_item_turns_red(tmp_path):
    source = REPO_ROOT / CREATE_REL
    text = _read(source)
    section = _section(text, "6. Validate the Skill")
    item = [i for i in _checkbox_items(section) if JUDGEMENT_LITERAL in i]
    assert item, "artifact missing: cannot build the negative case before the item exists"
    mutated = "\n".join(line for line in text.splitlines() if JUDGEMENT_LITERAL not in line)
    assert mutated != text, "the mutation removed nothing"
    broken = tmp_path / "SKILL.md"
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_create_skills_judgement(broken)
    assert any("exactly one" in p for p in problems), (
        "the negative case did not turn the assertion red — a shape check that "
        "survives its subject's removal proves nothing"
    )


# --------------------------------------------------------------------------- #
# SW-01 — the reference document's shape
# --------------------------------------------------------------------------- #
REF_STEP_HEADINGS = ("Locate", "Correct")


def assert_check_doc_shape(path: Path, owner_text: str) -> list[str]:
    text = _read(path)
    problems: list[str] = []
    lines = [ln for ln in text.splitlines() if ln.strip()]
    judgement_steps = [
        ln for ln in lines
        if re.match(r"^\s*(?:\d+\.|[-*])\s", ln) or ln.startswith("### ")
    ]
    if len(judgement_steps) > 12:
        problems.append(
            "%d judgement-step lines exceeds the 12-line budget of SW-01" % len(judgement_steps)
        )
    for heading in REF_STEP_HEADINGS:
        if heading.lower() not in text.lower():
            problems.append("no %r block — the two misplacement classes need a localisation method" % heading)
    if OWNER_LITERAL not in text:
        problems.append("no owner-path reference (%s)" % OWNER_LITERAL)
    # MUST NOT restate the owner's symptom table: no verbatim symptom-table row.
    owner_symptoms = _section(owner_text, "Misplacement Symptoms")
    owner_rows = {r.strip() for r in _table_rows(owner_symptoms) if r.strip().startswith("| 症状") is False and r.strip().count("|") >= 3}
    for row in owner_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if not cells or not cells[0] or set(cells[0]) <= set("-: "):
            continue
        if cells[0] in text:
            problems.append("restates the owner symptom row %r — SW-01 forbids a second symptom table" % cells[0])
    return problems


def test_sw01_reference_doc_exists_and_stays_in_budget():
    problems = assert_check_doc_shape(REPO_ROOT / CHECK_DOC_REL, _read(REPO_ROOT / OWNER_REL))
    assert not problems, "SW-01 reference-doc violations:\n- " + "\n- ".join(problems)


def test_sw01_negative_case_over_budget_reference_doc_turns_red(tmp_path):
    owner_text = _read(REPO_ROOT / OWNER_REL)
    filler = "\n".join("%d. step %d" % (i, i) for i in range(1, 15))
    broken = tmp_path / "mechanism-policy-check.md"
    broken.write_text(
        "# check\n\n%s\n\n## Locate\n\n## Correct\n\nsee %s\n" % (filler, OWNER_LITERAL),
        encoding="utf-8",
    )
    problems = assert_check_doc_shape(broken, owner_text)
    assert any("12-line budget" in p for p in problems), (
        "the negative case did not turn the step-budget assertion red"
    )


# --------------------------------------------------------------------------- #
# SW-02 — improve-skills § 2 survey question and § 3 candidate category
# --------------------------------------------------------------------------- #
SURVEY_ANCHORS = ("where does the policy take its value", "where the policy takes its value")
FREEZE_ANCHORS = ("freeze", "冻结")
PROHIBITION_ANCHORS = ("MUST NOT inherit", "hard-coded", "硬编码")
DIRECTION_ANCHORS = ("at run time", "run time", "运行时")


def assert_improve_skills_wiring(path: Path) -> list[str]:
    text = _read(path)
    problems: list[str] = []
    survey = _section(text, "2. 调研实现")
    survey_lower = survey.lower()
    if not any(a in survey_lower for a in SURVEY_ANCHORS):
        problems.append(
            "§ 2 carries no survey question answering 'where does the policy take its value'"
        )
    if "environment" not in survey_lower and "环境" not in survey:
        problems.append(
            "§ 2's survey question does not read the referenced environment files together "
            "with the body"
        )
    if OWNER_LITERAL not in survey:
        problems.append("§ 2 carries no owner-path reference (%s)" % OWNER_LITERAL)

    evidence = _section(text, "3. 调研证据")
    if CANDIDATE_LITERAL not in evidence:
        problems.append("§ 3 carries no %r candidate category" % CANDIDATE_LITERAL)
    else:
        para_start = evidence.index(CANDIDATE_LITERAL)
        para = evidence[max(0, para_start - 200): para_start + 600]
        para_lower = para.lower()
        if not any(a in para_lower for a in FREEZE_ANCHORS):
            problems.append(
                "the candidate category does not carry the freeze discipline "
                "('raised before the freeze, never added after it')"
            )
        if not any(a.lower() in para_lower for a in PROHIBITION_ANCHORS):
            problems.append(
                "the candidate carries no prohibition on inheriting a hard-coded value (FR-013)"
            )
        if not any(a.lower() in para_lower for a in DIRECTION_ANCHORS):
            problems.append(
                "the candidate carries no direction to let the policy come from the user or "
                "the environment at run time (FR-013)"
            )
    # Batch mode: the statement lives in the reference, the body keeps a pointer only.
    body_batch = [
        ln for ln in text.splitlines()
        if ("mechanism" in ln.lower() or "机制" in ln) and "batch" in ln.lower() and "once" in ln.lower()
    ]
    if body_batch:
        problems.append(
            "the body restates the batch-mode statement instead of pointing at the reference: %r"
            % body_batch[0][:80]
        )
    if "./references/loop-playbook.md" not in text:
        problems.append("no pointer to ./references/loop-playbook.md")
    return problems


def test_sw02_improve_skills_wiring():
    problems = assert_improve_skills_wiring(REPO_ROOT / IMPROVE_REL)
    assert not problems, "SW-02 violations:\n- " + "\n- ".join(problems)


def test_sw02_batch_statement_lives_in_the_playbook():
    playbook = _read(REPO_ROOT / PLAYBOOK_REL)
    batch = _section(playbook, "Input Contract — batch mode detail")
    lowered = batch.lower()
    assert "mechanism" in lowered and "policy" in lowered, (
        "the batch section carries no mechanism/policy statement — the judgement runs "
        "once for the whole batch"
    )
    assert ("once" in lowered) and ("not repeated per skill" in lowered or "not per skill" in lowered
                                    or "不逐个技能重复" in batch), (
        "the batch statement does not say the judgement runs once and is not repeated per skill"
    )


def test_sw02_negative_case_moving_the_candidate_literal_turns_red(tmp_path):
    text = _read(REPO_ROOT / IMPROVE_REL)
    assert CANDIDATE_LITERAL in text, "artifact missing: cannot build the negative case before the category exists"
    head, _, tail = text.partition(CANDIDATE_LITERAL)
    mutated = head + "policy source unclear" + tail
    broken = tmp_path / "SKILL.md"
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_improve_skills_wiring(broken)
    assert any(CANDIDATE_LITERAL in p for p in problems), (
        "the negative case did not turn the candidate-category assertion red"
    )


# --------------------------------------------------------------------------- #
# SW-04 — every wiring point precedes its side effect (T017)
# --------------------------------------------------------------------------- #
CONSUMPTION_ANCHOR = "§ Consumption Contract"
PROMPT_WORDING_MARKERS = (
    "需要你确认",
    "为什么现在需要",
    "你可以这样给",
)

# The two consumers whose wiring lands in US1 / US2 (T011 / T014). ``merge-skills``
# carries the same obligation but its body is rewritten by T030 (Part 4), so its leg
# is added there — asserting it now would red on an unwritten artifact, not on a defect.
WIRING_POINTS = (
    (CREATE_REL, "SW-04"),
    (IMPROVE_REL, "SW-04"),
)


def assert_wiring_order(path: Path) -> list[str]:
    text = _read(path)
    problems: list[str] = []
    lines = text.splitlines()
    wiring_idx = [i for i, ln in enumerate(lines) if CONSUMPTION_ANCHOR in ln]
    if len(wiring_idx) < 2:
        problems.append(
            "expected at least two references to the owner's %r (the section and its wiring "
            "points), found %d" % (CONSUMPTION_ANCHOR, len(wiring_idx))
        )
    for i in wiring_idx:
        window = "\n".join(lines[max(0, i - 2): i + 3])
        if OWNER_LITERAL not in window:
            problems.append(
                "line %d references %r without the owner path — a section anchor with no "
                "path is not a reference" % (i + 1, CONSUMPTION_ANCHOR)
            )
    for marker in PROMPT_WORDING_MARKERS:
        if marker in text:
            problems.append(
                "restates the owner's prompt skeleton (%r) — consumers point, they never "
                "carry the wording" % marker
            )
    if "environment error" not in text.lower() and "环境错误" not in text:
        problems.append(
            "does not name the environment-error class, so the two error wordings cannot be "
            "told apart at this consumer (FR-007)"
        )
    return problems


@pytest.mark.parametrize("rel", [p[0] for p in WIRING_POINTS], ids=[p[0].parent.name for p in WIRING_POINTS])
def test_sw04_wiring_points_name_the_owner_contract(rel: Path):
    problems = assert_wiring_order(REPO_ROOT / rel)
    assert not problems, "SW-04 violations in %s:\n- %s" % (rel, "\n- ".join(problems))


def test_sw04_negative_case_restating_the_prompt_turns_red(tmp_path):
    text = _read(REPO_ROOT / CREATE_REL)
    broken_text = text + "\n\n需要你确认：<策略项的可读名字>\n"
    broken = tmp_path / "SKILL.md"
    broken.write_text(broken_text, encoding="utf-8")
    problems = assert_wiring_order(broken)
    assert any("prompt skeleton" in p for p in problems), (
        "the negative case did not turn the prompt-restatement assertion red"
    )


def test_sw04_negative_case_unpinned_anchor_turns_red(tmp_path):
    broken = tmp_path / "SKILL.md"
    broken.write_text(
        "writer STOP.\n- 写作前按机制/策略判定的 § Consumption Contract 读-判-停。\n"
        "环境错误：(environment error) 另述。\n",
        encoding="utf-8",
    )
    problems = assert_wiring_order(broken)
    assert any("without the owner path" in p for p in problems), (
        "the negative case did not turn the owner-path assertion red"
    )


# --------------------------------------------------------------------------- #
# SW-04 side-effect-before-check legs (T017) — one scenario table drives both
# the positive assertions and the ordering negative case, so a reordering that
# cannot be detected by the table cannot be asserted by it either.
# --------------------------------------------------------------------------- #
READ_ANCHORS = ("read", "读")
JUDGE_ANCHORS = ("judge", "判")
STOP_ANCHORS = ("stop", "停")
NO_PRODUCT_ANCHORS = ("no half", "no file touched", "no half-edited", "无半成品", "不留半成品")
ENV_ERROR_ANCHORS = ("environment error", "环境错误")

# ``block_start`` marks where a wiring point's text begins when it is not a
# standalone paragraph; ``side_effect`` is the first line of the step whose write
# the point guards. For a wiring point that sits *inside* a numbered step, the
# side effect is the first writing line **after** the point within that step — the
# step heading itself is not a write; a check placed above a *message* bullet (one that
# only states what the check runs before) still has no write between it and the write it
# guards — the probe command itself lives in the message, never in the check's own bullet.
# ``owning_heading`` pins the step the check must sit inside (SW-04 step scope).
WIRING_SCENARIOS = (
    {
        "rel": CREATE_REL,
        "name": "create-skills § 2 writability pre-flight",
        "block_start": "**Both layers before any write**",
        "side_effect": "- **Writability pre-flight (fail fast)**:",
        "owning_heading": "### 2. Determine SKILL_HOME and metadata",
        "side_effect_name": "the pre-flight probe write",
    },
    {
        "rel": CREATE_REL,
        "name": "create-skills § 7 propagate",
        "block_start": "**Before the first edit of § 7 and of § 8**",
        "side_effect": "1. **Guard**:",
        "owning_heading": "### 7. Propagate the Skill",
        "side_effect_name": "§ 7's first edit step",
    },
    {
        "rel": CREATE_REL,
        "name": "create-skills § 8 report completion",
        "block_start": "Before writing the report, re-read this creation's policy items",
        "side_effect": "Summarize:",
        "owning_heading": "### 8. Report completion",
        "side_effect_name": "§ 8's report write",
    },
    {
        "rel": IMPROVE_REL,
        "name": "improve-skills § 7 edit",
        "block_start": "**Both layers before the first edit**",
        "side_effect": "- Edit `SKILL.md` to make the improved behavior executable",
        "owning_heading": "7. **Update the Skill for the next execution**",
        "side_effect_name": "§ 7's first edit line",
    },
    {
        "rel": MERGE_REL,
        "name": "merge-skills § 7 decommission",
        "block_start": "**Both layers before the decommission**",
        "side_effect": "- **Form carriers**:",
        "owning_heading": "### 7. Decommission the source as an independent skill",
        "side_effect_name": "§ 7's first destructive action",
    },
)


# A block ends at a blank line, the next list item / numbered step, or a heading
# — never at an inline-code span (`` \"$SKILL_HOME\" `` is not a line opening).
BLOCK_BOUNDARIES = (
    r"\n[ \t]*\n",
    r"\n[ \t]*[-*] \S",
    r"\n\d+\. ",
    r"\n#{2,6} ",
)


def _block_end(text: str, block: str) -> int:
    """Offset just past ``block``'s last non-blank line (a block cut at a blank line omits it).

    Using the raw block length would leave the newline that closes the paragraph inside the
    scan window, and a paragraph opener such as ``Summarize:`` on the next line would read as
    a stray reading line.
    """
    start = text.index(block)
    return start + len(block.rstrip())


def _block_at(text: str, anchor: str) -> str:
    """Return the block containing ``anchor``: a paragraph, a list item or one step line.

    The block is what the wiring point itself says, so the ordering assertion
    measures the check's own text and never its neighbours': it begins at the
    anchor's line (or at the enclosing list item) and ends at the next blank line,
    list item or numbered step.
    """
    start = text.index(anchor)
    line_start = text.rfind("\n", 0, start) + 1
    prev_line = text.rfind("\n", 0, line_start - 1)
    prev_line_start = prev_line + 1 if prev_line != -1 else 0
    prev_text = text[prev_line_start:line_start].strip()
    if prev_text.startswith("- ") or prev_text.startswith("* "):
        line_start = prev_line_start
    elif prev_text and not prev_text.startswith("#"):
        # a soft-wrapped paragraph line: walk up to its first line
        while prev_text and not prev_text.startswith(("- ", "* ")) and not re.match(r"^\d+\. ", prev_text):
            line_start = prev_line_start
            prev_line = text.rfind("\n", 0, line_start - 1)
            if prev_line == -1:
                line_start = 0
                break
            prev_line_start = prev_line + 1
            prev_text = text[prev_line_start:line_start].strip()
    para_end = len(text)
    for pattern in BLOCK_BOUNDARIES:
        m = re.search(pattern, text[start:])
        if m:
            para_end = min(para_end, start + m.start())
    return text[line_start:para_end]


def _any_anchor(paragraph: str, anchors: tuple) -> bool:
    low = paragraph.lower()
    return any(a in low for a in anchors)


def _structure(text: str) -> "tuple[int, int]":
    """Return ``(fence_end, structural_end)``: the length of the frontmatter fence and of a
    structural prelude (headings, tables, code fences) that a still-unwritten body may open with.

    Only these two regions may precede the first side effect without violating SW-04. Every
    other earlier point is a body location, and a check placed there is misplaced: e.g. the
    § 2 *bullet* that states the rule sits before § 2's own probe-write bullet, while the
    rule's own wording says the check runs **before the writability touch-test** — a check
    asserted at the bullet would pass text that no longer exhibits the contract.
    """
    fence_end = 0
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        offset = len(lines[0])
        for line in lines[1:]:
            offset += len(line)
            if line.strip() == "---":
                fence_end = offset
                break
    pos = fence_end
    in_fence = False
    structural_end = fence_end
    for line in text[fence_end:].splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            pos += len(line)
            structural_end = pos
            continue
        if in_fence:
            pos += len(line)
            structural_end = pos
            continue
        if not stripped or re.match(r"^#{1,6}\s", stripped) or stripped.startswith("|"):
            pos += len(line)
            structural_end = pos
            continue
        break
    return fence_end, structural_end


def assert_wiring_point_matches_contract(path: Path, anchor: str) -> list[str]:
    """Assert one wiring point carries the owner's read-judge-stop shape and wording split.

    Returns the list of violations; the side-effect ordering lives in
    ``assert_wiring_precedes_side_effect`` so each failure names its own cause.
    """
    text = _read(path)
    problems: list[str] = []
    if anchor not in text:
        return ["artifact missing: the wiring point %r is absent" % anchor]
    paragraph = _block_at(text, anchor)
    if OWNER_LITERAL not in paragraph:
        problems.append(
            "wiring point %r does not name the owner's Consumption Contract by path (%r) "
            "— a path reference is the only permitted form" % (anchor, OWNER_LITERAL)
        )
    for marker in PROMPT_WORDING_MARKERS:
        if marker in paragraph:
            problems.append(
                "wiring point %r restates the owner's prompt wording (%r) — the consumer "
                "points at the shape, it never carries it" % (anchor, marker)
            )
    if not _any_anchor(paragraph, READ_ANCHORS):
        problems.append("wiring point %r states no read step — read-judge-stop is a three-step form" % anchor)
    if not _any_anchor(paragraph, JUDGE_ANCHORS):
        problems.append("wiring point %r states no judge step — read-judge-stop is a three-step form" % anchor)
    if not _any_anchor(paragraph, STOP_ANCHORS):
        problems.append("wiring point %r states no stop step — read-judge-stop is a three-step form" % anchor)
    if not _any_anchor(paragraph, NO_PRODUCT_ANCHORS):
        problems.append(
            "wiring point %r does not say the stop leaves no half product (SW-04 / FR-008)" % anchor
        )
    if not re.search(r"before", paragraph, re.IGNORECASE):
        problems.append(
            "wiring point %r contains no ordering word — read-judge-stop MUST sit before the "
            "side effect, and the point itself must say so (SW-04)" % anchor
        )
    if not _any_anchor(paragraph, ENV_ERROR_ANCHORS):
        problems.append(
            "wiring point %r names no environment-error class, so the two error wordings are "
            "not distinguishable there (FR-007)" % anchor
        )
    return problems


GLOBAL_SIDE_EFFECTS = ("**Writability pre-flight (fail fast)**", "Never narrate the document's own history")


def assert_wiring_precedes_side_effect(path: Path, anchor: str, side_effect: str) -> list[str]:
    """Assert the wiring point is the **last** thing before the side effect it guards.

    1. The point must sit inside the step it guards (between that step's heading and the
       next heading of the same or a higher level) — a check parked in an earlier step
       precedes the side effect but no longer guards it.
    2. No other side-effect marker named in the same scenario block may sit between the
       point and its side effect.
    3. Every writing line between the point and the side effect must belong to the
       frontmatter fence, a structural prelude (heading / table / code fence), or the
       point's own paragraph — a check preceded by a write is not "before the write".
    """
    text = _read(path)
    if anchor not in text:
        return ["artifact missing: the wiring point %r is absent" % anchor]
    if side_effect not in text:
        return ["artifact missing: the side-effect anchor %r is absent" % side_effect]
    problems: list[str] = []
    paragraph = _block_at(text, anchor)
    check_start = text.index(paragraph)
    check_end = _block_end(text, paragraph)
    effect_at = text.index(side_effect)
    if check_end > effect_at:
        return [
            "the wiring point %r (ends at offset %d) sits at or after its side effect %r "
            "(offset %d) — the check must precede every write" % (anchor, check_end, side_effect, effect_at)
        ]

    headings = [
        (m.start(), len(m.group(1)))
        for m in re.finditer(r"^(#{2,6})\s.+$", text, re.MULTILINE)
    ]
    step_start = 0
    step_level = 2
    for offset, level in headings:
        if offset <= effect_at:
            step_start, step_level = offset, level
        else:
            break
    if check_end < step_start:
        problems.append(
            "the wiring point %r (offset %d) sits before the heading of the step it guards "
            "(offset %d) — a check parked in an earlier step precedes the write but no longer "
            "guards it (SW-04 places the check inside the step whose side effect it precedes)"
            % (anchor, check_start, step_start)
        )
    step_end = len(text)
    for offset, level in headings:
        if offset > effect_at and level <= step_level:
            step_end = offset
            break
    own_paragraph = _block_at(text, anchor)
    for marker in GLOBAL_SIDE_EFFECTS:
        at = text.find(marker)
        while at != -1:
            between_anchor_and_effect = check_end < at < effect_at
            inside_own_paragraph = text.index(own_paragraph) <= at < check_end
            if between_anchor_and_effect and not inside_own_paragraph:
                problems.append(
                    "side effect %r sits between the wiring point %r and its side effect %r "
                    "— the point must sit directly before the write it guards" % (marker, anchor, side_effect)
                )
            at = text.find(marker, at + 1)

    fence_end, structural_end = _structure(text)
    body = text[check_end:effect_at]
    written: list[str] = []
    for line in body.splitlines():
        line_at = text.index(line, check_end) if line else check_end
        if not line.strip() or line_at < structural_end:
            continue
        written.append(line.strip())
    if written:
        problems.append(
            "reading lines sit between the wiring point %r and its side effect %r (%r) — the "
            "check must be the last thing before the write, not merely before it somewhere"
            % (anchor, side_effect, written[0][:90])
        )
    return problems


def _owning_step(text: str, offset: int) -> int:
    """Offset of the heading of the step containing ``offset``."""
    start = 0
    for m in re.finditer(r"^(#{2,6})\s.+$", text, re.MULTILINE):
        if m.start() <= offset:
            start = m.start()
        else:
            break
    return start


def assert_wiring_sits_in_its_step(path: Path, anchor: str, heading, side_effect: str) -> list[str]:
    """Assert the point sits inside the step it guards, not in an earlier step that precedes the write.

    ``heading`` pins the step exactly (a heading literal); without it the point must at least
    sit inside the step that contains its side effect. Both forms run on the live tree.
    """
    text = _read(path)
    if anchor not in text:
        return ["artifact missing: the wiring point %r is absent" % anchor]
    problems: list[str] = []
    offset = text.index(anchor)
    step = _owning_step(text, offset)
    if heading:
        expected = text.find(heading)
        if expected == -1:
            return ["artifact missing: the step heading %r is absent" % heading]
        if step != expected:
            problems.append(
                "the wiring point %r sits in the step starting at offset %d, not in %r — a "
                "check parked in an earlier step precedes every write without guarding one"
                % (anchor, step, heading)
            )
    if side_effect in text:
        effect_step = _owning_step(text, text.index(side_effect))
        if offset < effect_step:
            problems.append(
                "the wiring point %r sits before the heading of the step it guards (offset %d)"
                % (anchor, effect_step)
            )
    return problems


def _variant_root(tmp_path, rel: Path) -> Path:
    """A ``tmp_path`` tree holding ``rel``'s current content; sibling anchors keep resolving."""
    copy = tmp_path / rel
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_text(_read(REPO_ROOT / rel), encoding="utf-8")
    return copy


def _move_block_below(path: Path, anchor: str, below: str) -> None:
    """Move ``anchor``'s paragraph to just after the line carrying ``below`` (in place)."""
    text = _read(path)
    paragraph = _block_at(text, anchor)
    without = text.replace(paragraph, "", 1)
    assert without != text, "artifact missing: the wiring paragraph could not be lifted out"
    effect_at = without.index(below)
    line_end = without.index("\n", effect_at) + 1
    path.write_text(without[:line_end] + paragraph + "\n" + without[line_end:], encoding="utf-8")


@pytest.mark.parametrize(
    "scenario",
    list(WIRING_SCENARIOS),
    ids=["%s::%s" % (s["rel"].parent.name, s["name"].split(" ")[-1]) for s in WIRING_SCENARIOS],
)
def test_sw04_wiring_point_shape_and_ordering(scenario):
    path = REPO_ROOT / scenario["rel"]
    problems = assert_wiring_point_matches_contract(path, scenario["block_start"])
    problems += assert_wiring_precedes_side_effect(path, scenario["block_start"], scenario["side_effect"])
    assert not problems, "SW-04 violations in %s (%s):\n- %s" % (
        scenario["rel"], scenario["name"], "\n- ".join(problems)
    )


def test_sw04_negative_case_reordering_a_wiring_point_turns_red(tmp_path):
    """Move improve-skills' § 7 check below its first edit line; the ordering assertion must go red."""
    scenario = next(s for s in WIRING_SCENARIOS if s["name"] == "improve-skills § 7 edit")
    broken = _variant_root(tmp_path, scenario["rel"])
    _move_block_below(broken, scenario["block_start"], scenario["side_effect"])
    problems = assert_wiring_precedes_side_effect(broken, scenario["block_start"], scenario["side_effect"])
    assert any("sits at or after its side effect" in p for p in problems), (
        "the negative case did not turn the ordering assertion red: %s" % problems
    )
    shape = assert_wiring_point_matches_contract(broken, scenario["block_start"])
    assert not shape, "the reordered copy must keep the paragraph's shape intact:\n- %s" % "\n- ".join(shape)


def test_sw04_negative_case_check_parked_in_an_earlier_step_turns_red(tmp_path):
    """Lift create-skills' § 7 check into § 2 — before every write, yet no longer guarding § 7."""
    scenario = next(s for s in WIRING_SCENARIOS if s["name"] == "create-skills § 7 propagate")
    broken = _variant_root(tmp_path, scenario["rel"])
    text = _read(broken)
    paragraph = _block_at(text, scenario["block_start"])
    earlier = _block_at(text, "**Both layers before any write**")
    parked = text.replace(paragraph, "", 1).replace(earlier, earlier + "\n" + paragraph, 1)
    broken.write_text(parked, encoding="utf-8")
    problems = assert_wiring_sits_in_its_step(
        broken, scenario["block_start"], scenario["owning_heading"], scenario["side_effect"]
    )
    assert any("not in" in p or "before the heading of the step it guards" in p for p in problems), (
        "a check parked in an earlier step still precedes the write — only the step-scope "
        "assertion can catch it, and it did not: %s" % problems
    )


def test_sw04_negative_case_a_later_write_between_check_and_side_effect_turns_red(tmp_path):
    """Create-skills' § 2 check before its own step is fine; a § 7 check after § 2's probe write is not."""
    scenario = next(s for s in WIRING_SCENARIOS if s["name"] == "create-skills § 8 report completion")
    broken = _variant_root(tmp_path, scenario["rel"])
    text = _read(broken)
    paragraph = _block_at(text, scenario["block_start"])
    without = text.replace(paragraph, "", 1)
    after_write = without.index("**Writability pre-flight (fail fast)**")
    line_end = without.index("\n", after_write) + 1
    broken.write_text(without[:line_end] + paragraph + "\n" + without[line_end:], encoding="utf-8")
    problems = assert_wiring_precedes_side_effect(broken, scenario["block_start"], scenario["side_effect"])
    assert any("sits between the wiring point" in p or "reading lines sit between" in p for p in problems), (
        "a check separated from its write by another write still passed the ordering assertion: %s"
        % problems
    )


def test_sw04_missing_policy_and_environment_error_wordings_are_distinguishable():
    """The owner keeps the two classes on separate rows; every wiring point names both."""
    owner_text = _read(OWNER)
    table = _section(owner_text, "两类判定的区分")
    rows = [r for r in _table_rows(table) if "策略缺失" in r or "环境错误" in r]
    assert len(rows) == 2, "the owner's two-class table must keep exactly two ruled rows, found %d" % len(rows)
    missing_row = next(r for r in rows if "策略缺失" in r)
    env_row = next(r for r in rows if "环境错误" in r)
    assert "缺的是" in missing_row, "the missing-policy row lost its wording"
    assert "取不到" in env_row, "the environment-error row lost its wording"
    assert missing_row != env_row, "the two classes must not collapse into one wording (FR-007)"
    for scenario in WIRING_SCENARIOS:
        paragraph = _block_at(_read(REPO_ROOT / scenario["rel"]), scenario["block_start"])
        assert _any_anchor(paragraph, ENV_ERROR_ANCHORS), (
            "%s names only one class — the two wordings must stay distinguishable there" % scenario["name"]
        )


def test_sw04_o2_design_principle_separates_the_two_layers():
    """create-skills' § Design Principles must not hand a reusable mechanism a run-environment default.

    § OD-06 / SW-04: the same rule read from the mechanism side says a principle is stated as
    the reusable form, and a landing point / default is a *policy input* the caller supplies —
    not part of the principle. A principle that names where artifacts land invites every
    future skill body to hard-code that landing point.
    """
    problems = assert_o2_design_principle(_read(REPO_ROOT / CREATE_REL))
    assert not problems, "SW-04 / OD-06 violations:\n- " + "\n- ".join(problems)


def assert_o2_design_principle(text: str) -> list[str]:
    """Return every way ``text``'s § Design Principles hands the mechanism a run-environment default."""
    section = _section(text, "Design Principles")
    problems: list[str] = []
    if "under `skills/` by default" in section:
        problems.append(
            "the 'Manage Degrees of Freedom' principle names a default landing point — that is a "
            "policy value living in the mechanism side (§ OD-06 § Consumption Contract)"
        )
    if "landing point" not in section:
        problems.append(
            "the principle says nothing about where a landing point comes from — the two layers "
            "are not separated at the design level"
        )
    return problems


def test_sw04_negative_case_a_default_landing_point_in_the_principle_turns_red(tmp_path):
    text = _read(REPO_ROOT / CREATE_REL)
    assert "Implement landing point" in text, "artifact missing: the principle line is absent"
    broken = tmp_path / "SKILL.md"
    broken.write_text(
        text.replace("Implement landing point", "Land somewhere under `skills/` by default", 1),
        encoding="utf-8",
    )
    problems = assert_o2_design_principle(broken.read_text(encoding="utf-8"))
    assert any("default landing point" in p for p in problems), (
        "the negative case did not turn the principle assertion red: %s" % problems
    )


def test_sw04_merge_skills_decommission_is_reachable():
    """The merge-skills leg exists (empty literals still pass, an absent body does not)."""
    path = REPO_ROOT / MERGE_REL
    _read(path)
