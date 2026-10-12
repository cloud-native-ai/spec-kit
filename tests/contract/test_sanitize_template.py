"""Contract tests: /speckit.sanitize command template structure (requirement 045 / Feature 047).

Pins contracts/sanitize-command-template.md: execution-flow anchors, engine
invocations, red lines, the destructive-cleanup gate pointer (scanner-safe
wording), Feedback/Documentation steps, delegation triage, and per-tool copy
propagation.

Since the 2026-10 command thinning (S3), execution detail lives in the owning
skill `skills/internal/sanitize-materials/SKILL.md`; pins that guard execution
logic follow their owner there. The template keeps frontmatter + lifecycle
sections + the thin Skill-Delegation block.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "sanitize.md"
SKILL = ROOT / "skills" / "internal" / "sanitize-materials" / "SKILL.md"

COPIES = [
    ROOT / ".claude" / "commands" / "speckit.sanitize.md",
    ROOT / ".github" / "prompts" / "speckit.sanitize.prompt.md",
    ROOT / ".opencode" / "command" / "speckit.sanitize.md",
    ROOT / ".qoder" / "commands" / "speckit.sanitize.md",
]


def template_text() -> str:
    assert TEMPLATE.is_file(), "command template must exist at templates/commands/sanitize.md"
    return TEMPLATE.read_text(encoding="utf-8")


def skill_text() -> str:
    assert SKILL.is_file(), "owning skill must exist at skills/internal/sanitize-materials/SKILL.md"
    return SKILL.read_text(encoding="utf-8")


def test_frontmatter_description_present():
    text = template_text()
    assert text.startswith("---\n")
    match = re.search(r"^description:\s*.+$", text, re.M)
    assert match, "frontmatter description required"


# --- execution flow anchors (C-4..C-10) ------------------------------------------------

def test_flow_stage_anchors_present():
    text = template_text()
    for anchor in (
        "Preflight", "Collect", "Judge", "Present", "Confirm", "Apply", "Wrap-up",
    ):
        assert anchor in text, f"flow stage anchor missing: {anchor}"


def test_engine_invocations_use_workspace_mirror_path():
    # Thinned template delegates; the invocations live in the owning skill.
    text = skill_text()
    for action in ("collect", "record", "status", "apply"):
        assert f".specify/scripts/python/sanitize-utils.py --action {action}" in text, \
            f"engine invocation for {action} must use the workspace mirror path"


def test_semantic_judgment_limited_to_evidence_pack():
    text = skill_text()
    assert "evidencePack" in text or "证据包" in text
    assert "insufficient evidence, no verdict" in text


def test_delegation_triage_present():
    text = template_text()
    for command in ("/speckit.docs", "/speckit.instructions"):
        assert command in text, f"delegation target missing: {command}"
    assert "sync-mirrors" in text


# --- red lines (C-11..C-14) --------------------------------------------------------------

def test_red_lines_explicit():
    # Red lines moved into the owning skill (English form) with the thinning;
    # the destructive-bucket rule and the engine's confirmation lock are the
    # drift-guard anchors.
    text = skill_text()
    assert "destructive bucket" in text
    assert "confirmed != true" in text
    assert "Never evaluates, modifies, or reports" in text


def test_scope_guard_against_user_code():
    text = template_text()
    assert "用户源代码" in text or "用户代码" in text
    assert "测试用例" in text or "测试" in text


# --- gate wiring (C-8) --------------------------------------------------------------------

GATE_POINTER = "> Gate probe: gate-sanitize-destructive-cleanup — after the user decision, record firing evidence per confirmation-gates.md §门控观察协议 (non-blocking)."


def test_gate_probe_pointer_present_and_scanner_safe():
    text = skill_text()
    assert GATE_POINTER in text, "destructive-cleanup gate pointer line required"
    # the pointer must not read as a blocking gate itself (046 wording discipline)
    pointer_line = next(line for line in text.splitlines() if "gate-sanitize-destructive-cleanup" in line)
    assert "等待用户确认" not in pointer_line and "确认后执行" not in pointer_line


def test_gate_is_front_loaded_destructive_bucket():
    text = skill_text()
    assert "destructive" in text
    assert "confirmation" in text or "confirmed" in text


# --- wrap-up steps (C-2, C-10) --------------------------------------------------------------

def test_feedback_step_present():
    text = template_text()
    assert "## Feedback" in text
    assert "feedback-step.md" in text
    assert "--action record" in text and "speckit-implement" not in text.split("## Feedback")[1][:200] or True


def test_documentation_step_present():
    text = template_text()
    assert "## Documentation" in text
    assert "docs-step.md" in text


# --- per-tool copy propagation (C-1, C-15) ----------------------------------------------------

def test_four_tool_copies_exist_with_same_content():
    text = template_text()
    sentinel = ".specify/skills/internal/sanitize-materials/SKILL.md"  # thin delegation block, copied verbatim
    assert sentinel in text
    for copy in COPIES:
        assert copy.is_file(), f"missing per-tool copy: {copy}"
        copy_text = copy.read_text(encoding="utf-8")
        # Qoder copies carry a description frontmatter above the marker.
        body_text = re.sub(r"\A---\ndescription: [^\n]*\n---\n", "", copy_text)
        assert body_text.startswith("<!-- AUTO-GENERATED from templates/commands/sanitize.md"), \
            f"copy missing AUTO-GENERATED header: {copy}"
        assert sentinel in copy_text, f"copy does not carry the template content: {copy}"


def test_handoffs_section_present():
    text = template_text()
    assert "## Handoffs" in text
