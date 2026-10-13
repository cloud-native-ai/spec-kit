"""Contract test: probe-definitions.md umbrella expansion (Feature 056 / US1).

Pins the dispersed-probe entity set: new Probe Classes carrying code anchors
into ``trigger-utils.py`` / ``run-determination.py`` / ``evidence-utils.py``.
Bidirectional reconcile (FR-002/FR-003): every registered anchor exists in its
named engine source, and every pinned engine anchor has a registry row. Both
sides are mutation-provable — deleting either the anchor or the row turns the
matching test red with the offending name in the assertion message.

Registry file layout contract: the ``## Classes`` / ``## Objects`` headings are
the engine-parsed contract (feedback-utils ``_table_rows`` matches them
literally); the umbrella expansion ADDS chapters (``## Handler``,
``## HandlerBinding``, ``## 非实体 probe 目录``) without renaming them.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.script_api import ROOT, feedback_utils
DEFS = ROOT / "shared" / "definitions" / "probe-definitions.md"

# Drift-detector pins (legitimate literal duplicate per One Source of Truth:
# a literal pinned in a test to detect drift). Measured 2026-10-13:
# trigger-utils.py run_probes L565 (P1-P5); run-determination.py AXES L96 +
# availability probes probe_session_store L322 / probe_evidence_lane L1061;
# evidence-utils.py LANE_NAMES L27 + probe_node L194 / probe_session_store
# L220 / probe_platforms L241.
EXPECTED_ANCHORS: dict[str, set[str]] = {
    "scripts/python/trigger-utils.py": {"run_probes"},
    "scripts/python/run-determination.py": {"AXES", "probe_session_store", "probe_evidence_lane"},
    "scripts/python/evidence-utils.py": {"LANE_NAMES", "probe_node", "probe_session_store", "probe_platforms"},
}
EXPECTED_CLASSES = {"trigger-escalation", "run-determination", "evidence-lane"}
# Canonical code_anchor cell form (authored registry form, T005):
# `scripts/python/<name>.py`:`Anchor1`,`Anchor2`,...  — one path per cell,
# anchors comma-separated in backticks after the colon.
ANCHOR_CELL_RE = re.compile(r"`(scripts/[a-z0-9./_-]+)`:(.*)")
ANCHOR_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _parse_anchor_cell(cell: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for path, rest in ANCHOR_CELL_RE.findall(cell):
        for tok in rest.split(","):
            tok = tok.strip().strip("`").strip()
            if ANCHOR_TOKEN_RE.fullmatch(tok):
                pairs.append((path, tok))
    return pairs


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = i + 1
            break
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _table_rows(text: str, heading: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for line in _section(text, heading).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if set(cells) <= {"", "-", "—"} or all(set(c) <= set("-: ") for c in cells):
            continue
        if headers is None:
            headers = cells
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def _load_defs_text() -> str:
    return DEFS.read_text(encoding="utf-8")


def test_umbrella_header_declares_framework_scope() -> None:
    text = _load_defs_text()
    assert "伞形" in text, "registry header must declare the umbrella positioning"
    assert "Feedback Probe" in text, "header must name Feedback Probe as a domain instance"


def test_dispersed_probe_classes_registered() -> None:
    classes = _table_rows(_load_defs_text(), "Classes")
    class_ids = {c.get("class_id", "") for c in classes}
    missing = EXPECTED_CLASSES - class_ids
    assert not missing, f"registry missing dispersed-probe classes: {sorted(missing)}"


def test_class_rows_carry_resolvable_code_anchors() -> None:
    text = _load_defs_text()
    classes = _table_rows(text, "Classes")
    declared: dict[tuple[str, str], list[str]] = {}
    for c in classes:
        cid = c.get("class_id", "")
        for path, anchor in _parse_anchor_cell(c.get("code_anchor", "")):
            declared.setdefault((path, anchor), []).append(cid)
    # Forward: every declared anchor resolves in its named engine source.
    for (rel, anchor), owners in sorted(declared.items()):
        source = (ROOT / rel).read_text(encoding="utf-8")
        assert re.search(rf"\b{re.escape(anchor)}\b", source), (
            f"anchor '{anchor}' declared by class {owners} does not exist in {rel}"
        )
    # Reverse: every pinned engine anchor is declared by some class row.
    for rel, anchors in sorted(EXPECTED_ANCHORS.items()):
        for anchor in sorted(anchors):
            assert (rel, anchor) in declared, (
                f"engine anchor {rel}:{anchor} has no registry class row"
            )


def test_objects_for_new_classes_use_script_units() -> None:
    text = _load_defs_text()
    classes = _table_rows(text, "Classes")
    scripts_classes = {
        c.get("class_id", "")
        for c in classes
        if _parse_anchor_cell(c.get("code_anchor", ""))
    }
    objects = _table_rows(text, "Objects")
    relevant = [o for o in objects if o.get("class_id", "") in scripts_classes]
    assert relevant, "no Probe Objects registered under the dispersed-probe classes"
    for o in relevant:
        unit = o.get("unit", "")
        assert unit.startswith("scripts/python/"), (
            f"object '{o.get('object_id', '')}': unit '{unit}' must point at its engine script"
        )


def test_feedback_utils_probe_validate_still_green() -> None:
    registry = feedback_utils.load_probe_registry(ROOT)
    assert registry["available"], "probe-definitions.md missing at framework root"
    assert registry["errors"] == [], f"registry structural errors: {registry['errors']}"


def test_registry_counts_unchanged_for_feedback_domain() -> None:
    registry = feedback_utils.load_probe_registry(ROOT)
    internal = len(registry["objects"])
    external = len(registry["external"])
    assert internal >= 72 and external == 0, (
        f"unexpected probe population shift: internal={internal} external={external}"
    )


@pytest.mark.parametrize("rel,anchor", sorted(
    (rel, a) for rel, anchors in EXPECTED_ANCHORS.items() for a in anchors
))
def test_pinned_anchor_exists_in_source(rel: str, anchor: str) -> None:
    source = (ROOT / rel).read_text(encoding="utf-8")
    assert re.search(rf"\b{re.escape(anchor)}\b", source), f"{rel} lost anchor {anchor}"
