"""Contract tests for the exec-quant payload in the package leg (Feature 068).

Owns ``.specify/specs/068-exec-quant-feedback-channel/contracts/package-layout.md``
C-3..C-9: zip layout, byte-verbatim records, payload-manifest field set
(data-model § E4), MANIFEST § Exec-Quant Payload same-source rendering, dual
report faces (FR-004), FR-019 both directions, read-only source stores,
zero-change semantics of external exclusion / time filter / ``--all`` /
``--include-introspection``, and non-blocking degradation (exit 0).

Engine invocation is the engine's own CLI form in-process (same shape as
``test_feedback_utils_cli.py``); fixtures are all self-constructed.

Red-first evidence: notes/red-first-evidence.md (§ T005).
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from tests.contract.helpers_introspection import (_record, _report_text,
                                                  _write_report)
from tests.script_api import feedback_utils as fu

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)
PAYLOAD_KIND = "speckit.exec-quant-payload"  # data-model § E4

E4_FIELDS = {"schema_version", "kind", "identity", "record_count",
             "source_form_counts", "skipped_unreadable", "truncated_count",
             "cap_records", "cap_bytes", "collected_at_range"}


# --------------------------------------------------------------------------- #
# fixture helpers
# --------------------------------------------------------------------------- #
def _make_workspace(tmp_path: Path, project: str = "cws-lib-python") -> Path:
    spec = tmp_path / ".specify"
    spec.mkdir(parents=True, exist_ok=True)
    (spec / "instructions.md").write_text(
        f"- **Project Name**: {project}\n", encoding="utf-8")
    return tmp_path


def _make_eq(collected_at: str) -> dict:
    return {"kind": STR001, "schema_version": 1, "unit_id": "/speckit.plan",
            "unit_type": "command", "run_id": "r1", "collected_at": collected_at}


def _write_record(ws: Path, name: str, collected_at: str, pad: int = 0) -> bytes:
    rdir = ws / ".specify" / "memory" / "exec-quant" / "records"
    rdir.mkdir(parents=True, exist_ok=True)
    record = dict(_make_eq(collected_at), schema_version=2)
    if pad:
        record["pad"] = "x" * pad
    raw = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    (rdir / name).write_bytes(raw)
    return raw


def _store(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "feedback"


def _eq_store(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant"


def _snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()
            and "packages" not in p.parts}  # packages/ = zip output artifact


def _package(ws: Path, capsys, *extra: str) -> dict:
    """Run --action package --format json; return the JSON payload."""
    capsys.readouterr()  # drain output left by fixture helpers (_record etc.)
    rc = fu.main(["--action", "package", "--workspace-root", str(ws),
                  "--format", "json", *extra])
    assert rc == 0, "package degradations must not fail the action (C-9)"
    return json.loads(capsys.readouterr().out)


def _package_text(ws: Path, capsys, *extra: str) -> str:
    capsys.readouterr()  # drain output left by fixture helpers (_record etc.)
    rc = fu.main(["--action", "package", "--workspace-root", str(ws), *extra])
    assert rc == 0
    return capsys.readouterr().out


# --------------------------------------------------------------------------- #
# C-3: zip layout
# --------------------------------------------------------------------------- #
def test_zip_layout_payload_only_under_exec_quant(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        names = zf.namelist()
        manifest = zf.read("MANIFEST.md").decode("utf-8")

    assert "exec-quant/payload-manifest.json" in names
    assert "exec-quant/records/2026-a.json" in names
    # payload exists ONLY under exec-quant/: every non-exec-quant member is
    # one of the pre-existing declared forms (entries / MANIFEST / notes /
    # introspection), never a stray payload file.
    outside = [n for n in names if not n.startswith("exec-quant/")]
    assert all(n == "MANIFEST.md"
               or n == "SUBMISSION-NOTES.md"
               or n.startswith("introspection/")
               or (n.endswith(".md") and "exec-quant" not in n)
               for n in outside)
    assert "Feedback Package Manifest" in manifest  # MANIFEST.md intact


def test_record_members_byte_verbatim(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    raw = _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z", pad=40)
    _record(ws, "run-a")

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        assert zf.read("exec-quant/records/2026-a.json") == raw
        # zero reordering/re-encoding: member decodes to the same JSON object
        assert json.loads(zf.read("exec-quant/records/2026-a.json"))["pad"]


# --------------------------------------------------------------------------- #
# C-4 / data-model E4: payload-manifest field set
# --------------------------------------------------------------------------- #
def test_payload_manifest_field_set_e4(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")
    _write_record(ws, "2026-b.json", "2026-01-02T00:00:00Z")

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        pm = json.loads(zf.read("exec-quant/payload-manifest.json"))
        record_members = [n for n in zf.namelist()
                          if n.startswith("exec-quant/records/")]

    assert set(pm.keys()) == E4_FIELDS
    assert pm["schema_version"] == 1
    assert pm["kind"] == PAYLOAD_KIND
    assert set(pm["identity"].keys()) == {"project_name", "source_commit",
                                          "identity_status"}
    assert pm["identity"]["project_name"] == "cws-lib-python"
    assert pm["identity"]["identity_status"] == "identified"
    assert pm["record_count"] == 2 == len(record_members)  # E4 identity law
    assert pm["source_form_counts"] == {"records-dir": 2, "legacy-jsonl": 0}
    assert pm["skipped_unreadable"] == 0
    assert pm["truncated_count"] == 0
    assert pm["cap_records"] == fu.MAX_PAYLOAD_RECORDS  # effective caps (C-2)
    assert pm["cap_bytes"] == fu.MAX_PAYLOAD_BYTES
    assert pm["collected_at_range"] == ["2026-01-01T00:00:00Z",
                                        "2026-01-02T00:00:00Z"]


def test_payload_manifest_counts_legacy_form(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    legacy = ws / ".specify" / "memory" / "exec-quant" / "records.jsonl"
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text(json.dumps(_make_eq("2026-01-01T00:00:00Z")) + "\n"
                      + "{broken\n", encoding="utf-8")

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        pm = json.loads(zf.read("exec-quant/payload-manifest.json"))
        names = zf.namelist()

    assert pm["record_count"] == 1
    assert pm["source_form_counts"] == {"records-dir": 0, "legacy-jsonl": 1}
    assert pm["skipped_unreadable"] == 1
    assert "exec-quant/records/legacy-records-L0001.json" in names


# --------------------------------------------------------------------------- #
# C-6 / E5: MANIFEST human section, same source as machine manifest
# --------------------------------------------------------------------------- #
def _manifest_section(manifest_text: str) -> str:
    lines = manifest_text.splitlines()
    start = next(i for i, l in enumerate(lines)
                 if l.strip().lower().startswith("## exec-quant payload"))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def test_manifest_human_section_same_source(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")
    legacy = ws / ".specify" / "memory" / "exec-quant" / "records.jsonl"
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text("{broken line\n", encoding="utf-8")

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        pm = json.loads(zf.read("exec-quant/payload-manifest.json"))
        section = _manifest_section(zf.read("MANIFEST.md").decode("utf-8"))

    # every machine number appears in the human section (same-source rendering)
    assert f"**Records**: {pm['record_count']}" in section
    assert f"records-dir {pm['source_form_counts']['records-dir']}" in section
    assert f"legacy-jsonl {pm['source_form_counts']['legacy-jsonl']}" in section
    assert f"**Skipped unreadable**: {pm['skipped_unreadable']}" in section
    assert f"**Truncated**: {pm['truncated_count']}" in section
    assert pm["identity"]["project_name"] in section
    assert "triggered: no" in section


def test_manifest_empty_payload_section_declares_no_data(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")  # feedback entry present; NO exec-quant store

    result = _package(ws, capsys)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        pm = json.loads(zf.read("exec-quant/payload-manifest.json"))
        section = _manifest_section(zf.read("MANIFEST.md").decode("utf-8"))

    assert pm["record_count"] == 0
    assert pm["collected_at_range"] is None
    assert "无量化数据" in section  # C-6: empty payload section MUST exist


# --------------------------------------------------------------------------- #
# C-7: dual report faces
# --------------------------------------------------------------------------- #
def test_json_report_face_visible_counts(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    result = _package(ws, capsys)

    rep = result["exec_quant_payload"]
    assert rep["record_count"] == 1
    assert rep["skipped_unreadable"] == 0
    assert rep["truncated_count"] == 0
    assert rep["source_form_counts"] == {"records-dir": 1, "legacy-jsonl": 0}
    assert rep["identity_status"] == "identified"


def test_text_report_face_visible_counts(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    out = _package_text(ws, capsys)

    assert "exec-quant payload" in out
    assert "1 record" in out  # the record count is visible on the text face


# --------------------------------------------------------------------------- #
# C-8 / FR-019: both directions
# --------------------------------------------------------------------------- #
def test_fr019_empty_feedback_still_packages(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")  # payload only

    result = _package(ws, capsys)

    assert result["zip"] and (ws / result["zip"]).exists()
    assert result["packaged"] == 0
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        manifest = zf.read("MANIFEST.md").decode("utf-8")
        names = zf.namelist()
    assert "- **Entries**: 0" in manifest  # explicit zero, MANIFEST face
    assert "exec-quant/records/2026-a.json" in names  # payload rides along


def test_fr019_double_empty_no_package_with_explicit_note(tmp_path, capsys):
    ws = _make_workspace(tmp_path)  # no feedback entries, no exec-quant store

    result = _package(ws, capsys)

    assert result["zip"] is None
    assert result["packaged"] == 0
    note = result.get("note", "")
    assert "feedback" in note.lower() and "exec-quant" in note.lower()


# --------------------------------------------------------------------------- #
# FR-002 / SC-001: read-only source stores
# --------------------------------------------------------------------------- #
def test_source_stores_read_only_after_package(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")
    before_fb = _snapshot(_store(ws))
    before_eq = _snapshot(_eq_store(ws))

    _package(ws, capsys)

    assert _snapshot(_store(ws)) == before_fb  # feedback store untouched
    assert _snapshot(_eq_store(ws)) == before_eq  # exec-quant store untouched


# --------------------------------------------------------------------------- #
# C-8: external exclusion / time filter / --all / --include-introspection
# --------------------------------------------------------------------------- #
def test_time_filter_all_semantics_unchanged_payload_full(
        tmp_path, capsys, monkeypatch):
    ws = _make_workspace(tmp_path)
    # Drive a monotonically increasing clock: entries and the submission
    # boundary share second granularity otherwise (same reason
    # test_feedback_package.py monkeypatches now_iso).
    counter = {"n": 0}

    def fake_now():
        counter["n"] += 1
        return f"2026-06-01T00:00:{counter['n']:02d}Z"

    monkeypatch.setattr(fu, "now_iso", fake_now)
    _record(ws, "run-1")
    _record(ws, "run-2")
    fu.main(["--action", "mark-submitted", "--workspace-root", str(ws)])
    _record(ws, "run-3")  # after the submission boundary
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")
    _write_record(ws, "2026-b.json", "2026-01-02T00:00:00Z")

    result = _package(ws, capsys)  # default: time filter applies to entries
    assert result["packaged"] == 1
    # FR-001: the payload is NOT watermarked — full inclusion regardless
    assert result["exec_quant_payload"]["record_count"] == 2
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        manifest = zf.read("MANIFEST.md").decode("utf-8")
    assert "- **Entries**: 1" in manifest

    result = _package(ws, capsys, "--all")
    # --all = the full store; mark-submitted archives but never removes
    # entries, so all three recorded entries are still there (zero change).
    assert result["packaged"] == 3
    assert result["exec_quant_payload"]["record_count"] == 2


def test_external_exclusion_semantics_unchanged(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a", kind="external")
    _record(ws, "run-b")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    result = _package(ws, capsys)

    assert result["excluded_external"] == 1  # external still excluded
    assert result["packaged"] == 1
    # the payload sweep is independent of the external exclusion
    assert result["exec_quant_payload"]["record_count"] == 1


def test_include_introspection_semantics_unchanged(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    # A linked report is required for the Introspection section to render
    # (pre-existing package behavior); set it up the same way
    # test_feedback_introspection_engine.py does.
    eid = _record(ws, "run-a")
    report_id = "introspection-20260828T030000Z"
    _write_report(ws, report_id, _report_text(report_id, [eid]))
    rc = fu.main(["--action", "introspect-register", "--workspace-root",
                  str(ws), "--report-file",
                  str(ws / ".specify/memory/feedback/introspection"
                      f"/{report_id}.md")])
    assert rc == 0
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    result = _package(ws, capsys, "--include-introspection")

    with zipfile.ZipFile(ws / result["zip"]) as zf:
        manifest = zf.read("MANIFEST.md").decode("utf-8")
        names = zf.namelist()
    assert f"introspection/{report_id}.md" in names  # existing member intact
    assert "## Introspection Reports" in manifest  # existing section intact
    assert "## Exec-Quant Payload" in manifest  # new section coexists


def test_mark_submitted_archive_has_no_payload(tmp_path, capsys):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    capsys.readouterr()  # drain the record JSON first
    rc = fu.main(["--action", "mark-submitted", "--workspace-root", str(ws),
                  "--format", "json"])
    assert rc == 0
    result = json.loads(capsys.readouterr().out)
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        names = zf.namelist()

    assert not any(n.startswith("exec-quant/") for n in names)  # zero change


# --------------------------------------------------------------------------- #
# C-9: degradations are non-blocking, exit 0
# --------------------------------------------------------------------------- #
def test_payload_degradations_exit_zero(tmp_path, capsys, monkeypatch):
    ws = _make_workspace(tmp_path)
    _record(ws, "run-a")
    (ws / ".specify" / "memory" / "exec-quant" / "records").mkdir(parents=True)
    (ws / ".specify" / "memory" / "exec-quant" / "records" / "bad.json"
     ).write_bytes(b"{broken")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")
    _write_record(ws, "2026-b.json", "2026-01-02T00:00:00Z")
    monkeypatch.setattr(fu, "MAX_PAYLOAD_RECORDS", 1)  # force truncation

    result = _package(ws, capsys)  # rc asserted 0 by _package

    rep = result["exec_quant_payload"]
    assert rep["skipped_unreadable"] == 1
    assert rep["truncated_count"] == 1  # 2026-b over the patched cap
    assert rep["record_count"] == 1


def test_identity_degradation_exit_zero(tmp_path, capsys):
    ws = tmp_path  # no instructions.md and no .git; basename fallback applies
    _record(ws, "run-a")
    _write_record(ws, "2026-a.json", "2026-01-01T00:00:00Z")

    result = _package(ws, capsys)

    assert result["zip"]
    assert result["exec_quant_payload"]["record_count"] == 1
