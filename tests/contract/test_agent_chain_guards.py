"""Contract test: chain closure + manifest correspondence
(contracts/teaching-and-guards.md C-9, C-10).

The wiring half (create-team step markers) is guarded by
test_seat_instantiation_flow.py; this file guards the RUNTIME half of the
chain (an instantiated seat definition renders onto the host registration
surface with its capacity fields) and the manifest↔definition correspondence
(SC-003's guard form), including the third-party edge case.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from specify_cli import app

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

SEAT_DEF = (
    "---\n"
    'name: "Stage Executor"\n'
    'description: "Executes one stage of the serial chain."\n'
    "user-invocable: true\n"
    "model-tier: auto\n"
    "capability-tools: [Read, Grep, Bash]\n"
    "run-turn-budget: 25\n"
    "team-scope: demo-team\n"
    "---\n"
    "Body of the seat executor.\n"
)


def _project(tmp_path):
    root = tmp_path / "proj"
    inst = root / ".specify" / "agents" / "instances"
    inst.mkdir(parents=True)
    (inst / "stage-executor.agent.md").write_text(SEAT_DEF)
    return root


def _render(root, tool="qoder"):
    prev = os.getcwd()
    os.chdir(root)
    try:
        return CliRunner().invoke(app, ["render-agents", "--ai", tool])
    finally:
        os.chdir(prev)


def test_c9_chain_closure_seat_reaches_host_surface(tmp_path):
    root = _project(tmp_path)
    result = _render(root)
    assert result.exit_code == 0, result.output
    seat = root / ".qoder" / "agents" / "stage-executor.agent.md"
    assert seat.is_file() and not seat.is_symlink()
    content = seat.read_text(encoding="utf-8")
    assert "tools" in content and "maxTurns" in content
    assert "Stage Executor" in content
    # wiring half also present on the shipped surface
    skill = (REPO_ROOT / "skills" / "create-team" / "SKILL.md").read_text(encoding="utf-8")
    assert "seat instantiation" in skill and "specify render-agents" in skill


def test_c9_manifest_records_rendered_seat(tmp_path):
    root = _project(tmp_path)
    result = _render(root)
    assert result.exit_code == 0, result.output
    manifest = json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text(encoding="utf-8")
    )
    assert any(
        "stage-executor" in rel for rel in manifest["entries"]
    ), manifest["entries"].keys()


def test_c10_manifest_definition_correspondence(tmp_path):
    root = _project(tmp_path)
    result = _render(root)
    assert result.exit_code == 0, result.output
    manifest = json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text(encoding="utf-8")
    )
    sources = {entry["source"] for entry in manifest["entries"].values()}
    # every manifest source resolves to a definition file in the neutral layers
    for source in sources:
        assert (root / ".specify" / "agents" / source).is_file(), source
    # every definition file (glob, no hand list) is covered by the manifest
    defs = set()
    for layer in ("templates", "instances"):
        layer_dir = root / ".specify" / "agents" / layer
        if layer_dir.is_dir():
            defs.update(f"{layer}/{p.name}" for p in layer_dir.glob("*.agent.md"))
    assert defs == sources, (defs, sources)


def test_c10_foreign_user_file_not_flagged(tmp_path):
    root = _project(tmp_path)
    result = _render(root)
    assert result.exit_code == 0, result.output
    # a user-owned agent beside the rendered products
    foreign = root / ".qoder" / "agents" / "my-own-agent.md"
    foreign.write_text("---\nname: Mine\ndescription: User asset.\n---\nBody.\n")
    # correspondence check re-run read-only: foreign file is NOT in the manifest
    # and is NOT a definition — it must not break the correspondence invariant
    manifest = json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text(encoding="utf-8")
    )
    sources = {entry["source"] for entry in manifest["entries"].values()}
    defs = set()
    for layer in ("templates", "instances"):
        layer_dir = root / ".specify" / "agents" / layer
        if layer_dir.is_dir():
            defs.update(f"{layer}/{p.name}" for p in layer_dir.glob("*.agent.md"))
    assert defs == sources
    assert not any("my-own-agent" in rel for rel in manifest["entries"])
    # and a second render does not delete it (user assets never pruned)
    result2 = _render(root)
    assert result2.exit_code == 0, result2.output
    assert foreign.is_file()
