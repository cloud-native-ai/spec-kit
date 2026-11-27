"""Unit tests for the batch decision engine ``scripts/python/decision-batch.py`` (Feature 112).

Package P1 authors the US1 legs red-first: every test here fails on its own missing
behaviour (the engine's scan core lands with T019…T021), never on an import error. The
tests drive the engine as a real process so exit codes and payloads are observed as a
caller observes them.

Payload schema this module pins (the scan action, ``--format json``):

* ``action`` = ``"scan"``; ``scan_time`` = ISO-8601 UTC (the only non-deterministic
  field); ``presentation_digest`` = a deterministic digest over the timestamp-free
  projection; ``result`` ∈ {``"presentation"``, ``"nothing-pending"``}.
* ``batch_context`` carries the five context-floor answers: ``why_now``,
  ``silence_meaning``, ``how_to_object``, ``what_stays_pending``,
  ``completeness_disclosure`` (plain language, rendered into the text body verbatim).
* ``bookkeeping``: ``sources`` = one row per closed source with ``source_id``,
  ``presence`` ∈ {``read``, ``absent``, ``unreadable``}, ``candidates`` and
  ``absent_reason``; ``candidates`` / ``presented_rows`` / ``duplicate_merged`` /
  ``named_exclusions`` (candidate-level exclusions with ``reason``); the identity
  ``candidates = presented_rows + duplicate_merged + len(named_exclusions)``;
  ``excluded_families`` = the C-108 named exclusion families (e.g. ``rec-row``) counted
  without becoming candidates; ``verdict`` = ``"complete"`` (refusals carry no verdict).
* ``items[]``: ``identity`` = {``subject``, ``resource_locator``}; ``sources`` =
  {``source_id``, ``carrier``, ``locator``, ``position``}; ``decision_class``;
  ``context``; ``options[]`` = the five elements; ``recommended_default`` = {``label``,
  ``status`` ∈ {``grounded``, ``no-evidence``}, ``pointers``, ``basis``};
  ``qualification`` = {``state``, ``reasons`` (closed named reasons), ``missing_fields``,
  optional ``prior_decision`` = {``pointer``, ``chosen_label``}};
  ``objection_instructions``.

Fixture rows are copied into ``tmp_path`` so scans never touch the repository fixtures;
bytecode writing is disabled for every subprocess.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "decision-batch.py"
FIXTURES = ROOT / "tests" / "fixtures" / "decision-batch"

SOURCES = ("register-open-decision-row", "authored-pending-item")
FLOOR_KEYS = ("why_now", "silence_meaning", "how_to_object", "what_stays_pending",
              "completeness_disclosure")


# --------------------------------------------------------------------------- helpers
def run_engine(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def copy_fixture(name: str, tmp_path: Path) -> Path:
    target = tmp_path / name
    shutil.copytree(FIXTURES / name, target)
    return target


def scan(root: Path, fmt: str = "json") -> subprocess.CompletedProcess:
    return run_engine("scan", "--workspace-root", str(root), "--format", fmt)


def scan_payload(root: Path) -> dict:
    proc = scan(root, "json")
    assert proc.returncode == 0, (
        f"scan exited {proc.returncode} (expected 0): {proc.stdout[-800:]} {proc.stderr[-800:]}"
    )
    try:
        return json.loads(proc.stdout)
    except ValueError as exc:  # a payload that cannot be parsed is a behaviour failure
        raise AssertionError(f"scan payload is not JSON: {exc}: {proc.stdout[:400]}")


def scan_text(root: Path) -> tuple[str, dict]:
    proc = scan(root, "text")
    assert proc.returncode == 0, (
        f"scan --format text exited {proc.returncode}: {proc.stderr[-800:]}"
    )
    return proc.stdout, scan_payload(root)


def item_by_subject(payload: dict, subject: str) -> dict:
    matches = [i for i in payload["items"] if i["identity"]["subject"] == subject]
    assert len(matches) == 1, (
        f"expected exactly one presented item with subject {subject!r}, got {len(matches)}: "
        f"{[i['identity'] for i in payload['items']]}"
    )
    return matches[0]


def snapshot(root: Path) -> list[tuple[str, int, int]]:
    entries = []
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        if path.is_file():
            stat = path.stat()
            entries.append((str(path.relative_to(root)), stat.st_size, stat.st_mtime_ns))
    return entries


def strip_timestamp(payload: dict) -> dict:
    clone = json.loads(json.dumps(payload))
    clone.pop("scan_time", None)
    return clone


# ---------------------------------------------------------------- roster & identity
def test_roster_closed_and_predicates(tmp_path: Path) -> None:
    """C-101: exactly two closed sources; candidacy by the predicates alone."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    sources = payload["bookkeeping"]["sources"]
    assert [s["source_id"] for s in sources] == list(SOURCES), (
        f"the source roster is not the closed two: {sources}"
    )
    by_id = {s["source_id"]: s for s in sources}
    assert by_id["register-open-decision-row"]["presence"] == "read"
    assert by_id["authored-pending-item"]["presence"] == "read"
    # Three open OI- rows meet the word-boundary predicate; resolved-for-v1 and
    # openness-pending do not; the fenced block never counts.
    assert by_id["register-open-decision-row"]["candidates"] == 3, by_id
    assert by_id["authored-pending-item"]["candidates"] == 2, by_id
    subjects = {i["identity"]["subject"] for i in payload["items"]}
    assert "围栏内的伪待决策项" not in subjects, "a fenced pending block was counted"
    assert "已解决项（不是候选）" not in subjects
    assert "建议不是决策项" not in subjects


