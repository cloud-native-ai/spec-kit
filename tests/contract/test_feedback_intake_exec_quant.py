"""Contract tests for the exec-quant intake action (Feature 068, US2).

Owns ``.specify/specs/068-exec-quant-feedback-channel/contracts/intake-contract.md``
C-10..C-17: the ``--action ingest-exec-quant --package <zip>`` signature
(required ``--package`` + existing ``--workspace-root``), payload recognition
by the ``exec-quant/`` member prefix (no prefix → zero counts, exit 0, zero
storage writes — the 068-pre package stays zero-difference), degraded
manifest handling, unknown-project attribution without guessing, idempotent
re-ingest (F-01: same-key/different-content → keep-first + identity_conflicts),
the shared flock critical section (``aggregated/.write.lock``) with
tmp+rename entry writes, the C-16 output keys / exit-code ladder, and the
storage boundary (zero feedback-store contamination, zero touch of feedback
entries / introspection / SUBMISSION-NOTES, ingest never triggers aggregate).

Fixtures are all self-constructed packages; the real inbound baseline
``feedback/feedback-20261022T062525Z.zip`` is never touched. Engine
invocation is the engine's own CLI form in-process.

Red-first evidence: notes/red-first-evidence.md (§ T011).
"""
from __future__ import annotations

import fcntl
import json
import re
import threading
import zipfile
from pathlib import Path

import pytest

from tests.script_api import feedback_utils as fu

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)
PAYLOAD_KIND = "speckit.exec-quant-payload"  # data-model § E4

ENTRY_FORM = re.compile(r"^\d{8}T\d{6}\d{6}Z-[0-9a-f]{8}\.json$")  # entry_filename() 形态
SLUG_GROUP_FORM = re.compile(r"^[a-z0-9-]+-[0-9a-f]{8}$")  # D5 slug + hash8

REQUIRED_OUTPUT_KEYS = {"record_count", "ingested", "duplicates_skipped",
                        "skipped_unreadable", "identity_conflicts",
                        "groups_touched", "manifest_unreadable"}  # C-16


# --------------------------------------------------------------------------- #
# fixture helpers (self-constructed packages)
# --------------------------------------------------------------------------- #
def _rec(collected_at: str = "2026-01-01T00:00:00Z", unit: str = "/speckit.plan",
         unit_type: str = "command", run: str = "r1", **extra) -> dict:
    record = {"kind": STR001, "schema_version": 2, "unit_id": unit,
              "unit_type": unit_type, "run_id": run, "collected_at": collected_at}
    record.update(extra)
    return record


def _identity(project: str = "cws-lib-python", source_commit=None,
              status: str = "identified") -> dict:
    return {"project_name": project, "source_commit": source_commit,
            "identity_status": status}


def _make_package(directory: Path, records: list, project: str = "cws-lib-python",
                  *, identity=None, include_manifest: bool = True,
                  corrupt_manifest: bool = False, extra_members: dict = None,
                  name: str = "feedback-2026.zip") -> Path:
    """Build a self-constructed inbound zip with an exec-quant payload."""
    extra_members = extra_members or {}
    manifest = {
        "schema_version": 1,
        "kind": PAYLOAD_KIND,
        "identity": identity if identity is not None else _identity(project),
        "record_count": len(records),
        "source_form_counts": {"records-dir": len(records), "legacy-jsonl": 0},
        "skipped_unreadable": 0,
        "truncated_count": 0,
        "cap_records": 1000,
        "cap_bytes": 16777216,
        "collected_at_range": None,
    }
    zip_path = directory / name
    with zipfile.ZipFile(zip_path, "w") as zf:
        if include_manifest:
            body = ("{corrupt json" if corrupt_manifest
                    else json.dumps(manifest, ensure_ascii=False))
            zf.writestr("exec-quant/payload-manifest.json", body)
        for i, record in enumerate(records):
            zf.writestr(f"exec-quant/records/{i:04d}.json",
                        json.dumps(record, ensure_ascii=False) + "\n")
        for member, body in extra_members.items():
            zf.writestr(member, body)
    return zip_path


