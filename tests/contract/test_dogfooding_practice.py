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


# ---------------------------------------------------------------------------
# Guidance section (instructions-template) — C-2 / C-3 / C-5
# ---------------------------------------------------------------------------

SECTION_HEADING = "## Dogfooding Practice"
ENGINE_ACTIONS = {"record", "status", "list", "mark-submitted", "reindex", "package", "upstream"}
# Project identifiers that MUST NOT leak into a project-neutral shared section.
FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "Feature 036", "032-dogfooding-practice", "cloud-native-ai"]


def guidance_section(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION_HEADING:
            start = i
            break
    assert start is not None, f"section heading {SECTION_HEADING!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


# --- C-2 (Loop A): actionable feed-back-to-framework path ---

def test_c2_section_present_in_template():
    assert SECTION_HEADING in read(SRC), f"{SECTION_HEADING!r} missing in templates/instructions-template.md"


def test_c2_loop_a_path():
    body = guidance_section(read(SRC))
    assert "Loop A" in body, "Loop A subsection missing"
    for step in ("record", "package"):
        assert step in body, f"Loop A path step {step!r} missing"
    assert re.search(r"threshold", body, re.IGNORECASE), "threshold prompt mention missing"
    assert re.search(r"manual", body, re.IGNORECASE), "manual submission mention missing"
    assert re.search(r"no automatic|never transmits|zero automatic", body, re.IGNORECASE), \
        "zero-automatic-transmission statement missing"


def test_c2_action_names_are_real():
    body = guidance_section(read(SRC))
    used = set(re.findall(r"--action\s+([a-z-]+)", body))
    unknown = used - ENGINE_ACTIONS
    assert not unknown, f"guidance references non-existent engine actions: {unknown}"


def test_c2_project_neutral():
    body = guidance_section(read(SRC))
    for bad in FORBIDDEN:
        assert bad not in body, f"project-specific identifier {bad!r} leaked into shared guidance"
    for bad in ("Dogfooded", "Dogfoodding"):
        assert bad not in body, f"misspelled variant {bad!r} in guidance section"


# --- C-3: byte-identical mirrors ---

def test_c3_mirror_byte_identical():
    assert SRC.read_bytes() == MIRROR.read_bytes(), \
        "templates/instructions-template.md and .specify/templates/instructions-template.md differ"


# --- C-5: single delivery point, no duplication ---

def test_c5_section_appears_once_per_mirror():
    for p in (SRC, MIRROR):
        assert read(p).count(SECTION_HEADING) == 1, f"{SECTION_HEADING!r} must appear exactly once in {p}"


# --- C-2 (Loop B): capability mapping, anti-patterns, staged adoption ---

LOOP_B_CAPABILITIES = ["feedback", "memory", "history", "review", "task record"]
ANTI_PATTERNS = ["formalis", "echo chamber", "dead-letter", "over-ideal"]


def test_c2_loop_b_capability_mapping():
    body = guidance_section(read(SRC))
    assert "Loop B" in body, "Loop B subsection missing"
    low = body.lower()
    for cap in LOOP_B_CAPABILITIES:
        assert cap in low, f"Loop B capability mapping missing {cap!r}"


def test_c2_anti_patterns_and_adoption():
    body = guidance_section(read(SRC)).lower()
    for ap in ANTI_PATTERNS:
        assert ap in body, f"anti-pattern {ap!r} missing from guidance"
    assert re.search(r"staged|stage[- ]by[- ]stage|core team first", body), "staged adoption advice missing"
    assert re.search(r"tailor|not suited|proxy user|drill", body), "scenario-tailoring advice missing"


# --- C-4: no new machinery (FR-004 / SC-004) ---

ENGINE_SRC = ROOT / "scripts" / "python" / "feedback-utils.py"
ENGINE_MIRROR = ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"
COMMANDS_DIR = ROOT / "templates" / "commands"


def test_c4_engine_action_set_unchanged():
    src = read(ENGINE_SRC)
    m = re.search(r'choices=\[([^\]]+)\]', src)
    assert m, "argparse --action choices not found"
    actions = set(re.findall(r'"([a-z-]+)"', m.group(1)))
    assert actions == ENGINE_ACTIONS, f"engine action set changed: {actions ^ ENGINE_ACTIONS}"


def test_c4_engine_mirror_untouched():
    assert ENGINE_SRC.read_bytes() == ENGINE_MIRROR.read_bytes(), "feedback-utils.py mirrors diverged"


def test_c4_no_dogfooding_steps_in_command_templates():
    for p in sorted(COMMANDS_DIR.glob("*.md")):
        assert "Dogfooding" not in read(p), \
            f"command template {p.name} gained Dogfooding content — violates FR-004 (no new steps)"


def test_c4_no_new_memory_layout():
    memory = ROOT / ".specify" / "memory"
    dirs = {d.name for d in memory.iterdir() if d.is_dir()}
    assert dirs <= {"features", "feedback", "knowledge", "session"}, \
        f"unexpected new .specify/memory/ subdirectory: {dirs - {'features', 'feedback', 'knowledge', 'session'}}"
