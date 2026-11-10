"""Contract test: the `Sealed` status-domain drift guard (Feature 099, C-024…C-029).

Subject: every surface that must identify the one new status value `Sealed` in the same change —
the schema owner and each declared carrier / machine consumer C-025 enumerates:

* the schema owner — `shared/workflow/acceptance-hardening.md` § Feature Status (value
  definition, the single forward transition `Ready for Review → Sealed`, and its conditions);
* the feature-details template — § Canonical Status State Machine transition rows, the
  `**Status**` tracking bullet, and the `[FEATURE_STATUS]` glossary row;
* the feature-index template — its closed status vocabulary line;
* `shared/workflow/feature-integration.md` § Status State Machine — the `/speckit.seal`
  protocol row, plus the `Ready for Review → Completed` closure for new work;
* `skills/internal/manage-features/SKILL.md` — its `Status vocabulary` line;
* `shared/definitions/non-disposable-definitions.md` — the Status Readability domain row and
  the status × verdict table's `Sealed` row;
* `scripts/python/non-disposable-check.py` — the status × verdict table the engine judges by;
* `scripts/python/closure-acceptance-check.py` — the completion-claim family (`CLAIMED_IMPLEMENTED`,
  with `AUDIT_FAMILY` following it).

One test per surface, so removing `Sealed` from any one of them turns exactly that leg red and
the failure message names the surface (C-029). This module deliberately does NOT assert mirror
parity: the `.specify/` mirrors are one fact with one owner — the `sync-mirrors.py --check` run
recorded in this feature's test evidence — and a second copy of it here would be the drift it
claims to catch.

Red-first (099 T003): written before T006–T013 land, when none of these surfaces carries the
value. The red run is recorded in `.specify/specs/099-speckit-seal/notes/red-first-evidence.md`.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
OWNER = ROOT / "shared" / "workflow" / "acceptance-hardening.md"
INTEGRATION = ROOT / "shared" / "workflow" / "feature-integration.md"
DETAILS = ROOT / "templates" / "feature-details-template.md"
INDEX_TEMPLATE = ROOT / "templates" / "feature-index-template.md"
MANAGE_FEATURES = ROOT / "skills" / "internal" / "manage-features" / "SKILL.md"
NON_DISPOSABLE_OWNER = ROOT / "shared" / "definitions" / "non-disposable-definitions.md"
NON_DISPOSABLE_ENGINE = ROOT / "scripts" / "python" / "non-disposable-check.py"
CLOSURE_ENGINE = ROOT / "scripts" / "python" / "closure-acceptance-check.py"

SEALED = "Sealed"

#: The closed seven-value feature-status domain `Sealed` completes (C-024: exactly +1).
SEVEN_STATUSES = {
    "Draft",
    "Planned",
    "Implemented",
    "Blocked",
    "Ready for Review",
    "Sealed",
    "Completed",
}

NEXT_TOP_HEADING = re.compile(r"(?m)^##\s")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start_re: str) -> str:
    start = re.search(start_re, text, re.M)
    assert start, "section not found: %r in the file under test" % start_re
    tail = text[start.end():]
    nxt = NEXT_TOP_HEADING.search(tail)
    return tail[: nxt.start()] if nxt else tail


def _owner_feature_status() -> str:
    return _section(_read(OWNER), r"^## Feature Status")


def _template_state_machine() -> str:
    return _section(_read(DETAILS), r"^### Canonical Status State Machine")


def _transitions(text: str):
    """`[(from, to, row)]` for every `| From | To | …` row of the transition table."""
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [c.strip().strip("`").strip("*") for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        frm, to = cells[0], cells[1]
        if frm in ("From", "") or set(frm) <= {"-", ":", " "}:
            continue
        rows.append((frm, to, stripped))
    return rows


def _integration_table() -> str:
    return _section(_read(INTEGRATION), r"^## Status State Machine")


# --------------------------------------------------------------------------- #
# the schema owner
# --------------------------------------------------------------------------- #

def test_schema_owner_defines_sealed_and_its_single_transition():
    """C-025: the value and the transition are decided in § Feature Status, not in a carrier."""
    body = _owner_feature_status()
    assert SEALED in body, (
        "shared/workflow/acceptance-hardening.md § Feature Status does not define `Sealed`; "
        "the schema owner MUST decide the value before any carrier projects it (C-025)"
    )
    assert "terminal" in body.lower(), (
        "the owner MUST state that `Sealed` is terminal (FR-002 / C-026)"
    )
    assert "Ready for Review → Sealed" in body, (
        "the owner MUST carry the single forward transition `Ready for Review → Sealed` (C-024)"
    )
    assert "/speckit.seal" in body, (
        "the owner MUST name `/speckit.seal` as the transition's only owner command (C-024)"
    )
    sources = set(re.findall(r"([A-Za-z][A-Za-z ]*) → Sealed", body))
    assert sources == {"Ready for Review"}, (
        "the owner carries a transition into `Sealed` from %r; the only legal forward edge is "
        "`Ready for Review → Sealed` (C-024)" % sorted(sources)
    )
    assert "Sealed → Ready for Review" in body, (
        "the owner MUST carry the audit correction `Sealed → Ready for Review` as the only "
        "backward edge (C-026)"
    )
    assert re.search(r"(?i)evidence", body), (
        "the audit correction MUST require cited evidence (C-026)"
    )


# --------------------------------------------------------------------------- #
# the feature-details template (declared carrier)
# --------------------------------------------------------------------------- #

def test_template_transition_table_carries_the_sealed_edges_and_seven_state_set():
    """C-029 surface 1: § Canonical Status State Machine's transition table."""
    transitions = _transitions(_template_state_machine())
    assert transitions, (
        "templates/feature-details-template.md § Canonical Status State Machine carries no "
        "parseable transition rows — the surface this guard names is gone"
    )
    states = {s for frm, to, _ in transitions for s in (frm, to) if s and s != "(n/a)"}
    assert states == SEVEN_STATUSES, (
        "templates/feature-details-template.md § Canonical Status State Machine transition table "
        "MUST carry the seven-status set; measured %r (C-029 surface 1, FR-001)"
        % sorted(states)
    )
    sealed_rows = [(frm, to) for frm, to, _ in transitions if to == SEALED]
    assert sealed_rows == [("Ready for Review", SEALED)], (
        "the template MUST carry exactly one transition into `Sealed`, from `Ready for Review`; "
        "measured %r (C-024)" % sealed_rows
    )
    assert any((frm, to) == (SEALED, "Ready for Review") for frm, to, _ in transitions), (
        "the template MUST carry the narrow `Sealed → Ready for Review` audit correction (C-026)"
    )


