"""Contract cases for event waits and fixed-sleep elimination (098 US4, C-001…C-010).

Owner of the propositions: `.specify/specs/098-suite-speed-optimizations/contracts/
event-wait.contract.md`. Judgement surface: AST scans over the clause-declared scope
files, the shared helper's signature and its adopted call sites, and the closed
exemption registry — never a re-implementation of a wait.

Cases:

1. ``test_c001_the_scope_is_exactly_the_clause_declared_six_files`` — the scan scope is
   derived from contract clause C-001 (closed set: six files, all present).
2. ``test_c002_the_scope_files_carry_zero_synchronization_sleep`` — AST call-site scan;
   every hit is named file and line (FR-017).
3. ``test_c003_the_exemption_registry_is_closed_and_per_line`` — exactly the two
   exemptions clause C-003 declares, each with its reason text and a live per-site
   anchor; a stale row or a scope-file exemption fails.
4. ``test_c006_c007_the_helper_defaults_are_thirty_seconds_and_a_small_interval`` — the
   shared ``wait_until`` defaults: ``timeout == 30`` and ``interval <= 0.2``.
5. ``test_c009_adopted_wait_call_sites_assert_a_deadline_and_a_small_interval`` — every
   ``wait_until`` call in the scope files is an ``assert`` with a named failure message,
   an explicit numeric ``timeout <= 30`` and an ``interval <= 0.2`` when given.
6. ``test_c006_no_inline_polling_loop_in_the_scope_files`` — completion waits go through
   the shared helper; a ``while`` loop over ``time.time()`` is a scan hit.
7. ``test_c004_entry_creation_uses_the_injected_clock`` — every ``pointer_entry`` call in
   ``test_client_metrics.py`` passes ``now=`` (the injected clock), so entry ordering
   never depends on real elapsed time.
8. ``test_c006_a_timeout_is_never_converted_to_skip_or_xfail`` — no ``pytest.skip`` /
   ``pytest.xfail`` call site exists in the scope files (a timeout is a named failure).
"""

from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

import pytest

from fixtures.line_fixtures import wait_until

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / ".specify"
    / "specs"
    / "098-suite-speed-optimizations"
    / "contracts"
    / "event-wait.contract.md"
)

#: The declaration-time copy of the C-001 scope, checked against the clause at guard
#: time — a scope change must revise the clause, never only this guard.
SCOPE = (
    "tests/contract/test_client_metrics.py",
    "tests/integration/test_sdd_loop_efficiency_runner.py",
    "tests/integration/test_session_kill_reattach.py",
    "tests/contract/test_line_envelope_contract.py",
    "tests/contract/test_feedback_probe_cli.py",
    "tests/contract/test_store_state_protocol.py",
)

#: The closed exemption registry (C-003): file -> (per-site anchor, reason text).
EXEMPTIONS = {
    "tests/unit/test_line_registry_engine.py": (
        "time.sleep(2)",
        "the generated flock holder must outlive the 0.2 s lock timeout under test",
    ),
    "tests/unit/test_concurrency_check_engine.py": (
        "time.sleep(0.12)",
        "synthetic task duration that a wall-clock comparison measures",
    ),
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _clause(name: str) -> str:
    """One contract clause's text, from ``- **C-00N**`` to the next clause."""
    text = CONTRACT.read_text(encoding="utf-8")
    match = re.search(
        rf"^- \*\*{name}\*\*.*?(?=^- \*\*C-\d{{3}}\*\*|\Z)", text, re.M | re.S)
    assert match, f"contract clause {name} is missing from {CONTRACT}"
    return match.group(0)


def _paths_in(text: str) -> set:
    return set(re.findall(r"`(tests/[^`]+\.py)`", text))


def _src(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _tree(rel: str) -> ast.AST:
    return ast.parse(_src(rel), filename=rel)


def _parents(tree: ast.AST) -> dict:
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    return parents


def _call_name(node: ast.Call):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _is_sleep_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and func.attr == "sleep":
        return True
    return isinstance(func, ast.Name) and func.id == "sleep"


def _sleep_sites(rel: str) -> list:
    sites = []
    for node in ast.walk(_tree(rel)):
        if isinstance(node, ast.Call) and _is_sleep_call(node):
            sites.append(f"{rel}:{node.lineno}")
    return sorted(set(sites))


def _literal_number(node):
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    return None


def _is_time_clock_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"time", "monotonic"}
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "time"
    )


def _while_loop_polls_the_clock(node: ast.AST) -> bool:
    return isinstance(node, ast.While) and any(
        _is_time_clock_call(child) for child in ast.walk(node))


# --------------------------------------------------------------------------- #
# C-001 / C-002 / C-003 — scope, zero-sleep scan, exemption registry
# --------------------------------------------------------------------------- #

def test_c001_the_scope_is_exactly_the_clause_declared_six_files():
    declared = _paths_in(_clause("C-001"))
    scope = set(SCOPE)
    assert scope == declared, (
        "the guard's scan scope MUST equal the closed set clause C-001 declares; "
        f"guard-only={sorted(scope - declared)} clause-only={sorted(declared - scope)}"
    )
    missing = sorted(rel for rel in scope if not (ROOT / rel).is_file())
    assert not missing, f"C-001: declared scope files are missing: {missing}"


