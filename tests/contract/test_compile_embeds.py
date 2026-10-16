"""Contract tests: compile-embeds [C3] compiler semantics (056 US3, T018).

Guards, over a sandbox workspace (registry copy + engines + synthetic units):
determinism (recompile byte-identical), zero-effective-handler units emit no
`## Wrap-up`, `--check` drift pre-check (exit 0 clean / exit 1 drift, never
writes), and the compiled-form contract — single `## Wrap-up` with the
AUTO-GENERATED banner replacing the manual `## Feedback` / `## Documentation`
spans (title-migration duty), handlers in ascending order, skill gate line.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from tests.script_api import probe_utils

REPO_ROOT = Path(__file__).resolve().parents[2]

_REGISTRY = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
_ENGINE_COPIES = (
    "probe-utils.py",
    "feedback-utils.py",
    "scan-confirmation-gates.py",
    "run-determination.py",
    "trigger-utils.py",
    "exec-quant.py",
)
_OWNER_COPIES = (
    ("shared/workflow/feedback-step.md", "shared/workflow"),
    ("shared/workflow/docs-step.md", "shared/workflow"),
    ("skills/internal/create-team/SKILL.md", "skills/internal/create-team"),
    ("shared/guidelines/confirmation-gates.md", "shared/guidelines"),
)

_UNIT_A = """---
description: sandbox unit A
---

# /speckit.sandbox-a

## Body

Work happens here.

## Feedback

Manual feedback face of unit A.

## Documentation

Manual docs face of unit A.
"""

_UNIT_B = """---
description: sandbox unit B
---

# /speckit.sandbox-b

## Feedback

Manual feedback face of unit B.
"""

_SKILL_UNIT = """---
name: sandbox-skill
---

# sandbox-skill

## Workflow

Do the thing.

## Feedback

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, skip.

