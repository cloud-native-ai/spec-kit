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

# =====================================================================================
# US2 — objection reply, silence, settlement and the batch record (T024 red-first;
# green claimed at T032). The record action is unimplemented until T029/T030, so every
# test below fails on its own missing behaviour, never on an import error.
# =====================================================================================

def write_presentation(root: Path, target: Path) -> Path:
    proc = scan(root, "json")
    assert proc.returncode == 0, f"scan exited {proc.returncode}: {proc.stderr[-600:]}"
    target.write_text(proc.stdout, encoding="utf-8")
    return target


def write_reply(target: Path, text: str) -> Path:
    target.write_text(text, encoding="utf-8")
    return target


def record(root: Path, presentation: Path, reply: Path | None = None,
           authorization: str | None = "interactive",
           fmt: str = "json") -> subprocess.CompletedProcess:
    args = ["record", "--workspace-root", str(root), "--presentation", str(presentation)]
    if reply is not None:
        args += ["--reply", str(reply)]
    if authorization is not None:
        args += ["--authorization", authorization]
    args += ["--format", fmt]
    return run_engine(*args)


def record_payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.returncode == 0, (
        f"record exited {proc.returncode}: {proc.stdout[-800:]} {proc.stderr[-800:]}"
    )
    return json.loads(proc.stdout)


def knowledge_files(root: Path) -> list[Path]:
    directory = root / ".specify" / "knowledge"
    return sorted(directory.glob("*.md")) if directory.is_dir() else []


def single_record_text(root: Path) -> str:
    files = knowledge_files(root)
    assert len(files) == 1, f"expected exactly one batch record, found {files}"
    return files[0].read_text(encoding="utf-8")


def row_line(record_text: str, subject: str) -> str:
    matches = [line for line in record_text.splitlines()
               if line.startswith("|") and f"| {subject} |" in line]
    assert len(matches) == 1, f"expected one item row for {subject!r}: {matches}"
    return matches[0]


def frontmatter(record_text: str) -> dict:
    head = record_text.split("---", 2)[1]
    meta: dict = {}
    for line in head.splitlines():
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match:
            meta[match.group(1)] = match.group(2).strip().strip('"')
    return meta


def decision_blocks(record_text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] | None = None
    for line in record_text.splitlines():
        if line.startswith("### D-"):
            if current:
                blocks.append("\n".join(current))
            current = [line]
        elif line.startswith("#"):
            if current:
                blocks.append("\n".join(current))
                current = None
        elif current is not None:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


NO_OBJECTIONS_REPLY = """reply_verbatim: |
  没有异议，按建议默认值处理。
no_objections: true
"""


