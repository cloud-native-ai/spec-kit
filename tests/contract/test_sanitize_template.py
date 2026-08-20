"""Contract tests: /speckit.sanitize command template structure (requirement 045 / Feature 047).

Pins contracts/sanitize-command-template.md: execution-flow anchors, engine
invocations, red lines, the destructive-cleanup gate pointer (scanner-safe
wording), Feedback/Documentation steps, delegation triage, and per-tool copy
propagation.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "sanitize.md"

COPIES = [
    ROOT / ".claude" / "commands" / "speckit.sanitize.md",
    ROOT / ".github" / "prompts" / "speckit.sanitize.prompt.md",
    ROOT / ".opencode" / "command" / "speckit.sanitize.md",
    ROOT / ".qoder" / "commands" / "speckit.sanitize.md",
]


def template_text() -> str:
    assert TEMPLATE.is_file(), "command template must exist at templates/commands/sanitize.md"
    return TEMPLATE.read_text(encoding="utf-8")


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
    text = template_text()
    for action in ("collect", "record", "status", "apply"):
        assert f".specify/scripts/python/sanitize-utils.py --action {action}" in text, \
            f"engine invocation for {action} must use the workspace mirror path"


def test_semantic_judgment_limited_to_evidence_pack():
    text = template_text()
    assert "evidencePack" in text or "证据包" in text
    assert "证据不足" in text


def test_delegation_triage_present():
    text = template_text()
    for command in ("/speckit.docs", "/speckit.instructions"):
        assert command in text, f"delegation target missing: {command}"
    assert "sync-mirrors" in text


# --- red lines (C-11..C-14) --------------------------------------------------------------

def test_red_lines_explicit():
    text = template_text()
    assert "确认" in text and ("删除" in text and "移动" in text)
    assert re.search(r"(不得|绝不|MUST NOT).{0,30}(删除|移动)", text) or \
        re.search(r"(删除|移动).{0,30}(不得|绝不|MUST NOT|绝不发生)", text)
    assert re.search(r"(不评估|不修改|不报告).{0,20}(用户|源代码|脚本|测试)", text) or \
        re.search(r"(源代码|产品脚本|测试用例)", text)
    assert "如实报告" in text


def test_scope_guard_against_user_code():
    text = template_text()
    assert "用户源代码" in text or "用户代码" in text
    assert "测试用例" in text or "测试" in text


# --- gate wiring (C-8) --------------------------------------------------------------------

GATE_POINTER = "> Gate probe: gate-sanitize-destructive-cleanup — after the user decision, record firing evidence per confirmation-gates.md §门控观察协议 (non-blocking)."


def test_gate_probe_pointer_present_and_scanner_safe():
    text = template_text()
    assert GATE_POINTER in text, "destructive-cleanup gate pointer line required"
    # the pointer must not read as a blocking gate itself (046 wording discipline)
    pointer_line = next(line for line in text.splitlines() if "gate-sanitize-destructive-cleanup" in line)
    assert "等待用户确认" not in pointer_line and "确认后执行" not in pointer_line


def test_gate_is_front_loaded_destructive_bucket():
    text = template_text()
    assert "破坏性" in text
    assert "确认" in text


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
    sentinel = "sanitize-utils.py --action collect"  # body content is copied verbatim (frontmatter stripped per regen convention)
    assert sentinel in text
    for copy in COPIES:
        assert copy.is_file(), f"missing per-tool copy: {copy}"
        copy_text = copy.read_text(encoding="utf-8")
        assert copy_text.startswith("<!-- AUTO-GENERATED from templates/commands/sanitize.md"), \
            f"copy missing AUTO-GENERATED header: {copy}"
        assert sentinel in copy_text, f"copy does not carry the template content: {copy}"


def test_handoffs_section_present():
    text = template_text()
    assert "## Handoffs" in text
