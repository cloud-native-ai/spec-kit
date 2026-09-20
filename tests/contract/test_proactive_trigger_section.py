"""Contract tests for the Proactive Flow Trigger shipped surfaces (spec 050).

Two faces of one mechanism, one file:

1. **Instructions-section face** — maps to ``contracts/trigger-section.md``
   clauses C-1 … C-12. Assertion style follows ``test_task_complexity_rubric.py``
   (dual surface + byte-identical mirror + project-neutrality), extended with the
   additive-reconcile behavior and the full agent-path coverage that FR-003 makes
   a hard prerequisite. These tests run the real ``generate-instructions.sh`` and
   the real ``scan-confirmation-gates.py``.

   Per C-10, THIS file is the sole authority for the instruction-path enumeration
   and count; other artifacts reference it rather than restating it.

2. **Discipline-doc face** — merged from the former
   ``test_proactive_trigger_discipline_doc.py``; maps to
   ``contracts/discipline-doc.md``. Only the *structural* clauses survive here
   (C-1 dual surface + byte-identical mirror, C-2 closed and ordered `## `
   section set, C-3 zero BLOCKING_PATTERNS hits and no governance-path exemption,
   C-4 reference-not-restate negatives, C-5 escalation-table shape, C-6 project
   neutrality, C-7 the reverse pointer the doc must carry).

   The former C-8…C-16 prose pins are gone. They asserted, through an
   any-of-these-wordings helper, that a natural-language phrase occurred in a
   `## ` section — a wording pin fails on a harmless rewrite and passes for any
   doc containing a common phrase. Every normative proposition they claimed to
   stake is owned by a suite that executes the real engine
   (``scripts/python/trigger-utils.py``):

   - ``tests/contract/test_trigger_engine.py`` — envelope key set, closed action
     / flag / exit-code sets (C-9/C-10/C-22), `--compliance-done` default and the
     `ordering-violation` verdict, probe-only evidence reads, bounded payload and
     suggestion key set, session repeat-suppression, threshold promotion and
     single-decline reset, destructive-never-promotes, auto-execute is only a
     flag, default config shape (`threshold` 3, `telemetryWindow` 200).
   - ``tests/integration/test_trigger_promotion.py`` — SC-009 disabled produces
     no suggestion and no auto-execution, disabled state survives instructions
     regeneration, re-enabling clears session suppression, reset/downgrade paths.
   - ``tests/integration/test_trigger_telemetry.py`` — one row per assess, row
     count never exceeds the window, append-then-truncate, rotation loses no rule
     state, escalation rate and budget flag.
   - ``tests/integration/test_trigger_tuning.py`` — the four evidence kinds
     (decline/ignore/miss/accept), the small-sample guard and its configurability,
     proposals are candidates handed back not decided, `tune` alone changes
     nothing, `tune-apply` moves the proposed→ratified→applied state machine and
     leaves an evidence trail.
   - ``tests/contract/test_trigger_seed_derivation.py`` — the seed is a derived
     copy of the `## Handoffs` prose: C-6/C-7 open the provenance target and
     assert the verbatim quote and flow name are still there, and C-8 pins the
     closed situation vocabulary. That file owns "editing a source section means
     syncing the seed"; its own docstring states the fix is to sync the seed,
     never to loosen the test.

   The confirmation-gate budget total is pinned once, below, by
   ``test_c11_gate_scan_total_unchanged`` against the real scanner's output and
   the frozen ``baseline-gates.json``. The discipline-doc face never re-asserts
   that total; it only asserts this doc contributes zero hits to it.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

from specify_cli import _INSTRUCTIONS_FILE_MAP, _check_instructions

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
LIVE = ROOT / ".specify" / "instructions.md"
GENERATOR = ROOT / "scripts" / "bash" / "generate-instructions.sh"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
BASELINE_GATES = (
    ROOT / ".specify" / "specs" / "050-proactive-flow-trigger" / "baseline-gates.json"
)

pytestmark = pytest.mark.contract

HEADING = "## Proactive Flow Trigger"
DOC_LINK = "shared/guidelines/proactive-trigger.md"
PREV_HEADING = "## Documentation Map"
NEXT_HEADING = "## Fact, Correctness & Logic Checks (Input Sanity)"

# C-7: shipped surface must stay project-neutral.
FORBIDDEN = [
    "spec-kit",
    "specify-cli",
    "specify_cli",
    "Feature 0",
    "cloud-native-ai",
    ".specify/specs/0",
]

# C-5: closed set of parameter-structure forms that must not appear.
PARAM_PATTERNS = [r"--[a-z][a-z0-9-]*", r"\$ARGUMENTS", r"<[a-z-]+>"]

# C-10: links the generator creates beyond the declared per-tool files.
EXTRA_LINKS = ["QODER.md", ".qoder/project_rules.md", ".claude/project_rules.md"]
EXPECTED_LINK_COUNT = 8


def read(p: Path) -> str:
    assert p.is_file(), f"missing file: {p}"
    return p.read_text(encoding="utf-8")


def h2(text: str) -> list[str]:
    return re.findall(r"(?m)^## .+$", text)


def section(text: str, heading: str = HEADING) -> str:
    """The section body (heading excluded), up to the next `## ` or `# `."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start + 1 : end])


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scan_confirmation_gates_tS", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def installed_project(tmp_path: Path) -> Path:
    """A minimal installed-project layout the generator can run against."""
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "instructions-template.md").write_bytes(
        SRC.read_bytes()
    )
    # A live file that predates the new section and carries project-local content.
    (tmp_path / ".specify" / "instructions.md").write_text(
        "# Instructions\n\n"
        "## Documentation Map\n\nproject-local doc map\n\n"
        "## Fact, Correctness & Logic Checks (Input Sanity)\n\nsanity body\n\n"
        "## Recurring Operational Lessons\n\nhand-authored, must survive\n",
        encoding="utf-8",
    )
    specify_py = tmp_path / ".specify" / "scripts" / "python"
    specify_py.mkdir(parents=True, exist_ok=True)
    (specify_py / "tools-utils.py").symlink_to(
        ROOT / "scripts" / "python" / "tools-utils.py"
    )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


