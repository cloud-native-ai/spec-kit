"""Contract: /speckit.sanitize renumber lane.

The lane repairs sequence-number collisions left by concurrent/parallel lines. It
is a data-repair lane, not a new command and not a new confirmation gate.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "sanitize.md"
SKILL = ROOT / "skills" / "internal" / "sanitize-materials" / "SKILL.md"
DOC = ROOT / "docs" / "reference" / "commands" / "sanitize.md"
ENGINE = ROOT / "scripts" / "python" / "renumber-utils.py"
MIRROR = ROOT / ".specify" / "scripts" / "python" / "renumber-utils.py"

COPIES = [
    ROOT / ".claude" / "commands" / "speckit.sanitize.md",
    ROOT / ".github" / "prompts" / "speckit.sanitize.prompt.md",
    ROOT / ".opencode" / "command" / "speckit.sanitize.md",
    ROOT / ".qoder" / "commands" / "speckit.sanitize.md",
]


def _text(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def test_engine_exists_in_source_and_mirror():
    assert ENGINE.is_file(), "renumber engine must ship under scripts/python/"
    assert MIRROR.is_file(), "renumber engine must be mirrored into .specify/scripts/python/"
    assert ENGINE.read_text(encoding="utf-8") == MIRROR.read_text(encoding="utf-8")


def test_template_declares_lane_engine_and_store():
    text = _text(TEMPLATE)
    assert "--lane materials|retention|renumber|all" in text
    assert "renumber-utils.py" in text
    assert "序号重排" in text
    assert ".specify/memory/renumber/" in text
    assert "git branch -m" in text, "branch renames must be reported, never executed"


def test_skill_declares_lane_families_and_red_lines():
    text = _text(SKILL)
    assert "--lane materials|retention|renumber|all" in text
    for stage in ("N1", "N2", "N3", "N4", "N5"):
        assert f"### {stage} —" in text, f"missing renumber stage: {stage}"
    for family in ("spec-number", "register", "rec-follow", "local"):
        assert family in text, f"missing number family: {family}"
    assert "Duplicate-only red line" in text
    assert "Git-ref red line" in text
    assert "Dated-record red line" in text
    assert "Sanctioned writer" in text
    assert "excluded_hits" in text
    assert ".specify/memory/renumber/" in text
    assert "renumber-utils.py" in text


def test_gate_pointer_reused_not_duplicated():
    text = _text(SKILL)
    pointers = [line for line in text.splitlines()
                if line.startswith("> Gate probe: gate-sanitize-destructive-cleanup")]
    assert len(pointers) == 2, \
        "materials Stage 5 and the renumber lane share one gate (no second gate)"
    assert "no second gate" in text


def test_generated_copies_carry_the_lane():
    for copy in COPIES:
        text = _text(copy)
        assert "--lane materials|retention|renumber|all" in text, f"copy missing lane: {copy}"
        assert "renumber-utils.py" in text, f"copy missing engine: {copy}"


def test_docs_describe_the_lane():
    text = _text(DOC)
    assert "Renumber lane" in text
    assert "renumber-utils.py" in text
    assert "duplicate-only" in text or "Duplicate-only" in text
    assert ".specify/memory/renumber/" in text


def test_engine_cli_contract():
    manifest = subprocess.run(
        [sys.executable, str(ENGINE), "--action", "args-manifest"],
        capture_output=True, text=True, timeout=60)
    assert manifest.returncode == 0, manifest.stderr
    import json
    payload = json.loads(manifest.stdout)
    assert set(payload) == {"scan", "plan", "apply", "status", "dismiss", "args-manifest"}
    assert payload["apply"]["required"] == ["--plan"]
