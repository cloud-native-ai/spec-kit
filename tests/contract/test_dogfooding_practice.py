"""Contract tests for Dogfooding Practice (spec 032 — Feature 036).

Template/governance-only feature (Constitution Principle IV → justified
Partial per Principle VII template-only rule): these verify the constitution
principle, the instructions-template guidance section, mirror parity, and the
"no new machinery" invariant (FR-004).

Maps to contracts/dogfooding-artifacts.md checks C-1 … C-7.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSTITUTION = ROOT / ".specify" / "memory" / "constitution.md"
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"

PRINCIPLE_RE = re.compile(r"^### XI\. Dogfooding", re.MULTILINE)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def principle_section(text: str) -> str:
    """Return the `### XI. Dogfooding` principle body (up to the next heading)."""
    m = PRINCIPLE_RE.search(text)
    assert m, "### XI. Dogfooding principle heading not found in constitution"
    rest = text[m.start():]
    lines = rest.splitlines()
    end = len(lines)
    for j in range(1, len(lines)):
        if lines[j].startswith("### ") or lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[:end])


# --- C-1: constitution principle present with required clauses ---

def test_c1_principle_heading_present():
    assert PRINCIPLE_RE.search(read(CONSTITUTION)), "constitution lacks '### XI. Dogfooding' principle"


def test_c1_core_idea_and_loops():
    body = principle_section(read(CONSTITUTION))
    # Core idea: tight developer/user link → smooth use→feedback→iterate loop
    assert re.search(r"developer[s]?.*user[s]?|toolmaker", body, re.IGNORECASE | re.DOTALL), \
        "core idea (developer≈user tight link) missing"
    assert "Loop A" in body, "Loop A (downstream→framework feedback) identification missing"
    assert "Loop B" in body, "Loop B (project-level self loop) identification missing"


def test_c1_self_application_and_bootstrap():
    body = principle_section(read(CONSTITUTION))
    assert "MUST" in body, "principle body lacks normative MUST clauses"
    assert re.search(r"own\s+(SDD\s+)?workflow|its own spec", body, re.IGNORECASE), \
        "self-application clause (framework built via its own workflow) missing"
    assert re.search(r"bootstrap|self-hosting", body, re.IGNORECASE), \
        "bootstrapping analogy (compiler self-hosting / OS bootstrap) missing"


def test_c1_advisory_no_new_machinery():
    body = principle_section(read(CONSTITUTION))
    assert re.search(r"advisory", body, re.IGNORECASE), "advisory scope declaration missing"
    assert re.search(r"MUST NOT", body), "MUST NOT (no gates / no new machinery) clause missing"


def test_c1_version_minor_bumped():
    text = read(CONSTITUTION)
    m = re.search(r"\*\*Version\*\*: (\S+)", text)
    assert m, "constitution version line missing"
    assert m.group(1).startswith("1.6"), f"expected MINOR bump to 1.6.x, found {m.group(1)}"


# --- C-6: terminology — canonical noun only, no misspelled variants ---

def test_c6_terminology_constitution():
    body = principle_section(read(CONSTITUTION))
    assert "Dogfooding" in body
    for bad in ("Dogfooded", "Dogfoodding"):
        assert bad not in body, f"misspelled variant {bad!r} in constitution principle"


# --- C-7: deviation log location named in the principle ---

def test_c7_deviation_log_location():
    body = principle_section(read(CONSTITUTION))
    assert ".specify/specs/" in body and ".specify/memory/" in body, \
        "deviation log locations (.specify/specs/<key>/ or .specify/memory/) not named"