def test_c002_the_scope_files_carry_zero_synchronization_sleep():
    hits = [site for rel in SCOPE for site in _sleep_sites(rel)]
    assert not hits, (
        "C-002: synchronization `time.sleep` MUST be zero in the scope files; "
        "each hit names file and line:\n  " + "\n  ".join(hits)
    )


def test_c003_the_exemption_registry_is_closed_and_per_line():
    c003 = _clause("C-003")
    flat_c003 = " ".join(c003.split())
    declared = _paths_in(c003)
    assert set(EXEMPTIONS) == declared, (
        "C-003: the exemption registry is a closed set; a new exemption requires "
        f"revising the clause. registry-only={sorted(set(EXEMPTIONS) - declared)} "
        f"clause-only={sorted(declared - set(EXEMPTIONS))}"
    )
    problems = []
    for rel, (anchor, reason) in EXEMPTIONS.items():
        if rel in SCOPE:
            problems.append(f"{rel}: a scope file can never be exempted (C-003)")
        if " ".join(reason.split()) not in flat_c003:
            problems.append(f"{rel}: reason text is not the clause's wording: {reason!r}")
        text = _src(rel)
        if anchor not in text:
            problems.append(
                f"{rel}: the registered site {anchor!r} is gone — a stale exemption "
                "MUST NOT linger (C-003)")
    assert not problems, "C-003 exemption registry:\n  " + "\n  ".join(problems)


# --------------------------------------------------------------------------- #
# C-006 / C-007 / C-009 — helper defaults and adopted call sites
# --------------------------------------------------------------------------- #

def test_c006_c007_the_helper_defaults_are_thirty_seconds_and_a_small_interval():
    signature = inspect.signature(wait_until)
    timeout = signature.parameters["timeout"].default
    interval = signature.parameters["interval"].default
    assert float(timeout) == 30.0, (
        "C-006/C-007: wait_until's default deadline is the enacted 30 s, "
        f"got {timeout!r}")
    assert float(interval) <= 0.2, (
        f"C-007: the polling interval MUST be <= 0.2 s, got {interval!r}")


def test_c009_adopted_wait_call_sites_assert_a_deadline_and_a_small_interval():
    problems = []
    for rel in SCOPE:
        tree = _tree(rel)
        parents = _parents(tree)
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and _call_name(node) == "wait_until"):
                continue
            site = f"{rel}:{node.lineno}"
            parent = parents.get(node)
            if not (isinstance(parent, ast.Assert) and parent.test is node):
                problems.append(
                    f"{site}: the wait result MUST be asserted at the call site (C-006)")
                continue
            if parent.msg is None:
                problems.append(
                    f"{site}: the assert MUST carry a named failure message (C-006)")
            keywords = {kw.arg: kw.value for kw in node.keywords}
            if "timeout" not in keywords:
                problems.append(
                    f"{site}: an explicit numeric timeout keyword is required (C-007)")
            else:
                timeout = _literal_number(keywords["timeout"])
                if timeout is None:
                    problems.append(
                        f"{site}: the deadline MUST be a literal number (C-007)")
                elif timeout > 30:
                    problems.append(
                        f"{site}: deadline {timeout}s exceeds the 30 s ceiling "
                        "without a recorded reason (C-007)")
            if "interval" in keywords:
                interval = _literal_number(keywords["interval"])
                if interval is None or interval > 0.2:
                    problems.append(
                        f"{site}: interval MUST be a literal <= 0.2 s (C-007)")
    assert not problems, "C-009 adopted wait call sites:\n  " + "\n  ".join(problems)


def test_c006_no_inline_polling_loop_in_the_scope_files():
    hits = []
    for rel in SCOPE:
        for node in ast.walk(_tree(rel)):
            if _while_loop_polls_the_clock(node):
                hits.append(f"{rel}:{node.lineno}")
    assert not hits, (
        "C-006: completion waits go through the shared wait_until helper; an inline "
        "while-loop over time.time() is a scan hit:\n  " + "\n  ".join(hits))


def test_c006_a_timeout_is_never_converted_to_skip_or_xfail():
    hits = []
    for rel in SCOPE:
        for node in ast.walk(_tree(rel)):
            if isinstance(node, ast.Call) and _call_name(node) in {"skip", "xfail"}:
                hits.append(f"{rel}:{node.lineno}")
    assert not hits, (
        "C-006/FR-021: a timeout MUST surface as a named failure, never as "
        "skip/xfail:\n  " + "\n  ".join(hits))


# --------------------------------------------------------------------------- #
# C-004 — entry ordering comes from the injected clock
# --------------------------------------------------------------------------- #

def test_c004_entry_creation_uses_the_injected_clock():
    rel = "tests/contract/test_client_metrics.py"
    problems = []
    for node in ast.walk(_tree(rel)):
        if isinstance(node, ast.Call) and _call_name(node) == "pointer_entry":
            if "now" not in {kw.arg for kw in node.keywords}:
                problems.append(f"{rel}:{node.lineno}")
    assert not problems, (
        "C-004: every entry-creating pointer_entry call MUST carry the injected clock "
        "(`now=`), so ordering never depends on real elapsed time; missing at:\n  "
        + "\n  ".join(problems)
    )