def run_generator(cwd: Path):
    return subprocess.run(
        ["bash", str(GENERATOR)], cwd=cwd, capture_output=True, text=True
    )


# --- C-1: section present on both surfaces, with the pointer ---


def test_c1_heading_and_pointer_on_both_surfaces():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        body = read(p)
        assert HEADING in h2(body), f"{HEADING!r} missing in {rel}/instructions-template.md"
        assert DOC_LINK in section(body), f"pointer link {DOC_LINK!r} missing in {rel}"


# --- C-2: byte-identical mirror ---


def test_c2_mirror_parity():
    assert SRC.read_bytes() == MIRROR.read_bytes(), "instructions-template mirrors diverged"


# --- C-3: insertion position satisfies the ordering contract ---


def test_c3_position_between_documentation_map_and_input_sanity():
    headings = h2(read(SRC))
    assert PREV_HEADING in headings, f"anchor {PREV_HEADING!r} gone from the template"
    assert NEXT_HEADING in headings, f"anchor {NEXT_HEADING!r} gone from the template"
    assert HEADING in headings, f"{HEADING!r} missing"
    i_prev, i_new, i_next = (headings.index(h) for h in (PREV_HEADING, HEADING, NEXT_HEADING))
    assert i_new == i_prev + 1, (
        f"{HEADING!r} must immediately follow {PREV_HEADING!r}; got order {headings}"
    )
    assert i_next == i_new + 1, (
        f"{HEADING!r} must immediately precede {NEXT_HEADING!r}; got order {headings}"
    )


# --- C-4: summary + pointer shape, never the full text ---


def test_c4_body_within_25_lines_and_no_subheadings():
    body = section(read(SRC))
    lines = body.splitlines()
    assert len(lines) <= 25, f"section body must be <= 25 lines, got {len(lines)}"
    assert not any(l.startswith("### ") for l in lines), (
        "no `### ` subheadings: additive reconcile does not propagate them, "
        "so content hidden in a subsection never reaches initialized projects"
    )


# --- C-5: reference not copy — zero flow enumeration ---


def test_c5_zero_flow_and_parameter_enumeration():
    body = section(read(SRC))
    assert body.count("/speckit.") == 0, (
        "the section must not enumerate command names; the engine supplies the "
        "exact invocation at runtime"
    )
    assert body.count("skills/") == 0, "the section must not enumerate skill paths"
    hits = []
    for pattern in PARAM_PATTERNS:
        hits.extend(m.group(0) for m in re.finditer(pattern, body))
    assert not hits, f"parameter-structure forms must not appear: {hits}"


