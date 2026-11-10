"""Unit tests: the migrate planner foundation model (097 T005; T010/T011 unit slots).

Red-first: this file is authored before the MIGRATE_* foundation exists in
``specify_cli``; every failure below must be an AttributeError/ImportError
against the not-yet-written model, never a broken assertion.

Contract owners referenced by these assertions (never restated as new rosters):

* dimension tokens and their fixed order -> ``data-model.md`` E-8 (read here);
* disposition domain -> ``requirements.md`` FR-014 (read by the contract
  test); this file only uses its machine tokens.
"""

import hashlib
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / ".specify" / "specs" / "097-speckit-migrate-command"


def _e8_dimensions() -> tuple:
    """Read the five dimension tokens and their order from data-model.md E-8."""
    text = (SPEC_DIR / "data-model.md").read_text(encoding="utf-8")
    section = text[text.index("## E-8"):text.index("## E-9")]
    return tuple(re.findall(r"^\| `([a-z-]+)` \|", section, re.MULTILINE))


def _item(**overrides):
    from specify_cli import MigrateItem

    fields = dict(
        dimension="templates-generated",
        target=".specify/templates/plan-template.md",
        current="differs",
        expected="byte-equal to installed asset",
        disposition="replace",
        mechanism="replace",
        evidence=["templates/plan-template.md"],
        archiveTo=".specify/archive/migrate/20261110T093012Z-1a2b3c4d/templates/plan-template.md",
    )
    fields.update(overrides)
    return MigrateItem(**fields)


# ---------------------------------------------------------------------------
# T005 — dimension tokens, id shape, dedup + stable order, serialization,
#        refuse/blocked reason enforcement
# ---------------------------------------------------------------------------


def test_dimension_tokens_and_order_come_from_data_model_e8():
    from specify_cli import MIGRATE_DIMENSIONS

    assert _e8_dimensions() == (
        "templates-generated",
        "anchor-layout",
        "compat-links",
        "mirror-consistency",
        "migration-residue",
    )
    assert tuple(MIGRATE_DIMENSIONS) == _e8_dimensions()


def test_item_id_is_sha1_prefix_of_dimension_and_target():
    item = _item(dimension="compat-links", target="CLAUDE.md")
    expected = hashlib.sha1(b"compat-links|CLAUDE.md").hexdigest()[:12]
    assert item.id == expected


def test_plan_dedupes_dimension_target_and_sorts_stably():
    from specify_cli import MigratePlan

    items = [
        _item(dimension="migration-residue", target=".specify/skills/web-test"),
        _item(dimension="templates-generated", target=".specify/templates/b.md"),
        _item(dimension="templates-generated", target=".specify/templates/a.md"),
        # Duplicate (dimension, target) — must collapse to exactly one item.
        _item(dimension="templates-generated", target=".specify/templates/a.md"),
        _item(dimension="anchor-layout", target=".specify/memory/constitution.md"),
    ]
    plan = MigratePlan(items=items)

    keys = [(i.dimension, i.target) for i in plan.items]
    assert len(keys) == len(set(keys))
    assert [d for d, _ in keys] == [
        "templates-generated",
        "templates-generated",
        "anchor-layout",
        "migration-residue",
    ]
    assert keys[0][1] == ".specify/templates/a.md"
    assert keys[1][1] == ".specify/templates/b.md"


def test_repeated_serialization_is_byte_identical():
    from specify_cli import MigratePlan

    base = [
        _item(dimension="templates-generated", target=".specify/templates/b.md"),
        _item(dimension="migration-residue", target=".specify/skills/web-test"),
        _item(dimension="anchor-layout", target=".specify/memory/constitution.md"),
    ]
    shuffled = [base[2], base[0], base[1]]

    first = MigratePlan(items=list(base)).to_json()
    second = MigratePlan(items=list(shuffled)).to_json()
    third = MigratePlan(items=list(base)).to_json()

    assert first == second == third
    payload = json.loads(first)
    assert payload["planVersion"] == 1
    assert [item["id"] for item in payload["items"]] == [
        item["id"] for item in json.loads(second)["items"]
    ]


def test_text_and_json_envelopes_carry_the_same_items():
    from specify_cli import MigratePlan

    plan = MigratePlan(
        mode="dry-run",
        workspace="/tmp/example",
        workspace_kind="client",
        items=[
            _item(dimension="templates-generated", target=".specify/templates/a.md"),
            _item(
                dimension="compat-links",
                target="CLAUDE.md",
                current="missing",
                expected="symlink -> .specify/instructions.md",
                disposition="write",
                mechanism="symlink",
            ),
        ],
        notes=["command-copies: no tool surface detected"],
    )

    payload = plan.to_payload()
    text = plan.to_text()
    for item in payload["items"]:
        assert item["target"] in text
        assert item["disposition"] in text
    assert payload["summary"]["total"] == 2
    assert payload["summary"]["byDimension"]["templates-generated"] == 1
    assert payload["summary"]["byDimension"]["compat-links"] == 1
    assert payload["notes"] == ["command-copies: no tool surface detected"]


