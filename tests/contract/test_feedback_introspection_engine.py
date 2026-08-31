"""Contract test: introspect-register engine action (req 047).

Pins contracts/engine-cli.md C-1..C-6 / C-15 (register path) against
`feedback_utils --action introspect-register`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.contract.helpers_introspection import _record, _report_text, _write_report
from tests.script_api import feedback_utils


def _index(workspace: Path) -> dict:
    return json.loads(
        (workspace / ".specify/memory/feedback/index.json").read_text())


def _register(workspace: Path, report_path: Path, *extra: str) -> int:
    return feedback_utils.main([
        "--action", "introspect-register", "--workspace-root", str(workspace),
        "--report-file", str(report_path), *extra,
    ])


@pytest.mark.contract
class TestRegisterValidation:
    """C-1/C-15: violations → exit 2, violations listed, nothing written."""

    def test_invalid_report_exit_2_and_no_writes(self, feedback_store: Path, capsys):
        eid = _record(feedback_store, "reg-a")
        report_id = "introspection-20260828T010000Z"
        # missing 根因 → structural violation
        text = _report_text(report_id, [eid]).replace("- **根因**: 根因陈述\n", "")
        path = _write_report(feedback_store, report_id, text)
        capsys.readouterr()
        rc = _register(feedback_store, path)
        assert rc == 2
        assert "C-9" in capsys.readouterr().err
        assert _index(feedback_store).get("introspections", []) == []
        entry = _index(feedback_store)["entries"][0]
        assert not entry.get("introspection_ref")


@pytest.mark.contract
class TestRegisterLinking:
    """C-2: draft register links entries and records the report."""

    def test_register_links_entries_and_records(self, feedback_store: Path):
        e1 = _record(feedback_store, "reg-b")
        e2 = _record(feedback_store, "reg-c")
        report_id = "introspection-20260828T010100Z"
        path = _write_report(feedback_store, report_id,
                             _report_text(report_id, [e1, e2]))
        rc = _register(feedback_store, path)
        assert rc == 0
        index = _index(feedback_store)
        reports = index.get("introspections", [])
        assert [r["id"] for r in reports] == [report_id]
        assert reports[0]["status"] == "draft"
        assert sorted(reports[0]["entries"]) == sorted([e1, e2])
        for entry in index["entries"]:
            assert entry.get("introspection_ref") == f"{report_id}#F-01"
        # entry frontmatter mirrors the link (body untouched)
        entry_file = feedback_store / ".specify/memory/feedback" / index["entries"][0]["file"]
        assert f'introspection_ref: "{report_id}#F-01"' in entry_file.read_text()
        assert "## Review" in entry_file.read_text()

    def test_register_json_output_shape(self, feedback_store: Path, capsys):
        e1 = _record(feedback_store, "reg-d")
        report_id = "introspection-20260828T010200Z"
        path = _write_report(feedback_store, report_id,
                             _report_text(report_id, [e1]))
        capsys.readouterr()
        rc = _register(feedback_store, path, "--format", "json")
        assert rc == 0
        out = json.loads(capsys.readouterr().out)
        assert out["report_id"] == report_id
        assert out["linked"] == 1
        assert out["disposed"] == 0
        assert out["superseded"] is None


@pytest.mark.contract
class TestRegisterIdempotencyAndSupersede:
    """C-4 idempotent re-register; C-10 supersede flips the old report."""

    def test_reregister_updates_in_place(self, feedback_store: Path):
        e1 = _record(feedback_store, "reg-e")
        report_id = "introspection-20260828T010300Z"
        path = _write_report(feedback_store, report_id,
                             _report_text(report_id, [e1]))
        assert _register(feedback_store, path) == 0
        assert _register(feedback_store, path) == 0
        reports = _index(feedback_store).get("introspections", [])
        assert [r["id"] for r in reports] == [report_id]

    def test_supersede_flips_old_report(self, feedback_store: Path):
        e1 = _record(feedback_store, "reg-f")
        old_id = "introspection-20260828T010400Z"
        old_path = _write_report(feedback_store, old_id, _report_text(old_id, [e1]))
        assert _register(feedback_store, old_path) == 0
        new_id = "introspection-20260828T010500Z"
        new_path = _write_report(feedback_store, new_id,
                                 _report_text(new_id, [e1], supersedes=old_id))
        capsys_rc = _register(feedback_store, new_path)
        assert capsys_rc == 0
        reports = {r["id"]: r for r in _index(feedback_store)["introspections"]}
        assert reports[old_id]["status"] == "superseded"
        assert reports[new_id]["status"] == "draft"
        # old report file frontmatter flipped, body intact
        old_meta, old_body = feedback_utils.parse_frontmatter(
            old_path.read_text(encoding="utf-8"))
        assert old_meta["status"] == "superseded"
        assert "## Findings" in old_body


@pytest.mark.contract
class TestDisposeExtension:
    """engine-cli C-7/C-8: dispose --reason/--ref, zero regression without."""

    def test_dispose_without_new_flags_byte_compatible(self, feedback_store: Path):
        eid = _record(feedback_store, "disp-a")
        rc = feedback_utils.main([
            "--action", "dispose", "--workspace-root", str(feedback_store),
            "--id", eid, "--to", "processed"])
        assert rc == 0
        entry = _index(feedback_store)["entries"][0]
        assert entry["disposition"] == "processed"
        assert not entry.get("introspection_ref")
        assert not entry.get("disposition_reason")
        entry_file = feedback_store / ".specify/memory/feedback" / entry["file"]
        text = entry_file.read_text(encoding="utf-8")
        assert "introspection_ref" not in text
        assert "disposition_reason" not in text

    def test_dispose_with_reason_and_ref(self, feedback_store: Path):
        eid = _record(feedback_store, "disp-b")
        rc = feedback_utils.main([
            "--action", "dispose", "--workspace-root", str(feedback_store),
            "--id", eid, "--to", "ignored",
            "--reason", "introspection:introspection-20260828T020000Z#F-01",
            "--ref", "introspection-20260828T020000Z#F-01"])
        assert rc == 0
        entry = _index(feedback_store)["entries"][0]
        assert entry["disposition"] == "ignored"
        assert entry["disposition_reason"].startswith("introspection:")
        assert entry["introspection_ref"] == "introspection-20260828T020000Z#F-01"

    def test_dispose_ref_format_rejected(self, feedback_store: Path, capsys):
        eid = _record(feedback_store, "disp-c")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "dispose", "--workspace-root", str(feedback_store),
            "--id", eid, "--to", "processed", "--ref", "bogus-ref"])
        assert rc == 2


@pytest.mark.contract
class TestRegisterConfirm:
    """engine-cli C-3/C-5: --confirm applies batch dispositions from 建议处置."""

    def test_confirm_applies_suggestions_and_flips_status(self, feedback_store: Path):
        e1 = _record(feedback_store, "conf-a")
        e2 = _record(feedback_store, "conf-b")
        report_id = "introspection-20260828T020100Z"
        text = _report_text(report_id, [e1, e2], findings_extra=(
            f"- **建议处置**: {e1}:processed, {e2}:ignored\n"))
        path = _write_report(feedback_store, report_id, text)
        assert _register(feedback_store, path) == 0
        # draft register alone does not dispose
        for entry in _index(feedback_store)["entries"]:
            assert not entry.get("disposition")
        rc = _register(feedback_store, path, "--confirm")
        assert rc == 0
        index = _index(feedback_store)
        by_id = {e["id"]: e for e in index["entries"]}
        assert by_id[e1]["disposition"] == "processed"
        assert by_id[e2]["disposition"] == "ignored"
        assert by_id[e1]["disposition_reason"].startswith("introspection:")
        reports = {r["id"]: r for r in index["introspections"]}
        assert reports[report_id]["status"] == "confirmed"
        meta, _body = feedback_utils.parse_frontmatter(path.read_text(encoding="utf-8"))
        assert meta["status"] == "confirmed"
        assert meta["confirmed_at"]

    def test_confirm_without_suggestions_flips_status_only(self, feedback_store: Path):
        e1 = _record(feedback_store, "conf-c")
        report_id = "introspection-20260828T020200Z"
        path = _write_report(feedback_store, report_id, _report_text(report_id, [e1]))
        assert _register(feedback_store, path) == 0
        assert _register(feedback_store, path, "--confirm") == 0
        entry = _index(feedback_store)["entries"][0]
        assert not entry.get("disposition")

    def test_confirmed_report_reregister_does_not_reopen(self, feedback_store: Path):
        e1 = _record(feedback_store, "conf-d")
        report_id = "introspection-20260828T020300Z"
        text = _report_text(report_id, [e1], findings_extra=f"- **建议处置**: {e1}:processed\n")
        path = _write_report(feedback_store, report_id, text)
        assert _register(feedback_store, path) == 0
        assert _register(feedback_store, path, "--confirm") == 0
        # rewrite the file back to draft and re-register without --confirm:
        # index must keep confirmed, dispositions must not be reapplied
        write_text = path.read_text(encoding="utf-8").replace(
            'status: "confirmed"', 'status: "draft"')
        path.write_text(write_text, encoding="utf-8")
        entry = _index(feedback_store)["entries"][0]
        entry_file = feedback_store / ".specify/memory/feedback" / entry["file"]
        text_e = entry_file.read_text(encoding="utf-8")
        entry_file.write_text(
            text_e.replace('disposition: "processed"', 'disposition: ""'),
            encoding="utf-8")
        index = _index(feedback_store)
        index["entries"][0]["disposition"] = ""
        (feedback_store / ".specify/memory/feedback/index.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
        assert _register(feedback_store, path) == 0
        index = _index(feedback_store)
        assert index["introspections"][0]["status"] == "confirmed"
        assert index["entries"][0]["disposition"] == ""


@pytest.mark.contract
class TestPackageIncludeIntrospection:
    """engine-cli C-9..C-12: package --include-introspection."""

    def _setup_linked(self, workspace: Path, kind: str | None = None):
        eid = _record(workspace, "pkg-a", kind=kind)
        report_id = "introspection-20260828T030000Z"
        text = _report_text(report_id, [eid])
        if kind == "external":
            text = text.replace("upstream-bound(package-attachment)",
                                "local-sink(direct-fix)")
        path = _write_report(workspace, report_id, text)
        assert _register(workspace, path) == 0
        return eid, report_id

    def _latest_zip(self, workspace: Path) -> Path:
        zips = sorted(
            (workspace / ".specify/memory/feedback/packages").glob("*.zip"))
        assert zips
        return zips[-1]

    def test_include_adds_report_and_manifest_section(self, feedback_store: Path):
        _eid, report_id = self._setup_linked(feedback_store)
        rc = feedback_utils.main([
            "--action", "package", "--workspace-root", str(feedback_store),
            "--include-introspection"])
        assert rc == 0
        import zipfile
        with zipfile.ZipFile(self._latest_zip(feedback_store)) as z:
            names = z.namelist()
            assert f"introspection/{report_id}.md" in names
            manifest = z.read("MANIFEST.md").decode("utf-8")
        assert "## Introspection Reports" in manifest
        assert report_id in manifest

    def test_without_flag_zero_regression(self, feedback_store: Path):
        _eid, report_id = self._setup_linked(feedback_store)
        rc = feedback_utils.main([
            "--action", "package", "--workspace-root", str(feedback_store)])
        assert rc == 0
        import zipfile
        with zipfile.ZipFile(self._latest_zip(feedback_store)) as z:
            names = z.namelist()
            manifest = z.read("MANIFEST.md").decode("utf-8")
        assert not any(n.startswith("introspection/") for n in names)
        assert "## Introspection Reports" not in manifest

    def test_missing_report_marked_not_fatal(self, feedback_store: Path):
        _eid, report_id = self._setup_linked(feedback_store)
        # delete the report file after linking
        (feedback_store / ".specify/memory/feedback/introspection"
         / f"{report_id}.md").unlink()
        rc = feedback_utils.main([
            "--action", "package", "--workspace-root", str(feedback_store),
            "--include-introspection"])
        assert rc == 0
        import zipfile
        with zipfile.ZipFile(self._latest_zip(feedback_store)) as z:
            manifest = z.read("MANIFEST.md").decode("utf-8")
            names = z.namelist()
        assert "(missing)" in manifest
        assert f"introspection/{report_id}.md" not in names

    def test_external_only_report_never_packaged(self, feedback_store: Path):
        _eid, report_id = self._setup_linked(feedback_store, kind="external")
        rc = feedback_utils.main([
            "--action", "package", "--workspace-root", str(feedback_store),
            "--include-introspection"])
        assert rc == 0
        zdir = feedback_store / ".specify/memory/feedback/packages"
        if list(zdir.glob("*.zip")):
            import zipfile
            with zipfile.ZipFile(self._latest_zip(feedback_store)) as z:
                names = z.namelist()
            assert not any(n.startswith("introspection/") for n in names)