def test_incomplete_block_still_candidate(tmp_path: Path) -> None:
    """C-102: a block-level defect never removes a candidate from enumeration."""
    payload = scan_payload(copy_fixture("incomplete-block", tmp_path))
    item = item_by_subject(payload, "演示缺上下文的项")
    assert item["qualification"]["state"] == "incomplete", item["qualification"]
    assert "missing-field" in item["qualification"]["reasons"], item["qualification"]
    assert "context" in item["qualification"].get("missing_fields", []), item["qualification"]
    count = item_by_subject(payload, "演示计数不符项")
    assert "option-count-mismatch" in count["qualification"]["reasons"], count["qualification"]
    missing_class = item_by_subject(payload, "演示缺类项")
    assert "class-missing" in missing_class["qualification"]["reasons"], (
        missing_class["qualification"]
    )


def test_identity_byte_equal_and_merge(tmp_path: Path) -> None:
    """C-104: repeated references merge into one row listing every source."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    item = item_by_subject(payload, "演示数据保留期")
    refs = item["sources"]
    assert sorted(r["source_id"] for r in refs) == [
        "authored-pending-item", "register-open-decision-row", "register-open-decision-row",
    ], refs
    assert payload["bookkeeping"]["presented_rows"] == 2, payload["bookkeeping"]
    assert payload["bookkeeping"]["duplicate_merged"] == 3, payload["bookkeeping"]


def test_origin_linkage_states(tmp_path: Path) -> None:
    """C-105: origin token + explicit path + exactly one match; failures stay incomplete."""
    payload = scan_payload(copy_fixture("incomplete-block", tmp_path))
    unresolved = item_by_subject(payload, "OI-911")
    assert unresolved["qualification"]["state"] == "incomplete", unresolved["qualification"]
    assert "authority-unresolved" in unresolved["qualification"]["reasons"], (
        unresolved["qualification"]
    )
    ambiguous = item_by_subject(payload, "OI-912")
    assert ambiguous["qualification"]["state"] == "incomplete", ambiguous["qualification"]
    assert "ambiguous-link" in ambiguous["qualification"]["reasons"], (
        ambiguous["qualification"]
    )
    two_source = scan_payload(copy_fixture("two-source", tmp_path / "ts"))
    linked = item_by_subject(two_source, "演示数据保留期")
    assert linked["qualification"]["state"] == "eligible", linked["qualification"]
    assert any(r["source_id"] == "register-open-decision-row" for r in linked["sources"])


def test_class_gate_states(tmp_path: Path) -> None:
    """C-106: ai-autonomous excluded; unknown class incomplete; class conflict excluded."""
    auto = scan_payload(copy_fixture("autonomous", tmp_path / "auto"))
    assert auto["items"] == [], auto["items"]
    reasons = [e["reason"] for e in auto["bookkeeping"]["named_exclusions"]]
    assert "not-human-held" in reasons, auto["bookkeeping"]

    conflict = scan_payload(copy_fixture("class-conflict", tmp_path / "conflict"))
    assert conflict["items"] == [], conflict["items"]
    not_held = [
        e for e in conflict["bookkeeping"]["named_exclusions"] if e["reason"] == "not-human-held"
    ]
    assert not_held, conflict["bookkeeping"]
    classes = set()
    for entry in not_held:
        classes.update(entry.get("classes", []))
    assert classes == {"human-interactive", "ai-autonomous"}, not_held


def test_already_resolved_read_time_join(tmp_path: Path) -> None:
    """C-107 (declared in A-26): source resolution field and prior-batch join both exclude."""
    payload = scan_payload(copy_fixture("resolution-join", tmp_path))
    subjects = {i["identity"]["subject"] for i in payload["items"]}
    assert "演示已解决来源项" not in subjects
    assert "演示已落盘项" not in subjects
    exclusions = payload["bookkeeping"]["named_exclusions"]
    reasons = [e["reason"] for e in exclusions]
    assert reasons.count("already-resolved") >= 2, exclusions
    vias = {e.get("via") for e in exclusions if e.get("reason") == "already-resolved"}
    assert "resolution-field" in vias and "prior-batch" in vias, exclusions


def test_named_exclusions_counted(tmp_path: Path) -> None:
    """C-108: exclusion families are counted by name, never silently dropped."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    families = payload["bookkeeping"].get("excluded_families", {})
    assert families.get("rec-row") == 1, payload["bookkeeping"]
    bookkeeping = payload["bookkeeping"]
    assert bookkeeping["candidates"] == (
        bookkeeping["presented_rows"]
        + bookkeeping["duplicate_merged"]
        + len(bookkeeping["named_exclusions"])
    ), bookkeeping


