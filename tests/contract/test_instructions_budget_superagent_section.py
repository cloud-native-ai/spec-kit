"""Contract tests: the Super Agent pointer section in the instructions template (095 T040).

Owner of the design contract: ``.specify/specs/095-superagent-role/contracts/harness-landing.contract.md``
C-1 (section form and size target), C-4 (the generator's budget report is the judge), C-5
(the guarding test). The section is a pointer, never a second rule source: it states the
relative role, names the owner page and declares the ``role-transition`` injection's physical
presence — with no budget literal, no copied rule text and no table.

The budget value is derived from ``scripts/bash/generate-instructions.sh`` (its
``INSTRUCTIONS_BUDGET_BYTES`` is the only definition point), never restated here. The
verdict arithmetic matches the generator: ``over`` fires at ``size >= budget``, so the last
admissible byte is ``budget - 1``.

Red-first (Constitution IV): authored before T042 adds the section, so the section legs fail
on their own "section missing" assertion — never on an import error. The budget leg is green
at authoring time; it guards T043's generated file afterwards.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE = REPO_ROOT / ".specify" / "instructions.md"
GENERATOR = REPO_ROOT / "scripts" / "bash" / "generate-instructions.sh"

HEADING = "## Super Agent (相对逻辑角色)"
LEFT_NEIGHBOUR = "## Spec Kit Framework Map"
RIGHT_NEIGHBOUR = "## Spec Kit Runtime & Symlink Model"
OWNER_PATH = ".specify/shared/definitions/superagent-definitions.md"
INJECTION_IDENTIFIER = "role-transition"

#: C-1 target, including the heading.
SECTION_MAX_BYTES = 600

_BUDGET_RE = re.compile(r"^INSTRUCTIONS_BUDGET_BYTES=(\d+)\s*$", re.M)

#: The nine item ids are owned by the owner page; a pointer section that reproduces any of
#: them has copied the injection list instead of pointing at it.
NINE_ITEM_SLUGS = (
    "role-activation-scope",
    "self-identity-parent-edge",
    "downward-obligation-checklist",
    "concurrency-budget-ref",
    "reporting-path",
    "state-carriers-writer-boundary",
    "attention-classes-escalation",
    "depth-remaining-prohibitions",
    "aggregate-return-contract",
)

#: Rule text owned elsewhere. A pointer section never carries it.
COPIED_RULE_LITERALS = (
    "先想并发",
    "串行须具名理由并记读数",
    "汇报内容下限",
    "四要素",
)


def _budget_bytes() -> int:
    match = _BUDGET_RE.search(GENERATOR.read_text(encoding="utf-8"))
    assert match, (
        "generate-instructions.sh no longer declares INSTRUCTIONS_BUDGET_BYTES as a "
        "top-level assignment — it is the single owner of the budget value, so this "
        "test cannot derive it"
    )
    return int(match.group(1))


def _sections(text: str) -> dict[str, str]:
    """Split exactly like the generator: heading line plus body up to the next ``## ``."""
    parts = re.split(r"(?m)^(## .+)$", text)
    return {parts[i]: parts[i] + parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _template_section() -> str:
    sections = _sections(TEMPLATE.read_text(encoding="utf-8"))
    assert HEADING in sections, (
        f"the pointer section {HEADING!r} is missing from templates/instructions-template.md"
    )
    return sections[HEADING]


def _pointer_violations(section: str) -> list[str]:
    """Everything a pointer section must not be. A pure function so the seeds can use it."""
    budget = _budget_bytes()
    violations = []
    if OWNER_PATH not in section:
        violations.append(f"owner path {OWNER_PATH!r} missing")
    if INJECTION_IDENTIFIER not in section:
        violations.append(f"injection identifier {INJECTION_IDENTIFIER!r} missing")
    if len(section.encode("utf-8")) > SECTION_MAX_BYTES:
        violations.append(
            f"section is {len(section.encode('utf-8'))} B, above the {SECTION_MAX_BYTES} B target"
        )
    if re.search(r"(?m)^\|", section):
        violations.append("section carries a table")
    if re.search(r"(?m)^#{3,} ", section):
        violations.append("section carries a sub-heading")
    for literal in (str(budget), f"{budget:,}", "INSTRUCTIONS_BUDGET_BYTES"):
        if literal in section:
            violations.append(f"budget literal {literal!r} leaked into the section")
    for slug in NINE_ITEM_SLUGS:
        if slug in section:
            violations.append(f"injection item id {slug!r} copied into the section")
    for literal in COPIED_RULE_LITERALS:
        if literal in section:
            violations.append(f"copied rule text {literal!r} found in the section")
    return violations


def test_section_sits_between_the_two_fixed_neighbours():
    """C-1: the section lands between Framework Map and Runtime & Symlink Model."""
    headings = re.findall(r"(?m)^## .+$", TEMPLATE.read_text(encoding="utf-8"))
    assert HEADING in headings, f"the pointer section {HEADING!r} is missing"
    assert LEFT_NEIGHBOUR in headings and RIGHT_NEIGHBOUR in headings
    left = headings.index(LEFT_NEIGHBOUR)
    middle = headings.index(HEADING)
    right = headings.index(RIGHT_NEIGHBOUR)
    assert left < middle < right, (
        f"the section is not between its two neighbours: indices left={left} "
        f"section={middle} right={right}"
    )


def test_section_is_pointer_form():
    """C-1: pointer form only — owner path + injection identifier, no copy, no budget value."""
    violations = _pointer_violations(_template_section())
    assert violations == [], "pointer-form violations: " + "; ".join(violations)


def test_live_file_carries_the_section():
    """C-5: the generator-produced live file carries the section in the same position."""
    live = LIVE.read_text(encoding="utf-8")
    headings = re.findall(r"(?m)^## .+$", live)
    assert HEADING in headings, (
        "the live .specify/instructions.md does not carry the section — run "
        "bash scripts/bash/generate-instructions.sh after syncing the template mirror"
    )
    assert OWNER_PATH in live, "the live section does not carry the owner pointer"
    assert headings.index(LEFT_NEIGHBOUR) < headings.index(HEADING) < headings.index(
        RIGHT_NEIGHBOUR
    ), "the live section is not between its two fixed neighbours"


def test_generated_size_stays_under_the_script_owned_budget():
    """C-4: the live file stays under the generator's budget, with positive headroom."""
    budget = _budget_bytes()
    size = len(LIVE.read_bytes())
    assert size <= budget - 1, (
        f"the live instructions file is {size} B; the generator's verdict is `over` at "
        f"{budget} B, so the last admissible byte is {budget - 1} B"
    )
    assert budget - size > 0, f"no positive headroom: {size} B against {budget} B"


def test_pointer_check_is_not_blind():
    """The pointer-form check fires on the three defects C-1 names (seeded mutations)."""
    section = _template_section()

    budget_seed = section + f"\n\nBudget: {_budget_bytes()} B.\n"
    assert _pointer_violations(budget_seed), "a seeded budget literal was not detected"

    owner_seed = section.replace(OWNER_PATH, ".specify/shared/definitions/other.md")
    assert owner_seed != section
    assert _pointer_violations(owner_seed), "a seeded missing owner path was not detected"

    table_seed = section + "\n| a | b |\n|---|---|\n"
    assert _pointer_violations(table_seed), "a seeded table was not detected"
