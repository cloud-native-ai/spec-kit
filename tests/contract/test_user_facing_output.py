"""Contract test: user-facing output channel — echo commands render in a boundary envelope.

Owner of the design: ``shared/guidelines/user-facing-output.md``. This module owns the
machine-decidable half of that owner document:

* the owner document exists in framework source and runtime mirror;
* the stable envelope literal is declared once and carries its required fields;
* every declared echo command/mode carries the canonical ``Output class`` marker and the
  owner pointer (the marker set is the machine-readable membership);
* the thin entries keep their existing ``verbatim`` obligation and add no rendering shape;
* the dispatch surfaces carry the owner pointer, and view-team carries the re-emission rule
  (a tool result is not user-facing presentation);
* the zero-second-mechanism boundary holds: no second channel, store or renderer, and the
  envelope tokens appear only at their owner.

Red-first: authored before the owner document and markers exist, so a missing artifact
fails as "artifact missing", never as a wrongly written assertion.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
OWNER_REL = "shared/guidelines/user-facing-output.md"
OWNER = ROOT / OWNER_REL
MIRROR = ROOT / ".specify" / OWNER_REL

# One-source-of-truth permits a literal pinned in a test. These two tokens are the stable
# envelope delimiters; everything else about the envelope is derived from the owner text.
ENVELOPE_BEGIN = "[user-output:begin]"
ENVELOPE_END = "[user-output:end]"

# The declared echo members as of this change. A marker is the membership; a future echo
# command adds its marker and updates this tuple in the same change.
ECHO_MARKERS = (
    ("templates/commands/status.md", "**Output class (digest, guard)**"),
    ("templates/commands/measure.md", "**Output class (summary)**"),
    ("templates/commands/team.md", "**Output class (view)**"),
    ("templates/commands/goal.md", "**Output class (view)**"),
    ("templates/commands/anchor.md", "**Output class (view)**"),
    ("templates/commands/tools.md", "**Output class (view, list)**"),
    ("templates/commands/todo.md", "**Output class (list)**"),
    ("skills/internal/run-agent/SKILL.md", "**Output class (no-argument listing)**"),
)

DISPATCH_POINTER_SURFACES = (
    "shared/definitions/superagent-definitions.md",
    "skills/internal/run-agent/SKILL.md",
    "skills/internal/run-team/SKILL.md",
    "templates/instructions-template.md",
)

# The status command's rendering audit forbids these strings before ## Wrap-up.
FORBIDDEN_RENDERING_TOKENS = ("line_id=", "omitted=", "DEFAULT_CAP", "cap=<n>", "RO-0")


def _text(rel: str) -> str:
    path = ROOT / rel
    assert path.is_file(), f"expected artifact missing: {rel}"
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing H2 section: ## {heading}"
    return m.group(1)


def test_owner_document_exists_in_source_and_mirror():
    assert OWNER.is_file(), (
        f"owner document missing: {OWNER_REL} — author it before the wire-up"
    )
    assert MIRROR.is_file(), (
        f"runtime mirror missing: .specify/{OWNER_REL} — run "
        "`python3 scripts/python/sync-mirrors.py --write shared`"
    )
    assert MIRROR.read_bytes() == OWNER.read_bytes(), (
        "the owner document drifted between framework source and runtime mirror"
    )


def test_owner_declares_the_four_owned_facts_and_the_no_new_channel_boundary():
    text = _text(OWNER_REL)
    for needle in ("通道归属", "回显命令", "呈现边界", "稳定包封"):
        assert needle in text, f"owner document lost its owned fact heading: {needle!r}"
    scope = _section(text, "范围限制 (Scope limits)")
    for needle in ("不新增控制台通道", "不新增第二渲染器", "不新增存储"):
        assert needle in scope, (
            f"the zero-new-mechanism boundary must state {needle!r} in ## 范围限制"
        )
    assert "live console" in text or "既有" in scope, (
        "the channel must be stated as the existing live console, not a new one"
    )


def test_envelope_literal_is_declared_once_with_its_required_fields():
    text = _text(OWNER_REL)
    assert text.count(ENVELOPE_BEGIN) == 1, (
        f"{ENVELOPE_BEGIN!r} must be declared exactly once in the owner document"
    )
    assert text.count(ENVELOPE_END) == 1, (
        f"{ENVELOPE_END!r} must be declared exactly once in the owner document"
    )
    begin_line = next(
        line for line in text.splitlines() if ENVELOPE_BEGIN in line
    )
    for field in ("command=", "action=", "exit=", "attribution=", "generated="):
        assert field in begin_line, f"envelope begin line lost its field {field!r}"
    assert "verbatim" in text, "the envelope body must be declared verbatim"
    assert "stdout" in text and "stderr" in text, (
        "the owner document must separate stdout (body) from stderr (outside the body)"
    )


def test_declared_echo_members_carry_marker_and_owner_pointer():
    for rel, marker in ECHO_MARKERS:
        text = _text(rel)
        assert marker in text, f"{rel}: missing canonical echo marker {marker!r}"
        assert "user-facing-output.md" in text, (
            f"{rel}: the echo declaration must point at the owner document"
        )
    status = _text("templates/commands/status.md")
    marker_line = next(
        line for line in status.splitlines() if "**Output class (digest, guard)**" in line
    )
    leaked = [token for token in FORBIDDEN_RENDERING_TOKENS if token in marker_line]
    assert not leaked, (
        f"the status echo declaration must avoid the rendering-audit tokens: {leaked}"
    )


def test_thin_entries_keep_verbatim_and_add_no_second_reading():
    for rel in ("templates/commands/status.md", "templates/commands/measure.md"):
        text = _text(rel)
        assert "verbatim" in text, f"{rel} lost its verbatim presentation obligation"
    flat = " ".join(_text("templates/commands/status.md").split())
    assert "Do **not** paraphrase a digest" in flat, (
        "status must keep the no-paraphrase sentence"
    )


def test_dispatch_surfaces_carry_the_owner_pointer():
    for rel in DISPATCH_POINTER_SURFACES:
        assert "user-facing-output.md" in _text(rel), (
            f"{rel}: dispatch/ambient surface lost the user-facing-output pointer"
        )


def test_view_team_carries_the_re_emission_rule():
    text = _text("skills/internal/view-team/SKILL.md")
    for needle in ("自己的消息", "工具结果", "已在上方"):
        assert needle in text, (
            f"view-team must carry the re-emission rule ({needle!r}): a collapsed tool "
            "result is not user-facing presentation"
        )


def test_envelope_tokens_have_one_authoring_home():
    hits = []
    for base in ("shared", "templates", "skills"):
        for path in sorted((ROOT / base).rglob("*.md")):
            rel = path.relative_to(ROOT).as_posix()
            if rel == OWNER_REL:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if ENVELOPE_BEGIN in content or ENVELOPE_END in content:
                hits.append(rel)
    assert hits == [], (
        "the envelope literal may only live in its owner document; these surfaces copied "
        f"it: {hits}"
    )


def test_no_new_engine_or_store_was_introduced():
    for rel in (
        "scripts/python/user-facing-output.py",
        "scripts/python/presentation-utils.py",
        "scripts/python/output-utils.py",
    ):
        assert not (ROOT / rel).exists(), (
            f"{rel} would be a second mechanism; this discipline adds no engine"
        )
    assert not (ROOT / "shared" / "declarations" / "facts" / "user-facing-output.yaml").exists(), (
        "the discipline adds no declaration-fact file or store"
    )