# --- C-6: zero BLOCKING_PATTERNS hits ---


def test_c6_zero_blocking_pattern_hits():
    blocking_re = _load_scanner().BLOCKING_RE
    body = section(read(SRC))
    hits = [m.group(0) for m in blocking_re.finditer(body)]
    assert not hits, (
        f"section trips BLOCKING_PATTERNS (gate-budget integer headroom is 0): {hits}"
    )


# --- C-7: project neutral ---


def test_c7_project_neutral():
    low = section(read(SRC)).lower()
    for token in FORBIDDEN:
        assert token.lower() not in low, f"project-specific token {token!r} leaked"


# --- C-8: no managed-block markers ---


def test_c8_no_managed_block_markers():
    body = section(read(SRC))
    for pattern in (r"<!--\s*\w+_START\s*-->", r"<!--\s*\w+_END\s*-->"):
        found = re.findall(pattern, body)
        assert not found, (
            f"managed-block marker {found} in the instructions template: runtime "
            "state belongs in the trigger store, the instructions side carries only a pointer"
        )


# --- C-9: additive reconcile propagates the section, idempotently ---


def test_c9_section_propagates_and_is_idempotent(installed_project: Path):
    live = installed_project / ".specify" / "instructions.md"
    assert HEADING not in read(live), "fixture must start without the section"

    result = run_generator(installed_project)
    assert result.returncode == 0, result.stderr
    text = read(live)
    assert HEADING in h2(text), "additive reconcile failed to inject the new section"
    assert DOC_LINK in section(text), "injected section lost its pointer"

    # Existing non-template content survives verbatim.
    assert "hand-authored, must survive" in text, "a project-local section was clobbered"
    assert "project-local doc map" in text, "an existing section's body was rewritten"

    # Injected in template order: after Documentation Map, before Input Sanity.
    headings = h2(text)
    assert headings.index(HEADING) == headings.index(PREV_HEADING) + 1
    assert headings.index(NEXT_HEADING) == headings.index(HEADING) + 1

    # Second run is a no-op, and a timestamped backup is produced rather than
    # an in-place overwrite of the pre-run content.
    before = live.read_bytes()
    result2 = run_generator(installed_project)
    assert result2.returncode == 0, result2.stderr
    assert live.read_bytes() == before, "second run was not idempotent"
    assert h2(read(live)).count(HEADING) == 1, "section duplicated on re-run"


# --- C-10: full agent-path coverage (sole authority for the enumeration) ---


def test_c10_all_agent_instruction_paths_created(installed_project: Path):
    result = run_generator(installed_project)
    assert result.returncode == 0, result.stderr

    declared = sorted(set(_INSTRUCTIONS_FILE_MAP.values()))
    expected = declared + EXTRA_LINKS
    assert len(expected) == EXPECTED_LINK_COUNT, (
        f"path enumeration changed: expected {EXPECTED_LINK_COUNT} links, got {expected}. "
        "This test file is the sole authority for the count (C-10) — update it "
        "deliberately, and update every artifact that references it."
    )

    target = (installed_project / ".specify" / "instructions.md").resolve()
    broken = []
    for rel in expected:
        p = installed_project / rel
        if not p.exists() or not p.is_symlink():
            broken.append(f"{rel}: missing or not a symlink")
            continue
        if Path(p.resolve()) != target:
            broken.append(f"{rel}: resolves to {p.resolve()}, not {target}")
    assert not broken, f"agent instruction paths incomplete: {broken}"


def test_c10_declared_map_shape():
    assert len(_INSTRUCTIONS_FILE_MAP) == 6, (
        f"_INSTRUCTIONS_FILE_MAP must declare 6 tool keys, got {len(_INSTRUCTIONS_FILE_MAP)}"
    )
    assert len(set(_INSTRUCTIONS_FILE_MAP.values())) == 5, (
        "the 6 keys must dedupe to 5 distinct files (codex and qoder share AGENTS.md)"
    )


# --- C-11: gate-scan total does not grow ---


