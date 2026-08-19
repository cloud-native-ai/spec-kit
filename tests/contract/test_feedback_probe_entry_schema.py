"""Contract test: feedback entry schema probe extension (req 041).

Pins ``.specify/specs/041-refactor-feedback-probe/contracts/entry-schema.md``:
C-1 probe/kind/slice frontmatter written by ``record`` (engine-resolved, never
caller-supplied), C-1.1 exit 2 when the unit has no probe object (registry
present), legacy fallback when the registry is absent, C-3 external entries
via ``custom:`` units, C-4 index mirror keys.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.script_api import feedback_utils

REGISTRY = """# Feedback Probe Definitions

## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| command-wrapup | internal | command run review | commands | record→package | wrap-up |
| external-custom | external | custom unit review | host-custom | record→local | wrap-up |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| speckit-plan-wrapup | command-wrapup | /speckit.plan | wrap-up |
"""


def _record(root: Path, *extra: str) -> int:
    return feedback_utils.main([
        "--action", "record", "--workspace-root", str(root),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", "schema-run", "--review", "review text",
        "--points", "one point", *extra,
    ])


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    defs = tmp_path / ".specify" / "shared" / "definitions"
    defs.mkdir(parents=True, exist_ok=True)
    (defs / "probe-definitions.md").write_text(REGISTRY, encoding="utf-8")
    return tmp_path


def _entry_file(root: Path) -> Path:
    files = sorted((root / ".specify" / "memory" / "feedback").glob("*.md"))
    assert files, "no entry written"
    return files[-1]


@pytest.mark.contract
class TestRecordProbeResolution:
    def test_record_writes_probe_kind_slice_frontmatter(
        self, workspace: Path, capsys
    ):
        capsys.readouterr()
        assert _record(workspace) == 0
        from tests.script_api import feedback_utils
        meta, _body = feedback_utils.parse_frontmatter(
            _entry_file(workspace).read_text(encoding="utf-8"))
        assert meta["probe"] == "speckit-plan-wrapup"
        assert meta["kind"] == "internal"
        assert meta["slice"] == "commands"

    def test_index_mirror_carries_probe_keys(self, workspace: Path, capsys):
        capsys.readouterr()
        assert _record(workspace) == 0
        import json
        index = json.loads(
            (workspace / ".specify" / "memory" / "feedback" / "index.json")
            .read_text(encoding="utf-8"))
        entry = index["entries"][-1]
        assert entry["probe"] == "speckit-plan-wrapup"
        assert entry["kind"] == "internal"
        assert entry["slice"] == "commands"

    def test_record_exit2_when_no_probe_object(self, workspace: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(workspace),
            "--unit-id", "/speckit.ghost", "--unit-type", "command",
            "--run-id", "ghost", "--review", "r", "--points", "p",
        ])
        assert rc == 2
        assert "no probe object for unit" in capsys.readouterr().err

    def test_record_legacy_mode_when_registry_absent(
        self, tmp_path: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(tmp_path),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", "legacy", "--review", "r", "--points", "p",
        ])
        assert rc == 0
        text = _entry_file(tmp_path).read_text(encoding="utf-8")
        assert "probe:" not in text.split("## Review")[0]
        assert "kind:" not in text.split("## Review")[0]

    def test_record_custom_unit_resolves_external(
        self, workspace: Path, capsys
    ):
        probes = workspace / ".specify" / "memory" / "feedback" / "probes"
        probes.mkdir(parents=True, exist_ok=True)
        (probes / "ext-myteam-deploy-wrapup.md").write_text(
            "---\nobject_id: ext-myteam-deploy-wrapup\n"
            "class_id: external-custom\nunit: custom:myteam/deploy-skill\n"
            "lifecycle_point: wrap-up\n---\n", encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(workspace),
            "--unit-id", "custom:myteam/deploy-skill", "--unit-type", "custom-unit",
            "--run-id", "ext-run", "--review", "r", "--points", "p",
        ])
        assert rc == 0
        meta, _body = feedback_utils.parse_frontmatter(
            _entry_file(workspace).read_text(encoding="utf-8"))
        assert meta["kind"] == "external"
        assert meta["slice"] == "host-custom"
        assert meta["probe"] == "ext-myteam-deploy-wrapup"

    def test_record_rejects_custom_unit_with_internal_type(
        self, workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(workspace),
            "--unit-id", "custom:myteam/deploy-skill", "--unit-type", "command",
            "--run-id", "x", "--review", "r", "--points", "p",
        ])
        assert rc == 2


GATE_REGISTRY = """# Feedback Probe Definitions

## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| command-wrapup | internal | command run review | commands | record→package | wrap-up |
| command-gate | internal | gate firing evidence | commands | record→package | confirm-gate |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| speckit-plan-wrapup | command-wrapup | /speckit.plan | wrap-up |
| gate-plan-sample | command-gate | /speckit.plan | gate-plan-sample |
"""


@pytest.fixture
def gate_workspace(tmp_path: Path) -> Path:
    defs = tmp_path / ".specify" / "shared" / "definitions"
    defs.mkdir(parents=True, exist_ok=True)
    (defs / "probe-definitions.md").write_text(GATE_REGISTRY, encoding="utf-8")
    return tmp_path


@pytest.mark.contract
class TestRecordGateProbeResolution:
    """044 Phase 7: (unit, lifecycle_point) resolution for gate probes."""

    def test_record_with_lifecycle_point_stamps_gate_object(
        self, gate_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(gate_workspace),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--lifecycle-point", "gate-plan-sample",
            "--run-id", "gate:gate-plan-sample:20260819T000000Z",
            "--review", "confirm-gate firing: approved-as-is", "--points", "one point",
        ])
        assert rc == 0
        meta, _body = feedback_utils.parse_frontmatter(
            _entry_file(gate_workspace).read_text(encoding="utf-8"))
        assert meta["probe"] == "gate-plan-sample"
        assert meta["kind"] == "internal"
        assert meta["slice"] == "commands"

    def test_record_without_lifecycle_point_keeps_wrapup_resolution(
        self, gate_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(gate_workspace),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", "wrapup-run", "--review", "review", "--points", "one point",
        ])
        assert rc == 0
        meta, _body = feedback_utils.parse_frontmatter(
            _entry_file(gate_workspace).read_text(encoding="utf-8"))
        assert meta["probe"] == "speckit-plan-wrapup"

    def test_record_unknown_lifecycle_point_exit2(
        self, gate_workspace: Path, capsys
    ):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(gate_workspace),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--lifecycle-point", "gate-nonexistent",
            "--run-id", "bad-gate", "--review", "r", "--points", "p",
        ])
        assert rc == 2
        assert "lifecycle_point" in capsys.readouterr().err