def _agg(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant" / "aggregated"


def _groups(ws: Path) -> list:
    aggregated = _agg(ws)
    if not aggregated.is_dir():
        return []
    return sorted(p for p in aggregated.iterdir()
                  if p.is_dir() and p.name != "summaries")


def _snapshot(root: Path) -> dict:
    if not root.is_dir():
        return {}
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _ingest(ws: Path, package: Path, capsys, *extra: str):
    """Run --action ingest-exec-quant --format json; return (payload, rc)."""
    capsys.readouterr()  # drain any prior output
    rc = fu.main(["--action", "ingest-exec-quant", "--package", str(package),
                  "--workspace-root", str(ws), "--format", "json", *extra])
    return json.loads(capsys.readouterr().out), rc


def _flat_records(ws: Path) -> list:
    return [p for group in _groups(ws)
            for p in (group / "records").glob("*.json")]


# --------------------------------------------------------------------------- #
# C-10: action signature — registration and required --package
# --------------------------------------------------------------------------- #
def test_action_is_registered():
    # C-10: the intake action joins the engine's action registry; feedback
    # actions keep their own registry entries untouched (C-26 face).
    assert "ingest-exec-quant" in fu._ACTIONS
    assert "package" in fu._ACTIONS  # pre-existing actions unchanged


def test_missing_package_flag_exit_2(tmp_path, capsys):
    # C-10: --package is REQUIRED for this action; the failure must be
    # attributable to the missing flag (never to an unregistered action) and
    # exit 2 — via the argparse usage error or the engine's FeedbackError.
    code = None
    try:
        code = fu.main(["--action", "ingest-exec-quant",
                        "--workspace-root", str(tmp_path)])
    except SystemExit as exc:
        code = exc.code
    err = capsys.readouterr().err
    assert code == 2
    assert "--package" in err  # the complaint names the missing flag
    assert "invalid choice" not in err  # the action itself is registered


# --------------------------------------------------------------------------- #
# C-11 / FR-009: no-payload package → zero difference, exit 0
# --------------------------------------------------------------------------- #
def test_no_payload_package_zero_difference(tmp_path, capsys):
    ws = tmp_path
    pkg = _make_package(ws, [], extra_members={
        "MANIFEST.md": "# Feedback Package Manifest\n",
        "SUBMISSION-NOTES.md": "notes\n"})
    before_fb = _snapshot(ws / ".specify" / "memory" / "feedback")

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0  # no payload is not an error (C-11 / quickstart scenario 5)
    assert payload["record_count"] == 0
    assert payload["ingested"] == 0
    assert payload["duplicates_skipped"] == 0
    assert payload["skipped_unreadable"] == 0
    assert payload["identity_conflicts"] == 0
    assert payload["groups_touched"] == 0
    assert payload["manifest_unreadable"] is False
    assert not _agg(ws).exists()  # zero storage write, zero directory creation
    assert _snapshot(ws / ".specify" / "memory" / "feedback") == before_fb


# --------------------------------------------------------------------------- #
# C-11: degraded payload-manifest → member-by-member attempt, non-blocking
# --------------------------------------------------------------------------- #
def test_manifest_missing_records_still_ingested(tmp_path, capsys):
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z"), _rec("2026-01-02T00:00:00Z")]
    pkg = _make_package(ws, records, include_manifest=False)

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0  # degradation is non-blocking (C-16)
    assert payload["manifest_unreadable"] is True
    assert payload["record_count"] == 2
    assert payload["ingested"] == 2
    # identity lives in the manifest: without it → literal unknown-project group
    assert [g.name for g in _groups(ws)] == ["unknown-project"]


def test_manifest_corrupt_json_still_ingests(tmp_path, capsys):
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z")]
    pkg = _make_package(ws, records, corrupt_manifest=True)

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["manifest_unreadable"] is True
    assert payload["ingested"] == 1
    assert payload["skipped_unreadable"] == 0


# --------------------------------------------------------------------------- #
# C-11 / FR-010: unreadable / wrong-kind members counted, non-blocking
# --------------------------------------------------------------------------- #
def test_unreadable_and_wrong_kind_members_skipped(tmp_path, capsys):
    ws = tmp_path
    good = _rec("2026-01-01T00:00:00Z")
    wrong_kind = _rec("2026-01-02T00:00:00Z", unit="/speckit.other", run="rx")
    pkg_path = ws / "mixed.zip"
    with zipfile.ZipFile(pkg_path, "w") as zf:
        zf.writestr("exec-quant/payload-manifest.json",
                    json.dumps({"schema_version": 1, "kind": PAYLOAD_KIND,
                                "identity": _identity(),
                                "record_count": 3}))
        zf.writestr("exec-quant/records/0000.json",
                    json.dumps(good, ensure_ascii=False))
        zf.writestr("exec-quant/records/0001.json", "{not json")
        zf.writestr("exec-quant/records/0002.json",
                    json.dumps(dict(wrong_kind, kind="some.other.kind"),
                               ensure_ascii=False))

    payload, rc = _ingest(ws, pkg_path, capsys)

    assert rc == 0  # skipped members never block the action (C-11)
    assert payload["record_count"] == 3
    assert payload["ingested"] == 1
    assert payload["skipped_unreadable"] == 2
    assert len(_flat_records(ws)) == 1


# --------------------------------------------------------------------------- #
# C-12: attribution and grouping — never guess the identity
# --------------------------------------------------------------------------- #
def test_manifest_identity_missing_lands_unknown_project(tmp_path, capsys):
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z")]
    pkg = _make_package(ws, records, identity=None)
    # rewrite the manifest WITHOUT the identity key at all
    with zipfile.ZipFile(pkg, "w") as zf:
        zf.writestr("exec-quant/payload-manifest.json",
                    json.dumps({"schema_version": 1, "kind": PAYLOAD_KIND,
                                "record_count": 1}))
        zf.writestr("exec-quant/records/0000.json",
                    json.dumps(records[0], ensure_ascii=False))

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["ingested"] == 1
    assert [g.name for g in _groups(ws)] == ["unknown-project"]  # 字面分组


def test_unknown_project_status_lands_literal_group_no_guessing(tmp_path, capsys):
    # identity_status == "unknown-project" wins even though the zip file NAME
    # carries a project-looking token — attribution MUST NOT guess from the
    # path or the record content (C-12 / Edge Cases).
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z")]
    pkg = _make_package(ws, records, name="totally-other-project-run7.zip",
                        identity=_identity(project="", status="unknown-project"))

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["ingested"] == 1
    assert [g.name for g in _groups(ws)] == ["unknown-project"]
    envelope = json.loads(_flat_records(ws)[0].read_text(encoding="utf-8"))
    assert envelope["aggregation_envelope"]["source_project"] == "unknown-project"


def test_identified_identity_slug_group_and_envelope_attribution(tmp_path, capsys):
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z"),
               _rec("2026-01-02T00:00:00Z", unit="/speckit.implement")]
    pkg = _make_package(ws, records, project="cws-lib-python")

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["ingested"] == 2
    assert payload["groups_touched"] == 1
    groups = _groups(ws)
    assert len(groups) == 1
    expected_group = fu._source_slug(
        "cws-lib-python", fu._identity_key(records[0], "cws-lib-python"))
    assert groups[0].name == expected_group  # D5: slug + identity hash8
    assert SLUG_GROUP_FORM.match(groups[0].name)

    envelopes = sorted((groups[0] / "records").glob("*.json"))
    assert len(envelopes) == 2
    by_record = {json.loads(p.read_text(encoding="utf-8"))["record"]["unit_id"]:
                 json.loads(p.read_text(encoding="utf-8")) for p in envelopes}
    for record in records:
        envelope = by_record[record["unit_id"]]
        env = envelope["aggregation_envelope"]
        assert envelope["record"] == record  # verbatim, zero-drop (C-14/C-15)
        assert env["source_project"] == "cws-lib-python"
        assert env["package_file"] == pkg.name  # bare zip filename (E6)
        assert env["identity_key"] == fu._identity_key(record, "cws-lib-python")
        assert env["content_hash"] == fu._content_hash(record)


