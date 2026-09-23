"""Contract test: docs-sync step injection (spec 033 US3).

Driven by ``.specify/specs/033-docs-command/contracts/docs-step-injection.md``
(C-1…C-9): single source of truth ``shared/workflow/docs-step.md``, injected as
a reference-only ``## Documentation`` section into the complex command templates
(adjacent to ``## Feedback``, before ``## Handoffs``); the simple templates stay
clean.

This scope is **not** the classification table's complex set. Not every complex
command carries ``## Documentation``: ``history`` has ``## Feedback`` and no
``## Documentation``, so it is held out in ``DOCS_STEP_EXCLUDED`` with a reason the
suite re-measures — repairing a template without updating the dict goes red instead
of drifting silently. (``feedback`` and ``sanitize`` were held out for placing
``## Documentation`` before ``## Feedback``, contrary to C-3's adjacency; their
sections were swapped on 2026-09-24 and the re-measuring test then forced both the
dict and ``COMPLEX_COMMANDS`` to be updated in the same change.)
"""
from __future__ import annotations

import re
import runpy
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SOURCE = REPO_ROOT / "shared" / "workflow" / "docs-step.md"
MIRROR = REPO_ROOT / ".specify" / "shared" / "workflow" / "docs-step.md"
CLASSIFICATION_TEST = REPO_ROOT / "tests" / "contract" / "test_feedback_command_classification.py"

COMPLEX_COMMANDS = [
    "requirements", "clarify", "plan", "tasks", "implement",
    "analyze", "checklist", "review", "research",
    "instructions", "tools", "skills", "todo", "docs",
    "interview", "derive",
    # `team` reclassified simple → complex on 2026-09-23 (user-adjudicated,
    # introspection-20260923T120035Z#F-02); see
    # tests/contract/test_feedback_command_classification.py for the criteria.
    "team",
    # Added 2026-09-24 on measurement: both already carry a correctly positioned
    # `## Documentation` (offsets `## Feedback` < `## Documentation` < `## Handoffs`)
    # and were the two of the four newly classified complex commands that satisfy
    # C-3 as written. The other two were repaired the same day and added below.
    "goal", "session",
    # Added 2026-09-24 after repair: these two placed `## Documentation` *before*
    # `## Feedback`, which C-3's adjacency forbids; the sections were swapped in the
    # templates, and test_c2a then forced this list to be updated rather than drift.
    "feedback", "sanitize",
]
SIMPLE_COMMANDS = ["agents", "constitution", "feature"]

# Complex commands held out of the docs-step scope, each with a measured reason.
# ``test_c2a_exclusions_are_re_measured`` re-checks the reason against the template,
# so this dict cannot outlive the defect it documents.
DOCS_STEP_EXCLUDED = {
    "history": "no-documentation-section",
}

# Anti-vacuity sentinel: an empty or truncated scope list would make every
# per-command assertion below pass without a single template being read.
MIN_COMPLEX = 21


def classification_complex() -> set[str]:
    """The classification contract's complex set, via its owning test module."""
    return set(runpy.run_path(str(CLASSIFICATION_TEST))["COMPLEX_COMMANDS"])


def correctly_positioned_docs_carriers() -> set[str]:
    """Templates carrying `## Documentation` where C-3 requires it: after
    `## Feedback`, before `## Handoffs`, with nothing in between."""
    out = set()
    for path in COMMANDS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        fb = heading_offset(text, "## Feedback")
        doc = heading_offset(text, "## Documentation")
        ho = heading_offset(text, "## Handoffs")
        if doc == -1 or fb == -1 or not fb < doc:
            continue
        if ho != -1 and not doc < ho:
            continue
        if re.search(r"^## (?!Feedback)", text[fb:doc], re.M):
            continue
        out.add(path.stem)
    return out


def section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing {heading}"
    return m.group(1)


@pytest.mark.contract
def test_c1_single_source_and_mirror():
    assert SOURCE.is_file(), "shared/workflow/docs-step.md missing"
    assert MIRROR.is_file(), ".specify mirror missing"
    assert SOURCE.read_bytes() == MIRROR.read_bytes(), "docs-step mirror drift"


