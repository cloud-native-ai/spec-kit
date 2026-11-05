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
    """Return the body of the first ``##``/``###`` heading starting with the prefix."""
    lines = text.splitlines()
    start = None
    level = None
    for i, line in enumerate(lines):
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if 2 <= depth <= 3 and stripped.startswith(" " + heading_prefix):
            start, level = i, depth
            break
    assert start is not None, "section not found: %r" % heading_prefix
    body = [lines[start]]
    in_fence = False
    for line in lines[start + 1:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if not in_fence and depth == level and stripped.startswith(" "):
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
    body_batch = [ln for ln in text.splitlines() if "batch" in ln.lower() and "once" in ln.lower()]
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

# (consumer rel path, wiring literal, side-effect literal)
WIRING_POINTS = (
    (CREATE_REL, "SW-04", None),
    (IMPROVE_REL, "SW-04", None),
    (MERGE_REL, "SW-04", None),
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


def test_sw04_create_skills_preflight_precedes_the_writes():
    text = _read(REPO_ROOT / CREATE_REL)
    preflight = text.index("Writability pre-flight")
    section7 = text.index("### 7. Propagate the Skill")
    section8 = text.index("### 8. Report completion")
    wiring = [i for i in re.finditer(re.escape(CONSUMPTION_ANCHOR), text)]
    assert wiring, "artifact missing: create-skills carries no %r reference" % CONSUMPTION_ANCHOR
    assert any(preflight <= w.start() <= section7 for w in wiring), (
        "the pre-flight (§ 2) carries no Consumption Contract reference — a missing policy "
        "must stop before the first write"
    )
    assert any(w.start() < section8 for w in wiring), (
        "no Consumption Contract reference precedes § 8's report"
    )


def test_sw04_improve_skills_edit_precedes_the_edit_step():
    text = _read(REPO_ROOT / IMPROVE_REL)
    edit = text.index("7. **Update the Skill for the next execution**")
    wiring = [m.start() for m in re.finditer(re.escape(CONSUMPTION_ANCHOR), text)]
    assert wiring, "artifact missing: improve-skills carries no %r reference" % CONSUMPTION_ANCHOR
    assert min(wiring) < edit, (
        "the Consumption Contract reference sits after § 7's edit — the check must precede "
        "the side effect"
    )


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
