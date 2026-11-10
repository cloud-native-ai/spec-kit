"""Contract tests: the role-transition payload wiring (Feature 095, P3 / T020).

What this pins
--------------
contracts/role-transition-payload.contract.md:

- **C-2** — a dispatch-duty-granted payload carries the literal `role-transition` marker plus
  the closed nine-item pointer list (item-id slugs fixed by `data-model.md` § 7).
- **C-3** — the *existing* pre-dispatch self-check form (a payload-substring judgement) is
  extended to require the identifier **and each item-id slug**; the identifier alone is
  insufficient, and a missing one blocks before dispatch as a payload-construction defect.
- **C-4** — the anti-nesting red lines bound the payload: no skill-load instruction, no
  driver-skill reference, no loop logic, no full driver manual.
- **C-5 / C-6** — the return contract's five items; a dual-role executor loses none, and its
  aggregate keeps per-child attribution.
- **C-11** — the five wiring surfaces change by fields / pointers only.
- **C-13** — this module is the listed guarding test.

The fixture set (`tests/fixtures/superagent-role/payload/`) supplies the concrete payload
texts: the complete injection, the one-item-deleted copy, the skill-load violation, and the
named seven-downlink-fields block.

Red-first (Constitution IV): at T020 the fixtures land first (T019) and the five wiring
surfaces are still unchanged skill text, so the surface legs fail against the current files;
the payload legs pass.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"

RUN_AGENT = (
    REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md",
    REPO_ROOT / ".specify" / "skills" / "internal" / "run-agent" / "SKILL.md",
)
TEAM_SKILL = (
    REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md",
    REPO_ROOT / ".specify" / "skills" / "internal" / "create-team" / "SKILL.md",
)
TEAM_PATTERNS = (
    REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "patterns.md",
    REPO_ROOT / ".specify" / "skills" / "internal" / "create-team" / "references" / "patterns.md",
)
DRIVER_SKILL = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md",
    REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver" / "SKILL.md",
)
STAGE_PROMPTS = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "stage-prompts.md",
    REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver" / "references" / "stage-prompts.md",
)

SURFACES = (RUN_AGENT, TEAM_SKILL, TEAM_PATTERNS, DRIVER_SKILL, STAGE_PROMPTS)

FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "superagent-role" / "payload"
COMPLETE = FIXTURE_ROOT / "role-transition-complete.md"
MISSING_ITEM = FIXTURE_ROOT / "role-transition-missing-item.md"
SKILL_LOAD = FIXTURE_ROOT / "role-transition-skill-load.md"
FIELDS_BLOCK = FIXTURE_ROOT / "role-fields.md"

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

SEVEN_FIELDS = (
    "parent_identity",
    "child_label",
    "role_declaration",
    "dispatch_duty",
    "depth_position",
    "authority_ref",
    "return_channel",
)

UPLOAD_DUTIES = (
    "result or deliverable path",
    "evidence pointer",
    "explicit anomaly line",
    "concurrency reading triple",
    "returning executor's identity",
)

MAPPING_COLUMNS = ("label", "role", "dispatch_duty", "workspace", "parent")

# The four anti-nesting red lines (owner: subagent-definitions.md § Dispatch-Time
# Governance Obligation). Each predicate matches an *instruction / content form*, never a
# mere mention -- the payload text may name a red line while staying compliant.
SKILL_LOAD_RE = re.compile(r"\bload\b[^\n]{0,60}\.md|加载[^\n]{0,60}(?:\.md|技能)", re.I)
DRIVER_REF_RE = re.compile(r"sdd-loop-driver|stage-runner\.sh|驱动手册|driver skill", re.I)
LOOP_RE = re.compile(r"while\s+True|for\s+\w+\s+in\s+|循环直到|until\s+(?:all|every|none)", re.I)
FULL_MANUAL_RE = re.compile(
    r"U0\s*(?:–|-)\s*U6|REQUIREMENTS-DONE|PLAN-DONE|TASKS-DONE|ANALYZE-DONE|CHECKLIST-DONE"
)

RED_LINES = (
    ("skill-load", SKILL_LOAD_RE),
    ("driver-skill", DRIVER_REF_RE),
    ("loop-logic", LOOP_RE),
    ("full-manual", FULL_MANUAL_RE),
)


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    return " ".join(text.split())


def _section(text: str, start: str, stop: str) -> str:
    assert start in text, f"section start marker missing: {start!r}"
    body = text[text.index(start) + len(start):]
    assert stop in body, f"section stop marker missing after {start!r}: {stop!r}"
    return body[: body.index(stop)]


def _self_check(payload: str) -> list[str]:
    """The pre-dispatch self-check form: identifier + each item-id slug, as substrings."""
    required = ("role-transition",) + NINE_ITEM_SLUGS
    return [needle for needle in required if needle not in payload]


def _anti_nesting(payload: str) -> list[str]:
    return [name for name, pattern in RED_LINES if pattern.search(payload)]


def _upload_duties_missing(text: str) -> list[str]:
    return [duty for duty in UPLOAD_DUTIES if duty not in _norm(text)]


# ---------------------------------------------------------------- fixtures (T019)


def test_payload_fixture_set_present():
    """The four payload fixtures exist; the seven-fields block has its own named carrier."""
    for path in (COMPLETE, MISSING_ITEM, SKILL_LOAD, FIELDS_BLOCK):
        assert path.is_file(), f"payload fixture missing: {path.relative_to(REPO_ROOT)}"


# ---------------------------------------------------------------- C-2 / C-3


def test_nine_item_slugs_closed_list_and_payload_presence():
    """The closed nine-item list lives on the owner page and rides in the complete payload."""
    owner = _read(OWNER)
    missing = [slug for slug in NINE_ITEM_SLUGS if f"`{slug}`" not in owner]
    assert not missing, f"owner page lost role-transition item ids: {missing}"
    payload = _read(COMPLETE)
    assert _self_check(payload) == [], "the complete payload fails its own self-check"


def test_self_check_blocks_a_missing_item():
    """Delete one item-id slug -> the substring self-check reports exactly that slug."""
    complete = _read(COMPLETE)
    assert [slug for slug in NINE_ITEM_SLUGS if slug not in complete] == []
    mutated = _read(MISSING_ITEM)
    missing = _self_check(mutated)
    assert len(missing) == 1 and missing[0] in NINE_ITEM_SLUGS, (
        f"the one-item-deleted payload must miss exactly one item-id slug, got {missing}"
    )


def test_identifier_alone_is_insufficient():
    """A payload that carries only the marker is blocked with all nine slugs reported."""
    payload = "The payload carries the role-transition injection."
    missing = _self_check(payload)
    assert missing == list(NINE_ITEM_SLUGS), (
        "the self-check must judge each item-id slug, not the identifier alone"
    )
    markerless = _read(COMPLETE).replace("role-transition", "transition-role")
    assert _self_check(markerless) == ["role-transition"], (
        "a payload without the stable identifier must be blocked on the identifier"
    )


# ---------------------------------------------------------------- C-4


def test_anti_nesting_red_lines():
    """The clean payload stays green; each of the four red lines turns the check red."""
    clean = _read(COMPLETE)
    assert _anti_nesting(clean) == [], "the complete payload violates an anti-nesting red line"

    fixture_violations = _anti_nesting(_read(SKILL_LOAD))
    assert fixture_violations == ["skill-load"], (
        f"the skill-load fixture must trip exactly the skill-load red line, got {fixture_violations}"
    )

    variants = {
        "driver-skill": clean + "\nRead `sdd-loop-driver` and its stage runner first.\n",
        "loop-logic": clean + "\nwhile True: dispatch the next child.\n",
        "full-manual": clean + "\n## The Loop (U0–U6)\nU0 ENTRY ... U6 CLOSE\n",
    }
    for name, payload in variants.items():
        assert name in _anti_nesting(payload), f"the {name} mutation did not turn the check red"


def test_anti_nesting_red_lines_are_declared_by_their_owners():
    """The payload red lines stay owned elsewhere; the wiring surface names them by pointer."""
    run_agent = _read(RUN_AGENT[0])
    block = _section(run_agent, "**Anti-nesting obligation", "**Pre-dispatch probe")
    assert "driver/loop skill" in block and "load any skill" in block
    assert "loop logic" in block
    assert "subagent-definitions.md" in block, "the anti-nesting owner is not named by pointer"


# ---------------------------------------------------------------- C-3 / C-11: run-agent


def test_run_agent_pointer_item_and_self_check_extension():
    """run-agent's dispatch-injection block carries the pointer item and the slug self-check."""
    block = _norm(
        _section(
            _read(RUN_AGENT[0]),
            "**Dispatch-time injection (mandatory)**",
            "**Anti-nesting obligation",
        )
    )
    assert "`role-transition`" in block, "the role-transition pointer item is missing"
    assert "superagent-definitions.md" in block, "the closed list is not reached by pointer"
    assert "Role-Transition Injection" in block, "the owner section is not named"
    assert "nine item-id slugs" in block, "the self-check is not extended to the item ids"
    assert "identifier alone is insufficient" in block, (
        "the block must state that the identifier alone does not pass"
    )
    assert "payload-construction defect" in block, "the blocking classification is missing"


