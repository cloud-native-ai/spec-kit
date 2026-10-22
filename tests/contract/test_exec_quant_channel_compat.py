"""Compatibility guard contract tests for the 068 exec-quant feedback channel (US4).

Owns ``.specify/specs/068-exec-quant-feedback-channel/contracts/compatibility-security.md``
C-27 (no-payload package → zero-difference receive: zero counts, exit 0, zero
storage write; empty feedback + empty payload → package stays packageless with
an explicit note), C-28 (version / layout / shape tolerance: records-dir and
legacy jsonl, schema v1 and v2, ``{value, provenance}`` objects and bare
[[STR-002]] strings coexist through the full package → receive → aggregate
chain; unknown new fields survive verbatim into the aggregated layer; the
legacy monolithic stream is read-only, never rewritten), C-29 (zero new
blocking confirmation gates — the three legs stay out of every gate surface
and any exit switch is only a non-blocking optional parameter) and C-30
(storage boundary — the aggregated layer exists only under
``exec-quant/aggregated/``, the two store inventories never count each other,
exec-quant records never mix into the feedback store).

Regression-net form (tasks.md Phase 5 header note): guards the three legs'
landed behavior; NOT red-first — a red is attributed (subject regression vs
assertion defect, SKILL § TDD) before any fix, never silently dropped.

The real inbound baseline ``feedback/feedback-20261022T062525Z.zip`` is used
READ-ONLY as the equal-structure reference (member names only); the exercised
packages are always self-constructed. Engine invocation is in-process via
``tests/script_api.py`` (framework sources, never the ``.specify/`` mirrors).

Run evidence: notes/red-first-evidence.md (§ part 5, T024).
"""
from __future__ import annotations

import builtins
import json
import zipfile
from pathlib import Path

import pytest

from tests.script_api import _load_module, feedback_utils as fu

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]

EQ = _load_module("exec_quant_compat_contract", "exec-quant.py")

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)
NOT_EVALUATED = "not_evaluated"  # [[STR-002]] (requirements § Shared Strings)
PAYLOAD_KIND = "speckit.exec-quant-payload"  # data-model § E4

REAL_BASELINE_ZIP = REPO_ROOT / "feedback" / "feedback-20261022T062525Z.zip"

#: pre-existing destructive/warned action set (C-26: zero growth by 068)
PREEXISTING_DESTRUCTIVE = frozenset({
    "package", "cleanup", "migrate-legacy", "mark-submitted",
    "dispose", "introspect-register",
})
CONFIRM_FLAG_NAMES = {"--yes", "--force", "--no-confirm", "--assume-yes",
                      "--approve", "--i-am-sure", "--non-interactive-confirmed"}


# --------------------------------------------------------------------------- #
# fixture helpers
# --------------------------------------------------------------------------- #
def _rec(collected_at: str = "2026-01-01T00:00:00Z", unit: str = "/speckit.plan",
         run: str = "r1", **extra) -> dict:
    record = {"kind": STR001, "schema_version": 2, "unit_id": unit,
              "unit_type": "command", "run_id": run,
              "collected_at": collected_at}
    record.update(extra)
    return record


def _make_package(directory: Path, records: list, project: str = "cws-chain-src",
                  name: str = "feedback-2026.zip") -> Path:
    manifest = {
        "schema_version": 1, "kind": PAYLOAD_KIND,
        "identity": {"project_name": project, "source_commit": None,
                     "identity_status": "identified"},
        "record_count": len(records),
        "source_form_counts": {"records-dir": len(records), "legacy-jsonl": 0},
        "skipped_unreadable": 0, "truncated_count": 0,
        "cap_records": 1000, "cap_bytes": 16777216,
        "collected_at_range": None,
    }
    zip_path = directory / name
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("exec-quant/payload-manifest.json",
                    json.dumps(manifest, ensure_ascii=False))
        for i, record in enumerate(records):
            zf.writestr(f"exec-quant/records/{i:04d}.json",
                        json.dumps(record, ensure_ascii=False) + "\n")
    return zip_path


def _ingest(ws: Path, package: Path, capsys):
    capsys.readouterr()
    rc = fu.main(["--action", "ingest-exec-quant", "--package", str(package),
                  "--workspace-root", str(ws), "--format", "json"])
    return json.loads(capsys.readouterr().out), rc


