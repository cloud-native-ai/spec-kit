"""Contract tests: the settlement contract owner page (spec 106, US1 / T004).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clauses: ``contracts/settlement-contract.contract.md`` C-01…C-12.

What this pins

* C-01 — exactly one closed seven-value settlement set with its three semantic classes
  and the verbatim literals ``silent-end`` / ``unknown``.
* C-02 — one row per value naming the positive evidence required and the readings that
  explicitly do not constitute it (including the closed four independent-verification
  mechanisms and the settlement boundary options ``--live-window`` / ``--wait-deadline``
  / ``--start-grace``).
* C-03 / C-04 — ``silent-end`` is an explicit terminal state (never a fallback) and
  ``unknown`` is a detection-defect state with its two finding labels.
* C-05…C-07 — attempts/labels, the start record (``<label>.attempt`` in the existing
  dispatch log root) or ``unknown``, the return channel is not liveness evidence, and
  the parent settles before it reports.
* C-08 / C-09 — report / retry / stop reactions, no silent repair, explicit-only
  cancellation.
* C-10 — the additive ``settlement_version`` and the per-shape legacy rule.
* C-11 — virtual exclusion and the foreground-terminal native branch.
* C-12 — § Role Edges keeps its four closed edge kinds; § Termination owns the closed
  three-kind settlement violation set.
* FR-013 — no second value table or second evidence matrix on the declaration surfaces
  (``shared/``, ``skills/``, ``templates/``); only the owner page carries the set.

Red-first (Constitution IV): this module was authored before the owner-section
amendment, so every leg fails on its own named missing-artifact assertion — never on an
import or collection error.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER_SRC = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"

SETTLEMENT_VALUES = (
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
)
VALUE_CLASSES = {
    "completed": "terminal",
    "failed": "terminal",
    "anomaly": "terminal",
    "cancelled": "terminal",
    "running": "non-terminal",
    "silent-end": "terminal",
    "unknown": "detection-defect",
}
CLOSED_VERIFICATION_MECHANISMS = ("u4", "team-verification", "five-element", "return-record")
EDGE_KINDS = (
    "self-dispatch",
    "dangling-parent",
    "unbacked-role-claim",
    "depth-inconsistent",
)
SETTLEMENT_KINDS = (
    "settlement-unrecorded",
    "settlement-out-of-set",
    "settlement-unbacked",
)

DECLARATION_SURFACES = ("shared", "skills", "templates")


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    return " ".join(text.split())


def _page() -> str:
    return _read(OWNER_SRC)


def _sections(text: str) -> dict:
    """Map each level-2 heading line to its body (until the next level-2 heading)."""
    sections = {}
    current = None
    body = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(body)
            current = line.strip()
            body = []
            continue
        if current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return sections


def _termination() -> str:
    sections = _sections(_page())
    hits = [heading for heading in sections if heading.startswith("## Termination")]
    assert hits, (
        "§ Termination is missing from shared/definitions/superagent-definitions.md "
        "(the settlement contract owner section, C-01)"
    )
    assert len(hits) == 1, f"exactly one § Termination section is allowed, found {hits}"
    return sections[hits[0]]


def _role_edges() -> str:
    sections = _sections(_page())
    hits = [heading for heading in sections if heading.startswith("## Role Edges")]
    assert hits, "§ Role Edges section missing"
    return sections[hits[0]]


def _tables(text: str) -> list:
    """Return every markdown table as (header_cells, [row_cells, ...])."""
    tables = []
    header = None
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None:
                tables.append((header, rows))
                header, rows = None, []
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set(":- ") and "-" in cell for cell in cells if cell):
            continue
        rows.append(cells)
    if header is not None:
        tables.append((header, rows))
    return tables


def _value_rows() -> dict:
    """Key the § Termination value table's rows by their backticked value."""
    section = _termination()
    for header, rows in _tables(section):
        if header and header[0].lower() == "value":
            keyed = {}
            for cells in rows:
                key = cells[0].strip().strip("`")
                if key in SETTLEMENT_VALUES:
                    keyed[key] = cells
            return keyed
    raise AssertionError("no settlement value table (header first cell 'Value') in § Termination")


