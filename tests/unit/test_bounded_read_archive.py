"""Unit tests: bounded reads of an inbound feedback archive (zip-bomb surface).

Port family: upstream ``118062eac`` ("harden: secure extension and preset
archive downloads") — its bounded ZIP member read, safe-member validation and
central-directory preflight, adapted to what ``feedback-utils.py`` actually does
with a package: read members into memory, never extract.

Subject is the framework source ``scripts/python/feedback-utils.py`` (loaded via
``tests/script_api``), never the ``.specify/`` mirror (two-hats rule).

The contract this port must NOT break is the 068 intake leg
(``.specify/specs/068-exec-quant-feedback-channel/contracts/intake-contract.md``):

* C-11 / FR-010 — an unreadable member is a non-blocking ``skipped_unreadable``
  count, so an over-limit or unsafe-named member degrades the same way and the
  action still completes with exit 0;
* C-12 — a manifest that cannot be read degrades to ``manifest_unreadable`` and
  the ``unknown-project`` group, never a guess;
* C-16 — the seven-key output face is unchanged, and exit 2 stays reserved for
  "the action as a whole is not executable" (here: an archive whose structure is
  over its ceiling, the same class as a zip that will not open).

Ceilings are exercised two ways: at their real declared values (an oversized
member is refused by its *declared* size, so nothing inflates), and with the
module constant monkeypatched small — the pattern the sibling payload tests
already use — so a bomb fixture never has to be gigabytes to prove the bound.

Red-first evidence: /tmp/speckit-p1/redfirst-d-before.txt (a 512 MiB member in a
522 KB package drove peak RSS to 1044 MiB before this port; 0 MiB growth after).
"""
from __future__ import annotations

import io
import json
import struct
import zipfile
from pathlib import Path

import pytest

from tests.script_api import ROOT, feedback_utils as fu

RECORDS_PREFIX = f"{fu.PAYLOAD_DIRNAME}/{fu.PAYLOAD_RECORDS_DIRNAME}/"
MANIFEST_NAME = f"{fu.PAYLOAD_DIRNAME}/{fu.PAYLOAD_MANIFEST_NAME}"
INTAKE_KEYS = {"record_count", "ingested", "duplicates_skipped",
               "skipped_unreadable", "identity_conflicts", "groups_touched",
               "manifest_unreadable"}


# --------------------------------------------------------------------------- #
# fixture helpers (all self-constructed)
# --------------------------------------------------------------------------- #
def _record(run: str = "r1", **extra) -> dict:
    record = {"kind": fu.RECORD_KIND, "schema_version": 2,
              "unit_id": "/speckit.plan", "unit_type": "command",
              "run_id": run, "collected_at": "2026-01-01T00:00:00Z"}
    record.update(extra)
    return record


def _manifest(project: str = "probe-project", pad: int = 0) -> bytes:
    return json.dumps({"kind": fu.PAYLOAD_KIND,
                       "schema_version": fu.PAYLOAD_SCHEMA_VERSION,
                       "pad": "x" * pad,
                       "identity": {"project_name": project,
                                    "source_commit": None,
                                    "identity_status": "identified"}}).encode()


def _package(path: Path, members) -> Path:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, raw in members:
            zf.writestr(name, raw)
    return path


def _bomb_member(size: int) -> bytes:
    """A member whose *declared* size is huge but whose bytes are tiny."""
    return b"0" * size


