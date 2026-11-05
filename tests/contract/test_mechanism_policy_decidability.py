"""Contract tests for Feature 082 US4 — the worked-example set is decidable and single (T021).

Owns ``data-model.md`` § E-7 (the ``Decidability Sample`` entity) against the owner's
``## Worked Examples`` section. The examples themselves live in
``shared/definitions/mechanism-policy-definitions.md``; this module only asserts that the
set is **machine-parsable into per-item records**, that every answer is one of the three
**closed** values, that every basis cites **only** the boundary-test criterion, and that
the owner's set is the **only** place this feature enumerates examples.

Legs:

* **parse** — ``S-NN`` headings become records with ``snippet`` (a fenced block), an
  ``answer`` from the closed three, and a one-line ``basis``; at least 12 items.
* **answer domain** — ``{机制, 策略, 待澄清}`` and nothing else (V-21: a fourth value such as
  "视情况" means the criterion is undecidable).
* **basis discipline** — a basis opens with the boundary-test phrase and introduces no rule
  id, no clause reference and no second criterion.
* **sole enumeration** — no second copy of the examples in ``contracts/`` or
  ``data-model.md``.

Red-first (Constitution IV / GM-01) and every shape assertion carries a negative case
(GM-07).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER_REL = Path("shared/definitions/mechanism-policy-definitions.md")
DATA_MODEL_REL = Path(".specify/specs/082-mechanism-policy-separation/data-model.md")
CONTRACTS_DIR = REPO_ROOT / ".specify/specs/082-mechanism-policy-separation/contracts"

CLOSED_ANSWERS = ("机制", "策略", "待澄清")
MIN_ITEMS = 12
# The only criterion a basis may cite: the boundary test's own phrasing.
# The criterion is one binary question; a basis states it in either polarity — the content
# survives the swap (mechanism) or must change with it (policy). Both are the same test.
BASIS_REQUIRED_PHRASES = ("换掉运行环境", "随运行环境", "与哪个运行环境", "切换运行模式",
                          "with the runtime environment", "independent of the runtime")
BASIS_MAX_CHARS = 120


# --------------------------------------------------------------------------- #
# parsing
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def owner_text() -> str:
    path = REPO_ROOT / OWNER_REL
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def worked_examples_block(text: str) -> str:
    """The ``## Worked Examples`` body, cut at the next level-2 heading.

    A fenced snippet may *contain* a line that looks like a heading (S-07's own snippet is
    one), so the section end is found by skipping fenced regions rather than by a plain
    ``^## `` search.
    """
    m = re.search(r"^## Worked Examples\s*$", text, re.MULTILINE)
    assert m, "artifact missing: the owner carries no '## Worked Examples' section"
    lines = text[m.end():].splitlines()
    body: list[str] = []
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            body.append(line)
            continue
        if not in_fence and re.match(r"^## ", line):
            break
        body.append(line)
    return "\n".join(body)


def parse_examples(text: str) -> list[dict]:
    """Return one record per ``**S-NN（…）**`` item; an unparsable item yields ``None`` fields."""
    block = worked_examples_block(text)
    chunks = re.split(r"^\*\*(S-\d+)（", block, flags=re.MULTILINE)
    records: list[dict] = []
    for i in range(1, len(chunks), 2):
        sample_id, body = chunks[i], chunks[i + 1]
        # A snippet is any fenced block: three or more backticks open it and the same run
        # closes it, so a snippet may itself contain a fence-width line (S-07 does).
        snippet_match = re.search(r"\n(`{3,})[a-z]*\n(.*?)\n\1[ \t]*\n", body, re.DOTALL)
        answer_match = re.search(r"^答案[:：]\s*(机制|策略|待澄清|[^。，\n]+)", body, re.MULTILINE)
        basis_match = re.search(r"依据[:：]\s*([^\n]+)", body)
        records.append(
            {
                "sample_id": sample_id,
                "snippet": snippet_match.group(1).strip() if snippet_match else None,
                "answer": answer_match.group(1).strip() if answer_match else None,
                "basis": basis_match.group(1).strip() if basis_match else None,
            }
        )
    return records


# --------------------------------------------------------------------------- #
# assertions — each returns the list of violations so a negative case can reuse it
# --------------------------------------------------------------------------- #
def assert_examples_parse(text: str) -> list[str]:
    problems: list[str] = []
    records = parse_examples(text)
    if len(records) < MIN_ITEMS:
        problems.append(
            "the owner enumerates %d worked examples, fewer than the %d the set must carry"
            % (len(records), MIN_ITEMS)
        )
    ids = [r["sample_id"] for r in records]
    if len(set(ids)) != len(ids):
        problems.append("sample ids are not unique: %s" % ids)
    for record in records:
        if not record["snippet"]:
            problems.append("%s has no fenced snippet" % record["sample_id"])
        if not record["answer"]:
            problems.append(
                "%s has no answer line — the item cannot be parsed into a record" % record["sample_id"]
            )
        if not record["basis"]:
            problems.append("%s has no basis line" % record["sample_id"])
    return problems


def assert_answers_closed(text: str) -> list[str]:
    problems: list[str] = []
    for record in parse_examples(text):
        if record["answer"] is None:
            continue
        if record["answer"] not in CLOSED_ANSWERS:
            problems.append(
                "%s answers %r, outside the closed set %s — a fourth value means the criterion "
                "is undecidable (V-21)" % (record["sample_id"], record["answer"], CLOSED_ANSWERS)
            )
    return problems


# Rule ids and clause references a basis MUST NOT introduce (the basis cites the boundary
# test only; everything else would be a second criterion).
FORBIDDEN_BASIS_MARKERS = ("FR-", "SC-", "OD-", "SW-", "§", "见 ", "because", "按照")


def assert_bases_cite_only_the_boundary_test(text: str) -> list[str]:
    problems: list[str] = []
    for record in parse_examples(text):
        basis = record["basis"]
        if not basis:
            continue
        if not any(phrase in basis for phrase in BASIS_REQUIRED_PHRASES):
            problems.append(
                "%s cites no boundary-test phrase (%r) — every basis must rest on the "
                "criterion, not on a new rule"
                % (record["sample_id"], BASIS_REQUIRED_PHRASES)
            )
        for marker in FORBIDDEN_BASIS_MARKERS:
            if marker in basis:
                problems.append(
                    "%s' basis introduces %r — the basis may cite only the boundary test"
                    % (record["sample_id"], marker)
                )
        if len(basis) > BASIS_MAX_CHARS:
            problems.append(
                "%s' basis runs to %d characters — it is a paragraph, not a one-line basis"
                % (record["sample_id"], len(basis))
            )
    return problems


def assert_examples_are_single_copy(text: str, data_model: Path | None = None) -> list[str]:
    """The owner's set is the only enumeration of examples in this feature's artifacts.

    ``data_model`` overrides the path under scan so a negative case can point the same
    scanner at a ``tmp_path`` copy instead of re-implementing it.
    """
    problems: list[str] = []
    owner_ids = {r["sample_id"] for r in parse_examples(text)}
    targets = [("data-model.md", _read(data_model if data_model is not None else REPO_ROOT / DATA_MODEL_REL))]
    for path in sorted(CONTRACTS_DIR.glob("*.md")):
        targets.append((str(path.relative_to(REPO_ROOT)), path.read_text(encoding="utf-8")))
    for label, body in targets:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith(("|", ">")):
                continue
            ids_here = set(re.findall(r"\bS-\d{2}\b", stripped))
            if len(ids_here) >= 2:
                problems.append(
                    "%s enumerates sample ids %s on one line — the owner's set is the only "
                    "enumeration this feature may carry" % (label, sorted(ids_here))
                )
            if ids_here & {"S-01", "S-02"}:
                # A single but *representative* sample id copies the set just as surely: a
                # reader who follows `S-01` here reads an example the owner is the one place
                # to see. Cite the set by section, never by one of its items.
                problems.append(
                    "%s points at sample id %s — cite the set by section, never by one of its "
                    "items (the owner's set is the only enumeration)"
                    % (label, sorted(ids_here & {"S-01", "S-02"}))
                )
            if re.search(r"^\*\*S-\d{2}（", stripped):
                problems.append(
                    "%s carries a worked example in the owner's own item form" % label
                )
    assert owner_ids, "artifact missing: the owner enumerates no sample ids"
    return problems


# --------------------------------------------------------------------------- #
# tests
# --------------------------------------------------------------------------- #
def test_e7_examples_parse_into_records():
    problems = assert_examples_parse(owner_text())
    print("parsed=%d items" % len(parse_examples(owner_text())))
    assert not problems, "E-7 violations:\n- %s" % "\n- ".join(problems)


def test_e7_answers_are_one_of_the_closed_three():
    problems = assert_answers_closed(owner_text())
    assert not problems, "E-7 violations:\n- %s" % "\n- ".join(problems)


def test_e7_bases_cite_only_the_boundary_test():
    problems = assert_bases_cite_only_the_boundary_test(owner_text())
    assert not problems, "E-7 violations:\n- %s" % "\n- ".join(problems)


def test_e7_example_set_is_the_only_enumeration():
    problems = assert_examples_are_single_copy(owner_text())
    assert not problems, "E-7 violations:\n- %s" % "\n- ".join(problems)


def test_e7_negative_case_a_representative_sample_id_turns_red(tmp_path):
    """A data-model copy quoting ``S-01`` as a representative item re-enumerates the set."""
    model = _read(REPO_ROOT / DATA_MODEL_REL)
    broken_text = model.replace("## E-7", "## E-7\n\n例如 `S-01` 就是机制侧的一条。", 1)
    assert broken_text != model, "artifact missing: data-model.md carries no E-7 section"
    broken = tmp_path / "data-model.md"
    broken.write_text(broken_text, encoding="utf-8")
    problems = assert_examples_are_single_copy(owner_text(), data_model=broken)
    assert any("points at sample id" in p for p in problems), (
        "quoting a representative sample id did not turn the single-copy scan red: %s" % problems
    )


def test_e7_negative_case_appending_an_undefined_rule_basis_turns_red(tmp_path):
    text = owner_text()
    marker = "答案：机制。依据：换掉运行环境这句话照样成立。"
    assert marker in text, "artifact missing: cannot build the negative case before S-01 exists"
    injected = text.replace(
        marker,
        "答案：机制。依据：按 FR-099 的新规则判定。",
        1,
    )
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(injected, encoding="utf-8")
    problems = assert_bases_cite_only_the_boundary_test(broken.read_text(encoding="utf-8"))
    assert any("FR-" in p for p in problems), (
        "the negative case did not turn the basis assertion red: %s" % problems
    )
    assert any("boundary-test phrase" in p for p in problems), (
        "the negative case did not turn the criterion assertion red: %s" % problems
    )


def test_e7_negative_case_a_fourth_answer_value_turns_red(tmp_path):
    text = owner_text()
    marker = "答案：机制。依据：换掉运行环境这句话照样成立。"
    assert marker in text, "artifact missing: cannot build the negative case before S-01 exists"
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(
        text.replace(marker, "答案：视情况。依据：换掉运行环境这句话照样成立。", 1),
        encoding="utf-8",
    )
    problems = assert_answers_closed(broken.read_text(encoding="utf-8"))
    assert any("outside the closed set" in p for p in problems), (
        "the negative case did not turn the closed-answer assertion red: %s" % problems
    )


def test_e7_negative_case_dropping_below_the_minimum_turns_red(tmp_path):
    """Remove enough records to fall under ``MIN_ITEMS`` — one record above the floor would not move it.

    The live set carries headroom over the floor (14 vs 12), so the mutation removes the
    tail records down to ``MIN_ITEMS - 1``; the count assertion must then fire. A negative
    case that removes only one record proves the set is above the floor, not that the
    floor is enforced.
    """
    text = owner_text()
    records = parse_examples(text)
    assert len(records) > MIN_ITEMS, (
        "artifact missing: the set carries %d records, no headroom over the %d floor — the "
        "negative case cannot drop below it" % (len(records), MIN_ITEMS)
    )
    victims = [r["sample_id"] for r in records[MIN_ITEMS - 1:]]
    trimmed = text
    for sample_id in victims:
        start = trimmed.index("**%s（" % sample_id)
        nxt = re.search(r"^\*\*S-\d+（|^## ", trimmed[start + 1:], re.MULTILINE)
        end = start + 1 + nxt.start() if nxt else len(trimmed)
        trimmed = trimmed[:start] + trimmed[end:]
    assert len(parse_examples(trimmed)) == MIN_ITEMS - 1, (
        "artifact missing: the mutation left %d records, expected %d"
        % (len(parse_examples(trimmed)), MIN_ITEMS - 1)
    )
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(trimmed, encoding="utf-8")
    problems = assert_examples_parse(broken.read_text(encoding="utf-8"))
    assert any("fewer than" in p for p in problems), (
        "dropping a record did not turn the count assertion red: %s" % problems
    )