def test_source_presence_levels(tmp_path: Path) -> None:
    """C-109: absent roots are named empty sources; an unreadable register refuses."""
    absent = scan_payload(copy_fixture("absent-root", tmp_path / "absent"))
    by_id = {s["source_id"]: s for s in absent["bookkeeping"]["sources"]}
    for source_id in SOURCES:
        assert by_id[source_id]["presence"] == "read"
    authored = by_id["authored-pending-item"]
    assert authored.get("absent_roots"), authored
    assert absent["bookkeeping"]["verdict"] == "complete", absent["bookkeeping"]

    unreadable_root = copy_fixture("unreadable-register", tmp_path / "unreadable")
    proc = scan(unreadable_root, "json")
    assert proc.returncode == 1, (
        f"an unreadable register exited {proc.returncode}, expected 1: {proc.stdout}"
    )
    assert "register-open-decision-row" in (proc.stdout + proc.stderr), (
        f"the refusal does not name the source: {proc.stdout} {proc.stderr}"
    )
    assert "presented_rows" not in proc.stdout, "a refused scan presented a partial batch"


def test_scan_zero_write(tmp_path: Path) -> None:
    """C-110: the whole scan path writes nothing."""
    root = copy_fixture("two-source", tmp_path)
    before = snapshot(root)
    proc = scan(root, "text")
    assert proc.returncode == 0, proc.stderr
    after = snapshot(root)
    assert before == after, (
        "scan changed the workspace tree: "
        f"created={sorted(set(after) - set(before))[:3]} "
        f"removed={sorted(set(before) - set(after))[:3]}"
    )