# ---------------------------------------------------------------- C-11: seven downlink fields


@pytest.mark.parametrize(
    "surface, extractor",
    [
        (
            "team Per-Agent Payload role_fields row",
            lambda: _role_fields_row(),
        ),
        (
            "driver envelope role_edge object",
            lambda: _driver_envelope_block(),
        ),
        (
            "role-fields fixture block",
            lambda: _read(FIELDS_BLOCK),
        ),
    ],
)
def test_seven_downlink_fields_on_each_wired_surface(surface, extractor):
    """Every surface that carries the downlink fields carries all seven of them."""
    text = extractor()
    missing = [field for field in SEVEN_FIELDS if field not in text]
    assert not missing, f"{surface} lacks downlink role fields: {missing}"


def _role_fields_row() -> str:
    block = _section(_read(TEAM_PATTERNS[0]), "Per-Agent Payload:", "Context Isolation Rules:")
    match = re.search(r"^\| `role_fields` \|.*$", block, re.M)
    assert match, "the Per-Agent Payload table carries no role_fields row"
    row = match.group(0)
    assert "superagent-definitions.md" in row, "the role_fields row must point at the owner page"
    assert "dual-role" in row, "the role_fields row must keep dual-role out of role_declaration"
    return row


def _driver_envelope_block() -> str:
    return _section(
        _read(STAGE_PROMPTS[0]), "### 归属信封（每个事件）", "### 消息入口程序"
    )