@pytest.mark.contract
def test_c2_injection_scope_counts():
    assert len(SIMPLE_COMMANDS) == 3
    # No exact count for COMPLEX_COMMANDS on purpose: test_c2b derives the scope from
    # the classification table minus the re-measured exclusions, which is a stronger
    # check, and a second hard-coded number here would only drift against it. What this
    # guard owns is truncation — an empty or short list makes every per-command
    # assertion below pass without reading a single template.
    assert len(COMPLEX_COMMANDS) >= MIN_COMPLEX, (
        f"scope list holds {len(COMPLEX_COMMANDS)} entries (< {MIN_COMPLEX}) — it looks "
        f"truncated, which would make the per-command assertions below vacuous"
    )


@pytest.mark.contract
def test_c2a_exclusions_are_re_measured():
    """Every held-out command must still exhibit the reason it is held out for."""
    for cmd, reason in DOCS_STEP_EXCLUDED.items():
        text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
        fb = heading_offset(text, "## Feedback")
        doc = heading_offset(text, "## Documentation")
        if reason == "no-documentation-section":
            assert fb != -1 and doc == -1, (
                f"{cmd}.md now carries ## Documentation — remove it from DOCS_STEP_EXCLUDED "
                f"and add it to COMPLEX_COMMANDS"
            )
        elif reason == "documentation-before-feedback":
            assert doc != -1 and fb != -1 and doc < fb, (
                f"{cmd}.md's ## Documentation is no longer mis-ordered — remove it from "
                f"DOCS_STEP_EXCLUDED and add it to COMPLEX_COMMANDS"
            )
        else:
            pytest.fail(f"unknown exclusion reason for {cmd}: {reason!r}")


@pytest.mark.contract
def test_c2b_scope_is_classification_minus_verified_exclusions():
    """No complex command is silently dropped from the docs-step scope."""
    expected = classification_complex() - set(DOCS_STEP_EXCLUDED)
    assert set(COMPLEX_COMMANDS) == expected, (
        f"docs-step scope drift — missing: {sorted(expected - set(COMPLEX_COMMANDS))}; "
        f"extra: {sorted(set(COMPLEX_COMMANDS) - expected)}"
    )
    assert set(COMPLEX_COMMANDS) == correctly_positioned_docs_carriers(), (
        "the scope list and the measured set of correctly positioned ## Documentation "
        "carriers disagree"
    )


def heading_offset(text: str, heading: str) -> int:
    """Offset of `heading` matched as a WHOLE line, or -1.

    A bare ``text.find("## Documentation")`` also matches prose that names a *different*
    heading — `## Documentation Map` is a real section of the instructions template and
    Route R1 refers to it by name — which silently reorders the comparison and reports a
    section-order violation in a file whose order is correct.
    """
    m = re.search(rf"(?m)^{re.escape(heading)}[ \t]*$", text)
    return m.start() if m else -1


@pytest.mark.contract
@pytest.mark.parametrize("cmd", COMPLEX_COMMANDS)
def test_c3_c4_documentation_section_position_and_reference(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    fb = heading_offset(text, "## Feedback")
    doc = heading_offset(text, "## Documentation")
    ho = heading_offset(text, "## Handoffs")
    assert doc != -1, f"{cmd}.md missing ## Documentation"
    assert fb != -1 and fb < doc, f"{cmd}.md: ## Documentation must follow ## Feedback"
    assert ho == -1 or doc < ho, f"{cmd}.md: ## Documentation must precede ## Handoffs"
    between = text[fb:doc]
    assert not re.search(r"^## (?!Feedback)", between, re.M), \
        f"{cmd}.md: ## Documentation must be adjacent to ## Feedback"
    body = section(text, "## Documentation")
    assert "docs-step.md" in body, f"{cmd}.md Documentation section must cite docs-step.md"
    assert len(body) < 1500, f"{cmd}.md Documentation section must reference, not copy, the rules"
    assert "需记录" in body and "无需记录" in body, f"{cmd}.md missing the conclusion contract"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", SIMPLE_COMMANDS)
def test_c2_simple_commands_not_injected(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert "## Documentation" not in text, f"{cmd}.md must not carry the docs-sync step"


@pytest.mark.contract
def test_c6_c7_incremental_and_zero_new_machinery():
    text = SOURCE.read_text(encoding="utf-8")
    assert "R0" in text and "NEVER trigger" in text, "incremental-only rule missing"
    assert "Non-blocking" in text
    assert "Zero new machinery" in text