# --------------------------------------------------------------------------- #
# C-01 — the closed seven-value set and the three semantic classes
# --------------------------------------------------------------------------- #
def test_owner_page_carries_the_verbatim_termination_lead():
    page = _page()
    assert "**Termination.**" in page, "the verbatim `**Termination.**` lead is missing"
    assert "`silent-end`" in page, "STR-001 literal `silent-end` missing"
    assert "`unknown`" in page, "STR-002 literal `unknown` missing"


def test_exactly_one_closed_seven_value_set():
    rows = _value_rows()
    assert tuple(sorted(rows)) == tuple(sorted(SETTLEMENT_VALUES)), (
        f"settlement value set diverges: {sorted(rows)}"
    )
    section = _norm(_termination())
    assert "Exactly one closed set of seven settlement values" in section, (
        "the closed-set declaration is missing"
    )
    assert "a value outside it is never coerced" in section, (
        "the no-coercion rule is missing"
    )
    for value in SETTLEMENT_VALUES:
        assert any(
            header and header[0].lower() == "value"
            for header, _rows in _tables(_termination())
        ), "value table must exist"
        assert value in rows, f"value row missing: {value}"


def test_three_semantic_classes_map_each_value():
    rows = _value_rows()
    for value, expected in VALUE_CLASSES.items():
        assert expected in rows[value][1].lower(), (
            f"{value} must be classified {expected}, got {rows[value][1]!r}"
        )
    section = _norm(_termination())
    assert "three semantic classes" in section, "the three-class declaration is missing"
    assert "`terminal`" in section and "`non-terminal`" in section and "`detection-defect`" in section


# --------------------------------------------------------------------------- #
# C-02 — per-value positive evidence and what explicitly does not count
# --------------------------------------------------------------------------- #
PER_VALUE_PHRASES = {
    "completed": (
        "success terminal record",
        "independent verification",
        "`u4`",
        "`team-verification`",
        "`five-element`",
        "`return-record`",
        "exit code 0 alone",
        "verification absent",
    ),
    "failed": (
        "non-zero terminal record",
        "named failure return",
        "without the required completion evidence",
        "explicit anomaly signal",
        "silence",
    ),
    "anomaly": (
        "explicit anomaly signal",
        "terminal evidence",
        "`ANOMALY:`",
        "stays `running`",
    ),
    "cancelled": (
        "parent-side cancellation record",
        "destructive-action discipline",
        "dropped connection",
    ),
    "running": (
        "live check performed at settlement time",
        "`--live-window`",
        "stale reading",
    ),
    "silent-end": (
        "start record",
        "execution subject gone",
        "all four terminal evidences",
        "`--wait-deadline`",
        "`wait_deadline_s`",
        "`--start-grace`",
        "`start_grace_s`",
        "no live signal",
        "`--live-window`",
        "never `silent-end`",
    ),
    "unknown": (
        "`unreadable`",
        "start-record-missing",
        "inference of success",
    ),
}


def test_every_value_row_names_positive_evidence_and_non_evidence():
    rows = _value_rows()
    for value, phrases in PER_VALUE_PHRASES.items():
        assert value in rows, f"value row missing: {value}"
        row_text = _norm(" | ".join(rows[value]))
        missing = [phrase for phrase in phrases if phrase not in row_text]
        assert not missing, f"{value} evidence row missing phrases {missing}: {row_text!r}"


def test_completion_mechanisms_are_the_closed_four():
    section = _norm(_termination())
    for mechanism in CLOSED_VERIFICATION_MECHANISMS:
        assert f"`{mechanism}`" in section, f"verification mechanism missing: {mechanism}"
    assert "closed four" in section, "the closed-four mechanism declaration is missing"
    assert "any mechanism outside the closed four" in section, (
        "the out-of-set mechanism exclusion is missing"
    )


