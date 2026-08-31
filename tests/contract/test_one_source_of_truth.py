"""Contract tests for the One Source of Truth discipline (Constitution Principle XIV).

The discipline lives in a dedicated single-source doc
(``shared/guidelines/one-source-of-truth.md``); the instructions template carries
only a summary + pointer, and the constitution carries the principle. These verify
the doc's content, the template's pointer shape (without inlining), the doc's own
compliance with the rule it states (its section headings exist in exactly one
place), project-neutrality, and mirror parity — the "tests" for a prompt/template
artifact.
"""

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
DOC = ROOT / "shared" / "guidelines" / "one-source-of-truth.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "one-source-of-truth.md"
CONSTITUTION = ROOT / ".specify" / "memory" / "constitution.md"
DOC_LINK = "shared/guidelines/one-source-of-truth.md"

HEADING = "## One Source Of Truth"
DOC_SECTIONS = [
    "## Declare the owner",
    "## Reference, don't copy",
    "## Legitimate duplicates",
    "## Counts and enumerations",
    "## Resolving a disagreement",
    "## Relationship to adjacent principles",
]
# Project identifiers that MUST NOT leak into a project-neutral shared document.
FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "cloud-native-ai"]
MIN_VERSION = (1, 11)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def section(text: str) -> str:
    """Return the text of the `## One Source Of Truth` section (up to the next `## `)."""
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


# --- C-1: the discipline doc exists, with a byte-identical mirror ---

def test_c1_doc_exists_with_mirror():
    assert DOC.is_file(), f"missing discipline doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing discipline doc mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "discipline doc mirror drift"


# --- C-2: the doc declares its own ownership and carries every section ---

def test_c2_doc_declares_itself_the_owner():
    head = "\n".join(read(DOC).splitlines()[:8])
    assert "single source of truth" in head.lower(), \
        "doc must declare what it owns in its opening lines"
    assert "MUST NOT copy" in head, "doc must forbid copying its rules"


def test_c2_doc_has_all_sections():
    body = read(DOC)
    for h in DOC_SECTIONS:
        assert h in body, f"section {h!r} missing from discipline doc"


# --- C-3: the substantive rules are present, not just the headings ---

def test_c3_owner_selection_order():
    low = read(DOC).lower()
    for tier in ("code", "machine-generated", "authored document"):
        assert tier in low, f"owner-selection tier {tier!r} missing from discipline doc"


def test_c3_three_legitimate_duplicate_kinds():
    low = read(DOC).lower()
    for kind in ("mechanical copy", "guard copy", "dated record"):
        assert kind in low, f"legitimate duplicate kind {kind!r} missing"
    assert "drifting copy" in low, "the drifting-copy verdict is missing"


def test_c3_counts_rule_removes_the_copy():
    low = read(DOC).lower()
    assert "remove the copy" in low, \
        "the counts rule must say to remove the copy rather than correct the number"


def test_c3_normative_keywords():
    body = read(DOC)
    assert "MUST" in body and "MUST NOT" in body, \
        "discipline doc must use MUST / MUST NOT normative keywords"


# --- C-4: template carries heading + pointer, exactly once, in both copies ---

def test_c4_heading_and_link_present_in_both():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        text = read(p)
        assert text.count(HEADING) == 1, \
            f"{HEADING!r} must appear exactly once in {rel}/instructions-template.md"
        body = section(text)
        assert DOC_LINK in body, f"pointer link {DOC_LINK!r} missing in {rel}"


# --- C-5: the template summarizes without inlining the doc's own structure ---

def test_c5_template_does_not_inline_doc_sections():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        body = read(p)
        for h in DOC_SECTIONS:
            inline = h.removeprefix("## ")
            assert inline not in body, \
                f"doc section {inline!r} inlined into {rel}/instructions-template.md"


def test_c5_template_summary_names_the_core_rule():
    low = section(read(SRC)).lower()
    assert "owner" in low, "summary must name the owner concept"
    assert "reference" in low, "summary must carry the reference obligation"


# --- C-6: the doc obeys its own rule — its sections live in exactly one place ---

def test_c6_single_source_sweep():
    for h in DOC_SECTIONS:
        needle = h.removeprefix("## ")
        offenders = []
        for base in ("shared", "templates"):
            for path in (ROOT / base).rglob("*.md"):
                if path == DOC:
                    continue
                if needle in read(path):
                    offenders.append(str(path.relative_to(ROOT)))
        assert not offenders, \
            f"section {needle!r} must live only in the discipline doc, also found in: {offenders}"


# --- C-7: project-neutral (the doc ships to every downstream project) ---

def test_c7_project_neutral():
    for name, text in (("template section", section(read(SRC))), ("doc", read(DOC))):
        low = text.lower()
        for token in FORBIDDEN:
            assert token.lower() not in low, \
                f"project-specific token {token!r} leaked into {name}"


# --- C-8: constitution carries the principle and the version was bumped ---

def test_c8_constitution_principle_present():
    body = read(CONSTITUTION)
    assert re.search(r"^### XIV\. One Source of Truth", body, re.M), \
        "Principle XIV missing from the constitution"
    assert DOC_LINK in body, "Principle XIV must anchor the discipline doc by path"


def test_c8_constitution_version_bumped():
    m = re.search(r"\*\*Version\*\*:\s*(\S+)", read(CONSTITUTION))
    assert m, "constitution version line not found"
    parts = tuple(int(x) for x in m.group(1).split(".")[:2])
    assert parts >= MIN_VERSION, \
        f"constitution version {m.group(1)} below the {MIN_VERSION} floor for Principle XIV"


# --- C-9: byte-identical instructions-template mirrors ---

def test_c9_mirror_parity():
    assert SRC.read_bytes() == MIRROR.read_bytes(), \
        "instructions-template mirrors diverged"
