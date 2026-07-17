"""Contract tests for the Glossary Mechanism (spec 029 — Feature 031).

Template-heavy feature (Constitution Principle VII): these verify template
content, canonical paths, mirror parity, ambient wiring, protocol coverage, and
non-destructive re-initialization — the "tests" for prompt/template artifacts.

Maps to contracts/: glossary-file-format.md, instruction-init.md,
glossary-protocol.md.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "glossary-utils.py"
COMMANDS = ["requirements", "plan", "tasks", "implement"]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# --- Template + mirror parity (glossary-file-format.md C-5, instruction-init.md C-5) ---

def test_glossary_template_present_and_mirrored():
    src = ROOT / "templates" / "glossary-template.md"
    mirror = ROOT / ".specify" / "templates" / "glossary-template.md"
    assert src.exists(), "templates/glossary-template.md missing"
    assert mirror.exists(), ".specify mirror of glossary-template.md missing"
    assert read(src) == read(mirror), "glossary-template.md mirror not byte-identical"


def test_glossary_template_has_required_structure():
    text = read(ROOT / "templates" / "glossary-template.md")
    assert "# Project Glossary" in text
    assert "| Canonical | Variants | Meaning | Origin | Status |" in text
    # authoring rules present
    for rule in ("Common words", "authoritative", "onflict"):
        assert rule in text, f"authoring rule '{rule}' missing from template"


# --- Ambient wiring (instruction-init.md C-4) ---

def test_documentation_map_has_glossary_row():
    for rel in ("templates/instructions-template.md",
                ".specify/templates/instructions-template.md"):
        text = read(ROOT / rel)
        assert "`.specify/memory/glossary.md`" in text, f"Glossary row missing in {rel}"
        assert "| **Glossary** |" in text, f"Glossary Documentation Map row missing in {rel}"


def test_instructions_template_mirror_identical():
    assert read(ROOT / "templates/instructions-template.md") == \
        read(ROOT / ".specify/templates/instructions-template.md")


# --- Init hook (instruction-init.md C-1) ---

def test_generate_instructions_invokes_glossary_init():
    text = read(ROOT / "scripts" / "bash" / "generate-instructions.sh")
    assert "glossary-utils.py" in text, "generate-instructions.sh does not init the glossary"
    assert "--action init" in text


def test_instructions_command_has_glossary_seeding_guidance():
    for rel in ("templates/commands/instructions.md",
                ".specify/templates/commands/instructions.md"):
        text = read(ROOT / rel)
        assert "## Glossary Initialization" in text, f"seeding guidance missing in {rel}"


# --- Protocol doc (glossary-protocol.md) ---

def test_shared_protocol_present_and_mirrored():
    src = ROOT / "shared" / "workflow" / "glossary.md"
    mirror = ROOT / ".specify" / "shared" / "workflow" / "glossary.md"
    assert src.exists() and mirror.exists()
    assert read(src) == read(mirror), "shared/workflow/glossary.md mirror not byte-identical"


def test_shared_protocol_covers_all_rules():
    text = read(ROOT / "shared" / "workflow" / "glossary.md").lower()
    # correction / traceable / ambiguity
    assert "variant" in text and "canonical" in text
    assert "override" in text or "traceable" in text
    assert "ambiguous" in text and "defer" in text
    # enrichment
    assert "checkpoint" in text and "common" in text
    # conflict + confirmation
    assert "conflict" in text and "confirm" in text
    # precedence
    assert "authoritative" in text and "user" in text


# --- Command templates + per-tool copies carry the Glossary step (protocol C-*) ---

@pytest.mark.parametrize("cmd", COMMANDS)
def test_command_templates_reference_glossary(cmd):
    surfaces = [
        ROOT / f"templates/commands/{cmd}.md",
        ROOT / f".specify/templates/commands/{cmd}.md",
        ROOT / f".claude/commands/speckit.{cmd}.md",
        ROOT / f".github/prompts/speckit.{cmd}.prompt.md",
        ROOT / f".qoder/commands/speckit.{cmd}.md",
    ]
    for p in surfaces:
        assert p.exists(), f"missing command surface {p}"
        text = read(p)
        assert "## Glossary" in text, f"'## Glossary' step missing in {p}"
        assert "glossary.md" in text, f"glossary reference missing in {p}"


# --- Non-destructive round-trip (instruction-init.md C-3, FR-013) ---

def test_init_is_non_destructive_roundtrip(tmp_path: Path):
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "glossary-template.md").write_text(
        read(ROOT / "templates" / "glossary-template.md"), encoding="utf-8"
    )
    (tmp_path / ".specify" / "memory").mkdir(parents=True)

    def run(*args):
        cp = subprocess.run(
            [sys.executable, str(ENGINE), "--root", str(tmp_path), *args],
            capture_output=True, text=True,
        )
        assert cp.returncode == 0, cp.stderr
        return json.loads(cp.stdout)

    assert run("--action", "init")["created"] is True
    run("--action", "add", "--canonical", "Domain Term", "--meaning", "m",
        "--origin", "user", "--status", "confirmed")
    # Re-init must not discard the user entry.
    assert run("--action", "init")["created"] is False
    listing = run("--action", "list")
    assert any(e["canonical"] == "Domain Term" and e["origin"] == "user"
               for e in listing["entries"]), "user entry lost across re-init"
