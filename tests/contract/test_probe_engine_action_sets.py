"""Contract test: engine action closed sets (Feature 056 / US2, [C4]).

Pins BOTH migration sides exactly (bidirectional: extra or missing action fails):
- ``probe-utils.py`` allowed set: probes, map, probe-inject, handlers, compile-embeds
- ``feedback-utils.py`` retained set: record, status, list, dispose, mark-submitted,
  reindex, package, cleanup, upstream, migrate-legacy, introspect-register

Also owns [C2] rule 5 for the registry side: every kind=engine Handler action
must hit the REAL engine action union (feedback-utils 11 + run-determination
ACTIONS + probe-utils 5), parsed from the argparse/constant literals — never a
hand-copied list.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.script_api import ROOT

DEFS = ROOT / "shared" / "definitions" / "probe-definitions.md"
FEEDBACK_SCRIPT = ROOT / "scripts" / "python" / "feedback-utils.py"
PROBE_SCRIPT = ROOT / "scripts" / "python" / "probe-utils.py"
RUNDET_SCRIPT = ROOT / "scripts" / "python" / "run-determination.py"
EXECQUANT_SCRIPT = ROOT / "scripts" / "python" / "exec-quant.py"

FEEDBACK_ALLOWED = {
    "record", "status", "list", "dispose", "mark-submitted", "reindex",
    "package", "cleanup", "upstream", "migrate-legacy", "introspect-register",
}
PROBE_ALLOWED = {"probes", "map", "probe-inject", "handlers", "compile-embeds"}


def _action_choices(path: Path) -> set[str]:
    src = path.read_text(encoding="utf-8")
    idx = src.index('"--action"')
    m = re.search(r"choices=\[(.*?)\]", src[idx:], re.DOTALL)
    assert m, f"{path.name}: no --action choices literal found"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def _rundet_actions() -> set[str]:
    src = RUNDET_SCRIPT.read_text(encoding="utf-8")
    m = re.search(r"^ACTIONS = \(([^)]*)\)", src, re.MULTILINE)
    assert m, "run-determination.py: ACTIONS constant not found"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def _trigger_actions() -> set[str]:
    src = (p_run := Path(__file__).resolve().parents[2] / "scripts" / "python" / "trigger-utils.py").read_text(encoding="utf-8")
    m = re.search(r"^ACTIONS = \(([^)]*)\)", src, re.MULTILINE)
    assert m, "trigger-utils.py: ACTIONS constant not found"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def _execquant_actions() -> set[str]:
    src = EXECQUANT_SCRIPT.read_text(encoding="utf-8")
    m = re.search(r"^ACTIONS = \(([^)]*)\)", src, re.MULTILINE)
    assert m, "exec-quant.py: ACTIONS constant not found"
    actions = set(re.findall(r'"([^"]+)"', m.group(1)))
    return actions | _action_choices(EXECQUANT_SCRIPT)


def test_probe_utils_action_set_exact() -> None:
    assert PROBE_SCRIPT.is_file(), "probe-utils.py missing — probe family not migrated"
    got = _action_choices(PROBE_SCRIPT)
    assert got == PROBE_ALLOWED, (
        f"probe-utils.py --action set drifted: extra={sorted(got - PROBE_ALLOWED)} "
        f"missing={sorted(PROBE_ALLOWED - got)}"
    )


def test_feedback_utils_action_set_exact() -> None:
    got = _action_choices(FEEDBACK_SCRIPT)
    assert got == FEEDBACK_ALLOWED, (
        f"feedback-utils.py --action set drifted: extra={sorted(got - FEEDBACK_ALLOWED)} "
        f"missing={sorted(FEEDBACK_ALLOWED - got)}"
    )


def test_engine_action_sets_disjoint() -> None:
    probe = _action_choices(PROBE_SCRIPT) if PROBE_SCRIPT.is_file() else set()
    overlap = _action_choices(FEEDBACK_SCRIPT) & probe
    assert not overlap, f"probe/feedback engine action sets overlap: {sorted(overlap)}"


def test_exec_quant_action_set_exact() -> None:
    """059 exact-pin: the new engine's action closure, read BOTH ways
    (ACTIONS constant + argparse choices), is exactly the D1 closed set."""
    assert EXECQUANT_SCRIPT.is_file(), "exec-quant.py missing — engine not implemented"
    got = _execquant_actions()
    expected = {"collect", "list-records", "score", "collect-dispatch"}
    assert got == expected, (
        f"exec-quant.py action set drifted: extra={sorted(got - expected)} "
        f"missing={sorted(expected - got)}"
    )


def _registered_engine_actions() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    headers: list[str] | None = None
    lines = DEFS.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Handler":
            start = i + 1
            break
    assert start is not None, "registry has no ## Handler chapter"
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if set(cells) <= {"", "-", "—"} or all(set(c) <= set("-: ") for c in cells):
            continue
        if headers is None:
            headers = cells
            continue
        row = dict(zip(headers, cells))
        if row.get("kind", "") == "engine":
            rows.append((row.get("handler_id", ""), row.get("action", "").strip("`")))
    return rows


def test_registered_engine_actions_hit_real_engine_union() -> None:
    union = (_action_choices(FEEDBACK_SCRIPT) | _rundet_actions()
             | _trigger_actions())
    if PROBE_SCRIPT.is_file():
        union |= _action_choices(PROBE_SCRIPT)
    if EXECQUANT_SCRIPT.is_file():
        union |= _execquant_actions()
    registered = _registered_engine_actions()
    assert registered, "no kind=engine Handler rows registered"
    for hid, action in registered:
        assert action in union, (
            f"{hid}: kind=engine action '{action}' is not a real engine action"
        )