# ------------------------------------------------------------ presentation surface
def test_presentation_order_deterministic(tmp_path: Path) -> None:
    """C-201: roster order → carrier path → occurrence position."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    order = [i["identity"]["subject"] for i in payload["items"]]
    assert order == ["演示数据保留期", "演示日志级别"], order


def test_row_slots_incomplete_named(tmp_path: Path) -> None:
    """C-202: every slot is present; a missing slot is shown empty and named, never invented."""
    payload = scan_payload(copy_fixture("incomplete-block", tmp_path))
    item = item_by_subject(payload, "演示缺上下文的项")
    assert item["context"] in (None, ""), item["context"]
    assert "context" in item["qualification"]["missing_fields"]
    # The slots that DO exist are shown in full (options + default + basis + sources).
    assert [o["label"] for o in item["options"]] == ["方案甲", "方案乙"]
    assert item["recommended_default"]["label"] == "方案甲"
    assert item["sources"], item["sources"]
    assert item["objection_instructions"], "the row carries no objection instructions"


def test_batch_context_floor(tmp_path: Path) -> None:
    """C-203: the five batch-level answers are present and rendered into the text body."""
    text, payload = scan_text(copy_fixture("two-source", tmp_path))
    context = payload["batch_context"]
    for key in FLOOR_KEYS:
        assert context.get(key), f"batch_context lacks {key}: {context}"
        assert str(context[key]) in text, (
            f"the text body does not render the {key} answer: {context[key]!r}"
        )


def test_no_truncation_all_rows(tmp_path: Path) -> None:
    """C-205: every presented item appears in full; no cap, no summary replacement."""
    text, payload = scan_text(copy_fixture("two-source", tmp_path))
    assert payload["items"], "the fixture presents no rows"
    for item in payload["items"]:
        assert item["identity"]["subject"] in text, item["identity"]
        for option in item["options"]:
            assert option["label"] in text, (item["identity"], option)


def test_scan_twice_field_identical(tmp_path: Path) -> None:
    """C-206: two scans differ only in the scan timestamp."""
    root = copy_fixture("two-source", tmp_path)
    first = scan_payload(root)
    second = scan_payload(root)
    assert strip_timestamp(first) == strip_timestamp(second), (
        "two scans of the same tree differ beyond scan_time"
    )


def test_autonomous_presented_zero(tmp_path: Path) -> None:
    """C-207: zero ai-autonomous presentations, with the exclusion counted."""
    payload = scan_payload(copy_fixture("autonomous", tmp_path))
    assert payload["items"] == [], payload["items"]
    assert payload["bookkeeping"]["presented_rows"] == 0
    assert any(e["reason"] == "not-human-held" for e in payload["bookkeeping"]["named_exclusions"])


# ------------------------------------------------------ recommended default & grounding
def test_default_is_declared_member(tmp_path: Path) -> None:
    """C-301: the recommended default is exactly the block's declared default member."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    item = item_by_subject(payload, "演示数据保留期")
    declared = [o["label"] for o in item["options"] if o["default"] == "yes"]
    assert declared == ["保留 30 天"], declared
    assert item["recommended_default"]["label"] == declared[0]


def test_no_default_presented_not_settled(tmp_path: Path) -> None:
    """C-302: zero default markers present as no-default with the cardinality defect named."""
    payload = scan_payload(copy_fixture("incomplete-block", tmp_path))
    item = item_by_subject(payload, "演示无默认项")
    assert item["qualification"]["state"] == "no-default", item["qualification"]
    assert item["qualification"]["reasons"], "the cardinality defect is not named"
    assert item["recommended_default"]["label"] in (None, ""), item["recommended_default"]


def test_grounding_join_closed_inputs(tmp_path: Path) -> None:
    """C-303: the grounding join reads the closed prior-experience carriers deterministically."""
    payload = scan_payload(copy_fixture("grounding-grounded", tmp_path))
    item = item_by_subject(payload, "演示接地项")
    grounding = item["recommended_default"]
    assert grounding["status"] == "grounded", grounding
    assert grounding["pointers"], grounding
    assert any("prior-records.md" in p for p in grounding["pointers"]), grounding


def test_grounded_pointers_all_resolve(tmp_path: Path) -> None:
    """C-304: every emitted pointer resolves (path exists; an anchor is findable)."""
    root = copy_fixture("grounding-grounded", tmp_path)
    payload = scan_payload(root)
    item = item_by_subject(payload, "演示接地项")
    pointers = item["recommended_default"]["pointers"]
    assert pointers
    for pointer in pointers:
        target, _, anchor = str(pointer).partition("#")
        path = root / target
        assert path.is_file(), f"emitted pointer does not resolve: {pointer!r}"
        if anchor:
            assert anchor in path.read_text(encoding="utf-8"), (
                f"emitted pointer anchor is not findable: {pointer!r}"
            )


def test_no_evidence_explicit(tmp_path: Path) -> None:
    """C-305: no resolvable prior-experience pointer reads no-evidence, never a soft claim."""
    payload = scan_payload(copy_fixture("grounding-none", tmp_path))
    item = item_by_subject(payload, "演示无证据项")
    grounding = item["recommended_default"]
    assert grounding["status"] == "no-evidence", grounding
    assert grounding["pointers"] == [], grounding


def test_prior_conflict_detected(tmp_path: Path) -> None:
    """C-306: a prior record with a different chosen option presents prior-decision-conflict."""
    payload = scan_payload(copy_fixture("prior-conflict", tmp_path))
    item = item_by_subject(payload, "演示前例冲突项")
    assert item["qualification"]["state"] == "prior-decision-conflict", item["qualification"]
    prior = item["qualification"].get("prior_decision") or {}
    assert "history-records.md" in str(prior.get("pointer", "")), prior
    assert prior.get("chosen_label") == "保留 90 天", prior