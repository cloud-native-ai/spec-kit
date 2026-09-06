"""Structural contract tests for the /speckit.derive command surface (048 / Feature 049).

Contract: .specify/specs/048-derive-command/contracts/derive-command-template.md

Pins the delivery fan-out (canonical template -> 4 per-tool copies), the reference
doc, the concept-authority link discipline (reference, never restate), the
degradation clause and the /speckit.research boundary, the `--slug`-not-`--topic`
flag surface, the Feedback -> Documentation -> Handoffs wrap-up order, and zero
blocking confirmation gates.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates" / "commands" / "derive.md"
PER_TOOL_COPIES = (
    REPO_ROOT / ".claude" / "commands" / "speckit.derive.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.derive.prompt.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.derive.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.derive.md",
)
REFERENCE_DOC = REPO_ROOT / "docs" / "reference" / "commands" / "derive.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "derive-utils.py"
ENGINE_MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "derive-utils.py"
GATE_SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

AUTHORITY = "shared/definitions/derivation-definitions.md"

pytestmark = pytest.mark.contract


def _frontmatter(text: str) -> str:
    assert text.startswith("---\n"), "template must open with frontmatter"
    return text.split("---", 2)[1]


def _field(text: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", _frontmatter(text), re.M)
    assert m, f"frontmatter is missing {key}:"
    return m.group(1).strip()


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing {heading}"
    return m.group(1)


def _blocking_re():
    spec = importlib.util.spec_from_file_location("scan_confirmation_gates", GATE_SCANNER)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BLOCKING_RE


# --------------------------------------------------------------------------
# canonical template + frontmatter
# --------------------------------------------------------------------------

def test_canonical_source_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


def test_canonical_has_frontmatter_with_a_description():
    assert "description:" in _frontmatter(CANONICAL.read_text(encoding="utf-8"))


def test_short_description_is_within_fifty_chars():
    short = _field(CANONICAL.read_text(encoding="utf-8"), "short-description")
    assert short and len(short) <= 50, f"short-description is {len(short)} chars: {short!r}"


# --------------------------------------------------------------------------
# per-tool fan-out
# --------------------------------------------------------------------------

@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copy_exists_and_is_generated(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text, f"{path.name} lacks the AUTO-GENERATED header"
    assert "templates/commands/derive.md" in text, f"{path.name} does not name its source template"


def test_qoder_copy_description_equals_the_template_short_description():
    template_short = _field(CANONICAL.read_text(encoding="utf-8"), "short-description")
    qoder = (REPO_ROOT / ".qoder" / "commands" / "speckit.derive.md").read_text(encoding="utf-8")
    assert _field(qoder, "description") == template_short


# --------------------------------------------------------------------------
# engine + mirror
# --------------------------------------------------------------------------

def test_engine_and_its_specify_mirror_are_byte_identical():
    assert ENGINE.is_file()
    assert ENGINE_MIRROR.is_file(), "run sync-mirrors.py --write"
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes()


# --------------------------------------------------------------------------
# wrap-up order: Feedback -> Documentation -> Handoffs (Documentation adjacent)
# --------------------------------------------------------------------------

def test_documentation_section_position_and_reference():
    text = CANONICAL.read_text(encoding="utf-8")
    fb = text.find("## Feedback")
    doc = text.find("## Documentation")
    ho = text.find("## Handoffs")
    assert fb != -1 and doc != -1 and ho != -1, "the wrap-up sections must all exist"
    assert fb < doc < ho, "order must be Feedback -> Documentation -> Handoffs"
    between = text[fb:doc]
    assert not re.search(r"^## (?!Feedback)", between, re.M), \
        "## Documentation must be adjacent to ## Feedback"
    body = _section(text, "## Documentation")
    assert "docs-step.md" in body, "Documentation must cite the canonical docs-step convention"
    assert len(body) < 1500, "Documentation must reference, not copy, the docs-sync rules"
    assert "需记录" in body and "无需记录" in body, "missing the conclude-with-one-of contract"


def test_feedback_unit_id_is_the_command_id():
    text = CANONICAL.read_text(encoding="utf-8")
    assert '--unit-id "/speckit.derive"' in text, "feedback unit-id must be the command id"


# --------------------------------------------------------------------------
# concept-authority discipline + the command's own boundary clauses
# --------------------------------------------------------------------------

def test_command_links_to_the_concept_authority():
    assert AUTHORITY in CANONICAL.read_text(encoding="utf-8")


def test_command_states_reference_not_restate():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "引用而不复述" in text or "never restate" in text.lower(), \
        "the command must declare the link-not-restate rule"


def test_command_states_the_degradation_clause():
    assert "no-online-capability" in CANONICAL.read_text(encoding="utf-8")


def test_command_states_the_boundary_vs_research():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "/speckit.research" in text
    assert "Boundary" in text, "the template must draw the /speckit.derive vs /speckit.research line"


def test_command_uses_slug_and_never_topic():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "--slug" in text, "the engine flag is --slug"
    assert "--topic" not in text, "--topic was removed from the engine; the template must not use it"


def test_template_has_zero_blocking_confirmation_gates():
    text = CANONICAL.read_text(encoding="utf-8")
    hits = _blocking_re().findall(text)
    assert hits == [], f"command template carries a blocking gate: {hits}"


# --------------------------------------------------------------------------
# reference doc
# --------------------------------------------------------------------------

def test_reference_doc_exists():
    assert REFERENCE_DOC.is_file(), f"reference doc missing: {REFERENCE_DOC}"


def test_reference_doc_directory_has_no_readme():
    docs = sorted(p.name for p in (REPO_ROOT / "docs" / "reference" / "commands").glob("*.md"))
    assert "derive.md" in docs
    assert "README.md" not in docs, "nested README.md is a reserved-name violation"