def _snapshot(root: Path) -> dict:
    if not root.is_dir():
        return {}
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _feedback_entry(ws: Path, run_id: str) -> None:
    rc = fu.main(["--action", "record", "--workspace-root", str(ws),
                  "--unit-id", "/speckit.plan", "--unit-type", "command",
                  "--run-id", run_id, "--review", f"review for {run_id}",
                  "--points", "ok"])
    assert rc == 0


# --------------------------------------------------------------------------- #
# C-27: no-payload package → zero-difference receive
# --------------------------------------------------------------------------- #
def test_self_constructed_no_payload_package_zero_difference(tmp_path, capsys):
    ws = tmp_path / "ws"
    (ws / ".specify").mkdir(parents=True)
    pkg = tmp_path / "equal-structure.zip"
    with zipfile.ZipFile(pkg, "w") as zf:  # the pre-068 package face only
        zf.writestr("MANIFEST.md", "# Feedback Package Manifest\n\n- **Entries**: 2\n")
        zf.writestr("20260101T000000Z-speckit-plan.md", "entry one\n")
        zf.writestr("20260101T000100Z-speckit-review.md", "entry two\n")
        zf.writestr("SUBMISSION-NOTES.md", "submission notes\n")
        zf.writestr("introspection/20260101T000200Z.md", "report body\n")

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["record_count"] == 0
    assert payload["ingested"] == 0
    assert payload["duplicates_skipped"] == 0
    assert payload["skipped_unreadable"] == 0
    assert payload["identity_conflicts"] == 0
    assert payload["groups_touched"] == 0
    assert payload["manifest_unreadable"] is False
    assert _snapshot(ws) == {}  # zero storage write, zero directory creation


@pytest.mark.skipif(not REAL_BASELINE_ZIP.is_file(),
                    reason="real inbound baseline zip absent in this checkout")
def test_real_baseline_reference_read_only_and_equal_structure(tmp_path, capsys):
    # the real package is a READ-ONLY reference: its member structure defines
    # the self-constructed equal-structure zip; its bytes must be untouched
    before = REAL_BASELINE_ZIP.read_bytes()
    with zipfile.ZipFile(REAL_BASELINE_ZIP) as zf:
        structure = zf.namelist()
    assert structure, "reference zip unexpectedly empty"
    assert not any(name.startswith("exec-quant/") for name in structure), (
        "the reference zip no longer represents the 068-pre package shape")

    ws = tmp_path / "ws"
    (ws / ".specify").mkdir(parents=True)
    pkg = tmp_path / "equal-structure.zip"
    with zipfile.ZipFile(pkg, "w") as zf:  # same names, synthetic bodies
        for name in structure:
            zf.writestr(name, f"synthetic body: {name}\n")

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["record_count"] == 0 and payload["ingested"] == 0
    assert _snapshot(ws) == {}  # zero-difference receive
    assert REAL_BASELINE_ZIP.read_bytes() == before  # reference untouched


def test_double_empty_packages_nothing_with_explicit_note(tmp_path, capsys):
    # C-27: empty feedback + empty payload → package behaves exactly as
    # before 068 (no zip produced, explicitly explained — C-8 semantics)
    ws = tmp_path  # no feedback entries, no exec-quant store

    capsys.readouterr()
    rc = fu.main(["--action", "package", "--workspace-root", str(ws),
                  "--format", "json"])

    assert rc == 0
    result = json.loads(capsys.readouterr().out)
    assert result["zip"] is None and result["packaged"] == 0
    note = result.get("note", "")
    assert "feedback" in note.lower() and "exec-quant" in note.lower(), (
        f"package-less result lost its explicit explanation: {note!r}")
    assert _snapshot(ws) == {}  # nothing was produced at all


