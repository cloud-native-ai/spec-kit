"""Contract tests for the Task Complexity Rubric (spec 031 — Feature 032).

Template-only feature (Constitution Principle IV → justified Partial): these
verify the rubric section's presence, required structure, project-neutrality,
and mirror parity in the instructions template — the "tests" for a prompt/
template artifact.

Maps to contracts/rubric-section.md checks C-1 … C-10.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"

HEADING = "## Task Complexity Rubric"
TIERS = ["Trivial", "Standard", "Complex", "High-stakes / Ambiguous"]
# Project identifiers that MUST NOT leak into a project-neutral shared section.
FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "Feature 032", ".specify/", "cloud-native-ai"]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def section(text: str) -> str:
    """Return the text of the `## Task Complexity Rubric` section (up to the next `## `)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == HEADING:
            start = i
            break
    assert start is not None, f"section heading {HEADING!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


# --- C-1: stable heading present in both mirrors (STR-001) ---

def test_c1_heading_present_in_both():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        assert HEADING in read(p), f"{HEADING!r} missing in {rel}/instructions-template.md"


# --- C-2: the section contains a Markdown table ---

def test_c2_section_has_table():
    body = section(read(SRC))
    assert any(l.lstrip().startswith("|") for l in body.splitlines()), "no Markdown table in rubric section"


# --- C-3: exactly the four labeled tiers ---

def test_c3_four_tiers_labeled():
    body = section(read(SRC))
    for tier in TIERS:
        assert tier in body, f"tier label {tier!r} missing from rubric section"


# --- C-4: five signal dimensions named ---

def test_c4_five_signals_named():
    body = section(read(SRC)).lower()
    for signal in ("scope", "uncertainty", "blast radius", "cross-cutting", "requirements clarity"):
        assert signal in body, f"signal dimension {signal!r} missing from rubric section"


# --- C-5: per-tier thinking-depth behavior (depth labels + behavior verbs) ---

def test_c5_thinking_depth_behavior():
    body = section(read(SRC))
    low = body.lower()
    for depth in ("minimal", "moderate", "deep", "exhaustive"):
        assert depth in low, f"depth level {depth!r} missing from rubric section"
    for verb in ("explor", "plan", "verif"):
        assert verb in low, f"behavior verb {verb!r} missing from rubric section"


# --- C-6: tie-break rule (higher tier on conflict) ---

def test_c6_tie_break_rule():
    low = section(read(SRC)).lower()
    assert "higher tier" in low, "tie-break rule (higher tier) missing from rubric section"


# --- C-7: default tier + clarify-on-ambiguity ---

def test_c7_default_tier_and_clarify():
    low = section(read(SRC)).lower()
    assert "default" in low, "default-tier rule missing from rubric section"
    assert "clarif" in low, "clarify-on-ambiguity guidance missing from rubric section"


# --- C-8: explicit efficiency-vs-quality tradeoff (both failure modes) ---

def test_c8_efficiency_quality_tradeoff():
    low = section(read(SRC)).lower()
    assert "efficiency" in low and "quality" in low, "efficiency/quality tradeoff missing"
    assert "under-think" in low or "under-thinking" in low, "under-thinking failure mode missing"
    assert "over-think" in low or "over-thinking" in low, "over-thinking failure mode missing"


# --- C-9: project-neutral (no repo-specific identifiers) ---

def test_c9_project_neutral():
    body = section(read(SRC))
    low = body.lower()
    for token in FORBIDDEN:
        assert token.lower() not in low, f"project-specific token {token!r} leaked into shared rubric section"


# --- C-10: the section is byte-identical across both mirrors ---

def test_c10_mirror_parity():
    assert section(read(SRC)) == section(read(MIRROR)), "rubric section not byte-identical across mirrors"