def test_boundary_inputs_are_declared_with_defaults():
    section = _norm(_termination())
    assert "`--wait-deadline`" in section
    assert "`--live-window`" in section
    assert "`--start-grace`" in section
    assert "`--deadline-grace`" in section, (
        "the C1 post-deadline reclassification must ride the watcher's existing grace"
    )


# --------------------------------------------------------------------------- #
# C-03 / C-04 — silent-end is explicit, unknown is a detection defect
# --------------------------------------------------------------------------- #
def test_silent_end_is_not_a_fallback():
    section = _norm(_termination())
    assert "not a fallback" in section
    assert "MUST NOT be folded into `completed` or `failed`" in section
    assert "reported as still running" in section
    assert "MUST NOT be declared before the deadline" in section
    assert "settlement-time observation" in section
    assert "late return" in section and "never a rewrite" in section


def test_unknown_is_a_detection_defect_with_two_labels():
    section = _norm(_termination())
    assert "detection-defect state, never an ending" in section
    assert "`unreadable`" in section and "`start-record-missing`" in section
    assert "do not claim success" in section
    assert "names the unreadable pointers or the missing start slot" in section


# --------------------------------------------------------------------------- #
# C-05 / C-06 / C-07 — attempts, start record, return channel, settle-before-report
# --------------------------------------------------------------------------- #
def test_attempts_labels_and_start_record():
    section = _norm(_termination())
    assert "one unique label" in section
    assert "new dispatch attempt with a new label" in section
    assert "old attempt's artifacts are kept" in section
    assert "stale attempt's late return" in section
    assert "`<label>.attempt`" in section
    assert "`--logs-dir`" in section
    assert "C1 reuses its existing four-piece" in section
    assert "not a new storage root" in section
    assert "cannot prove it existed" in section
    assert "never `completed`" in section
    assert "seven-field `return_channel`" in section
    assert "silence is neither liveness nor completion" in section


def test_parent_settles_before_it_reports():
    section = _norm(_termination())
    assert "settles every attempt it opened before its own externally visible completion report" in section
    assert "incomplete and cannot claim success" in section


# --------------------------------------------------------------------------- #
# C-08 / C-09 — reactions, no silent repair, explicit-only cancellation
# --------------------------------------------------------------------------- #
def test_three_reactions_and_no_silent_repair():
    section = _norm(_termination())
    assert "**report**" in section and "**retry**" in section and "**stop**" in section
    assert "abnormal report" in section
    assert "named diagnosis or a user ruling" in section
    assert "`running` + live evidence + the stop reason" in section
    assert "silent repair" in section
    for forbidden in ("fabricate", "backfill", "rewrite", "delete evidence", "stale return"):
        assert forbidden in section, f"no-silent-repair item missing: {forbidden}"
    assert "no kill" in section, "the engine's zero-disposal authority must be stated"


def test_cancellation_is_explicit_only():
    section = _norm(_termination())
    assert "only from a parent-side explicit cancellation record" in section
    assert "MUST NOT be inferred as cancellation" in section


# --------------------------------------------------------------------------- #
# C-10 — additive version and the per-shape legacy rule
# --------------------------------------------------------------------------- #
def test_version_and_legacy_rule():
    section = _norm(_termination())
    assert "`settlement_version`" in section
    assert "annotated `legacy`" in section
    assert "never reported as compliant" in section
    assert "never rewritten" in section
    assert "does not produce a failing exit code" in section
    assert "claim file is version-bearing if and only if it carries `settlement_version`" in section
    assert "7-column header is its version declaration" in section
    assert "5-column-header row is version-less legacy" in section
    assert "exempt from all three settlement violations" in section
    assert "single deterministic refusal is `unknown`" in section
    assert "regardless of the version declaration" in section
    assert "No pre-built rejection mechanism" in section