# --------------------------------------------------------------------------- #
# C-28: version / layout / shape tolerance through the full chain
# --------------------------------------------------------------------------- #
def test_triple_coexistence_full_chain_package_receive_aggregate(
        tmp_path, capsys):
    ws1 = tmp_path / "source-ws"
    rdir = ws1 / ".specify" / "memory" / "exec-quant" / "records"
    rdir.mkdir(parents=True)
    v2 = _rec("2026-01-01T00:00:00Z", "/speckit.plan", "r-v2",
              quality={"elapsed_ms": {"value": 1200, "provenance": "carried"},
                       "tokens": NOT_EVALUATED,
                       "brand_new_axis": NOT_EVALUATED,
                       "odd_future_form": "raw-unforeseen"},
              future_top_level_field={"note": "unknown new field"})
    v1 = {"kind": STR001, "schema_version": 1, "unit_id": "/speckit.implement",
          "unit_type": "command", "run_id": "r-v1",
          "collected_at": "2026-01-02T00:00:00Z",
          "quality": {"elapsed_ms": NOT_EVALUATED}}
    (rdir / "v2.json").write_text(json.dumps(v2) + "\n", encoding="utf-8")
    (rdir / "v1.json").write_text(json.dumps(v1) + "\n", encoding="utf-8")
    legacy = ws1 / ".specify" / "memory" / "exec-quant" / "records.jsonl"
    legacy.write_text(json.dumps(
        _rec("2026-01-03T00:00:00Z", "/speckit.review", "r-legacy",
             quality={"tokens": {"value": 7, "provenance": "measured"}},
             legacy_extra="keep-me"), ensure_ascii=False) + "\n{broken\n",
        encoding="utf-8")
    store_before = _snapshot(ws1 / ".specify" / "memory" / "exec-quant")
    _feedback_entry(ws1, "run-entry")

    # leg 1 — package: both layouts, both schemas, both shapes in one zip
    capsys.readouterr()
    rc = fu.main(["--action", "package", "--workspace-root", str(ws1),
                  "--format", "json"])
    assert rc == 0
    packaged = json.loads(capsys.readouterr().out)
    rep = packaged["exec_quant_payload"]
    assert rep["record_count"] == 3
    assert rep["source_form_counts"] == {"records-dir": 2, "legacy-jsonl": 1}
    assert rep["skipped_unreadable"] == 1  # the broken legacy line, counted
    with zipfile.ZipFile(ws1 / packaged["zip"]) as zf:
        members = [n for n in zf.namelist() if n.startswith("exec-quant/records/")]
        carried = {n: json.loads(zf.read(n)) for n in members}
    assert len(members) == 3
    assert "exec-quant/records/legacy-records-L0001.json" in members
    carried_forms = {json.dumps(rec, sort_keys=True) for rec in carried.values()}
    assert json.dumps(v2, sort_keys=True) in carried_forms  # verbatim carry
    assert json.dumps(v1, sort_keys=True) in carried_forms
    assert _snapshot(ws1 / ".specify" / "memory" / "exec-quant") == store_before

    # leg 2 — receive: unknown fields survive verbatim into the aggregated layer
    ws2 = tmp_path / "target-ws"
    (ws2 / ".specify").mkdir(parents=True)
    payload, rc = _ingest(ws2, ws1 / packaged["zip"], capsys)
    assert rc == 0
    assert payload["ingested"] == 3 and payload["skipped_unreadable"] == 0
    aggregated = ws2 / ".specify" / "memory" / "exec-quant" / "aggregated"
    envelopes = [json.loads(p.read_text(encoding="utf-8"))
                 for p in aggregated.glob("*/records/*.json")]
    landed = {json.dumps(env["record"], sort_keys=True): env for env in envelopes}
    assert len(landed) == 3
    for original in (v2, v1, json.loads(json.dumps(
            _rec("2026-01-03T00:00:00Z", "/speckit.review", "r-legacy",
                 quality={"tokens": {"value": 7, "provenance": "measured"}},
                 legacy_extra="keep-me")))):
        key = json.dumps(original, sort_keys=True)
        assert key in landed, f"record lost or mutated on receive: {original}"
    assert landed[json.dumps(v2, sort_keys=True)]["record"] == v2  # zero drop

    # leg 3 — aggregate: shapes normalized by the D8 rule, nothing fabricated
    capsys.readouterr()
    rc = EQ.main(["--action", "aggregate", "--workspace-root", str(ws2),
                  "--format", "json"])
    assert rc == 0
    view = json.loads(capsys.readouterr().out)
    source = view["sources"][0]
    assert source["record_count"] == 3
    quality = source["quality"]
    assert quality["elapsed_ms"] == {"evaluated": 1, "not_evaluated": 2}
    assert quality["tokens"] == {"evaluated": 1, "not_evaluated": 2}
    assert quality["brand_new_axis"] == {"evaluated": 0, "not_evaluated": 3}
    assert quality["odd_future_form"] == {"evaluated": 0, "not_evaluated": 3}
    assert source["coverage"] == {"evaluated_total": 2, "not_evaluated_total": 10}
    assert view["totals"]["record_count"] == 3


