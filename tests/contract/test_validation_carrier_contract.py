"""Contract test: the read-only validation/detection fan-out carrier rule.

Owner documents:

* ``shared/definitions/subagent-definitions.md`` § Mode Selection -- carrier taxonomy
  (native / virtual / external) and the rule that a host session-creation API is not a carrier;
* ``shared/workflow/execution-topology.md`` § Carrier decision -- the local-topology
  carve-out that the validation/detection fan-out is worker dispatch, not stage dispatch;
* ``shared/workflow/external-dispatch-recipes.md`` § Recipe 7 -- the concrete read-only
  command shape (visibility triplet, no session persistence, write-tool allowlist);
* ``skills/internal/analyze-artifacts/references/{validation-and-report,detection-and-severity}.md``
  -- the dispatch-time rule the analyzing agent actually reads;
* ``skills/external/sdd-loop-driver/{SKILL.md,references/dispatch-recipes.md}`` -- the
  conflicting stage-dispatch prohibition, scoped to stage dispatch only.

The defect this guards (2026-10-28, xuanji-iac analyze run): the analyze executor was a
non-nesting subagent, read a carrier-less "validation subagent" instruction plus a blanket
local ``qodercli`` prohibition, and met the wave with the host's ``create_chat_session`` API --
producing five user-visible standard sessions instead of ephemeral read-only workers.

Set ``SPEC_KIT_CONTRACT_ROOT`` to run the same assertions against a prepared tree; the
negative check for this suite copies the seven source/mirror pairs into a temp root, deletes
the carrier bullet, and requires this suite to fail.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPEC_KIT_CONTRACT_ROOT", REPO_ROOT))

# canonical source -> runtime mirror (external skills flatten to .specify/skills/<name>)
PAIRS = {
    "shared/definitions/subagent-definitions.md": "shared/definitions/subagent-definitions.md",
    "shared/workflow/execution-topology.md": "shared/workflow/execution-topology.md",
    "shared/workflow/external-dispatch-recipes.md": "shared/workflow/external-dispatch-recipes.md",
    "skills/internal/analyze-artifacts/references/validation-and-report.md": (
        "skills/internal/analyze-artifacts/references/validation-and-report.md"
    ),
    "skills/internal/analyze-artifacts/references/detection-and-severity.md": (
        "skills/internal/analyze-artifacts/references/detection-and-severity.md"
    ),
    "skills/external/sdd-loop-driver/references/dispatch-recipes.md": (
        "skills/sdd-loop-driver/references/dispatch-recipes.md"
    ),
    "skills/external/sdd-loop-driver/SKILL.md": "skills/sdd-loop-driver/SKILL.md",
}

VALIDATION = "skills/internal/analyze-artifacts/references/validation-and-report.md"
DETECTION = "skills/internal/analyze-artifacts/references/detection-and-severity.md"
SUBAGENT = "shared/definitions/subagent-definitions.md"
RECIPES = "shared/workflow/external-dispatch-recipes.md"
TOPOLOGY = "shared/workflow/execution-topology.md"
DRIVER_RECIPES = "skills/external/sdd-loop-driver/references/dispatch-recipes.md"
DRIVER_SKILL = "skills/external/sdd-loop-driver/SKILL.md"


def _read(rel: str) -> str:
    path = ROOT / rel
    assert path.is_file(), f"missing contract document: {rel}"
    return path.read_text(encoding="utf-8")


def _bypass_lines(text: str) -> list[str]:
    """Lines that both name a session-creation API and carry a prohibition token."""
    tokens = ("create_chat_session", "fork_chat_session")
    prohibitions = ("PROHIBITED", "MUST NOT", "禁止")
    return [
        line
        for line in text.splitlines()
        if any(t in line for t in tokens) and any(p in line for p in prohibitions)
    ]


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_validation_wave_has_carrier_and_prohibition(root_kind: str) -> None:
    rel = VALIDATION if root_kind == "source" else f".specify/{PAIRS[VALIDATION]}"
    text = _read(rel)
    assert "Dispatch carrier" in text
    assert "workers, never sessions" in text
    assert "subagent-definitions.md" in text
    assert "external read-only CLI" in text
    assert "external-dispatch-recipes.md" in text
    assert "git status --porcelain" in text
    assert _bypass_lines(text), "session-creation API must be named in a prohibition line"
    assert "not a successful" in text and "fallback" in text


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_detection_delegation_uses_same_carrier(root_kind: str) -> None:
    rel = DETECTION if root_kind == "source" else f".specify/{PAIRS[DETECTION]}"
    text = _read(rel)
    assert "workers, never sessions" in text
    assert "subagent-definitions.md" in text
    assert "create_chat_session" in text
    assert _bypass_lines(text)


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_mode_selection_excludes_session_creation(root_kind: str) -> None:
    rel = SUBAGENT if root_kind == "source" else f".specify/{PAIRS[SUBAGENT]}"
    text = _read(rel)
    assert "Session-creation APIs are not a carrier" in text
    assert "create_chat_session" in text
    assert "non-nesting subagent" in text
    assert "External (one process per worker, parallel)" in text


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_external_recipe_carries_read_only_fanout(root_kind: str) -> None:
    rel = RECIPES if root_kind == "source" else f".specify/{PAIRS[RECIPES]}"
    text = _read(rel)
    assert "Recipe 7 — Read-only Validation Fan-out" in text
    assert "--no-session-persistence" in text
    assert "dispatch.sh" in text
    assert "git status --porcelain" in text
    assert _bypass_lines(text)


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_local_topology_scopes_prohibition_to_stage_dispatch(root_kind: str) -> None:
    rel = TOPOLOGY if root_kind == "source" else f".specify/{PAIRS[TOPOLOGY]}"
    text = _read(rel)
    assert "Analysis/validation fan-out is not stage dispatch" in text
    assert "subagent-definitions.md" in text
    assert "never a session-creation API" in text


@pytest.mark.parametrize("root_kind", ["source", "mirror"])
def test_sdd_driver_carveout_is_visible(root_kind: str) -> None:
    recipes_rel = DRIVER_RECIPES if root_kind == "source" else f".specify/{PAIRS[DRIVER_RECIPES]}"
    skill_rel = DRIVER_SKILL if root_kind == "source" else f".specify/{PAIRS[DRIVER_SKILL]}"
    recipes = _read(recipes_rel)
    skill = _read(skill_rel)
    assert "验证波" in recipes
    assert "subagent-definitions.md" in recipes
    assert _bypass_lines(recipes)
    assert "阶段派发 MUST NOT 启动 qodercli" in skill
    assert "验证波例外" in skill


def test_source_and_mirror_are_byte_identical() -> None:
    for source_rel, mirror_rel in PAIRS.items():
        source = (ROOT / source_rel).read_bytes()
        mirror = (ROOT / ".specify" / mirror_rel).read_bytes()
        assert source == mirror, f"mirror drift: {mirror_rel} != {source_rel} (run sync-mirrors.py)"
