"""Contract tests for the unified archive, `migrate-archive` and the residual probe.

Feature 094, `contracts/unified-archive-and-migration.md` C-31…C-50; tasks rows
T028–T030, T035–T039, T041 and the engine half of T078 (the probe-residual clauses).
Every test drives the engine as a subprocess over a fixture repository, so the
assertions are about the CLI surface the consumers actually call.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

ARCHIVE = Path(".specify/archive/goal-team")
RECEIPTS = ARCHIVE / "receipts"
TREES = ARCHIVE / "trees"

GOAL_SOURCE = """---
status: {status}
created: 2026-11-09
updated: 2026-11-09
---

# Goal: {slug}

## Objective

{objective}

## Success Criteria

1. {criterion}

## History

- 2026-11-09 — created in the spec-local layout.
"""

TEAM_SOURCE = """---
name: fixture team {slug}
slug: {slug}
description: A fixture team that proves the archive move.
goal: >-
  Carry the fixture goal to a single archive landing point without losing a byte
  of its definition or its run history.
goal_slug: {goal_slug}
lifecycle_state: {lifecycle}
scope: spec
spec_dir: .specify/specs/{spec}
territory:
  write:
    - .specify/specs/{spec}/**
---

# Team: {slug}

## Goal

The fixture goal is carried by the unified archive.
"""


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no JSON payload; stderr={proc.stderr!r}"
    return json.loads(proc.stdout)


def _seed_spec_goal(root: Path, spec: str, slug: str | None = None, *,
                    objective: str = "Move the fixture definition without losing a byte.",
                    criterion: str = "The definition survives the move.",
                    status: str = "active") -> Path:
    slug = slug or spec
    tree = root / ".specify/specs" / spec / "goal" / slug
    tree.mkdir(parents=True, exist_ok=True)
    (tree / "goal.md").write_text(
        GOAL_SOURCE.format(status=status, slug=slug, objective=objective,
                           criterion=criterion),
        encoding="utf-8")
    return tree


def _seed_spec_team(root: Path, spec: str, slug: str | None = None, *,
                    goal_slug: str | None = None,
                    lifecycle: str = "active") -> Path:
    slug = slug or spec
    tree = root / ".specify/specs" / spec / "team" / slug
    tree.mkdir(parents=True, exist_ok=True)
    (tree / "team.md").write_text(
        TEAM_SOURCE.format(spec=spec, slug=slug, goal_slug=goal_slug or slug,
                           lifecycle=lifecycle),
        encoding="utf-8")
    return tree


def _receipt(root: Path, kind: str, slug: str) -> dict:
    path = root / RECEIPTS / f"{kind}-{slug}.yaml"
    assert path.is_file(), f"missing receipt: {path}"
    fields: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition(":")
        if sep and key and not key.startswith(" "):
            fields[key.strip()] = value.strip()
    return fields


def _snapshot(root: Path) -> list[tuple]:
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append((str(path.relative_to(root)), path.stat().st_mtime_ns,
                         hashlib.sha256(path.read_bytes()).hexdigest()))
    return rows


def _body(text: str) -> str:
    """Everything after the closing frontmatter delimiter — the byte region a binding
    insertion/rewrite must never touch."""
    return text.split("---", 2)[2]


# ---------------------------------------------------------------------------
# T028 / C-31…C-50 — the migration moves the tree and leaves a receipt
# ---------------------------------------------------------------------------

def test_migration_moves_the_tree_and_leaves_an_archive_not_delete_receipt(tmp_path):
    spec = "091-fixture"
    _seed_spec_goal(tmp_path, spec, slug="alpha")
    _seed_spec_team(tmp_path, spec, slug="crew", goal_slug="alpha")

    proc = _run(tmp_path, "migrate-archive", "--apply")
    assert proc.returncode == 0, f"stdout={proc.stdout!r} stderr={proc.stderr!r}"

    # C-31 — the two archive rows are the only landing points.
    goal_target = tmp_path / ".specify/anchoring/alpha/goal.md"
    team_target = tmp_path / ".specify/teams/crew/team.md"
    assert goal_target.is_file()
    assert team_target.is_file()

    # C-36 — origin is set on every migrated definition; the binding is complete.
    goal_binding = _payload(_run(tmp_path, "binding", "goal", "alpha"))
    assert goal_binding["owner"] == "human"
    assert goal_binding["owner_id"] == "human"
    assert goal_binding["origin"] == spec
    team_binding = _payload(_run(tmp_path, "binding", "teams", "crew"))
    assert team_binding["origin"] == spec

    # C-35/C-37 — moved, not copied; the source tree is gone from its old position
    # and every file stays readable under trees/.
    assert not (tmp_path / ".specify/specs" / spec / "goal/alpha").exists()
    assert not (tmp_path / ".specify/specs" / spec / "team/crew").exists()
    archived_goal = tmp_path / TREES / spec / "goal/alpha/goal.md"
    archived_team = tmp_path / TREES / spec / "teams/crew/team.md"
    assert archived_goal.is_file()
    assert archived_team.is_file()

    # C-32/C-33 — one receipt per definition, nine mandatory fields plus the literal.
    goal_receipt = _receipt(tmp_path, "goal", "alpha")
    assert goal_receipt["kind"] == "goal"
    assert goal_receipt["source_spec"] == spec
    assert goal_receipt["source_slug"] == "alpha"
    assert goal_receipt["target_slug"] == "alpha"
    assert goal_receipt["target_path"] == ".specify/anchoring/alpha/goal.md"
    assert goal_receipt["archived_path"] == f".specify/archive/goal-team/trees/{spec}/goal/alpha"
    assert re.match(r"^sha256:[0-9a-f]{64}$", goal_receipt["concept_digest"])
    assert goal_receipt["result"] == "migrated"
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", goal_receipt["at"])
    assert goal_receipt["delete_policy"] == "archive-not-delete"
    team_receipt = _receipt(tmp_path, "teams", "crew")
    assert team_receipt["kind"] == "teams"
    assert team_receipt["result"] == "migrated"
    assert team_receipt["delete_policy"] == "archive-not-delete"

    # C-43 — after a complete migration the residual probe reads zero.
    probe = _payload(_run(tmp_path, "probe-residual"))
    assert probe["counts"] == {"goal": 0, "teams": 0}


# ---------------------------------------------------------------------------
# T029 / C-38 — a second run writes nothing and reports noop
# ---------------------------------------------------------------------------

def test_a_second_run_writes_nothing_and_is_a_noop(tmp_path):
    spec = "092-fixture"
    _seed_spec_goal(tmp_path, spec, slug="beta")
    _seed_spec_team(tmp_path, spec, slug="beta-crew", goal_slug="beta")
    first = _run(tmp_path, "migrate-archive", "--apply")
    assert first.returncode == 0, first.stderr

    before = _snapshot(tmp_path)
    second = _run(tmp_path, "migrate-archive", "--apply")
    assert second.returncode == 0
    decisions = _payload(second)["decisions"]
    assert {d["slug"] for d in decisions} == {"beta", "beta-crew"}
    assert {d["result"] for d in decisions} == {"noop"}
    assert _snapshot(tmp_path) == before, "a noop run must write nothing (C-38)"


# ---------------------------------------------------------------------------
# T030 / C-40 — a non-equivalent conflict names both candidates, never overwrites
# ---------------------------------------------------------------------------

def test_a_conflict_names_both_candidates_and_never_overwrites(tmp_path):
    spec = "093-fixture"
    source = _seed_spec_goal(tmp_path, spec, slug="gamma",
                             objective="Move the fixture without losing a byte.")
    target = tmp_path / ".specify/anchoring/gamma/goal.md"
    target.parent.mkdir(parents=True)
    target.write_text(
        GOAL_SOURCE.format(status="active", slug="gamma",
                           objective="A different outcome entirely.",
                           criterion="The definition survives the move."),
        encoding="utf-8")
    before = target.read_text(encoding="utf-8")

    proc = _run(tmp_path, "migrate-archive", "--apply")
    assert proc.returncode == 4, f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
    error = _payload(proc)["error"]
    assert ".specify/anchoring/gamma/goal.md" in error, error
    assert ".specify/specs/093-fixture/goal/gamma/goal.md" in error, error
    assert target.read_text(encoding="utf-8") == before, "the target must not be overwritten"
    assert (source / "goal.md").is_file(), "the source must stay readable after a refusal"
    assert not (tmp_path / TREES / spec).exists()
    assert not (tmp_path / RECEIPTS / "goal-gamma.yaml").exists()


def test_a_binding_only_difference_is_not_a_conflict(tmp_path):
    """C-40's last sentence: the binding block is excluded from the comparison."""
    spec = "093b-fixture"
    source = _seed_spec_goal(tmp_path, spec, slug="delta")
    target = tmp_path / ".specify/anchoring/delta/goal.md"
    target.parent.mkdir(parents=True)
    target.write_text(
        source.joinpath("goal.md").read_text(encoding="utf-8")
        .replace("updated: 2026-11-09\n",
                 "updated: 2026-11-09\nbinding:\n  owner: command-run\n"
                 "  owner_id: r20261109T064500Z-094a\n  origin: null\n"),
        encoding="utf-8")
    before = target.read_text(encoding="utf-8")

    proc = _run(tmp_path, "migrate-archive", "--apply")
    assert proc.returncode == 0, f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
    assert target.read_text(encoding="utf-8") == before, (
        "an equivalent target must not be overwritten by the migration (C-38)")
    assert (tmp_path / TREES / spec / "goal/delta/goal.md").is_file()
    assert _receipt(tmp_path, "goal", "delta")["result"] == "migrated"


# ---------------------------------------------------------------------------
# T035 / C-33 — the receipt carries every mandatory field
# ---------------------------------------------------------------------------

def test_the_receipt_carries_every_mandatory_field(tmp_path):
    spec = "094-fixture"
    _seed_spec_goal(tmp_path, spec, slug="epsilon")
    assert _run(tmp_path, "migrate-archive", "--apply").returncode == 0

    receipt = _receipt(tmp_path, "goal", "epsilon")
    required = {"kind", "source_spec", "source_slug", "target_slug", "target_path",
                "archived_path", "concept_digest", "result", "at", "delete_policy"}
    assert set(receipt) == required, f"receipt fields drifted: {sorted(receipt)}"


# ---------------------------------------------------------------------------
# T036 / C-33/C-34 — the two receipt shapes stay distinct and are not a read surface
# ---------------------------------------------------------------------------

def test_archive_and_migration_receipts_are_distinguishable_and_not_a_read_surface(tmp_path):
    spec = "095-fixture"
    _seed_spec_goal(tmp_path, spec, slug="zeta")
    assert _run(tmp_path, "migrate-archive", "--apply").returncode == 0
    assert _receipt(tmp_path, "goal", "zeta")["result"] in (
        "migrated", "noop", "conflict", "interrupted")

    # An archive receipt lives in the same directory family with `result: archived`.
    archive_receipt = tmp_path / RECEIPTS / "goal-retired-ghost.yaml"
    archive_receipt.write_text(
        "kind: goal\nsource_spec: 095-fixture\nsource_slug: ghost\n"
        "target_slug: ghost\ntarget_path: .specify/anchoring/ghost/goal.md\n"
        "archived_path: .specify/anchoring/ghost/concept.md\n"
        "concept_digest: sha256:" + "0" * 64 + "\nresult: archived\n"
        "at: 2026-11-09T00:00:00Z\ndelete_policy: archive-not-delete\n",
        encoding="utf-8")

    listing = _payload(_run(tmp_path, "list"))
    assert all(row["slug"] != "ghost" for row in listing["goals"]), (
        "a receipt must never be read as a current fact (C-34)")
    missing = _run(tmp_path, "binding", "goal", "ghost")
    assert missing.returncode == 3, (
        f"a receipt is not a definition; got {missing.returncode}: {missing.stdout!r}")


# ---------------------------------------------------------------------------
# T037 / C-36 — origin set, body verbatim, no cross-definition lineage rebuilt
# ---------------------------------------------------------------------------

def test_origin_is_set_and_no_lineage_is_rebuilt(tmp_path):
    spec = "096-fixture"
    goal_tree = _seed_spec_goal(tmp_path, spec, slug="eta")
    team_tree = _seed_spec_team(tmp_path, spec, slug="eta-crew", goal_slug="eta")
    goal_body = _body(goal_tree.joinpath("goal.md").read_text(encoding="utf-8"))
    team_body = _body(team_tree.joinpath("team.md").read_text(encoding="utf-8"))

    assert _run(tmp_path, "migrate-archive", "--apply").returncode == 0

    goal_target = tmp_path / ".specify/anchoring/eta/goal.md"
    team_target = tmp_path / ".specify/teams/eta-crew/team.md"
    assert _body(goal_target.read_text(encoding="utf-8")) == goal_body
    assert _body(team_target.read_text(encoding="utf-8")) == team_body
    team_text = team_target.read_text(encoding="utf-8")
    assert "goal_slug: eta\n" in team_text, "the one-way identity reference is preserved"
    assert f"origin: {spec}\n" in team_text, "origin names the source spec directory"
    assert "goal_snapshot" not in team_text and "lineage:" not in team_text


# ---------------------------------------------------------------------------
# T038 / C-37 — archive-not-delete: every source file readable under trees/
# ---------------------------------------------------------------------------

def test_every_source_file_is_readable_under_trees_after_migration(tmp_path):
    spec = "097-fixture"
    goal_tree = _seed_spec_goal(tmp_path, spec, slug="theta")
    (goal_tree / "summary").mkdir()
    (goal_tree / "summary" / "summary.md").write_text("derived summary\n", encoding="utf-8")
    (goal_tree / "notes.txt").write_text("an owned file\n", encoding="utf-8")
    team_tree = _seed_spec_team(tmp_path, spec, slug="theta-crew", goal_slug="theta")
    (team_tree / "runs").mkdir()
    (team_tree / "runs" / "20261109T000000Z-report.md").write_text(
        "run report\n", encoding="utf-8")

    original: dict[str, str] = {}
    for tree in (goal_tree, team_tree):
        for path in tree.rglob("*"):
            if path.is_file():
                original[str(path.relative_to(tmp_path))] = path.read_text(encoding="utf-8")

    assert _run(tmp_path, "migrate-archive", "--apply").returncode == 0

    archived_goal = tmp_path / TREES / spec / "goal/theta"
    archived_team = tmp_path / TREES / spec / "teams/theta-crew"
    restored: dict[str, str] = {}
    for tree in (archived_goal, archived_team):
        for path in tree.rglob("*"):
            if path.is_file():
                restored[path.name + str(len(restored))] = path.read_text(encoding="utf-8")
    assert sorted(restored.values()) == sorted(original.values()), (
        "every source file must stay readable under trees/ (archive-not-delete)")


# ---------------------------------------------------------------------------
# T041 / C-42 — the dry run writes nothing and agrees with the real run
# ---------------------------------------------------------------------------

def test_the_dry_run_writes_nothing_and_agrees_with_the_real_run(tmp_path):
    spec = "098-fixture"
    _seed_spec_goal(tmp_path, spec, slug="iota")
    _seed_spec_team(tmp_path, spec, slug="iota-crew", goal_slug="iota")

    dry = _run(tmp_path, "migrate-archive", "--dry-run")
    assert dry.returncode == 0, dry.stderr
    assert not (tmp_path / ".specify" / "archive").exists(), (
        "the dry run writes nothing — no archive directory, no receipt, no definition")
    assert not (tmp_path / ".specify" / "anchoring").exists()
    planned = _payload(dry)["decisions"]
    assert {d["result"] for d in planned} == {"migrated"}
    for decision in planned:
        assert decision["receipt"]["delete_policy"] == "archive-not-delete"

    real = _run(tmp_path, "migrate-archive", "--apply")
    assert real.returncode == 0, real.stderr
    executed = _payload(real)["decisions"]
    assert ([(d["kind"], d["slug"], d["result"]) for d in executed]
            == [(d["kind"], d["slug"], d["result"]) for d in planned]), (
        "the dry run and the real run must reach the same decisions (C-42)")
    for decision in executed:
        receipt = _receipt(tmp_path, decision["kind"], decision["slug"])
        for key, value in decision["receipt"].items():
            if key == "at":
                continue
            assert receipt[key] == str(value)


# ---------------------------------------------------------------------------
# T078 engine half / C-43, C-44, C-49 — read-only probe, scratch area ignored
# ---------------------------------------------------------------------------

def test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area(tmp_path):
    goal_tree = _seed_spec_goal(tmp_path, "099-fixture", slug="kappa")
    team_tree = _seed_spec_team(tmp_path, "099-fixture", slug="kappa-crew",
                                goal_slug="kappa")
    decoy = tmp_path / ".specify/.tmp/s094/repo/.specify/specs/900-x/goal/decoy"
    decoy.mkdir(parents=True)
    (decoy / "goal.md").write_text("decoy definition\n", encoding="utf-8")

    before = _snapshot(tmp_path)
    proc = _run(tmp_path, "probe-residual")
    assert proc.returncode == 0
    payload = _payload(proc)
    assert payload["counts"] == {"goal": 1, "teams": 1}
    assert payload["residuals"]["goal"] == [
        ".specify/specs/099-fixture/goal/kappa/goal.md"]
    assert payload["residuals"]["teams"] == [
        ".specify/specs/099-fixture/team/kappa-crew/team.md"]
    assert all("decoy" not in path for rows in payload["residuals"].values()
               for path in rows), "the run scratch area is never enumerated (C-49)"
    assert _snapshot(tmp_path) == before, "the probe writes nothing (C-43)"

    listing = _payload(_run(tmp_path, "list"))
    assert listing["goals"] == [], "a residual is never read as a current definition (C-44)"
    assert goal_tree.is_dir() and team_tree.is_dir()


def test_no_other_action_invokes_the_migration(tmp_path):
    """C-50 — migration never runs implicitly; only the explicit action moves trees."""
    spec = "100-fixture"
    source = _seed_spec_goal(tmp_path, spec, slug="lambda")
    for args in (("list",), ("probe-residual",), ("validate", "lambda"),
                 ("binding", "goal", "lambda")):
        _run(tmp_path, *args)
    assert source.joinpath("goal.md").is_file()
    assert not (tmp_path / ".specify" / "archive").exists()