# --------------------------------------------------------------------------- #
# C-29: zero new blocking confirmation gates
# --------------------------------------------------------------------------- #
def test_new_legs_join_no_confirmation_gate_surface(tmp_path, capsys,
                                                    monkeypatch):
    # C-26 face: the pre-existing destructive/warned set itself did not grow
    assert frozenset(fu._DESTRUCTIVE_ACTIONS) == PREEXISTING_DESTRUCTIVE
    # C-29: no consent/opt-in flag exists on either engine's parser
    fu_flags = {opt for act in fu.build_parser()._actions for opt in act.option_strings}
    eq_flags = {opt for act in EQ.build_parser()._actions for opt in act.option_strings}
    assert not fu_flags & CONFIRM_FLAG_NAMES
    assert not eq_flags & CONFIRM_FLAG_NAMES
    # the aggregate exit switch is only the non-blocking --format parameter
    assert EQ.ARG_MANIFEST["aggregate"]["required"] == []
    # runtime: a blocking prompt is never consulted by any of the three legs
    monkeypatch.setattr(builtins, "input",
                        lambda *_a, **_k: (_ for _ in ()).throw(
                            AssertionError("blocking prompt consulted")))

    ws1 = tmp_path / "source-ws"
    rdir = ws1 / ".specify" / "memory" / "exec-quant" / "records"
    rdir.mkdir(parents=True)
    (rdir / "r.json").write_text(json.dumps(_rec(run="r-gate")) + "\n",
                                 encoding="utf-8")
    _feedback_entry(ws1, "run-gate")
    capsys.readouterr()
    assert fu.main(["--action", "package", "--workspace-root", str(ws1),
                    "--format", "json"]) == 0
    packaged = json.loads(capsys.readouterr().out)

    ws2 = tmp_path / "target-ws"
    (ws2 / ".specify").mkdir(parents=True)
    assert fu.main(["--action", "ingest-exec-quant",
                    "--package", str(ws1 / packaged["zip"]),
                    "--workspace-root", str(ws2), "--format", "json"]) == 0
    assert EQ.main(["--action", "aggregate", "--workspace-root", str(ws2),
                    "--format", "json"]) == 0


# --------------------------------------------------------------------------- #
# C-30: storage boundary
# --------------------------------------------------------------------------- #
def test_storage_boundary_and_inventory_disjunction(tmp_path, capsys):
    ws = tmp_path / "ws"
    (ws / ".specify").mkdir(parents=True)
    _feedback_entry(ws, "run-feedback")
    eq_unit = "custom:boundary/leak-probe"
    rdir = ws / ".specify" / "memory" / "exec-quant" / "records"
    rdir.mkdir(parents=True)
    (rdir / "eq.json").write_text(json.dumps(
        _rec(unit=eq_unit, run="run-quant")) + "\n", encoding="utf-8")
    feedback_store = ws / ".specify" / "memory" / "feedback"
    before = _snapshot(feedback_store)

    pkg = _make_package(ws, [_rec(unit=eq_unit, run="run-quant")])
    payload, rc = _ingest(ws, pkg, capsys)
    assert rc == 0 and payload["ingested"] == 1
    capsys.readouterr()
    assert EQ.main(["--action", "aggregate", "--workspace-root", str(ws),
                    "--format", "json"]) == 0

    # the aggregated layer exists only under exec-quant/aggregated/
    aggregated_dirs = [p for p in ws.rglob("aggregated") if p.is_dir()]
    assert aggregated_dirs == [ws / ".specify" / "memory" / "exec-quant" / "aggregated"]
    # exec-quant records never mix into the feedback store
    assert _snapshot(feedback_store) == before
    for path in feedback_store.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert STR001 not in text and eq_unit not in text
            assert "aggregation_envelope" not in text

    # inventory disjunction: each store's counting face counts only its own kind
    capsys.readouterr()
    assert fu.main(["--action", "list", "--workspace-root", str(ws),
                    "--format", "json"]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["count"] == 1  # only the feedback entry
    assert eq_unit not in json.dumps(listed) and STR001 not in json.dumps(listed)

    capsys.readouterr()
    assert EQ.main(["--action", "list-records", "--workspace-root", str(ws),
                    "--format", "json"]) == 0
    records_json = capsys.readouterr().out
    listed_records = json.loads(records_json)
    assert len(listed_records) == 1  # only the exec-quant record — the
    # aggregated/ envelopes beside it never enter the counting face
    assert listed_records[0]["unit_id"] == eq_unit
    assert "run-feedback" not in records_json and "speckit-plan" not in records_json
