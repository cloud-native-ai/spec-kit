"""Integration: US1 converge — dry-run zero writes, apply converges, re-run clean (097 T015).

Green claims: contracts/migrate-cli.md C-4 (deterministic plan part, receipt
envelope) and contracts/migrate-engine.md C-4 (client reference-tree
comparison surfaces).

Fixtures come from the declaration-driven builders (tests/fixtures/migrate-097/
builders.py): the latest project is the current assets projected through init's
own copy mechanism; the legacy project is that same tree mutated back into the
legacy layout by names read out of their owner declarations.

Red-first: authored before the planner/executor exist, so every invocation
returns the framework's "no such command" exit 2 — the failures prove the
behaviour is absent.

The mutation test is the FR-008 red-ability proof: excising one dimension's
planner leaves that dimension at zero items, which is exactly what the
per-dimension "at least one item" assertion above would otherwise miss.
"""

import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "migrate-097" / "builders.py"
POINTER_TOPIC = "goal-team-archive-migration"
GOAL_TEAM_PREFIXES = (
    ".specify/goals",
    ".specify/teams",
    ".specify/memory/goals",
    ".specify/memory/teams",
)


def _builders():
    spec = importlib.util.spec_from_file_location(
        "_migrate_us1_builders", BUILDERS_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _invoke(args, input_text=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args, input=input_text)


def _tree_digest(root: Path) -> str:
    """Content+shape digest of the whole tree, symlinks included.

    Directories, symlink targets and file bytes all feed the hash, so a created
    link, an archived file or a renamed directory is visible (C-7 invariant 1).
    """
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L {rel} -> {os.readlink(path)}\n".encode("utf-8"))
        elif path.is_dir():
            digest.update(f"D {rel}\n".encode("utf-8"))
        else:
            content = hashlib.sha256(path.read_bytes()).hexdigest()
            digest.update(f"F {rel} {content}\n".encode("utf-8"))
    return digest.hexdigest()


def _json_payload(result, expected_code):
    assert result.exit_code == expected_code, (
        f"exit {result.exit_code}, expected {expected_code}\n{result.output}"
    )
    return json.loads(result.stdout)


def _dry_run(workspace):
    return _invoke(
        ["migrate", "--workspace", str(workspace), "--format", "json"]
    )


def _assert_static_pointer(payload):
    pointers = payload.get("pointers") or []
    matches = [p for p in pointers if p.get("topic") == POINTER_TOPIC]
    assert matches, f"E-9 static pointer missing: {pointers!r}"
    pointer = matches[0]
    assert pointer["ownerCommand"] == "/speckit.goal"
    assert "migrate-archive" in pointer["ownerEngine"]
    assert pointer.get("note")


def _assert_no_goal_team_items(payload):
    for item in payload["items"]:
        assert not item["target"].startswith(GOAL_TEAM_PREFIXES), item
        assert "goal" not in item["dimension"] and "team" not in item["dimension"], item


# ---------------------------------------------------------------------------
# Latest project: dry-run is clean and writes nothing
# ---------------------------------------------------------------------------


def test_latest_fixture_dry_run_is_clean_with_an_unchanged_tree_hash(tmp_path):
    workspace = _builders().build_latest_project(tmp_path / "latest")
    before = _tree_digest(workspace)

    payload = _json_payload(_dry_run(workspace), 0)

    assert payload["outcome"] == "clean"
    assert payload["exitCode"] == 0
    assert payload["summary"]["total"] == 0
    assert payload["receiptPath"] is None
    assert _tree_digest(workspace) == before, "dry-run wrote to the workspace"
    _assert_static_pointer(payload)
    _assert_no_goal_team_items(payload)


# ---------------------------------------------------------------------------
# Legacy project: planned, every dimension represented, zero writes, stable
# ---------------------------------------------------------------------------


def test_legacy_fixture_dry_run_is_planned_with_every_dimension_and_zero_writes(
    tmp_path,
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")
    before = _tree_digest(workspace)

    first = _json_payload(_dry_run(workspace), 1)
    after_first = _tree_digest(workspace)
    second = _json_payload(_dry_run(workspace), 1)

    assert after_first == before, "first dry-run wrote to the workspace"
    assert _tree_digest(workspace) == before, "second dry-run wrote to the workspace"
    assert first["outcome"] == "planned"
    assert first["exitCode"] == 1
    for dimension in specify_cli.MIGRATE_DIMENSIONS:
        assert first["summary"]["byDimension"][dimension] >= 1, (
            f"dimension {dimension!r} has no item: {first['summary']}"
        )
    for item in first["items"]:
        assert item["evidence"], f"item without an owner evidence path: {item}"
    assert first["items"] == second["items"], (
        "repeated dry-runs on one tree must be byte-identical (FR-006)"
    )
    assert first["summary"] == second["summary"]
    _assert_static_pointer(first)
    _assert_no_goal_team_items(first)


# ---------------------------------------------------------------------------
# Apply converges under the simulated interactive second key; re-run is clean
# ---------------------------------------------------------------------------


def test_apply_with_simulated_interactive_confirmation_converges_then_clean(
    tmp_path, monkeypatch
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")
    monkeypatch.setattr(
        specify_cli, "migrate_interactive_terminal", lambda: True
    )

    result = _invoke(
        [
            "migrate",
            "--workspace",
            str(workspace),
            "--apply",
            "--format",
            "json",
        ],
        input_text="y\n",
    )
    payload = _json_payload(result, 0)

    assert payload["outcome"] == "applied"
    assert payload["exitCode"] == 0
    assert payload["receiptPath"], "apply must name its receipt file"
    receipt_path = workspace / payload["receiptPath"]
    assert receipt_path.is_file()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert payload["receipt"]["runId"] == receipt["runId"]
    assert receipt["status"] == "completed"
    assert receipt["outcome"] == "applied"
    assert receipt["items"], "receipt carries no items"
    assert all(item["status"] == "done" for item in receipt["items"]), [
        (item["target"], item["status"]) for item in receipt["items"]
    ]
    assert receipt["archives"], "apply archived nothing"
    for entry in receipt["archives"]:
        assert (workspace / entry["archiveTo"]).exists(), (
            f"archived object not found at its receipt path: {entry}"
        )
        assert entry["digest"], entry
    assert len(receipt["recover"]) == len(receipt["archives"]), (
        "every archive entry needs one recovery path"
    )
    _assert_static_pointer(receipt)
    _assert_no_goal_team_items(receipt)
    assert receipt["pointers"] == payload["receipt"]["pointers"]

    before = _tree_digest(workspace)
    second = _json_payload(_dry_run(workspace), 0)
    assert second["outcome"] == "clean"
    assert second["summary"]["total"] == 0
    assert _tree_digest(workspace) == before, (
        "the post-apply re-run wrote to the workspace (FR-017 idempotence)"
    )


# ---------------------------------------------------------------------------
# Mixed project (SC-003 / contract C-8): planned -> applied -> clean, and the
# per-item equivalence assertion has power beyond existence
# ---------------------------------------------------------------------------

MIXED_DIMENSIONS = ("templates-generated", "compat-links", "migration-residue")


def test_mixed_fixture_converges_in_one_apply_then_reruns_clean(
    tmp_path, monkeypatch
):
    workspace = _builders().build_mixed_project(tmp_path / "mixed")
    before = _tree_digest(workspace)

    dry = _json_payload(_dry_run(workspace), 1)

    assert dry["outcome"] == "planned"
    assert _tree_digest(workspace) == before, "the mixed dry-run wrote to the workspace"
    for dimension in MIXED_DIMENSIONS:
        assert dry["summary"]["byDimension"][dimension] >= 1, (
            f"the mixed fixture constructed a {dimension!r} class but plans no item"
        )

    monkeypatch.setattr(specify_cli, "migrate_interactive_terminal", lambda: True)
    applied = _json_payload(
        _invoke(
            [
                "migrate",
                "--workspace",
                str(workspace),
                "--apply",
                "--format",
                "json",
            ],
            input_text="y\n",
        ),
        0,
    )
    assert applied["outcome"] == "applied"
    receipt = applied["receipt"]
    assert all(item["status"] == "done" for item in receipt["items"]), [
        (item["target"], item["status"]) for item in receipt["items"]
    ]
    for entry in receipt["archives"]:
        assert (workspace / entry["archiveTo"]).exists(), entry
    assert len(receipt["recover"]) == len(receipt["archives"])

    before_rerun = _tree_digest(workspace)
    rerun = _json_payload(_dry_run(workspace), 0)
    assert rerun["outcome"] == "clean"
    assert rerun["summary"]["total"] == 0
    assert _tree_digest(workspace) == before_rerun, (
        "the mixed post-apply re-run wrote to the workspace (FR-017 idempotence)"
    )


def test_mixed_fixture_equivalence_assertion_has_power_beyond_existence(
    tmp_path, monkeypatch
):
    """SC-003 red-ability: an existence-only reading would pass a corrupted tree."""
    workspace = _builders().build_mixed_project(tmp_path / "mixed")
    monkeypatch.setattr(specify_cli, "migrate_interactive_terminal", lambda: True)
    _json_payload(
        _invoke(
            [
                "migrate",
                "--workspace",
                str(workspace),
                "--apply",
                "--format",
                "json",
            ],
            input_text="y\n",
        ),
        0,
    )
    _json_payload(_dry_run(workspace), 0)

    target_rel = ".specify/templates/plan-template.md"
    target = workspace / target_rel
    target.write_text(
        target.read_text(encoding="utf-8")
        + "\n<!-- corrupted after convergence -->\n",
        encoding="utf-8",
    )

    assert target.exists(), "the weakening scenario needs the target to exist"

    weakened = _json_payload(_dry_run(workspace), 1)
    assert weakened["outcome"] == "planned"
    corrupted = [
        item for item in weakened["items"] if item["target"] == target_rel
    ]
    assert corrupted, (
        "existence-only would accept a corrupted converged tree; the per-item "
        "equivalence assertion must flag the byte difference"
    )


# ---------------------------------------------------------------------------
# FR-008 red-ability: excising one dimension removes its items
# ---------------------------------------------------------------------------


def test_removing_one_dimension_makes_the_per_dimension_check_red(
    tmp_path, monkeypatch
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")

    control = _json_payload(_dry_run(workspace), 1)
    for dimension in specify_cli.MIGRATE_DIMENSIONS:
        with monkeypatch.context() as patch:
            patch.setitem(
                specify_cli._MIGRATE_DIMENSION_PLANNERS, dimension, lambda ctx: []
            )
            mutated = _json_payload(_dry_run(workspace), 1)
        assert mutated["summary"]["byDimension"][dimension] == 0, (
            f"removing the {dimension!r} planner did not remove its items — "
            "the per-dimension assertion has no discriminative power"
        )
        assert control["summary"]["byDimension"][dimension] >= 1
