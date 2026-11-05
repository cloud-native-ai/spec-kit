"""Contract tests for Feature 082 US1 — owner-document form (T010).

Owns the OD-02…OD-06 and OD-09 legs of
``.specify/specs/082-mechanism-policy-separation/contracts/owner-document.contract.md``
that ``tasks.md`` T010 names. The remaining owner legs (OD-01 / OD-07 / OD-08 /
OD-10 and the mirror byte-equality) belong to ``test_mechanism_policy_owner_doc.py``
as sequenced by GM-01; this module is the US1 half only, so the two never assert
the same shape twice.

Legs:

* **OD-02 — the two canonical words and the binary test.** ``机制 (Mechanism)`` and
  ``策略 (Policy)`` appear verbatim; the boundary test is one question with two
  answers and admits no middle tier; the four entity classes of the example table
  each have at least one row.
* **OD-04 — two symptom tables.** Each has at least two rows whose correction
  names a landing class (``技能资产`` / ``运行环境``), not "should be fixed".
* **OD-06 — the consumption contract.** All three prompt fields, a copyable
  skeleton, one marked example on each side, the missing-policy /
  environment-error branches textually distinguishable, the before-any-side-effect
  declaration, and the two prohibitions.
* **OD-09 — the worked-example set.** Parses into at least 12 items, each with a
  snippet, an answer from the closed three values and a basis citing only the
  boundary test; the set is marked as SC-001 / SC-005's sole denominator.

Red-first (Constitution IV / GM-01): the owner document is created by T003–T006,
which precede this row; the legs therefore red only on a removed or drifted shape,
and every shape leg carries a GM-07 negative case so that "green because nothing
was checked" is impossible.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER_REL = Path("shared/definitions/mechanism-policy-definitions.md")
OWNER = REPO_ROOT / OWNER_REL

ANSWERS = ("机制", "策略", "待澄清")
LANDING_CLASSES = ("技能资产", "运行环境")


def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    lines = text.splitlines()
    start = level = None
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


def _rows(section_text: str) -> list[list[str]]:
    """Return table body rows of a section as cell lists (header and rule dropped)."""
    rows: list[list[str]] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else rows


# --------------------------------------------------------------------------- #
# OD-02
# --------------------------------------------------------------------------- #
def assert_terminology(text: str) -> list[str]:
    problems: list[str] = []
    term = _section(text, "Terminology")
    for word in ("机制 (Mechanism)", "策略 (Policy)"):
        if word not in term:
            problems.append("the canonical word %r is not verbatim in § Terminology" % word)
    boundary = _section(text, "边界测试")
    if "换掉运行环境" not in boundary or "要不要改" not in boundary:
        problems.append("the boundary test is not phrased as the swap-the-environment question")
    if "二值" not in boundary and "binary" not in boundary.lower():
        problems.append("the boundary test is not declared binary")
    if "接受「视情况」" not in boundary and "no middle tier" not in boundary.lower():
        problems.append("the boundary test does not close the middle tier ('视情况')")
    examples = _rows(_section(text, "示例表"))
    if len(examples) < 4:
        problems.append("§ 示例表 has %d rows, fewer than the four entity classes" % len(examples))
    joined = " ".join(" ".join(r) for r in examples)
    for needle in ("机制", "策略", "误置", "Meta-layer Membership"):
        if needle not in joined:
            problems.append("§ 示例表 covers no row for the entity class %r" % needle)
    return problems


def test_od02_terminology_and_binary_boundary():
    problems = assert_terminology(_read(OWNER))
    assert not problems, "OD-02 violations:\n- " + "\n- ".join(problems)


# --------------------------------------------------------------------------- #
# OD-04
# --------------------------------------------------------------------------- #
def assert_symptom_tables(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Misplacement Symptoms")
    for heading in ("机制误置", "策略误置"):
        assert heading in section, "artifact missing: § Misplacement Symptoms has no %r table" % heading
        table = _section(text, heading)
        rows = _rows(table)
        if len(rows) < 2:
            problems.append("%s has %d rows — at least two observable symptoms are required"
                            % (heading, len(rows)))
        for cells in rows:
            if len(cells) < 3:
                problems.append("%s row %r is not the | 症状 | 可观测表现 | 改正方向 | shape"
                                % (heading, cells))
                continue
            correction = cells[-1]
            if not any(c in correction for c in LANDING_CLASSES):
                problems.append(
                    "%s row %r names no landing class (%s) — a correction that only says "
                    "'should be fixed' is not actionable"
                    % (heading, cells[0], " / ".join(LANDING_CLASSES))
                )
    return problems


def test_od04_two_symptom_tables_with_landing_corrections():
    problems = assert_symptom_tables(_read(OWNER))
    assert not problems, "OD-04 violations:\n- " + "\n- ".join(problems)


def test_od04_negative_case_dropping_a_landing_class_turns_red(tmp_path):
    text = _read(OWNER)
    mutated = text.replace("移回**技能资产**", "移回", 1).replace(
        "改为**运行环境侧**的输入", "改为输入", 1
    )
    assert mutated != text, "artifact missing: nothing to mutate for the negative case"
    broken = tmp_path / OWNER_REL.name
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_symptom_tables(_read(broken))
    assert any("names no landing class" in p for p in problems), (
        "the negative case did not turn the landing-class assertion red"
    )


# --------------------------------------------------------------------------- #
# OD-06
# --------------------------------------------------------------------------- #
def assert_consumption_contract(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Consumption Contract")
    skeleton = _section(text, "提示形态")
    for field in ("缺的是", "为什么现在需要", "你可以这样给"):
        if field not in skeleton:
            problems.append("the prompt shape carries no %r field (FR-006)" % field)
    if skeleton.count("```text") < 3:
        problems.append(
            "expected the copyable skeleton plus one example per side (>= 3 code blocks), "
            "found %d" % skeleton.count("```text")
        )
    for side in ("写入侧", "读取侧"):
        if side not in skeleton:
            problems.append("no example marked %r" % side)
    branches = _section(text, "两类判定的区分")
    if "策略缺失" not in branches or "环境错误" not in branches:
        problems.append("the two error classes are not named in one table")
    lowered = section.lower()
    if "副作用之前" not in section and "before any side effect" not in lowered:
        problems.append("no declaration that the check precedes any side effect (FR-008)")
    if "半成品" not in section and "half" not in lowered:
        problems.append("no declaration that stopping leaves no half product")
    for prohibition in ("MUST NOT"):
        if prohibition not in section:
            problems.append("§ Consumption Contract carries no %r prohibition" % prohibition)
    for needle in ("默认值", "默认落点"):
        if needle not in section:
            problems.append("the prohibition on %r is missing (FR-005)" % needle)
    for step in ("读", "判", "停"):
        if not re.search(r"\*\*%s\*\*" % step, section):
            problems.append("the read-judge-stop chain has no %r step" % step)
    return problems


def test_od06_consumption_contract_is_complete():
    problems = assert_consumption_contract(_read(OWNER))
    assert not problems, "OD-06 violations:\n- " + "\n- ".join(problems)


def test_od06_negative_case_merging_the_error_classes_turns_red(tmp_path):
    text = _read(OWNER)
    mutated = text.replace("**环境错误**", "**错误**", 1)
    assert mutated != text, "artifact missing: nothing to mutate for the negative case"
    broken = tmp_path / OWNER_REL.name
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_consumption_contract(_read(broken))
    assert any("two error classes" in p for p in problems), (
        "the negative case did not turn the error-class assertion red"
    )


# --------------------------------------------------------------------------- #
# OD-09 — worked examples
# --------------------------------------------------------------------------- #
EXAMPLE_ID = re.compile(r"^\*\*(S-\d{2})\b", re.MULTILINE)
ANSWER_LINE = re.compile(r"答案[：:]\s*(机制|策略|待澄清)\s*[。.]?\s*依据[：:]\s*(.+)$", re.MULTILINE)

BASIS_ALLOWED = (
    "换掉运行环境",
    "换环境",
    "随运行环境",
    "与运行环境",
    "运行环境",
    "运行模式",
    "运行侧",
)


def parse_worked_examples(text: str) -> list[dict[str, str]]:
    section = _section(text, "Worked Examples")
    ids = [m.group(1) for m in EXAMPLE_ID.finditer(section)]
    answers = list(ANSWER_LINE.finditer(section))
    records: list[dict[str, str]] = []
    for idx, match in enumerate(answers):
        start = match.start()
        fence_start = section.rfind("```", 0, start)
        snippet = section[fence_start:start] if fence_start != -1 else ""
        records.append(
            {
                "id": ids[idx] if idx < len(ids) else "?",
                "answer": match.group(1),
                "basis": match.group(2).strip(),
                "snippet": snippet.strip(),
            }
        )
    return records


def assert_worked_examples(text: str) -> list[str]:
    problems: list[str] = []
    section = _section(text, "Worked Examples")
    records = parse_worked_examples(text)
    if len(records) < 12:
        problems.append("%d worked examples parse, fewer than the closed 12-item minimum" % len(records))
    ids = EXAMPLE_ID.findall(section)
    if len(ids) != len(records):
        problems.append(
            "%d example blocks but %d parsed answers — every block must carry a snippet, an "
            "answer and a basis" % (len(ids), len(records))
        )
    seen: set[str] = set()
    for record in records:
        if record["id"] in seen:
            problems.append("duplicate worked-example id %r" % record["id"])
        seen.add(record["id"])
        if record["answer"] not in ANSWERS:
            problems.append("%s answers %r — the closed three values are %r"
                            % (record["id"], record["answer"], ANSWERS))
        if not record["snippet"].startswith("```"):
            problems.append("%s carries no fenced snippet" % record["id"])
        if not any(b in record["basis"] for b in BASIS_ALLOWED):
            problems.append("%s cites a basis that is not the boundary test: %r"
                            % (record["id"], record["basis"]))
        if record["answer"] == "待澄清" and "两" not in record["basis"]:
            problems.append("%s answers 待澄清 without saying why both directions hold"
                            % record["id"])
    if "SC-001" not in section or "SC-005" not in section:
        problems.append("§ Worked Examples is not marked as the SC-001 / SC-005 denominator")
    if "唯一" not in section and "sole" not in section.lower():
        problems.append("§ Worked Examples does not declare itself the sole enumerating location")
    return problems


def test_od09_worked_example_set_is_parsable_and_closed():
    problems = assert_worked_examples(_read(OWNER))
    assert not problems, "OD-09 violations:\n- " + "\n- ".join(problems)


def test_od09_negative_case_removing_one_answer_turns_red(tmp_path):
    text = _read(OWNER)
    lines = text.splitlines()
    drop = next(i for i, ln in enumerate(lines) if ln.strip().startswith("答案："))
    mutated = "\n".join(lines[:drop] + lines[drop + 1:])
    broken = tmp_path / OWNER_REL.name
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_worked_examples(_read(broken))
    assert problems, (
        "removing one worked-example answer left the parse assertion green — the count "
        "check is not reading the answers it claims to read"
    )
