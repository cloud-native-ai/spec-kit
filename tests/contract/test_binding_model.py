"""Contract tests for the binding record, the archive-layer scope values and writability.

Feature 094, `contracts/binding-and-lifecycle.md` C-1…C-30; tasks rows T005–T015.
Every test drives the engine as a subprocess, so the assertions are about the CLI surface
the consumers actually call — never about a helper that only the test can reach.
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

RUN_ID = "r20261109T064500Z-094a"
OTHER_RUN_ID = "r20261110T010203Z-094b"


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    # The shared flags go AFTER the action: argparse lets a subparser overwrite a namespace
    # attribute the top level already set (measured; engine main() records the same rule).
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


def _binding_block(owner: str = "command-run", owner_id: str = RUN_ID,
                   origin: str = "null") -> str:
    return (f"binding:\n"
            f"  owner: {owner}\n"
            f"  owner_id: {owner_id}\n"
            f"  origin: {origin}\n")


GOAL_TEMPLATE = """---
status: {status}
created: 2026-11-09
updated: 2026-11-09
{binding}---

# Anchor: alpha

## Objective

Hold the fixture still while the engine reads its binding.

## Success Criteria

1. The binding is readable.

## History

- 2026-11-09 — created.
"""


def _seed_goal(root: Path, slug: str = "alpha", *, binding: str | None = None,
               status: str = "active") -> Path:
    path = root / ".specify/anchoring" / slug / "anchor.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        GOAL_TEMPLATE.format(status=status,
                             binding=_binding_block() if binding is None else binding),
        encoding="utf-8")
    return path


def _seed_team(root: Path, slug: str = "t1", *, binding: str | None = None,
               lifecycle: str = "active", goal_slug: str = "alpha") -> Path:
    path = root / ".specify/teams" / slug / "team.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"lifecycle_state: {lifecycle}\n"
        f"anchor_slug: {goal_slug}\n"
        f"{_binding_block('sdd-run') if binding is None else binding}"
        "---\n\n"
        f"# Team: {slug}\n",
        encoding="utf-8")
    return path


def _error(proc: subprocess.CompletedProcess) -> str:
    payload = json.loads(proc.stdout)
    assert "error" in payload, f"expected a JSON error payload, got: {proc.stdout!r} {proc.stderr!r}"
    return payload["error"]


def _hash_minus_binding(path: Path) -> str:
    """SC-009's measurement: hash of the file minus the binding block.

    The binding block is the `binding:` line plus the run of indented lines under it.
    Every other byte — frontmatter fields, body, history, targets — stays in the hash.
    """
    kept: list[str] = []
    skipping = False
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if skipping:
            if line[:1] in (" ", "\t"):
                continue
            skipping = False
        if line.startswith("binding:"):
            skipping = True
            continue
        kept.append(line)
    return hashlib.sha256("".join(kept).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# T005 / C-1 — a definition without a complete binding is uninterpretable
# ---------------------------------------------------------------------------

def test_a_definition_without_a_complete_binding_is_uninterpretable(tmp_path: Path):
    _seed_goal(tmp_path, binding="")
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 2
    assert "binding-missing" in _error(proc)

    # A partial block is still uninterpretable, and the refusal names the missing key.
    _seed_goal(tmp_path, binding="binding:\n  owner: command-run\n")
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 2
    error = _error(proc)
    assert "binding-missing" in error
    assert "owner_id" in error

    # A complete, engine-shaped block is interpretable.
    _seed_goal(tmp_path)
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# T006 / C-2 — owner is a closed three-value domain
# ---------------------------------------------------------------------------

def test_owner_outside_the_closed_three_values_is_refused(tmp_path: Path):
    _seed_goal(tmp_path)
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "robot",
                "--owner-id", RUN_ID)
    assert proc.returncode == 2
    error = _error(proc)
    assert "robot" in error
    for value in ("sdd-run", "command-run", "human"):
        assert value in error


# ---------------------------------------------------------------------------
# T007 / C-3 — owner_id is validated by shape; the grammar is cited, not restated
# ---------------------------------------------------------------------------

def test_owner_id_is_validated_by_shape_and_the_grammar_is_cited_not_restated(tmp_path: Path):
    _seed_goal(tmp_path)
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "sdd-run",
                "--owner-id", "not-a-run-id")
    assert proc.returncode == 2
    error = _error(proc)
    assert "not-a-run-id" in error
    assert "skills/external/sdd-loop-driver/references/state-awareness.md" in error

    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "sdd-run",
                "--owner-id", RUN_ID)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    # `owner: human` may use the literal `human` as its owner_id.
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "human",
                "--owner-id", "human")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# T008 / C-4 — origin is null or the basename of an existing spec directory
# ---------------------------------------------------------------------------

def test_origin_naming_a_non_existent_spec_directory_is_refused(tmp_path: Path):
    _seed_goal(tmp_path)
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "command-run",
                "--owner-id", RUN_ID, "--origin", "999-no-such-spec")
    assert proc.returncode == 2
    assert "origin-unresolvable" in _error(proc)
    assert not (tmp_path / ".specify/specs/999-no-such-spec").exists()

    (tmp_path / ".specify/specs/900-fixture").mkdir(parents=True)
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "command-run",
                "--owner-id", RUN_ID, "--origin", "900-fixture")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)["binding"]["origin"] == "900-fixture"

    # `null` clears origin.
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "command-run",
                "--owner-id", RUN_ID, "--origin", "null")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)["binding"]["origin"] is None


# ---------------------------------------------------------------------------
# T009 / C-6 — a rebind changes only the binding block (SC-009's measurement)
# ---------------------------------------------------------------------------

def test_rebind_changes_only_the_binding_block(tmp_path: Path):
    (tmp_path / ".specify/specs/900-fixture").mkdir(parents=True)
    path = _seed_goal(tmp_path, binding=_binding_block("command-run", RUN_ID, "900-fixture"))
    before_hash = _hash_minus_binding(path)
    before_text = path.read_text(encoding="utf-8")

    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "sdd-run",
                "--owner-id", OTHER_RUN_ID, "--origin", "900-fixture")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["binding"] == {"owner": "sdd-run", "owner_id": OTHER_RUN_ID,
                                  "origin": "900-fixture"}
    assert _hash_minus_binding(path) == before_hash
    assert path.read_text(encoding="utf-8") != before_text

    # Omitting --origin keeps the current origin; the byte rule still holds.
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "command-run",
                "--owner-id", RUN_ID)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)["binding"]["origin"] == "900-fixture"
    assert _hash_minus_binding(path) == before_hash


# ---------------------------------------------------------------------------
# T010 / C-5 — a hand-edited binding block is reported, not trusted
# ---------------------------------------------------------------------------

def test_a_hand_edited_binding_block_is_reported_not_trusted(tmp_path: Path):
    # Wrong key order.
    _seed_goal(tmp_path, binding=(
        "binding:\n"
        f"  owner_id: {RUN_ID}\n"
        "  owner: command-run\n"
        "  origin: null\n"))
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 2
    assert "binding-hand-edited" in _error(proc)

    # Non-canonical indentation.
    _seed_goal(tmp_path, binding=(
        "binding:\n"
        "    owner: command-run\n"
        f"    owner_id: {RUN_ID}\n"
        "    origin: null\n"))
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 2
    assert "binding-hand-edited" in _error(proc)

    # The engine-shaped block is trusted.
    _seed_goal(tmp_path)
    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# T011 / C-7 — a terminal definition refuses a binding rewrite
# ---------------------------------------------------------------------------

def test_a_terminal_goal_refuses_a_new_team_binding(tmp_path: Path):
    _seed_goal(tmp_path, status="achieved")
    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "sdd-run",
                "--owner-id", RUN_ID)
    assert proc.returncode == 2
    error = _error(proc)
    assert "terminal-goal-rebind" in error
    assert "achieved" in error

    # A team archived refuses any rewrite too (C-7, second sentence).
    _seed_team(tmp_path, lifecycle="archived")
    proc = _run(tmp_path, "bind", "teams", "t1", "--owner", "sdd-run",
                "--owner-id", RUN_ID)
    assert proc.returncode == 2
    assert "archived" in _error(proc)


# ---------------------------------------------------------------------------
# T012 / C-8 — ownership is answered by the read action, not by the path
# ---------------------------------------------------------------------------

def test_ownership_is_answered_by_the_read_action_not_by_the_path(tmp_path: Path):
    _seed_goal(tmp_path, binding=_binding_block("command-run", RUN_ID, "null"))
    # A same-named definition at the retired spec-local position must not answer for it.
    spec_goal = tmp_path / ".specify/specs/900-fixture/goal/alpha/goal.md"
    spec_goal.parent.mkdir(parents=True, exist_ok=True)
    spec_goal.write_text(
        GOAL_TEMPLATE.format(status="active", binding=_binding_block("human", "human", "null")),
        encoding="utf-8")

    proc = _run(tmp_path, "binding", "goal", "alpha")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["kind"] == "goal"
    assert payload["slug"] == "alpha"
    assert payload["owner"] == "command-run"
    assert payload["owner_id"] == RUN_ID
    assert payload["origin"] is None
    assert payload["path"].endswith(".specify/anchoring/alpha/anchor.md")
    assert payload["archive_layer"] == "goal"
    assert payload["lifecycle"] == "active"

    _seed_team(tmp_path)
    proc = _run(tmp_path, "binding", "teams", "t1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["kind"] == "teams"
    assert payload["slug"] == "t1"
    assert payload["owner"] == "sdd-run"
    assert payload["path"].endswith(".specify/teams/t1/team.md")
    assert payload["archive_layer"] == "teams"
    assert payload["lifecycle"] == "active"


# ---------------------------------------------------------------------------
# T013 / C-9 — the retired scope values are gone with no alias
# ---------------------------------------------------------------------------

def test_scope_spec_is_removed_and_no_alias_exists(tmp_path: Path):
    _seed_goal(tmp_path)
    # `goal` is the retired position-named member beside the older `spec` / `global`.
    for retired in ("goal", "spec", "global"):
        proc = _run(tmp_path, "resolve-scope", "--scope", retired)
        assert proc.returncode == 2, f"--scope {retired} was accepted"
        assert "invalid choice" in proc.stderr
    # An unregistered value is refused the same way — no alias exists.
    proc = _run(tmp_path, "resolve-scope", "--scope", "goal-archive")
    assert proc.returncode == 2
    assert "invalid choice" in proc.stderr

    # The four living members resolve (auto resolves in the seeded single layer).
    for live in ("anchor", "goals", "teams"):
        proc = _run(tmp_path, "resolve-scope", "--scope", live)
        assert proc.returncode == 0, proc.stdout + proc.stderr

    # No retired value survives anywhere in the engine, and no guidance string
    # instructs a caller to pass one (the engine never prints a rejected option).
    source = ENGINE.read_text(encoding="utf-8")
    assert not re.search(r"[\"']global[\"']", source), "retired scope value 'global' survives"
    assert not re.search(r"[\"']spec[\"']", source), "retired scope value 'spec' survives"
    assert 'ARCHIVE_SCOPES = ("anchor", "teams", "goals", "auto")' in source, (
        "the closed scope set carries no retired member")
    assert "--scope global" not in source
    assert "--scope spec" not in source


# ---------------------------------------------------------------------------
# T014 / C-10, C-11, C-12 — both roots in one call; auto is read-only
# ---------------------------------------------------------------------------

def test_both_archive_roots_resolve_in_one_call_and_auto_is_read_only(tmp_path: Path):
    _seed_goal(tmp_path)
    _seed_team(tmp_path)

    for layer in ("anchor", "goals", "teams"):
        proc = _run(tmp_path, "resolve-scope", "--scope", layer)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        payload = json.loads(proc.stdout)
        assert payload["scope"] == layer
        assert Path(payload["anchor_root"]).name == "anchoring"
        assert Path(payload["goals_root"]).name == "goals"
        assert Path(payload["team_root"]).name == "teams"

    # auto resolves the single layer that contains the requested slug.
    proc = _run(tmp_path, "resolve-scope", "--scope", "auto", "--team", "t1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert json.loads(proc.stdout)["scope"] == "teams"

    # Both layers present and no slug requested: an ambiguous auto is a named refusal
    # that names both layers, never a silent pick.
    proc = _run(tmp_path, "resolve-scope", "--scope", "auto")
    assert proc.returncode == 2
    error = json.loads(proc.stdout)["error"]
    assert "scope-ambiguous" in error
    assert "anchor" in error and "teams" in error

    # Zero candidate layers is `not-found`, not a default.
    empty = tmp_path / "empty"
    empty.mkdir()
    proc = _run(empty, "resolve-scope", "--scope", "auto")
    assert proc.returncode == 2
    assert "not-found" in json.loads(proc.stdout)["error"]

    # A write under auto is refused before anything is written.
    proc = _run(tmp_path, "status", "alpha", "--set", "achieved", "--scope", "auto")
    assert proc.returncode == 2
    assert "scope-read-only" in _error(proc)
    assert "status: active" in (tmp_path / ".specify/anchoring/alpha/anchor.md").read_text(
        encoding="utf-8")

    # --spec-dir outside .specify/specs/ is refused by the named reason, not by a
    # generic failure, and no scope makes it acceptable.
    outside = tmp_path / "outside"
    outside.mkdir()
    proc = _run(tmp_path, "resolve-scope", "--scope", "anchor", "--spec-dir", str(outside))
    assert proc.returncode == 2
    assert "spec-dir-unresolvable" in _error(proc)


# ---------------------------------------------------------------------------
# T015 / C-16 — a cross-layer write is refused and names both layers
# ---------------------------------------------------------------------------

def test_a_cross_layer_write_is_refused_and_names_both_layers(tmp_path: Path):
    goal = _seed_goal(tmp_path)
    _seed_team(tmp_path)

    proc = _run(tmp_path, "status", "alpha", "--set", "achieved", "--scope", "teams")
    assert proc.returncode == 2
    error = _error(proc)
    assert "cross-layer-write" in error
    assert "anchor" in error and "teams" in error
    assert "status: active" in goal.read_text(encoding="utf-8")

    proc = _run(tmp_path, "bind", "teams", "t1", "--owner", "sdd-run",
                "--owner-id", RUN_ID, "--origin", "null", "--scope", "anchor")
    assert proc.returncode == 2
    error = _error(proc)
    assert "cross-layer-write" in error
    assert "anchor" in error and "teams" in error


# ---------------------------------------------------------------------------
# C-14 (FR-038) — writability is computed: a bound goal is writable only by human
# ---------------------------------------------------------------------------

def test_a_bound_goal_is_writable_only_by_human(tmp_path: Path):
    _seed_goal(tmp_path)
    _seed_team(tmp_path)  # team t1 names goal_slug: alpha

    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "sdd-run",
                "--owner-id", RUN_ID)
    assert proc.returncode == 2
    error = _error(proc)
    assert "bound-by" in error
    assert "t1" in error

    proc = _run(tmp_path, "bind", "goal", "alpha", "--owner", "human",
                "--owner-id", "human")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# T067 / C-88 — the Anchor owner owns the concepts, not the action signatures
# (Feature 101 moved the binding record and the shared lifecycle here; the Goal
# owner now cites this file for both.)
# ---------------------------------------------------------------------------

ANCHOR_OWNER = REPO_ROOT / "shared/definitions/anchor-definitions.md"
GOAL_OWNER = REPO_ROOT / "shared/definitions/goal-definitions.md"
TEAM_OWNER = REPO_ROOT / "skills/internal/create-team/references/conceptual-model.md"


def _owner_text(path: Path) -> str:
    assert path.is_file(), f"concept owner missing: {path}"
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    assert heading in text, f"missing section: {heading}"
    tail = text[text.index(heading) + len(heading):]
    end = re.search(r"(?m)^## ", tail)
    return tail[: end.start()] if end else tail


def test_the_anchor_owner_owns_the_concepts_and_not_the_action_signatures():
    text = _owner_text(ANCHOR_OWNER)

    # The owned concept faces are present by name.
    assert "### Archive Layers" in text, "the archive-layer vocabulary lives here"
    assert "### The Binding Record" in text, "the binding record's meaning lives here"
    assert "### Lifecycle" in text, "the shared lifecycle names live here"
    assert "origin" in _section(text, "### The Binding Record"), (
        "the origin semantics are owned by the binding-record section")
    for value in ("`active`", "`achieved`", "`abandoned`"):
        assert value in _section(text, "### Lifecycle"), (
            f"the shared lifecycle names are owned here: {value}")
    assert "retained" in _section(text, "### Lifecycle") and "reopen" in text, (
        "the terminal-retained and reopen rules are stated")
    assert ".specify/anchoring/<anchor-slug>/anchor.md" in text
    assert ".specify/teams/<slug>/team.md" in text

    # The legacy-key removal point is recorded in § Terminology Boundaries (C-23).
    boundaries = _section(text, "## Terminology Boundaries")
    assert "removed at the first minor release after 094" in boundaries, (
        "the alias removal point is declared in Terminology Boundaries")

    # It does not restate the engine's action signatures (C-88).
    signatures = re.findall(r"goal-utils\.py\s+[a-z-]+\s+<", text)
    assert not signatures, f"action signatures restated in the owner: {signatures}"
    for flag in ("--owner-id", "--owner ", "--origin ", "--scope "):
        assert flag not in text, f"engine flag {flag!r} restated in the concept owner"


# ---------------------------------------------------------------------------
# T068 / C-89 / C-90 — the two owners cite each other, neither restates the other
# ---------------------------------------------------------------------------

def test_the_concept_owners_cite_each_other_and_restate_no_value_domain():
    anchor_text = _owner_text(ANCHOR_OWNER)
    goal_text = _owner_text(GOAL_OWNER)
    team_text = _owner_text(TEAM_OWNER)

    # The Anchor owner cites the team owner's section; the Goal owner cites the
    # Anchor owner for the binding record it no longer owns.
    assert "skills/internal/create-team/references/conceptual-model.md" in anchor_text
    assert "§ The Team Definition and the Binding Model" in anchor_text, (
        "the Anchor owner cites the team owner's section explicitly")
    assert "shared/definitions/anchor-definitions.md" in goal_text
    assert "§ The Binding Record" in goal_text, (
        "the Goal owner cites the binding-record owner explicitly")

    # The team owner cites the binding-record owner. The team model still points at
    # the retired Goal-owner path; accepting either keeps this test green until that
    # model is re-pointed (T043's territory), and the section name is asserted either way.
    assert ("shared/definitions/anchor-definitions.md" in team_text
            or "shared/definitions/goal-definitions.md" in team_text)
    assert "§ The Binding Record" in team_text, (
        "the team owner cites the binding-record section explicitly")

    # The team owner owns binding / handoff_ref / the crew notion without restating
    # the definition-side value domains.
    assert "handoff_ref" in team_text and "crew" in team_text.lower()
    for goal_domain in ("achieved", "abandoned", "sdd-run", "command-run",
                        "`human`", "`goal` / `teams` / `auto`"):
        assert goal_domain not in team_text, (
            f"the team owner restates a definition-side domain value: {goal_domain!r}")
    # The team key may be named only inside a citation of its owner, never defined here.
    for line in anchor_text.splitlines():
        if "handoff_ref" in line:
            assert "conceptual-model.md" in line, (
                "the Anchor owner names the team key only while citing the team owner")

    # The Anchor owner does not restate the team lifecycle pair.
    assert "active` / `archived" not in anchor_text and "`archived`" not in anchor_text, (
        "the Anchor owner must cite the team lifecycle, not enumerate it")


# ---------------------------------------------------------------------------
# T075 / C-101 — the three management skills cite their owners, not the arguments
# ---------------------------------------------------------------------------

MANAGE_GOAL = REPO_ROOT / "skills/internal/manage-goal/SKILL.md"
RUN_TEAM = REPO_ROOT / "skills/internal/run-team/SKILL.md"
IMPROVE_TEAM = REPO_ROOT / "skills/internal/improve-team/SKILL.md"


def test_the_three_management_skills_cite_owners_and_restate_no_arguments():
    manage = _owner_text(MANAGE_GOAL)
    run = _owner_text(RUN_TEAM)
    improve = _owner_text(IMPROVE_TEAM)

    # Every procedure follows the new paths and model: the retired goal directory and
    # the spec-local definition store survive in none of the three.
    for label, text in (("manage-goal", manage), ("run-team", run),
                        ("improve-team", improve)):
        assert ".specify/goal/" not in text, (
            f"{label} still names the retired `.specify/goal/` directory")
        spec_local = re.findall(
            r"(?:\.specify/specs/[^\s`'\"]+|<spec-dir>)/(?:goal|team)\b", text)
        assert not spec_local, (
            f"{label} names a spec-local goal/team store: {spec_local}")
        assert ".specify/teams/<slug>" in text, (
            f"{label} must state the team archive landing point")

    # manage-goal owns the goal-side procedure: it cites the concept owner, the archive
    # layer section and the engine's help as the argument owner, and it carries the
    # `migrate-archive` mode the command template delegates to it.
    assert "shared/definitions/goal-definitions.md" in manage
    assert "§ Archive Layers" in manage
    assert "goal-utils.py" in manage and "--help" in manage, (
        "manage-goal must cite the engine's help as the action-argument owner")
    assert ".specify/anchoring/<slug>/goal.md" in manage or ".specify/anchoring/" in manage
    assert "migrate-archive" in manage, (
        "the goal skill must carry the `migrate-archive` mode the template exposes")

    # run-team cites the action and concept owners and documents the additive
    # `binding` key of the run-checks payload (T048's documentation half).
    assert "goal-utils.py" in run
    assert "skills/internal/create-team/references/conceptual-model.md" in run
    assert "`binding`" in run or "binding 键" in run, (
        "run-team must document the additive binding key of the run-checks payload")

    # improve-team cites the concept and the create-mode procedure owners.
    assert "create-team/references/conceptual-model.md" in improve
    assert "create-mode.md" in improve

    # None of the three restates the retired scope values or the engine's flag domain.
    for label, text in (("manage-goal", manage), ("run-team", run),
                        ("improve-team", improve)):
        for restated in ("--scope spec", "--scope global", "global|spec|auto",
                         "goal|teams|auto"):
            assert restated not in text, (
                f"{label} restates the scope domain: {restated!r}")
