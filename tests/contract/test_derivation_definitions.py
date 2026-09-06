"""Contract tests for the Derivation concept anchor (048 / Feature 049).

Driving files:
  shared/definitions/derivation-definitions.md  (the concept authority under test)
  .specify/specs/048-derive-command/contracts/derivation-model.md  (C-16 drift guard)

The anchor OWNS the Derivation concept (four record schemas, the provenance grade
set, C1-C7, A1-A14, the closed banned-justification set, capability degradation).
These tests pin: its existence and byte-identical `.specify/shared/` mirror, its
ownership declaration, the presence of each owned schema/section, the no-leakage
discipline (no blocking gates, no reserved one-source-of-truth headings, no URLs,
no feature identifiers), and the three-way drift guard that keeps the anchor's
§Banned Justifications bullet, the engine's `BANNED_JUSTIFICATIONS`, and
requirements.md's `STR-001` row literally equal (derivation-model.md C-16).
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

from tests.derive_fixtures import load_engine_module

REPO_ROOT = Path(__file__).resolve().parents[2]

ANCHOR = REPO_ROOT / "shared" / "definitions" / "derivation-definitions.md"
MIRROR = REPO_ROOT / ".specify" / "shared" / "definitions" / "derivation-definitions.md"
REQUIREMENTS = REPO_ROOT / ".specify" / "specs" / "048-derive-command" / "requirements.md"
GATE_SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

ENGINE = load_engine_module("derive_utils_definitions")

#: The twelve reserved one-source-of-truth / token-efficiency headings that a
#: concept anchor MUST NOT reproduce (it links to their owners instead).
RESERVED_HEADINGS = (
    "Declare the owner",
    "Reference, don't copy",
    "Legitimate duplicates",
    "Counts and enumerations",
    "Resolving a disagreement",
    "Relationship to adjacent principles",
    "程序优先(Program-First)",
    "摘要优先(Summary-First)",
    "升级阶梯(Escalation Ladder)",
    "小文件阈值",
    "判定边界",
    "消耗观察(Consumption Observation)",
)

#: The four record schemas the anchor owns.
RECORD_SCHEMAS = ("Source Record", "Move Record", "Step Record", "Element Record")

pytestmark = pytest.mark.contract


def _blocking_re():
    """Load BLOCKING_RE from the hyphenated scanner filename via importlib."""
    spec = importlib.util.spec_from_file_location("scan_confirmation_gates", GATE_SCANNER)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BLOCKING_RE


def _banned_bullet_literals() -> list[str]:
    """The anchor's §Banned Justifications bullet, split on ` · ` (derivation-model C-16)."""
    text = ANCHOR.read_text(encoding="utf-8")
    section = text.split("### Banned Justifications", 1)[1]
    section = section.split("\n## ", 1)[0]
    bullet = next(line for line in section.splitlines() if "·" in line and "`" in line)
    return [tok.strip().strip("`").strip() for tok in bullet.split("·")]


def _str001_literals() -> list[str]:
    """requirements.md's STR-001 definition cell — the backtick-wrapped literals."""
    row = next(line for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
               if "STR-001" in line and "·" in line and line.lstrip().startswith("|"))
    cells = row.split("|")
    definition_cell = cells[2]  # | `STR-001` | <definition> | <references> |
    return re.findall(r"`([^`]+)`", definition_cell)


# --------------------------------------------------------------------------
# existence, mirror, ownership
# --------------------------------------------------------------------------

def test_anchor_exists():
    assert ANCHOR.is_file(), f"concept anchor missing: {ANCHOR}"


def test_specify_mirror_is_byte_identical():
    assert MIRROR.is_file(), f"mirror missing: {MIRROR} (run sync-mirrors.py --write)"
    assert ANCHOR.read_bytes() == MIRROR.read_bytes(), "anchor and its .specify mirror diverged"


def test_anchor_declares_ownership_in_its_opening_lines():
    opening = "\n".join(ANCHOR.read_text(encoding="utf-8").splitlines()[:10])
    assert "single source of truth" in opening, "the anchor must declare ownership up front"
    assert "Derivation" in opening


# --------------------------------------------------------------------------
# owned content — the four schemas, the grade set, the required sections
# --------------------------------------------------------------------------

@pytest.mark.parametrize("schema", RECORD_SCHEMAS)
def test_anchor_carries_each_record_schema(schema):
    assert schema in ANCHOR.read_text(encoding="utf-8")


def test_anchor_carries_the_grade_set():
    text = ANCHOR.read_text(encoding="utf-8")
    assert "Provenance Grades" in text
    for grade in ("primary", "authoritative-secondary", "community", "unverified"):
        assert grade in text, f"grade {grade} missing from the anchor"


@pytest.mark.parametrize("heading", [
    "Contradiction Handling", "Script / Prompt Boundary", "Terminology Boundaries",
])
def test_anchor_carries_the_required_sections(heading):
    assert heading in ANCHOR.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# no-leakage discipline
# --------------------------------------------------------------------------

def test_anchor_has_zero_blocking_confirmation_gates():
    text = ANCHOR.read_text(encoding="utf-8")
    hits = _blocking_re().findall(text)
    assert hits == [], f"anchor must carry no blocking confirmation gate: {hits}"


@pytest.mark.parametrize("reserved", RESERVED_HEADINGS)
def test_anchor_does_not_reproduce_a_reserved_heading(reserved):
    """One-source-of-truth: the anchor links to these owners, never restates them."""
    assert reserved not in ANCHOR.read_text(encoding="utf-8")


def test_anchor_carries_no_url_literal():
    text = ANCHOR.read_text(encoding="utf-8")
    assert not re.search(r"https?://", text), "a distributable concept anchor cites no live URL"


def test_anchor_carries_no_feature_identifier():
    text = ANCHOR.read_text(encoding="utf-8")
    assert not re.search(r"Feature \d{3}", text)
    assert not re.search(r"\.specify/specs/\d{3}-", text)


# --------------------------------------------------------------------------
# C-16 — three-way drift guard on the closed banned-justification set
# --------------------------------------------------------------------------

def test_banned_justifications_agree_across_anchor_engine_and_requirements():
    anchor_set = set(_banned_bullet_literals())
    engine_set = set(ENGINE.BANNED_JUSTIFICATIONS)
    req_set = set(_str001_literals())
    assert anchor_set == engine_set == req_set, (
        "drift in the closed banned-justification set\n"
        f"  anchor-only:   {sorted(anchor_set - engine_set)}\n"
        f"  engine-only:   {sorted(engine_set - anchor_set)}\n"
        f"  req-vs-engine: {sorted(req_set ^ engine_set)}"
    )


def test_banned_justification_set_is_the_closed_fifteen():
    """The count is the tripwire, not a definition; the owner is the anchor."""
    assert len(_banned_bullet_literals()) == 15
    assert len(set(_banned_bullet_literals())) == 15
    assert len(ENGINE.BANNED_JUSTIFICATIONS) == 15