# --------------------------------------------------------------------------- #
# C-13 / FR-008: idempotency, cross-package overlap, keep-first conflicts
# --------------------------------------------------------------------------- #
def test_duplicate_ingest_idempotent(tmp_path, capsys):
    ws = tmp_path
    records = [_rec("2026-01-01T00:00:00Z"), _rec("2026-01-02T00:00:00Z")]
    pkg = _make_package(ws, records)

    first, rc1 = _ingest(ws, pkg, capsys)
    assert rc1 == 0
    assert first["ingested"] == 2
    landed = {p: p.read_bytes() for p in _flat_records(ws)}

    second, rc2 = _ingest(ws, pkg, capsys)

    assert rc2 == 0
    assert second["ingested"] == 0
    assert second["duplicates_skipped"] == second["record_count"] == 2  # 全量幂等
    assert second["identity_conflicts"] == 0
    assert _flat_records(ws) and all(p.read_bytes() == landed[p]
                                     for p in landed)  # envelopes immutable


def test_cross_package_overlap_dedup(tmp_path, capsys):
    # US2-4: two different packages carrying overlapping records (full
    # inclusion strategy) merge idempotently by source-record identity.
    ws = tmp_path
    shared = _rec("2026-01-02T00:00:00Z")
    pkg_a = _make_package(ws, [_rec("2026-01-01T00:00:00Z"), shared],
                          name="pkg-a.zip")
    pkg_b = _make_package(ws, [dict(shared), _rec("2026-01-03T00:00:00Z")],
                          name="pkg-b.zip")

    first, _ = _ingest(ws, pkg_a, capsys)
    assert first["ingested"] == 2
    second, rc = _ingest(ws, pkg_b, capsys)

    assert rc == 0
    assert second["ingested"] == 1  # only the genuinely new record
    assert second["duplicates_skipped"] == 1  # the shared one
    assert second["identity_conflicts"] == 0
    assert len(_flat_records(ws)) == 3


