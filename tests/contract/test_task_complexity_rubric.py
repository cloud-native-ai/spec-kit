"""Contract tests for the Task Complexity Rubric (spec 031 — Feature 032).

The rubric now lives in a dedicated single-source doc
(``shared/guidelines/task-complexity-rubric.md``); the instructions template
carries only a summary + pointer. These verify the doc's full content, the
template's pointer shape, project-neutrality, and mirror parity — the "tests"
for a prompt/template artifact.

Maps to contracts/rubric-section.md checks C-1 … C-10 (amended 2026-08-17 for
the summary+pointer form).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
DOC = ROOT / "shared" / "guidelines" / "task-complexity-rubric.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "task-complexity-rubric.md"
DOC_LINK = "shared/guidelines/task-complexity-rubric.md"

HEADING = "## Task Complexity Rubric"
TIERS = ["Trivial", "Standard", "Complex", "High-stakes"]
# Project identifiers that MUST NOT leak into a project-neutral shared section.
FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "Feature 032", "cloud-native-ai"]


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


# --- C-1: stable heading + pointer link present in template and mirror ---

def test_c1_heading_and_link_present_in_both():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        body = section(read(p))
        assert HEADING in body, f"{HEADING!r} missing in {rel}/instructions-template.md"
        assert DOC_LINK in body, f"pointer link {DOC_LINK!r} missing in {rel}"


def test_c1_doc_exists_with_mirror():
    assert DOC.is_file(), f"missing rubric doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing rubric doc mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "rubric doc mirror drift"


# --- C-2 … C-8: full-content contracts now pin the external doc ---

def test_c2_doc_has_table():
    assert any(l.lstrip().startswith("|") for l in read(DOC).splitlines()), \
        "no Markdown table in rubric doc"


def test_c3_four_tiers_labeled():
    body = read(DOC)
    for tier in TIERS + ["High-stakes / Ambiguous"]:
        assert tier in body, f"tier label {tier!r} missing from rubric doc"


def test_c4_five_signals_named():
    low = read(DOC).lower()
    for signal in ("scope", "uncertainty", "blast radius", "cross-cutting", "requirements clarity"):
        assert signal in low, f"signal dimension {signal!r} missing from rubric doc"


def test_c5_thinking_depth_behavior():
    low = read(DOC).lower()
    for depth in ("minimal", "moderate", "deep", "exhaustive"):
        assert depth in low, f"depth level {depth!r} missing from rubric doc"
    for verb in ("explor", "plan", "verif"):
        assert verb in low, f"behavior verb {verb!r} missing from rubric doc"


def test_c6_tie_break_rule():
    low = read(DOC).lower()
    assert "higher tier" in low, "tie-break rule (higher tier) missing from rubric doc"


def test_c7_default_tier_and_clarify():
    low = read(DOC).lower()
    assert "default" in low and "standard" in low, "default-tier rule missing from rubric doc"
    assert "clarif" in low, "clarify-on-ambiguity guidance missing from rubric doc"


def test_c8_efficiency_quality_tradeoff():
    low = read(DOC).lower()
    assert "efficiency" in low and "quality" in low, "efficiency/quality tradeoff missing"
    assert "under-think" in low or "under-thinking" in low, "under-thinking failure mode missing"
    assert "over-think" in low or "over-thinking" in low, "over-thinking failure mode missing"


# --- template summary shape: tiers/tie-break/default inline, full table external ---

def test_template_summary_carries_tiers_tiebreak_default():
    low = section(read(SRC)).lower()
    for tier in ("trivial", "standard", "complex", "high-stakes"):
        assert tier in low, f"summary must name tier {tier!r}"
    assert "higher tier" in low, "summary must carry the tie-break rule"
    assert "standard" in low and "default" in low, "summary must carry the default tier"


def test_template_summary_does_not_inline_the_full_table():
    body = section(read(SRC))
    assert "| Tier | Typical signals |" not in body, \
        "the full tier table must live in the external doc, not the template"


# --- C-9: project-neutral (no repo-specific identifiers) ---

def test_c9_project_neutral():
    for name, text in (("template section", section(read(SRC))), ("doc", read(DOC))):
        low = text.lower()
        for token in FORBIDDEN:
            assert token.lower() not in low, \
                f"project-specific token {token!r} leaked into {name}"


# --- C-10: byte-identical mirrors ---

def test_c10_mirror_parity():
    assert SRC.read_bytes() == MIRROR.read_bytes(), \
        "instructions-template mirrors diverged"