def test_template_feature_status_token_and_status_bullet_admit_sealed():
    """C-029 surface 2: the `[FEATURE_STATUS]` glossary row and the `**Status**` bullets."""
    text = _read(DETAILS)
    token = next((l for l in text.splitlines()
                  if l.startswith("|") and "[FEATURE_STATUS]" in l), None)
    assert token, (
        "templates/feature-details-template.md lost its `[FEATURE_STATUS]` glossary row — "
        "the surface this guard names is gone"
    )
    assert SEALED in token, (
        "the `[FEATURE_STATUS]` glossary row does not admit `Sealed`: %r "
        "(C-029 surface 2, FR-001)" % token
    )
    assert re.search(r"(?m)^- \*\*Sealed\*\*:", text), (
        "the Status Tracking list carries no `- **Sealed**:` bullet; every status the token "
        "admits needs its definition-of-done bullet (C-029 surface 2)"
    )


# --------------------------------------------------------------------------- #
# the two vocabulary owners SV-06 names
# --------------------------------------------------------------------------- #

def test_index_template_vocabulary_admits_sealed():
    """C-029 surface 3: templates/feature-index-template.md's closed status vocabulary."""
    lines = [l for l in _read(INDEX_TEMPLATE).splitlines()
             if re.search(r"(?i)status vocabulary", l)]
    assert lines, (
        "templates/feature-index-template.md carries no status vocabulary line — the surface "
        "this guard names is gone"
    )
    declared = " ".join(lines)
    assert re.search(r"`%s`" % SEALED, declared), (
        "templates/feature-index-template.md's status vocabulary does not admit `Sealed`: %r "
        "(C-029 surface 3, FR-001)" % declared
    )


def test_manage_features_vocabulary_admits_sealed():
    """C-029 surface 4: skills/internal/manage-features/SKILL.md's status vocabulary."""
    row = next((l for l in _read(MANAGE_FEATURES).splitlines()
                if re.match(r"^\s*-\s*Status vocabulary:", l)), None)
    assert row, (
        "skills/internal/manage-features/SKILL.md carries no `Status vocabulary` line — the "
        "surface this guard names is gone"
    )
    members = [v.strip().strip("`") for v in row.split(":", 1)[1].split("|")]
    assert SEALED in members, (
        "skills/internal/manage-features/SKILL.md's `Status vocabulary` line does not admit "
        "`Sealed`: %r (C-029 surface 4, FR-001)" % members
    )


# --------------------------------------------------------------------------- #
# the protocol row
# --------------------------------------------------------------------------- #

def test_feature_integration_carries_the_seal_protocol_row_and_closes_completed():
    """C-029 surface 5: § Status State Machine's `/speckit.seal` protocol row."""
    table = _integration_table()
    rows = [l for l in table.splitlines() if l.startswith("| `/speckit.seal`")]
    assert len(rows) == 1, (
        "shared/workflow/feature-integration.md § Status State Machine MUST carry exactly one "
        "`/speckit.seal` protocol row; found %d (C-029 surface 5, FR-001)" % len(rows)
    )
    assert "Ready for Review → Sealed" in rows[0], (
        "the `/speckit.seal` protocol row does not carry `Ready for Review → Sealed`: %r "
        "(C-029 surface 5)" % rows[0]
    )
    assert "not restated" in rows[0], (
        "the protocol row MUST reference the owner's criteria instead of restating them: %r"
        % rows[0]
    )
    assert "Ready for Review → Completed" in table and re.search(r"(?i)closed for new work", table), (
        "§ Status State Machine MUST annotate `Ready for Review → Completed` as closed for new "
        "work and point new work at `Ready for Review → Sealed` (FR-003 / C-027)"
    )