def test_same_identity_different_content_keep_first(tmp_path, capsys):
    # F-01 remediation: identity_key excludes content, so the same-key /
    # different-content branch MUST be constructible; keep-first, count it.
    ws = tmp_path
    original = _rec("2026-01-01T00:00:00Z")
    conflicting = dict(original, schema_version=1, pad="changed-content")
    pkg_first = _make_package(ws, [original], name="first.zip")
    pkg_second = _make_package(ws, [conflicting], name="second.zip")

    first, _ = _ingest(ws, pkg_first, capsys)
    assert first["ingested"] == 1
    kept_path = _flat_records(ws)[0]
    kept_before = kept_path.read_bytes()

    second, rc = _ingest(ws, pkg_second, capsys)

    assert rc == 0  # a conflict is a counted degradation, not a failure
    assert second["ingested"] == 0
    assert second["duplicates_skipped"] == 0  # not a duplicate: different content
    assert second["identity_conflicts"] == 1
    assert kept_path.read_bytes() == kept_before  # keep-first: no overwrite
    kept = json.loads(kept_path.read_text(encoding="utf-8"))
    assert kept["record"] == original
    assert kept["aggregation_envelope"]["content_hash"] == fu._content_hash(original)


# --------------------------------------------------------------------------- #
# C-13/C-14: one flock critical section, entry_filename() form, atomic writes
# --------------------------------------------------------------------------- #
def test_dedup_and_write_share_one_flock_critical_section(tmp_path, capsys):
    # While aggregated/.write.lock is held, ingest MUST NOT complete: the
    # duplicate check and the write share one flock critical section (C-13).
    ws = tmp_path
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z",
                                   unit="custom:conc/probe-1")])
    lock_path = _agg(ws) / ".write.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    done = threading.Event()
    outcome = {}

    def worker():
        try:
            outcome["rc"] = fu.main([
                "--action", "ingest-exec-quant", "--package", str(pkg),
                "--workspace-root", str(ws), "--format", "json"])
        except BaseException as exc:  # surface the real (red-phase) cause
            outcome["error"] = exc
        finally:
            done.set()

    with lock_path.open("a+", encoding="utf-8") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        blocked_as_expected = not done.wait(0.5)
        fcntl.flock(guard, fcntl.LOCK_UN)
    assert done.wait(15), "ingest did not finish after the lock was released"
    thread.join(timeout=5)
    if "error" in outcome:
        raise outcome["error"]
    assert blocked_as_expected, (
        "ingest completed while aggregated/.write.lock was held — the "
        "duplicate check and the write must share one flock critical section "
        "(C-13)")
    assert outcome["rc"] == 0
    assert lock_path.exists()  # the lock file lives at aggregated/.write.lock


