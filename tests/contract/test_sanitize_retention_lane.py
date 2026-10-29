"""Contract: /speckit.sanitize retention lane.

The lane is a data lifecycle, not a new command and not a new confirmation gate.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "sanitize.md"
SKILL = ROOT / "skills" / "internal" / "sanitize-materials" / "SKILL.md"
DOC = ROOT / "docs" / "reference" / "commands" / "sanitize.md"
MEMORY_DOC = ROOT / "docs" / "reference" / "skills" / "memory.md"
FEEDBACK_DOC = ROOT / "docs" / "reference" / "skills" / "feedback.md"
ENGINE = ROOT / "scripts" / "python" / "record-retention.py"

COPIES = [
    ROOT / ".claude" / "commands" / "speckit.sanitize.md",
    ROOT / ".github" / "prompts" / "speckit.sanitize.prompt.md",
    ROOT / ".opencode" / "command" / "speckit.sanitize.md",
    ROOT / ".qoder" / "commands" / "speckit.sanitize.md",
]


def _text(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def test_skill_declares_lane_and_receipt_gate():
    text = _text(SKILL)
    assert "--lane materials|retention|renumber|all" in text
    assert "record-retention.py --action scan" in text
    assert "Receipt red line" in text
    assert "No receipt means no deletion" in text
    assert "30 days" in text or "30-day" in text
    assert ".specify/memory/retention/" in text
    assert "settled_at" in text
    assert "needs-promotion" in text


def test_template_declares_lane_and_engine():
    text = _text(TEMPLATE)
    assert "--lane materials|retention|renumber|all" in text
    assert "record-retention.py" in text
    assert "retention lane" in text
    assert ".specify/memory/retention/" in text


def test_generated_copies_carry_the_lane():
    for copy in COPIES:
        text = _text(copy)
        assert "--lane" in text, f"copy missing lane: {copy}"
        assert "record-retention.py" in text, f"copy missing engine: {copy}"


def test_retention_action_set_is_closed():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "args-manifest"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    manifest = json.loads(proc.stdout)
    assert list(manifest) == ["scan", "distill", "plan", "apply", "status",
                              "args-manifest"]
    assert manifest["apply"]["required"] == ["--plan"]


def test_no_second_confirmation_gate():
    text = _text(SKILL)
    assert "gate-sanitize-destructive-cleanup" in text
    assert "gate-record-retention" not in text
    assert not re.search(r"gate-.*retention", text), \
        "the retention lane must reuse the sanitize destructive gate"


def test_docs_describe_the_retention_lane():
    assert "Retention lane" in _text(DOC)
    assert "Governed session retention" in _text(MEMORY_DOC)
    assert "Post-consume retirement" in _text(FEEDBACK_DOC)
