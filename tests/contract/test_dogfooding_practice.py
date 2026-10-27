"""Contract tests for Dogfooding Practice (spec 032 — Feature 036).

Template/governance-only feature (Constitution Principle IV → justified
Partial per Principle VII template-only rule): these verify the constitution
principle, the instructions-template summary+pointer section, the single-source
dogfooding doc, mirror parity, and the "no new machinery" invariant (FR-004).

Maps to contracts/dogfooding-artifacts.md checks C-1 … C-7 (amended 2026-08-17:
full-content assertions moved to shared/guidelines/dogfooding.md; the template
carries only a summary + link).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSTITUTION = ROOT / ".specify" / "memory" / "constitution.md"
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
DOC = ROOT / "shared" / "guidelines" / "dogfooding.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "dogfooding.md"
DOC_LINK = "shared/guidelines/dogfooding.md"

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
    parts = tuple(int(x) for x in m.group(1).split(".")[:2])
    assert parts >= (1, 6), f"expected version >= 1.6 (Dogfooding landed in 1.6.0), found {m.group(1)}"


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
# Single-source doc + template summary — C-2 / C-3 / C-5
# ---------------------------------------------------------------------------

SECTION_HEADING = "## Dogfooding Practice"
# Amended by requirement 041-refactor-feedback-probe: the engine action set
# legitimately grows (probes + map/cleanup/migrate-legacy/probe-inject as they land).
# Amended by requirement 047-feedback-introspection: + introspect-register.
# Amended by requirement 056-probe-handler-system: the probe family (probes /
# map / probe-inject) moved to scripts/python/probe-utils.py — closed sets
# pinned both ways by tests/contract/test_probe_engine_action_sets.py.
# Amended by requirement 063-review-p1-governance (C-22, 2026-10-20): the
# wrap-up engine gains `args-manifest` (the machine-readable argument manifest
# the compile-embeds renderer consumes). Closed-set pin updated same-batch.
# 068 C-10 (2026-10-22, same-batch amendment): the receive leg adds the explicit
# `ingest-exec-quant` engine action; the closed-set pin follows the action set.
FEEDBACK_ENGINE_ACTIONS = {"record", "status", "list", "dispose", "mark-submitted", "reindex", "package", "upstream", "cleanup", "migrate-legacy", "introspect-register", "args-manifest", "ingest-exec-quant"}
PROBE_ENGINE_ACTIONS = {"probes", "map", "probe-inject", "handlers", "compile-embeds"}
ENGINE_ACTIONS = FEEDBACK_ENGINE_ACTIONS | PROBE_ENGINE_ACTIONS
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


# --- C-2 (template): summary + pointer shape ---

def test_c2_section_present_in_template():
    assert SECTION_HEADING in read(SRC), f"{SECTION_HEADING!r} missing in templates/instructions-template.md"


def test_c2_template_summary_shape():
    body = guidance_section(read(SRC))
    assert "Loop A" in body and "Loop B" in body, "summary must name both loops"
    assert DOC_LINK in body, f"pointer link {DOC_LINK!r} missing from template summary"
    assert re.search(r"no automatic", body, re.IGNORECASE), \
        "summary must keep the zero-automatic-transmission statement"
    assert "| Capability | Role in your product's loop |" not in body, \
        "the Loop B capability table must live in the external doc, not the template"


def test_c2_doc_exists_with_mirror():
    assert DOC.is_file(), f"missing dogfooding doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing dogfooding doc mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "dogfooding doc mirror drift"


# --- C-2 (doc): Loop A path / Loop B mapping / anti-patterns ---

def test_c2_loop_a_path():
    body = read(DOC)
    assert "Loop A" in body, "Loop A section missing from doc"
    for step in ("record", "package"):
        assert step in body, f"Loop A path step {step!r} missing"
    assert re.search(r"threshold", body, re.IGNORECASE), "threshold prompt mention missing"
    assert re.search(r"manual", body, re.IGNORECASE), "manual submission mention missing"
    assert re.search(r"no automatic|never transmits|zero automatic", body, re.IGNORECASE), \
        "zero-automatic-transmission statement missing"


def test_c2_action_names_are_real():
    used = set(re.findall(r"--action\s+([a-z-]+)", read(DOC)))
    unknown = used - ENGINE_ACTIONS
    assert not unknown, f"doc references non-existent engine actions: {unknown}"


def test_c2_project_neutral():
    for name, text in (("template section", guidance_section(read(SRC))), ("doc", read(DOC))):
        for bad in FORBIDDEN:
            assert bad not in text, f"project-specific identifier {bad!r} leaked into {name}"
        for bad in ("Dogfooded", "Dogfoodding"):
            assert bad not in text, f"misspelled variant {bad!r} in {name}"


# --- C-3: byte-identical mirrors — folded into tests/contract/test_mirror_parity_suite.py
# (spec 067 T020; ledger row in test-evidence/test-consolidation-ledger.md)

# --- C-5: single delivery point, no duplication ---

def test_c5_section_appears_once_per_mirror():
    for p in (SRC, MIRROR):
        assert read(p).count(SECTION_HEADING) == 1, f"{SECTION_HEADING!r} must appear exactly once in {p}"


LOOP_B_CAPABILITIES = ["feedback", "memory", "history", "review", "task record"]
ANTI_PATTERNS = ["formalis", "echo chamber", "dead-letter", "over-ideal"]


def test_c2_loop_b_capability_mapping():
    body = read(DOC)
    assert "Loop B" in body, "Loop B section missing from doc"
    low = body.lower()
    for cap in LOOP_B_CAPABILITIES:
        assert cap in low, f"Loop B capability mapping missing {cap!r}"


# --- C-7 (072): the Loop B recipe uses the custom: unit form with its reason ---

def test_loop_b_recipe_uses_custom_unit_form():
    """Feature 072 C-7: `skill:<scenario-name>` is rejected for client findings
    (in a client project it either matches no probe object — the engine refuses
    the record — or resolves as a framework-internal unit routed upstream), so
    the Loop B recipe MUST name the `custom:<owner>/<name>` form instead."""
    body = read(DOC)
    loop_b = body.split("## Loop B", 1)[1].split("## ", 1)[0]
    assert "custom:<owner>/<name>" in loop_b, (
        "the Loop B recipe MUST name the custom:<owner>/<name> unit form (072 C-7)"
    )
    assert '--unit-id "skill:' not in loop_b, (
        "the Loop B recipe MUST NOT instruct recording with a skill: unit (072 C-7) — "
        "the rejected family may be named in the reason, never in the instruction"
    )


def test_loop_b_recipe_states_the_reason():
    loop_b = read(DOC).split("## Loop B", 1)[1].split("## ", 1)[0]
    assert re.search(r"reason|because|why", loop_b, re.IGNORECASE), (
        "the Loop B recipe MUST state why the custom: form replaces skill: (072 C-7)"
    )
    assert re.search(r"probe object|框架内部|upstream|上送", loop_b), (
        "the stated reason MUST name the probe-object / framework-unit failure mode (072 C-7)"
    )
    # The rest of Loop B is unchanged: the capability table rows all survive.
    for cap in ("Feedback engine", "Memory", "History", "Review", "Task records"):
        assert cap in loop_b, f"Loop B capability row {cap!r} must survive the recipe rewrite"


def test_c2_anti_patterns_and_adoption():
    body = read(DOC).lower()
    for ap in ANTI_PATTERNS:
        assert ap in body, f"anti-pattern {ap!r} missing from doc"
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
    assert actions == FEEDBACK_ENGINE_ACTIONS, (
        f"feedback engine action set changed: {actions ^ FEEDBACK_ENGINE_ACTIONS}")


def test_c4_engine_mirror_untouched():
    assert ENGINE_SRC.read_bytes() == ENGINE_MIRROR.read_bytes(), "feedback-utils.py mirrors diverged"


def test_c4_no_dogfooding_steps_in_command_templates():
    for p in sorted(COMMANDS_DIR.glob("*.md")):
        assert "Dogfooding" not in read(p), \
            f"command template {p.name} gained Dogfooding content — violates FR-004 (no new steps)"


# test_c4_no_new_memory_layout deleted 2026-08-15: stale pin
# (evidence/todo/tools dirs legitimately predate the assertion; owner verdict: delete)
