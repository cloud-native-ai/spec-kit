"""Contract tests: compile reconcile guards (056 US4, T027 — red-first).

Five breakage classes over a sandbox workspace, each constructed as a mutation
and each demanded to surface with its class: orphan handler (the artifact
carries a call line the registry cannot generate → exit 2), missing handler
(a current-fingerprint artifact lacks a subscribed call line → exit 2), illegal
action (exit 2 naming the handler_id), order conflict (exit 2), wording hit
(the generator refuses the write). Plus the FR-008/FR-014 order contract pin:
h-run-determination orders before h-feedback-record and h-threshold-notice.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

from tests.script_api import probe_utils

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]


def _embeds_suite():
    path = REPO_ROOT / "tests" / "contract" / "test_compile_embeds.py"
    spec = importlib.util.spec_from_file_location("_compile_embeds_suite", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_compile_embeds_suite"] = module
    spec.loader.exec_module(module)
    return module


CE = _embeds_suite()
REGISTRY_TEXT = (REPO_ROOT / "shared" / "definitions" / "probe-definitions.md").read_text(
    encoding="utf-8")


def _compile(tmp_path, capsys, registry_text=REGISTRY_TEXT):
    ws = CE._build_workspace(tmp_path, registry_text)
    rc, _ = CE._run(ws, capsys)
    assert rc == 0, "sandbox compile must be green before the mutation"
    return ws


def _compile_check(ws, capsys):
    rc, payload = CE._run(ws, capsys, "--check")
    return rc, payload


def _unit_a(ws):
    return ws / "templates" / "commands" / "sandbox-a.md"


@pytest.mark.contract
def test_orphan_handler_line_is_structural_exit_2(tmp_path, capsys):
    ws = _compile(tmp_path, capsys)
    p = _unit_a(ws)
    p.write_text(p.read_text(encoding="utf-8").replace(
        "5. Token Reflection",
        "5. Token Reflection"), encoding="utf-8")  # no-op keeps ordering explicit
    text = p.read_text(encoding="utf-8")
    orphan = ("\n5. Ghost Handler — `python3 .specify/scripts/python/feedback-utils.py "
              "--action ghost-action --unit-id \"/speckit.sandbox-a\" "
              "--unit-type command`\n")
    p.write_text(text.rstrip("\n") + "\n" + orphan, encoding="utf-8")
    rc, payload = _compile_check(ws, capsys)
    assert rc == 2, (
        f"orphan handler line (unregistered action) must be a structural error (exit 2), "
        f"got {rc}: {payload}"
    )
    assert "/speckit.sandbox-a" in str(payload), "the drift report must name the unit"
    assert any("orphan" in str(v).lower() for v in
               (payload.get("structural") or payload.get("drift") or [payload])), \
        f"the report must name the orphan class: {payload}"


@pytest.mark.contract
def test_missing_handler_line_is_structural_exit_2(tmp_path, capsys):
    ws = _compile(tmp_path, capsys)
    p = _unit_a(ws)
    text = p.read_text(encoding="utf-8")
    # Registry unchanged ⇒ the artifact's fingerprint is still current; dropping a
    # subscribed call line is hand corruption, not a stale render.
    removed = re.sub(r"^3\. Feedback Record.*\n", "", text, flags=re.M)
    assert removed != text, "mutation must actually remove the Feedback Record line"
    p.write_text(removed, encoding="utf-8")
    rc, payload = _compile_check(ws, capsys)
    assert rc == 2, (
        f"missing subscribed handler in a current-fingerprint artifact must be a "
        f"structural error (exit 2), got {rc}: {payload}"
    )
    assert any("missing" in str(v).lower() for v in
               (payload.get("structural") or payload.get("drift") or [payload])), \
        f"the report must name the missing class: {payload}"


@pytest.mark.contract
def test_stale_render_after_registry_change_is_exit_1(tmp_path, capsys):
    """The lifecycle's exit-1 leg: a registry edit makes the artifact a stale render —
    regenerable, recompile fixes it; it must NOT be classified structural."""
    ws = _compile(tmp_path, capsys)
    registry = ws / ".specify" / "shared" / "definitions" / "probe-definitions.md"
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            "| h-token-reflection | @point:wrap-up | all |",
            "| h-token-reflection | @point:wrap-up | speckit-analyze-wrapup |"),
        encoding="utf-8")
    rc, payload = _compile_check(ws, capsys)
    assert rc == 1, (
        f"a stale render after a registry edit is regenerable drift (exit 1), got {rc}: "
        f"{payload}"
    )
    assert payload.get("drift"), "the drift list must name the stale units"


@pytest.mark.contract
def test_illegal_action_exits_2_naming_handler(tmp_path, capsys):
    ws = _compile(tmp_path, capsys)
    registry = ws / ".specify" / "shared" / "definitions" / "probe-definitions.md"
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            "| h-run-determination | engine | determine |",
            "| h-run-determination | engine | ghost-action |"),
        encoding="utf-8")
    rc = probe_utils.main(["--action", "handlers", "--validate",
                           "--workspace-root", str(ws)])
    assert rc == 2, "illegal engine action must exit 2"
    err = capsys.readouterr().err
    assert "h-run-determination" in err and "ghost-action" in err, (
        f"the error must name the handler and the action: {err}"
    )


@pytest.mark.contract
def test_order_conflict_exits_2(tmp_path, capsys):
    ws = _compile(tmp_path, capsys)
    registry = ws / ".specify" / "shared" / "definitions" / "probe-definitions.md"
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            "| h-feedback-record | engine | record | non-blocking | 20 |",
            "| h-feedback-record | engine | record | non-blocking | 10 |"),
        encoding="utf-8")
    rc = probe_utils.main(["--action", "handlers", "--validate",
                           "--workspace-root", str(ws)])
    assert rc == 2, "two distinct handlers at the same point and order must exit 2"
    err = capsys.readouterr().err
    assert "h-feedback-record" in err, f"the error must name a conflicting handler: {err}"


@pytest.mark.contract
def test_wording_hit_refuses_the_write(tmp_path, capsys):
    # A registry whose rendered line would carry blocking wording: the sandbox owner
    # gains a lowercase blocking heading, an agent handler anchors on it.
    registry = REGISTRY_TEXT.replace(
        "| h-run-determination | engine | determine | non-blocking | 10 | "
        "scripts/python/run-determination.py |",
        "| h-run-determination | engine | determine | non-blocking | 10 | "
        "scripts/python/run-determination.py |\n"
        "| h-stop-and-confirm | agent | stop and confirm the draft | non-blocking "
        "| 25 | shared/workflow/feedback-step.md |")
    # Anchor at the table header separator: inserting mid-row (substring inside a
    # row carrying a 覆盖说明 cell) would corrupt the row's cells.
    registry = registry.replace(
        "| handler_id | selector | scope | 覆盖说明 |\n"
        "|------------|----------|-------|----------|",
        "| handler_id | selector | scope | 覆盖说明 |\n"
        "|------------|----------|-------|----------|\n"
        "| h-stop-and-confirm | @point:wrap-up | all | wording-gate drill row |")
    ws = CE._build_workspace(tmp_path, registry)
    owner = ws / "shared" / "workflow" / "feedback-step.md"
    owner.write_text(
        owner.read_text(encoding="utf-8")
        + "\n## stop and confirm the draft\n\nDrill heading.\n",
        encoding="utf-8")
    rc = probe_utils.main(["--action", "compile-embeds",
                           "--workspace-root", str(ws)])
    assert rc == 2, "generated wording hitting BLOCKING_PATTERNS must refuse (exit 2)"
    err = capsys.readouterr().err
    assert "wording gate" in err, f"the refusal must name the wording gate: {err}"
    for path in CE._unit_paths(ws).values():
        assert "## Wrap-up" not in path.read_text(encoding="utf-8"), \
            "a refused compile must not write any section"


@pytest.mark.contract
def test_order_contract_pinned(tmp_path, capsys):
    """FR-008/FR-014: run-determination orders before feedback-record and
    threshold-notice (the threshold consumes the determination result)."""
    text = (REPO_ROOT / ".specify" / "shared" / "definitions"
            / "probe-definitions.md").read_text(encoding="utf-8")
    handlers = {h["handler_id"]: int(h["order"])
                for h in probe_utils._table_rows(text, "Handler")}
    assert handlers["h-run-determination"] < handlers["h-feedback-record"]
    assert handlers["h-run-determination"] < handlers["h-threshold-notice"]


@pytest.mark.contract
def test_clean_tree_check_is_green(tmp_path, capsys):
    ws = _compile(tmp_path, capsys)
    rc, payload = _compile_check(ws, capsys)
    assert rc == 0 and payload.get("drift") == []
