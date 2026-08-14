"""Contract test: feedback-utils.py probe registry (Feature 028 / requirement 041).

Enforces ``.specify/specs/041-refactor-feedback-probe/contracts/probe-registry.md``
(C-2 Classes schema, C-3 internal Objects schema, C-4 external probe files,
C-5 reconcile invariants) via the ``--action probes`` engine surface
(``--validate`` / ``--reconcile`` / ``--format json``).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

VALID_REGISTRY = """# Feedback Probe Definitions

## Slices

- commands
- skills
- host-custom

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


def _workspace(tmp_path: Path, registry: str | None = VALID_REGISTRY) -> Path:
    if registry is not None:
        defs = tmp_path / ".specify" / "shared" / "definitions"
        defs.mkdir(parents=True, exist_ok=True)
        (defs / "probe-definitions.md").write_text(registry, encoding="utf-8")
    return tmp_path


def _external_probe(tmp_path: Path, name: str, body: str) -> Path:
    probes = tmp_path / ".specify" / "memory" / "feedback" / "probes"
    probes.mkdir(parents=True, exist_ok=True)
    path = probes / f"{name}.md"
    path.write_text(body, encoding="utf-8")
    return path


def _embed_workspace(tmp_path: Path) -> Path:
    cmds = tmp_path / "templates" / "commands"
    cmds.mkdir(parents=True, exist_ok=True)
    (cmds / "plan.md").write_text("# plan\n\n## Feedback\n\nstep\n", encoding="utf-8")
    skill = tmp_path / "skills" / "study-project"
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text("# study\n\n## Feedback\n\nstep\n", encoding="utf-8")
    return tmp_path


@pytest.mark.contract
class TestProbesValidate:
    def test_validate_ok_on_valid_registry(self, tmp_path: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 0

    def test_validate_exit2_on_missing_class_field(self, tmp_path: Path, capsys):
        broken = VALID_REGISTRY.replace(
            "| command-wrapup | internal | command run review |",
            "| command-wrapup | internal |  |",
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path, broken)),
        ])
        assert rc == 2

    def test_validate_exit2_on_bad_kind(self, tmp_path: Path, capsys):
        broken = VALID_REGISTRY.replace(
            "| skill-wrapup | internal |", "| skill-wrapup | hybrid |"
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path, broken)),
        ])
        assert rc == 2

    def test_validate_exit2_on_duplicate_object_id(self, tmp_path: Path, capsys):
        broken = VALID_REGISTRY + (
            "| skill-study-wrapup | skill-wrapup | skill:other | wrap-up |\n"
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path, broken)),
        ])
        assert rc == 2

    def test_validate_exit2_on_unknown_class_reference(self, tmp_path: Path, capsys):
        broken = VALID_REGISTRY + (
            "| orphan-object | no-such-class | /speckit.todo | wrap-up |\n"
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path, broken)),
        ])
        assert rc == 2

    def test_validate_exit2_on_bad_unit_syntax(self, tmp_path: Path, capsys):
        broken = VALID_REGISTRY + (
            "| bad-unit | command-wrapup | speckit.plan | wrap-up |\n"
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path, broken)),
        ])
        assert rc == 2


@pytest.mark.contract
class TestProbesListing:
    def test_probes_json_lists_merged_view(self, tmp_path: Path, capsys):
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--format", "json",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 0
        out = json.loads(capsys.readouterr().out)
        classes = out["classes"]
        objects = out["objects"]
        assert len(classes) == 3
        assert len(objects) == 2
        by_id = {o["object_id"]: o for o in objects}
        assert by_id["speckit-plan-wrapup"]["kind"] == "internal"
        assert by_id["speckit-plan-wrapup"]["slice"] == "commands"

    def test_external_probe_file_included_in_merged_view(
        self, tmp_path: Path, capsys
    ):
        _external_probe(
            tmp_path,
            "ext-myteam-deploy-wrapup",
            "---\nobject_id: ext-myteam-deploy-wrapup\n"
            "class_id: external-custom\nunit: custom:myteam/deploy-skill\n"
            "lifecycle_point: wrap-up\n---\n\nTargets our custom deploy skill.\n",
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--format", "json",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 0
        out = json.loads(capsys.readouterr().out)
        ext = [o for o in out["objects"] if o["object_id"].startswith("ext-")]
        assert len(ext) == 1
        assert ext[0]["kind"] == "external"
        assert ext[0]["slice"] == "host-custom"


@pytest.mark.contract
class TestExternalProbeValidation:
    def test_external_requires_ext_prefix(self, tmp_path: Path, capsys):
        _external_probe(
            tmp_path,
            "myteam-deploy-wrapup",
            "---\nobject_id: myteam-deploy-wrapup\n"
            "class_id: external-custom\nunit: custom:myteam/deploy-skill\n"
            "lifecycle_point: wrap-up\n---\n",
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 2

    def test_external_must_reference_external_class(self, tmp_path: Path, capsys):
        _external_probe(
            tmp_path,
            "ext-bad-kind",
            "---\nobject_id: ext-bad-kind\nclass_id: command-wrapup\n"
            "unit: custom:myteam/deploy-skill\nlifecycle_point: wrap-up\n---\n",
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 2

    def test_external_requires_custom_unit_syntax(self, tmp_path: Path, capsys):
        _external_probe(
            tmp_path,
            "ext-bad-unit",
            "---\nobject_id: ext-bad-unit\nclass_id: external-custom\n"
            "unit: /speckit.plan\nlifecycle_point: wrap-up\n---\n",
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--validate",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 2


@pytest.mark.contract
class TestProbesReconcile:
    def test_reconcile_zero_gap_exit0(self, tmp_path: Path, capsys):
        _embed_workspace(tmp_path)
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--reconcile",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 0

    def test_reconcile_exit2_on_missing_object_for_embed(
        self, tmp_path: Path, capsys
    ):
        _embed_workspace(tmp_path)
        cmds = tmp_path / "templates" / "commands"
        (cmds / "todo.md").write_text("# todo\n\n## Feedback\n\nstep\n",
                                      encoding="utf-8")
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--reconcile",
            "--workspace-root", str(_workspace(tmp_path)),
        ])
        assert rc == 2
        assert "/speckit.todo" in capsys.readouterr().err

    def test_reconcile_exit2_on_orphan_object(self, tmp_path: Path, capsys):
        _embed_workspace(tmp_path)
        # registry declares an internal object whose embed template is absent
        orphan = VALID_REGISTRY + (
            "| speckit-ghost-wrapup | command-wrapup | /speckit.ghost | wrap-up |\n"
        )
        capsys.readouterr()
        rc = feedback_utils.main([
            "--action", "probes", "--reconcile",
            "--workspace-root", str(_workspace(tmp_path, orphan)),
        ])
        assert rc == 2
        assert "speckit-ghost-wrapup" in capsys.readouterr().err