def test_refuse_item_requires_reason_naming_both_candidates():
    from specify_cli import MigrateItem, make_refuse_item

    with pytest.raises(ValueError):
        MigrateItem(
            dimension="compat-links",
            target=".github/skills",
            current="exists-differs (regular directory)",
            expected="symlink -> .specify/skills",
            disposition="refuse",
            reason="",
        )

    with pytest.raises(ValueError):
        MigrateItem(
            dimension="compat-links",
            target=".github/skills",
            current="exists-differs (regular directory)",
            expected="symlink -> .specify/skills",
            disposition="refuse",
            reason="conflict; no candidates named",
        )

    item = make_refuse_item(
        "compat-links",
        ".github/skills",
        current="exists-differs (regular directory)",
        expected="symlink -> .specify/skills",
    )
    assert item.disposition == "refuse"
    assert item.status == "refused"
    assert item.archiveTo is None
    assert item.reason
    assert "exists-differs (regular directory)" in item.reason
    assert "symlink -> .specify/skills" in item.reason


def test_blocked_item_requires_reason_for_the_missing_second_key():
    from specify_cli import MigrateItem, make_blocked_item

    with pytest.raises(ValueError):
        MigrateItem(
            dimension="migration-residue",
            target=".specify/skills/web-test",
            current="legacy-location",
            expected="absent",
            disposition="blocked",
            reason="",
        )

    item = make_blocked_item(
        "migration-residue",
        ".specify/skills/web-test",
        current="legacy-location",
        expected="absent",
    )
    assert item.disposition == "blocked"
    assert item.status == "blocked"
    assert "second key" in item.reason


# ---------------------------------------------------------------------------
# T010 — workspace-kind detection and engine loading points
# ---------------------------------------------------------------------------


def test_workspace_kind_framework_source_iff_skills_external_dir(tmp_path):
    from specify_cli import detect_migrate_workspace_kind

    (tmp_path / ".specify").mkdir()
    assert detect_migrate_workspace_kind(tmp_path) == "client"

    (tmp_path / "skills" / "external").mkdir(parents=True)
    assert detect_migrate_workspace_kind(tmp_path) == "framework-source"


def test_engine_loading_points_follow_the_workspace_kind(tmp_path, monkeypatch):
    import specify_cli

    resource_root = tmp_path / "resource"
    (resource_root / "scripts" / "python").mkdir(parents=True)
    monkeypatch.setattr(specify_cli, "get_resource_path", lambda: resource_root)

    workspace = tmp_path / "client"
    (workspace / ".specify" / "scripts" / "python").mkdir(parents=True)
    assert specify_cli.resolve_migrate_engine_dir(workspace, "client") == (
        resource_root / "scripts" / "python"
    )
    assert specify_cli.resolve_migrate_engine_dir(workspace, "framework-source") == (
        workspace / ".specify" / "scripts" / "python"
    )
    # Default kind is detected from the workspace, not guessed from versions.
    assert specify_cli.resolve_migrate_engine_dir(workspace) == (
        resource_root / "scripts" / "python"
    )


# ---------------------------------------------------------------------------
# T011 — client reference-tree builder
# ---------------------------------------------------------------------------


def _build_minimal_resource_root(tmp_path: Path) -> Path:
    resource = tmp_path / "resource"
    (resource / "memory").mkdir(parents=True)
    (resource / "memory" / "constitution.md").write_text("# c\n", encoding="utf-8")
    (resource / "templates" / "commands").mkdir(parents=True)
    (resource / "templates" / "demo-template.md").write_text(
        "demo\n", encoding="utf-8"
    )
    (resource / "templates" / "commands" / "requirements.md").write_text(
        "---\ndescription: requirements fixture\n---\n\nbody {ARGS}\n",
        encoding="utf-8",
    )
    (resource / "scripts" / "python").mkdir(parents=True)
    (resource / "scripts" / "python" / "example-script.py").write_text(
        "print('x')\n", encoding="utf-8"
    )
    return resource


def test_tool_surface_detection_is_restricted_to_existing_dirs(tmp_path):
    from specify_cli import detect_migrate_tool_surfaces

    workspace = tmp_path / "ws"
    (workspace / ".qoder" / "commands").mkdir(parents=True)
    (workspace / ".github" / "prompts").mkdir(parents=True)
    surfaces = detect_migrate_tool_surfaces(workspace)
    assert set(surfaces) == {"qoder", "copilot"}
    assert surfaces["qoder"] == ".qoder/commands"
    assert surfaces["copilot"] == ".github/prompts"


def test_script_variant_detected_from_existing_copies(tmp_path):
    from specify_cli import detect_migrate_script_variant

    workspace = tmp_path / "ws"
    commands = workspace / ".qoder" / "commands"
    commands.mkdir(parents=True)
    assert detect_migrate_script_variant(workspace) == "sh"

    (commands / "speckit.plan.md").write_text(
        "run `pwsh scripts/bash/create-new-plan.ps1`\n", encoding="utf-8"
    )
    assert detect_migrate_script_variant(workspace) == "ps"


def test_reference_tree_projects_assets_and_is_removed(tmp_path, monkeypatch):
    import specify_cli

    resource = _build_minimal_resource_root(tmp_path)
    monkeypatch.setattr(specify_cli, "get_resource_path", lambda: resource)

    workspace = tmp_path / "ws"
    (workspace / ".specify").mkdir(parents=True)
    (workspace / ".qoder" / "commands").mkdir(parents=True)

    with specify_cli.build_client_reference_tree(workspace) as reference_root:
        assert reference_root.is_dir()
        assert (
            reference_root / ".specify" / "templates" / "demo-template.md"
        ).is_file()
        assert (
            reference_root / ".specify" / "scripts" / "python" / "example-script.py"
        ).is_file()
        assert (
            reference_root / ".qoder" / "commands" / "speckit.requirements.md"
        ).is_file()
        captured = reference_root

    assert not captured.exists()
    # The workspace itself is never written by the builder.
    assert not (workspace / ".specify" / "templates").exists()
