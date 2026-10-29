"""Contract tests: compatibility, containment and the safety negative boundary (slice 074b, T019).

What this pins
--------------
`contracts/compat-and-safety.md` C-7…C-12 — the clauses the *edits* of this slice could break
without any of the three behavioural suites noticing, because they are shaped as negations:

- **C-7** the nested entry stays additive on the standalone entry contract: it is a distinct entry
  whose semantics are validation-then-refuse, it adds no branch to that six-condition validation,
  and the standalone entry's own shape is declared unchanged at its owner;
- **C-8** Feature 070's work packages remain the only in-run decomposition, and the report section
  this slice added describes no work packages;
- **C-9** Feature 058's U0–U6 contract is preserved, and the report section introduces no stage and
  no sentinel — it records an outcome and paths;
- **C-10** no automatic merge or push, no scheduler or daemon, no automatic feedback transmission, no
  second confirmation gate; the report section's outcome is data, never an integration authorization;
- **C-11** no new `/speckit.*` command and no new skill — every delivered row is an existing owner or
  a test, and the flow-class inventory stays clean;
- **C-12** no new store — the report section is text inside an existing report, the attribution row is
  one item of the existing ledger, the pointer surfaces are sections of existing documents, and the
  containment carrier is a test-evidence artifact.

Measurement rules used below
----------------------------
* **The delivery surface is read, not recalled.** `_delivery_surface()` parses the nine rows of
  `feature-ref.md` § 2 (the slice's own declaration of what it delivers, with its EDIT/NEW kind), so
  the negative clauses are decided against the files the slice says it touched rather than against a
  list copied into this module.
* **Absence needs a positive control.** "The scanner found no gate in these documents" is worthless
  if the scanner cannot see that family of document at all, so `test_c10_…` also asserts the scanner
  *does* report gates in two documents of the same families. Without that half the case would be a
  check that cannot go red.
* **Counts are not the subject.** C-11 is decided by the engine's own verdict (`0 finding(s)`,
  `gaps=0`) and by the delivery surface's path shapes, never by pinning an inventory size: a pinned
  number would go stale the first time an unrelated feature adds a legitimate unit, and would say
  nothing about *this* slice either way.
* **The section is located by its own heading**, and its body is read to the next heading. An
  extraction that silently returned the empty string would make every absence assertion below pass,
  so the extraction asserts the heading is found exactly once and the body is non-empty first.

Red shape at T019 time (recorded in `notes/red-first-evidence.md` § E-7): the module does not exist,
so the red run is `ERROR: file or directory not found` with `no tests ran` and exit 4 — the file's
absence, not a failing assertion, is the red artefact.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "074b-nested-governance"

FEATURE_REF = SLICE_DIR / "feature-ref.md"
CONTAINMENT_CARRIER = SLICE_DIR / "test-evidence" / "compat-baseline-nodeids.txt"

REPORT_OWNER = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"
SUMMARY_MAPPING = REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "summary-mapping.md"
DRIVER_SKILL = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
NESTED_INVOCATION = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "nested-invocation.md"
)
DECOMPOSITION_MODEL = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "decomposition-model.md"
)
ROUTING_ENGINE = REPO_ROOT / "scripts" / "python" / "sdd-route.py"
FLOW_CLASS_ENGINE = REPO_ROOT / ".specify" / "scripts" / "python" / "flow-class-check.py"
GATE_SCANNER = REPO_ROOT / ".specify" / "scripts" / "python" / "scan-confirmation-gates.py"

#: The heading that owns the section this slice added (its body is the whole C-8…C-12 subject).
NESTED_SECTION_HEADING = "### Nested SDD Runs section"

#: Tokens that would mean the report section had taken on an authority it must not carry (C-10).
INTEGRATION_TOKENS = (
    "MUST merge",
    "MUST push",
    "集成",
    "scheduler",
    "daemon",
    "cron",
    "确认门",
    "confirmation gate",
    "自动上送",
)

#: Store families this slice must not add to (C-12).
STORE_PREFIXES = (".specify/state/", ".specify/memory/session/", ".specify/memory/knowledge/")

#: The nine rows `feature-ref.md` § 2 declares: `| <n> | `<path>` | <KIND> | … |`.
DELIVERY_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([A-Z]+)\s*\|")


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    assert path.is_file(), f"missing artifact: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    """Body of the one heading starting with ``heading_prefix``, up to the next heading."""
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.startswith(heading_prefix)]
    assert len(starts) == 1, (
        f"expected exactly one heading starting with {heading_prefix!r}, found {len(starts)}"
    )
    start = starts[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^#{1,4} ", lines[index]):
            end = index
            break
    body = "\n".join(lines[start:end]).strip()
    assert body, f"the {heading_prefix!r} section is empty — absence checks over it would be vacuous"
    return body


def _report_section() -> str:
    return _section(_read(REPORT_OWNER), NESTED_SECTION_HEADING)


def _delivery_surface() -> list:
    rows = [
        (int(match.group(1)), match.group(2), match.group(3))
        for match in (DELIVERY_ROW.match(line) for line in _read(FEATURE_REF).splitlines())
        if match
    ]
    assert [row[0] for row in rows] == list(range(1, 10)), (
        f"feature-ref.md § 2 must declare the nine delivery rows, parsed {rows}"
    )
    return rows


def _gate_report() -> dict:
    proc = subprocess.run(
        ["python3", str(GATE_SCANNER), "--root", str(REPO_ROOT), "--json"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"gate scanner failed: {proc.stderr}"
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# C-7 — the nested entry stays an additive, validation-then-refuse entry
# ---------------------------------------------------------------------------


def test_c7_the_nested_entry_is_distinct_and_the_standalone_entry_is_declared_unchanged():
    """C-7: the nested form is its own entry, and the owner says the standalone entry did not move."""
    skill = _read(DRIVER_SKILL)
    assert "Invoked-from-Team Entry" in skill, (
        "the nested entry form must remain a distinct entry in the driver manual (C-7)"
    )
    assert "独立入口" in skill and "追加" in skill and "不是替换" in skill, (
        "the owner must still declare the standalone entry's own shape and skeleton unchanged and "
        "the nested entry purely additive (C-7)"
    )


def test_c7_the_entry_validation_stays_a_closed_six_condition_set():
    """C-7: "validation-then-refuse" is only decidable while the validation set is closed — this
    slice adds no seventh condition to it."""
    doc = _read(NESTED_INVOCATION)
    conditions = re.findall(r"^\|\s*(V-\d+)\s*\|", doc, re.MULTILINE)
    assert conditions == [f"V-{n}" for n in range(1, 7)], (
        "the entry-validation set must stay exactly V-1…V-6, in order; a seventh row would be a "
        f"branch this slice is not allowed to add (C-7). Found {conditions}"
    )
    assert "拒绝启动并点名失败的条件" in doc, (
        "the semantics must stay validation-then-refuse, not default-resolution (C-7)"
    )


def test_c7_the_routing_engine_keeps_one_closed_action_set():
    """C-7: the nested entry is one action beside the standalone ones — a new action would be a new
    entry, and this slice adds none."""
    proc = subprocess.run(
        ["python3", str(ROUTING_ENGINE), "--help"], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stderr
    assert "--action {route,authorize,golden}" in proc.stdout, (
        "the engine's action set must stay {route, authorize, golden}: `authorize` is the nested "
        "entry and the other two are the standalone forms (C-7)"
    )


# ---------------------------------------------------------------------------
# C-8 / C-9 — the in-run decomposition and the stage contract stay where they are
# ---------------------------------------------------------------------------


def test_c8_work_packages_stay_the_only_in_run_decomposition():
    """C-8: the preset keeps its role, and the report section does not describe work packages."""
    model = _read(DECOMPOSITION_MODEL)
    assert "Work Package record" in model, (
        "the in-run decomposition mechanism must remain the driver's work-package model (C-8)"
    )
    section = _report_section()
    for token in ("Work Package", "work package", "工作包"):
        assert token not in section, (
            f"the nested-run report section must not describe {token!r}: work packages stay the "
            "in-run decomposition and are not a substitute for nested invocation (C-8)"
        )


def test_c9_the_u0_u6_stage_contract_is_untouched_and_the_section_adds_no_stage():
    """C-9: the stage roster stays intact, and the section introduces neither a stage nor a
    sentinel — it records an outcome and paths."""
    skill = _read(DRIVER_SKILL)
    missing = [stage for stage in (f"U{n}" for n in range(7)) if stage not in skill]
    assert not missing, f"the U0–U6 stage contract lost {missing} (C-9)"
    section = _report_section()
    assert not re.search(r"\bU[0-6]\b", section), (
        "the report section must reference no stage: it records an outcome and paths, it does not "
        "run one (C-9)"
    )
    assert not re.search(r"-DONE\b", section), (
        "the report section must not introduce a sentinel (C-9)"
    )
    assert "哨兵" not in section, (
        "the report section must not claim or define a sentinel (C-9)"
    )


# ---------------------------------------------------------------------------
# C-10 — the safety boundary (all negations, each with a live subject)
# ---------------------------------------------------------------------------


def test_c10_integration_stays_with_the_outer_layer():
    """C-10: zero merge, zero push — stated where the nested run is bound, not in the report."""
    doc = _read(NESTED_INVOCATION) + _read(DRIVER_SKILL)
    assert "MUST NOT merge" in doc and "MUST NOT push" in doc, (
        "the nested run must still be bound to zero merge and zero push, with integration left to "
        "the outer layer (C-10)"
    )


def test_c10_the_report_section_grants_no_integration_and_starts_no_machinery():
    """C-10: the section is data. It carries no integration verb, no scheduler or daemon, no
    automatic transmission and no second gate, and it names the outer layer's own obligations as
    unchanged rather than re-deciding them."""
    section = _report_section()
    offenders = [token for token in INTEGRATION_TOKENS if token in section]
    assert not offenders, (
        "the nested-run report section may not carry integration authority or start machinery: "
        f"found {offenders} (C-10)"
    )
    assert "写者唯一" in section, (
        "the section must keep the supervisor as the sole writer and the nested run as a non-writer "
        "of tracked artifacts — that is what makes its outcome a record rather than a decision "
        "point (C-10)"
    )
    assert "## Verification" in section and "并列" in section, (
        "the section must stay a peer of `## Verification`, never a replacement for the outer "
        "run's verification duty (C-10 / C-21)"
    )


def test_c10_no_confirmation_gate_is_declared_by_any_delivered_document():
    """C-10: this slice adds no confirmation gate — decided over the slice's own delivery surface,
    with a positive control proving the scanner sees these document families at all."""
    report = _gate_report()
    gate_files = {gate["file"] for gate in report["gates"]}
    delivered = [path for _n, path, _kind in _delivery_surface() if path.endswith(".md")]
    offenders = sorted(set(delivered) & gate_files)
    assert not offenders, (
        "a delivered document declares a confirmation gate; this slice adds no second gate (C-10): "
        f"{offenders}"
    )
    assert gate_files & {
        "skills/internal/create-team/references/summary-mapping.md",
        "shared/guidelines/task-complexity-rubric.md",
    }, (
        "positive control: the scanner must report gates in sibling documents of the same families, "
        "otherwise the empty intersection above is a blind check rather than evidence (C-10)"
    )


# ---------------------------------------------------------------------------
# C-11 / C-12 — no new command, no new skill, no new store
# ---------------------------------------------------------------------------


def test_c11_the_flow_class_inventory_stays_clean():
    """C-11: the inventory keeps its finding count — the engine's verdict, not a pinned size."""
    proc = subprocess.run(
        ["python3", str(FLOW_CLASS_ENGINE), "--action", "check"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 finding(s)" in proc.stdout, (
        "the flow-class inventory reports findings; a new command or skill that this slice "
        f"introduced without a ledger row is one of the ways that happens (C-11):\n{proc.stdout}"
    )
    assert "gaps=0" in proc.stdout, (
        f"the flow-class inventory reports coverage gaps (C-11):\n{proc.stdout}"
    )


def test_c11_the_delivery_surface_adds_no_command_and_no_skill():
    """C-11: every delivered path is an existing owner being edited or a test being written."""
    rows = _delivery_surface()
    assert not [path for _n, path, _k in rows if path.startswith("templates/commands/")], (
        "no `/speckit.*` command template may appear on this slice's delivery surface (C-11)"
    )
    new_rows = [(path, kind) for _n, path, kind in rows if kind == "NEW"]
    assert new_rows, "the delivery surface must declare its NEW rows, or this check is vacuous"
    for path, kind in new_rows:
        assert path.startswith("tests/"), (
            f"a NEW row {path!r} ({kind}) is not a test: this slice creates no skill, command or "
            "engine (C-11)"
        )
    for _n, path, kind in rows:
        if kind == "EDIT":
            assert (REPO_ROOT / path).is_file(), (
                f"an EDIT row {path!r} must name an existing owner — the slice is a diff of "
                "existing owners, never a new surface (C-11)"
            )


def test_c12_no_store_is_added_and_the_carriers_are_existing_faces():
    """C-12: no registry, ledger, state spine, ownership model or integration queue is added; the
    report section is text inside an existing report, the attribution row reuses the existing
    ledger field by path, and the containment carrier is a test-evidence artifact."""
    rows = _delivery_surface()
    for _n, path, _kind in rows:
        assert not path.startswith(STORE_PREFIXES), (
            f"{path!r} is a store path; this slice adds no store (C-12)"
        )
        assert not path.endswith((".jsonl", ".json", ".sqlite", ".db")), (
            f"{path!r} is a data store file; the report section is text inside an existing report "
            "and the attribution row is one item of the existing ledger (C-12)"
        )
    assert CONTAINMENT_CARRIER.is_file(), (
        "the containment carrier must be a test-evidence artifact (C-12)"
    )
    carrier = _read(CONTAINMENT_CARRIER)
    assert [f"## S{n}" in carrier for n in range(1, 8)].count(True) == 7, (
        "the carrier must still hold its seven named sets — its shape is part of the claim (C-12)"
    )
    section = _report_section()
    assert "target_ref" in section and SUMMARY_MAPPING.name in section, (
        "the attribution row must reuse the existing ledger field and reach it by path, adding no "
        "field of its own (C-12 / C-26)"
    )
    assert "Goal 字段" in section, (
        "the section must state the Goal field set obligation it consumes (C-12)"
    )