def _ingest(tmp_path: Path, package: Path, capsys):
    workspace = tmp_path / "ws"
    workspace.mkdir(exist_ok=True)
    rc = fu.main(["--action", "ingest-exec-quant", "--package", str(package),
                  "--workspace-root", str(workspace), "--format", "json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out) if captured.out.strip() else None
    return rc, payload, captured.err, workspace


def _envelopes(workspace: Path):
    aggregated = (workspace / fu.EXEC_QUANT_STORAGE_REL / fu.AGGREGATED_DIRNAME)
    if not aggregated.is_dir():
        return []
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(aggregated.glob("*/records/*.json"))]


class _LyingArchive:
    """An archive whose declared size is small but whose stream is huge.

    CPython's ``zipfile`` trusts the central directory, so this differential is
    built by hand: it is the case the chunked read exists for, and it records
    every request size so the bound can be asserted on what was actually pulled.
    """

    def __init__(self, declared: int, data: bytes):
        self.info = zipfile.ZipInfo("exec-quant/records/liar.json")
        self.info.file_size = declared
        self.stream = io.BytesIO(data)
        self.requests: list[int] = []

    def getinfo(self, name):
        return self.info

    def open(self, name, mode="r"):
        outer = self

        class _SpyStream:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self, size=-1):
                outer.requests.append(size)
                return outer.stream.read(size)

        return _SpyStream()


def _as_zip64(path: Path) -> Path:
    """Rewrite a small zip's EOCD to the zip64 escape markers + a real EOCD64.

    A genuine >65535-entry archive is too expensive for a unit test; the escape
    markers are what select the code path, so they are written directly and the
    result is verified to still be a zip ``zipfile`` itself accepts.
    """
    raw = path.read_bytes()
    index = raw.rfind(b"PK\x05\x06")
    assert index >= 0
    fields = struct.unpack_from("<4s4H2LH", raw, index)
    entries, central_size, central_offset = fields[4], fields[5], fields[6]
    assert fields[7] == 0, "fixture must carry no EOCD comment"
    eocd64 = struct.pack("<4sQ2H2L4Q", b"PK\x06\x06", 44, 45, 45, 0, 0,
                         entries, entries, central_size, central_offset)
    locator = struct.pack("<4sLQL", b"PK\x06\x07", 0, index, 1)
    escaped = struct.pack("<4s4H2LH", b"PK\x05\x06", 0, 0, 0xFFFF, 0xFFFF,
                          0xFFFFFFFF, central_offset, 0)
    path.write_bytes(raw[:index] + eocd64 + locator + escaped)
    return path


# --------------------------------------------------------------------------- #
# subject guard + the declared bounds
# --------------------------------------------------------------------------- #
def test_subject_is_framework_source_engine():
    assert (Path(fu.__file__).resolve()
            == (ROOT / "scripts" / "python" / "feedback-utils.py").resolve())


def test_archive_ceilings_are_declared_once_in_the_engine():
    # drift pins (a literal in a test is a sanctioned duplicate of the owner)
    assert fu.MAX_ARCHIVE_MEMBER_BYTES == 1 * 1024 * 1024
    assert fu.MAX_ARCHIVE_ENTRIES == 4096
    assert fu.MAX_ARCHIVE_CENTRAL_BYTES == 4 * 1024 * 1024
    assert fu.MAX_ARCHIVE_PATH_BYTES == 4096
    assert fu.MAX_ARCHIVE_COMPONENT_BYTES == 255
    assert fu.ARCHIVE_READ_CHUNK_BYTES == 64 * 1024
    # the total payload allowance is the package leg's own cap, not a second one
    assert fu.MAX_PAYLOAD_BYTES == 16 * 1024 * 1024


# --------------------------------------------------------------------------- #
# per-member ceiling: a bomb degrades, it never inflates and never blocks
# --------------------------------------------------------------------------- #
def test_oversize_declared_member_is_skipped_and_the_action_completes(tmp_path, capsys):
    # real default ceiling: the member declares twice the per-member cap, so it
    # is refused on its declaration — no inflation, no monkeypatch needed.
    oversize = fu.MAX_ARCHIVE_MEMBER_BYTES * 2
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
        (RECORDS_PREFIX + "bomb.json", _bomb_member(oversize)),
    ])
    assert package.stat().st_size < oversize // 100  # tiny on disk, huge declared
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err  # C-11: a payload problem never blocks the action
    assert set(payload) == INTAKE_KEYS  # C-16: the output face is unchanged
    assert payload["record_count"] == 2
    assert payload["skipped_unreadable"] == 1
    assert payload["ingested"] == 1
    assert payload["manifest_unreadable"] is False
    assert len(_envelopes(workspace)) == 1