def test_driver_envelope_names_sidecar_and_role_edge():
    """The stage envelope sidecar gains the role_edge object without a new channel."""
    block = _driver_envelope_block()
    assert "prompt-<line>-<stage>.md.meta.json" in block
    assert "role_edge" in block
    assert "superagent-definitions.md" in block, "the field semantics are not reached by pointer"


# ---------------------------------------------------------------- C-11: team report mapping


def test_team_report_mapping_table_is_mandatory():
    """`## Execution Detail` must carry the five-column dispatch mapping table."""
    text = _read(TEAM_SKILL[0])
    section = _section(text, "### Report contract", "### Verification")
    assert "## Execution Detail" in section
    assert "每个被派发的执行体一行" in section, "one row per dispatched executor is not required"
    header = [line for line in section.splitlines() if all(f"`{c}`" in line for c in MAPPING_COLUMNS)]
    assert header, f"the dispatch mapping table columns are missing: {MAPPING_COLUMNS}"
    assert "dual-role" in section, "the role column must keep dual-role out"
    assert (
        "## Result Summary ## Deliverables ## Verification ## Execution Detail ## Run Workspace ## Summary"
        in text
    ), "the existing report template section list must stay byte-identical"
    assert "\n## Dispatch" not in text, "no new top-level dispatch section may be introduced"


# ---------------------------------------------------------------- C-11: driver pointer line


def test_driver_pointer_line_root_superagent():
    """The driver manual carries the one-line pointer; execution stays with existing gates."""
    text = _read(DRIVER_SKILL[0])
    topology = _section(text, "## Driver Topology", "## When to Load")
    assert "根 super agent" in topology, "the driver-as-root-super-agent pointer line is missing"
    assert "superagent-definitions.md" in topology, "the owner page is not reached by pointer"
    assert "role_edge" in topology, "the stage payload role fields are not named"
    assert "不新增门禁" in topology, "the no-new-gate boundary is missing"


# ---------------------------------------------------------------- C-5 / C-6


def test_return_contract_five_items():
    """Every return carries the five uplink items; the run-agent surface keeps the anomaly line."""
    owner = _read(OWNER)
    missing = _upload_duties_missing(owner)
    assert not missing, f"the uplink return contract lost items: {missing}"
    run_agent = _read(RUN_AGENT[0])
    assert "explicit anomaly line" in _norm(run_agent), (
        "the dispatch-time injection no longer requires the returned anomaly line"
    )


def test_aggregate_per_child_attribution():
    """The dual-role aggregate keeps per-child attribution and does not replace child evidence."""
    owner = _norm(_read(OWNER))
    assert "per-child attribution, per-child evidence paths" in owner
    assert "the aggregate does not replace the child evidence" in owner


def test_dual_role_duties_intact_mutation():
    """Granting the superagent role and dropping one upload duty turns the check red."""
    owner = _read(OWNER)
    assert "gaining the superagent role reduces none of them" in _norm(owner), (
        "the dual-role duties-intact rule is missing from the owner page"
    )
    assert _upload_duties_missing(owner) == []
    mutated = owner.replace("an explicit anomaly line", "an optional note")
    assert _upload_duties_missing(mutated) == ["explicit anomaly line"], (
        "dropping an upload duty while the dual role is granted must turn the check red"
    )


# ---------------------------------------------------------------- mirrors (T026)


@pytest.mark.parametrize("pair", SURFACES, ids=lambda p: p[0].relative_to(REPO_ROOT).as_posix())
def test_wired_surface_mirror_is_identical(pair):
    """Each wired surface and its runtime mirror are byte-identical after the sync."""
    source, mirror = pair
    assert source.is_file(), f"missing source: {source.relative_to(REPO_ROOT)}"
    assert mirror.is_file(), f"missing mirror: {mirror.relative_to(REPO_ROOT)}"
    assert _read(source) == _read(mirror), (
        f"mirror drift on {source.relative_to(REPO_ROOT)}; run "
        f"python3 scripts/python/sync-mirrors.py --write --only {source.relative_to(REPO_ROOT)}"
    )