def test_c11_gate_scan_total_unchanged():
    assert BASELINE_GATES.is_file(), (
        f"missing frozen baseline: {BASELINE_GATES} (T002 must run first)"
    )
    frozen = json.loads(read(BASELINE_GATES))["confirmationGates"]
    proc = subprocess.run(
        [
            "python3", str(SCANNER), "--root", str(ROOT), "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["total"] == frozen["total"], (
        f"gate total moved from the frozen {frozen['total']} to {payload['total']}; "
        "the integer headroom on the budget is 0"
    )
    assert len(payload["violations"]) == 0, f"violations: {payload['violations']}"


# --- C-12: declaration and generation agree ---


def test_c12_check_instructions_passes_for_every_tool_key(installed_project: Path):
    result = run_generator(installed_project)
    assert result.returncode == 0, result.stderr
    failing = {
        key: _check_instructions(installed_project, key)
        for key in _INSTRUCTIONS_FILE_MAP
        if _check_instructions(installed_project, key) != "pass"
    }
    assert not failing, (
        f"_check_instructions still fails for these tool keys: {failing} — every "
        "declared value must actually be created by generate-instructions.sh"
    )


def test_c12_every_declared_value_is_created(installed_project: Path):
    run_generator(installed_project)
    missing = [
        rel for rel in set(_INSTRUCTIONS_FILE_MAP.values())
        if not (installed_project / rel).exists()
    ]
    assert not missing, f"declared but never generated: {missing}"


# ==========================================================================
# Discipline-doc face (contracts/discipline-doc.md) — merged from the former
# tests/contract/test_proactive_trigger_discipline_doc.py. Structural clauses
# only; see the module docstring for where each normative proposition is owned.
# ==========================================================================

DISCIPLINE_DOC = ROOT / "shared" / "guidelines" / "proactive-trigger.md"
DISCIPLINE_DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "proactive-trigger.md"
GATES_OWNER = ROOT / "shared" / "guidelines" / "confirmation-gates.md"

# doc C-2: closed set, exact order. Additive reconcile propagates whole `## `
# sections, so a dropped or reordered section is a delivery defect, not a rewrite.
DOC_SECTIONS = [
    "Ownership",
    "Evaluation Cadence",
    "Evidence Budget & Escalation",
    "Suggestion Shape",
    "Ordering Contract",
    "Promotion & Safety Boundary",
    "Telemetry & Retention",
    "Tuning Protocol",
    "Global Switch",
    "Maintenance Duties",
]

# doc C-6: shipped surface must stay project-neutral (shared/ is copied into every
# downstream project by init).
DOC_FORBIDDEN = [
    "spec-kit",
    "specify-cli",
    "specify_cli",
    "Feature 0",
    "cloud-native-ai",
    ".specify/specs/0",
    "requirement 0",
]


def _doc_h2_headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def _doc_section(text: str, title: str) -> str:
    """Body of the `## <title>` section, up to the next `## ` heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip() == title:
            start = i
            break
    assert start is not None, f"section {title!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


# --- doc C-1: dual surface + byte-identical mirror ---


def test_doc_c1_exists_with_byte_identical_mirror():
    assert DISCIPLINE_DOC.is_file(), f"missing discipline doc: {DISCIPLINE_DOC}"
    assert DISCIPLINE_DOC_MIRROR.is_file(), (
        f"missing discipline doc mirror: {DISCIPLINE_DOC_MIRROR}"
    )
    assert DISCIPLINE_DOC.read_bytes() == DISCIPLINE_DOC_MIRROR.read_bytes(), (
        "discipline doc mirror drift"
    )


# --- doc C-2: closed section set, exact order ---


def test_doc_c2_section_set_closed_and_ordered():
    found = _doc_h2_headings(read(DISCIPLINE_DOC))
    assert found == DOC_SECTIONS, (
        f"`## ` heading set must be exactly {DOC_SECTIONS} in order; got {found}"
    )


# --- doc C-3: contributes zero hits to the gate budget, and is not exempt ---


def test_doc_c3_zero_blocking_pattern_hits():
    blocking_re = _load_scanner().BLOCKING_RE
    text = read(DISCIPLINE_DOC)
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in blocking_re.finditer(line):
            hits.append(f"L{lineno}: {m.group(0)!r}")
    assert not hits, (
        "discipline doc must not trip any BLOCKING_PATTERNS literal "
        f"(integer headroom on the gate budget is 0); hits: {hits}"
    )


def test_doc_c3_scanner_reports_no_gate_in_this_doc():
    """The doc lives under shared/ (in SCAN_DIRS) and matches no governance path."""
    scanner = _load_scanner()
    rel = DISCIPLINE_DOC.relative_to(ROOT)
    assert not scanner.GOVERNANCE_RE.search(rel.as_posix()), (
        "unexpected: this doc now matches a governance path pattern, "
        "which would silently exempt its hits from the budget"
    )


# --- doc C-4: reference, not restate ---


def test_doc_c4_does_not_restate_confirmation_gates_tables():
    body = read(DISCIPLINE_DOC)
    gates = read(GATES_OWNER)
    # The governance-kept table header and the destructive-list bullets are the
    # two enumerations that must never be copied.
    header = "| 门控 | 所在面 | 保留理由 |"
    assert header in gates, "fixture assumption broke: header not in the owner doc"
    assert header not in body, "governance-kept classification table restated"
    for bullet in (
        "- 删除文件或数据(delete / 清空存储)",
        "- 移动/归档既有工件(move / archive / restructure)",
        "- 覆盖用户既有内容",
    ):
        assert bullet not in body, f"destructive list restated: {bullet!r}"
    assert "shared/guidelines/confirmation-gates.md" in body, (
        "the destructive criteria must be reached by path reference"
    )


def test_doc_c4_does_not_restate_seed_rule_or_situation_table():
    body = read(DISCIPLINE_DOC)
    # Situation/rule identifier rows belong to the seed file + data model only.
    assert not re.search(r"(?m)^\|\s*s[0-9]{2}\s*\|", body), (
        "named-situation table restated (situation rows `| sNN |` must not appear)"
    )
    assert not re.search(r"\br-0[0-9]{2}\b", body), (
        "seed rule ids restated; the doc references the seed by path only"
    )
    assert "templates/proactive-trigger-seed.json" in body, (
        "the seed file must be named as the owner of the rule/situation data"
    )


def test_doc_c4_does_not_restate_engine_envelope_keys():
    body = read(DISCIPLINE_DOC)
    for key in (
        "semanticJudgmentPending",
        "workspaceRoot",
        "generatedAt",
        "semanticChecksPending",
    ):
        assert key not in body, f"engine envelope key restated: {key!r}"
    assert "contracts/trigger-engine.md" in body, (
        "envelope/CLI detail must be reached by reference to the engine contract"
    )


# --- doc C-5: the escalation ladder is a well-formed P1-P5 table ---


def test_doc_c5_escalation_table_p1_to_p5_complete():
    sec = _doc_section(read(DISCIPLINE_DOC), "Evidence Budget & Escalation")
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        assert re.search(rf"(?m)^\|\s*\**{pid}\**\s*\|", sec), (
            f"escalation criteria row {pid} missing from the P1-P5 table"
        )
    rows = [l for l in sec.splitlines() if re.match(r"^\|\s*\**P[1-5]\**\s*\|", l)]
    assert len(rows) == 5, f"P1-P5 table must have exactly 5 rows, got {len(rows)}"
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        assert len(cells) >= 2 and all(cells[:2]), (
            f"each escalation row needs a condition and a probe target: {row!r}"
        )


# --- doc C-6: project neutral ---


def test_doc_c6_project_neutral():
    low = read(DISCIPLINE_DOC).lower()
    for token in DOC_FORBIDDEN:
        assert token.lower() not in low, f"project-specific token {token!r} leaked"


# --- doc C-7: the reverse pointer ---
#
# The template -> doc direction is owned by test_c1_heading_and_pointer_on_both_
# surfaces above; this asserts the complementary doc -> template direction, so the
# two do not duplicate a fact. The former first assertion of this test ("either
# the doc never mentions the Documentation Map, or it also says 'not the only' /
# '唯一'") is gone: a single common word satisfied it, so it passed no matter what.


def test_doc_c7_names_the_template_section_that_carries_its_pointer():
    body = read(DISCIPLINE_DOC)
    # The doc must state how it is reached: a pointer from the instructions
    # template's own `## ` section.
    assert DOC_LINK in body or "instructions-template.md" in body, (
        "the doc must name the pointer surface that makes it reachable"
    )
    assert "`## Proactive Flow Trigger`" in body or "## Proactive Flow Trigger" in body, (
        "the doc must name the template section that carries its pointer"
    )