def test_bomb_member_is_refused_without_inflating_past_the_ceiling(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fu, "MAX_ARCHIVE_MEMBER_BYTES", 4096)
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
        (RECORDS_PREFIX + "bomb.json", _bomb_member(1024 * 1024)),
    ])
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["skipped_unreadable"] == 1
    assert payload["ingested"] == 1
    assert len(_envelopes(workspace)) == 1


def test_lying_declared_size_is_still_bounded_by_the_chunked_read():
    archive = _LyingArchive(declared=16, data=b"x" * 100000)
    with pytest.raises(fu.FeedbackError):
        fu._read_archive_member_limited(archive, "m", 1024)
    # only limit + 1 bytes were ever pulled, in bounded requests
    assert archive.stream.tell() == 1025
    assert archive.requests and max(archive.requests) <= fu.ARCHIVE_READ_CHUNK_BYTES


def test_member_read_returns_exact_bytes_within_the_ceiling():
    data = json.dumps(_record()).encode()
    archive = _LyingArchive(declared=len(data), data=data)
    assert fu._read_archive_member_limited(archive, "m", len(data)) == data


def test_remaining_budget_tightens_the_per_member_ceiling():
    data = b"x" * 500
    archive = _LyingArchive(declared=len(data), data=data)
    with pytest.raises(fu.FeedbackError):
        fu._read_archive_member_limited(archive, "m", 4096, budget=100)
    assert archive.stream.tell() == 0  # refused on the declaration, before reading


def test_total_payload_budget_stops_reading_and_counts_the_rest(tmp_path, monkeypatch, capsys):
    records = [(RECORDS_PREFIX + f"r{i}.json",
                json.dumps(_record(run=f"r{i}", pad="x" * 400)).encode())
               for i in range(8)]
    monkeypatch.setattr(fu, "MAX_PAYLOAD_BYTES", 1200)
    package = _package(tmp_path / "pkg.zip", [(MANIFEST_NAME, _manifest()), *records])
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["record_count"] == 8  # every member is still counted
    assert payload["ingested"] + payload["skipped_unreadable"] == 8
    assert payload["skipped_unreadable"] > 0  # the budget ran out
    assert payload["ingested"] == len(_envelopes(workspace))
    # the manifest has its own ceiling: it does not eat the record budget
    assert payload["manifest_unreadable"] is False


def test_oversize_manifest_degrades_to_unknown_project(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fu, "MAX_ARCHIVE_MEMBER_BYTES", 256)
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest(pad=400)),  # over the ceiling; the record fits
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
    ])
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["manifest_unreadable"] is True
    assert payload["ingested"] == 1
    envelopes = _envelopes(workspace)
    assert envelopes[0]["aggregation_envelope"]["identity_status"] == fu.UNKNOWN_PROJECT


# --------------------------------------------------------------------------- #
# safe member names
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", [
    "exec-quant/records/../../evil.json",
    "exec-quant/records/./evil.json",
    "exec-quant//records/evil.json",
    "exec-quant/records/../evil.json",
    "exec-quant/records/evil.json//",
    # A NUL in a member name is covered by the predicate table below, not here:
    # zipfile itself truncates a written filename at the NUL, so the hostile
    # name cannot reach the engine through a zipfile-produced archive.
    "exec-quant/records/ev\til.json",
    "exec-quant/records/evil.json ",
    "exec-quant/records/evil.json.",
    "exec-quant/records/ evil.json",
    "exec-quant/records/ev<il.json",
    "exec-quant/records/ev|il.json",
    "exec-quant/records\\..\\evil.json",
    "exec-quant/records/" + "n" * 256 + ".json",
    "exec-quant/" + "d/" * 3000 + "evil.json",
])
def test_unsafe_member_name_is_not_ingested(tmp_path, capsys, name):
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
        (name, json.dumps(_record(run="hostile")).encode()),
    ])
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["record_count"] == 2
    assert payload["skipped_unreadable"] == 1
    assert payload["ingested"] == 1
    assert [e["record"]["run_id"] for e in _envelopes(workspace)] == ["r1"]


