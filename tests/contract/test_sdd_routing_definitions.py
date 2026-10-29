"""Contract tests: the routing owner document's shape (slice 074a, task T005).

What this pins
--------------
`shared/definitions/sdd-routing-definitions.md` is the single owner of the routing rule
(`contracts/routing-decision.md` C-17) and the declaration site of the control hierarchy
(`contracts/hierarchy-and-authorization.md` C-1 / C-2) and of the four invocation kinds
(`contracts/bootstrap-and-maintenance.md` C-44 / C-45 / C-46). Those obligations are
about **shape and placement**, which is what this file asserts:

1. the opening declares the document's ownership and enumerates the four facts it owns
   (five input value domains, three-value verdict table, fixed precedence, reason-code
   vocabulary), each with the section it lands in;
2. those sections exist — a declared landing point that does not resolve is a dangling
   ownership claim, not a layout preference;
3. the five inputs each carry a **closed** value domain, and the five dimensions the
   decision MUST NOT consume are stated as a rule;
4. `## Invocation kinds` classifies **exactly four** kinds and keeps bootstrap /
   maintenance distinct from the development flow, including the no-`.specify/` case
   and the shared authorization predicate for subagent dispatch;
5. every `[[STR-NNN]]` citation resolves to a row of the slice's `## Shared Strings`;
6. the four owned vocabularies are written **once**: no other surface this slice produces
   repeats a closed vocabulary verbatim (reverse count by landing phrase — a hit is a
   finding, per `one-source-of-truth.md`).

Boundary: this file asserts nothing about the routing *outcome* reasoning (that is
`test_sdd_routing_engine.py`) and nothing about the anti-nesting predicate's wording at
its own owner site (that is `test_sdd_invocation_governance.py`).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER_PATH = REPO_ROOT / "shared" / "definitions" / "sdd-routing-definitions.md"
REQUIREMENTS_PATH = (
    REPO_ROOT / ".specify" / "specs" / "074a-authorized-routing" / "requirements.md"
)

#: The four facts the owner document declares it owns, in the order the contract lists
#: them (C-17). Each entry: (fact id, keywords that must co-occur in its declaration row).
FACTS = (
    ("F-1", ("五项", "取值域")),
    ("F-2", ("三值", "裁决表")),
    ("F-3", ("优先级",)),
    ("F-4", ("理由码",)),
)

#: Dimensions the decision MUST NOT consume (C-18). Each dimension accepts either the
#: requirement's own wording or its English equivalent, so the rule can be written in
#: whichever language the document uses.
FORBIDDEN_DIMENSIONS = (
    ("实现介质", "implementation medium", "medium"),
    ("扩展名", "extension"),
    ("语言", "language"),
    ("工件数", "artifact count", "artefact count"),
    ("作者身份", "author identity", "author"),
)

#: The four invocation kinds (C-44). `sdd-loop-driver` is the only SDD invocation.
INVOCATION_ENTRIES = (
    "sdd-loop-driver",
    "sdd-project-setup",
    "sdd-house-keeping",
)


def _read_owner() -> str:
    assert OWNER_PATH.is_file(), f"owner document missing: {OWNER_PATH}"
    return OWNER_PATH.read_text(encoding="utf-8")


def _sections(text: str) -> dict:
    """Map every level-2 heading to its body (level-3 headings stay in the body)."""
    sections: dict = {}
    current = None
    buffer: list = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def _preamble(text: str) -> str:
    """Everything before the first level-2 heading — the ownership declaration region."""
    head = []
    for line in text.splitlines():
        if line.startswith("## "):
            break
        head.append(line)
    return "\n".join(head)


def _table_rows(body: str) -> list:
    """Markdown table rows as cell lists; separator rows dropped."""
    rows = []
    for line in body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def _section_or_fail(name: str) -> str:
    sections = _sections(_read_owner())
    assert name in sections, (
        f"owner document has no '## {name}' section; declared landings must resolve "
        f"(sections present: {sorted(sections)})"
    )
    return sections[name]


def _normalize_phrase(text: str) -> str:
    """Reduce a rendered vocabulary to its value sequence: backticks/pipes/spacing gone."""
    return re.sub(r"[^0-9A-Za-z_]+", "", text)


def _closed_vocabularies(text: str) -> set:
    """Every run of >= 3 backticked values on one line, as a normalized sequence.

    This is the mechanical form of "reverse count by landing phrase": a closed value
    domain or a closed word list rendered by the owner is exactly such a run.
    """
    found = set()
    for line in text.splitlines():
        values = re.findall(r"`([^`\n]+)`", line)
        if len(values) >= 3:
            phrase = _normalize_phrase("".join(values))
            if phrase:
                found.add(phrase)
    return found


# ---------------------------------------------------------------------------
# 1. Ownership declaration
# ---------------------------------------------------------------------------


def test_owner_document_declares_itself_as_the_single_owner():
    preamble = _preamble(_read_owner())
    assert "Owner" in preamble, (
        "the owner document MUST declare its ownership in its opening lines (C-17)"
    )
    assert "shared/definitions/sdd-routing-definitions.md" in preamble, (
        "the declaration MUST name its own path, so a reader can tell which file owns "
        "the rule (C-17)"
    )


def test_owner_declaration_enumerates_the_four_owned_facts():
    preamble = _preamble(_read_owner())
    rows = {row[0].strip("* "): row for row in _table_rows(preamble) if row}
    for fact_id, keywords in FACTS:
        key = next((k for k in rows if k.startswith(fact_id) or fact_id in k), None)
        assert key is not None, (
            f"the ownership declaration does not enumerate {fact_id}; C-17 requires all "
            f"four owned facts to be named in the opening"
        )
        row_text = " ".join(rows[key])
        for keyword in keywords:
            assert keyword in row_text, (
                f"{fact_id} declaration does not name {keyword!r} (row: {row_text!r})"
            )


def test_each_fact_has_a_resolvable_landing_section():
    preamble = _preamble(_read_owner())
    sections = _sections(_read_owner())
    rows = {row[0].strip("* "): row for row in _table_rows(preamble) if row and len(row) >= 3}
    for fact_id, _keywords in FACTS:
        key = next((k for k in rows if k.startswith(fact_id) or fact_id in k), None)
        assert key is not None, f"{fact_id} not declared"
        landing_cell = rows[key][-1]
        landing = landing_cell.lstrip("§ ").strip()
        landing = re.split(r"[（(]", landing)[0].strip()
        assert landing in sections, (
            f"{fact_id} declares its landing as '## {landing}', which the document does "
            f"not contain — an ownership claim with no landing point is not decidable "
            f"(sections present: {sorted(sections)})"
        )


# ---------------------------------------------------------------------------
# 2. The five inputs and their closed domains (F-1)
# ---------------------------------------------------------------------------


def test_five_inputs_declare_closed_value_domains():
    body = _section_or_fail("Inputs")
    rows = _table_rows(body)
    assert rows, "§ Inputs declares no table: each input's closed domain MUST be written out"
    data_rows = rows[1:]
    assert len(data_rows) == 5, (
        f"the decision consumes exactly five declared inputs (C-18); § Inputs declares "
        f"{len(data_rows)}"
    )
    for row in data_rows:
        domain_cell = " ".join(row[1:])
        values = re.findall(r"`([^`]+)`", domain_cell)
        assert len(values) >= 2, (
            f"row {row[0]!r} declares no closed domain (needs >= 2 enumerated values, "
            f"C-18): {domain_cell!r}"
        )
        assert any(marker in domain_cell for marker in ("MUST NOT", "不得", "只允许", "closed", "封闭")), (
            f"row {row[0]!r} does not state that its domain is closed: {domain_cell!r}"
        )


def test_change_nature_domain_carries_definition_class():
    body = _section_or_fail("Inputs")
    row = next(
        (r for r in _table_rows(body) if "change_nature" in " ".join(r) or "变更性质" in " ".join(r)),
        None,
    )
    assert row is not None, "§ Inputs has no change-nature row"
    cell = " ".join(row[1:])
    for value in ("feature", "maintenance", "definition-class"):
        assert f"`{value}`" in cell, (
            f"change_nature's closed domain MUST carry `{value}` as a declared value "
            f"(C-18: definition-class rides the change nature, not a sixth input)"
        )


def test_complexity_tier_domain_cites_the_rubric_owner():
    body = _section_or_fail("Inputs")
    row = next(
        (r for r in _table_rows(body) if "complexity" in " ".join(r).lower() or "复杂度" in " ".join(r)),
        None,
    )
    assert row is not None, "§ Inputs has no complexity-tier row"
    cell = " ".join(row[1:])
    assert "task-complexity-rubric.md" in cell, (
        "the tier domain MUST cite .specify/shared/guidelines/task-complexity-rubric.md "
        "as the tier owner instead of restating the rubric (C-19)"
    )
    for marker in ("MUST NOT", "不复述", "不得复述"):
        if marker in cell:
            break
    else:
        assert False, "the tier row MUST forbid restating the rubric's signals/table (C-19)"


def test_forbidden_dimensions_are_stated_as_a_rule():
    text = _read_owner()
    rule_line = next(
        (
            line
            for line in text.splitlines()
            if any(marker in line for marker in ("MUST NOT", "不得"))
            and all(
                any(form in line for form in dimension)
                for dimension in FORBIDDEN_DIMENSIONS
            )
        ),
        None,
    )
    assert rule_line is not None, (
        "the owner document MUST state, as a rule, that the decision consumes none of: "
        "implementation medium, file extension, language, artifact count, author "
        "identity (C-18)"
    )


# ---------------------------------------------------------------------------
# 3. Invocation kinds (C-44 / C-45 / C-46)
# ---------------------------------------------------------------------------


def test_invocation_kinds_are_exactly_four():
    body = _section_or_fail("Invocation kinds")
    rows = _table_rows(body)
    assert rows, "§ Invocation kinds declares no table"
    data_rows = rows[1:]
    assert len(data_rows) == 4, (
        f"§ Invocation kinds MUST classify exactly four kinds (C-44), found "
        f"{len(data_rows)}: {data_rows}"
    )
    joined = " ".join(" ".join(row) for row in data_rows)
    for entry in INVOCATION_ENTRIES:
        assert entry in joined, f"§ Invocation kinds does not name {entry!r} (C-44)"
    assert "直接修改" in joined or "direct modification" in joined.lower(), (
        "§ Invocation kinds does not name direct modification as the fourth kind (C-44)"
    )


def test_only_the_driver_is_an_sdd_invocation():
    body = _section_or_fail("Invocation kinds")
    rows = _table_rows(body)
    data_rows = rows[1:]
    driver_rows = [row for row in data_rows if "sdd-loop-driver" in " ".join(row)]
    assert len(driver_rows) == 1, "exactly one kind is the driver (C-44)"
    assert any(cell.strip().startswith("是") for cell in driver_rows[0]), (
        "the driver row MUST be marked as the SDD invocation (C-44)"
    )
    for row in data_rows:
        joined = " ".join(row)
        if "sdd-loop-driver" in joined:
            continue
        assert not any(cell.strip().startswith("是") for cell in row), (
            f"only `sdd-loop-driver` constitutes an SDD invocation; row {row[0]!r} is "
            f"marked as one (C-44)"
        )


def test_bootstrap_and_maintenance_stay_distinct_and_keep_the_setup_path():
    body = _section_or_fail("Invocation kinds")
    for entry in ("sdd-project-setup", "sdd-house-keeping"):
        assert entry in body, f"§ Invocation kinds does not classify {entry!r} (C-44)"
    assert re.search(r"(不同于|distinct from)", body), (
        "bootstrap/maintenance MUST be stated as distinct from the development flow (C-44)"
    )
    setup_rule = next(
        (line for line in body.splitlines() if "MUST NOT" in line and "直接修改" in line),
        None,
    )
    assert setup_rule is not None, (
        "the no-`.specify/` case MUST state that an SDD-routed change is not degraded to "
        "direct modification (C-45)"
    )
    assert "sdd-project-setup" in setup_rule or "sdd-project-setup" in body, (
        "the setup path MUST name its entry (C-45)"
    )
    assert "--action authorize" in body, (
        "setup/house-keeping subagent dispatch MUST satisfy the same effective-"
        "authorization predicate, whose executable form is "
        "`scripts/python/sdd-route.py --action authorize` (C-46)"
    )


# ---------------------------------------------------------------------------
# 4. Shared-string citations resolve
# ---------------------------------------------------------------------------


def test_every_shared_string_reference_resolves():
    owner_text = _read_owner()
    requirements = REQUIREMENTS_PATH.read_text(encoding="utf-8")
    defined = set(re.findall(r"^\|\s*`(STR-\d{3})`", requirements, re.M))
    assert defined, "requirements.md § Shared Strings declares no rows"
    referenced = set(re.findall(r"\[\[(STR-\d{3})\]\]", owner_text))
    assert referenced, (
        "the owner document cites no shared string by id; literals consumed by tests "
        "MUST be cited as [[STR-NNN]] (requirements.md § Shared Strings)"
    )
    missing = sorted(referenced - defined)
    assert not missing, f"unresolvable shared-string citations: {missing}"


# ---------------------------------------------------------------------------
# 5. Hierarchy and direct modification (C-1 / C-2)
# ---------------------------------------------------------------------------


def test_hierarchy_section_states_one_chain_and_one_boundary():
    body = _section_or_fail("Hierarchy")
    for layer in ("Goal", "Team", "Agent"):
        assert layer in body, f"§ Hierarchy does not name the {layer} layer (C-1)"
    assert re.search(r"(SDD 运行|SDD run)", body), "§ Hierarchy does not name the SDD run (C-1)"
    assert re.search(r"(从属|subordinate)", body), (
        "§ Hierarchy MUST state that an SDD run is a subordinate execution path (C-1)"
    )
    prohibition = next(
        (line for line in body.splitlines() if "MUST NOT" in line and "Goal" in line),
        None,
    )
    assert prohibition is not None, (
        "§ Hierarchy MUST forbid an SDD run from mutating the upper layers (C-1)"
    )
    for verb in ("创建", "重绑", "改范围", "终止"):
        assert verb in prohibition, (
            f"the hierarchy boundary MUST name {verb!r} among the forbidden mutations (C-1)"
        )


def test_direct_modification_section_distinguishes_it_from_an_sdd_run():
    body = _section_or_fail("Direct modification")
    assert re.search(r"(工件链|artifact chain)", body), (
        "§ Direct modification MUST define the kind by the absent SDD artifact chain (C-2)"
    )
    assert ".specify/shared/guidelines/confirmation-gates.md" in body, (
        "the applicable gate set MUST be cited by path, never restated (C-2)"
    )
    assert re.search(r"(MUST NOT 复述|不复述|never restated)", body), (
        "§ Direct modification MUST state that the gate set is not restated here (C-2)"
    )


# ---------------------------------------------------------------------------
# 6. One landing place for each owned vocabulary
# ---------------------------------------------------------------------------


def test_owned_vocabularies_are_written_only_in_the_owner_document():
    owner_text = _read_owner()
    vocabularies = _closed_vocabularies(owner_text)
    assert vocabularies, (
        "the owner document declares no closed vocabulary (a run of >= 3 enumerated "
        "values); the four owned facts land as closed vocabularies, so an empty set "
        "means the facts are not written yet (C-17, F-1…F-4)"
    )
    candidates = [
        REPO_ROOT / "scripts" / "python" / "sdd-route.py",
        REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "nested-invocation.md",
        REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md",
        REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md",
        REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "create-mode.md",
        REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md",
    ]
    findings = []
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in vocabularies:
            if phrase and phrase in _normalize_phrase(text):
                findings.append(f"{path.relative_to(REPO_ROOT)} repeats a closed vocabulary")
    assert not findings, (
        "the four owned facts MUST land exactly once, in the owner document; these "
        "surfaces repeat one verbatim (C-17 / C-30):\n" + "\n".join(findings)
    )
