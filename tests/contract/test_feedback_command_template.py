"""Contract test: /speckit.feedback command template (req 041, US4).

Pins ``.specify/specs/041-refactor-feedback-probe/contracts/feedback-command.md``:
C-1 canonical template + mirror + per-tool copies, C-2/C-3/C-4 three-mode
structure, ## Feedback + ## Documentation steps.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "feedback.md"

# Per-tool copies only for tool dirs that exist in THIS repo (mirrors
# regen-command-copies.py's present-dirs behavior; codex/hermes are generated
# downstream by `specify init`, not here).
TOOL_COPIES = [
    (Path(".claude/commands"), "speckit.feedback.md"),
    (Path(".github/prompts"), "speckit.feedback.prompt.md"),
    (Path(".qoder/commands"), "speckit.feedback.md"),
    (Path(".opencode/command"), "speckit.feedback.md"),
]
PRESENT_COPIES = [
    (REPO_ROOT / rel, name)
    for rel, name in TOOL_COPIES
    if (REPO_ROOT / rel).is_dir()
]


@pytest.mark.contract
class TestFeedbackCommandTemplate:
    def test_template_exists(self):
        assert TEMPLATE.is_file(), "templates/commands/feedback.md missing"

    def test_three_execution_modes_present(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for needle in ("Mode 1", "Mode 2", "Mode 3",
                       "--action", "probes", "cleanup", "probe-inject"):
            assert needle in text, f"template missing: {needle}"

    def test_feedback_and_documentation_steps(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        assert "## Feedback" in text
        assert "/speckit.feedback" in text
        assert "## Documentation" in text

    # test_spec_mirror_identical removed 2026-08-17: the .specify/templates/commands/
    # mirror is retired — per-tool copies are generated straight from templates/commands/.

    def test_tool_copies_exist_with_generated_header(self):
        assert PRESENT_COPIES, "no tool command dirs found"
        for directory, name in PRESENT_COPIES:
            copy = directory / name
            assert copy.is_file(), f"missing tool copy: {copy}"
            head = "\n".join(copy.read_text(encoding="utf-8").splitlines()[:5])
            assert "AUTO-GENERATED" in head, f"{copy} missing AUTO-GENERATED header"

    def test_default_mode_is_probe_overview(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        assert "no arguments" in text or "不带参数" in text, \
            "template must state that Mode 1 is the no-argument default"
