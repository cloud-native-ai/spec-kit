"""Contract test: feedback-utils.py engine CLI probe extensions (req 041).

Pins ``.specify/specs/041-refactor-feedback-probe/contracts/engine-cli.md``:
C-7 ``--action map`` (deterministic whole-file rebuild of the probe map).
Later phases append cases here (cleanup C-5, migrate-legacy C-8, probe-inject
C-6, package exclusion C-4) — one test file per contract document.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

VALID_REGISTRY = """# Feedback Probe Definitions

## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| command-wrapup | internal | command run review | commands | record→package | wrap-up |
| skill-wrapup | internal | skill run review | skills | record→package | wrap-up |
| external-custom | external | custom unit review | host-custom | record→local | wrap-up |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| speckit-plan-wrapup | command-wrapup | /speckit.plan | wrap-up |
| skill-study-wrapup | skill-wrapup | skill:study-project | wrap-up |
"""


@pytest.fixture
def probe_workspace(tmp_path: Path) -> Path:
    defs = tmp_path / ".specify" / "shared" / "definitions"
    defs.mkdir(parents=True, exist_ok=True)
    (defs / "probe-definitions.md").write_text(VALID_REGISTRY, encoding="utf-8")
    store = tmp_path / ".specify" / "memory" / "feedback"
    store.mkdir(parents=True, exist_ok=True)
    (store / ".gitkeep").touch()
    return tmp_path


@pytest.mark.contract
class TestMapAction:
    def test_map_writes_probe_map_md(self, probe_workspace: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace),
        ])
        assert rc == 0
        assert (probe_workspace / ".specify" / "memory" / "feedback"
                / "probe-map.md").is_file()

    def test_map_is_deterministic_byte_identical(
        self, probe_workspace: Path, capsys
    ):
        capsys.readouterr()
        map_path = (probe_workspace / ".specify" / "memory" / "feedback"
                    / "probe-map.md")
        feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace)])
        first = map_path.read_bytes()
        feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace)])
        second = map_path.read_bytes()
        assert first == second

    def test_map_covers_all_classes_and_objects(
        self, probe_workspace: Path, capsys
    ):
        capsys.readouterr()
        feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace)])
        text = (probe_workspace / ".specify" / "memory" / "feedback"
                / "probe-map.md").read_text(encoding="utf-8")
        for needle in ("command-wrapup", "skill-wrapup", "external-custom",
                       "speckit-plan-wrapup", "skill-study-wrapup",
                       "/speckit.plan", "skill:study-project",
                       "internal", "record→package"):
            assert needle in text, f"map missing: {needle}"

    def test_map_contains_mermaid_block(self, probe_workspace: Path, capsys):
        capsys.readouterr()
        feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace)])
        text = (probe_workspace / ".specify" / "memory" / "feedback"
                / "probe-map.md").read_text(encoding="utf-8")
        assert "```mermaid" in text

    def test_map_json_output_shape(self, probe_workspace: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "map", "--format", "json",
            "--workspace-root", str(probe_workspace),
        ])
        assert rc == 0
        out = json.loads(capsys.readouterr().out)
        assert out["classes"] == 3
        assert out["objects"] == 2
        assert out["map"].endswith("probe-map.md")


def _record_entry(root: Path, unit_id: str, unit_type: str, run_id: str) -> int:
    return feedback_utils.main([
        "--action", "record", "--workspace-root", str(root),
        "--unit-id", unit_id, "--unit-type", unit_type,
        "--run-id", run_id, "--review", "review text", "--points", "a point",
    ])


@pytest.mark.contract
class TestListFiltersAndDispose:
    @pytest.fixture
    def mixed_workspace(self, probe_workspace: Path) -> Path:
        probes = (probe_workspace / ".specify" / "memory" / "feedback" / "probes")
        probes.mkdir(parents=True, exist_ok=True)
        (probes / "ext-myteam-deploy-wrapup.md").write_text(
            "---\nobject_id: ext-myteam-deploy-wrapup\n"
            "class_id: external-custom\nunit: custom:myteam/deploy-skill\n"
            "lifecycle_point: wrap-up\n---\n", encoding="utf-8")
        assert _record_entry(probe_workspace, "/speckit.plan", "command", "r1") == 0
        assert _record_entry(
            probe_workspace, "skill:study-project", "skill", "r2") == 0
        assert _record_entry(
            probe_workspace, "custom:myteam/deploy-skill", "custom-unit", "r3") == 0
        return probe_workspace

    def test_list_filter_by_slice(self, mixed_workspace: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "list", "--format", "json", "--limit", "0",
            "--slice", "commands", "--workspace-root", str(mixed_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["count"] == 1
        assert out["matches"][0]["unit_id"] == "/speckit.plan"

    def test_list_filter_by_kind_external(self, mixed_workspace: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "list", "--format", "json", "--limit", "0",
            "--kind", "external", "--workspace-root", str(mixed_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["count"] == 1
        assert out["matches"][0]["kind"] == "external"

    def test_list_filter_by_kind_internal_excludes_external(
        self, mixed_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "list", "--format", "json", "--limit", "0",
            "--kind", "internal", "--workspace-root", str(mixed_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["count"] == 2
        assert all(m["kind"] == "internal" for m in out["matches"])

    def test_dispose_sets_disposition_and_filter_finds_it(
        self, mixed_workspace: Path, capsys
    ):
        index = json.loads(
            (mixed_workspace / ".specify" / "memory" / "feedback" / "index.json")
            .read_text(encoding="utf-8"))
        target = index["entries"][0]["id"]
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "dispose", "--id", target, "--to", "processed",
            "--workspace-root", str(mixed_workspace),
        ])
        assert rc == 0
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "list", "--format", "json", "--limit", "0",
            "--disposition", "processed", "--workspace-root", str(mixed_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["count"] == 1
        assert out["matches"][0]["id"] == target

    def test_dispose_rejects_bad_state(self, mixed_workspace: Path, capsys):
        index = json.loads(
            (mixed_workspace / ".specify" / "memory" / "feedback" / "index.json")
            .read_text(encoding="utf-8"))
        target = index["entries"][0]["id"]
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "dispose", "--id", target, "--to", "yolo",
            "--workspace-root", str(mixed_workspace),
        ])
        assert rc == 2


@pytest.mark.contract
class TestCleanupAction:
    def _record(self, root: Path, run_id: str) -> None:
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(root),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", run_id, "--review", "r", "--points", "p",
        ])
        assert rc == 0

    def _package(self, root: Path, capsys) -> str:
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "package", "--format", "json",
            "--workspace-root", str(root),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0 and out["zip"]
        return out["zip"]

    def test_cleanup_dry_run_lists_then_removes_packaged_entries(
        self, probe_workspace: Path, capsys
    ):
        self._record(probe_workspace, "c1")
        zip_rel = self._package(probe_workspace, capsys)
        store = probe_workspace / ".specify" / "memory" / "feedback"

        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "cleanup", "--package", zip_rel, "--dry-run",
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0 and out["dry_run"] is True
        assert len(out["would_remove"]) == 1

        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "cleanup", "--package", zip_rel,
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert len(out["removed"]) == 1
        assert not list(store.glob("2*.md")), "active entry file not removed"
        assert (store / "cleanup-log.md").is_file()

        import json as _j
        index = _j.loads((store / "index.json").read_text(encoding="utf-8"))
        assert index["entries"] == []

    def test_cleanup_scopes_to_packaged_batch_only(
        self, probe_workspace: Path, capsys
    ):
        self._record(probe_workspace, "keep-me")   # archived by mark-submitted
        capsys.readouterr()
        feedback_utils.main([
            "--action", "mark-submitted",
            "--workspace-root", str(probe_workspace),
        ])
        # now_iso() has second granularity: an entry recorded in the SAME
        # second as mark-submitted falls outside the pending window
        # (created > submitted_at is False). Cross the boundary deliberately.
        import time
        time.sleep(1.1)
        self._record(probe_workspace, "remove-me")  # pending → packaged
        zip_rel = self._package(probe_workspace, capsys)
        store = probe_workspace / ".specify" / "memory" / "feedback"
        before = sorted(p.name for p in store.glob("2*.md"))
        assert len(before) == 2

        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "cleanup", "--package", zip_rel,
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        assert rc == 0
        remaining = sorted(p.name for p in store.glob("2*.md"))
        assert len(remaining) == 1, "cleanup must only remove packaged entries"

    def test_cleanup_unknown_package_exit2(
        self, probe_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "cleanup", "--package", "feedback-9999.zip",
            "--workspace-root", str(probe_workspace),
        ])
        assert rc == 2


def _write_legacy_entry(root: Path, unit_id: str, run_id: str) -> str:
    """Hand-write an OLD-format entry (no probe field) like pre-041 stores."""
    store = root / ".specify" / "memory" / "feedback"
    store.mkdir(parents=True, exist_ok=True)
    entry_id = f"20260101T000000Z-{unit_id.replace(':', '-').replace('/', '-')}"
    body = (
        "---\n"
        f"id: {entry_id}\n"
        f"unit_id: {unit_id}\n"
        "unit_type: command\n"
        f"run_id: {run_id}\n"
        "scope: local\n"
        "partial: false\n"
        'created: "2026-01-01T00:00:00Z"\n'
        'summary: "legacy entry"\n'
        "---\n\n## Review\nold review\n\n## Optimization Points\n- old point\n"
    )
    (store / f"{entry_id}.md").write_text(body, encoding="utf-8")
    return entry_id


@pytest.mark.contract
class TestMigrateLegacy:
    def test_status_reports_legacy_remaining(
        self, probe_workspace: Path, capsys
    ):
        _write_legacy_entry(probe_workspace, "/speckit.plan", "legacy-run")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "reindex", "--workspace-root", str(probe_workspace),
        ])
        assert rc == 0
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "status", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["legacy_remaining"] == 1
        assert out["external_count"] == 0

    def test_migrate_legacy_deletes_per_plan(
        self, probe_workspace: Path, capsys
    ):
        entry_id = _write_legacy_entry(probe_workspace, "/speckit.plan", "legacy-run")
        feedback_utils.main([
            "--action", "reindex", "--workspace-root", str(probe_workspace)])
        plan = probe_workspace / "migration-plan.md"
        plan.write_text(f"# plan\n\n{entry_id} -> delete\n", encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "migrate-legacy", "--plan-file", str(plan),
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["deleted"] == [entry_id]
        assert not (probe_workspace / ".specify" / "memory" / "feedback"
                    / f"{entry_id}.md").exists()
        assert (probe_workspace / ".specify" / "memory" / "feedback"
                / "migration-log.md").is_file()

    def test_migrate_legacy_re_registers_with_probe_fields(
        self, probe_workspace: Path, capsys
    ):
        entry_id = _write_legacy_entry(probe_workspace, "/speckit.plan", "legacy-run")
        feedback_utils.main([
            "--action", "reindex", "--workspace-root", str(probe_workspace)])
        plan = probe_workspace / "migration-plan.md"
        plan.write_text(f"{entry_id} -> re-register\n", encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "migrate-legacy", "--plan-file", str(plan),
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["re_registered"] == [entry_id]
        entry_file = (probe_workspace / ".specify" / "memory" / "feedback"
                      / f"{entry_id}.md")
        assert entry_file.exists()  # re-registered in place
        meta, body = feedback_utils.parse_frontmatter(
            entry_file.read_text(encoding="utf-8"))
        assert meta["probe"] == "speckit-plan-wrapup"
        assert meta["kind"] == "internal"
        assert meta["slice"] == "commands"
        assert meta["migrated_from"] == entry_id
        assert meta["created"] == "2026-01-01T00:00:00Z"
        assert "## Review" in body

    def test_migrate_legacy_unknown_id_exit2(
        self, probe_workspace: Path, capsys
    ):
        plan = probe_workspace / "migration-plan.md"
        plan.write_text("ghost-entry -> delete\n", encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "migrate-legacy", "--plan-file", str(plan),
            "--workspace-root", str(probe_workspace),
        ])
        assert rc == 2


@pytest.mark.contract
class TestProbeInjectAndExclusion:
    def test_probe_inject_writes_ext_file_and_enters_merged_view(
        self, probe_workspace: Path, capsys
    ):
        notes = probe_workspace / "notes.md"
        notes.write_text("Collect deploy friction for our custom skill.\n",
                         encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probe-inject", "--unit", "custom:myteam/deploy-skill",
            "--notes-file", str(notes),
            "--format", "json", "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["object_id"].startswith("ext-")
        ext_file = (probe_workspace / ".specify" / "memory" / "feedback"
                    / "probes" / f"{out['object_id']}.md")
        assert ext_file.is_file()
        # merged view + map now include it
        capsys.readouterr()
        feedback_utils.main([
            "--action", "probes", "--format", "json",
            "--workspace-root", str(probe_workspace)])
        listing = json.loads(capsys.readouterr().out)
        assert any(o["object_id"] == out["object_id"]
                   and o["kind"] == "external" for o in listing["objects"])
        capsys.readouterr()
        feedback_utils.main([
            "--action", "map", "--workspace-root", str(probe_workspace)])
        map_text = (probe_workspace / ".specify" / "memory" / "feedback"
                    / "probe-map.md").read_text(encoding="utf-8")
        assert out["object_id"] in map_text

    def test_probe_inject_conflict_exit2(self, probe_workspace: Path, capsys):
        notes = probe_workspace / "notes.md"
        notes.write_text("x\n", encoding="utf-8")
        args = ["--action", "probe-inject", "--unit", "custom:myteam/deploy",
                "--notes-file", str(notes), "--workspace-root", str(probe_workspace)]
        capsys.readouterr()
        assert feedback_utils.main(args) == 0
        capsys.readouterr()
        assert feedback_utils.main(args) == 2

    def test_package_excludes_external_entries(
        self, probe_workspace: Path, capsys, tmp_path: Path
    ):
        probes = (probe_workspace / ".specify" / "memory" / "feedback" / "probes")
        probes.mkdir(parents=True, exist_ok=True)
        (probes / "ext-myteam-deploy-wrapup.md").write_text(
            "---\nobject_id: ext-myteam-deploy-wrapup\n"
            "class_id: external-custom\nunit: custom:myteam/deploy-skill\n"
            "lifecycle_point: wrap-up\n---\n", encoding="utf-8")
        assert _record_entry(probe_workspace, "/speckit.plan", "command", "in-1") == 0
        assert _record_entry(
            probe_workspace, "custom:myteam/deploy-skill", "custom-unit", "ext-1") == 0
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "package", "--format", "json",
            "--workspace-root", str(probe_workspace),
        ])
        out = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert out["excluded_external"] == 1
        assert out["packaged"] == 1
        import zipfile
        zip_path = probe_workspace / out["zip"]
        with zipfile.ZipFile(zip_path) as zf:
            contents = zf.read(
                [n for n in zf.namelist() if n.endswith(".md")
                 and n != "MANIFEST.md"][0]).decode("utf-8")
            manifest = zf.read("MANIFEST.md").decode("utf-8")
        assert "kind: \"external\"" not in contents
        assert "ext-myteam-deploy-wrapup" not in manifest
        assert "speckit-plan-wrapup" in manifest  # probe column present


@pytest.mark.contract
class TestSmokeRemediationContracts:
    """F2 + F16 remediation contracts (2026-08-15 command smoke test)."""

    def test_f2_probes_text_render_includes_zero_object_class(
        self, probe_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--workspace-root", str(probe_workspace),
        ])
        out = capsys.readouterr().out
        assert rc == 0
        assert "external-custom" in out, "zero-object class missing from overview"
        assert "尚无实例" in out

    def test_f16_anchor_mismatch_warning_on_destructive(self, tmp_path):
        import subprocess, sys
        (tmp_path / ".specify").mkdir()
        # F16 fires only for the .specify/scripts/ engine COPY (self-location
        # anchoring); the canonical scripts/python copy falls back to CWD.
        engine = Path(feedback_utils.__file__).resolve().parents[2] / \
            ".specify" / "scripts" / "python" / "feedback-utils.py"
        result = subprocess.run(
            [sys.executable, str(engine), "--action", "dispose", "--id", "ghost"],
            cwd=tmp_path, capture_output=True, text=True,
        )
        assert result.returncode == 2
        assert "anchored at" in result.stderr
        assert "--workspace-root" in result.stderr

    def test_f16_explicit_root_silences_warning(self, tmp_path):
        import subprocess, sys
        (tmp_path / ".specify").mkdir()
        engine = Path(feedback_utils.__file__).resolve().parents[2] / \
            ".specify" / "scripts" / "python" / "feedback-utils.py"
        result = subprocess.run(
            [sys.executable, str(engine), "--action", "dispose",
             "--id", "ghost", "--workspace-root", str(tmp_path)],
            cwd=tmp_path, capture_output=True, text=True,
        )
        assert "anchored at" not in result.stderr