def test_reply_forms_and_abort_zero_records(tmp_path: Path) -> None:
    """C-401: an abort / a follow-up-only file / an empty reply write zero records."""
    root = copy_fixture("reply-shapes", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")

    missing = record(root, presentation, reply=None)
    assert missing.returncode != 0, "record accepted a missing reply file"
    assert knowledge_files(root) == []

    empty = write_reply(tmp_path / "empty.md", "   \n\n")
    refused_empty = record(root, presentation, reply=empty)
    assert refused_empty.returncode == 1, (
        f"an empty reply exited {refused_empty.returncode}, expected 1: {refused_empty.stdout}"
    )
    assert knowledge_files(root) == []

    follow_up_only = write_reply(
        tmp_path / "follow-up.md",
        "reply_verbatim: |\n  这一项为什么建议保留 30 天？\n",
    )
    refused_follow_up = record(root, presentation, reply=follow_up_only)
    assert refused_follow_up.returncode == 1, (
        "a follow-up-only file without structured entries or a no-objections "
        f"declaration was treated as a reply: {refused_follow_up.stdout}"
    )
    assert knowledge_files(root) == []


def test_objection_binds_identity_verbatim(tmp_path: Path) -> None:
    """C-402: objections bind by identity; the verbatim reply is preserved in a blockquote."""
    root = copy_fixture("reply-shapes", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    verbatim_line = "只改「演示应答甲」为「保留 90 天」，其余没意见。"
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n"
        f"  {verbatim_line}\n"
        "objections:\n"
        "  - subject: 演示应答甲\n"
        "    action: alternative\n"
        "    option_label: 保留 90 天\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    text = single_record_text(root)

    assert f"> {verbatim_line}" in text, "the verbatim reply is not preserved in a blockquote"
    first = row_line(text, "演示应答甲")
    second = row_line(text, "演示应答乙")
    assert "objected-alternative" in first, first
    assert "accepted-default" in second, second
    decisions = decision_blocks(text)
    assert len(decisions) == 2, decisions
    chosen = [block for block in decisions if "保留 90 天" in block]
    assert len(chosen) == 1, decisions
    chosen_block = chosen[0]
    assert "- **chosen_option**: 保留 90 天" in chosen_block
    assert "- **rationale**:" in chosen_block
    rationale = next(line for line in chosen_block.splitlines()
                     if line.startswith("- **rationale**:"))
    assert "改选" in rationale, rationale
    assert verbatim_line not in rationale, (
        "the rationale restates the verbatim reply instead of key points only")
    assert payload["settled"] == 2 and payload["parked"] == 0


def test_reply_membership_refusals(tmp_path: Path) -> None:
    """C-403: unknown identity, duplicate entries and non-member labels are refused, zero writes."""
    root = copy_fixture("reply-shapes", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")

    non_member = write_reply(tmp_path / "non-member.md", (
        "reply_verbatim: |\n  我想改成「保留 365 天」。\n"
        "objections:\n"
        "  - subject: 演示应答甲\n"
        "    action: alternative\n"
        "    option_label: 保留 365 天\n"
        "no_objections: false\n"
    ))
    refused = record(root, presentation, reply=non_member)
    assert refused.returncode == 1, refused.stdout
    combined = refused.stdout + refused.stderr
    assert "保留 365 天" in combined and "other" in combined.lower() and "path" in combined.lower(), (
        f"the refusal does not state the membership / other-path rule: {combined}"
    )
    assert knowledge_files(root) == []

    unknown = write_reply(tmp_path / "unknown.md", (
        "reply_verbatim: |\n  改一下那个别的事项。\n"
        "objections:\n"
        "  - subject: 不存在的项\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    refused = record(root, presentation, reply=unknown)
    assert refused.returncode == 1, refused.stdout
    assert knowledge_files(root) == []

    duplicate = write_reply(tmp_path / "duplicate.md", (
        "reply_verbatim: |\n  两项都要改。\n"
        "objections:\n"
        "  - subject: 演示应答甲\n"
        "    action: park\n"
        "  - subject: 演示应答甲\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    refused = record(root, presentation, reply=duplicate)
    assert refused.returncode == 1, refused.stdout
    assert knowledge_files(root) == []


def test_silence_eligibility_matrix(tmp_path: Path) -> None:
    """C-404: a zero-objection reply settles only the eligible item; the rest stay pending."""
    root = copy_fixture("eligibility-matrix", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    payload = record_payload(record(root, presentation, reply=reply))
    text = single_record_text(root)

    assert payload["settled"] == 1 and payload["pending"] == 4, payload
    assert payload["decisions"] == [
        {"subject": "演示矩阵合格项", "disposition": "accepted-default", "decision_id": "D-001"}
    ], payload["decisions"]
    assert "accepted-default" in row_line(text, "演示矩阵合格项")
    assert "irreversible-default" in row_line(text, "演示矩阵不可逆项")
    assert "no-default" in row_line(text, "演示矩阵无默认项")
    assert "prior-decision-conflict" in row_line(text, "演示矩阵前例冲突项")
    assert "incomplete" in row_line(text, "演示矩阵不完整项")
    for subject in ("演示矩阵不可逆项", "演示矩阵无默认项", "演示矩阵前例冲突项", "演示矩阵不完整项"):
        assert "pending" in row_line(text, subject), subject
    assert len(decision_blocks(text)) == 1


def test_park_no_record_stays_pending(tmp_path: Path) -> None:
    """C-405: a park produces no decision record, the row is carried and the item re-presents."""
    root = copy_fixture("eligibility-matrix", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  先放下「演示矩阵合格项」。\n"
        "objections:\n"
        "  - subject: 演示矩阵合格项\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    text = single_record_text(root)

    assert payload["parked"] == 1 and payload["settled"] == 0, payload
    assert "objected-parked" in row_line(text, "演示矩阵合格项")
    assert decision_blocks(text) == []
    again = scan_payload(root)
    assert "演示矩阵合格项" in {item["identity"]["subject"] for item in again["items"]}, (
        "a parked item was not presented again by the next scan"
    )


def test_unattended_and_missing_authorization_refused(tmp_path: Path) -> None:
    """C-406: unattended and undeclared authorization are refused at record, zero writes."""
    root = copy_fixture("eligibility-matrix", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)

    unattended = record(root, presentation, reply=reply, authorization="unattended")
    assert unattended.returncode == 1, (
        f"an unattended record exited {unattended.returncode}, expected 1: {unattended.stdout}"
    )
    assert "authorization" in (unattended.stdout + unattended.stderr).lower()
    assert knowledge_files(root) == []

    undeclared = record(root, presentation, reply=reply, authorization=None)
    assert undeclared.returncode == 1, undeclared.stdout
    assert knowledge_files(root) == []

    read_only = run_engine("scan", "--workspace-root", str(root), "--format", "json",
                           "--authorization", "unattended")
    assert read_only.returncode == 0, read_only.stderr


def test_ineligible_explicit_settlement(tmp_path: Path) -> None:
    """C-407: explicit alternatives settle ineligible items; an unresolvable record refuses."""
    root = copy_fixture("eligibility-matrix", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  不可逆项改成「方案乙」，无默认项选「方案甲」。\n"
        "objections:\n"
        "  - subject: 演示矩阵不可逆项\n"
        "    action: alternative\n"
        "    option_label: 方案乙\n"
        "  - subject: 演示矩阵无默认项\n"
        "    action: alternative\n"
        "    option_label: 方案甲\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    text = single_record_text(root)

    assert payload["settled"] == 3, payload  # the eligible silence row plus the two objections
    irreversible = row_line(text, "演示矩阵不可逆项")
    no_default = row_line(text, "演示矩阵无默认项")
    assert "irreversible-default" in irreversible and "objected-alternative" in irreversible
    assert "no-default" in no_default and "objected-alternative" in no_default

    broken = copy_fixture("eligibility-matrix", tmp_path / "broken")
    broken_presentation = write_presentation(broken, tmp_path / "broken-scan.json")
    broken_reply = write_reply(tmp_path / "broken-reply.md", (
        "reply_verbatim: |\n  不完整项选「方案甲」。\n"
        "objections:\n"
        "  - subject: 演示矩阵不完整项\n"
        "    action: alternative\n"
        "    option_label: 方案甲\n"
        "no_objections: false\n"
    ))
    refused = record(broken, broken_presentation, reply=broken_reply)
    assert refused.returncode == 1, refused.stdout
    assert "incomplete" in (refused.stdout + refused.stderr).lower()
    assert knowledge_files(broken) == []


def test_no_cross_batch_preauthorization(tmp_path: Path) -> None:
    """C-409: batch two neither re-settles batch one's identity nor reuses its records."""
    root = copy_fixture("drift", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan1.json")
    reply = write_reply(tmp_path / "reply1.md", (
        "reply_verbatim: |\n  「演示漂移乙」先放着，其余按建议。\n"
        "objections:\n"
        "  - subject: 演示漂移乙\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    first = record_payload(record(root, presentation, reply=reply))
    assert first["settled"] == 1 and first["parked"] == 1, first

    second_scan = scan_payload(root)
    subjects = [item["identity"]["subject"] for item in second_scan["items"]]
    assert subjects == ["演示漂移乙"], subjects
    exclusions = second_scan["bookkeeping"]["named_exclusions"]
    assert any(entry["reason"] == "already-resolved"
               and entry.get("via") in ("resolution-field", "prior-batch")
               and entry.get("subject") == "演示漂移甲"
               for entry in exclusions), exclusions

    second_presentation = write_presentation(root, tmp_path / "scan2.json")
    second_reply = write_reply(tmp_path / "reply2.md", NO_OBJECTIONS_REPLY)
    second = record_payload(record(root, second_presentation, reply=second_reply))
    assert second["batch_id"] != first["batch_id"]
    assert second["record_path"] != first["record_path"]
    assert [decision["subject"] for decision in second["decisions"]] == ["演示漂移乙"]
    second_text = (root / second["record_path"]).read_text(encoding="utf-8")
    assert "演示漂移甲" not in second_text, "a settled identity was re-recorded in batch two"


def test_record_drift_refused_zero_write(tmp_path: Path) -> None:
    """C-501: a source change between scan and record refuses with zero writes and no id."""
    root = copy_fixture("drift", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    source = root / ".specify" / "specs" / "demo" / "two.md"
    before_source = source.read_bytes()
    register_before = (root / ".specify" / "register.md").read_bytes()
    with source.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n### PENDING — 演示漂移新增项\n\n"
            "- **decision_class**: human-interactive\n"
            "- **subject**: 演示漂移新增项\n"
            "- **context**: 扫描之后新增的候选。\n"
            "- **options**: 1\n"
            "  - label: 唯一方案\n"
            "    consequences: 保持现状\n"
            "    reversibility: reversible\n"
            "    default: yes\n"
            "    evidence: .specify/specs/demo/ref.md\n"
            "  forced: 只有一种可行做法\n"
            "- **basis**: 无\n"
            "- **origin**: demo-producer\n"
            "- **created_at**: 2026-11-20T00:00:00Z\n")
    refused = record(root, presentation, reply=reply)
    assert refused.returncode == 1, refused.stdout
    combined = (refused.stdout + refused.stderr).lower()
    assert "drift" in combined or "changed" in combined, combined
    assert knowledge_files(root) == [], "a refused record left a batch record behind"
    assert source.read_bytes() != before_source  # our own mutation, not the engine's
    assert (root / ".specify" / "register.md").read_bytes() == register_before


def test_batch_id_shape_and_duplicate_refusal(tmp_path: Path) -> None:
    """C-502: the minted id carries the closed shape; a same-id second write is refused."""
    root = copy_fixture("batch-family", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    first = record_payload(record(root, presentation, reply=reply))
    batch_id = first["batch_id"]
    assert re.match(r"^B-\d{8}T\d{6}Z-[0-9a-f]{8}$", batch_id), batch_id
    record_path = root / first["record_path"]
    assert record_path.is_file()
    record_text = record_path.read_text(encoding="utf-8")
    assert frontmatter(record_text).get("title") == f"decision-batch-{batch_id}"
    before = record_path.read_bytes()
    assert len(knowledge_files(root)) == 1

    duplicate = record(root, presentation, reply=reply)
    assert duplicate.returncode == 1, (
        f"a same-id second record exited {duplicate.returncode}, expected 1: {duplicate.stdout}"
    )
    assert batch_id in (duplicate.stdout + duplicate.stderr)
    assert record_path.read_bytes() == before, "a duplicate record rewrote the existing batch record"
    assert len(knowledge_files(root)) == 1


def test_batch_record_layout_via_memory_engine(tmp_path: Path) -> None:
    """C-503: one dated knowledge entry with the batch head, item rows and decision records."""
    root = copy_fixture("batch-family", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  把「演示家庭项乙」改为「方案甲」。\n"
        "objections:\n"
        "  - subject: 演示家庭项乙\n"
        "    action: alternative\n"
        "    option_label: 方案甲\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    batch_id = payload["batch_id"]

    head = frontmatter(text)
    assert head.get("scope") == "knowledge", head
    assert head.get("source") == "/speckit.decide", head
    assert head.get("title") == f"decision-batch-{batch_id}", head
    for key in ("id", "tags", "created", "session_id", "summary"):
        assert key in head, f"memory-engine frontmatter lacks {key!r}: {head}"
    for needle in (f"# 决策批次记录 {batch_id}", "## 批次头", f"- batch_id: {batch_id}",
                   "- 扫描时点:", "- 工具版本:", "- 来源与候选计数", "- 完备性",
                   "- 授权: interactive", "> 把「演示家庭项乙」改为「方案甲」。",
                   "## 逐项行表", "## 决策记录", "## 收尾"):
        assert needle in text, f"batch record lacks {needle!r}"
    header = "| 主体 | 来源 | 资格 | 接地 | 建议默认 | 处置 | 决策 |"
    assert header in text, "the item-row table header is missing"
    assert "| 演示家庭项甲 |" in text and "| 演示家庭项乙 |" in text
    assert "### D-001 — 演示家庭项甲" in text
    assert "### D-002 — 演示家庭项乙" in text


def test_decision_record_batch_family(tmp_path: Path) -> None:
    """C-504: settled records carry the three batch-family fields together, values in domain."""
    root = copy_fixture("batch-family", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  把「演示家庭项乙」改为「方案甲」。\n"
        "objections:\n"
        "  - subject: 演示家庭项乙\n"
        "    action: alternative\n"
        "    option_label: 方案甲\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    blocks = decision_blocks(text)
    assert len(blocks) == 2, blocks
    record_path = payload["record_path"]

    assert text.count("- **batch_id**:") == 2
    assert text.count("- **batch_disposition**:") == 2
    assert text.count("- **recommendation_grounding**:") == 2
    for block in blocks:
        for field in ("batch_id", "batch_disposition", "recommendation_grounding"):
            assert f"- **{field}**: " in block, (field, block)
        grounding = next(line for line in block.splitlines()
                         if line.startswith("- **recommendation_grounding**:"))
        assert grounding.split(":", 1)[1].strip() in ("grounded", "no-evidence")
        assert "- **evidence**: " in block and record_path in block
        assert ".specify/specs/demo/household.md" in block
        assert "- **actor**: user" in block
        assert "- **transmission_status**: not-transmitted" in block

    first = next(block for block in blocks if "演示家庭项甲" in block)
    second = next(block for block in blocks if "演示家庭项乙" in block)
    assert "- **batch_disposition**: accepted-default" in first
    assert "- **chosen_option**: 方案甲" in first
    assert "未对本项提出异议" in first
    assert "- **batch_disposition**: objected-alternative" in second
    assert "- **chosen_option**: 方案甲" in second
    assert "改选" in second

# =====================================================================================
# US3 — register registration, source updates and replay (T033 red-first; green
# claimed at T039). The register/status/resolution write-back and the replay action
# are unimplemented until T036/T037, so every test below fails on its own missing
# behaviour, never on an import error.
# =====================================================================================

def register_file(root: Path) -> Path:
    return root / ".specify" / "register.md"


def register_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def register_row(text: str, row_id: str) -> str | None:
    matches = [line for line in text.splitlines()
               if line.strip().startswith("|")
               and register_cells(line)
               and register_cells(line)[0].replace("*", "").replace("`", "") == row_id]
    assert len(matches) <= 1, f"more than one register row names {row_id!r}: {matches}"
    return matches[0] if matches else None


def replay(root: Path, batch: Path, fmt: str = "json") -> subprocess.CompletedProcess:
    return run_engine("replay", "--workspace-root", str(root), "--batch", str(batch),
                      "--format", fmt)


REGISTER_HEADER_CELLS = ["编号", "含义(一行)", "权威路径(完整陈述)", "状态"]


def test_register_registration_and_status_update(tmp_path: Path) -> None:
    """C-505: settled row gains the batch and decision id, parked row stays open, rows append."""
    root = copy_fixture("register-updates", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    before = register_file(root).read_text(encoding="utf-8")
    before_rows = [line for line in before.splitlines() if line.strip().startswith("|")]
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  先暂缓「演示登记暂缓项」，其余按建议。\n"
        "objections:\n"
        "  - subject: 演示登记暂缓项\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    batch_id = payload["batch_id"]
    record_path = payload["record_path"]
    after = register_file(root).read_text(encoding="utf-8")

    settled = register_row(after, "OI-801")
    assert settled is not None, "the settled register row was deleted"
    settled_cells = register_cells(settled)
    assert batch_id in settled_cells[3] and "D-001" in settled_cells[3], settled_cells
    before_cells = register_cells(register_row(before, "OI-801"))
    assert settled_cells[:3] == before_cells[:3], "cells other than the status were rewritten"

    parked = register_row(after, "OI-802")
    assert parked is not None, "the parked register row was deleted"
    parked_status = register_cells(parked)[3]
    assert parked_status.startswith("open"), parked_status
    assert batch_id in parked_status, parked_status

    assert register_row(after, "OI-899") == register_row(before, "OI-899"), (
        "a resolved historical register row was rewritten")

    after_rows = [line for line in after.splitlines() if line.strip().startswith("|")]
    assert len(after_rows) == len(before_rows) + 2, (
        "the register must gain exactly the batch row and the decision range row")
    appended = [line for line in after_rows if record_path in line]
    assert len(appended) == 2, f"expected the batch row and the decision range row: {appended}"
    assert any(batch_id in line for line in appended), appended
    decision_rows = [line for line in appended if "D-001" in line]
    assert len(decision_rows) == 1, appended
    assert payload["decisions"] == [
        {"subject": "演示登记结案项", "disposition": "accepted-default", "decision_id": "D-001"}
    ], payload["decisions"]


def test_resolution_annotation_and_disclosure(tmp_path: Path) -> None:
    """C-506: settlement appends the block resolution; a write failure is disclosed."""
    root = copy_fixture("register-updates", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    carrier = root / ".specify" / "specs" / "demo" / "ledger.md"
    original = carrier.read_text(encoding="utf-8")
    reply = write_reply(tmp_path / "reply.md", (
        "reply_verbatim: |\n  先暂缓「演示登记暂缓项」，其余按建议。\n"
        "objections:\n"
        "  - subject: 演示登记暂缓项\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    payload = record_payload(record(root, presentation, reply=reply))
    batch_id = payload["batch_id"]
    after = carrier.read_text(encoding="utf-8")

    needle = f"- **resolution**: {batch_id} -> D-001"
    assert after.count("- **resolution**:") == 1, (
        "the settled block must gain exactly one resolution field")
    assert needle in after, after[-400:]
    restored = after.replace(needle + "\n", "", 1)
    assert restored == original, "the block content changed beyond the appended resolution"

    second = scan_payload(root)
    assert "演示登记结案项" not in {item["identity"]["subject"] for item in second["items"]}
    exclusions = second["bookkeeping"]["named_exclusions"]
    assert any(entry["reason"] == "already-resolved"
               and entry.get("via") == "resolution-field"
               and entry.get("subject") == "演示登记结案项"
               for entry in exclusions), exclusions

    read_only_root = copy_fixture("register-updates", tmp_path / "read-only")
    read_only_scan = write_presentation(read_only_root, tmp_path / "read-only-scan.json")
    read_only_carrier = read_only_root / ".specify" / "specs" / "demo" / "ledger.md"
    os.chmod(read_only_carrier, 0o444)
    try:
        proc = record(read_only_root, read_only_scan, reply=write_reply(
            tmp_path / "read-only-reply.md", NO_OBJECTIONS_REPLY))
    finally:
        os.chmod(read_only_carrier, 0o644)
    assert proc.returncode == 0, (
        f"a settled batch with an unwritable source carrier exited {proc.returncode}: "
        f"{proc.stdout} {proc.stderr}")
    disclosed = json.loads(proc.stdout)
    assert disclosed.get("disclosures"), "the source update failure was not disclosed"
    assert any(".specify/specs/demo/ledger.md" in json.dumps(entry)
               for entry in disclosed["disclosures"]), disclosed["disclosures"]
    assert "- **resolution**:" not in read_only_carrier.read_text(encoding="utf-8")
    again = scan_payload(read_only_root)
    assert "演示登记结案项" not in {item["identity"]["subject"] for item in again["items"]}
    assert any(entry["reason"] == "already-resolved" and entry.get("via") == "prior-batch"
               and entry.get("subject") == "演示登记结案项"
               for entry in again["bookkeeping"]["named_exclusions"]), (
        "the prior-batch read-time join did not prevent re-presentation")


def test_absent_register_created_from_header(tmp_path: Path) -> None:
    """C-505: an absent register is created from the existing header form before registration."""
    root = copy_fixture("register-absent", tmp_path)
    assert not register_file(root).exists()
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    payload = record_payload(record(root, presentation, reply=reply))
    assert register_file(root).is_file(), "the absent register was not created"
    text = register_file(root).read_text(encoding="utf-8")
    header = register_row(text, "编号")
    assert header is not None, f"the created register lacks the four-column header: {text[:300]}"
    assert register_cells(header) == REGISTER_HEADER_CELLS, register_cells(header)
    assert payload["batch_id"] in text
    assert "D-001" in text


def test_two_batches_distinct_paths(tmp_path: Path) -> None:
    """C-507: distinct batches write distinct paths, stay mutually read-only, reuse no record."""
    root = copy_fixture("concurrency", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan1.json")
    reply = write_reply(tmp_path / "reply1.md", (
        "reply_verbatim: |\n  「演示并发乙」先放着，其余按建议。\n"
        "objections:\n"
        "  - subject: 演示并发乙\n"
        "    action: park\n"
        "no_objections: false\n"
    ))
    first = record_payload(record(root, presentation, reply=reply))
    first_path = root / first["record_path"]
    first_bytes = first_path.read_bytes()

    second_scan = scan_payload(root)
    assert [item["identity"]["subject"] for item in second_scan["items"]] == ["演示并发乙"]
    assert any(entry["reason"] == "already-resolved"
               and entry.get("subject") == "演示并发甲"
               for entry in second_scan["bookkeeping"]["named_exclusions"])

    second_presentation = write_presentation(root, tmp_path / "scan2.json")
    second_reply = write_reply(tmp_path / "reply2.md", NO_OBJECTIONS_REPLY)
    second = record_payload(record(root, second_presentation, reply=second_reply))

    assert second["batch_id"] != first["batch_id"]
    assert second["record_path"] != first["record_path"]
    assert len(knowledge_files(root)) == 2, knowledge_files(root)
    assert first_path.read_bytes() == first_bytes, (
        "a later batch wrote into another batch's record")
    second_text = (root / second["record_path"]).read_text(encoding="utf-8")
    assert "演示并发甲" not in second_text, "a settled identity was re-recorded in batch two"

    replayed = replay(root, first_path)
    assert replayed.returncode == 0, (
        f"replaying the first batch after the second exited {replayed.returncode}: "
        f"{replayed.stdout[-600:]} {replayed.stderr[-600:]}")
    assert json.loads(replayed.stdout)["batch_id"] == first["batch_id"]


def test_replay_from_record_only(tmp_path: Path) -> None:
    """C-508: replay rebuilds the batch from the record alone, read-only and deterministic."""
    root = copy_fixture("replay-broken", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    payload = record_payload(record(root, presentation, reply=reply))
    record_file = root / payload["record_path"]
    presentation.unlink()
    reply.unlink()
    source = root / ".specify" / "specs" / "demo" / "replay.md"
    with source.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n### PENDING — 演示重放新增项\n\n"
            "- **decision_class**: human-interactive\n"
            "- **subject**: 演示重放新增项\n"
            "- **context**: 记录之后新增的来源，不得出现在重放结果里。\n"
            "- **options**: 1\n"
            "  - label: 唯一方案\n"
            "    consequences: 保持现状\n"
            "    reversibility: reversible\n"
            "    default: yes\n"
            "    evidence: .specify/specs/demo/ref.md\n"
            "  forced: 只有一种可行做法\n"
            "- **basis**: 无\n"
            "- **origin**: demo-producer\n"
            "- **created_at**: 2026-11-20T00:00:00Z\n")
    before = snapshot(root)
    proc = replay(root, record_file)
    assert proc.returncode == 0, f"replay exited {proc.returncode}: {proc.stderr[-600:]}"
    out = json.loads(proc.stdout)
    assert out["action"] == "replay" and out["result"] == "replayed"
    assert out["batch_id"] == payload["batch_id"]
    assert [item["subject"] for item in out["items"]] == ["演示重放项"], (
        "replay re-scanned live sources instead of reconstructing the recorded item set")
    assert out["reply_verbatim"] == "没有异议，按建议默认值处理。"
    assert out["completeness"]["verdict"] == "complete"
    assert out["completeness"]["candidates"] == out["completeness"]["presented_rows"]
    assert [{
        "decision_id": item["decision_id"],
        "subject": item["subject"],
        "chosen_option": item["chosen_option"],
        "batch_disposition": item["batch_disposition"],
        "recommendation_grounding": item["recommendation_grounding"],
    } for item in out["decisions"]] == [{
        "decision_id": "D-001",
        "subject": "演示重放项",
        "chosen_option": "方案甲",
        "batch_disposition": "accepted-default",
        "recommendation_grounding": "no-evidence",
    }], out["decisions"]
    assert out["items"][0]["disposition"] == "accepted-default"
    assert out["items"][0]["decision_id"] == "D-001"
    assert out["pointers"] and all(pointer["resolved"] for pointer in out["pointers"])
    assert snapshot(root) == before, "replay wrote into the workspace"
    again = replay(root, record_file)
    assert again.returncode == 0
    assert again.stdout == proc.stdout, "two replays of one record are not byte-identical"


def test_replay_broken_pointer_nonzero(tmp_path: Path) -> None:
    """C-508: an unresolvable pointer is named and the replay exits non-zero."""
    root = copy_fixture("replay-broken", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    payload = record_payload(record(root, presentation, reply=reply))
    record_file = root / payload["record_path"]
    text = record_file.read_text(encoding="utf-8")
    assert ".specify/specs/demo/ref.md" in text
    broken_pointer = ".specify/specs/demo/missing-ref.md"
    record_file.write_text(text.replace(".specify/specs/demo/ref.md", broken_pointer),
                           encoding="utf-8")
    proc = replay(root, record_file)
    assert proc.returncode == 1, (
        f"replay over a broken pointer exited {proc.returncode}, expected 1")
    combined = proc.stdout + proc.stderr
    assert broken_pointer in combined, f"the broken pointer is not named: {combined[-600:]}"

# =====================================================================================
# US4 — completeness is honest: bookkeeping, refusal, explicit emptiness (T040 red-first;
# green claimed at T045) and the regression guards authored after their subjects (T042).
# The structured closed-set claim, the partition and the named absent-source list land
# with T043, so every red-first test below fails on its own missing behaviour.
# =====================================================================================

US4_FIXTURES = ("two-source", "incomplete-block", "autonomous", "absent-root")


def test_completeness_claim_shape(tmp_path: Path) -> None:
    """C-601: completeness is a closed-set claim with the owner's elements."""
    payload = scan_payload(copy_fixture("two-source", tmp_path))
    books = payload["bookkeeping"]
    claim = books.get("completeness_claim")
    assert claim, "bookkeeping lacks the structured closed-set completeness claim"
    assert claim["referent"] == "this-scan", claim
    assert claim["comparison_unit"] == "per-candidate-classification", claim
    assert claim["allowed_delta"] == [], "the allowed delta must be unconditionally empty"
    assert "closed-set-claims.md" in claim["elements_owner"], claim
    assert claim["verdict"] == "complete", claim
    partition = claim["partition"]
    assert set(partition) == {"presented_rows", "duplicate_merged", "not_human_held",
                              "already_resolved"}, partition
    assert (partition["presented_rows"] + partition["duplicate_merged"]
            + partition["not_human_held"] + partition["already_resolved"]) == books["candidates"], (
        "the partition does not sum to the candidate count")


def test_bookkeeping_identity_holds(tmp_path: Path) -> None:
    """C-602: the identity holds on every fixture and is carried into the batch-record head."""
    for name in US4_FIXTURES:
        payload = scan_payload(copy_fixture(name, tmp_path))
        books = payload["bookkeeping"]
        assert books["candidates"] == (books["presented_rows"] + books["duplicate_merged"]
                                       + len(books["named_exclusions"])), name
        assert sum(source["candidates"] for source in books["sources"]) == books["candidates"], name
        claim = books["completeness_claim"]
        partition = claim["partition"]
        assert partition["presented_rows"] == books["presented_rows"], name
        assert partition["duplicate_merged"] == books["duplicate_merged"], name
        assert (partition["not_human_held"] + partition["already_resolved"]
                == len(books["named_exclusions"])), name
        assert (partition["presented_rows"] + partition["duplicate_merged"]
                + partition["not_human_held"] + partition["already_resolved"]
                == books["candidates"]), name

    root = copy_fixture("batch-family", tmp_path / "record")
    presentation = write_presentation(root, tmp_path / "record-scan.json")
    books = json.loads(presentation.read_text(encoding="utf-8"))["bookkeeping"]
    payload = record_payload(record(root, presentation, reply=write_reply(
        tmp_path / "record-reply.md", NO_OBJECTIONS_REPLY)))
    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    identity = next(line for line in text.splitlines() if line.startswith("- 完备性:"))
    assert f"candidates={books['candidates']}" in identity, identity
    assert f"presented_rows={books['presented_rows']}" in identity, identity
    assert f"duplicate_merged={books['duplicate_merged']}" in identity, identity
    assert f"named_exclusions={len(books['named_exclusions'])}" in identity, identity
    assert "verdict=complete" in identity, identity
    assert "- 完备性声明:" in text, "the batch head carries no completeness claim"
    assert "referent=this-scan" in text and "comparison_unit=per-candidate-classification" in text
    assert "allowed_delta=空" in text
    assert "closed-set-claims.md" in text
    assert "- 分区:" in text and "not_human_held=" in text and "already_resolved=" in text
    assert "- 缺席来源:" in text


def test_absent_source_named_not_clean(tmp_path: Path) -> None:
    """C-604: an absent carrier is a named empty source, never a clean full scan."""
    root = copy_fixture("absent-root", tmp_path)
    payload = scan_payload(root)
    assert payload["result"] == "presentation"
    authored = next(source for source in payload["bookkeeping"]["sources"]
                    if source["source_id"] == "authored-pending-item")
    assert authored["presence"] == "read", authored
    assert sorted(authored["absent_roots"]) == [".specify/anchoring", ".specify/goals",
                                                ".specify/teams"], authored
    claim = payload["bookkeeping"]["completeness_claim"]
    for absent_root in authored["absent_roots"]:
        assert absent_root in claim["absent_sources"], claim["absent_sources"]
    assert claim["verdict"] == "complete"
    assert "缺席" in payload["batch_context"]["completeness_disclosure"]

    empty = scan_payload(copy_fixture("empty-project", tmp_path / "empty-project"))
    assert empty["result"] == "nothing-pending"
    named = empty["bookkeeping"]["completeness_claim"]["absent_sources"]
    assert ".specify/register.md" in named, named
    for rel_root in (".specify/specs", ".specify/goals", ".specify/anchoring", ".specify/teams"):
        assert rel_root in named, named


def test_nothing_pending_success_no_record(tmp_path: Path) -> None:
    """C-605: zero candidates is an explicit success with no batch record."""
    root = copy_fixture("empty-project", tmp_path)
    proc = scan(root, "json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["result"] == "nothing-pending", payload["result"]
    claim = payload["bookkeeping"]["completeness_claim"]
    assert claim["candidates"] == 0 and claim["verdict"] == "complete", claim
    assert not (root / ".specify" / "knowledge").exists(), (
        "nothing-pending created a knowledge store")
    text, _ = scan_text(root)
    assert "没有待决策项" in text

    presentation = tmp_path / "empty-scan.json"
    presentation.write_text(proc.stdout, encoding="utf-8")
    reply = write_reply(tmp_path / "reply.md", NO_OBJECTIONS_REPLY)
    refused = record(root, presentation, reply=reply)
    assert refused.returncode == 1, (
        f"record over a nothing-pending result exited {refused.returncode}, expected 1")
    assert not (root / ".specify" / "knowledge").exists()


def lock_a_scan_root_candidate(root: Path) -> Path:
    locked = root / ".specify" / "specs" / "demo" / "locked"
    locked.mkdir()
    (locked / "hidden.md").write_text(
        "# 演示不可枚举\n\n### PENDING — 演示不可枚举项\n\n"
        "- **decision_class**: human-interactive\n"
        "- **subject**: 演示不可枚举项\n"
        "- **context**: 所在目录不可读，候选无法被枚举。\n"
        "- **options**: 1\n"
        "  - label: 唯一方案\n"
        "    consequences: 保持现状\n"
        "    reversibility: reversible\n"
        "    default: yes\n"
        "    evidence: .specify/specs/demo/ref.md\n"
        "  forced: 只有一种可行做法\n"
        "- **basis**: 无\n"
        "- **origin**: demo-producer\n"
        "- **created_at**: 2026-11-20T00:00:00Z\n",
        encoding="utf-8")
    return locked


def test_unclassifiable_candidate_refused(tmp_path: Path) -> None:
    """C-606: a candidate that cannot be enumerated refuses the batch, never drops silently."""
    root = copy_fixture("two-source", tmp_path)
    locked = lock_a_scan_root_candidate(root)
    before = snapshot(root)
    os.chmod(locked, 0o000)
    try:
        proc = scan(root, "json")
    finally:
        os.chmod(locked, 0o755)
    assert proc.returncode == 1, (
        "a scan that could not enumerate every candidate exited "
        f"{proc.returncode}, expected 1: {proc.stdout[-600:]}")
    payload = json.loads(proc.stdout)
    assert payload["result"] == "refused", payload
    assert any(refusal["source_id"] == "authored-pending-item"
               for refusal in payload["refusals"]), payload["refusals"]
    assert "items" not in payload and "completeness_claim" not in payload
    assert snapshot(root) == before, "a refused scan wrote into the workspace"


def test_no_partial_complete_claim(tmp_path: Path) -> None:
    """C-607: a batch that missed a candidate never claims completeness or presents a part."""
    root = copy_fixture("two-source", tmp_path)
    locked = lock_a_scan_root_candidate(root)
    os.chmod(locked, 0o000)
    try:
        proc = scan(root, "json")
    finally:
        os.chmod(locked, 0o755)
    assert proc.returncode == 1, (
        f"a partial scan exited {proc.returncode}, expected 1: {proc.stdout[-600:]}")
    payload = json.loads(proc.stdout)
    assert payload["result"] == "refused", payload
    assert "items" not in payload, "a refused batch presented a partial item set"
    assert "completeness_claim" not in payload
    assert '"verdict": "complete"' not in proc.stdout
    assert "演示数据保留期" not in proc.stdout, (
        "a readable candidate was presented inside a refused partial batch")
    assert not (root / ".specify" / "knowledge").exists()

# -------------------------------------------------------------------------------------
# T042 — regression-exception guards: their subjects predate the guards (scan refusal
# landed with T019, the batch-record head with T030), so these samples are not red-first
# by construction; they pin the landed behaviour and go red when it is doctored.
# -------------------------------------------------------------------------------------

def test_unreadable_source_refusal(tmp_path: Path) -> None:
    """C-603 guard: a carrier-level unreadable register refuses the whole batch."""
    root = copy_fixture("unreadable-register", tmp_path)
    before = snapshot(root)
    proc = scan(root, "json")
    assert proc.returncode == 1, proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["result"] == "refused", payload
    refusal = payload["refusals"][0]
    assert refusal["source_id"] == "register-open-decision-row", refusal
    assert "register.md" in refusal["detail"], refusal
    assert "演示登记表不可读项" not in proc.stdout, "a partial batch was presented"
    assert snapshot(root) == before, "a refused scan wrote into the workspace"


def test_batch_record_head_completeness(tmp_path: Path) -> None:
    """C-602 guard: the batch-record head carries the per-source counts, identity and verdict."""
    root = copy_fixture("batch-family", tmp_path)
    presentation = write_presentation(root, tmp_path / "scan.json")
    books = json.loads(presentation.read_text(encoding="utf-8"))["bookkeeping"]
    payload = record_payload(record(root, presentation, reply=write_reply(
        tmp_path / "reply.md", NO_OBJECTIONS_REPLY)))
    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    identity = next(line for line in text.splitlines() if line.startswith("- 完备性:"))
    assert f"candidates={books['candidates']}" in identity, identity
    assert f"presented_rows={books['presented_rows']}" in identity, identity
    assert f"duplicate_merged={books['duplicate_merged']}" in identity, identity
    assert f"named_exclusions={len(books['named_exclusions'])}" in identity, identity
    assert "verdict=complete" in identity, identity
    for source in books["sources"]:
        assert any(line.strip().startswith(f"- {source['source_id']}: presence={source['presence']};")
                   and f"candidates={source['candidates']}" in line
                   for line in text.splitlines()), (source, "missing per-source count line")

# =====================================================================================
# US5 — a redecision supersedes the prior record, never overwrites it, and refuses
# rather than degrades when the prior carrier cannot take the append (T046 red-first;
# green claimed at T052). The `superseded_by` face lands with T050, so both tests below
# fail on their own missing behaviour, never on an import error.
# =====================================================================================

def supersession_reply(subject: str, label: str) -> str:
    return (
        "reply_verbatim: |\n"
        f"  改回「{label}」。\n"
        "objections:\n"
        f"  - subject: {subject}\n"
        "    action: alternative\n"
        f"    option_label: {label}\n"
        "no_objections: false\n"
    )


def test_supersession_append_only(tmp_path: Path) -> None:
    """C-510: a redecision adds a new record and appends `superseded_by` to the prior
    record, keeping every pre-existing byte of the prior carrier identical."""
    root = copy_fixture("prior-conflict", tmp_path)
    prior_carrier = root / ".specify" / "specs" / "demo" / "history-records.md"
    prior_before = prior_carrier.read_bytes()
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md",
                        supersession_reply("演示前例冲突项", "保留 30 天"))
    payload = record_payload(record(root, presentation, reply=reply))

    text = (root / payload["record_path"]).read_text(encoding="utf-8")
    assert "- **chosen_option**: 保留 30 天" in text, (
        "the new record does not carry the redecision")
    assert payload["decisions"] == [
        {"subject": "演示前例冲突项", "disposition": "objected-alternative",
         "decision_id": "D-001"}
    ], payload["decisions"]

    lines_before = prior_before.decode("utf-8").splitlines()
    lines_after = prior_carrier.read_text(encoding="utf-8").splitlines()
    appended = [line for line in lines_after if "- **superseded_by**:" in line]
    assert len(appended) == 1, (
        "expected exactly one appended superseded_by line, got: "
        f"{lines_after[-4:]}")
    stripped = [line for line in lines_after if "- **superseded_by**:" not in line]
    assert stripped == lines_before, (
        "the append changed bytes other than the single superseded_by line")
    assert "D-001" in appended[0] and payload["record_path"] in appended[0], appended[0]
    old_text = prior_carrier.read_text(encoding="utf-8")
    assert "### D-010 — 演示前例冲突项" in old_text
    assert "- **chosen_option**: 保留 90 天" in old_text, (
        "the prior record's chosen option was rewritten")
    assert "上一轮讨论" in old_text, "the prior record's context was rewritten"


def test_supersession_unwritable_prior_refused(tmp_path: Path) -> None:
    """C-510: an unwritable prior carrier refuses the redecision with zero writes — it is
    never degraded to a fresh decision (an unreadable carrier already refuses at scan)."""
    root = copy_fixture("unwritable-old-record", tmp_path)
    prior_carrier = root / ".specify" / "specs" / "demo" / "old-record.md"
    item_carrier = root / ".specify" / "specs" / "demo" / "item.md"
    presentation = write_presentation(root, tmp_path / "scan.json")
    reply = write_reply(tmp_path / "reply.md",
                        supersession_reply("演示不可写前例项", "保留 30 天"))
    prior_before = prior_carrier.read_bytes()
    item_before = item_carrier.read_bytes()
    register_before = (root / ".specify" / "register.md").read_bytes()
    assert os.access(prior_carrier, os.W_OK), "the fixture carrier is already read-only"
    os.chmod(prior_carrier, 0o444)
    try:
        refused = record(root, presentation, reply=reply)
    finally:
        os.chmod(prior_carrier, 0o644)
    assert refused.returncode == 1, (
        f"an unwritable prior carrier exited {refused.returncode}, expected 1: "
        f"{refused.stdout} {refused.stderr}")
    combined = refused.stdout + refused.stderr
    assert "old-record.md" in combined, (
        f"the refusal does not name the prior carrier: {combined}")
    assert "演示不可写前例项" in combined, combined
    assert knowledge_files(root) == [], "a refused redecision left a batch record behind"
    assert prior_carrier.read_bytes() == prior_before
    assert item_carrier.read_bytes() == item_before
    assert (root / ".specify" / "register.md").read_bytes() == register_before