# --------------------------------------------------------------------------- #
# C-11 — virtual exclusion and the foreground-terminal native branch
# --------------------------------------------------------------------------- #
def test_virtual_and_native_boundaries():
    section = _norm(_termination())
    assert "excluded from background settlement" in section
    assert "cannot detach from the session" in section
    assert "parent is the executor" in section
    assert "no orphan edge exists" in section
    assert "unfinished virtual work MUST NOT be reported `completed`" in section
    assert "foreground-terminal" in section
    assert "no settlement edge is created" in section


# --------------------------------------------------------------------------- #
# C-12 — the two closed violation sets
# --------------------------------------------------------------------------- #
def test_settlement_violation_set_is_closed_at_three():
    section = _norm(_termination())
    for kind in SETTLEMENT_KINDS:
        assert f"`{kind}`" in section, f"settlement violation kind missing: {kind}"
    assert "A fourth settlement kind MUST NOT be emitted before this page is revised." in section
    assert "`--action settle`" in section
    assert "read-only" in section


def test_role_edges_keeps_four_edge_kinds_and_points_at_settlement():
    role_edges = _role_edges()
    heading_tables = _tables(role_edges)
    kind_cells = set()
    for _header, rows in heading_tables:
        for cells in rows:
            kind_cells.add(cells[0].strip().strip("`"))
    for kind in EDGE_KINDS:
        assert kind in kind_cells, f"edge violation kind missing from § Role Edges: {kind}"
    assert "A fifth kind MUST NOT be emitted before this page is revised." in _norm(role_edges)
    pointer = _norm(role_edges)
    for kind in SETTLEMENT_KINDS:
        assert f"`{kind}`" in pointer, (
            "§ Role Edges must point at the three settlement violation kinds"
        )
    assert "separate closed three-kind violation set" in pointer


def test_c1_verdict_mapping_is_declared():
    section = _norm(_termination())
    for token in ("DONE", "FAILED", "ANOMALY", "INCOMPLETE", "DEAD", "NO_SIGNAL", "TIMEOUT", "RUNNING"):
        assert f"`{token}`" in section, f"C1 verdict token missing from the mapping: {token}"
    assert "`DONE` → `completed`" in section
    assert "`FAILED` → `failed`" in section
    assert "`ANOMALY` → `anomaly`" in section
    assert "`INCOMPLETE` → `failed` (incomplete)" in section
    assert "`DEAD` → `silent-end`" in section
    assert "`NO_SIGNAL` → `silent-end`" in section
    assert "`TIMEOUT` / `RUNNING` → `running`" in section


def test_carrier_inventory_is_closed():
    section = _termination()
    for carrier_id in ("C1", "C2", "C3", "C4", "C5", "C6"):
        assert carrier_id in section, f"carrier id missing from the closed inventory: {carrier_id}"
    assert "outside this list is outside the contract" in _norm(section)


# --------------------------------------------------------------------------- #
# FR-013 — no second value table / evidence matrix on the declaration surfaces
# --------------------------------------------------------------------------- #
def test_no_second_value_table_on_declaration_surfaces():
    offenders = []
    evidence_matrix_offenders = []
    for surface in DECLARATION_SURFACES:
        root = REPO_ROOT / surface
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.resolve() == OWNER_SRC.resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            present = {
                value for value in SETTLEMENT_VALUES if f"`{value}`" in text
            }
            if len(present) >= 5:
                offenders.append((path.relative_to(REPO_ROOT).as_posix(), sorted(present)))
            lowered = text.lower()
            for line in text.splitlines():
                if not line.lstrip().startswith("#"):
                    continue
                heading = line.lower()
                if "settlement" in heading and "evidence" in heading:
                    evidence_matrix_offenders.append(
                        (path.relative_to(REPO_ROOT).as_posix(), line.strip())
                    )
    assert not offenders, (
        "a second settlement value table exists on a declaration surface "
        f"(only the owner page may carry the set): {offenders}"
    )
    assert not evidence_matrix_offenders, (
        f"a second settlement evidence matrix heading exists: {evidence_matrix_offenders}"
    )