# --------------------------------------------------------------------------- #
# the owner page and engine consumers of the status × verdict table
# --------------------------------------------------------------------------- #

def _non_disposable_status_rows():
    """Rows of the `| 注册表状态 ↓ / 闭环裁决 → | accept | block |` table."""
    text = _read(NON_DISPOSABLE_OWNER)
    start = re.search(r"(?m)^\| 注册表状态 ↓ / 闭环裁决 → \|", text)
    assert start, (
        "shared/definitions/non-disposable-definitions.md lost its status × verdict table — "
        "the surface this guard names is gone"
    )
    rows = {}
    for line in text[start.start():].splitlines()[1:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        if set(stripped.strip("|").replace(" ", "")) <= set("-:"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        rows[cells[0].strip("`")] = cells[1:]
    return rows


def test_non_disposable_owner_domain_line_admits_sealed():
    """C-029 surface 6a: the Status Readability registry-status domain line."""
    line = next((l for l in _read(NON_DISPOSABLE_OWNER).splitlines()
                 if "注册表状态值域" in l), None)
    assert line, (
        "shared/definitions/non-disposable-definitions.md carries no 注册表状态值域 row — the "
        "surface this guard names is gone"
    )
    assert SEALED in line, (
        "the Status Readability domain row does not admit `Sealed`: %r "
        "(C-029 surface 6a, FR-001)" % line
    )


def test_non_disposable_owner_status_verdict_table_carries_the_sealed_row():
    """C-029 surface 6b: the closed status × verdict table's `Sealed` row."""
    rows = _non_disposable_status_rows()
    assert SEALED in rows, (
        "the status × verdict table carries no `Sealed` row — the value falls outside the "
        "judged range instead of being judged (C-029 surface 6b, FR-001)"
    )
    accept_cell, block_cell = rows[SEALED]
    assert "✗" in block_cell, (
        "`Sealed × block` MUST be judged a contradiction (a sealed feature claims every final "
        "criterion passed); measured %r (C-029 surface 6b)" % block_cell
    )
    assert "✗" not in accept_cell, (
        "`Sealed × accept` MUST read as consistent; measured %r (C-029 surface 6b)"
        % accept_cell
    )
    family = next((l for l in _read(NON_DISPOSABLE_OWNER).splitlines()
                   if "完成声明" in l), None)
    assert family and SEALED in family, (
        "the completion-claim family sentence MUST name `Sealed` among the cells that receive "
        "`status-claims-implemented-but-blocked`: %r" % family
    )


def test_non_disposable_check_engine_judges_the_sealed_cells():
    """C-029 surface 6c: scripts/python/non-disposable-check.py's status × verdict table."""
    source = _read(NON_DISPOSABLE_ENGINE)
    table = re.search(r"def contradiction\(.*?\n(.*?)\n\s*return table\.get", source, re.S)
    assert table, (
        "scripts/python/non-disposable-check.py no longer carries its `contradiction` table — "
        "the surface this guard names is gone"
    )
    body = table.group(1)
    assert re.search(r'\("Sealed", "accept"\):\s*False', body), (
        "scripts/python/non-disposable-check.py's status × verdict table has no consistent "
        "`Sealed × accept` cell (C-029 surface 6c, FR-001)"
    )
    assert re.search(r'\("Sealed", "block"\):\s*True', body), (
        "scripts/python/non-disposable-check.py's status × verdict table has no contradictory "
        "`Sealed × block` cell (C-029 surface 6c, FR-001)"
    )


# --------------------------------------------------------------------------- #
# the closure completion-claim family
# --------------------------------------------------------------------------- #

def test_closure_completion_claim_family_admits_sealed():
    """C-029 surface 7: CLAIMED_IMPLEMENTED and the AUDIT_FAMILY that follows it."""
    source = _read(CLOSURE_ENGINE)
    claimed = re.search(r"(?m)^CLAIMED_IMPLEMENTED = \(([^)]*)\)", source)
    assert claimed, (
        "scripts/python/closure-acceptance-check.py no longer defines `CLAIMED_IMPLEMENTED` — "
        "the surface this guard names is gone"
    )
    members = [m.strip().strip('"\'') for m in claimed.group(1).split(",") if m.strip()]
    assert SEALED in members, (
        "`CLAIMED_IMPLEMENTED` does not admit `Sealed`; a sealed row would not be read as a "
        "completion claim (C-029 surface 7, plan § Disclosed Rulings 3): %r" % members
    )
    assert re.search(r"(?m)^AUDIT_FAMILY = CLAIMED_IMPLEMENTED\b", source), (
        "the audit family MUST follow the completion-claim family; a second literal list here "
        "would be the duplication this guard exists to catch (C-029 surface 7)"
    )