Manual feedback face of the sandbox skill.
"""


def _build_workspace(tmp_path: Path, registry_text: str) -> Path:
    ws = tmp_path / "ws"
    (ws / ".specify" / "shared" / "definitions").mkdir(parents=True)
    (ws / "shared" / "workflow").mkdir(parents=True)
    (ws / "scripts" / "python").mkdir(parents=True)
    (ws / "templates" / "commands").mkdir(parents=True)
    (ws / "skills" / "internal" / "sandbox-skill").mkdir(parents=True)
    # The engine reads the registry from the .specify/ runtime face; owner
    # paths resolve against the workspace root (framework source face).
    (ws / ".specify" / "shared" / "definitions" / "probe-definitions.md").write_text(
        registry_text, encoding="utf-8")
    # Mirror the non-entity catalog's pointer targets (validate requires each
    # declared path to exist relative to the workspace root).
    catalog = re.search(
        r"^## 非实体 probe 目录\n(.*?)(?=^## )", registry_text,
        re.MULTILINE | re.DOTALL)
    if catalog:
        for target in re.findall(r"^- `([^`]+)` — ", catalog.group(1), re.MULTILINE):
            dest = ws / target
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text((REPO_ROOT / target).read_text(encoding="utf-8"),
                            encoding="utf-8")
    for rel, _dir in _OWNER_COPIES:
        dest = ws / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = (REPO_ROOT / rel).read_text(encoding="utf-8")
        if rel.startswith(("templates/", "skills/")):
            # Owner copies under a scan path must not become compile units of
            # their own: strip the compiled Wrap-up face (owner validation only
            # needs the anchor headings).
            idx = body.find("\n## Wrap-up")
            if idx != -1:
                body = body[:idx] + "\n"
        dest.write_text(body, encoding="utf-8")
    for name in _ENGINE_COPIES:
        (ws / "scripts" / "python" / name).write_text(
            (REPO_ROOT / "scripts" / "python" / name).read_text(encoding="utf-8"),
            encoding="utf-8")
    (ws / "templates" / "commands" / "sandbox-a.md").write_text(
        _UNIT_A, encoding="utf-8")
    (ws / "templates" / "commands" / "sandbox-b.md").write_text(
        _UNIT_B, encoding="utf-8")
    (ws / "skills" / "internal" / "sandbox-skill" / "SKILL.md").write_text(
        _SKILL_UNIT, encoding="utf-8")
    return ws


def _unit_paths(ws: Path) -> dict:
    return {
        "/speckit.sandbox-a": ws / "templates" / "commands" / "sandbox-a.md",
        "/speckit.sandbox-b": ws / "templates" / "commands" / "sandbox-b.md",
        "skill:sandbox-skill": ws / "skills" / "internal" / "sandbox-skill" / "SKILL.md",
    }


def _digests(ws: Path) -> dict:
    return {uid: hashlib.sha256(p.read_bytes()).hexdigest()
            for uid, p in _unit_paths(ws).items()}


def _run(ws: Path, capsys, *extra: str) -> dict:
    rc = probe_utils.main(["--action", "compile-embeds",
                           "--workspace-root", str(ws), "--format", "json",
                           *extra])
    out = capsys.readouterr().out
    return rc, json.loads(out)


@pytest.mark.contract
def test_compile_embeds_determinism(tmp_path, capsys):
    ws = _build_workspace(tmp_path, _REGISTRY.read_text(encoding="utf-8"))
    rc1, p1 = _run(ws, capsys)
    assert rc1 == 0
    assert sorted(p1["written"]) == ["/speckit.sandbox-a", "/speckit.sandbox-b",
                                     "skill:sandbox-skill"]
    first = _digests(ws)
    rc2, p2 = _run(ws, capsys)
    assert rc2 == 0
    assert p2["written"] == [] and p2["unchanged"] == 3
    assert _digests(ws) == first, "recompile from unchanged registry must be byte-identical"


@pytest.mark.contract
def test_compile_embeds_zero_handler_no_section(tmp_path, capsys):
    # Re-scope the four all-rows to an object no sandbox unit owns: sandbox
    # units get zero effective handlers at the wrap-up point.
    registry = _REGISTRY.read_text(encoding="utf-8").replace(
        "| @point:wrap-up | all |", "| @point:wrap-up | speckit-analyze-wrapup |")
    ws = _build_workspace(tmp_path, registry)
    rc, payload = _run(ws, capsys)
    assert rc == 0
    assert sorted(payload["zero_section"]) == ["/speckit.sandbox-a",
                                               "/speckit.sandbox-b",
                                               "skill:sandbox-skill"]
    for path in _unit_paths(ws).values():
        text = path.read_text(encoding="utf-8")
        assert not [ln for ln in text.splitlines()
                    if ln.strip() == "## Wrap-up"], \
            "zero-effective-handler unit must emit no Wrap-up section"


@pytest.mark.contract
def test_compile_embeds_check_clean_and_drift(tmp_path, capsys):
    ws = _build_workspace(tmp_path, _REGISTRY.read_text(encoding="utf-8"))
    rc, _ = _run(ws, capsys)
    assert rc == 0
    rc, payload = _run(ws, capsys, "--check")
    assert rc == 0 and payload["drift"] == []

    drifted = _unit_paths(ws)["/speckit.sandbox-b"]
    drifted.write_text(drifted.read_text(encoding="utf-8").replace(
        "3. Feedback Record", "3. Feedback Record (hand-edited)"), encoding="utf-8")
    rc, payload = _run(ws, capsys, "--check")
    assert rc == 1, "--check must exit 1 on drift"
    assert payload["drift"] == ["/speckit.sandbox-b"]
    assert "(hand-edited)" in drifted.read_text(encoding="utf-8"), \
        "--check must never write"


@pytest.mark.contract
def test_compiled_form_contract(tmp_path, capsys):
    ws = _build_workspace(tmp_path, _REGISTRY.read_text(encoding="utf-8"))
    rc, _ = _run(ws, capsys)
    assert rc == 0

    text_a = _unit_paths(ws)["/speckit.sandbox-a"].read_text(encoding="utf-8")
    headings = [ln.strip() for ln in text_a.splitlines() if ln.startswith("## ")]
    assert headings == ["## Body", "## Wrap-up"], \
        "manual Feedback/Documentation spans must migrate into one Wrap-up"
    assert "AUTO-GENERATED by probe-utils.py --action compile-embeds" in text_a
    assert "do not edit; edit the registry, then recompile" in text_a
    order = [ln for ln in text_a.splitlines() if ln[:3] in ("1. ", "2. ", "3. ", "4. ", "5. ")]
    assert [ln.split(" — ")[0] for ln in order] == [
        "1. Run Determination", "2. Exec Quant", "3. Feedback Record",
        "4. Threshold Notice", "5. Token Reflection"]
    assert "--unit-id \"/speckit.sandbox-a\" --unit-type command" in text_a
    assert "docs-sync" not in text_a, \
        "docs-sync rows are per-command-object; units without that object get no line"

    text_s = _unit_paths(ws)["skill:sandbox-skill"].read_text(encoding="utf-8")
    assert "Runtime-mode gate" in text_s, "skill units keep the runtime-mode gate"
    assert "--unit-type skill" in text_s
    assert "## Documentation" not in text_s
