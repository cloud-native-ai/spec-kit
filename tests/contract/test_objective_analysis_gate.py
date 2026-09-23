"""Contract test: the objective-analysis gate (same-author detection delegation).

Owner document: ``shared/workflow/objective-analysis-gate.md``.

This test is the authoritative roster of binding commands. Per the owner-selection
order in ``shared/guidelines/one-source-of-truth.md`` a fact a program can derive
belongs to code, so the owner document points here instead of restating the list.

Two shapes of drift are guarded:

* the gate stops being reachable -- the owner doc, its mirror, its Documentation
  Map row, or a binding command's pointer goes missing;
* the gate stops being owned -- a command template restates the owner's rule body
  instead of linking it, or the owner starts carrying per-command severity
  vocabulary that each template already owns.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SOURCE = REPO_ROOT / "shared" / "workflow" / "objective-analysis-gate.md"
MIRROR = REPO_ROOT / ".specify" / "shared" / "workflow" / "objective-analysis-gate.md"
SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
INSTR_TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
INSTR_LIVE = REPO_ROOT / ".specify" / "instructions.md"

LINK = "objective-analysis-gate.md"
MAP_ROW_LABEL = "| **Objective Analysis** |"
MAP_ROW_TARGET = ".specify/shared/workflow/objective-analysis-gate.md"

# cmd -> the literal cap token its own pointer must name. Severity vocabulary is
# owned by each command template, so the owner doc states the cap only as "the
# command's mid tier" and each pointer supplies its local literal. Commands with
# no tier vocabulary name the local analogue instead.
BINDING = {
    "analyze": "MEDIUM",
    "review": "P1",
    "clarify": "downstream artifact",
    "plan": "Partial",
    "checklist": "CHK",
}

NOT_BINDING = ["todo", "session", "feature", "constitution", "implement", "tasks"]

# The eight gate rules, by bold label. Asserted as labels, never as a count --
# a count would be a second fact free to drift from the list it summarizes.
GATE_RULES = [
    "Split by disjoint artifact scope",
    "Name the same-author condition in the brief",
    "Require a propagation-surface answer before any severity",
    "Treat every mapping table as an assertion, never as evidence",
    "Keep detection and validation disjoint",
    "Report the condition and the downgrade rate",
    "Subagent-unavailable fallback",
    "Derive every briefing premise mechanically before dispatch",
]

# Rules 1-6 are exclusively the owner's. Rule 7's label is deliberately NOT in
# this list: "Subagent-unavailable fallback" pre-exists as local content in the
# validation sections of analyze.md, review.md and plan.md, where it governs the
# validation wave rather than detection. Asserting its absence would demand
# deleting rules that were correct before this gate existed. Rule 8 (briefing
# premises machine-derived) is likewise outside the first six: it binds the
# orchestrator's dispatch brief, and a command MAY name it locally without
# copying the owner's body -- the slice stays the six detection-delegation rules.
#
# Matched as bare phrases, not as `**label**`: bold punctuation varies (a label
# may carry its period inside the markers), and an assertion that only passes on
# a punctuation mismatch is a false green.
RESTATED_IN_COMMANDS_FORBIDDEN = GATE_RULES[:6]

# Shipped surfaces must stay project-neutral.
FORBIDDEN = [
    "spec-kit", "specify-cli", "specify_cli", "Feature 0",
    "cloud-native-ai", ".specify/specs/0",
]

# A pointer region is one line. Bounded so the reference cannot quietly grow into
# a copy of the owner's rule body (same bound as test_docs_step_injection.py).
MAX_POINTER_REGION = 1500


def _read(path: Path) -> str:
    assert path.is_file(), f"missing artifact: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _pointer_regions(text: str) -> list[str]:
    """The lines that carry the pointer.

    Measured per line, not per paragraph: a pointer may sit inside a nested list
    (plan.md's Constitution Check step) where the surrounding block has no blank
    lines, so paragraph-splitting would measure unrelated list content and the
    length bound would test the wrong thing. Every pointer is written as a single
    unwrapped markdown line, so the line is the faithful unit.
    """
    return [line for line in text.splitlines() if LINK in line]


def _load_scanner():
    """Load the real gate scanner and reuse its BLOCKING_RE -- never a copy."""
    spec = importlib.util.spec_from_file_location("_scan_gates_oag", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _blocking_hits(text: str) -> list[str]:
    scanner = _load_scanner()
    return [line for line in text.splitlines() if scanner.BLOCKING_RE.search(line)]


# --- owner doc: exists, mirrored, declares ownership ---


@pytest.mark.contract
def test_owner_doc_exists_and_mirror_is_byte_identical():
    assert SOURCE.read_bytes() == MIRROR.read_bytes(), (
        "objective-analysis-gate mirror drift -- run "
        "`python3 scripts/python/sync-mirrors.py --write shared`"
    )


@pytest.mark.contract
def test_owner_declares_ownership_in_its_opening_lines():
    head = "\n".join(_read(SOURCE).splitlines()[:6])
    assert "Canonical convention" in head, "opener must announce the convention"
    assert "single source of truth" in head, "opener must declare ownership"
    assert "rather than restating it" in head, (
        "opener must state the reference-not-copy obligation on consumers"
    )


@pytest.mark.contract
@pytest.mark.parametrize("label", GATE_RULES)
def test_owner_carries_every_gate_rule(label: str):
    assert f"**{label}**" in _read(SOURCE), f"owner doc lost gate rule: {label}"


@pytest.mark.contract
def test_owner_defers_the_binding_roster_to_this_test():
    text = _read(SOURCE)
    assert Path(__file__).name in text, (
        "the owner must name this test as the roster owner rather than restating the roster"
    )
    for cmd in BINDING:
        assert f"/speckit.{cmd}" not in text, (
            f"owner doc restates a binding command ({cmd}); the roster belongs to this test"
        )


@pytest.mark.contract
def test_owner_defers_severity_vocabulary_to_the_commands():
    text = _read(SOURCE)
    assert "owned locally" in text, "owner must state that tier vocabulary is owned by each command"
    assert "mid tier" in text, "owner must state the cap generically"
    # No per-command tier table: those literals belong to each template.
    assert "P0/P1/P2" not in text and "CRITICAL/HIGH/MEDIUM/LOW" not in text, (
        "owner doc must not carry a per-command severity table"
    )


@pytest.mark.contract
def test_owner_names_its_exemptions():
    text = _read(SOURCE)
    assert "validate-tasks.py" in text, "deterministic program validators must be exempt"
    assert "no authorship bias" in text, "the exemption needs its reason, not just its verdict"
    assert "自省" in text, "explicit self-reflection must be exempt"
    assert "/speckit.derive" in text, "external-source verification must be exempt"


@pytest.mark.contract
def test_owner_records_the_measurement_as_dated_not_as_a_threshold():
    text = _read(SOURCE)
    assert "never a threshold" in text, (
        "the 12/10 downgrade observation is a dated record and must not read as a live threshold"
    )


# --- ambient reachability: the Documentation Map row ---


@pytest.mark.contract
@pytest.mark.parametrize("path", [INSTR_TEMPLATE, INSTR_LIVE], ids=["template", "live"])
def test_documentation_map_row_present(path: Path):
    text = _read(path)
    assert MAP_ROW_LABEL in text, f"{path.name} lost the Objective Analysis Documentation Map row"
    row = next(line for line in text.splitlines() if line.startswith(MAP_ROW_LABEL))
    assert MAP_ROW_TARGET in row, "the row must point at the installed owner path"


@pytest.mark.contract
def test_documentation_map_row_reach_is_not_overclaimed():
    # generate-instructions.sh reconciles at top-level `## ` section granularity,
    # so a new table ROW cannot reach an already-initialized project. The owner
    # doc must say so instead of implying the row propagates everywhere.
    text = _read(SOURCE)
    assert "section granularity" in text, (
        "owner doc must record that the Map row does not propagate to initialized projects"
    )


# --- binding commands: pointer present, names its local cap, stays a reference ---


@pytest.mark.contract
@pytest.mark.parametrize("cmd", sorted(BINDING))
def test_binding_command_carries_the_pointer(cmd: str):
    assert LINK in _read(COMMANDS_DIR / f"{cmd}.md"), (
        f"{cmd}.md must reference the objective-analysis gate"
    )


@pytest.mark.contract
@pytest.mark.parametrize("cmd,cap", sorted(BINDING.items()))
def test_pointer_names_its_own_local_cap(cmd: str, cap: str):
    regions = _pointer_regions(_read(COMMANDS_DIR / f"{cmd}.md"))
    assert regions, f"{cmd}.md references the gate but not from an identifiable paragraph"
    assert any(cap in r for r in regions), (
        f"{cmd}.md's pointer must name its own literal cap ({cap!r}); "
        "the owner states the cap only as 'the command's mid tier'"
    )


@pytest.mark.contract
@pytest.mark.parametrize("cmd", sorted(BINDING))
def test_pointer_references_not_copies(cmd: str):
    for region in _pointer_regions(_read(COMMANDS_DIR / f"{cmd}.md")):
        assert len(region) < MAX_POINTER_REGION, (
            f"{cmd}.md's pointer grew into a copy of the owner's rules "
            f"({len(region)} chars); link the owner instead"
        )


@pytest.mark.contract
@pytest.mark.parametrize("label", RESTATED_IN_COMMANDS_FORBIDDEN)
def test_owned_rule_labels_are_not_restated_in_any_command(label: str):
    offenders = sorted(
        p.name for p in COMMANDS_DIR.glob("*.md") if label in p.read_text(encoding="utf-8")
    )
    assert not offenders, (
        f"these command templates restate an owned rule body ({label}): {offenders} -- "
        "a restated rule is a copy free to drift; link the owner doc instead"
    )


@pytest.mark.contract
@pytest.mark.parametrize("cmd", NOT_BINDING)
def test_non_binding_commands_stay_clean(cmd: str):
    assert LINK not in _read(COMMANDS_DIR / f"{cmd}.md"), (
        f"{cmd}.md must not carry the gate -- it produces no findings about self-authored artifacts"
    )


# --- wording safety and neutrality on shipped surfaces ---


@pytest.mark.contract
def test_owner_doc_is_gate_neutral():
    # The gate budget has zero integer headroom: any new BLOCKING_RE hit inside
    # scan scope breaks test_proactive_trigger_section.py's pinned total.
    hits = _blocking_hits(_read(SOURCE))
    assert not hits, f"owner doc adds blocking-gate wording: {hits[:3]}"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", sorted(BINDING))
def test_pointer_regions_are_gate_neutral(cmd: str):
    for region in _pointer_regions(_read(COMMANDS_DIR / f"{cmd}.md")):
        hits = _blocking_hits(region)
        assert not hits, f"{cmd}.md's pointer adds blocking-gate wording: {hits[:3]}"


@pytest.mark.contract
def test_owner_doc_stays_project_neutral():
    text = _read(SOURCE)
    for token in FORBIDDEN:
        assert token not in text, f"shipped surface leaks a project-specific identifier: {token}"


# --- F-06: the detection contract gains an emitted field, not just prose -------
#
# Rule 3's propagation-surface answer used to exist only as a prose obligation, so
# the orchestrator could not machine-check that a detector applied it. These pins
# guard the two halves of the fix: the owner states the OUTPUT FORM (rule 3) and the
# briefing-premise rule (rule 8), and analyze.md emits the field as a report column
# with a matching intake rule and a stable, scope-free ID scheme.


@pytest.mark.contract
def test_owner_rule3_states_the_propagation_surface_output_form():
    text = _read(SOURCE)
    # The finding row's first field is the propagation surface; severity is derived from it.
    assert "Output form" in text, "rule 3 lost its output-form sentence"
    assert "FIRST field" in text, "rule 3 must fix the propagation surface as the row's first field"
    assert "DERIVED" in text, "rule 3 must state severity is derived from the propagation surface"


@pytest.mark.contract
def test_owner_rule8_requires_machine_derived_briefing_premises():
    text = _read(SOURCE)
    # A wrong premise in the brief aims the whole pass at the wrong target, so every
    # count/structural premise is machine-derived; what cannot be derived is an open question.
    assert "machine-derived before dispatch" in text
    assert "open question" in text
    assert "never as an assertion" in text


@pytest.mark.contract
def test_analyze_report_form_emits_propagation_surface():
    text = _read(COMMANDS_DIR / "analyze.md")
    # F-06①: the §6 report table carries a propagation_surface column, placed BEFORE
    # Severity so the row reads as "severity derived from propagation surface".
    header = next(
        (l for l in text.splitlines() if l.startswith("| ID | Category |")),
        "",
    )
    cols = [c.strip() for c in header.strip().strip("|").split("|")]
    assert "propagation_surface" in cols, f"§6 table lost the propagation_surface column: {cols}"
    # anti-vacuity: the pre-existing columns are still there, so the order claim is meaningful
    for c in ("ID", "Category", "Severity", "Recommendation"):
        assert c in cols, f"§6 table lost a pre-existing column {c!r}: {cols}"
    assert cols.index("propagation_surface") < cols.index("Severity"), (
        f"propagation_surface must precede Severity (severity is derived from it): {cols}"
    )
    # F-06④: IDs are category-initial prefixed and stable; scope lives in Category, never in the ID.
    assert "category initial" in text, "§6 lost the category-initial ID rule"
    assert "MUST NOT carry a scope-letter prefix" in text, (
        "§6 lost the no-scope-letter ID rule the rerun delta depends on"
    )
    # F-06⑤: a cluster-level slot that aggregates MEDIUM findings without re-tiering any row.
    assert "Systemic Observations" in text, "§6 lost the Systemic Observations slot"
    assert "WITHOUT raising any single row's severity" in text, (
        "Systemic Observations must not become a licence to inflate a single severity"
    )
    # F-06①: §5.5 intake -- a `none` propagation_surface row is capped at MEDIUM and is
    # never dispatched to the validation wave as CRITICAL/HIGH.
    assert "Propagation-surface intake" in text, "§5.5 lost the propagation-surface intake rule"
    assert "MUST NOT be dispatched to this wave as CRITICAL/HIGH" in text, (
        "§5.5 intake must bar a `none` row from the CRITICAL/HIGH validation wave"
    )
