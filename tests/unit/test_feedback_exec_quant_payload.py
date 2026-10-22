"""Unit tests for the exec-quant payload collection (Feature 068, US1).

Covers the package-leg sweep semantics owned by
``.specify/specs/068-exec-quant-feedback-channel/contracts/package-layout.md``
C-1 (read-only sweep, dual form, kind filter, skipped_unreadable, legacy
naming, source_form_counts) and C-2 (deterministic sort, caps + truncation),
plus the package-level identity (C-5 / research D3) and the implement-time
minimal rules for analyze findings U-01/U-02/U-03:

* U-01 (CHK005): truncation granularity is the whole record; a single record
  larger than the byte cap is itself truncated (never split).
* U-02 (CHK006): a record missing ``collected_at`` sorts as the empty string
  (first, ascending), deterministically.
* U-03 (CHK007): every probed item lands in exactly one of the three buckets
  ``record_count`` / ``skipped_unreadable`` / ``truncated_count``, so the E4
  identity ``skipped + truncated + record_count == probed total`` holds by
  construction with no fourth field.

Fixtures are all self-constructed (tasks.md § Environment Prerequisites: the
sample client store is a read-only reference, never touched by tests).

Red-first evidence: notes/red-first-evidence.md (§ T004).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils as fu

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)
PAYLOAD_KIND = "speckit.exec-quant-payload"  # data-model § E4

HEX40 = "1234567890abcdef1234567890abcdef12345678"


# --------------------------------------------------------------------------- #
# fixture helpers (self-constructed stores)
# --------------------------------------------------------------------------- #
def _eq_store(workspace: Path) -> Path:
    return workspace / ".specify" / "memory" / "exec-quant"


def _write_record(store: Path, name: str, record: dict, pad: int = 0) -> bytes:
    if pad:
        record = dict(record, pad="x" * pad)
    raw = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    rdir = store / "records"
    rdir.mkdir(parents=True, exist_ok=True)
    (rdir / name).write_bytes(raw)
    return raw


def _make_record(collected_at: str, kind: str = STR001, unit: str = "/speckit.plan") -> dict:
    return {"kind": kind, "schema_version": 2, "unit_id": unit,
            "unit_type": "command", "run_id": "r1", "collected_at": collected_at}


def _write_legacy(store: Path, lines: list) -> None:
    text = "".join(line + "\n" for line in lines)
    store.mkdir(parents=True, exist_ok=True)
    (store / "records.jsonl").write_text(text, encoding="utf-8")


def _snapshot(store: Path) -> dict:
    return {str(p.relative_to(store)): p.read_bytes()
            for p in sorted(store.rglob("*")) if p.is_file()}


# --------------------------------------------------------------------------- #
# C-1: dual-form sweep, full inclusion
# --------------------------------------------------------------------------- #
def test_collect_dual_form_full_inclusion(tmp_path):
    store = _eq_store(tmp_path)
    _write_record(store, "2026-a.json", _make_record("2026-01-01T00:00:00Z"))
    _write_record(store, "2026-b.json", _make_record("2026-01-02T00:00:00Z"))
    _write_legacy(store, [json.dumps(_make_record("2026-01-03T00:00:00Z")),
                          json.dumps(_make_record("2026-01-04T00:00:00Z"))])

    payload = fu._collect_exec_quant_payload(tmp_path)

    names = [r["name"] for r in payload["records"]]
    assert payload["record_count"] == 4  # 2 records-dir + 2 legacy, all in
    assert "2026-a.json" in names and "2026-b.json" in names
    assert "legacy-records-L0001.json" in names
    assert "legacy-records-L0002.json" in names


def test_collect_kind_filter_and_unreadable_skipped(tmp_path):
    store = _eq_store(tmp_path)
    _write_record(store, "good.json", _make_record("2026-01-01T00:00:00Z"))
    _write_record(store, "wrong-kind.json", _make_record("2026-01-02T00:00:00Z",
                                                         kind="some.other.kind"))
    (store / "records").mkdir(parents=True, exist_ok=True)
    (store / "records" / "broken.json").write_bytes(b"{not json")
    (store / "records" / "not-object.json").write_bytes(b'"just a string"')
    _write_legacy(store, [json.dumps(_make_record("2026-01-03T00:00:00Z")),
                          ""][:1])  # one good legacy line

    payload = fu._collect_exec_quant_payload(tmp_path)

    assert payload["record_count"] == 2
    assert payload["skipped_unreadable"] == 3  # wrong-kind + broken + non-object


def test_legacy_entry_names_line_numbers_from_one(tmp_path):
    store = _eq_store(tmp_path)
    _write_legacy(store, [json.dumps(_make_record("2026-01-01T00:00:00Z")),
                          "",  # blank line: not an entry, physical numbering kept
                          json.dumps(_make_record("2026-01-02T00:00:00Z"))])

    payload = fu._collect_exec_quant_payload(tmp_path)

    names = [r["name"] for r in payload["records"]]
    assert names == ["legacy-records-L0001.json", "legacy-records-L0003.json"]
    assert payload["skipped_unreadable"] == 0  # blank line is not a record


def test_source_form_counts_dual_counting(tmp_path):
    store = _eq_store(tmp_path)
    _write_record(store, "a.json", _make_record("2026-01-01T00:00:00Z"))
    _write_legacy(store, [json.dumps(_make_record("2026-01-02T00:00:00Z")),
                          json.dumps(_make_record("2026-01-03T00:00:00Z"))])

    payload = fu._collect_exec_quant_payload(tmp_path)

    assert payload["source_form_counts"] == {"records-dir": 1, "legacy-jsonl": 2}
    assert sum(payload["source_form_counts"].values()) == payload["record_count"]


# --------------------------------------------------------------------------- #
# C-2: deterministic sort + caps
# --------------------------------------------------------------------------- #
def test_sort_collected_at_then_source_name_deterministic(tmp_path):
    store = _eq_store(tmp_path)
    _write_record(store, "z-late.json", _make_record("2026-01-03T00:00:00Z"))
    _write_record(store, "m-early.json", _make_record("2026-01-01T00:00:00Z"))
    _write_record(store, "a-early.json", _make_record("2026-01-01T00:00:00Z"))
    _write_legacy(store, [json.dumps(_make_record("2026-01-02T00:00:00Z"))])

    first = fu._collect_exec_quant_payload(tmp_path)
    second = fu._collect_exec_quant_payload(tmp_path)

    order = [r["name"] for r in first["records"]]
    assert order == ["a-early.json", "m-early.json",
                     "legacy-records-L0001.json", "z-late.json"]
    assert [r["name"] for r in second["records"]] == order  # cross-call stable
    assert first["collected_at_range"] == ["2026-01-01T00:00:00Z",
                                           "2026-01-03T00:00:00Z"]


def test_cap_constants_pinned_values():
    # C-2 is the single normative source of the cap values; this literal pin
    # exists to detect drift (One Source Of Truth: test-pinned duplicate).
    assert fu.MAX_PAYLOAD_RECORDS == 1000
    assert fu.MAX_PAYLOAD_BYTES == 16 * 1024 * 1024


def test_record_cap_truncation_counts(tmp_path, monkeypatch):
    store = _eq_store(tmp_path)
    for i in range(5):
        _write_record(store, f"r{i}.json", _make_record(f"2026-01-0{i + 1}T00:00:00Z"))
    monkeypatch.setattr(fu, "MAX_PAYLOAD_RECORDS", 3)

    payload = fu._collect_exec_quant_payload(tmp_path)

    assert payload["record_count"] == 3
    assert payload["truncated_count"] == 2
    assert payload["cap_records"] == 3  # effective cap recorded (C-2 取证)
    assert [r["name"] for r in payload["records"]] == ["r0.json", "r1.json", "r2.json"]


def test_byte_cap_whole_record_granularity_and_oversize(tmp_path, monkeypatch):
    # U-01: truncation granularity = whole records; a single record bigger
    # than the cap is itself truncated — no partial bytes ever leave the store.
    store = _eq_store(tmp_path)
    _write_record(store, "small.json", _make_record("2026-01-01T00:00:00Z"))
    _write_record(store, "huge.json", _make_record("2026-01-02T00:00:00Z"), pad=2048)
    monkeypatch.setattr(fu, "MAX_PAYLOAD_BYTES", 1024)

    payload = fu._collect_exec_quant_payload(tmp_path)

    sizes = {r["name"]: len(r["data"]) for r in payload["records"]}
    assert sizes["small.json"] < 1024
    assert payload["record_count"] == 1
    assert payload["truncated_count"] == 1  # the oversize record itself
    assert sum(sizes.values()) <= fu.MAX_PAYLOAD_BYTES


def test_byte_cap_greedy_prefix_stops_at_first_violator(tmp_path, monkeypatch):
    store = _eq_store(tmp_path)
    r1 = _write_record(store, "r1.json", _make_record("2026-01-01T00:00:00Z"), pad=60)
    _write_record(store, "r2.json", _make_record("2026-01-02T00:00:00Z"), pad=60)
    _write_record(store, "r3.json", _make_record("2026-01-03T00:00:00Z"), pad=60)
    r2 = (store / "records" / "r2.json").read_bytes()
    r3 = (store / "records" / "r3.json").read_bytes()
    cap = len(r1) + len(r2) + 10  # r1+r2 fit, r3 would exceed
    monkeypatch.setattr(fu, "MAX_PAYLOAD_BYTES", cap)

    payload = fu._collect_exec_quant_payload(tmp_path)

    names = [r["name"] for r in payload["records"]]
    assert names == ["r1.json", "r2.json"]
    assert payload["truncated_count"] == 1  # r3 and everything after it
    total = sum(len(r["data"]) for r in payload["records"])
    assert total <= cap


def test_missing_collected_at_sorts_first(tmp_path):
    # U-02: missing collected_at sorts as "" (first, ascending), deterministic.
    store = _eq_store(tmp_path)
    _write_record(store, "with-time.json", _make_record("2026-01-01T00:00:00Z"))
    _write_record(store, "no-time.json", {"kind": STR001, "unit_id": "/speckit.plan"})

    payload = fu._collect_exec_quant_payload(tmp_path)

    names = [r["name"] for r in payload["records"]]
    assert names == ["no-time.json", "with-time.json"]
    assert payload["collected_at_range"] == ["", "2026-01-01T00:00:00Z"]


def test_bucket_exhaustiveness_invariant(tmp_path, monkeypatch):
    # U-03: record_count + skipped_unreadable + truncated_count == probed total.
    store = _eq_store(tmp_path)
    for i in range(4):
        _write_record(store, f"g{i}.json", _make_record(f"2026-01-0{i + 1}T00:00:00Z"))
    _write_record(store, "bad.json", _make_record("2026-01-05T00:00:00Z",
                                                  kind="other.kind"))
    _write_legacy(store, [json.dumps(_make_record("2026-01-06T00:00:00Z")),
                          "not-json-at-all"])
    probed_total = 7  # 4 good + 1 wrong-kind + 1 good legacy + 1 broken legacy
    monkeypatch.setattr(fu, "MAX_PAYLOAD_RECORDS", 3)

    payload = fu._collect_exec_quant_payload(tmp_path)

    assert (payload["record_count"] + payload["skipped_unreadable"]
            + payload["truncated_count"] == probed_total)


# --------------------------------------------------------------------------- #
# C-1: read-only source store
# --------------------------------------------------------------------------- #
def test_sweep_is_read_only_on_source_store(tmp_path):
    store = _eq_store(tmp_path)
    _write_record(store, "a.json", _make_record("2026-01-01T00:00:00Z"))
    _write_legacy(store, [json.dumps(_make_record("2026-01-02T00:00:00Z"))])
    before = _snapshot(store)

    fu._collect_exec_quant_payload(tmp_path)

    assert _snapshot(store) == before  # zero change, zero move, zero delete


def test_missing_store_degrades_to_empty_payload(tmp_path):
    payload = fu._collect_exec_quant_payload(tmp_path)  # no exec-quant dir at all

    assert payload["record_count"] == 0
    assert payload["skipped_unreadable"] == 0
    assert payload["truncated_count"] == 0
    assert payload["collected_at_range"] is None
    assert payload["source_form_counts"] == {"records-dir": 0, "legacy-jsonl": 0}


# --------------------------------------------------------------------------- #
# C-5 / D3: package-level identity
# --------------------------------------------------------------------------- #
def test_identity_reads_project_name_line(tmp_path):
    spec_dir = tmp_path / ".specify"
    spec_dir.mkdir(parents=True)
    (spec_dir / "instructions.md").write_text(
        "# Title\n\n- **Project Name**: cws-lib-python\n\nbody\n", encoding="utf-8")

    identity = fu._resolve_package_identity(tmp_path)

    assert identity["project_name"] == "cws-lib-python"
    assert identity["identity_status"] == "identified"


def test_identity_falls_back_to_workspace_basename(tmp_path):
    # (a) no instructions.md at all; (b) instructions.md without the line.
    identity = fu._resolve_package_identity(tmp_path)
    assert identity["project_name"] == tmp_path.name
    assert identity["identity_status"] == "identified"

    (tmp_path / ".specify").mkdir()
    (tmp_path / ".specify" / "instructions.md").write_text(
        "# no project name here\n", encoding="utf-8")
    identity = fu._resolve_package_identity(tmp_path)
    assert identity["project_name"] == tmp_path.name
    assert identity["identity_status"] == "identified"


def test_identity_unknown_project_when_no_name_available():
    # Root has no instructions.md and no basename — both fallbacks exhausted.
    identity = fu._resolve_package_identity(Path("/"))
    assert identity["project_name"] == ""
    assert identity["identity_status"] == "unknown-project"


def _make_git_dir(workspace: Path) -> None:
    git = workspace / ".git"
    (git / "refs" / "heads").mkdir(parents=True)
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git / "refs" / "heads" / "main").write_text(HEX40 + "\n", encoding="utf-8")


def test_source_commit_resolves_head_via_git_files(tmp_path):
    _make_git_dir(tmp_path)
    assert fu._resolve_source_commit(tmp_path) == HEX40


def test_source_commit_detached_head_and_packed_refs(tmp_path):
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text(HEX40 + "\n", encoding="utf-8")  # detached form
    assert fu._resolve_source_commit(tmp_path) == HEX40

    (git / "HEAD").write_text("ref: refs/heads/packed-only\n", encoding="utf-8")
    (git / "packed-refs").write_text(
        f"# pack-refs with: peeled \n{HEX40} refs/heads/packed-only\n",
        encoding="utf-8")
    assert fu._resolve_source_commit(tmp_path) == HEX40


def test_source_commit_null_without_git_and_on_garbage(tmp_path):
    assert fu._resolve_source_commit(tmp_path) is None  # no .git

    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("ref: refs/heads/void\n", encoding="utf-8")
    assert fu._resolve_source_commit(tmp_path) is None  # dangling ref

    (git / "HEAD").write_text("garbage-head-content\n", encoding="utf-8")
    assert fu._resolve_source_commit(tmp_path) is None  # unparseable HEAD


def test_source_commit_rejects_non_40hex(tmp_path):
    git = tmp_path / ".git"
    (git / "refs" / "heads").mkdir(parents=True)
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git / "refs" / "heads" / "main").write_text("not-a-sha\n", encoding="utf-8")
    assert fu._resolve_source_commit(tmp_path) is None  # E2: 40-hex or null