def test_envelope_files_entry_filename_form_and_no_residue(tmp_path, capsys):
    # C-14: envelope filenames use the entry_filename() form
    # (timestamp-uuid8), decoupled from the source member names; the atomic
    # tmp+rename write leaves no residue beside the entries.
    ws = tmp_path
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z")])

    _, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    files = _flat_records(ws)
    assert len(files) == 1
    assert ENTRY_FORM.match(files[0].name)
    assert files[0].name != "0000.json"  # decoupled from the source name
    siblings = [p.name for p in files[0].parent.iterdir()]
    assert all(ENTRY_FORM.match(name) for name in siblings)  # zero .tmp residue


# --------------------------------------------------------------------------- #
# C-16: output keys and the exit-code ladder
# --------------------------------------------------------------------------- #
def test_output_json_required_keys_and_types(tmp_path, capsys):
    ws = tmp_path
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z")])

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert REQUIRED_OUTPUT_KEYS <= set(payload.keys())  # C-16 MUST contain
    assert isinstance(payload["manifest_unreadable"], bool)
    for key in ("record_count", "ingested", "duplicates_skipped",
                "skipped_unreadable", "identity_conflicts", "groups_touched"):
        assert isinstance(payload[key], int)


def test_nonexistent_package_file_exit_2(tmp_path):
    # C-16: the action as a whole is not executable → exit 2
    rc = fu.main(["--action", "ingest-exec-quant",
                  "--package", str(tmp_path / "no-such.zip"),
                  "--workspace-root", str(tmp_path), "--format", "json"])
    assert rc == 2


def test_non_zip_file_exit_2(tmp_path):
    bogus = tmp_path / "not-a-zip.zip"
    bogus.write_text("this is not a zip archive", encoding="utf-8")
    rc = fu.main(["--action", "ingest-exec-quant", "--package", str(bogus),
                  "--workspace-root", str(tmp_path), "--format", "json"])
    assert rc == 2


def test_storage_unwritable_exit_2(tmp_path, capsys):
    # The aggregated layer cannot be created (its parent path is a regular
    # file) → the action is not executable → exit 2, counted as an error and
    # never as a silent degradation.
    ws = tmp_path
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z")])
    store = ws / ".specify" / "memory" / "exec-quant"
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text("blocks aggregated/ creation", encoding="utf-8")

    rc = fu.main(["--action", "ingest-exec-quant", "--package", str(pkg),
                  "--workspace-root", str(ws), "--format", "json"])

    assert rc == 2
    assert "error" in capsys.readouterr().err.lower()


# --------------------------------------------------------------------------- #
# C-14 / C-10: storage boundary — feedback face untouched, zero contamination
# --------------------------------------------------------------------------- #
def test_feedback_store_untouched_no_contamination(tmp_path, capsys):
    ws = tmp_path
    feedback_store = ws / ".specify" / "memory" / "feedback"
    feedback_store.mkdir(parents=True)
    entry = feedback_store / "20260101T000000Z-speckit-plan.md"
    entry.write_text("# feedback entry (pre-existing)\n", encoding="utf-8")
    probe_unit = "custom:zero/leak-probe"
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z", unit=probe_unit)],
                        extra_members={
                            "SUBMISSION-NOTES.md": "submission notes\n",
                            "introspection/20260101T000000Z.md": "report\n",
                            "20260101T000100Z-speckit-plan.md": "entry member\n"})
    before = _snapshot(feedback_store)

    payload, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert payload["ingested"] == 1
    assert _snapshot(feedback_store) == before  # zero touch, zero new files
    # exec-quant records MUST NOT enter the feedback store (C-14 / 059 FR-009)
    for path in feedback_store.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert probe_unit not in text
            assert STR001 not in text


def test_ingest_does_not_trigger_aggregate(tmp_path, capsys):
    # C-17: ingest MUST NOT trigger aggregate — no summaries/ appears, ever.
    ws = tmp_path
    pkg = _make_package(ws, [_rec("2026-01-01T00:00:00Z"),
                             _rec("2026-01-02T00:00:00Z")])

    _, rc = _ingest(ws, pkg, capsys)

    assert rc == 0
    assert not (_agg(ws) / "summaries").exists()
    assert len(_flat_records(ws)) == 2  # only the envelopes landed