@pytest.mark.parametrize("name,expected", [
    ("exec-quant/records/a.json", True),
    ("exec-quant/records/", True),          # the one-slash directory marker
    ("exec-quant/records/sub/a.json", True),
    ("exec-quant/records/中文.json", True),  # non-ASCII is portable
    ("", False),
    ("/exec-quant/records/a.json", False),
    ("C:/exec-quant/records/a.json", False),
    ("exec-quant/records/a.json/", True),   # ONE trailing slash is a directory marker
    ("exec-quant/records/a.json//", False),
    ("exec-quant/records//a.json", False),
    ("exec-quant/records/.", False),
    ("exec-quant/records/..", False),
    ("exec-quant/records/a\x00.json", False),
    ("exec-quant/records/a\u0085.json", False),  # C1 control
    ("exec-quant/records/" + "n" * 256, False),
])
def test_safe_member_name_predicate(name, expected):
    assert fu._is_safe_member_name(name) is expected


# --------------------------------------------------------------------------- #
# structural ceilings: the archive as a whole is refused (exit 2), zero writes
# --------------------------------------------------------------------------- #
def test_member_ceiling_refuses_the_archive_before_any_write(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fu, "MAX_ARCHIVE_ENTRIES", 3)
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        *[(RECORDS_PREFIX + f"r{i}.json", json.dumps(_record(run=f"r{i}")).encode())
          for i in range(5)],
    ])
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 2
    assert payload is None
    assert "ceiling" in err
    assert not (workspace / fu.EXEC_QUANT_STORAGE_REL).exists()  # zero storage touch


def test_central_directory_ceiling_is_checked_before_zipfile_allocates(tmp_path, monkeypatch):
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
    ])
    monkeypatch.setattr(fu, "MAX_ARCHIVE_CENTRAL_BYTES", 8)

    def _must_not_allocate(*args, **kwargs):
        raise AssertionError("ZipFile was constructed before the preflight refused")

    monkeypatch.setattr(fu.zipfile, "ZipFile", _must_not_allocate)
    with pytest.raises(fu.FeedbackError) as excinfo:
        fu._preflight_archive_bounds(package, "probe")
    assert "central directory" in str(excinfo.value)


def test_preflight_reads_the_eocd_through_a_benign_comment(tmp_path, monkeypatch):
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
    ])
    with zipfile.ZipFile(package, "a") as zf:
        zf.comment = b"an ordinary archive comment" * 20
    # the count is read through the comment: tightening the ceiling must refuse
    monkeypatch.setattr(fu, "MAX_ARCHIVE_ENTRIES", 1)
    with pytest.raises(fu.FeedbackError) as excinfo:
        fu._preflight_archive_bounds(package, "probe")
    assert "2 members" in str(excinfo.value)


def test_fake_eocd_signature_in_a_comment_declines_instead_of_false_refusing(tmp_path, capsys):
    package = _package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
    ])
    with zipfile.ZipFile(package, "a") as zf:
        zf.comment = b"decoy PK\x05\x06 signature inside the comment" * 4
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    # The decoy makes the tail ambiguous for zipfile too, so the archive is
    # genuinely unreadable. What matters is WHICH refusal the user sees: the
    # preflight must decline (fail-open) and leave zipfile's own verdict intact,
    # never invent a ceiling refusal for an archive it could not read.
    assert rc == 2
    assert "not a readable zip" in err
    assert "ceiling" not in err


