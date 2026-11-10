"""Contract tests: the super agent definition owner page (Feature 095, P1 / T004).

What this pins
--------------
`shared/definitions/superagent-definitions.md` is the single owner of the super agent
concept — the parent-side relative logical role on a dispatch edge. The sibling pages
`agent-definitions.md`, `subagent-definitions.md` and `framework-map.md` carry pointer
lines only (contracts/harness-landing.contract.md C-2 / C-5). The owner page declares the
role model itself: the relative role with set semantics and the output-only `dual-role`
marker, the edge predicate with its four closed violation kinds, unbounded role depth
stated orthogonal to the SDD license-chain depth 2, the super↔sub protocol (downlink,
uplink, four message classes, waiting, attempts, authorization, termination), the closed
nine-item `role-transition` injection, the three-fact-layer state-sync/recovery mapping,
the single-renderer visualization mapping, the zero-second-mechanism boundary, and the
terminology boundary. contracts/role-transition-payload.contract.md C-13 also pins the
four message-class tokens and the no-progress-forwarding rule against this page.

Rules this page references keep their owners: concurrency
(`subagent-definitions.md` § The Concurrency Obligation), reporting
(`shared/guidelines/reporting-obligations.md`), authorization (`sdd-route.py`), waiting /
attribution (`watch-model.md`), the dispatch injections (`fast-fail.md`,
`re-anchoring-definitions.md`), the script interface contract, and the SDD
dispatch-time governance. The page must cite those paths and must not copy their rule
text or the instruction-budget literal.

Red-first (Constitution IV): at T004 the owner page and its runtime mirror do not exist
yet, so every leg fails as "artifact missing" — never as an import or collection error.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFS = REPO_ROOT / "shared" / "definitions"
OWNER_SRC = DEFS / "superagent-definitions.md"
OWNER_MIRROR = REPO_ROOT / ".specify" / "shared" / "definitions" / "superagent-definitions.md"
AGENT_DEFS = DEFS / "agent-definitions.md"
SUBAGENT_DEFS = DEFS / "subagent-definitions.md"
FRAMEWORK_MAP = DEFS / "framework-map.md"

THREE_LAYER_OWNERS = {"agent-definitions.md", "subagent-definitions.md"}
THREE_LAYER_MARKER = "Agent Template → Agent Instance → Agent Execution"

REQUIRED_SECTIONS = (
    "## The Relative Role (相对角色)",
    "## Role Edges (角色边)",
    "## Role Depth (角色深度)",
    "## The super↔sub Protocol (super↔sub 协议)",
    "## Role-Transition Injection (身份转变注入)",
    "## State Synchronization & Recovery (状态同步与恢复)",
    "## Visualization & Tracking (状态跟踪与可视化)",
    "## Zero Second Mechanism (零第二机制)",
    "## Terminology Boundaries (术语边界)",
)

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

MESSAGE_CLASSES = ("ack", "answer", "result", "attention-escalation")

POINTER_OWNERS = (
    "subagent-definitions.md",
    "Dispatch-Time Governance Obligation",
    "The Concurrency Obligation",
    "reporting-obligations.md",
    "sdd-route.py",
    "watch-model.md",
    "fast-fail.md",
    "re-anchoring-definitions.md",
    "script-interface-definitions.md",
    "agent-definitions.md",
)

FORBIDDEN_PAGE_TEXT = (
    "38400",
    "38,400",
    "INSTRUCTIONS_BUDGET_BYTES",
    "先想并发",
    "串行须具名理由并记读数",
    "汇报内容下限",
    "四要素",
    "收窄后的可判定谓词",
)

DEPTH_SENTENCE = (
    "Role depth is unbounded and descriptive; the SDD license-chain depth 2 is an "
    "authorization limit owned by `subagent-definitions.md` § Dispatch-Time Governance "
    "Obligation — the two axes are orthogonal and neither rewrites the other."
)


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _owner_text() -> str:
    return _read(OWNER_SRC)


def _norm(text: str) -> str:
    return " ".join(text.split())


def test_owner_page_present_on_both_sides():
    """The owner page exists in the framework source and in the synced runtime mirror."""
    source = _read(OWNER_SRC)
    mirror = _read(OWNER_MIRROR)
    assert source == mirror, (
        "owner page drifted between framework source and runtime mirror; run "
        "python3 scripts/python/sync-mirrors.py --write "
        "--only shared/definitions/superagent-definitions.md"
    )


def test_ownership_declared_up_front():
    """The opening declares the single ownership before the first level-2 section."""
    preamble = _owner_text().split("\n## ", 1)[0].lower()
    assert "single owner" in preamble, "ownership must be declared up front"
    assert "super agent" in preamble
    assert "relative" in preamble


def test_required_sections_present():
    """The nine model sections land as level-2 headings."""
    headings = {line.strip() for line in _owner_text().splitlines() if line.startswith("## ")}
    missing = [heading for heading in REQUIRED_SECTIONS if heading not in headings]
    assert not missing, f"required sections missing: {missing}"


def test_nine_item_closed_list():
    """The `role-transition` injection carries the closed nine item-id slugs."""
    text = _owner_text()
    assert "`role-transition`" in text, "stable injection identifier missing"
    missing = [slug for slug in NINE_ITEM_SLUGS if f"`{slug}`" not in text]
    assert not missing, f"role-transition item ids missing: {missing}"
    assert "The list is closed" in _norm(text), "the nine-item list must be declared closed"


def test_four_message_class_tokens():
    """The closed message-class set and the no-progress-forwarding rule are stated here."""
    text = _owner_text()
    missing = [token for token in MESSAGE_CLASSES if f"`{token}`" not in text]
    assert not missing, f"message-class tokens missing: {missing}"
    assert "Unclassified progress MUST NOT travel up an edge" in _norm(text), (
        "no-progress-forwarding rule missing"
    )


def test_pointer_only_discipline():
    """Owner rules are reached by pointer; no rule text or budget literal is copied."""
    text = _owner_text()
    missing = [pointer for pointer in POINTER_OWNERS if pointer not in text]
    assert not missing, f"rule owners not reached by pointer: {missing}"
    leaked = [literal for literal in FORBIDDEN_PAGE_TEXT if literal in text]
    assert not leaked, f"copied owner rule text / budget literal found on the owner page: {leaked}"


def test_role_depth_vs_license_chain_sentence():
    """The orthogonality sentence ties unbounded role depth to the depth-2 license chain."""
    assert DEPTH_SENTENCE in _norm(_owner_text()), (
        "the role-depth-vs-license-chain sentence is missing or paraphrased"
    )


def test_agent_definitions_has_no_second_subagent_definition():
    """`agent-definitions.md` keeps a pointer, never a second subagent definition."""
    text = _read(AGENT_DEFS)
    assert "subagent-definitions.md" in text, "subagent owner pointer missing"
    assert "## What a Subagent Is" not in text, "second subagent definition section appeared"
    assert "task-scoped delegated worker" not in text, "subagent definition text copied"


def test_three_sibling_pointer_lines():
    """All three sibling pages carry the pointer line / row to the new owner."""
    agent = _read(AGENT_DEFS)
    assert "superagent-definitions.md" in agent, "agent-definitions.md pointer line missing"
    assert "fourth layer" in agent, "the 'not a fourth layer' statement is missing"

    subagent = _norm(_read(SUBAGENT_DEFS))
    assert "superagent-definitions.md" in subagent, "subagent-definitions.md pointer missing"
    assert "parent-side role" in subagent and "child side" in subagent, (
        "the parent-side / child-side boundary sentence is missing"
    )

    map_rows = [
        line
        for line in _read(FRAMEWORK_MAP).splitlines()
        if line.strip().startswith("|") and "superagent-definitions.md" in line
    ]
    assert map_rows, "framework-map.md carries no pointer row for the owner page"
    assert any("owner" in row.lower() for row in map_rows), (
        "the framework-map row must say what the page owns"
    )


def test_owner_page_avoids_three_layer_marker_literal():
    """The owner page is not a third owner of the taxonomy marker (T004 guard parity)."""
    assert THREE_LAYER_MARKER not in _owner_text(), (
        "the owner page repeats the three-layer marker literal"
    )
    offenders = [
        f.name
        for f in sorted(DEFS.glob("*.md"))
        if f.name not in THREE_LAYER_OWNERS and THREE_LAYER_MARKER in _read(f)
    ]
    assert not offenders, f"third owner of the three-layer taxonomy: {offenders}"
