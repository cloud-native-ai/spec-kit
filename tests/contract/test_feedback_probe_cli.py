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