def test_zip64_archive_is_preflighted_and_still_ingests(tmp_path, monkeypatch, capsys):
    package = _as_zip64(_package(tmp_path / "pkg.zip", [
        (MANIFEST_NAME, _manifest()),
        (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode()),
    ]))
    with zipfile.ZipFile(package) as zf:  # the fixture is a zip zipfile accepts
        assert len(zf.namelist()) == 2
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["ingested"] == 1
    # the zip64 branch really is the one deciding: tighten the ceiling and the
    # EOCD64 declaration (2 members) must be what refuses it
    monkeypatch.setattr(fu, "MAX_ARCHIVE_ENTRIES", 1)
    with pytest.raises(fu.FeedbackError) as excinfo:
        fu._preflight_archive_bounds(package, "probe")
    assert "2 members" in str(excinfo.value)


def test_not_a_zip_keeps_the_existing_refusal_message(tmp_path, capsys):
    bogus = tmp_path / "bogus.zip"
    bogus.write_bytes(b"this is not a zip at all")
    rc, payload, err, workspace = _ingest(tmp_path, bogus, capsys)
    assert rc == 2
    assert "not a readable zip" in err


def test_package_larger_than_the_payload_record_cap_is_not_refused(tmp_path, capsys):
    # the archive ceiling counts EVERY member, so a package carrying more
    # feedback entries than the payload record cap must still be accepted
    members = [(MANIFEST_NAME, _manifest()),
               (RECORDS_PREFIX + "ok.json", json.dumps(_record()).encode())]
    members += [(f"feedback/e{i}.md", b"# entry\n") for i in range(1200)]
    assert len(members) > fu.MAX_PAYLOAD_RECORDS
    package = _package(tmp_path / "pkg.zip", members)
    rc, payload, err, workspace = _ingest(tmp_path, package, capsys)
    assert rc == 0, err
    assert payload["ingested"] == 1
    assert payload["record_count"] == 1  # non-payload members are not records


# --------------------------------------------------------------------------- #
# cleanup: names only, same structural bounds, nothing removed on refusal
# --------------------------------------------------------------------------- #
def _cleanup_fixture(tmp_path):
    workspace = tmp_path / "ws"
    store = workspace / fu.FEEDBACK_SUBDIR
    store.mkdir(parents=True)
    (store / "20260101T000000Z-unit.md").write_text(
        "---\nid: e1\nunit_id: /speckit.plan\n---\nbody\n", encoding="utf-8")
    package = _package(tmp_path / "pkg.zip", [
        ("MANIFEST.md", b"# manifest\n"),
        ("20260101T000000Z-unit.md", b"body\n"),
    ])
    return workspace, store, package


def test_cleanup_over_ceiling_archive_removes_nothing(tmp_path, monkeypatch, capsys):
    workspace, store, package = _cleanup_fixture(tmp_path)
    monkeypatch.setattr(fu, "MAX_ARCHIVE_ENTRIES", 1)
    rc = fu.main(["--action", "cleanup", "--package", str(package),
                  "--workspace-root", str(workspace), "--format", "json"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "ceiling" in err
    assert (store / "20260101T000000Z-unit.md").is_file()  # nothing removed


def test_cleanup_happy_path_is_unchanged(tmp_path, capsys):
    workspace, store, package = _cleanup_fixture(tmp_path)
    rc = fu.main(["--action", "cleanup", "--package", str(package),
                  "--workspace-root", str(workspace), "--format", "json"])
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    payload = json.loads(captured.out)
    assert payload["removed"] == ["e1"]
    assert not (store / "20260101T000000Z-unit.md").exists()


# --------------------------------------------------------------------------- #
# script interface contract: the help face projects the bounds it enforces
# --------------------------------------------------------------------------- #
def test_package_help_projects_the_ceilings_and_the_over_limit_behaviour():
    help_text = fu.build_parser().format_help()
    for constant in (fu.MAX_ARCHIVE_MEMBER_BYTES, fu.MAX_PAYLOAD_BYTES,
                     fu.MAX_ARCHIVE_ENTRIES, fu.MAX_ARCHIVE_CENTRAL_BYTES):
        assert str(constant) in help_text
    assert "skipped_unreadable" in help_text
    assert "exit 0" in help_text and "exit 2" in help_text